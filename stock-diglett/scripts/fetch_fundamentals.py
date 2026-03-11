#!/usr/bin/env python3
"""Fetch company fundamentals for a given ticker."""

import argparse
import json
import sys

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf


def safe_get(d: dict, *keys):
    """Safely get nested dict values."""
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return None
    return d


def fetch_fundamentals(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    if not info or info.get("trailingPegRatio") is None and info.get("marketCap") is None:
        # Try to see if we got anything useful
        if not info.get("shortName"):
            return {"error": f"No fundamental data found for {ticker}"}

    def g(key, default=None):
        return info.get(key, default)

    result = {
        "ticker": ticker.upper(),
        "company_name": g("shortName") or g("longName"),
        "sector": g("sector"),
        "industry": g("industry"),
        "market_cap": g("marketCap"),
        "enterprise_value": g("enterpriseValue"),
        "price": {
            "current": g("currentPrice") or g("regularMarketPrice"),
            "target_high": g("targetHighPrice"),
            "target_low": g("targetLowPrice"),
            "target_mean": g("targetMeanPrice"),
            "52w_high": g("fiftyTwoWeekHigh"),
            "52w_low": g("fiftyTwoWeekLow"),
        },
        "valuation": {
            "trailing_pe": g("trailingPE"),
            "forward_pe": g("forwardPE"),
            "peg_ratio": g("pegRatio"),
            "price_to_book": g("priceToBook"),
            "price_to_sales": g("priceToSalesTrailing12Months"),
            "ev_to_ebitda": g("enterpriseToEbitda"),
            "ev_to_revenue": g("enterpriseToRevenue"),
        },
        "profitability": {
            "profit_margin": g("profitMargins"),
            "operating_margin": g("operatingMargins"),
            "gross_margin": g("grossMargins"),
            "return_on_equity": g("returnOnEquity"),
            "return_on_assets": g("returnOnAssets"),
        },
        "income": {
            "total_revenue": g("totalRevenue"),
            "revenue_per_share": g("revenuePerShare"),
            "revenue_growth": g("revenueGrowth"),
            "earnings_growth": g("earningsGrowth"),
            "ebitda": g("ebitda"),
            "net_income": g("netIncomeToCommon"),
            "eps_trailing": g("trailingEps"),
            "eps_forward": g("forwardEps"),
        },
        "balance_sheet": {
            "total_cash": g("totalCash"),
            "total_debt": g("totalDebt"),
            "debt_to_equity": g("debtToEquity"),
            "current_ratio": g("currentRatio"),
            "book_value": g("bookValue"),
        },
        "dividends": {
            "dividend_rate": g("dividendRate"),
            "dividend_yield": g("dividendYield"),
            "payout_ratio": g("payoutRatio"),
            "ex_dividend_date": g("exDividendDate"),
        },
        "analyst": {
            "recommendation": g("recommendationKey"),
            "number_of_analysts": g("numberOfAnalystOpinions"),
        },
        "description": g("longBusinessSummary"),
    }

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch company fundamentals")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g. AAPL, NFLX)")
    args = parser.parse_args()

    result = fetch_fundamentals(args.ticker)
    print(json.dumps(result, indent=2, default=str))
