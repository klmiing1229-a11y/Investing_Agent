---
name: investing_agent
description: Quant-desk style read of one stock, ETF or crypto. Answers "is it a good time to buy/sell <ticker>?" with an evidence-scored lean (Buy lean / Hold / Sell lean / No edge + Low/Medium/High conviction), shown as a news table, a fundamentals score and a 14-line ✅/❌/⬜ technical checklist citing your own rules and published quant research, then conditional IF/THEN actions sized from a 2% risk budget. Never places orders or sets price targets. Also teaches quant trading (15-topic syllabus) and learns your notes into rules. Use when the message starts with "invest" or "timing", or the user asks "is it a good time to buy/sell <ticker>?", "check <ticker>", "teach me <quant topic>", "next lesson", or writes "learn:" followed by investing notes. Not for picking what to buy, portfolio construction or tax.
---

# investing_agent

This skill is a thin wrapper. The method is in `PROMPT.md`, the rules in `KB.md`, their sources in
`RESEARCH.md` and the teaching order in `QUANT_SYLLABUS.md`, all in this folder.

## The trigger
- A message that starts with `invest` (or the older `timing`), e.g. `invest NVDA`, `invest sell TSLA?`.
- Natural phrases: "is it a good time to buy SPY?", "check 0700.HK", "should I sell now?".
- `invest next lesson`, `invest teach me momentum`, `invest quiz me` → TEACH mode.
- `learn:` followed by notes → LEARN mode.
- Not for "what should I buy?", portfolio allocation or tax. Say so and stop.

## What to do
1. Read `PROMPT.md` and `KB.md` in this folder. Rules in `KB.md` win over the copies in `PROMPT.md`.
2. **Get the numbers (PROMPT.md Step 1):**
   - If the Longbridge MCP is connected, use the `invest` agent from `agent/` (live data, news, fundamentals).
   - Otherwise, if you can run shell commands:
     `python3 -I <this folder>/tools/indicators.py --yahoo <SYMBOL> --risk <2% of pot> --pot <pot>`
     (Yahoo symbols: `SPY`, `NVDA`, `0700.HK`, `BTC-USD`). It fetches the benchmark itself. If that
     fails, ask the user for a CSV path. News and fundamentals: use a web/news tool if you have one,
     otherwise mark them ⬜.
   - Otherwise ask the fill-in list.
3. If `PORTFOLIO.md` exists in this folder, read it for the pot, currency and "Your position" line.
   Never ask for account logins.
4. Answer in the PROMPT.md format, exactly.
5. Save the read to `reads/YYYY-MM-DD-<TICKER>.md` in this folder, with the script output underneath.
6. TEACH mode: follow `QUANT_SYLLABUS.md`, log to `lessons/teach-log.md`, update the Status column.
7. LEARN mode: append the new rules to `KB.md` under "Your rules" and update "Next free ID".
