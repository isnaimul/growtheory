"""
Lambda Function: alphavantage-news
Purpose: Stock data + market sentiment via AlphaVantage API + Amazon Nova
~80 lines of core logic
"""

import json
import logging
import requests
import boto3
from datetime import datetime, timedelta
from typing import Dict, List

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize Bedrock client for Nova
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

# AlphaVantage API configuration
ALPHAVANTAGE_API_KEY = "YOUR_ALPHAVANTAGE_KEY"  # Replace with your API key
ALPHAVANTAGE_BASE_URL = "https://www.alphavantage.co/query"


def fetch_stock_data(ticker: str) -> Dict:
    """Fetch stock price data from AlphaVantage"""
    try:
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': ticker,
            'apikey': ALPHAVANTAGE_API_KEY
        }
        
        response = requests.get(ALPHAVANTAGE_BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            quote = data.get('Global Quote', {})
            
            return {
                'price': float(quote.get('05. price', 0)),
                'change_percent': quote.get('10. change percent', '0%'),
                'volume': int(quote.get('06. volume', 0))
            }
        
        return {'price': 0, 'change_percent': '0%', 'volume': 0}
        
    except Exception as e:
        logger.error(f"AlphaVantage stock data error: {str(e)}")
        return {'price': 0, 'change_percent': '0%', 'volume': 0}


def fetch_news_sentiment(ticker: str) -> List[Dict]:
    """Fetch news articles and sentiment from AlphaVantage"""
    try:
        params = {
            'function': 'NEWS_SENTIMENT',
            'tickers': ticker,
            'apikey': ALPHAVANTAGE_API_KEY,
            'limit': 10
        }
        
        response = requests.get(ALPHAVANTAGE_BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('feed', [])
        
        return []
        
    except Exception as e:
        logger.error(f"AlphaVantage news error: {str(e)}")
        return []


def analyze_sentiment_with_nova(news_articles: List[Dict], ticker: str) -> Dict:
    """Use Amazon Nova to analyze news sentiment"""
    try:
        # Prepare news summary
        news_summary = "\n\n".join([
            f"Title: {article.get('title', 'N/A')}\nSummary: {article.get('summary', 'N/A')}"
            for article in news_articles[:5]  # Top 5 articles
        ])
        
        prompt = f"""Analyze the sentiment of recent news about {ticker}:

{news_summary}

Provide:
1. Overall sentiment score (-1.0 to 1.0, where -1 is very negative, 0 is neutral, 1 is very positive)
2. Price trend assessment (Bullish/Neutral/Bearish)
3. Key themes from the news (3-4 items)

Respond in JSON format:
{{
    "sentiment_score": 0.0,
    "price_trend": "Bullish/Neutral/Bearish",
    "key_themes": ["theme1", "theme2", "theme3"],
    "news_count": 0
}}
"""
        
        # Call Amazon Nova
        response = bedrock_runtime.invoke_model(
            modelId='amazon.nova-micro-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "max_new_tokens": 500,
                    "temperature": 0.3
                }
            })
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        nova_output = response_body['output']['message']['content'][0]['text']
        
        # Extract JSON
        import re
        json_match = re.search(r'\{.*\}', nova_output, re.DOTALL)
        if json_match:
            sentiment = json.loads(json_match.group())
            sentiment['news_count'] = len(news_articles)
            return sentiment
        
        raise ValueError("No valid JSON in Nova response")
        
    except Exception as e:
        logger.error(f"Nova sentiment analysis error: {str(e)}")
        return generate_fallback_sentiment(news_articles)


def generate_fallback_sentiment(news_articles: List[Dict]) -> Dict:
    """Generate fallback sentiment when Nova unavailable"""
    
    # Simple sentiment based on article count and basic keywords
    positive_keywords = ['growth', 'profit', 'success', 'innovation', 'expansion']
    negative_keywords = ['loss', 'decline', 'layoff', 'investigation', 'lawsuit']
    
    positive_count = 0
    negative_count = 0
    
    for article in news_articles[:5]:
        text = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
        positive_count += sum(1 for word in positive_keywords if word in text)
        negative_count += sum(1 for word in negative_keywords if word in text)
    
    # Calculate sentiment score
    if positive_count + negative_count > 0:
        sentiment_score = (positive_count - negative_count) / (positive_count + negative_count)
    else:
        sentiment_score = 0.0
    
    # Determine trend
    if sentiment_score > 0.3:
        trend = "Bullish"
    elif sentiment_score < -0.3:
        trend = "Bearish"
    else:
        trend = "Neutral"
    
    return {
        "sentiment_score": round(sentiment_score, 2),
        "price_trend": trend,
        "key_themes": ["Market performance", "Company developments", "Industry trends"],
        "news_count": len(news_articles),
        "source": "Fallback Analysis"
    }


def get_market_sentiment(ticker: str) -> Dict:
    """Main function to get market sentiment"""
    
    if ticker == "PRIVATE":
        return {
            "sentiment_score": 0.0,
            "price_trend": "N/A",
            "key_themes": ["Private company - market data not available"],
            "news_count": 0,
            "error": "Private company"
        }
    
    # Fetch stock data
    stock_data = fetch_stock_data(ticker)
    
    # Fetch news
    news_articles = fetch_news_sentiment(ticker)
    
    # Analyze sentiment with Nova
    sentiment_data = analyze_sentiment_with_nova(news_articles, ticker)
    
    # Combine results
    result = {
        **stock_data,
        **sentiment_data,
        'analysis_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    return result


def lambda_handler(event, context):
    """AWS Lambda handler"""
    try:
        # Parse input
        body = json.loads(event.get('body', '{}'))
        ticker = body.get('ticker', '')
        
        logger.info(f"Analyzing market sentiment for: {ticker}")
        
        # Get market sentiment
        result = get_market_sentiment(ticker)
        
        logger.info(f"Market sentiment result: {result}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        logger.error(f"Error in market sentiment analyzer: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }


# For local testing
if __name__ == "__main__":
    test_tickers = ["TSLA", "AAPL", "MSFT"]
    
    for ticker in test_tickers:
        print(f"\n{'='*50}")
        print(f"Ticker: {ticker}")
        result = get_market_sentiment(ticker)
        print(json.dumps(result, indent=2))
