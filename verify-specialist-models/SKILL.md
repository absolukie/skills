---
name: "verify-specialist-models"
description: "Re-verify the Specialist Model Playbook primer (lukezhang.si/blog/specialist-models/): run the saved real-UI harness against the local draft and re-check the live page and every source link."
---

# Verify: The Specialist Model Playbook

Feature map: `~/workspace/blog-drafts/specialist-models/verify/FEATURE_MAP.md`.
Harness: `~/workspace/blog-drafts/specialist-models/verify/qa.mjs` (puppeteer-core + Playwright headless shell, 390x844, real clicks, pageerror listener). Run: `cd ~/workspace/blog-drafts/specialist-models && node verify/qa.mjs`. Expect 30/30. It serves the local draft on :8937 and exercises: Fig 1 stepper both directions plus dots, arrow anchoring (identical top across steps), all 14 tappable cards, the latency race (balls move, four distinct durations), cost bars, the 13-stop timeline both directions plus arrow keys, zero external requests, zero page errors, no 390px overflow. Screenshots land in `verify/shots/`.

Live checks after any republish:
- `curl -s https://lukezhang.si/blog/specialist-models/` returns 200 and contains "The specialist model playbook" and "Dollar-weighted recall".
- `curl -s https://lukezhang.si/primers/` contains `/blog/specialist-models/`.
- Every href in the page returns 200 via curl with a browser UA (VentureBeat 429s curl but reads fine in a browser; treat a VB 429 as bot-wall, verify via browser.open instead).

The page also carries the tall-stage arrow tracker (visualizers rule 5, tall case): harmless here because both stages measure short, but if a future edit makes a stage taller than the viewport, the arrows must ride at viewport middle; the harness's anchor checks cover the short case.

Content invariants: zero em dashes and en dashes; Coinbase numbers exactly as in Coinbase's Part 3 (precision +7.5, recall +12.0, F1 +9.6, dollar-weighted recall +35.4 points; P50 0.683s vs 1.515s; training under $100 with the exclusion caveat attached); the /fine-tune-and-serve-llm skill described only as Armstrong described it; Together price discrepancy stated wherever the $0.17/$0.25 figure appears.
