---
name: verify-daves-day
description: Verify the Dave's Day primer (lukezhang.si/blog/daves-day/, "Dave's Day: How Free Chicken Topped the App Store") against its feature map by running the Playwright harness, which drives the real UI (chart toggle, mechanism cards, giveaway-day stepper with gestures, growth slider, timeline) and asserts computed styles, rendered geometry, and the verified chart numbers.
---

# Verify Dave's Day

Feature map: `~/workspace/blog-drafts/daves-day/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/daves-day/verify/verify.py` (local port 8933)

Run it:

```
python3 ~/workspace/blog-drafts/daves-day/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's load-bearing facts were checked firsthand on October 14, 2026 and are saved in `~/workspace/research_notes/daves-hot-chicken-app-store-20261014/` (Apple's own chart feeds as JSON, the App Store lookup record, the full report). Verified: number one on Apple's US Top Free Food and Drink chart, number five overall (feed timestamped 10:15 PM Pacific, October 14). NOT verified, and flagged on the page: an overall number one in 2026 (that happened in October 2025, per Wired).

Invariants the harness guards:
- Chart board: 10 rows per chart; Dave's is row 1 (category) and row 5 (overall), accent-highlighted on both; toggle restores the category chart.
- Mechanism cards: 6, first starts open, third toggles through its real header, chevron renders at 20px, card body computed font size 15.5px.
- Giveaway-day stepper: 6 cumulative rows, notes equal rows, terminal arrows display:none, dispatched-pointer swipes move both ways without double-stepping, arrows 46px and stable at the first row's midway across steps.
- Growth: CAGR formula typeset by KaTeX with adjacent legend; slider at 99.47 percent reads exactly 500 stores and 1.00 yr doubling; 50 percent reads 38 stores, 120 percent reads 1,207.
- Prose dollar amounts are NOT math: static paragraphs containing two dollar figures once paired into a fake inline formula (caught in the first screenshot pass); the harness asserts no .katex inside prose paragraphs or source cards.
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt. The head is the shared shell copied from feel-physics through </head>; this page adds its own style block for .rk-* chart rows and #spikeRows rules.
