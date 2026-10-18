---
name: verify-rotation-matrices
description: "Verify the Rotation Matrices at Work primer: re-run its Playwright harness (live matrix bench, worked-example stepper, composition lab, timeline) against the draft or the live page."
---

# Verify: Rotation Matrices at Work

Primer: https://lukezhang.si/blog/rotation-matrices/
Draft: ~/workspace/blog-drafts/rotation-matrices/index.html
Harness: ~/workspace/blog-drafts/rotation-matrices/verify/verify.py (private port 8923; pass a URL argument to test the live page instead of the local draft)
Feature map: ~/workspace/blog-drafts/rotation-matrices/verify/FEATURE_MAP.md

Run: `python3 ~/workspace/blog-drafts/rotation-matrices/verify/verify.py` (79 checks; REPORT.md + shots/ land beside it). The harness also covers the six mechanism-card visuals added 2026-10-15 (column explorer, pinned-axis switcher, cyclic ring + real/naive Ry toggle, composition lanes, pipeline tap stepper, gimbal + drift) and the KaTeX guards (katex.min.css in document.styleSheets, .katex-mathml computed position absolute).

Load-bearing assertions: Rz at 90 degrees prints its first column as (0, 1, 0) in the bench grid; Rz at 0 is the identity; the composition lab at 90/90 reports Frobenius distance 2.45 with probe results (0,-1,0) and (1,0,0) and the exact product matrices; zeroing theta x merges the orders to distance 0.00. Cubes are checked by canvas pixel diversity (real painted faces, redraws when theta changes), not by DOM state.

Quirks:
- Gesture suites must run before real arrow clicks OR the page's click swallower (400ms after a consumed gesture) eats the first arrow click; the page exempts .car-arrow clicks from the swallow, which is what makes the harness order safe. Keep that exemption.
- The renderer once shipped with face centers set to cube corners (faces splayed like panels); the pixel-diversity check passed anyway because panels are colorful. Only the screenshots caught it. Always view 02-bench.png and 05-lab.png after a run: you should see three coherent cubes with sticker grids and one pinned axis arrow each.
- The bench autoplays its sweep; the harness pauses via the slider (dragging sets playing=false) before asserting readouts.
