---
name: verify-48-hours-in-sf
description: Verify the 48 Hours in SF primer (lukezhang.si/blog/48-hours-in-sf/, "48 Hours in SF: The Model Is 20 Percent of It") against its feature map by running the Playwright harness, which drives the real UI (stack explorer, mechanism cards, harness stepper with gestures, retention lab, ARR bars, timeline) and asserts computed styles, rendered geometry, and the retention arithmetic.
---

# Verify 48 Hours in SF

Feature map: `~/workspace/blog-drafts/48-hours-in-sf/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/48-hours-in-sf/verify/verify.py` (local port 8934)

Run it:

```
python3 ~/workspace/blog-drafts/48-hours-in-sf/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page checks Greg Isenberg's October 14, 2026 post (21 observations from 48 hours in SF) against the published record. Its load-bearing numbers: ChartMogul's AI-native median gross revenue retention of 40 percent implies about 7.3 percent monthly churn, so the retention lab must read $40.3M left after 12 months, $7.3M needed monthly, half-life 9.1 at the default; Cursor's disclosed annualized revenue rungs are $100M / $500M / $1B / $2B / about $4B (Jan 2025 to Jun 2026).

Invariants the harness guards:
- Exactly 2 KaTeX elements (the connector equation and the decay equation); the stylesheet is loaded and .katex-mathml is clipped. Money in static prose is spelled in words so auto-render can never pair two dollar amounts into a fake formula; dollar figures live only in script-built cards, stat labels, and data values, which are inserted after the one render pass.
- Stack explorer: 3 layers, harness active by default with the accent border, taps swap title, body, and stat.
- Mechanism cards: 6, first open, third opens through its real header, chevron SVG renders at 20px.
- Harness stepper: 6 cumulative rows, count "Step n of 6", terminal next arrow display:none, arrows 46px at the stage's vertical midway (the page's own CSS override sets top:50%; the donor shell left tops unset, which dropped the arrows onto the counter), tap card and dispatched-pointer swipes advance exactly one step, a tap within the post-swipe guard window does not double-step.
- Timeline: 8 steps, count "n of 8", card text clears the prev arrow (the card carries 12px side margins for this), tap card advances, terminal arrow hides.
- ARR bars: 5 rows, each row's label, track, and value on one line, fills animate to scale on scroll into view.
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (cards, fhead, voices, xicon, meta, nokatex, fn, tl).
