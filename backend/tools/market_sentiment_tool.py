"""Market Sentiment Tool - Ultra Minimal"""

from strands.tools import tool
import requests
import os

API_KEY = os.environ.get('ALPHAVANTAGE_API_KEY', 'UCMBE27OTHKNVEKC')
URL = "https://www.alphavantage.co/query"


@tool
def analyze_market_sentiment(ticker_symbol: str) -> dict:
    """Analyzes market sentiment and news for a stock."""
    try:
        # Get quote
        quote = requests.get(URL, params={
            'function': 'GLOBAL_QUOTE', 'symbol': ticker_symbol, 'apikey': API_KEY
        }, timeout=10).json().get('Global Quote', {})
        
        # Get news
        news = requests.get(URL, params={
            'function': 'NEWS_SENTIMENT', 'tickers': ticker_symbol, 
            'apikey': API_KEY, 'limit': 10
        }, timeout=10).json().get('feed', [])
        
        # Calculate sentiment
        sentiments = [
            float(ts.get('ticker_sentiment_score', 0))
            for article in news[:10]
            for ts in article.get('ticker_sentiment', [])
            if float(ts.get('relevance_score', 0)) > 0.3
        ]
        
        avg = sum(sentiments) / len(sentiments) if sentiments else 0.0
        label = 'bullish' if avg > 0.15 else 'bearish' if avg < -0.15 else 'neutral'
        
        # Extract themes
        themes = list(set(
            topic.get('topic', '')
            for article in news
            for topic in article.get('topics', [])
            if topic.get('topic')
        ))[:5]
        
        # Generate signals
        change = float(quote.get('10. change percent', '0').replace('%', '').replace('+', ''))
        signals = []
        if change > 3: signals.append('strong_upward_momentum')
        if change < -3: signals.append('significant_decline')
        if avg > 0.2: signals.append('positive_news_sentiment')
        if avg < -0.2: signals.append('negative_news_sentiment')
        
        return {
            "ticker": ticker_symbol,
            "stock_data": {
                'price': float(quote.get('05. price', 0)),
                'change_percent': quote.get('10. change percent', '0%'),
                'volume': int(quote.get('06. volume', 0))
            },
            "news_sentiment": {
                'overall_sentiment': label,
                'sentiment_score': round(avg, 3),
                'article_count': len(news),
                'key_themes': themes
            },
            "market_signals": signals
        }
    except Exception as e:
        return {"ticker": ticker_symbol, "error": str(e)}