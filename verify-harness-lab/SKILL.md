---
name: "verify-harness-lab"
description: "Verification for Harness Lab (projects.lukezhang.si/harness-lab): feature map, real-click harness, and report locations. Trigger on: 'verify harness lab', 're-run harness lab QA', 'check harness lab'."
---

# Verify Harness Lab

Live URL: https://projects.lukezhang.si/harness-lab/

Run the harness (local files): `node ~/workspace/harness-lab/verify/qa.mjs`
It serves ~/workspace/harness-lab/site/ on port 8931 itself, drives headless Chromium (Playwright shell + puppeteer-core from moonblinked-studio's node_modules) at 390x844 with real clicks, and rewrites verify/qa-results.md. Exit code is nonzero when any check fails.

Feature map: ~/workspace/harness-lab/verify/FEATURE_MAP.md (the contract; compare the app against it, not against memory).
Last report: ~/workspace/harness-lab/verify/qa-results.md. Screenshots: ~/workspace/harness-lab/verify/shots/.

Quirks:
- S5 grading is synonym-aware on purpose: a question abstaining is only correct when the corpus genuinely lacks the topic. The returns question ("How long do I have to return an item?") MUST ground on D2.
- S9 speech output cannot be ear-verified headlessly; the map marks it UNVERIFIED.
- For a live run after deploy, point the harness's ROOT at the live site by loading pages from the live origin instead of the local server; local green plus a curl byte-compare of the served pages against ~/workspace/harness-lab/site/ is the accepted live proof when the proxy blocks browser runs.
