# Wikipedia Company News Scraper & AI Analyzer

An intelligent system that scrapes company information from Wikipedia and uses AWS Bedrock with Strands Agents SDK to analyze business intelligence insights including layoffs, acquisitions, mergers, and leadership changes.

## 🚀 Features

- **Web Scraping**: Automatically extracts company data from Wikipedia
- **AI Analysis**: Uses Claude (via AWS Bedrock) to analyze business trends
- **Multi-Company Support**: Batch process multiple companies at once
- **Intelligent Insights**: Identifies layoffs, acquisitions, mergers, and leadership changes
- **Interactive Agent**: Ask questions about company data in natural language
- **Batch Analysis**: Run predefined analyses and save results

## 📋 Prerequisites

- Python 3.10+
- AWS Account with Bedrock access
- AWS Credentials configured

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/isnaimul/wikipedia-scraper.git
cd wikipedia-scraper
```

### 2. Create and activate virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS credentials

```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `us-east-1`
- Output format: `json`

### 5. Enable Bedrock Model Access

1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Select region: **US East (N. Virginia)**
3. Click **Model access** → **Enable specific models**
4. Enable **Claude 3.5 Sonnet** or **Claude 4**
5. Wait for approval (usually instant)

## 📖 Usage

### Step 1: Add companies to scrape

Edit `companies.txt` and add company names (one per line):

```
Microsoft
Amazon (company)
Google
Tesla, Inc.
Meta Platforms
```

**Note:** Use exact Wikipedia page titles. Some companies need disambiguation like "Amazon (company)".

### Step 2: Scrape Wikipedia data

```bash
python run_scraper.py
```

This creates `company_news_data.json` with all scraped data.

### Step 3: Run interactive analysis

```bash
python analysis_agent.py
```

Ask questions like:
- "What layoffs have occurred across all companies?"
- "Tell me about Microsoft's acquisitions"
- "Compare Tesla and Amazon"
- "What industries are represented?"

### Step 4: Run batch analysis (optional)

```bash
python batch_analysis.py
```

Runs predefined analyses and saves to `batch_analysis_results.json`.

## 📁 Project Structure

```
wikipedia-scraper/
├── venv/                          # Virtual environment
├── wiki_scraper.py                # Wikipedia scraper
├── run_scraper.py                 # Scraper runner
├── companies.txt                  # List of companies
├── analysis_agent.py              # Strands AI agent
├── batch_analysis.py              # Batch analysis runner
├── deploy_agent.py                # AgentCore deployment
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore file
├── README.md                      # This file
├── company_news_data.json         # Output (created after scraping)
└── batch_analysis_results.json    # Output (created after analysis)
```

## 🔧 Configuration

### Change AWS Region

Edit `analysis_agent.py`:

```python
self.model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-west-2"  # Change this
)
```

### Change Model

Available models:
- `us.anthropic.claude-sonnet-4-20250514-v1:0` (Claude 4 Sonnet)
- `anthropic.claude-sonnet-4-20250514-v1:0` (Claude 3.5 Sonnet)

## 🛡️ Security

**NEVER commit AWS credentials to GitHub!**

- `.gitignore` is configured to exclude credentials
- Use AWS IAM roles for production deployments
- Rotate access keys regularly

## 📊 Example Output

### Scraped Data Structure

```json
{
  "company": "Microsoft",
  "url": "https://en.wikipedia.org/wiki/Microsoft",
  "insights": {
    "acquisitions": ["LinkedIn", "GitHub"],
    "layoffs": ["10,000 employees in 2023"],
    "industry_sector": "Technology"
  }
}
```

### Analysis Output

The AI agent provides natural language insights:
- Trend analysis across companies
- Industry comparisons
- Strategic recommendations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### "No module named 'strands'"
```bash
pip install strands-agents --force-reinstall
```

### "UnrecognizedClientException"
- Check AWS credentials: `aws sts get-caller-identity`
- Reconfigure: `aws configure`

### "No Wikipedia page found"
- Use exact Wikipedia page title
- Check page exists: https://en.wikipedia.org/wiki/[Company_Name]


