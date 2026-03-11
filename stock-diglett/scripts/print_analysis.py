#!/usr/bin/env python3
"""Print a styled stock analysis report in the terminal using Dracula ANSI theme.

Uses box-drawing characters to create Excel-like grid tables.
Uses unicodedata to correctly measure CJK character widths for alignment.
Output is buffered and auto-degrades when exceeding 20KB to avoid truncation.
"""

import json
import re
import sys
import unicodedata

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

# Box-drawing characters
TL = "┌"; TR = "┐"; BL = "└"; BR = "┘"
H = "─"; V = "│"; TJ = "┬"; BJ = "┴"; LJ = "├"; RJ = "┤"; X = "┼"

_ANSI_RE = re.compile(r'\033\[[0-9;]*m')

BUDGET = 20_000  # bytes


def vwidth(s):
    """Visual width of a string: strip ANSI, use unicodedata for char widths."""
    clean = _ANSI_RE.sub('', s)
    w = 0
    for ch in clean:
        eaw = unicodedata.east_asian_width(ch)
        w += 2 if eaw in ('F', 'W') else 1
    return w


def vpad(s, width):
    """Pad string s with spaces to reach visual width."""
    return s + " " * max(0, width - vwidth(s))


def vtrunc(s, width):
    """Truncate plain text s to fit within visual width."""
    w = 0
    for i, ch in enumerate(s):
        eaw = unicodedata.east_asian_width(ch)
        cw = 2 if eaw in ('F', 'W') else 1
        if w + cw > width:
            return s[:i]
        w += cw
    return s


def vsplit(s, width):
    """Split plain text s into lines that fit within visual width."""
    lines = []
    line = ""
    w = 0
    for ch in s:
        eaw = unicodedata.east_asian_width(ch)
        cw = 2 if eaw in ('F', 'W') else 1
        if w + cw > width:
            lines.append(line)
            line = ch
            w = cw
        else:
            line += ch
            w += cw
    if line:
        lines.append(line)
    return lines


def grid_top(widths, out):
    out.append(f"  {COMMENT}{TL}{TJ.join(H * w for w in widths)}{TR}{RST}")


def grid_mid(widths, out):
    out.append(f"  {COMMENT}{LJ}{X.join(H * w for w in widths)}{RJ}{RST}")


def grid_bot(widths, out):
    out.append(f"  {COMMENT}{BL}{BJ.join(H * w for w in widths)}{BR}{RST}")


def grid_row(cells, widths, out):
    """Append │cell│cell│cell│. Each cell is a colored string, padded to width."""
    parts = []
    for c, w in zip(cells, widths):
        parts.append(vpad(c, w))
    out.append(f"  {COMMENT}{V}{f'{COMMENT}{V}'.join(parts)}{COMMENT}{V}{RST}")


def grid_header(labels, widths, out):
    cells = [f"{PURPLE} {l}" for l in labels]
    grid_row(cells, widths, out)


def cell(color, text):
    return f"{color} {text}"


def verdict_color(v):
    if v in ("合理", "偏低", "极低", "充裕", "健康", "非常健康"):
        return GREEN
    elif v in ("偏高", "较弱", "极高（VIE架构失真）"):
        return ORANGE
    elif v in ("极薄", "极小盘股"):
        return RED
    return FG


def section_title(text, out):
    out.append("")
    out.append(f"  {PURPLE}{text}{RST}")


def _parse_chg(e):
    raw = str(e.get("chg", "0")).replace("%", "").replace("+", "")
    try:
        return abs(float(raw))
    except ValueError:
        return 0.0


