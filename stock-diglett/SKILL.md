---
name: stock-diglett
description: >
  Analyze stocks by fetching real market data and company fundamentals. Use when the user
  mentions a stock ticker (e.g. AAPL, NFLX, TSLA), asks about stock prices, company financials,
  or wants stock market analysis. Triggers on: "analyze [ticker]", "how's [ticker] doing",
  "stock price of [ticker]", "[ticker] fundamentals", "should I buy [ticker]", or any question
  about a specific stock's price, valuation, growth, or financials. Also triggers on Chinese
  phrases like "分析[ticker]", "[ticker]股票怎么样", "[ticker]最近走势".
---

# Stock Diglett

Analyze stocks using real market data from Yahoo Finance + web search for recent news context.

## Workflow

When the user asks about a stock:

1. **Identify the ticker(s)** from the user's message
2. **Run scripts silently** (redirect stdout to temp files, do NOT display via Bash):
   - `python3 scripts/chart_price.py <TICKER> --period <period> > /tmp/<ticker>_chart.txt 2>/dev/null` — price table
   - `python3 scripts/fetch_fundamentals.py <TICKER> > /tmp/<ticker>_fundamentals.json 2>/dev/null` — fundamentals JSON
3. **Search for recent news** using WebSearch if the user asks about recent events, price movements, or "why" questions
4. **Read** `references/analysis_guide.md` for metric interpretation benchmarks
5. **Prepare analysis**: replace the English `description` field in fundamentals JSON with a Chinese translation, then add `pros`, `cons`, `conclusion` fields. Create events JSON, then run `python3 scripts/print_analysis.py <fundamentals.json> [events.json] > /tmp/<ticker>_analysis.txt`
6. **Read temp files** with the Read tool, then **output the content directly as text** (no Bash) — the scripts produce plain text with Unicode box-drawing tables, no ANSI colors

## Scripts

### `scripts/fetch_price.py`

Fetch historical price data. Returns open/high/low/close/volume per day and period change %.

```
python3 scripts/fetch_price.py <TICKER> [--period 1mo] [--interval 1d] [--start YYYY-MM-DD --end YYYY-MM-DD]
```

Periods: `1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max`
Intervals: `1m, 5m, 15m, 30m, 1h, 1d, 5d, 1wk, 1mo, 3mo`

### `scripts/chart_price.py`

Print a plain-text price table with Unicode box-drawing characters. Shows OHLCV data, daily change %, volume, and an Event column with Yahoo Finance news headlines or classified move summaries for big-move days (>=3%). Output is plain text (no ANSI colors) for direct display.

```
python3 scripts/chart_price.py <TICKER> [--period 3mo] [--interval 1d] [--start YYYY-MM-DD --end YYYY-MM-DD]
```

### `scripts/fetch_fundamentals.py`

Fetch company fundamentals. Returns valuation (P/E, P/B, EV/EBITDA), profitability (margins, ROE, ROA), income (revenue, EPS, growth), balance sheet (debt, cash, ratios), dividends, and analyst consensus.

```
python3 scripts/fetch_fundamentals.py <TICKER>
```

## Response Guidelines

- Present key metrics in tables for readability
- Compare metrics against sector benchmarks (see `references/analysis_guide.md`)
- Highlight notable strengths and risks
- The price table script auto-fetches recent news headlines from Yahoo Finance and maps them to dates. For big-move days (>=3%) without a headline, use WebSearch to find the reason and mention it in the analysis
- When the user asks "why" a stock moved, always use WebSearch for recent news
- Answer in the same language the user used (Chinese or English)
- Include a disclaimer: market data may be delayed; this is not financial advice

## Dependency

Requires: `pip install yfinance`
