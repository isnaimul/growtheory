import json
import re
import traceback
from agents.company_analyst import company_agent

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])
        company = body.get('company')
        
        print(f"Analyzing {company}...")
        
        # Call agent
        result = company_agent(f"Analyze {company}")
        response_text = result.content if hasattr(result, 'content') else str(result)
        
        # Extract score
        score_match = re.search(r'(\d+)/100', response_text)
        score = int(score_match.group(1)) if score_match else 75
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                "company": company,
                "score": score,
                "hiringVelocity": 8,
                "stabilityScore": 9,
                "layoffRisk": 10,
                "verdict": "Strong company with excellent financials",
                "timestamp": "2024-10-15T10:00:00Z",
                "detailedAnalysis": response_text
            })
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }