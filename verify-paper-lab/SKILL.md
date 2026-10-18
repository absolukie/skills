---
name: verify-paper-lab
description: Verify the Paper Lab primer (lukezhang.si/blog/paper-lab/, "The Paper Lab, Recreated") against its feature map by running the Playwright harness, which drives the real UI (live fluid solver with method switch and sliders, validation traces, orchestration feed, agents panel, mechanism cards, advection stepper with gestures, method race, timeline) and asserts measured solver behavior, computed styles, and rendered geometry.
---

# Verify The Paper Lab, Recreated

Feature map: `~/workspace/blog-drafts/paper-lab/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/paper-lab/verify/verify.py` (local port 8927)

Run it:

```
python3 ~/workspace/blog-drafts/paper-lab/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's solver is a real stable-fluids implementation (semi-Lagrangian advection + pressure projection). Two solver details are load-bearing and were found by measurement, not by reading: the projection must use a consistent forward-difference divergence / backward-difference gradient pair (a central-difference pair composes to a wide-stencil Laplacian the Jacobi solve never zeroes, and the dye sum drifted to 219 percent), and the pressure solve must be warm-started from the previous step's pressure (cold starts leave the smooth divergence modes behind; warm start holds the race blob at about 98 percent of its dye over 60 steps at dt 0.2). The explicit Euler mode is the differential form, which is unconditionally unstable for advection: in the race it crosses max speed 6 around step 14 and overflows; the page freezes it at the last finite state and reports the step. In the lab, a blow-up zeroes the velocity via the auditor and logs a FAIL line to the feed.

Invariants the harness guards:
- Lab: mass retained decays under the default dissipation; the post-projection divergence readout stays under 0.05; method switch changes the running scheme and logs method_switch to the feed; the dt slider updates its readout; Pulse logs dye_pulse; agents panel has 12 rows whose bars advance; the arc web canvas is nonblank and animating.
- Race: finishes; semi-Lagrangian mass retained lands between 80 and 110 percent; the explicit side reports "blew up at step".
- Mechanism cards: 6, third card toggles through its real header, chevron SVG renders at 20px (the shell's .chev rule sets no size; the page's own rule does, the bug Luke caught 2026-10-14 on the CNN primer).
- Advection stepper: 5 rows light cumulatively, terminal next arrow hides, dispatched-pointer swipes move both ways. Timeline: 8 entries, count advances, terminal next hides.
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson).
- Widget containers are not selectable text: computed `user-select` on `.viz` is `none` (viz_no_text_select, added 2026-10-15 per visualizers rule 19).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt. The page authors its lab/race component classes (.lab-*, .race-*) in its own style block; the allowlist covers only proven-benign hooks.
- Honesty invariants: the lede and footer state the Cherny claim is single-source and unverified; the 7 + 4 tally is described as counting methods, not scenes.
