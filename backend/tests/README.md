The agent will call our tool to make decisions
It should look at:
1. revenue growth (growing or shrinking)
2. profit margins
3. stock performance (up or down)
4. market cap (company size/stability)
5. employee count changes (hiring or firing)

a simple output our tool can spit out to our agent:
```bash
{
    "company_name": "Microsoft Corporation",
    "financial_health": {
        "revenue": 281723994112,
        "market_cap": 3821019070464,
        "employees": 228000,
        "sector": "Technology",
        "industry": "Software - Infrastructure"
    },
    "stock_performance": {
        "current_price": 514.05,
        "month_high": 531.03,
        "month_low": 505.04,
        "trend": "stable"  # or "up", "down"
    },
    "analysis": {
        "financial_health_score": 85,  # 0-100
        "signals": ["strong_revenue", "stable_stock", "large_employer"]
    }
}
```
Our tool function should fetch data from our APIs, extract key metrics, calculate health scores, and identify signals and return this kind of dictionary