# Knowledge base: the rules every read applies

Every read cites these IDs. Two kinds of rule:

- **`R-` rules: yours.** The starter set (R-001…R-012) is common stage-analysis practice (the
  four-stage model popularised by Stan Weinstein) plus multi-signal confirmation. Replace or extend
  it with LEARN mode as you learn from courses, books and talks.
- **`W-` rules: published research.** Quant-desk standards drawn from peer-reviewed papers
  (momentum, reversal, trend filters, low beta, volatility, costs, backtest overfitting). Every
  source link is in [`RESEARCH.md`](RESEARCH.md).

**`R` wins over `W`** when they disagree, because the agent is checking *your* method. Both are
kept and the conflict is written down under Conflicts.

Format: `R-NNN · rule · source · date added`. Never renumber. Retire a rule by striking it
through (~~like this~~) with the reason. If two rules conflict, mark both ⚔ and add a line under
Conflicts saying which wins when.

Next free ID: **R-013** (your rules) · **W-014** (research)

## Stages

- **R-001** · A stock moves through 4 stages: 1 base, 2 uptrend, 3 top, 4 decline. Only buy in Stage 2, ideally its early part. · starter set · 2026-10
- **R-002** · Stage 2 starts with a breakout above resistance on rising volume. · starter set · 2026-10
- **R-003** · Stage 2 checklist, all five: (a) price above the 50-day moving average (50DMA); (b) 50DMA above the 200DMA; (c) both averages rising; (d) up-days on higher volume than down-days; (e) price less than 25% below its 52-week high. · starter set · 2026-10
- **R-004** · Stage 3 warning signs: wider swings, false breakouts, a flattening 50DMA. Large holders are often distributing; plan the exit and protect profit. · starter set · 2026-10
- **R-005** · Stage 4: price below falling averages. A "death cross" (50DMA crossing below the 200DMA) on heavy selling volume confirms it. · starter set · 2026-10

## Exits

- **R-006** · Don't try to predict the top. Decide the "if it falls to here, I'm out" line BEFORE you buy. · starter set · 2026-10
- **R-007** · Exit signals tend to arrive early and in order: a break of the 50DMA, then a break of the 200DMA. Waiting for the second one usually costs far more than the first. · starter set · 2026-10
- **R-008** · Losses are asymmetric. Recovery needed = 1 / (1 − loss) − 1, so −20% needs +25%, −50% needs +100%, −56% needs about +127%. · starter set · 2026-10

## Confirmation

- **R-009** · Relative strength: favour assets beating their benchmark (e.g. SPY for US stocks, the Tracker Fund 2800.HK for Hong Kong) over the same window. · starter set · 2026-10
- **R-010** · Group move: strong stocks tend to move with their sector. Check whether the sector is also in Stage 2. · starter set · 2026-10
- **R-011** · Multiple edge: one reason to enter is not enough. Want at least 3, ideally 3–4, of these 6 aligned: trendline · moving-average order 10/20/50/200 · support/resistance · RSI (overbought/oversold, divergence) · MACD (momentum turn) · volume. · starter set · 2026-10
- **R-012** · Macro shocks (war, oil spikes, rate surprises) hit almost everything at once. Check the overall market's mood before reading a single stock. · starter set · 2026-10

## Quant desk standards (published research)

Thresholds marked "agent convention" are practical cut-offs, not numbers from the paper.

