import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.company_analyst import company_agent

print("Testing company agent...")
response = company_agent("Tell me about Amazon stock ticker AMZN")
print(response)