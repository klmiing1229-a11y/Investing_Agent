# Example: "Is it a good time to buy SPY?"

Real read from 7 Oct 2026 (Asia morning, after the 6 Oct US close). Data route A: Longbridge MCP,
260 forward-adjusted daily candles, numbers from `tools/indicators.py`. The "Your position" line
uses the fictional `PORTFOLIO.example.md`.

---

**SPY.US · 779.09 USD · 2026-10-07 15:42 HKT · US market closed**
**Read: Conditions favour buying** — every Stage 2 test passes, but the new high came on light volume and the exit line is only 2% away.
**Stage:** 2, late part — rising, stacked averages, but already +24% from the March low, so not "early" (R-001, R-003)

**Stage 2 checklist (R-003) — 5/5**
✅ Price above 50DMA — 779.09 vs 763.81
✅ 50DMA above 200DMA — 763.81 vs 718.14
✅ Both averages rising — 50DMA +1.07%, 200DMA +1.34% (20 days)
✅ Up-days on more volume — ratio 1.05 (thin)
✅ Under 25% below 52-week high — 0.3% below 781.62

**Multiple edge (R-011) — 4/6 (want ≥3)**
✅ Trendline — new 52-week high on 6 Oct
✅ MA order 10/20/50/200 — 768.63 > 765.05 > 763.81 > 718.14
✅ Support/resistance — closed above the 13 Aug high (777.42)
❌ RSI — 62.7, neutral (computed from closes)
✅ MACD — line 2.79 above signal 1.74
❌ Volume — last day 0.78x the 20-day average; R-002 wants rising volume on a breakout

**Other checks**
⬜ Beats its benchmark (R-009) — SPY is the benchmark
⬜ Sector also strong (R-010) — no peer data returned
✅ Market mood OK (R-012) — US temperature 50, "neutral, gradually rising"

**Levels:** support 760.13 · resistance none (at highs) · exit line 763.81 = 50DMA (−2.0%; needs +2.0% to recover)

**Watch for**
⬜ A pullback that holds above 763.81 on falling volume, then a new high on rising volume
⬜ A close below 763.81 (50DMA), the first exit signal in R-007

**Your position:** one share ≈ 779 USD ≈ 16% of a 5,000 USD pot; adds to the existing VOO core (same index), so overlap, not diversification.
**Caveats:** none material · Rules: R-001, R-002, R-003, R-006, R-007, R-008, R-011, R-012 · education, not financial advice
