---
name: verify-already-clean
description: Verify the Already Clean primer (lukezhang.si/blog/already-clean/, "Already Clean: The Neurons Were Readable All Along") against its feature map by running the Playwright harness, which drives the real UI (legibility census scenarios, mechanism cards, neuron-audit stepper with gestures, audit-cost estimator, legibility bars, timeline) and asserts computed styles and the census arithmetic.
---

# Verify Already Clean

Feature map: `~/workspace/blog-drafts/already-clean/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/already-clean/verify/verify.py` (local port 8942)

Run it:

```
python3 ~/workspace/blog-drafts/already-clean/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's numbers are fixed by primary sources and must not drift: Qwen3-32B config (64 layers, 25,600 intermediate, 5,120 hidden) gives 1,638,400 MLP neurons and 3,276,800 poles; the packing substitution (n = 5120, epsilon = 0.1) gives exponent 12.8 and about 362,000 directions; the estimator at 10 minutes per neuron must read 31.2 years nonstop, 131 work-years, 11.4 days for a 1,000-agent fleet.

Invariants the harness guards:
- Hero: hero_img_fits asserts the hero image's own bounding box fits the .wrap column at 390 px (fixed 2026-10-15: the img carried class "hero", a padding rule, instead of "hero-img", so it rendered at 1200 px intrinsic width mostly off-screen while page overflow stayed clean).
- Census: 100 dots; Qwen scenario renders 90 one-job, 7 two-job, 3 unknown; the 2023 scenario renders 2 legible; the retrained InceptionV1 scenario renders 99; accent dot color is the real computed accent.
- Mechanism cards: 6, second card opens through its real header, chevron SVG renders at 20px.
- Audit stepper: 6 cumulative rows, terminal next arrow display none, tap advances, real mouse swipe advances and returns, first claim at least 160px wide at phone width.
- Estimator: slider driven by real keyboard input; readouts recompute.
- Bars: 4 rows at true scale (1.7 percent bar is a sliver, 99 percent bar nearly full).
- Timeline: 7 events, count text, terminal arrow hides.
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (feel-physics list plus cg-grid, cg-leg, lbRows).
