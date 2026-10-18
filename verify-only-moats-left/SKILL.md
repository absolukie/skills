---
name: verify-only-moats-left
description: "Verify the 'Only Moats Left' primer (lukezhang.si/blog/only-moats-left/): feature map, Playwright harness, and report. Run after any edit to the page."
---

# Verify: The Only Moats Left primer

Live URL: https://lukezhang.si/blog/only-moats-left/
Draft source: ~/workspace/blog-drafts/only-moats-left/index.html (canonical; deploy by
surgical overlay to blog/only-moats-left/ in absolukie/lukezhang-si, plus the image
at blog/only-moats-left/images/moat.webp)

Feature map: ~/workspace/blog-drafts/only-moats-left/verify/FEATURE_MAP.md
Harness: ~/workspace/blog-drafts/only-moats-left/verify/verify.py
Last report: ~/workspace/blog-drafts/only-moats-left/verify/REPORT.md

Run locally: `python3 ~/workspace/blog-drafts/only-moats-left/verify/verify.py`
Run live: `python3 ~/workspace/blog-drafts/only-moats-left/verify/verify.py https://lukezhang.si/blog/only-moats-left/`

The harness drives the real UI at 390x844: scoreboard stepper (one bar per tap,
terminal arrows hidden with display:none, arrows straddling the stage card at its
midway), six mechanism cards, the Bloomberg test rows, the 16-step timeline
(rule 5 anchor measurement, stable arrow top across steps), voices/camps/takeaways
counts, explore links, 21 sources, the zero em/en dash scan, and arrow-key routing
to whichever stepper is on screen. A pageerror fails the run.

Quirks: two steppers share one keydown handler by design; the handler routes by
which stage is on screen. The illustration is generated via the Codex CLI image
generator (never the Muse media pipeline); the figure ships unhidden only when
images/moat.webp exists.
