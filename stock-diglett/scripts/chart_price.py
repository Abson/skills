#!/usr/bin/env python3
"""Print a styled stock price table in the terminal."""

import argparse
import sys

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf


def chart_price(ticker: str, period: str = "3mo", interval: str = "1d",
                start: str = None, end: str = None):
    stock = yf.Ticker(ticker)

    kwargs = {"interval": interval}
    if start and end:
        kwargs["start"] = start
        kwargs["end"] = end
    else:
        kwargs["period"] = period

    hist = stock.history(**kwargs)
    if hist.empty:
        print(f"No data found for {ticker}")
        sys.exit(1)

    # Detect intraday vs daily intervals
    intraday = interval in ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h")

    if intraday:
        date_labels = [d.strftime("%Y-%m-%d %H:%M") for d in hist.index]
    else:
        date_labels = [d.strftime("%Y-%m-%d") for d in hist.index]

    opens = [round(r["Open"], 2) for _, r in hist.iterrows()]
    closes = [round(r["Close"], 2) for _, r in hist.iterrows()]
    highs = [round(r["High"], 2) for _, r in hist.iterrows()]
    lows = [round(r["Low"], 2) for _, r in hist.iterrows()]

    first = closes[0]
    last = closes[-1]
    change = round((last - first) / first * 100, 2)
    sign = "+" if change >= 0 else ""
    min_low = min(lows)
    max_high = max(highs)
    min_idx = lows.index(min_low)
    max_idx = highs.index(max_high)

    # Fetch news headlines and map to dates
    news_by_date = {}
    try:
        news_items = stock.news
        if news_items:
            for item in news_items:
                content = item.get("content", {})
                pub = content.get("pubDate") or content.get("displayTime")
                title = content.get("title", "")
                if pub and title:
                    nd = pub[:10]  # "YYYY-MM-DD"
                    if nd not in news_by_date or len(title) > len(news_by_date[nd]):
                        news_by_date[nd] = title
    except Exception:
        pass

    # No ANSI colors — plain text output for direct display
    RST = ""
    FG = ""
    PURPLE = ""
    CYAN = ""
    GREEN = ""
    RED = ""
    YELLOW = ""
    COMMENT = ""
    ORANGE = ""

    # Compute average volume for relative comparison
    volumes = [hist.iloc[i]["Volume"] for i in range(len(closes))]
    avg_vol = sum(volumes) / len(volumes) if volumes else 1

    def classify_move(idx):
        """Classify a big-move day based on price action and volume patterns."""
        pct = (closes[idx] - closes[idx - 1]) / closes[idx - 1] * 100
        vol_ratio = volumes[idx] / avg_vol if avg_vol > 0 else 1
        gap_pct = (opens[idx] - closes[idx - 1]) / closes[idx - 1] * 100
        up = pct > 0

        # Check for reversal (previous day moved in opposite direction >= 2%)
        prev_pct = (closes[idx - 1] - closes[idx - 2]) / closes[idx - 2] * 100 if idx >= 2 else 0
        is_reversal = (up and prev_pct <= -2) or (not up and prev_pct >= 2)

        # Check for consecutive trend (3+ days same direction)
        consec = 0
        for j in range(idx, 0, -1):
            d = closes[j] - closes[j - 1]
            if (up and d > 0) or (not up and d < 0):
                consec += 1
            else:
                break
        is_streak = consec >= 3

        # Classify
        arrow = "▲" if up else "▼"
        if abs(gap_pct) >= 3:
            vol_desc = "放量" if vol_ratio >= 1.5 else "缩量"
            label = f"{arrow} 跳空高开{vol_desc}" if up else f"{arrow} 跳空低开{vol_desc}"
        elif is_reversal and vol_ratio >= 1.5:
            label = f"{arrow} 放量反转拉升" if up else f"{arrow} 放量反转下杀"
        elif is_reversal:
            label = f"{arrow} 超跌反弹" if up else f"{arrow} 冲高回落"
        elif is_streak:
            label = f"{arrow} 连涨{consec}日" if up else f"{arrow} 连跌{consec}日"
        elif vol_ratio >= 2:
            label = f"{arrow} 放量拉升" if up else f"{arrow} 放量杀跌"
        elif vol_ratio >= 1.3:
            label = f"{arrow} 量增上涨" if up else f"{arrow} 量增下跌"
        elif vol_ratio <= 0.5:
            label = f"{arrow} 缩量上涨" if up else f"{arrow} 缩量下跌"
        else:
            label = f"{arrow} {'上涨' if up else '下跌'} {pct:+.1f}%"
        return label

    # Print daily price table
    print()
    period_label = period if not start else f"{start} to {end}"
    print(f"{PURPLE}  {ticker.upper()} Price Table ({period_label})  |  {GREEN if change >= 0 else RED}{sign}{change}%{RST}")
    print()
    header = f"{PURPLE}  Date        Open    High     Low   Close   Chg%     Volume   Event{RST}"
    sep = f"{COMMENT}  ──────────  ──────  ──────  ──────  ──────  ──────  ────────  ─────────────────────────────────{RST}"
    print(header)
    print(sep)
    for i in range(len(closes)):
        if i == 0:
            chg_str = f"{FG}   —  "
            chg_color = FG
        else:
            pct = (closes[i] - closes[i - 1]) / closes[i - 1] * 100
            chg_str = f"{pct:+.2f}%"
            chg_color = GREEN if pct >= 0 else RED
        vol = volumes[i]
        if vol >= 1_000_000:
            vol_str = f"{vol / 1_000_000:.1f}M"
        elif vol >= 1_000:
            vol_str = f"{vol / 1_000:.1f}K"
        else:
            vol_str = str(int(vol))
        # Highlight the big movers
        marker = f"{YELLOW} *" if i > 0 and abs((closes[i] - closes[i-1]) / closes[i-1] * 100) >= 5 else "  "
        # Event column: news headline or classified move summary
        day_key = date_labels[i][:10] if len(date_labels[i]) >= 10 else date_labels[i]
        event = news_by_date.get(day_key, "")
        if event:
            event = event[:40]
            event_str = f"{ORANGE}{event}"
        elif i > 0 and abs((closes[i] - closes[i-1]) / closes[i-1] * 100) >= 3:
            event_str = f"{YELLOW}{classify_move(i)}"
        else:
            event_str = ""
        print(f"{CYAN}  {date_labels[i]}  {FG}{opens[i]:>7.2f} {highs[i]:>7.2f} {lows[i]:>7.2f} {closes[i]:>7.2f}  {chg_color}{chg_str:>6s}{marker}{FG} {vol_str:>8s}  {event_str}{RST}")
    print(sep)
    print(f"{PURPLE}  Current: {FG}${last}  {COMMENT}|  {PURPLE}Low: {RED}${min_low} ({date_labels[min_idx]})  {COMMENT}|  {PURPLE}High: {GREEN}${max_high} ({date_labels[max_idx]})  {COMMENT}|  {PURPLE}Change: {GREEN if change >= 0 else RED}{sign}{change}%{RST}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print stock price table in terminal")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g. AAPL, NFLX)")
    parser.add_argument("--period", default="3mo",
                        help="Period: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max")
    parser.add_argument("--interval", default="1d",
                        help="Interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo")
    parser.add_argument("--start", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", help="End date YYYY-MM-DD")
    args = parser.parse_args()

    chart_price(args.ticker, args.period, args.interval, args.start, args.end)
