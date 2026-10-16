# Quant trading syllabus

Built from [`RESEARCH.md`](RESEARCH.md). TEACH mode works through this in order.
`invest next lesson` = the first ⬜ topic. `invest teach me <topic>` = that topic, any order.
Every lesson is formula-first: formula → symbols → plain words → worked example on a ticker you
hold or name, with numbers fetched in that run → 3 quiz questions. Wrong or "idk" answers get a
parallel question. The agent updates the Status column as you go.

Status: ⬜ not taught · 🟨 taught, quiz < 2/3 · ✅ taught, quiz ≥ 2/3

| # | Topic | Goal: after it you can… | Source / link to his courses | Status |
|---|---|---|---|---|
| 1 | Returns: simple vs log, compounding | compute a 1-month and a 12-month return and say why log returns add up | general; log transformations in econometrics | ⬜ |
| 2 | Volatility and annualising (σ√T) | read "TSLA 20d vol 30%" and turn it into a typical daily move | Lo 2002 caveat | ⬜ |
| 3 | Sharpe, Sortino, max drawdown | compare two holdings on risk-adjusted return and worst fall | Lo 2002; R-008 | ⬜ |
| 4 | Beta and correlation | explain beta as the OLS slope of stock returns on market returns | regression (OLS slope); W-007 | ⬜ |
| 5 | Trend following and moving averages | say what a 200DMA filter does and why it may not beat the market | Faber 2007; BLL 1992; W-005 | ⬜ |
| 6 | Time-series momentum | compute the 12m TSMOM signal and say when it reverses | Moskowitz-Ooi-Pedersen 2012; W-001 | ⬜ |
| 7 | Cross-sectional momentum and short-term reversal | explain 12-1 and why the last month is skipped | Jegadeesh-Titman 1993; Jegadeesh 1990; W-002, W-003 | ⬜ |
| 8 | Momentum crashes | name the "panic state" and why losers crash momentum | Daniel-Moskowitz 2016; W-004 | ⬜ |
| 9 | Factors: value, low beta, combining | say why value + momentum together beats either | Asness-Moskowitz-Pedersen 2013; Frazzini-Pedersen 2014 | ⬜ |
| 10 | Volatility targeting and position sizing | size a position from a risk budget and ATR | Moreira-Muir 2017; W-008, W-011 | ⬜ |
| 11 | Kelly criterion and fractional Kelly | compute Kelly for a coin bet and explain why pros use a fraction | MacLean-Thorp-Ziemba | ⬜ |
| 12 | Backtesting traps | spot look-ahead, survivorship and overfitting in a claimed backtest | Harvey-Liu-Zhu 2016; DSR; PBO; W-009 | ⬜ |
| 13 | Trading costs, turnover, the hold band | estimate what your broker's fees cost your pot per round trip | Novy-Marx-Velikov 2016; W-010 | ⬜ |
| 14 | Crypto factors | say what drives BTC returns that doesn't drive stocks | Liu-Tsyvinski 2021; W-013 | ⬜ |
| 15 | The job | explain quant trader vs researcher vs Goldman "strats", and the skills path (stats, Python, the books) | career sources in the research file | ⬜ |