- **W-001** · Time-series momentum: an asset's own trailing 12-month return predicts its next 1–12 months (positive → trend up); it partly reverses over longer horizons. Use: the 12m return sign is one evidence line. · Moskowitz, Ooi & Pedersen 2012 (JFE); critique Kim-Tse-Wald (weaker 2009–13)
- **W-002** · Cross-sectional momentum: past 3–12-month winners have tended to beat losers over the next 3–12 months. Measure it as 12-1 (skip the latest month). · Jegadeesh & Titman 1993 (JF)
- **W-003** · Short-term reversal: last month's sharp winners tend to give some back. A 1-month spike is not momentum; a price more than 2 standard deviations above its 50DMA (z > 2, agent convention) counts against a new buy. · Jegadeesh 1990; Lehmann 1990
- **W-004** · Momentum crashes: momentum fails hardest in "panic" states (after a market decline, with high volatility) when the market snaps back. If the benchmark is >10% below its 1y high AND its 20d vol > 60d vol (agent convention), momentum evidence gets lower conviction. · Daniel & Moskowitz 2016 (JFE)
- **W-005** · Trend filter: price above a long moving average (10-month ≈ 200DMA) historically cut drawdowns. Treat it as a RISK tool, not a return promise: simple MA rules weakened after data-snooping correction and after 1986. Agrees with R-003/R-007. · Faber 2007; Brock-Lakonishok-LeBaron 1992; Sullivan-Timmermann-White 1999
- **W-006** · Value and momentum are negatively correlated, so a momentum-only read is one factor. When a stock sits near the top of its own valuation range while momentum says buy, note the disagreement. · Asness, Moskowitz & Pedersen 2013 (JF)
- **W-007** · Low beta: high-beta stocks have historically earned LOWER risk-adjusted returns than low-beta ones. Beta > 1.5 vs the benchmark costs one conviction level on a Buy lean. · Frazzini & Pedersen 2014 (JFE)
- **W-008** · Volatility is forecastable; returns barely are. When 20d volatility exceeds 60d volatility, size smaller and drop one conviction level. · Moreira & Muir 2017 (JF)
- **W-009** · Evidence bar: a new signal needs t > 3.0, not 2.0, and a backtest Sharpe must be deflated for how many things were tried. The agent never claims a proven edge from its own reads; a hit rate from fewer than 30 scored reads is labelled anecdotal (30 = agent convention). · Harvey-Liu-Zhu 2016 (RFS); Bailey & López de Prado 2014 (DSR); Bailey et al. (PBO)
- **W-010** · Costs and the hold band: trading costs sink high-turnover strategies; the best fix is a stricter bar to OPEN a position than to KEEP it. So a Buy lean needs more evidence than a Hold. On a small pot, a broker's minimum per-order fee is a real % drag on frequent trades. · Novy-Marx & Velikov 2016 (RFS)
- **W-011** · Sizing: Kelly maximises growth, but its inputs (expected returns) are the least reliable numbers you have, so practitioners bet a fraction. The agent sizes from risk, not edge: units = risk budget ÷ (2 × ATR14). Default risk budget = 2% of the pot per position (2% and 2×ATR are practitioner conventions, not from a paper). If one share/lot exceeds the size, it says so. · MacLean-Thorp-Ziemba; Chopra & Ziemba 1993
- **W-012** · Sharpe ratios annualised by √252 assume uncorrelated returns and can overstate risk-adjusted return by more than 65% when returns are autocorrelated. The script's Sharpe is a PROXY and is never the deciding line. · Lo 2002 (FAJ)
- **W-013** · Crypto: crypto returns show strong time-series momentum and move on crypto-specific factors (adoption, attention), with little exposure to stock factors. For BTC, weight W-001 more and treat SPY beta as weak evidence. · Liu & Tsyvinski 2021 (RFS)

## Your rules

_(LEARN mode appends here, starting at R-013.)_

## Conflicts

- ⚔ **R-011 vs W-005/W-009.** R-011 counts RSI and MACD as edges. Published evidence for simple technical rules is mixed after data-snooping correction. **R-011 still applies (your rule wins)**; reads label RSI/MACD lines "weaker published evidence".
- ⚔ **R-001 vs W-001/W-002.** Momentum can be positive while the stage isn't 2 (e.g. a rebound inside a downtrend). **R-001 wins:** no Buy lean outside Stage 2, whatever momentum says.
