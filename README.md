# GrowTheory - AI Company Intelligence Platform

An AI-powered platform that helps job seekers analyze companies and make informed career decisions using AWS Bedrock.

## Project Status

**Hackathon:** AWS AI Agent Global Hackathon  
**Days Remaining:** 9  
**Current Stage:** Basic Bedrock setup complete

## Getting Started

### Prerequisites
- Python 3.13+ installed
- AWS Account with Bedrock access
- Git installed

### 1. Clone the Repository
```bash
git clone https://github.com/alisayeed248/growtheory.git
cd growtheory
```

### 2. Set Up Python Virtual Environment
```bash
python -m venv .venv

.\.venv\Scripts\Activate.ps1

source .venv/bin/activate

pip install boto3
```

### 3. Configure AWS Credentials
```bash
aws configure
```

Enter your 
- AWS Access Key ID
- AWS Secret Access Key
- Default region: us-east-1
- Default output format: json

### 4. Request Bedrock Model Access
1. Go to the Bedrock console
2. Click "Model access" in the left sidebar
3. Enable the models by requesting access


### 5. Test the Setup 
```bash
python test_bedrock.py
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