#!/usr/bin/env python3
"""Stock Timing Checklist: indicator calculator. Python 3.8+, standard library only, no API key.

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
volume behaviour, RSI(14), MACD(12,26,9), swing support/resistance and the 5-point Stage 2
checklist. It does not judge. The AI (or you) does that with PROMPT.md and KB.md.
Use at least 260 trading days so the 200-day average and its slope exist.
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


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    rows = load(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
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


if __name__ == "__main__":
    main()
