from strands import Agent
from strands.models.bedrock import BedrockModel
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.financial_analyzer import analyze_company_finances
from tools.news_analyzer import analyze_company_news

ANALYST_PROMPT = """You are a company intelligence analyst helping job seekers make informed career decisions.

When asked about a company:
1. Call analyze_company_finances with the ticker symbol
2. Call analyze_company_news with the company name and ticker symbol
3. Check the 'status' field in each tool response:
   - 'complete': All data sources worked perfectly
   - 'partial': Some APIs failed (check 'errors' field), but still provide analysis
   - 'failed': Tool completely failed, explain what data is missing
4. If 'errors' exist, briefly acknowledge the limitations but STILL provide maximum value with available data
5. Synthesize financial health, market sentiment, and news signals into a cohesive report
6. Give honest, data-driven recommendations with clear reasoning

Be transparent about data quality while remaining helpful. Even with partial data, you can provide valuable insights.

Format your analysis clearly:
- Overall Assessment (score/10)
- Key Findings (3-5 bullet points)
- Hiring Signals (green/red flags)
- Recommendation (APPLY / RESEARCH MORE / AVOID)
"""

model = BedrockModel(model_id="arn:aws:bedrock:us-east-1:975050287073:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0")

company_agent = Agent(
    model=model, 
    system_prompt=ANALYST_PROMPT, 
    tools=[analyze_company_finances, analyze_company_news]
)