import json

def lambda_handler(event, context):
    """
    This Lambda is called by Bedrock Agent to get company basics.
    
    Bedrock Agent sends event in this format:
    {
        "messageVersion": "1.0",
        "agent": {...},
        "actionGroup": "company-basics",
        "function": "getCompanyBasics",
        "parameters": [
            {"name": "company_name", "type": "string", "value": "Microsoft"}
        ]
    }
    """
    
    print("Event received:", json.dumps(event))  
    
    # Extract parameters from Bedrock Agent format
    parameters = event.get('parameters', [])
    company_name = None
    
    for param in parameters:
        if param.get('name') == 'company_name':
            company_name = param.get('value')
            break
    
    # Mock company data 
    company_data = {
        "name": company_name or "Unknown Company",
        "industry": "Technology",
        "employee_count": "100,000+",
        "headquarters": "Redmond, WA",
        "founded_year": 1975,
        "health_score": 85,
        "stock_trend": "up",
        "hiring_status": "actively_hiring",
        "glassdoor_rating": 4.2,
        "recent_news_sentiment": "positive"
    }
    
    # Bedrock Agent response
    response = {
        'messageVersion': '1.0',
        'response': {
            'actionGroup': event.get('actionGroup', ''),
            'function': event.get('function', ''),
            'functionResponse': {
                'responseBody': {
                    'TEXT': {
                        'body': json.dumps(company_data)
                    }
                }
            }
        }
    }
    
    print("Response:", json.dumps(response))  
    return response