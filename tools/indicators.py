#!/usr/bin/env python3
"""Investing Agent: indicator calculator. Python 3.8+, standard library only, no API key.

Three ways to feed it daily prices (oldest or newest first, either is fine):

  python3 indicators.py --yahoo SPY          fetch ~2 years of daily data from Yahoo Finance
                                             (unofficial public endpoint; may change or rate-limit),
                                             plus a 3-month comparison with SPY (or 2800.HK for .HK)
  python3 indicators.py prices.csv           a CSV with Date, High, Low, Close, Volume columns
                                             (Yahoo "Download", Stooq, Investing.com, your broker)
  python3 indicators.py candles.json         JSON: list of {timestamp, close, high, low, volume}
                                             (e.g. Longbridge MCP `candlesticks`) or rows
                                             [date, close, high, low, volume]

It prints the numbers behind the checklist: moving averages and their slope, 52-week high,
volume behaviour, RSI(14), MACD(12,26,9), swing support/resistance, the 5-point Stage 2
checklist and a QUANT block (volatility, momentum, drawdown, z-score, ATR, beta, size). It does not judge. The AI (or you) does that with PROMPT.md and KB.md.
Use at least 260 trading days so the 200-day average and its slope exist.

Optional flags (after the data argument) sharpen the QUANT block (KB W-rules):
  --bench FILE     benchmark candles (CSV or JSON) → beta, correlation, 3m/6m/12m vs bench.
                   The --yahoo route fetches SPY (or 2800.HK) itself, so no file is needed there.
  --risk AMOUNT    how much you are willing to lose if the stop is hit, in YOUR home currency
                   → position size (W-011). Common default: 2% of your pot.
  --fx RATE        home currency per 1 unit of the price currency (e.g. 7.8 for USD→HKD);
                   default 1 (prices already in your home currency)
  --pot AMOUNT     total pot in your home currency, so the size is also shown as % of pot
Crypto (candles on weekends) is annualised with 365 periods/year, stocks with 252.
"""
import csv
import json
import sys
import urllib.request


def _num(x):
    try:
        return float(str(x).replace(",", ""))
    except (TypeError, ValueError):
        return None


def load_json(path):
    rows = json.load(open(path))
    if isinstance(rows, dict):
        rows = rows.get("data") or rows.get("candlesticks") or rows.get("items") or []
    out = []
    for r in rows:
        if isinstance(r, dict):
            out.append((str(r.get("timestamp") or r.get("date", ""))[:10], _num(r["close"]),
                        _num(r["high"]), _num(r["low"]), _num(r.get("volume")) or 0.0))
        else:
            d, c, h, l, v = r[:5]
            out.append((str(d)[:10], _num(c), _num(h), _num(l), _num(v) or 0.0))
    return out


def load_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cols = {k.strip().lower(): k for k in reader.fieldnames or []}

        def col(*names):
            for n in names:
                if n in cols:
                    return cols[n]
            sys.exit(f"CSV needs a column named one of {names}; found {list(cols)}")

        cd, cc, ch, cl = col("date", "datetime", "time"), col("close", "price", "close/last"), col("high"), col("low")
        cv = cols.get("volume") or cols.get("vol.")
        out = []
        for r in reader:
            c, h, l = _num(r[cc]), _num(r[ch]), _num(r[cl])
            if None in (c, h, l):
                continue  # skip blank or "null" rows
            out.append((r[cd].strip()[:10], c, h, l, _num(r[cv]) if cv else 0.0))
    return out


