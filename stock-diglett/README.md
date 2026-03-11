# Stock Diglett

A Claude Code skill that fetches real-time market data from Yahoo Finance and generates comprehensive stock analysis reports — complete with price tables, fundamental metrics, event timelines, and actionable insights.

## What It Does

When you mention a stock ticker or ask about a company's financials, Claude automatically:

1. Pulls 3-month price history with daily OHLCV data
2. Fetches company fundamentals (valuation, profitability, growth, balance sheet)
3. Searches for recent news to explain significant price movements
4. Generates a structured analysis report with Unicode box-drawing tables

### Report Sections

- **Price Table** — 3-month daily OHLCV with change %, volume, and auto-tagged events
- **Company Profile** — Chinese-translated business description
- **Major Events** — Significant price moves (>=3%) with researched explanations
- **Valuation Metrics** — P/E, P/B, P/S, EV/EBITDA with benchmark comparisons
- **Profitability** — Gross/operating/net margins, ROE, ROA
- **Growth & Income** — Revenue growth, earnings growth, EPS
- **Balance Sheet** — Cash, debt, D/E ratio, current ratio
- **Pros & Cons** — AI-synthesized strengths and risks
- **Conclusion** — Actionable summary with suggested strategy

## Example Output

> User: `should I buy Moomoo?`

### Price Table

```
  FUTU Price Table (3mo)  |  -10.82%

  Date        Open    High     Low   Close   Chg%     Volume   Event
  ──────────  ──────  ──────  ──────  ──────  ──────  ────────  ─────────────────────────────────
  2025-12-10   173.25  175.77  169.00  173.36     —       913.9K
  2025-12-11   170.79  175.60  169.70  172.77  -0.34%       1.5M
  2025-12-12   175.12  176.65  169.80  171.45  -0.76%       1.2M
  2025-12-15   171.87  171.87  161.27  161.89  -5.58% *     1.7M  Wall Street Analysts Think Futu Holdings
  2025-12-16   160.00  166.50  159.00  163.39  +0.93%       1.3M
  ...
  2026-03-09   142.50  143.38  138.79  143.26  -0.14%       1.7M
  2026-03-10   147.78  155.01  147.76  154.60  +7.92% *     1.5M  Here's Why Futu Holdings (FUTU) Could be
  ──────────  ──────  ──────  ──────  ──────  ──────  ────────  ─────────────────────────────────
  Current: $154.6  |  Low: $137.84 (2026-03-03)  |  High: $189.38 (2026-01-12)  |  Change: -10.82%
```

### Analysis Report

