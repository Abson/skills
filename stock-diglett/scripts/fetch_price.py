#!/usr/bin/env python3
"""Fetch stock price data for a given ticker and date range."""

import argparse
import json
import sys

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf


def fetch_price(ticker: str, period: str = "1mo", interval: str = "1d",
                start: str = None, end: str = None) -> dict:
    stock = yf.Ticker(ticker)

    kwargs = {"interval": interval}
    if start and end:
        kwargs["start"] = start
        kwargs["end"] = end
    else:
        kwargs["period"] = period

    hist = stock.history(**kwargs)

    if hist.empty:
        return {"error": f"No price data found for {ticker}"}

    records = []
    for date, row in hist.iterrows():
        records.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"]),
        })

    current = records[-1]["close"] if records else None
    first = records[0]["close"] if records else None
    change_pct = round((current - first) / first * 100, 2) if first and current else None

    return {
        "ticker": ticker.upper(),
        "period": period if not start else f"{start} to {end}",
        "interval": interval,
        "current_price": current,
        "period_change_pct": change_pct,
        "data_points": len(records),
        "prices": records,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch stock price data")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g. AAPL, NFLX)")
    parser.add_argument("--period", default="1mo",
                        help="Period: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max")
    parser.add_argument("--interval", default="1d",
                        help="Interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo")
    parser.add_argument("--start", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", help="End date YYYY-MM-DD")
    args = parser.parse_args()

    result = fetch_price(args.ticker, args.period, args.interval, args.start, args.end)
    print(json.dumps(result, indent=2))