def load_yahoo(symbol, quiet=False):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=2y&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        data = json.load(urllib.request.urlopen(req, timeout=20))
        res = data["chart"]["result"][0]
    except Exception as e:  # network, rate limit, unknown symbol
        sys.exit(f"Yahoo fetch failed for {symbol}: {e}. Download a CSV instead.")
    import datetime as dt
    q = res["indicators"]["quote"][0]
    out = []
    for i, t in enumerate(res.get("timestamp") or []):
        c, h, l, v = q["close"][i], q["high"][i], q["low"][i], q["volume"][i]
        if None in (c, h, l):
            continue
        out.append((dt.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d"), c, h, l, v or 0.0))
    cur = res.get("meta", {}).get("currency", "")
    if not quiet:
        print(f"Source: Yahoo Finance chart data for {symbol} ({cur}), unadjusted daily closes")
    return out


BENCH = None


def load(arg, arg2=None):
    global BENCH
    if arg == "--yahoo":
        if not arg2:
            sys.exit("Usage: python3 indicators.py --yahoo SYMBOL   (e.g. SPY, NVDA, 0700.HK, BTC-USD)")
        rows = load_yahoo(arg2)
        sym = arg2.upper()
        if sym not in ("SPY", "2800.HK"):
            BENCH = "2800.HK" if sym.endswith(".HK") else "SPY"
    elif arg.lower().endswith(".csv"):
        rows = load_csv(arg)
    else:
        rows = load_json(arg)
    rows = [r for r in rows if r[1] is not None]
    rows.sort(key=lambda x: x[0])
    return rows


def sma(xs, n, end=None):
    end = len(xs) if end is None else end
    if end < n:
        return None
    return sum(xs[end - n:end]) / n


def ema_series(xs, n):
    k = 2 / (n + 1)
    out, e = [], None
    for x in xs:
        e = x if e is None else x * k + e * (1 - k)
        out.append(e)
    return out


def rsi(closes, n=14):
    if len(closes) <= n:
        return None
    gains = [max(closes[i] - closes[i - 1], 0) for i in range(1, len(closes))]
    losses = [max(closes[i - 1] - closes[i], 0) for i in range(1, len(closes))]
    ag, al = sum(gains[:n]) / n, sum(losses[:n]) / n
    for g, l in zip(gains[n:], losses[n:]):
        ag, al = (ag * (n - 1) + g) / n, (al * (n - 1) + l) / n
    return 100.0 if al == 0 else 100 - 100 / (1 + ag / al)


def fmt(x, d=2):
    return "n/a" if x is None else f"{x:,.{d}f}"


def _std(xs):
    if len(xs) < 2:
        return None
    m = sum(xs) / len(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def _pct(x, d=1):
    return "n/a" if x is None else f"{x * 100:+.{d}f}%"


def atr(h, l, c, n=14):
    if len(c) <= n:
        return None
    trs = [max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])) for i in range(1, len(c))]
    a = sum(trs[:n]) / n
    for t in trs[n:]:
        a = (a * (n - 1) + t) / n  # Wilder smoothing
    return a


def quant_block(dates, c, h, l, opts):
    """Quant desk numbers (KB W-001…). Prints facts only; the agent judges."""
    import datetime as dt
    n = len(c)
    weekend = any(dt.date.fromisoformat(d).weekday() >= 5 for d in dates[-30:])
    A = 365 if weekend else 252          # periods per year
    M = round(A / 12)                     # periods per month (21 stocks, 30 crypto)
    rets = [c[i] / c[i - 1] - 1 for i in range(1, n)]
    print(f"\nQUANT block ({'crypto, 365' if weekend else 'stock, 252'} periods/yr)")

    v20 = _std(rets[-20:]) * A ** 0.5 if len(rets) >= 20 else None
    v60 = _std(rets[-60:]) * A ** 0.5 if len(rets) >= 60 else None
    vp = lambda x: "n/a" if x is None else f"{x * 100:.1f}%"
    print(f"Volatility (annualised): 20d {vp(v20)} · 60d {vp(v60)}"
          + (f"  ← rising (20d > 60d)" if v20 and v60 and v20 > v60 * 1.1 else ""))

    def ret_over(k, skip=0):
        if n <= k:
            return None
        return c[-1 - skip] / c[-1 - k] - 1

    r1m, r3m, r6m, r12m = ret_over(M), ret_over(3 * M), ret_over(6 * M), ret_over(A)
    mom = ret_over(A, skip=M)  # 12-1 momentum: t-12m → t-1m, skipping the last month
    print(f"Returns: 1m {_pct(r1m)} · 3m {_pct(r3m)} · 6m {_pct(r6m)} · 12m {_pct(r12m)}")
    print(f"12-1 momentum (skip last month): {_pct(mom)}"
          + ("" if mom is not None else f"  (needs >{A} candles; fetch more)"))
    if r12m is not None:
        print(f"Time-series momentum sign (12m): {'positive → trend up' if r12m > 0 else 'negative → trend down'}")

    win = c[-A:] if n >= A else c
    peak, mdd = win[0], 0.0
    for x in win:
        peak = max(peak, x)
        mdd = min(mdd, x / peak - 1)
    cur_dd = c[-1] / max(win) - 1
    print(f"Max drawdown ({'1y' if n >= A else f'{len(win)}d'}): {_pct(mdd)} · current drawdown from peak {_pct(cur_dd)}")

    yr = rets[-A:] if len(rets) >= A else rets
    s = _std(yr)
    if s:
        mu = sum(yr) / len(yr)
        sharpe = mu * A / (s * A ** 0.5)
        downs = [min(x, 0) for x in yr]
        dd = (sum(x * x for x in downs) / len(downs)) ** 0.5
        sortino = mu * A / (dd * A ** 0.5) if dd else None
        print(f"Sharpe proxy ({len(yr)}d, rf=0, iid √{A} scaling): {fmt(sharpe)} · Sortino proxy {fmt(sortino)}")

    m50 = sma(c, 50)
    s50 = _std(c[-50:]) if n >= 50 else None
    z = (c[-1] - m50) / s50 if m50 and s50 else None
    print(f"Z-score vs 50DMA: {fmt(z)}" + ("  ← stretched (|z|>2)" if z is not None and abs(z) > 2 else ""))

    a14 = atr(h, l, c)
    print(f"ATR14: {fmt(a14)} ({_pct(a14 / c[-1] if a14 else None)} of price) · 2×ATR stop = {fmt(c[-1] - 2 * a14 if a14 else None)}")

    if opts.get("bench"):
        try:
            src = opts["bench"]
            raw = src if isinstance(src, list) else (load_csv(src) if src.lower().endswith(".csv") else load_json(src))
            b = sorted([r for r in raw if r[1] is not None], key=lambda x: x[0])
            bmap = {r[0]: r[1] for r in b}
            common = [d for d in dates if d in bmap]
            cm = {d: x for d, x in zip(dates, c)}
            pairs = [(cm[common[i]] / cm[common[i - 1]] - 1, bmap[common[i]] / bmap[common[i - 1]] - 1)
                     for i in range(1, len(common))][-252:]
            if len(pairs) >= 60:
                xs, ys = [p[1] for p in pairs], [p[0] for p in pairs]
                mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
                cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)
                beta = cov / _std(xs) ** 2
                corr = cov / (_std(xs) * _std(ys))
                print(f"Beta vs bench ({len(pairs)} shared days): {fmt(beta)} · correlation {fmt(corr)}")
            bc = [r[1] for r in b]
            for lab, k in (("3m", 63), ("6m", 126), ("12m", 252)):
                kk = k if not weekend else round(k * 365 / 252)
                mine = ret_over(kk)
                theirs = bc[-1] / bc[-1 - k] - 1 if len(bc) > k else None
                if mine is not None and theirs is not None:
                    print(f"  {lab}: {_pct(mine)} vs bench {_pct(theirs)} → {'beating' if mine > theirs else 'lagging'}")
        except Exception as e:  # bad file: say so, never guess
            print(f"Beta/relative strength: unknown (bench file error: {e})")
    else:
        print("Beta/relative strength: unknown (no --bench file)")

    if opts.get("risk") and a14:
        fx = opts.get("fx", 1.0)
        stop_hkd = 2 * a14 * fx
        units = opts["risk"] / stop_hkd
        notional = units * c[-1] * fx
        line = (f"Size (W-011): risk {opts['risk']:,.0f} ÷ 2×ATR ({stop_hkd:,.2f}/unit) = {units:,.4f} units"
                f" ≈ {notional:,.0f} position (home currency)")
        if opts.get("pot"):
            line += f" = {notional / opts['pot'] * 100:.1f}% of pot"
        print(line)


