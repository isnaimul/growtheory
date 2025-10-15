from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.company_analyst import company_agent

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    company = data.get('company')
    
    result = company_agent(f"Analyze {company}")
    
    if hasattr(result, 'content'):
        response_text = result.content
    else:
        response_text = str(result) 

    return jsonify({
        "company": company,
        "raw_response": response_text
    })

if __name__ == '__main__':
    app.run(debug=True, port=3000)