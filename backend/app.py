from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import traceback
from agents.company_analyst import company_agent  # No "backend." prefix

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        company = data.get('company')
        
        print(f"Analyzing {company}...")
        
        # Call agent
        result = company_agent(f"Analyze {company}")
        response_text = result.content if hasattr(result, 'content') else str(result)
        
        # Extract score
        score_match = re.search(r'(\d+)/100', response_text)
        score = int(score_match.group(1)) if score_match else 75
        
        print(f"Score extracted: {score}")
        
        return jsonify({
            "company": company,
            "score": score,
            "hiringVelocity": 8,
            "stabilityScore": 9,
            "layoffRisk": 10,
            "verdict": "Strong company with excellent financials",
            "timestamp": "2024-10-15T10:00:00Z",
            "detailedAnalysis": response_text
        })
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000, threaded=True)