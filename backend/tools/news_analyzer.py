from strands.tools import tool
from newsapi import NewsApiClient
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
ALPHA_URL = "https://www.alphavantage.co/query"


@tool
def analyze_company_news(company_name, ticker_symbol):
    """
    Analyzes recent news and market sentiment about a company using multiple sources.
    
    Args:
        company_name (str): Company name (e.g., "Microsoft", "Amazon")
        ticker_symbol (str): Stock ticker (e.g., "MSFT", "AMZN")
    
    Returns:
        dict: Comprehensive news and sentiment analysis
    """
    try:
        # Get AlphaVantage market sentiment (quantitative)
        alpha_sentiment = get_alphavantage_sentiment(ticker_symbol)
        
        # Get NewsAPI articles (qualitative, layoff detection)
        news_articles = get_newsapi_articles(company_name)
        
        # Combine analyses
        return {
            "company": company_name,
            "ticker": ticker_symbol,
            "market_sentiment": alpha_sentiment,
            "news_analysis": news_articles,
            "combined_assessment": generate_combined_assessment(alpha_sentiment, news_articles)
        }
        
    except Exception as e:
        return {"error": f"Failed to analyze news for {company_name}: {str(e)}"}


def get_alphavantage_sentiment(ticker_symbol):
    """Get quantitative sentiment from AlphaVantage"""
    try:
        # Get news sentiment
        response = requests.get(ALPHA_URL, params={
            'function': 'NEWS_SENTIMENT',
            'tickers': ticker_symbol,
            'apikey': ALPHAVANTAGE_API_KEY,
            'limit': 20
        }, timeout=10)
        
        news_data = response.json().get('feed', [])
        
        if not news_data:
            return {"error": "No sentiment data available"}
        
        # Calculate weighted sentiment score
        sentiments = []
        for article in news_data[:20]:
            for ts in article.get('ticker_sentiment', []):
                relevance = float(ts.get('relevance_score', 0))
                if relevance > 0.3:  # Only include relevant articles
                    sentiments.append(float(ts.get('ticker_sentiment_score', 0)))
        
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
        
        # Classify sentiment
        if avg_sentiment > 0.15:
            label = 'bullish'
        elif avg_sentiment < -0.15:
            label = 'bearish'
        else:
            label = 'neutral'
        
        # Extract key themes
        themes = []
        for article in news_data:
            for topic in article.get('topics', []):
                theme = topic.get('topic', '')
                if theme and theme not in themes:
                    themes.append(theme)
        
        return {
            "overall_sentiment": label,
            "sentiment_score": round(avg_sentiment, 3),
            "article_count": len(news_data),
            "key_themes": themes[:5]
        }
        
    except Exception as e:
        return {"error": f"AlphaVantage API failed: {str(e)}"}


def get_newsapi_articles(company_name):
    """Get articles and detect layoff/hiring signals"""
    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        
        from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        articles = newsapi.get_everything(
            q=company_name,
            from_param=from_date,
            language='en',
            sort_by='relevancy',
            page_size=15
        )
        
        if articles['status'] != 'ok' or not articles['articles']:
            return {"error": f"No news found for {company_name}"}
        
        headlines = []
        for article in articles['articles'][:15]:
            headlines.append({
                "title": article['title'],
                "description": article.get('description', ''),
                "source": article['source']['name'],
                "published": article['publishedAt']
            })
        
        # Analyze for job seeker signals
        signals = analyze_job_signals(headlines)
        
        return {
            "articles_found": len(headlines),
            "recent_headlines": headlines[:5],
            "job_signals": signals
        }
        
    except Exception as e:
        return {"error": f"NewsAPI failed: {str(e)}"}


def analyze_job_signals(headlines):
    """Detect layoff, hiring, and crisis signals"""
    
    layoff_keywords = ['layoff', 'layoffs', 'job cuts', 'workforce reduction', 'firing', 'restructuring', 'downsizing']
    hiring_keywords = ['hiring', 'expansion', 'growth', 'new roles', 'recruiting', 'job openings']
    crisis_keywords = ['lawsuit', 'scandal', 'investigation', 'fraud', 'crisis', 'bankruptcy']
    positive_keywords = ['profit', 'revenue growth', 'partnership', 'innovation', 'award', 'acquisition']
    
    layoff_count = 0
    hiring_count = 0
    crisis_count = 0
    positive_count = 0
    
    for h in headlines:
        text = (h['title'] + ' ' + h.get('description', '')).lower()
        
        if any(word in text for word in layoff_keywords):
            layoff_count += 1
        if any(word in text for word in hiring_keywords):
            hiring_count += 1
        if any(word in text for word in crisis_keywords):
            crisis_count += 1
        if any(word in text for word in positive_keywords):
            positive_count += 1
    
    return {
        "layoff_risk": "HIGH" if layoff_count > 2 else "MODERATE" if layoff_count > 0 else "LOW",
        "hiring_signals": "STRONG" if hiring_count > 3 else "MODERATE" if hiring_count > 0 else "WEAK",
        "crisis_indicators": crisis_count > 0,
        "positive_momentum": positive_count > layoff_count + crisis_count,
        "layoff_mentions": layoff_count,
        "hiring_mentions": hiring_count
    }


def generate_combined_assessment(alpha_sentiment, news_analysis):
    """Synthesize both data sources"""
    
    # Extract key metrics
    sentiment_score = alpha_sentiment.get('sentiment_score', 0)
    job_signals = news_analysis.get('job_signals', {})
    
    # Overall recommendation
    if sentiment_score > 0.15 and job_signals.get('layoff_risk') == 'LOW':
        recommendation = "STRONG - Positive market sentiment and stable employment"
    elif sentiment_score < -0.15 or job_signals.get('layoff_risk') == 'HIGH':
        recommendation = "CAUTION - Negative signals detected"
    else:
        recommendation = "MODERATE - Mixed signals, proceed with research"
    
    return {
        "recommendation": recommendation,
        "confidence": "high" if alpha_sentiment.get('article_count', 0) > 10 else "moderate"
    }