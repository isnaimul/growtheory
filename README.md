# GrowTheory - AI Company Intelligence Platform

An AI-powered platform that helps job seekers analyze companies and make informed career decisions using AWS Bedrock.

## Project Status

**Hackathon:** AWS AI Agent Global Hackathon  
**Days Remaining:** 8 
**Day 2 Progress:**
- ✅ Lambda function deployed (growtheory-company-basics)
- ✅ Bedrock Agent created with Claude 3.5 Sonnet
- ✅ Action group connected to Lambda
- ✅ End-to-end test working
- ✅ Agent autonomously calls tools

**Next Steps (Day 3):**
- Add 2 more Lambda functions (sentiment, financial data)
- Frontend integration
- Start building report card UI

**Tech Stack:**
- Amazon Bedrock Agent
- AWS Lambda (Python 3.13)
- Claude 3.5 Sonnet
- boto3

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