def render(d, events, level=0):
    """Render the full analysis report. Returns list of lines.

    level 0: full output
    level 1: remove description section
    level 2: also remove event table row separators
    level 3: also limit events to top 5 (by star DESC, abs(chg) DESC)
    """
    out = []
    ticker = d["ticker"]
    name = d["company_name"]
    price = d["price"]["current"]

    # ── Title ──
    out.append("")
    out.append(f"  {PURPLE}{name} ({ticker}) 基本面分析报告{RST}")
    out.append("")

    # ── 公司简介 ──
    if level < 1:
        section_title("公司简介", out)
        W_DESC = 86
        inner = W_DESC - 2
        grid_top([W_DESC], out)
        desc = d.get("description", "")
        for line in vsplit(desc, inner):
            grid_row([cell(FG, line)], [W_DESC], out)
        grid_bot([W_DESC], out)

    # ── 价格概览 ──
    section_title("价格概览", out)
    W1, W2 = 20, 30
    grid_top([W1, W2], out)
    grid_header(["指标", "数值"], [W1, W2], out)
    grid_mid([W1, W2], out)
    grid_row([cell(CYAN, "当前价格"), cell(FG, f"${price}")], [W1, W2], out)
    grid_row([cell(CYAN, "52周最高"), cell(RED, f"${d['price']['52w_high']}")], [W1, W2], out)
    grid_row([cell(CYAN, "52周最低"), cell(GREEN, f"${d['price']['52w_low']}")], [W1, W2], out)
    grid_bot([W1, W2], out)

    # ── 重大事件 ──
    ev_list = events
    if ev_list:
        if level >= 3:
            ev_list = sorted(ev_list, key=lambda e: (-int(e.get("star", 0)), -_parse_chg(e)))[:5]

        section_title("重大事件与股价波动", out)
        EW = [12, 10, 9, 7, 48]
        grid_top(EW, out)
        grid_header(["日期", "涨跌幅", "成交量", "★", "事件/原因"], EW, out)
        for ei, e in enumerate(ev_list):
            if level < 2 or ei == 0:
                grid_mid(EW, out)
            chg = str(e.get("chg", ""))
            if chg and chg[0] not in ("+", "-") and chg.replace(".", "", 1).replace("%", "").lstrip("-").isdigit():
                chg = f"+{chg}" if not chg.startswith("-") else chg
            if chg and not chg.endswith("%"):
                chg = f"{chg}%"
            chg_c = GREEN if chg.startswith("+") else RED if chg.startswith("-") else COMMENT
            star = e.get("star", 0)
            star_s = "★" * star if star else " "
            star_c = YELLOW if star else COMMENT
            desc_lines = vsplit(str(e.get("desc", "")), 46)
            vol_s = str(e.get("vol", ""))
            grid_row([
                cell(CYAN, str(e.get("date", ""))),
                cell(chg_c, chg),
                cell(FG, vol_s),
                cell(star_c, star_s),
                cell(FG, desc_lines[0] if desc_lines else ""),
            ], EW, out)
            for extra_line in desc_lines[1:]:
                grid_row([
                    cell(FG, ""),
                    cell(FG, ""),
                    cell(FG, ""),
                    cell(FG, ""),
                    cell(FG, extra_line),
                ], EW, out)
        grid_bot(EW, out)
        core = [e for e in ev_list if e.get("star", 0) >= 2]
        if core:
            out.append(f"  {YELLOW}核心催化剂: {FG}{core[0]['desc']}{RST}")

    # ── 4-column table helper ──
    TW = [20, 14, 14, 28]

    def table4(title, col_headers, rows):
        section_title(title, out)
        grid_top(TW, out)
        grid_header(col_headers, TW, out)
        grid_mid(TW, out)
        for label, val, bench, verd in rows:
            vc = verdict_color(verd)
            grid_row([cell(CYAN, label), cell(FG, val), cell(COMMENT, bench), cell(vc, verd)], TW, out)
        grid_bot(TW, out)

    # ── 估值指标 ──
    mc = d["market_cap"]
    mc_str = f"${mc/1e6:.0f}万" if mc < 1e9 else f"${mc/1e9:.1f}亿"
    mc_v = "极小盘股" if mc < 1e8 else "小盘股" if mc < 1e9 else ""

    pe = d["valuation"]["trailing_pe"]
    pe_s = f"{pe:.2f}" if pe else "N/A"
    pe_v = "合理" if pe and 15 <= pe <= 25 else "偏低" if pe and pe < 15 else "偏高" if pe else ""

    pb = d["valuation"]["price_to_book"]
    pb_s = f"{pb:.2f}" if pb else "N/A"
    pb_v = "偏低" if pb and pb < 3 else "偏高" if pb else ""

    ps = d["valuation"]["price_to_sales"]
    ps_s = f"{ps:.3f}" if ps else "N/A"
    ps_v = "极低" if ps and ps < 1 else "合理" if ps and ps < 5 else ""

    eveb = d["valuation"]["ev_to_ebitda"]
    eveb_s = f"{eveb:.0f}" if eveb else "N/A"
    eveb_v = "极高（VIE架构失真）" if eveb and eveb > 100 else "偏高" if eveb and eveb > 15 else "合理" if eveb else ""

    evr = d["valuation"]["ev_to_revenue"]
    evr_s = f"{evr:.2f}" if evr else "N/A"
    evr_v = "偏高" if evr and evr > 4 else ""

    table4("估值指标", ["指标", "数值", "参考基准", "评价"], [
        ("市值", mc_str, "—", mc_v),
        ("Trailing P/E", pe_s, "15-25", pe_v),
        ("P/B", pb_s, "< 3", pb_v),
        ("P/S", ps_s, "< 5", ps_v),
        ("EV/EBITDA", eveb_s, "10-15", eveb_v),
        ("EV/Revenue", evr_s, "—", evr_v),
    ])

    # ── 盈利能力 ──
    gm = d["profitability"]["gross_margin"]
    gm_s = f"{gm*100:.1f}%" if gm else "N/A"
    gm_v = "偏低" if gm and gm < 0.4 else "健康" if gm else ""

    om = d["profitability"]["operating_margin"]
    om_s = f"{om*100:.1f}%" if om else "N/A"
    om_v = "较弱" if om and om < 0.2 else "健康" if om else ""

    pm = d["profitability"]["profit_margin"]
    pm_s = f"{pm*100:.2f}%" if pm else "N/A"
    pm_v = "极薄" if pm and pm < 0.02 else "偏低" if pm and pm < 0.15 else "健康" if pm else ""

    roe = d["profitability"]["return_on_equity"]
    roe_s = f"{roe*100:.1f}%" if roe else "N/A"
    roe_v = "偏低" if roe and roe < 0.15 else "健康" if roe else ""

    roa = d["profitability"]["return_on_assets"]
    roa_s = f"{roa*100:.1f}%" if roa else "N/A"
    roa_v = "偏低" if roa and roa < 0.05 else "健康" if roa else ""

    table4("盈利能力", ["指标", "数值", "基准", "评价"], [
        ("毛利率", gm_s, "> 40%", gm_v),
        ("营业利润率", om_s, "> 20%", om_v),
        ("净利润率", pm_s, "> 15%", pm_v),
        ("ROE", roe_s, "> 15%", roe_v),
        ("ROA", roa_s, "> 5%", roa_v),
    ])

    # ── 增长与收入 ──
    section_title("增长与收入", out)
    IW = [20, 28]
    grid_top(IW, out)
    grid_header(["指标", "数值"], IW, out)

    rev = d["income"]["total_revenue"]
    rev_s = f"~{rev/1e8:.1f}亿美元" if rev else "N/A"
    grid_mid(IW, out)
    grid_row([cell(CYAN, "总营收"), cell(FG, rev_s)], IW, out)

    rg = d["income"]["revenue_growth"]
    rg_s = f"+{rg*100:.1f}% YoY" if rg else "N/A"
    rg_c = YELLOW if rg and rg > 0.2 else FG
    rg_note = " ★" if rg and rg > 0.3 else ""
    grid_row([cell(CYAN, "营收增长率"), cell(rg_c, rg_s + rg_note)], IW, out)

    ni = d["income"]["net_income"]
    ni_s = f"~{ni/1e4:.0f}万美元" if ni else "N/A"
    grid_row([cell(CYAN, "净利润"), cell(FG, ni_s)], IW, out)

    eps_s = f"${d['income']['eps_trailing']}" if d["income"]["eps_trailing"] else "N/A"
    grid_row([cell(CYAN, "EPS (TTM)"), cell(FG, eps_s)], IW, out)

    ebitda = d["income"]["ebitda"]
    ebitda_s = f"~{ebitda/1e4:.0f}万美元" if ebitda else "N/A"
    grid_row([cell(CYAN, "EBITDA"), cell(FG, ebitda_s)], IW, out)
    grid_bot(IW, out)

    # ── 资产负债表 ──
    cash = d["balance_sheet"]["total_cash"]
    cash_s = f"${cash/1e8:.2f}亿" if cash else "N/A"
    cash_v = "充裕" if cash and cash > 1e8 else ""

    debt = d["balance_sheet"]["total_debt"]
    debt_s = f"${debt/1e4:.0f}万" if debt else "N/A"
    debt_v = "极低" if debt and cash and debt < cash * 0.1 else ""

    de = d["balance_sheet"]["debt_to_equity"]
    de_s = f"{de/100:.2f}" if de else "N/A"
    de_v = "非常健康" if de and de/100 < 0.5 else "健康" if de and de/100 < 1.0 else ""

    cr = d["balance_sheet"]["current_ratio"]
    cr_s = f"{cr:.1f}" if cr else "N/A"
    cr_v = "健康" if cr and cr > 1.5 else "偏低" if cr else ""

    bv = d["balance_sheet"]["book_value"]
    bv_s = f"${bv:.2f}" if bv else "N/A"
    prem = ((price - bv) / bv * 100) if bv and price else 0
    bv_v = f"溢价约{prem:.0f}%" if prem > 0 else ""

    table4("资产负债表", ["指标", "数值", "基准", "评价"], [
        ("现金", cash_s, "—", cash_v),
        ("总负债", debt_s, "—", debt_v),
        ("负债权益比", de_s, "< 1.0", de_v),
        ("流动比率", cr_s, "> 1.5", cr_v),
        ("每股账面价值", bv_s, "—", bv_v),
    ])

    # ── 综合评价 ──
    pros = d.get("pros", [])
    cons = d.get("cons", [])
    conclusion = d.get("conclusion", "")

    if pros:
        section_title("✓ 优势", out)
        PW = [6, 70]
        grid_top(PW, out)
        for i, p in enumerate(pros, 1):
            lines = vsplit(str(p), 68)
            grid_row([cell(GREEN, f"{i}."), cell(FG, lines[0])], PW, out)
            for extra in lines[1:]:
                grid_row([cell(FG, ""), cell(FG, extra)], PW, out)
        grid_bot(PW, out)

    if cons:
        section_title("✗ 风险", out)
        PW = [6, 70]
        grid_top(PW, out)
        for i, c in enumerate(cons, 1):
            lines = vsplit(str(c), 68)
            grid_row([cell(RED, f"{i}."), cell(FG, lines[0])], PW, out)
            for extra in lines[1:]:
                grid_row([cell(FG, ""), cell(FG, extra)], PW, out)
        grid_bot(PW, out)

    if conclusion:
        section_title("结论", out)
        CW = [78]
        grid_top(CW, out)
        for line in vsplit(conclusion, 76):
            grid_row([cell(FG, line)], CW, out)
        grid_bot(CW, out)

    out.append("")
    out.append(f"  {COMMENT}! 免责声明：市场数据可能存在延迟，本分析仅供参考，不构成投资建议。{RST}")
    out.append("")

    return out


def main():
    if len(sys.argv) < 2:
        print("Usage: print_analysis.py <fundamentals.json> [events.json]")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        d = json.load(f)

    events = []
    if len(sys.argv) >= 3:
        with open(sys.argv[2]) as f:
            events = json.load(f)

    for level in range(4):
        lines = render(d, events, level)
        output = "\n".join(lines)
        if len(output.encode("utf-8")) <= BUDGET or level == 3:
            print(output)
            break


if __name__ == "__main__":
    main()
