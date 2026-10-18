---
name: verify-quant-terminal
description: "Verify the Quant Terminal (projects.lukezhang.si/quant-terminal/): feature map, Playwright harness, and report. Run after any edit to the page."
---

# Verify: Quant Terminal

Live URL: https://projects.lukezhang.si/quant-terminal/
Source: ~/workspace/quant-terminal/index.html (canonical; deploy by surgical
overlay to sites/quant-terminal/index.html in absolukie/lukezhang-si, plus a
SITES entry in worker.js if one is not already there)

Feature map: ~/workspace/quant-terminal/verify/FEATURE_MAP.md
Harness: ~/workspace/quant-terminal/verify/verify.py
Last report: ~/workspace/quant-terminal/verify/REPORT.md
Fixtures: ~/workspace/quant-terminal/verify/fixtures/ (real Binance API
responses captured Oct 12, 2026; refresh them if the API shape changes)

Run locally: `python3 ~/workspace/quant-terminal/verify/verify.py`

The harness drives the real UI at 390x844 with the Binance endpoints
intercepted by the captured fixtures: provider status line, symbol chip
switch, timeframe switch, indicator toggles, H-line drawing via a real
chart tap, drag pan, a typed backtest run (asserts trades found and a
percent return), the custom symbol flow, and the watchlist add. A
pageerror fails the run. Last run: 16/16.

Quirks: drawings persist per symbol plus timeframe, so the harness's
H-line lands under BTCUSDT 4h by design of its step order. The backtest
result on the fixture window is negative (minus 10.28 percent); that is
the tool reporting honestly, not a failure. Data providers in order:
Binance vision, Coinbase, Kraken; all three were CORS-open when checked.
