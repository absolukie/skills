---
name: verify-windmill-problem
description: Verify the windmill primer (lukezhang.si/blog/windmill-problem/, "The Windmill That Visits Every Point") against its feature map by running the Playwright harness, which drives the real UI (windmill lab steps on two point sets and both starts, mechanism cards, proof stepper with per-step diagram counts, trace stepper, timeline) and asserts the measured traces the page claims.
---

# Verify The Windmill That Visits Every Point

Feature map: `~/workspace/blog-drafts/windmill-problem/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/windmill-problem/verify/verify.py` (local port 8932)

Run it:

```
python3 ~/workspace/blog-drafts/windmill-problem/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's numbers are the ground truth the harness guards; they were measured with the workspace simulator at `~/workspace/research_notes/windmill-imo-2011/sim.py` (traces.json beside it) and the in-page lab must reproduce them exactly: meadow balanced start (pivot I, vertical) holds counts 4 and 4 at every rest state and completes all nine points at 157.2 degrees of total turn; the edge start (pivot H) holds 0 and 8 and visits only the seven hull points; the five point set (A(1,5), B(4,8), C(7,4), D(5,1), E(2,2)) completes at 135.00 degrees with sweep angles 18.43, 49.76, 31.26, 35.54, and its pivot cycle repeats every 180 degrees.

Invariants the harness guards:
- Lab: real Step clicks only (each animates one sweep, about 520 ms; the harness waits 780 ms); counts chips read "4 · 4" / "0 · 8" / "2 · 2" as innerText with the middot.
- Proof stepper: every step's inline SVG labels its own LEFT 2 / RIGHT 2 counts, computed from the state (pivot, theta) with a 0.01 degree nudge past the line; step 3 rings the old pivot B. If a diagram ever shows 1/3, the theta in PSTEPS has drifted from the true hit angle (71.5651 degrees for B to E).
- Trace stepper (rebuilt 2026-10-15 as a visual stage, rule 20): an SVG of the five point set with the line at the current angle, the swept sector shaded, visited pivots accent filled, and the current pivot ringed (hooks .tp/.tlab/.tline/.tsec/.tring in the css-audit allowlist); the harness asserts the drawing signature differs at every consecutive step, the sector appears from step 1, visited fills go 1 to 5, and the final readout shows 198.43 degrees with the 2 left, 2 right split.
- "The proof" section (added 2026-10-15): official IMO 2011 argument as a six step visual stepper on a generic seven point set (hooks .pp/.plab/.pring); balanced start, handoff invariant, and half turn steps must all show LEFT 3 / RIGHT 3 tallies in the drawing. Step 3 draws at 66 degrees, a few degrees past the true D to C hit angle (68.96), so the ringed old pivot D reads solidly on the side the new pivot came from; evaluating exactly at the rounded angle puts D within 0.02 degrees of the line and the tally flips to 2/4.
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson).
- Mechanism card chevron renders at 20px (the giant-chevron lesson).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (feel-physics list plus sb, wm, proof container hooks).
