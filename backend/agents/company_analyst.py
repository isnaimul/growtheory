from strands import Agent
from strands.models.bedrock import BedrockModel
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.financial_analyzer import analyze_company_finances
from tools.news_analyzer import analyze_company_news

ANALYST_PROMPT = """You are a company intelligence analyst helping job seekers.

When asked about a company, you must build a comprehensive report card by:
1. Call analyze_company_finances with the ticker symbol to get financial health
2. Call analyze_company_news with the company name to check recent news and layoff signals
3. Synthesize both data sources to provide:
   - Overall hiring recommendation
   - Layoff risk assessment
   - Company stability rating
   - Key insights for job seekers

Be data-driven and honest about both opportunities and risks."""

model = BedrockModel(model_id="arn:aws:bedrock:us-east-1:975050287073:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0")
company_agent = Agent(
    model=model, 
    system_prompt=ANALYST_PROMPT, 
    tools=[analyze_company_finances, analyze_company_news]
)