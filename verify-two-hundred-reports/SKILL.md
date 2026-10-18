---
name: "verify-two-hundred-reports"
description: "Verify the Two Hundred Direct Reports primer (lukezhang.si/blog/two-hundred-reports/): run its Playwright harness against the feature map and read the report. Use before and after changing the primer, or when Luke asks whether it still works."
---

# Verify Two Hundred Direct Reports

Primer: "Two Hundred Direct Reports" at https://lukezhang.si/blog/two-hundred-reports/
(tags business, ai). Subject: Alexandr Wang's claim, on David Senra's podcast
(October 11, 2026), that 200+ researchers at Meta's TBD Lab report directly to
him, tested against Graicunas's 1933 relationship formula, the 1:1 calendar
math, the layer ledger, and the flat-organization evidence base.

## Feature map
`~/workspace/blog-drafts/two-hundred-reports/verify/FEATURE_MAP.md`, written
from the reader's point of view: brief and quote, the two KaTeX equations with
legends, the Graicunas slider lab (Figure 1), six mechanism cards, the week
stepper (Figure 2), the layer ledger (Figure 3), the 10-step timeline, seven
voices, agree/split camps, takeaways, keep exploring, sources.

## Harness
`~/workspace/blog-drafts/two-hundred-reports/verify/verify.py` serves the draft
on port 8935 and drives Chromium at 390x844 through the real UI: slider input
events (222 at n = 6, about 1.61 x 10^62 at n = 200), card taps opening and
closing, stepper arrows, card tap, and a dispatched-pointer swipe, tree chips
(2,501 / 1,111 / 171 / 51 managers), computed-style and geometry assertions
(46px arrows, 20px chevrons, lede inset, KaTeX stylesheet loaded and
.katex-mathml position absolute), zero pageerrors. Last run: 65/65.
Screenshots in `verify/shots/`; results in `verify/results.json`.

## Re-run
```
cd ~/workspace/blog-drafts/two-hundred-reports/verify && python3 verify.py
```
To check the live page instead, serve the draft bytes comparison: the live
page must equal the draft plus exactly 248 bytes (analytics beacon), and the
primers index must serve the two-hundred-reports card first.
