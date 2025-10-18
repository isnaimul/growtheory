import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.news_analyzer import analyze_company_news

print("Testing merged news analyzer...")
result = analyze_company_news("Microsoft", "MSFT")

print("\n=== MARKET SENTIMENT ===")
print(result.get('market_sentiment'))

print("\n=== NEWS ANALYSIS ===")
print(result.get('news_analysis'))

print("\n=== COMBINED ASSESSMENT ===")
print(result.get('combined_assessment'))
print("\n=== FULL RESULT ===")
print(result)  # Add this to see everything