# GrowTheory - AI Company Intelligence Platform

An AI-powered platform that helps job seekers analyze companies and make informed career decisions using AWS Bedrock.

## Project Status

**Hackathon:** AWS AI Agent Global Hackathon  
**Days Remaining: 6** 
**Day 4 Progress:**
- ✅ Pivoted from Lambda/Bedrock Agent to Strands SDK
- ✅ Financial analyzer tool with yfinance integration
- ✅ Company health scoring (0-100 scale)
- ✅ Strands Agent with tool calling working
- ✅ End-to-end test with Claude 3.5 Haiku

**Previous Progress:**
- Built basic Bedrock connection
- Repository setup with proper structure
- AWS credentials configured
- Initial Lambda exploration (pivoted to Strands)

**Next Steps (Day 5):**
- Add Wikipedia tool for company background
- Add news sentiment analysis tool
- Implement multi-stage reasoning based on company type
- Begin frontend development

## Tech Stack

- **Agent Framework:** Strands SDK
- **LLM:** Claude 3.5 Haiku via Amazon Bedrock
- **Tools:** Custom Python tools with @tool decorator
- **Data Sources:** yfinance, NewsAPI (planned), Wikipedia (planned)
- **Python:** 3.13

## Project Structure
```bash
backend/
├── agents/          # Strands agents
├── tools/           # Custom tools (financial, news, etc.)
├── tests/           # Test files
└── config/          # Configuration and prompts
```

## Development Setup

### Prerequisites
- Python 3.13+
- AWS Account with Bedrock access (Claude 3.5 Haiku)
- Virtual environment

### Installation
```bash
# Clone and setup
git clone https://github.com/alisayeed248/growtheory.git
cd growtheory

# If on Windows, just run the ps1.
.\dev.ps1
```

### Running the Agent
```bash
python backend/tests/test_financial_tool.py
```
## Development Workflow

### Creating a Feature Branch
```bash
# Create and switch to new branch
git checkout -b feature/your-feature-name

# Make changes, then commit
git add .
git commit -m "Add feature description"

# Push branch to GitHub
git push origin feature/your-feature-name
```

### Useful Links
1. [Bedrock](https://docs.aws.amazon.com/bedrock/)
2. [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)
3. [Strands SDK Documentation](https://strandsagents.com/latest/documentation/docs/examples/)
4. [Strands Tools Reference](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/community-tools-package/)
