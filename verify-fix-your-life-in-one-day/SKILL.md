---
name: verify-fix-your-life-in-one-day
description: Verify the Dan Koe primer (lukezhang.si/blog/fix-your-life-in-one-day/, "Fix Your Life in One Day, Checked") against its feature map by running the Playwright harness, which drives the real UI (identity-loop stepper with gestures, compounding lab slider, one-day protocol board, mechanism cards, timeline) and asserts computed styles and rendered geometry.
---

# Verify Fix Your Life in One Day, Checked

Feature map: `~/workspace/blog-drafts/fix-your-life-in-one-day/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/fix-your-life-in-one-day/verify/verify.py` (local port 8939)

Run it:

```
python3 ~/workspace/blog-drafts/fix-your-life-in-one-day/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's numbers must reproduce the arithmetic stated in its copy: the compounding lab at +1 percent daily reads 37.8x after 365 days (1.01^365 = 37.7834, recomputed in this workspace), at minus 1 percent it reads 0.03x (0.0255), and the mirror chip at +1 percent reads 0.03x. The protocol census on the page is 14 + 9 + 7 = 30 prompts with 6 timed interrupts (11:00 am, 1:30 pm, 3:15 pm, 5:00 pm, 7:30 pm, 9:00 pm). Prompt wording on the page is paraphrased from Koe's essay, never copied; total direct quotation from the essay stays under 50 words.

Invariants the harness guards:
- Loop stepper: 8 rows light cumulatively, terminal arrows hide (prev at start, next at end), tap on the stage advances, dispatched-pointer swipes move both ways, first claim renders at least 160px wide at phone width.
- Compounding lab: slider drives instant recomputed readouts and a drawn canvas curve; default setting is Clear's +1 percent case.
- Day board: 3 phase chips (14/9/7), 6 time chips; tapping a time swaps the panel to that interrupt.
- Mechanism cards: 6, third card toggles through its real header, chevron SVG renders at 20px.
- Timeline: 9 entries, 1927 Adler to January 2026 Koe, count reads "9 of 9" at the end.
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson); exactly one display equation with a symbol legend.
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (copied from feel-physics).
- Honesty flags that must stay on the page: Koe's 80 to 90 percent failure figure flagged as his unverified claim against Oscarsson's measured 45 percent; one day framed as aiming, not installing (Lally 18 to 254 days); view counts platform-reported.
