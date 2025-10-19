import json
import re
import traceback
import boto3
import os
import time
import random
import hashlib
from datetime import datetime, timedelta
from decimal import Decimal
from agents.company_analyst import company_agent

TABLE_NAME = os.environ.get("COMPANY_CACHE_TABLE_NAME")

if not TABLE_NAME:
    raise EnvironmentError("COMPANY_CACHE_TABLE_NAME environment variable not set. Cannot initialize DynamoDB.")

# DynamoDB setup
dynamodb = boto3.resource("dynamodb")
cache_table = dynamodb.Table(TABLE_NAME)

CACHE_DURATION_HOURS = 24


def lambda_handler(event, context):
    """Main Lambda handler - routes to appropriate endpoint"""

    # Determine which endpoint was called
    http_method = event.get("httpMethod", "POST")
    path = event.get("path", "/api/analyze")

    print(f"Request: {http_method} {path}")

    try:
        # Route to appropriate handler
        if path == "/analyze" and http_method == "POST":
            return handle_analyze(event, context)

        elif path == "/dashboard" and http_method == "GET":
            return handle_dashboard(event, context)

        elif path == "/report" and http_method == "GET":
            return handle_get_report(event, context)

        else:
            return error_response(404, "Endpoint not found")

    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return error_response(500, str(e))


