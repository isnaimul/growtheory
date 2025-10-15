import json, requests, yfinance as yf
from datetime import datetime
from typing import Dict, Optional
from strands import Agent, tool
from strands.models import BedrockModel

FRED_API_KEY = "FRED API KEY HERE"
AWS_REGION = "us-east-1"
BEDROCK_MODEL = "AWS AGENT MODEL HERE "

COMPANIES = {
    'microsoft': ('Microsoft Corporation', 'MSFT'),
    'apple': ('Apple Inc.', 'AAPL'),
    'google': ('Alphabet Inc.', 'GOOGL'),
    'alphabet': ('Alphabet Inc.', 'GOOGL'),
    'amazon': ('Amazon.com, Inc.', 'AMZN'),
    'meta': ('Meta Platforms, Inc.', 'META'),
    'facebook': ('Meta Platforms, Inc.', 'META'),
    'tesla': ('Tesla, Inc.', 'TSLA'),
    'netflix': ('Netflix, Inc.', 'NFLX'),
    'nvidia': ('NVIDIA Corporation', 'NVDA'),
    'salesforce': ('Salesforce, Inc.', 'CRM'),
    'adobe': ('Adobe Inc.', 'ADBE'),
    'uber': ('Uber Technologies, Inc.', 'UBER'),
    'airbnb': ('Airbnb, Inc.', 'ABNB'),
    'spotify': ('Spotify Technology S.A.', 'SPOT'),
}

WEIGHTS = {'culture': 0.4, 'compensation': 0.3, 'stability': 0.2, 'growth': 0.1}
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"

def resolve_company(q: str) -> Optional[Dict]:
    q = q.lower().strip().replace(' inc', '').replace(' corp', '').replace(',', '')
    for key, (name, ticker) in COMPANIES.items():
        if q in key or key in q or ticker.lower() == q:
            return {'name': name, 'ticker': ticker}

def fetch_financial_data(ticker: str) -> Dict:
    try:
        info = yf.Ticker(ticker).info
        return {
            'revenue': info.get('totalRevenue', 0),
            'profit_margin': (info.get('profitMargins', 0) or 0) * 100,
            'employees': info.get('fullTimeEmployees', 1),
            'revenue_growth': (info.get('revenueGrowth', 0) or 0) * 100,
            'debt_to_equity': info.get('debtToEquity', 0) or 0
        }
    except Exception:
        return {}

def fetch_industry_benchmark(api_key: str) -> Dict:
    try:
        r = requests.get(FRED_URL, params={
            'series_id': 'CES0500000003',
            'api_key': api_key,
            'file_type': 'json',
            'limit': 1,
            'sort_order': 'desc'
        }, timeout=10)
        hourly = float(r.json()['observations'][0]['value'])
        return {'industry_avg_salary': hourly * 2080}
    except Exception:
        return {'industry_avg_salary': 75000}

def fetch_employee_sentiment(_: str) -> Dict:
    return {'overall_rating': 3.8, 'work_life_balance': 3.6, 'culture_values': 3.7, 'compensation_rating': 3.9}

def calculate_grade(fin: Dict, bench: Dict, sent: Dict) -> Dict:
    c = sent
    f = fin
    b = bench

    culture = c['overall_rating'] * .4 + c['work_life_balance'] * .3 + c['culture_values'] * .3
    emp = f.get('employees', 1)
    rev = f.get('revenue', 0)
    avg = b['industry_avg_salary']
    comp = min(((rev / emp) * .3 if rev else avg) / avg, 1.5) * 3.33
    stab = max(0, min(5, (1 - min(f['debt_to_equity'] / 200, 1)) * 2.5 + (f['profit_margin'] / 20) * 2.5))
    growth = max(0, min(5, (f['revenue_growth'] + 10) / 4))

    scores = {'culture': culture, 'compensation': comp, 'stability': stab, 'growth': growth}
    composite = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    tier = next((t for t, thr in zip("SABCF", [4.5, 4.0, 3.5, 3.0, 0]) if composite >= thr), "F")

    return {'tier': tier, 'composite': round(composite, 2), 'scores': {k: round(v, 1) for k, v in scores.items()}}

_current = {}

@tool
def analyze_company_data(company: str) -> str:
    info = resolve_company(company)
    if not info: return f"Company '{company}' not found"
    fin, bench, sent = fetch_financial_data(info['ticker']), fetch_industry_benchmark(FRED_API_KEY), fetch_employee_sentiment(info['name'])
    grade = calculate_grade(fin, bench, sent)
    global _current
    _current = {'company': info['name'], 'ticker': info['ticker'], 'financial': fin, 'benchmark': bench, 'sentiment': sent, 'grade': grade}
    return json.dumps(_current, indent=2)

def create_agent():
    model = BedrockModel(model_id=BEDROCK_MODEL, region_name=AWS_REGION)
    return Agent(model=model, tools=[analyze_company_data], system_prompt="""You are a workplace analyst. 
Format your answer exactly:
GRADE: [TIER]-Tier ([score]/5.0)
EXECUTIVE SUMMARY
...
COMPONENT SCORES
...
DETAILED ANALYSIS
...
RECOMMENDATION
...""")

def analyze(company: str) -> Dict:
    agent = create_agent()
    r = agent(f"Analyze {company} and provide a workplace report card")
    msg = getattr(r, 'message', r)
    text = (msg.get('content', [{}])[0].get('text', '') if isinstance(msg, dict) else str(msg))
    return {'company': _current.get('company', company), 'ticker': _current.get('ticker', ''), 'analysis': text, 'grade': _current.get('grade', {}), 'raw_data': _current}
