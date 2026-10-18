---
name: verify-feel-physics
description: Verify the feel primer (lukezhang.si/blog/feel-physics/, "Move Like a Thing") against its feature map by running the Playwright harness, which drives the real UI (spring lab words/sliders/throw, mechanism cards, blend stepper with gestures, retarget race, timeline) and asserts computed styles and physics readouts.
---

# Verify Move Like a Thing

Feature map: `~/workspace/blog-drafts/feel-physics/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/feel-physics/verify/verify.py` (local port 8926)

Run it:

```
python3 ~/workspace/blog-drafts/feel-physics/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page is an independent RK4 implementation of the feel runtime's equation. Its readouts must reproduce feel's published vocabulary arithmetic: heavy (mass 3, 1.35 Hz, zeta 0.74) gives stiffness k 215.8, damping c 37.66, overshoot 3.2 percent; bouncy gives 27.5 percent overshoot; the blend stepper's "heavy, snappy" endpoint is k 543.6, c 63.0, overshoot 2.0 percent. Settle times are measured from the page's own simulation (feel's plus/minus 2 percent band definition) and may differ a few percent from feel's table; the harness allows 550 to 850 ms for heavy.

Invariants the harness guards:
- Lab: 6 word chips; throw moves the puck across the stage; sliders retune to zero overshoot at zeta 1.
- Mechanism cards: 6, third card toggles through its real header, chevron SVG renders at 20px (the shell's .chev rule sets no size; the page's own rule does — the bug Luke caught 2026-10-14 on the CNN primer).
- Blend stepper: 5 rows light cumulatively, terminal next arrow hides, dispatched-pointer swipes move both ways.
- Race: both modes run clean; canvases draw.
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (cards, fhead, voices, xicon, meta, nokatex, fn, tl). Note the CNN/pi shell head does NOT define camps/voices children, sb, btn, viz-t, eqleg, srcs, take, tl children classes; this page authors them in its own style block. Check the audit before assuming a sibling head covers a class.
