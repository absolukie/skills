---
name: verify-harness-engineering
description: Verify the harness engineering primer (lukezhang.si/blog/harness-engineering/, "The Model Is Not the Agent") against its feature map by running the Playwright harness, which drives the real UI (reliability lab sliders and chips, mechanism cards, run stepper with gestures, 100-dot scenario grid, timeline) and asserts computed styles, rendered geometry, and the computed reliability numbers.
---

# Verify The Model Is Not the Agent

Feature map: `~/workspace/blog-drafts/harness-engineering/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/harness-engineering/verify/verify.py` (local port 8937)

Run it:

```
python3 ~/workspace/blog-drafts/harness-engineering/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's numbers are computed, not measured, and the harness guards the computation: with per-step success 0.95, 20 steps, and a verifier catching 90 percent of failures, clean-run probability is 1 - (0.05)(0.10) = 0.995 per step, compounded to 0.905, so the lab shows 90.5 percent and the dot grid shows exactly 36 clean dots (prompt only), 90 (checks), and 96 (full harness, 8 steps). The yield worked example is 46 / (380 + 214) = 0.077, labeled illustrative on the page.

Invariants the harness guards:
- Lab: sliders and catch-rate chips recompute live; zero pageerrors; scrollWidth at most 391.
- Mechanism cards: 6, third card toggles through its real header, chevron SVG renders at 20px.
- Run stepper: 6 rows light cumulatively, terminal next arrow hides (display none), arrows render at 46px, first claim renders at least 160px wide, dispatched-pointer swipes move both ways, receipt card present with its OBJECTIVE row.
- Dot grid: exactly 100 dots; scenario chips produce 36/90/96 clean dots.
- Timeline: 9 entries, December 2024 to September 6, 2026, count reaches 9 of 9.
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (cards, fhead, voices, xicon, meta, nokatex, fn, tl).
