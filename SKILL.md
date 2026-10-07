---
name: stock_timing_checklist
description: Checks whether a stock, ETF or crypto chart currently meets a written set of timing rules (stage analysis, moving averages, RSI, MACD, volume) and shows the result as a ✅/❌/⬜ checklist with levels and an exit line. Gives a conditions read (favour / mixed / don't favour), never a buy or sell call. Use when the message starts with "timing", or the user asks "is it a good time to buy/sell <ticker>?", "check <ticker>", or writes "learn:" followed by investing notes to add to the rules. Not for portfolio construction, tax, or picking what to buy.
---

# stock_timing_checklist

This skill is a thin wrapper. The method is in `PROMPT.md` and the rules are in `KB.md`, both in
this folder.

## The trigger
- A message that starts with `timing`, e.g. `timing NVDA`, `timing sell TSLA?`.
- Natural phrases: "is it a good time to buy SPY?", "check 0700.HK", "should I sell now?".
- `learn:` followed by notes → LEARN mode.
- Not for "what should I buy?", portfolio allocation or tax. Say so and stop.

## What to do
1. Read `PROMPT.md` and `KB.md` in this folder. Rules in `KB.md` win over the copies in `PROMPT.md`.
2. **Get the numbers (PROMPT.md Step 1):**
   - If a market-data MCP is connected (e.g. Longbridge), use it, or use the `stock-timing` agent from `agent/`.
   - Otherwise, if you can run shell commands: `python3 -I <this folder>/tools/indicators.py --yahoo <SYMBOL>`
     (Yahoo symbols: `SPY`, `NVDA`, `0700.HK`, `BTC-USD`). If that fails, ask the user for a CSV path.
   - Otherwise ask the fill-in list.
3. If `PORTFOLIO.md` exists in this folder, read it for the "Your position" line. Never ask for account logins.
4. Answer in the PROMPT.md checklist, exactly.
5. Save the read to `reads/YYYY-MM-DD-<TICKER>.md` in this folder, with the script output underneath.
6. LEARN mode: append the new rules to `KB.md` under "Your rules" and update "Next free ID".
