---
name: verify-handwired
description: Verify the Handwired primer (lukezhang.si/blog/handwired/, "Handwired: Written, Not Trained") against its feature map by running the Playwright harness, which drives the real UI (gate lab slider, mechanism cards, compile stepper with gestures, unfreeze lab train/reset, timeline) and asserts computed styles, rendered geometry, and the labs' arithmetic.
---

# Verify Handwired: Written, Not Trained

Feature map: `~/workspace/blog-drafts/handwired/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/handwired/verify/verify.py` (local port 8940)

Run it:

```
python3 ~/workspace/blog-drafts/handwired/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's arithmetic must reproduce the Handwired README example exactly: result = 12 - 2 * (relu(a - 4) - relu(a - 5)) for the program a > 4 ? 10 : 12. At a = 4.5 the gate lab reads relu values 0.50 and 0.00, gate 0.50, JS answer 10, net 11.00, slope minus 2. The unfreeze lab's numbers are computed in the harness run itself: at the default w = 5.5 the loss is 0.463 and 9 of 11 whole-number inputs are exact; Train (80 gradient steps, learning rate 0.05) lands at w about 4.21 with 10 of 11 exact; Reset restores w = 4, loss 0.000, 11 of 11.

Invariants the harness guards:
- Gate lab: slider drives reads and canvas; whole numbers match the JavaScript ternary exactly.
- Mechanism cards: 6, first open, second opens on a real tap, chevron SVG renders at 20px.
- Compile stepper: 6 cumulative rows, count text Step k of 6, terminal arrows display:none, arrows 46px centered on the rows container, dispatched-pointer swipes move both ways.
- Unfreeze lab: train and reset behave as above; the trained note keeps the words "still not exact".
- Timeline: 9 entries, arrows anchored at the first card's midway (card padded so text clears the arrows), terminal next hidden, swipe works.
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson); 3 display equations.
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` in the draft dir, with the draft's css-audit-allow.txt copied from feel-physics. Note the shell sizes .xlink svg at 20px (overriding the 14px attribute), as on every sibling primer; the harness asserts the shell size.