```
  Futu Holdings Limited (FUTU) 基本面分析报告

  公司简介
  ┌──────────────────────────────────────────────────────────────────────────────────────┐
  │ 富途控股是一家数字化证券经纪及财富管理产品分销服务商，业务覆盖香港及全球市场。公司通 │
  │ 过旗下「富途牛牛」和「Moomoo」两大数字平台提供在线金融服务，包括证券及衍生品交易经纪 │
  │ 、融资融券和基金分销服务。                                                           │
  └──────────────────────────────────────────────────────────────────────────────────────┘

  价格概览
  ┌────────────────────┬──────────────────────────────┐
  │ 指标               │ 数值                         │
  ├────────────────────┼──────────────────────────────┤
  │ 当前价格           │ $154.6                       │
  │ 52周最高           │ $202.53                      │
  │ 52周最低           │ $70.6                        │
  └────────────────────┴──────────────────────────────┘

  重大事件与股价波动
  ┌────────────┬──────────┬─────────┬───────┬────────────────────────────────────────────────┐
  │ 日期       │ 涨跌幅   │ 成交量  │ ★     │ 事件/原因                                      │
  ├────────────┼──────────┼─────────┼───────┼────────────────────────────────────────────────┤
  │ 2025-12-15 │ -5.58%   │ 1.7M    │ ★     │ 中概股整体回调，华尔街分析师重新评估富途目标价 │
  ├────────────┼──────────┼─────────┼───────┼────────────────────────────────────────────────┤
  │ 2026-01-02 │ +8.68%   │ 2.1M    │ ★     │ 新年首个交易日大涨，市场乐观情绪推动中概股集体 │
  │            │          │         │       │ 上扬，富途基本面强劲吸引买盘                   │
  ├────────────┼──────────┼─────────┼───────┼────────────────────────────────────────────────┤
  │ 2026-02-12 │ -4.75%   │ 2.4M    │ ★★    │ 中国央行维持LPR不变未降息，市场失望情绪蔓延，  │
  │            │          │         │       │ 中概科技股集体下跌                             │
  ├────────────┼──────────┼─────────┼───────┼────────────────────────────────────────────────┤
  │ 2026-03-10 │ +7.92%   │ 1.5M    │ ★★    │ 财报公布前一天大幅反弹，市场对Q4业绩预期乐观， │
  │            │          │         │       │ 分析师看好                                     │
  └────────────┴──────────┴─────────┴───────┴────────────────────────────────────────────────┘

  估值指标
  ┌────────────────────┬──────────────┬──────────────┬────────────────────────────┐
  │ 指标               │ 数值         │ 参考基准     │ 评价                       │
  ├────────────────────┼──────────────┼──────────────┼────────────────────────────┤
  │ 市值               │ $21.4亿      │ —            │                            │
  │ Trailing P/E       │ 17.27        │ 15-25        │ 合理                       │
  │ P/B                │ 4.59         │ < 3          │ 偏高                       │
  │ P/S                │ 1.130        │ < 5          │ 合理                       │
  │ EV/EBITDA          │ N/A          │ 10-15        │                            │
  │ EV/Revenue         │ 1.83         │ —            │                            │
  └────────────────────┴──────────────┴──────────────┴────────────────────────────┘

  盈利能力
  ┌────────────────────┬──────────────┬──────────────┬────────────────────────────┐
  │ 指标               │ 数值         │ 基准         │ 评价                       │
  ├────────────────────┼──────────────┼──────────────┼────────────────────────────┤
  │ 毛利率             │ 93.9%        │ > 40%        │ 健康                       │
  │ 营业利润率         │ 65.9%        │ > 20%        │ 健康                       │
  │ 净利润率           │ 51.70%       │ > 15%        │ 健康                       │
  │ ROE                │ 30.1%        │ > 15%        │ 健康                       │
  │ ROA                │ 5.1%         │ > 5%         │ 健康                       │
  └────────────────────┴──────────────┴──────────────┴────────────────────────────┘

  增长与收入
  ┌────────────────────┬────────────────────────────┐
  │ 指标               │ 数值                       │
  ├────────────────────┼────────────────────────────┤
  │ 总营收             │ ~190.1亿港元               │
  │ 营收增长率         │ +96.2% YoY ★               │
  │ 净利润             │ ~98.2亿港元                │
  │ EPS (TTM)          │ $8.9                       │
  │ EBITDA             │ N/A                        │
  └────────────────────┴────────────────────────────┘

  资产负债表
  ┌────────────────────┬──────────────┬──────────────┬────────────────────────────┐
  │ 指标               │ 数值         │ 基准         │ 评价                       │
  ├────────────────────┼──────────────┼──────────────┼────────────────────────────┤
  │ 现金               │ $1388.11亿   │ —            │ 充裕                       │
  │ 总负债             │ $136.3亿     │ —            │ 极低                       │
  │ 负债权益比         │ 0.37         │ < 1.0        │ 非常健康                   │
  │ 流动比率           │ 1.1          │ > 1.5        │ 偏低                       │
  │ 每股账面价值       │ $33.47       │ —            │ 溢价约362%                 │
  └────────────────────┴──────────────┴──────────────┴────────────────────────────┘

  ✓ 优势
  ┌──────┬──────────────────────────────────────────────────────────────────────┐
  │ 1.   │ 营收同比增长96.2%，净利润增长141.5%，增速炸裂，远超行业平均水平      │
  │ 2.   │ 估值极具吸引力：Trailing P/E仅17.3x，Forward P/E 13.2x，P/S仅1.13x  │
  │ 3.   │ 盈利能力顶级：毛利率93.9%、营业利润率65.9%、净利润率51.7%            │
  │ 4.   │ 20位分析师一致给出"强力买入"评级，平均目标价$232.55，约50%上行空间   │
  │ 5.   │ Moomoo平台国际化扩张顺利，覆盖美国、新加坡、澳洲、日本等多地        │
  │ 6.   │ 公司回购计划达8亿美元，展现管理层对自身价值的信心                    │
  └──────┴──────────────────────────────────────────────────────────────────────┘

  ✗ 风险
  ┌──────┬──────────────────────────────────────────────────────────────────────┐
  │ 1.   │ 中概股属性带来地缘政治风险，中美关系波动可能导致股价大幅震荡         │
  │ 2.   │ 近3个月股价下跌10.8%，从52周高点$202回调约24%，短期趋势偏弱          │
  │ 3.   │ 经纪业务高度依赖市场交易量和情绪，若全球股市转熊则营收可能迅速收缩   │
  │ 4.   │ 股价波动剧烈：3个月内单日涨跌超5%的天数达8天                        │
  └──────┴──────────────────────────────────────────────────────────────────────┘

  结论
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │ 富途控股基本面极其亮眼——近乎翻倍的营收增速、超过50%的净利润率、以及仅17x的P/ │
  │ E，使其成为成长股中罕见的"高增长+低估值"标的。Moomoo平台的全球化扩张为长期增 │
  │ 长提供了坚实支撑。建议采取分批建仓策略，利用近期回调逐步布局。               │
  └──────────────────────────────────────────────────────────────────────────────┘

  ! 免责声明：市场数据可能存在延迟，本分析仅供参考，不构成投资建议。
```

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- Python 3.8+

### Steps

```bash
# 1. Clone and copy the skill
git clone https://github.com/Abson/skills.git
cp -r skills/stock-diglett ~/.claude/skills/stock-diglett

# 2. That's it! Start Claude Code and use the skill
# Dependencies (yfinance) are auto-installed on first run
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
