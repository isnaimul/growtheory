from strands.tools import tool
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


@tool
def analyze_company_news(company_name):
    """
    Analyzes recent news sentiment about a company.
    
    Args:
        company_name (str): Company name (e.g., "Microsoft", "Amazon")
    
    Returns:
        dict: News analysis with sentiment and key themes
    """
    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        
        # Get news from last 30 days
        from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Fetch articles
        articles = newsapi.get_everything(
            q=company_name,
            from_param=from_date,
            language='en',
            sort_by='relevancy',
            page_size=10  # Get top 10 most relevant
        )
        
        if articles['status'] != 'ok' or not articles['articles']:
            return {"error": f"No news found for {company_name}"}
        
        # Extract headlines and descriptions
        headlines = []
        for article in articles['articles'][:10]:
            headlines.append({
                "title": article['title'],
                "description": article.get('description', ''),
                "source": article['source']['name'],
                "published": article['publishedAt']
            })
        
        # Analyze sentiment and themes
        analysis = analyze_sentiment(headlines, company_name)
        
        return {
            "company": company_name,
            "articles_found": len(headlines),
            "headlines": headlines[:5],  # Return top 5 for the agent
            "sentiment_analysis": analysis
        }
        
    except Exception as e:
        return {"error": f"Failed to fetch news for {company_name}: {str(e)}"}


def analyze_sentiment(headlines, company_name):
    """Analyze headlines for sentiment and key themes"""
    
    # Keywords for different signals
    layoff_keywords = ['layoff', 'layoffs', 'job cuts', 'workforce reduction', 'firing', 'restructuring']
    hiring_keywords = ['hiring', 'expansion', 'growth', 'new roles', 'recruiting']
    negative_keywords = ['decline', 'loss', 'lawsuit', 'scandal', 'investigation', 'crisis']
    positive_keywords = ['growth', 'profit', 'expansion', 'partnership', 'innovation', 'award']
    
    # Counters
    layoff_signals = 0
    hiring_signals = 0
    negative_count = 0
    positive_count = 0
    
    # Analyze each headline
    for h in headlines:
        text = (h['title'] + ' ' + h.get('description', '')).lower()
        
        if any(word in text for word in layoff_keywords):
            layoff_signals += 1
            negative_count += 1
        if any(word in text for word in hiring_keywords):
            hiring_signals += 1
            positive_count += 1
        if any(word in text for word in negative_keywords):
            negative_count += 1
        if any(word in text for word in positive_keywords):
            positive_count += 1
    
    # Determine overall sentiment
    if positive_count > negative_count * 1.5:
        overall_sentiment = "positive"
    elif negative_count > positive_count * 1.5:
        overall_sentiment = "negative"
    else:
        overall_sentiment = "neutral"
    
    return {
        "overall_sentiment": overall_sentiment,
        "layoff_indicators": layoff_signals > 0,
        "hiring_indicators": hiring_signals > 0,
        "positive_signals": positive_count,
        "negative_signals": negative_count,
        "layoff_mentions": layoff_signals
    }