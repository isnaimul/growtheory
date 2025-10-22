# GrowTheory - AI-Powered Company Intelligence Platform

An AI agent that provides real-time financial intelligence on publicly traded companies, helping investors and analysts make data-driven decisions.

**Live Demo:** [growtheory.vercel.app](https://growtheory.vercel.app)

---

## What It Does

GrowTheory is an autonomous AI agent that analyzes companies by:
- **Gathering financial data** from Yahoo Finance (revenue, market cap, profitability, stock performance)
- **Analyzing market sentiment** via AlphaVantage and NewsAPI
- **Providing economic context** using Federal Reserve economic indicators (FRED)
- **Generating intelligence reports** with investment outlook and risk assessment

Simply search for any publicly traded company ticker (e.g., AAPL, MSFT, TSLA) and get a comprehensive analysis in under 3 minutes.

---

## Architecture

### Tech Stack
- **Frontend:** React + Vite, deployed on Vercel
- **Backend:** AWS Lambda (Docker container)
- **AI Agent:** Amazon Bedrock (Claude 3.5 Haiku) + Strands SDK
- **Data Sources:** 
  - Yahoo Finance (yfinance)
  - AlphaVantage API
  - NewsAPI
  - Federal Reserve Economic Data (FRED)
- **Storage:** DynamoDB with TTL-based expiration
- **API Gateway:** REST API with CORS-enabled endpoints

### Agent Architecture
The AI agent uses **multi-stage reasoning** powered by Amazon Bedrock:

1. **Financial Analysis Tool** - Fetches real-time market data, calculates health scores
2. **News Sentiment Tool** - Analyzes recent news and market sentiment
3. **Agent Orchestration** - Claude autonomously decides which tools to call based on context
4. **Report Generation** - Synthesizes data into actionable intelligence

### AWS Services Used
- **Amazon Bedrock** - LLM inference (Claude 3.5 Haiku)
- **AWS Lambda** - Containerized Python application with agent logic
- **Amazon API Gateway** - RESTful API endpoints
- **Amazon DynamoDB** - Company analysis cache with TTL
- **Amazon ECR** - Docker image registry
- **Amazon CloudWatch** - Logging and monitoring

---

## Features

### Intelligent Caching
- **Multi-layer caching** reduces latency and costs:
  - Frontend cache (5 minutes)
  - Lambda memory cache (5 minutes) 
  - DynamoDB persistent cache (24 hours)

### Smart Pagination
- Dashboard displays analyzed companies with pagination
- Real-time cache status tracking

### Graceful Degradation
- Agent continues analysis even if individual APIs fail
- Transparent status reporting (`complete`, `partial`, `failed`)

### Investment Intelligence
- Overall health score (0-100)
- Letter grade assessment (A+ to D)
- Green flags and risk factors
- Market sentiment analysis
- Investment outlook (BULLISH/NEUTRAL/BEARISH)

---

## 🎮 How to Use

1. **Visit** [growtheory.vercel.app](https://growtheory.vercel.app)
2. **Search** for a company using its stock ticker (e.g., AAPL, MSFT, GOOGL)
3. **Wait** ~2-3 minutes while the AI agent gathers and analyzes data
4. **Review** the comprehensive intelligence report with:
   - Financial health score
   - Market sentiment
   - Investment outlook
   - Risk assessment

---

## Project Structure
```
growtheory/
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service layer
│   │   └── styles/        # CSS files
│   └── package.json
│
├── backend/
│   ├── agents/            # Strands AI agent
│   │   └── company_analyst.py
│   ├── tools/             # Agent tools
│   │   ├── financial_analyzer.py
│   │   └── news_analyzer.py
│   ├── lambdas/           # Lambda handler
│   │   └── lambda_handler.py
│   ├── Dockerfile         # Container definition
│   └── requirements.txt
│
└── README.md
```

---

## 🛠️ Local Development (Optional)

The application is fully deployed, but if you want to run it locally:

### Prerequisites
- Python 3.13+
- Node.js 18+
- AWS Account with Bedrock access
- API Keys: AlphaVantage, NewsAPI, FRED

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

# Set environment variables
export ALPHAVANTAGE_API_KEY=your_key
export NEWS_API_KEY=your_key
export FRED_API_KEY=your_key
export COMPANY_CACHE_TABLE_NAME=your_dynamodb_table
```

### Frontend Setup
```bash
cd frontend
npm install

# Create .env.local
echo "VITE_API_BASE_URL=your_api_gateway_url" > .env.local

npm run dev
```

---

## Hackathon Compliance

### AWS AI Agent Global Hackathon Requirements

✅ **LLM hosted on AWS**
- Amazon Bedrock with Claude 3.5 Haiku

✅ **Agent Framework**
- Strands SDK with custom tools

✅ **Autonomous Capabilities**
- Agent independently decides which tools to call
- Multi-stage reasoning with context awareness

✅ **External Integrations**
- 4 external APIs: Yahoo Finance, AlphaVantage, NewsAPI, FRED
- Real-time data fetching and synthesis

✅ **AWS Services Used**
- Amazon Bedrock (LLM)
- AWS Lambda (compute)
- Amazon DynamoDB (storage)
- Amazon API Gateway (API management)
- Amazon ECR (container registry)
- Amazon CloudWatch (monitoring)

---

## Performance

- **Average analysis time:** 120-180 seconds (fresh data)
- **Cached results:** < 1 second
- **Lambda cold start:** ~1.5 seconds
- **Lambda warm execution:** ~10ms (with cache hit)
- **DynamoDB reads:** Minimal due to multi-layer caching

---

## Security Features

- **API Gateway rate limiting:** 10 req/sec, 20 burst
- **CORS-enabled endpoints**
- **IAM least-privilege policies**
- **Environment variable management**
- **No sensitive data in frontend**

---

## 👥 Team

Built by Naimul Islam & Sayeed Ali

---

##  Acknowledgments

- AWS Bedrock team for Claude API access
- Strands SDK for agent framework
- AlphaVantage, NewsAPI, and FRED for data APIs