from strands import Agent
from strands.models.bedrock import BedrockModel
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.financial_analyzer import analyze_company_finances
from tools.market_sentiment_tool import analyze_market_sentiment

ANALYST_PROMPT = """You are a company intelligence analyst helping job seekers. You have analyze_company_finances and analyze_market_sentiment tools.
Use both for complete analysis, then give recommendation
When asked about a company:
1. Call analyze_company_finances with the ticker symbol
2. Interpret the financial health score (0-100)
3. Explain what the signals mean for job seekers
4. Give a recommendation

Be honest about risks but also highlight opportunities."""

# modelId has to be inference profile for 3.5 haiku, found in cross-region inference
model = BedrockModel(model_id="arn:aws:bedrock:us-east-1:975050287073:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0")
company_agent = Agent(
    model=model,
    system_prompt=ANALYST_PROMPT,
    tools=[analyze_company_finances, analyze_market_sentiment]
)
