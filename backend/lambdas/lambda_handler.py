import json
import re
import traceback
import boto3
import os
import time
import random
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
    path = event.get("path", "/analyze")

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


def handle_analyze(event, context):
    """POST /analyze - Main search endpoint with caching"""

    try:
        body = json.loads(event["body"])
        company = body.get("company")
        ticker = body.get(
            "ticker", company
        )  # Ticker optional, defaults to company name

        print(f"Analyzing: {company} ({ticker})")

        # Get cached or fresh analysis
        result = get_or_create_analysis(company, ticker)

        return success_response(result)

    except Exception as e:
        print(f"Analyze error: {str(e)}")
        traceback.print_exc()
        return error_response(500, str(e))


def handle_dashboard(event, context):
    """GET /dashboard?page=1 - Return paginated cached companies"""
    
    try:
        # Get page number from query params (default to 1)
        params = event.get('queryStringParameters', {}) or {}
        page = int(params.get('page', 1))
        per_page = 6
        
        print(f"Fetching dashboard data - page {page}")

        response = cache_table.scan()
        all_companies = response.get('Items', [])
        
        # Convert and sort
        companies = []
        for item in all_companies:
            companies.append({
                'ticker': item['ticker'],
                'company': item['company'],
                'score': int(item.get('score', 75)),
                'grade': item.get('grade', 'B'),
                'timestamp': item['timestamp']
            })
        
        companies.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Calculate pagination
        total_companies = len(companies)
        total_pages = max(1, (total_companies + per_page - 1) // per_page)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        page_companies = companies[start_idx:end_idx]

        print(f"Returning {len(page_companies)} companies (page {page}/{total_pages})")

        return success_response({
            'companies': page_companies,
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'total_companies': total_companies,
                'per_page': per_page
            }
        })

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


def get_or_create_analysis(company, ticker):
    """Core caching logic - check cache first, then run agent if needed"""

    cache_key = ticker.upper()

    # Try to get from cache
    try:
        response = cache_table.get_item(Key={"ticker": cache_key})

        if "Item" in response:
            cached_data = response["Item"]
            cached_at = datetime.fromisoformat(cached_data["timestamp"])
            age_hours = (datetime.now() - cached_at).total_seconds() / 3600

            # Check if cache is still fresh
            if age_hours < CACHE_DURATION_HOURS:
                print(f"✓ Cache HIT - {age_hours:.1f} hours old")

                # Simulate AI thinking for UX (10-15 seconds for cached results)
                time.sleep(random.uniform(10, 15))

                # Return cached data with metadata
                return decimal_to_int(
                    {
                        "cached": True,
                        "cache_age_hours": round(age_hours, 1),
                        "company": cached_data["company"],
                        "ticker": cached_data["ticker"],
                        "score": cached_data["score"],
                        "grade": cached_data["grade"],
                        "timestamp": cached_data["timestamp"],
                        "full_analysis": cached_data["full_analysis"],
                    }
                )
            else:
                print(f"Cache EXPIRED - {age_hours:.1f} hours old, fetching fresh data")

    except Exception as e:
        print(f"Cache lookup failed: {e}")

    # Cache miss or expired - run fresh analysis
    print(f"✗ Cache MISS - Running fresh analysis for {company}...")

    # Call agent
    agent_result = company_agent(f"Analyze {company} ({ticker}) for job seekers")
    response_text = (
        agent_result.content if hasattr(agent_result, "content") else str(agent_result)
    )

    # Extract score and calculate grade
    score = extract_score(response_text)
    grade = calculate_grade(score)

    # Prepare cache item
    timestamp = datetime.now().isoformat()
    expires_at = int(
        (datetime.now() + timedelta(hours=CACHE_DURATION_HOURS)).timestamp()
    )

    cache_item = {
        "ticker": cache_key,
        "company": company,
        "timestamp": timestamp,
        "expiresAt": expires_at,
        "score": score,
        "grade": grade,
        "full_analysis": response_text,
    }

    # Store in cache
    try:
        cache_table.put_item(Item=cache_item)
        print(f"✓ Cached result for {cache_key}")
    except Exception as e:
        print(f"Failed to cache: {e}")
        # Continue anyway - user still gets their result

    # Return fresh analysis
    return {
        "cached": False,
        "company": company,
        "ticker": cache_key,
        "score": score,
        "grade": grade,
        "timestamp": timestamp,
        "full_analysis": response_text,
    }


def extract_score(text):
    """Extract score from agent response"""

    # Try to find X/10 pattern
    match = re.search(r"(\d+(?:\.\d+)?)/10", text)
    if match:
        return int(float(match.group(1)) * 10)  # Convert to 0-100 scale

    # Try to find X/100 pattern
    match = re.search(r"(\d+)/100", text)
    if match:
        return int(match.group(1))

    # Default fallback
    print("Warning: Could not extract score, using default 75")
    return 75


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
