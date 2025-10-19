from strands.tools import tool
import yfinance as yf
from fredapi import Fred
import os
from dotenv import load_dotenv

load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")


@tool
def analyze_company_finances(ticker_symbol):
    """
    Analyzes a company's financial health using Yahoo Finance data.

    Args:
        ticker_symbol (str): Stock ticker symbol (e.g., "MSFT", "AAPL")

    Returns:
        dict: Financial analysis data
    """
    try:
        # Fetch company data
        company = yf.Ticker(ticker_symbol)
        info = company.info

        # Get stock history (last 3 months for trend analysis)
        hist = company.history(period="3mo")

        econ_context = get_economic_context()

        if hist.empty:
            return {"error": f"No data found for ticker: {ticker_symbol}"}

        # Extract key metrics
        current_price = hist["Close"].iloc[-1]
        month_ago_price = (
            hist["Close"].iloc[-22] if len(hist) > 22 else hist["Close"].iloc[0]
        )
        price_change_pct = ((current_price - month_ago_price) / month_ago_price) * 100

        # Determine trend
        if price_change_pct > 5:
            trend = "up"
        elif price_change_pct < -5:
            trend = "down"
        else:
            trend = "stable"

        # Calculate simple health score (0-100)
        health_score = calculate_health_score(info, price_change_pct, econ_context)

        # Identify signals
        signals = identify_signals(info, price_change_pct)

        # Return structured data
        return {
            "company_name": info.get("longName", "Unknown"),
            "ticker": ticker_symbol,
            "financial_health": {
                "revenue": info.get("totalRevenue"),
                "market_cap": info.get("marketCap"),
                "employees": info.get("fullTimeEmployees"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "profit_margin": info.get("profitMargins"),
            },
            "stock_performance": {
                "current_price": round(current_price, 2),
                "month_high": round(hist["High"].max(), 2),
                "month_low": round(hist["Low"].min(), 2),
                "price_change_pct": round(price_change_pct, 2),
                "trend": trend,
            },
            "economic_context": econ_context,
            "analysis": {"financial_health_score": health_score, "signals": signals},
        }

    except Exception as e:
        return {"error": f"Failed to analyze {ticker_symbol}: {str(e)}"}


def calculate_health_score(info, price_change_pct, econ_context):
    """Calculate a simple 0-100 health score with economic context."""
    score = 50 

    # Positive factors
    if info.get("profitMargins", 0) > 0.1:  # >10% profit margin
        score += 20
    if price_change_pct > 0:  # Stock trending up
        score += 15
    if info.get("marketCap", 0) > 100_000_000_000:  # >100B market cap
        score += 10

    # Negative factors
    if info.get("profitMargins", 0) < 0:  # Losing money
        score -= 30
    if price_change_pct < -10:  # Stock down >10%
        score -= 20

    employees = info.get('fullTimeEmployees', 1)
    revenue = info.get('totalRevenue', 0)

    if employees > 0 and revenue > 0:
        revenue_per_employee = revenue / employees
        avg_salary = econ_context.get('avg_annual_salary', 75000)
        
        # If company generates high revenue per employee, likely pays well
        if revenue_per_employee > avg_salary * 3:
            score += 5
    
    # Unemployment context: low unemployment = harder to hire = more valuable if hiring
    if econ_context.get('unemployment_rate', 4) < 4:
        score += 3  # Competitive market makes stable companies more valuable

    # Clamp to 0-100
    return max(0, min(100, score))

def get_economic_context():
    """Fetch current economic indicators from FRED"""
    try:
        fred = Fred(api_key=FRED_API_KEY)
        
        unemployment = fred.get_series('UNRATE', limit=1).iloc[-1]
        avg_hourly_wage = fred.get_series('CES0500000003', limit=1).iloc[-1]
        
        return {
            "unemployment_rate": round(unemployment, 1),
            "avg_hourly_wage": round(avg_hourly_wage, 2),
            "avg_annual_salary": round(avg_hourly_wage * 2080, 0)
        }
    except Exception as e:
        # Fallback if FRED fails
        return {
            "unemployment_rate": 4.0,
            "avg_annual_salary": 75000
        }


def identify_signals(info, price_change_pct):
    """Identify red/green flags."""
    signals = []

    # Green flags
    if info.get("totalRevenue", 0) > 10_000_000_000:  # >10B revenue
        signals.append("strong_revenue")
    if info.get("profitMargins", 0) > 0.15:  # >15% margins
        signals.append("high_profitability")
    if price_change_pct > 10:
        signals.append("strong_stock_performance")
    if info.get("fullTimeEmployees", 0) > 50000:
        signals.append("large_employer")

    # Red flags
    if info.get("profitMargins", 0) < 0:
        signals.append("unprofitable")
    if price_change_pct < -15:
        signals.append("stock_declining")

    return signals
