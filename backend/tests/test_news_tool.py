import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.news_analyzer import analyze_company_news

print("Testing news analyzer...")
result = analyze_company_news("Microsoft")
print(result)