import sys
import os
import json
import re
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS

# Import agent directly
from agents.company_analyst import company_agent

app = Flask(__name__)
CORS(app)

# Simple in-memory cache (will reset when server restarts)
analysis_cache = {}


def parse_agent_response(response_text):
    """Parse agent response to extract JSON metadata and analysis"""
    try:
        # Extract JSON block
        json_match = re.search(r'```json\s*(\{[^`]+\})\s*```', response_text, re.DOTALL)
        
        if not json_match:
            print("⚠️ No JSON found, using fallback")
            return {
                'official_name': 'Unknown Company',
                'ticker': 'UNKNOWN',
                'score': 75,
                'grade': 'B+',
                'financialData': None,
                'analysis_text': response_text
            }
        
        metadata = json.loads(json_match.group(1))
        analysis_start = json_match.end()
        analysis_text = response_text[analysis_start:].strip()
        
        return {
            'official_name': metadata.get('official_name', 'Unknown'),
            'ticker': metadata.get('ticker', 'UNKNOWN'),
            'score': int(metadata.get('score', 75)),
            'grade': metadata.get('grade', 'B+'),
            'financialData': metadata.get('financialData'),
            'analysis_text': analysis_text
        }
        
    except Exception as e:
        print(f"Parse error: {e}")
        return {
            'official_name': 'Unknown Company',
            'ticker': 'UNKNOWN',
            'score': 75,
            'grade': 'B+',
            'financialData': None,
            'analysis_text': response_text
        }


@app.route('/analyze', methods=['POST'])
def analyze():
    """POST /analyze - Main analysis endpoint"""
    try:
        data = request.get_json()
        company_input = data.get('company', '').strip()
        
        if not company_input:
            return jsonify({"error": "Company name required"}), 400
        
        print(f"\n{'='*60}")
        print(f"📥 Analyzing: {company_input}")
        print(f"{'='*60}")
        
        # Generate cache key from user input (normalized)
        cache_key = company_input.lower().replace(' ', '_')
        
        # Check cache first
        if cache_key in analysis_cache:
            print("✓ Cache HIT!")
            cached = analysis_cache[cache_key]
            cached['cached'] = True
            return jsonify(cached), 200
        
        # Call agent
        print("✗ Cache MISS - Calling agent...")
        agent_result = company_agent(f"Analyze {company_input} for job seekers")
        response_text = agent_result.content if hasattr(agent_result, "content") else str(agent_result)
        
        # Check if agent couldn't identify the company
        if "could not identify" in response_text.lower() or "cannot identify" in response_text.lower():
            print("❌ Company not found by agent")
            return jsonify({"error": f"Could not identify company '{company_input}'. Please check the spelling and try again."}), 404
        
        # Parse response
        parsed = parse_agent_response(response_text)
        
        # Additional check: if ticker is UNKNOWN, don't proceed
        if parsed['ticker'] == 'UNKNOWN' or parsed['official_name'] == 'Unknown Company':
            print("❌ Company resolution failed")
            return jsonify({"error": f"Could not identify company '{company_input}'. Please check the spelling and try again."}), 404
        
        print(f"✅ Parsed: {parsed['official_name']} ({parsed['ticker']})")
        print(f"📊 Financial Data: {'Yes' if parsed['financialData'] else 'No'}")
        
        # Generate storage ticker based on company type
        if parsed['ticker'] and parsed['ticker'] not in ['PRIVATE', 'UNKNOWN', 'N/A']:
            storage_ticker = parsed['ticker'].upper()
        else:
            normalized = parsed['official_name'].upper()
            normalized = re.sub(r'[^A-Z0-9\s]', '', normalized)  # Keep only letters, numbers, spaces
            normalized = re.sub(r'\s+', '_', normalized)          # Spaces to underscores
            normalized = re.sub(r'_(INC|LLC|LTD|CORP|CORPORATION|COMPANY)$', '', normalized)
            storage_ticker = normalized.strip('_')
        
        print(f"🔑 Storage ticker: {storage_ticker}")
        
        # Build response
        result = {
            "cached": False,
            "company": parsed['official_name'],
            "ticker": storage_ticker,
            "display_ticker": parsed['ticker'] if parsed['ticker'] != 'PRIVATE' else 'Not Publicly Traded',
            "score": parsed['score'],
            "grade": parsed['grade'],
            "financialData": parsed['financialData'],
            "timestamp": datetime.now().isoformat(),
            "detailedAnalysis": parsed['analysis_text']
        }
        
        # Cache it
        analysis_cache[cache_key] = result.copy()
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """GET /dashboard - Return cached analyses"""
    try:
        companies = []
        for key, data in analysis_cache.items():
            companies.append({
                'ticker': data['ticker'],
                'company': data['company'],
                'score': data['score'],
                'grade': data['grade'],
                'timestamp': data['timestamp']
            })
        
        # Sort by most recent
        companies.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify(companies[:20]), 200
        
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/report', methods=['GET'])
def report():
    """GET /report?ticker=MSFT - Get specific report"""
    try:
        ticker = request.args.get('ticker', '').upper()
        
        if not ticker:
            return jsonify({"error": "ticker parameter required"}), 400
        
        # Search cache for matching ticker
        for key, data in analysis_cache.items():
            if data.get('ticker', '').upper() == ticker:
                return jsonify(data), 200
        
        return jsonify({"error": f"Company {ticker} not found"}), 404
        
    except Exception as e:
        print(f"❌ Report error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "cached_companies": len(analysis_cache)
    }), 200


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Local Backend Server (No Lambda/DynamoDB)")
    print("="*60)
    print("📡 Backend API: http://localhost:5000")
    print("🌐 CORS enabled for: http://localhost:3000")
    print("\nEndpoints:")
    print("  POST   /analyze")
    print("  GET    /dashboard")
    print("  GET    /report?ticker=MSFT")
    print("  GET    /health")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')