def parse_opts(argv):
    opts, i = {}, 0
    while i < len(argv):
        k = argv[i]
        if k in ("--bench", "--risk", "--fx", "--pot") and i + 1 < len(argv):
            v = argv[i + 1]
            opts[k[2:]] = v if k == "--bench" else float(v)
            i += 2
        else:
            i += 1
    return opts


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    opts = parse_opts(sys.argv[2:])
    sym2 = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
    rows = load(sys.argv[1], sym2)
    if len(rows) < 30:
        sys.exit(f"Only {len(rows)} candles; need at least 30.")
    dates = [r[0] for r in rows]
    c = [r[1] for r in rows]
    h = [r[2] for r in rows]
    l = [r[3] for r in rows]
    v = [r[4] for r in rows]
    last = c[-1]
    n = len(c)

    print(f"Candles: {n} ({dates[0]} → {dates[-1]})   Last close: {fmt(last)}")
    if n < 200:
        print(f"⚠ Under 200 trading days of history: 200DMA = n/a (do NOT estimate it).")

    ma = {k: sma(c, k) for k in (10, 20, 50, 200)}
    # slope = MA now vs the same MA 20 trading days ago
    ma_prev = {k: sma(c, k, n - 20) for k in (50, 200)}
    print("MAs: " + " · ".join(f"{k}DMA {fmt(ma[k])}" for k in (10, 20, 50, 200)))
    for k in (50, 200):
        if ma[k] and ma_prev[k]:
            ch = (ma[k] / ma_prev[k] - 1) * 100
            print(f"  {k}DMA vs 20 days ago: {ch:+.2f}% → {'rising' if ch > 0.2 else 'falling' if ch < -0.2 else 'flat'}")
        else:
            print(f"  {k}DMA slope: n/a")
    present = [k for k in (10, 20, 50, 200) if ma[k] is not None]
    order = sorted(present, key=lambda k: -ma[k])
    print(f"  MA order (high→low): {' > '.join(str(k) for k in order)}"
          f"{'  ← bullish stack' if order == present else ''}")

    win = min(252, n)
    hi52, lo52 = max(h[-win:]), min(l[-win:])
    hi_date = dates[-win:][h[-win:].index(hi52)]
    below = (1 - last / hi52) * 100
    print(f"52w high {fmt(hi52)} ({hi_date}) · low {fmt(lo52)} · now {below:.1f}% below the high"
          + ("" if n >= 252 else f"  (only {n} days available)"))

    # Volume behaviour over the last 50 sessions: avg volume on up days vs down days
    up_v = [v[i] for i in range(max(1, n - 50), n) if c[i] > c[i - 1]]
    dn_v = [v[i] for i in range(max(1, n - 50), n) if c[i] < c[i - 1]]
    if up_v and dn_v:
        ratio = (sum(up_v) / len(up_v)) / (sum(dn_v) / len(dn_v))
        print(f"Volume (50d): up-day avg / down-day avg = {ratio:.2f} ({len(up_v)} up, {len(dn_v)} down)")
    else:
        ratio = None
    vol20 = sma(v, 20)
    if vol20:
        print(f"Last volume vs 20d avg: {v[-1] / vol20:.2f}x")

    r = rsi(c)
    r_prev = rsi(c[:-10]) if n > 30 else None
    print(f"RSI14: {fmt(r, 1)} (10 days ago {fmt(r_prev, 1)})  [computed from closes, Wilder]")

    e12, e26 = ema_series(c, 12), ema_series(c, 26)
    macd = [a - b for a, b in zip(e12, e26)]
    sig = ema_series(macd, 9)
    hist = [a - b for a, b in zip(macd, sig)]
    turn = ""
    if hist[-2] <= 0 < hist[-1]:
        turn = "  ← bullish cross today"
    elif hist[-2] >= 0 > hist[-1]:
        turn = "  ← bearish cross today"
    elif len(hist) > 5 and abs(hist[-1]) < abs(hist[-5]):
        turn = "  (histogram shrinking: momentum fading)"
    print(f"MACD(12,26,9): line {fmt(macd[-1])} · signal {fmt(sig[-1])} · hist {fmt(hist[-1])}{turn}")

    # Swing levels from the last 120 sessions: pivot = higher/lower than 5 bars each side
    look = min(120, n)
    piv_hi, piv_lo = [], []
    for i in range(n - look + 5, n - 5):
        if h[i] == max(h[i - 5:i + 6]):
            piv_hi.append(h[i])
        if l[i] == min(l[i - 5:i + 6]):
            piv_lo.append(l[i])
    sup = sorted([x for x in piv_lo if x < last], reverse=True)[:3]
    res = sorted([x for x in piv_hi if x > last])[:3]
    print(f"Swing support below: {', '.join(fmt(x) for x in sup) or 'none in 120d'}")
    print(f"Swing resistance above: {', '.join(fmt(x) for x in res) or 'none in 120d (at/near highs)'}")

    # Relative strength (R-009): change since the first close on/after 91 calendar days ago
    # (calendar dates, so 24/7 crypto and 5-day stocks cover the same window). Yahoo route only.
    if BENCH and n > 63:
        try:
            import datetime as dt
            start = (dt.date.fromisoformat(dates[-1]) - dt.timedelta(days=91)).isoformat()

            def move(ds, cs):
                i = next(k for k, d in enumerate(ds) if d >= start)
                return (cs[-1] / cs[i] - 1) * 100

            brows = load_yahoo(BENCH, quiet=True)
            mine = move(dates, c)
            theirs = move([r[0] for r in brows], [r[1] for r in brows])
            print(f"3-month move: {mine:+.1f}% vs benchmark {BENCH} {theirs:+.1f}%"
                  f" → {'beating' if mine > theirs else 'lagging'} it (KB R-009)")
        except SystemExit:
            print(f"3-month benchmark comparison: unknown ({BENCH} fetch failed)")

    print("\nStage 2 checklist (KB R-003):")
    chk = [
        ("a price > 50DMA", ma[50] is not None and last > ma[50]),
        ("b 50DMA > 200DMA", ma[50] is not None and ma[200] is not None and ma[50] > ma[200]),
        ("c both MAs rising", all(ma[k] and ma_prev[k] and ma[k] > ma_prev[k] * 1.002 for k in (50, 200))),
        ("d up-volume > down-volume", ratio is not None and ratio > 1),
        ("e < 25% below 52w high", below < 25),
    ]
    for name, ok in chk:
        unknown = (name.startswith("b") or name.startswith("c")) and ma[200] is None
        print(f"  {'n/a' if unknown else '✅' if ok else '❌'} {name}")
    print(f"  Score: {sum(ok for _, ok in chk)}/5")

    if BENCH and not opts.get("bench"):
        try:
            opts["bench"] = load_yahoo(BENCH, quiet=True)
        except SystemExit:
            pass
    quant_block(dates, c, h, l, opts)


if __name__ == "__main__":
    main()