def decimal_to_int(obj):
    """Convert DynamoDB Decimal types to int for JSON serialization"""
    if isinstance(obj, list):
        return [decimal_to_int(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: decimal_to_int(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    else:
        return obj


def parse_agent_response(response_text):
    """
    Parse the agent's structured response to extract metadata and analysis
    
    Returns:
        dict with keys: official_name, ticker, score, grade, financialData, analysis_text
    """
    try:
        # Extract JSON block from response
        json_match = re.search(r'```json\s*(\{[^`]+\})\s*```', response_text, re.DOTALL)
        
        if not json_match:
            print("⚠️ No JSON metadata found in response, attempting fallback parsing")
            return fallback_parse(response_text)
        
        # Parse the JSON metadata
        metadata = json.loads(json_match.group(1))
        
        # Extract the analysis text (everything after the JSON block)
        analysis_start = json_match.end()
        analysis_text = response_text[analysis_start:].strip()
        
        # Validate required fields
        required_fields = ['official_name', 'ticker', 'score', 'grade']
        if not all(field in metadata for field in required_fields):
            print(f"⚠️ Missing required fields in metadata: {metadata}")
            return fallback_parse(response_text)
        
        return {
            'official_name': metadata['official_name'],
            'ticker': metadata['ticker'],
            'score': int(metadata['score']),
            'grade': metadata['grade'],
            'financialData': metadata.get('financialData'),  # NEW: Extract financial data
            'analysis_text': analysis_text
        }
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return fallback_parse(response_text)
    except Exception as e:
        print(f"❌ Response parsing error: {e}")
        return fallback_parse(response_text)


def fallback_parse(response_text):
    """
    Fallback parsing if structured JSON is not found
    Uses regex to extract from markdown format
    """
    print("Using fallback parsing method")
    
    # Try to extract from "Analyzing [NAME] ([TICKER])" pattern
    analyzing_match = re.search(r'Analyzing\s+(.+?)\s+\(([^)]+)\)', response_text)
    
    if analyzing_match:
        official_name = analyzing_match.group(1).strip()
        ticker_raw = analyzing_match.group(2).strip()
        
        # Handle "Not Publicly Traded" case
        if "not publicly traded" in ticker_raw.lower():
            ticker = "PRIVATE"
        else:
            ticker = ticker_raw
    else:
        # Ultimate fallback
        official_name = "Unknown Company"
        ticker = "UNKNOWN"
    
    # Extract score from "Overall Assessment: X/10" pattern
    score_match = re.search(r'Overall Assessment:\s*(\d+(?:\.\d+)?)/10', response_text)
    if score_match:
        score = int(float(score_match.group(1)) * 10)  # Convert to 0-100 scale
    else:
        score = 75  # Default
    
    # Calculate grade
    grade = calculate_grade(score)
    
    return {
        'official_name': official_name,
        'ticker': ticker,
        'score': score,
        'grade': grade,
        'financialData': None,
        'analysis_text': response_text
    }


def generate_cache_key(ticker, official_name):
    """
    Generate cache key based on company type:
    - Public companies: Use ticker symbol (e.g., "MSFT")
    - Private companies: Use normalized company name (e.g., "MCKINSEY")
    
    Args:
        ticker: The ticker from resolver ("MSFT", "PRIVATE", or None)
        official_name: Official company name
        
    Returns:
        Cache key string for DynamoDB
    """
    if ticker and ticker not in ["PRIVATE", "UNKNOWN", "N/A", None]:
        # Public company - use ticker symbol
        return ticker.upper()
    else:
        # Private/Unknown company - use normalized company name
        # Remove ALL special characters to make URL-safe
        normalized = official_name.upper()
        normalized = re.sub(r'[^A-Z0-9\s]', '', normalized)  # Keep only alphanumeric and spaces
        normalized = re.sub(r'\s+', '_', normalized)          # Spaces to underscores
        normalized = re.sub(r'_(INC|LLC|LTD|CORP|CORPORATION|COMPANY)$', '', normalized)  # Remove suffixes
        return normalized.strip('_')


def handle_analyze(event, context):
    """POST /analyze - Main search endpoint with caching"""

    try:
        body = json.loads(event["body"])
        user_input = body.get("company", "").strip()

        if not user_input:
            return error_response(400, "Company name required")

        print(f"📥 Analyzing request for: {user_input}")

        # Call the agent (it will use resolver tool internally)
        result = get_or_create_analysis(user_input)
        
        # Check if result is an error response
        if isinstance(result, dict) and result.get('statusCode'):
            return result

        return success_response(result)

    except Exception as e:
        print(f"Analyze error: {str(e)}")
        traceback.print_exc()
        return error_response(500, str(e))


def handle_dashboard(event, context):
    """GET /dashboard - Return all cached companies"""

    try:
        print("Fetching dashboard data...")

        response = cache_table.scan()

        companies = []
        for item in response.get('Items', []):
            # Skip unknown/error entries
            if item['ticker'].startswith('UNKNOWN'):
                continue
                
            companies.append({
                'ticker': item['ticker'],
                'company': item.get('official_name', item['company']),
                'score': int(item.get('score', 75)),
                'grade': item.get('grade', 'B'),
                'timestamp': item['timestamp']
            })

        # Sort by most recent first
        companies.sort(key=lambda x: x["timestamp"], reverse=True)

        print(f"Returning {len(companies)} cached companies")

        return success_response(companies[:20])

    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        traceback.print_exc()
        return error_response(500, str(e))


def handle_get_report(event, context):
    """GET /report?ticker=AMZN - Get specific cached report"""

    try:
        params = event.get('queryStringParameters', {}) or {}
        ticker = params.get('ticker')
        
        if not ticker:
            return error_response(400, 'ticker parameter required')
        
        print(f"Fetching report for {ticker}")
        
        response = cache_table.get_item(Key={'ticker': ticker.upper()})
        
        if 'Item' not in response:
            return error_response(404, f'Company {ticker} not found in cache')
        
        # Convert Decimals before returning
        return success_response(decimal_to_int(response['Item']))

    except Exception as e:
        print(f"Get report error: {str(e)}")
        traceback.print_exc()
        return error_response(500, str(e))


def get_or_create_analysis(user_input):
    """
    Main analysis logic - uses agent with resolver tool
    Agent handles company resolution internally via tools
    """
    
    print(f"🔄 Processing: {user_input}")
    
    # Call the agent - it will use resolve_company tool first
    try:
        agent_result = company_agent(f"Analyze {user_input} for job seekers")
        response_text = (
            agent_result.content if hasattr(agent_result, "content") else str(agent_result)
        )
    except Exception as e:
        print(f"❌ Agent call failed: {e}")
        traceback.print_exc()
        return error_response(500, f"Analysis failed: {str(e)}")
    
    # Check if agent couldn't identify the company
    if "could not identify" in response_text.lower() or "cannot identify" in response_text.lower():
        print("❌ Company not found by agent")
        return error_response(404, f"Could not identify company '{user_input}'. Please check the spelling and try again.")
    
    # Parse the structured response
    parsed = parse_agent_response(response_text)
    
    official_name = parsed['official_name']
    ticker = parsed['ticker']
    score = parsed['score']
    grade = parsed['grade']
    financial_data = parsed.get('financialData')  # NEW
    analysis_text = parsed['analysis_text']
    
    # Additional check: if ticker is UNKNOWN, don't proceed
    if ticker == 'UNKNOWN' or official_name == 'Unknown Company':
        print("❌ Company resolution failed")
        return error_response(404, f"Could not identify company '{user_input}'. Please check the spelling and try again.")
    
    print(f"✅ Parsed: {official_name} ({ticker}) - Score: {score}")
    print(f"📊 Financial Data: {'Yes' if financial_data else 'No'}")
    
    # Generate cache key
    cache_key = generate_cache_key(ticker, official_name)
    
    print(f"🔑 Cache key: {cache_key}")
    
    # Check cache
    try:
        cache_response = cache_table.get_item(Key={"ticker": cache_key})
        
        if "Item" in cache_response:
            cached_data = cache_response["Item"]
            cached_at = datetime.fromisoformat(cached_data["timestamp"])
            age_hours = (datetime.now() - cached_at).total_seconds() / 3600
            
            if age_hours < CACHE_DURATION_HOURS:
                print(f"✓ Cache HIT - {age_hours:.1f} hours old")
                
                # Simulate AI thinking for UX
                time.sleep(random.uniform(10, 15))
                
                return decimal_to_int({
                    "cached": True,
                    "cache_age_hours": round(age_hours, 1),
                    "company": cached_data.get("official_name", cached_data["company"]),
                    "ticker": cache_key,
                    "display_ticker": ticker if ticker != 'PRIVATE' else 'Not Publicly Traded',
                    "score": cached_data["score"],
                    "grade": cached_data["grade"],
                    "financialData": cached_data.get("financialData"),  # NEW
                    "timestamp": cached_data["timestamp"],
                    "detailedAnalysis": cached_data["full_analysis"],
                })
            else:
                print(f"Cache EXPIRED - {age_hours:.1f} hours old")
    
    except Exception as e:
        print(f"Cache lookup failed: {e}")
    
    # No cache or expired - return fresh analysis
    print(f"✗ Cache MISS - Returning fresh analysis")
    
    # Prepare cache item
    timestamp = datetime.now().isoformat()
    expires_at = int(
        (datetime.now() + timedelta(hours=CACHE_DURATION_HOURS)).timestamp()
    )
    
    cache_item = {
        "ticker": cache_key,
        "company": official_name,
        "official_name": official_name,
        "display_ticker": ticker,
        "timestamp": timestamp,
        "expiresAt": expires_at,
        "score": score,
        "grade": grade,
        "financialData": financial_data,  # NEW
        "full_analysis": analysis_text,
    }
    
    # Store in cache
    try:
        cache_table.put_item(Item=cache_item)
        print(f"✓ Cached result for {cache_key}")
    except Exception as e:
        print(f"Failed to cache: {e}")
    
    # Return fresh analysis
    return {
        "cached": False,
        "company": official_name,
        "ticker": cache_key,
        "display_ticker": ticker if ticker != 'PRIVATE' else 'Not Publicly Traded',
        "score": score,
        "grade": grade,
        "financialData": financial_data,  # NEW
        "timestamp": timestamp,
        "detailedAnalysis": analysis_text,
    }


def calculate_grade(score):
    """Convert 0-100 score to letter grade"""
    if score >= 90:
        return "A+"
    if score >= 85:
        return "A"
    if score >= 80:
        return "A-"
    if score >= 75:
        return "B+"
    if score >= 70:
        return "B"
    if score >= 65:
        return "B-"
    if score >= 60:
        return "C+"
    if score >= 55:
        return "C"
    if score >= 50:
        return "C-"
    return "D"


def success_response(data):
    """Standard success response with CORS headers"""
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Content-Type": "application/json",
        },
        "body": json.dumps(data),
    }


def error_response(status_code, message):
    """Standard error response with CORS headers"""
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Content-Type": "application/json",
        },
        "body": json.dumps({"error": message}),
    }
