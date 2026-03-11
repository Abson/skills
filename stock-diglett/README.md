# Stock Diglett

A Claude Code skill that fetches real-time market data from Yahoo Finance and generates comprehensive stock analysis reports — complete with price tables, fundamental metrics, event timelines, and actionable insights.

## What It Does

When you mention a stock ticker or ask about a company's financials, Claude automatically:

1. Pulls 3-month price history with daily OHLCV data
2. Fetches company fundamentals (valuation, profitability, growth, balance sheet)
3. Searches for recent news to explain significant price movements
4. Generates a structured analysis report with Unicode box-drawing tables

### Example Output

```
  Alphabet Inc. (GOOGL) 基本面分析报告

  价格概览
  ┌────────────────────┬──────────────────────────────┐
  │ 指标               │ 数值                         │
  ├────────────────────┼──────────────────────────────┤
  │ 当前价格           │ $308.1                       │
  │ 52周最高           │ $349.0                       │
  │ 52周最低           │ $140.53                      │
  └────────────────────┴──────────────────────────────┘

  ✓ 优势
  ┌──────┬──────────────────────────────────────────────────────────────────────┐
  │ 1.   │ Google Cloud 营收同比增长48%至177亿美元，远超预期 ...               │
  └──────┴──────────────────────────────────────────────────────────────────────┘
```

The report includes these sections:

- **Price Table** — 3-month daily OHLCV with change %, volume, and auto-tagged events
- **Company Profile** — Chinese-translated business description
- **Major Events** — Significant price moves (>=3%) with researched explanations
- **Valuation Metrics** — P/E, P/B, P/S, EV/EBITDA with benchmark comparisons
- **Profitability** — Gross/operating/net margins, ROE, ROA
- **Growth & Income** — Revenue growth, earnings growth, EPS
- **Balance Sheet** — Cash, debt, D/E ratio, current ratio
- **Pros & Cons** — AI-synthesized strengths and risks
- **Conclusion** — Actionable summary with suggested strategy

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- Python 3.8+
- `yfinance` package

### Steps

```bash
# 1. Install the Python dependency
pip install yfinance

# 2. Clone and copy the skill
git clone https://github.com/Abson/skills.git
cp -r skills/stock-diglett ~/.claude/skills/stock-diglett

# 3. Verify the skill is loaded
# Start Claude Code — stock-diglett should appear in the skill list
```

### Verify Installation

Run Claude Code and type any of these:

```
analyze AAPL
TSLA fundamentals
should I buy GOOGL?
分析NFLX
```

If the skill is installed correctly, Claude will automatically fetch data and generate a report.

## How It Works

```
User: "analyze GOOGL"
         │
         ▼
┌─────────────────────┐
│  1. Identify Ticker  │  Claude parses the ticker from your message
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐     ┌──────────────────────┐
│  2. Fetch Price Data │────▶│  chart_price.py      │  3-month OHLCV + news headlines
└────────┬────────────┘     └──────────────────────┘
         │
         ▼
┌─────────────────────┐     ┌──────────────────────┐
│  3. Fetch Fundamentals────▶│  fetch_fundamentals.py│  P/E, margins, growth, etc.
└────────┬────────────┘     └──────────────────────┘
         │
         ▼
┌─────────────────────┐
│  4. Web Search       │  Find causes for big-move days (>=3%)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  5. AI Analysis      │  Claude adds pros, cons, conclusion to fundamentals JSON
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐     ┌──────────────────────┐
│  6. Render Report    │────▶│  print_analysis.py   │  Unicode box-drawing tables
└────────┬────────────┘     └──────────────────────┘
         │
         ▼
┌─────────────────────┐
│  7. Output to User   │  Plain text, directly in terminal
└─────────────────────┘
```

## Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `chart_price.py` | Price table with OHLCV, change %, volume, event tags | `python3 scripts/chart_price.py AAPL --period 3mo` |
| `fetch_price.py` | Raw price data (JSON) | `python3 scripts/fetch_price.py AAPL --period 1mo --interval 1d` |
| `fetch_fundamentals.py` | Company fundamentals (JSON) | `python3 scripts/fetch_fundamentals.py AAPL` |
| `print_analysis.py` | Render analysis report from prepared JSON | `python3 scripts/print_analysis.py fundamentals.json [events.json]` |

### Supported Options

- **Periods**: `1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max`
- **Intervals**: `1m, 5m, 15m, 30m, 1h, 1d, 5d, 1wk, 1mo, 3mo`
- **Custom date range**: `--start YYYY-MM-DD --end YYYY-MM-DD`

## Trigger Phrases

The skill activates automatically on:

| Language | Examples |
|----------|----------|
| English | `analyze AAPL`, `TSLA fundamentals`, `should I buy GOOGL?`, `how's NFLX doing?`, `stock price of AMZN` |
| Chinese | `分析AAPL`, `TSLA股票怎么样`, `GOOGL最近走势` |

## Updating

```bash
cd /path/to/skills
git pull
cp -r stock-diglett ~/.claude/skills/stock-diglett
```

## License

MIT
