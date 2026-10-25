---
name: verify-tesla-battery-machine
description: Verify the Tesla Battery Machine figure (projects.lukezhang.si/tesla-battery-machine): run its Playwright harness against the feature map and read the report. Use before and after changing the figure, or when Luke asks whether it still works.
---

# Verify the Tesla Battery Machine

The figure is a single standalone page: an isometric Model 3 Long Range
battery pack the reader runs through 8 gated steps, with every gauge
reading from one in-page model of the pack.

- Draft: `~/workspace/blog-drafts/tesla-battery-machine/index.html`
- Live: https://projects.lukezhang.si/tesla-battery-machine/
- Feature map: `~/workspace/blog-drafts/tesla-battery-machine/verify/FEATURE_MAP.md`
- Harness: `~/workspace/blog-drafts/tesla-battery-machine/verify/verify.py`
  (Python Playwright, serves the draft on port 8962, drives the real UI
  at 390x844: full step walk by tapping the actual buttons, only-next-live
  gating asserted at every step, DOM gauges compared against the page
  model's own state plus sourced anchors, motion continuity sampling on
  the two long steps, sound-word pops, reset, keyboard advance with the
  Space-fires-once guard, dark-card legibility, zero page errors.)
- Results: `~/workspace/blog-drafts/tesla-battery-machine/verify/results.json`
- Screenshots: `~/workspace/blog-drafts/tesla-battery-machine/verify/shots/`

Run it:

```
python3 ~/workspace/blog-drafts/tesla-battery-machine/verify/verify.py
```

A green run ends with `== n/n passed ==` and every check ok in
results.json. Read the screenshots after any run that changes the
drawing; the harness counts behaviour, not beauty.
