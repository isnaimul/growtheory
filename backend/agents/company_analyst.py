# backend/agents/company_analyst.py  
from strands import Agent
from backend.tools.financial_analyzer import analyze_company_finances

ANALYST_PROMPT = """You are a company intelligence analyst helping job seekers.

When asked about a company:
1. Call analyze_company_finances with the ticker symbol
2. Interpret the financial health score (0-100)
3. Explain what the signals mean for job seekers
4. Give a recommendation

Be honest about risks but also highlight opportunities."""

company_agent = Agent(
    system_prompt=ANALYST_PROMPT,
    tools=[analyze_company_finances]  
)