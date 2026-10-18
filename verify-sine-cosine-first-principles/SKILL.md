---
name: verify-sine-cosine-first-principles
description: Verify the sine and cosine primer (lukezhang.si/blog/sine-cosine-first-principles/, "Sine and Cosine From First Principles") against its feature map by running the Playwright harness, which drives the real UI (unit-circle stepper, squeeze slider, mechanism cards, derivative derivation stepper, series builder, timeline) and asserts computed styles, rendered geometry, and the numeric readouts against hand-computed values.
---

# Verify Sine and Cosine From First Principles

Feature map: `~/workspace/blog-drafts/sine-cosine-first-principles/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/sine-cosine-first-principles/verify/verify.py` (local port 8950)

Run it:

```
python3 ~/workspace/blog-drafts/sine-cosine-first-principles/verify/verify.py            # local draft
```

Live URL runs fail in this VM (host bot protection blocks the headless browser); verify live by curl 200s plus served bytes = draft + 248.

The page's readouts must reproduce the arithmetic computed independently during the build (Python, double precision): squeeze at h = 0.1 gives cos h = 0.995004 and sin h/h = 0.998334; at h = 0.01 the ratio is 0.999983 and the trap window (1 - cos h) is 0.000050 wide; at h = 0.8 the ratio is 0.896695 over cos h = 0.696707. The series builder's totals for sin(0.5) run 0.5, 0.4791666667, 0.4794270833, 0.4794255332, 0.4794255386. The harness asserts these strings from the rendered UI, not from the source.

Invariants the harness guards:
- Four interactive visualizers plus timeline: circle stepper (6 stops, exact and decimal readouts), squeeze slider (6 h stops, squeeze bar marker strictly between cos h and 1), derivation panel stepper (6 steps, terminal arrow hidden), cumulative series stepper (rows light cumulatively), timeline (7 events).
- Five expansion visualizers (added 2026-10-15 for Luke's five questions): radians unwrap stepper (5 stops, radius copies on the arc and on an unrolled strip, 1 radian = 57.2958 degrees, full turn 2 pi radii = 6.2832); addition-formula derivation (6 panels, x = 50 degrees, h = 10 degrees, red term sin x cos h = 0.7544065 and blue term cos x sin h = 0.1116189 lit in the picture and in the KaTeX formula via textcolor, asserted by computed span color, sum 0.8660254); tangent slider (7 stops, segment on the tangent line x = 1 asserted geometrically at 60 degrees, tan = 1.732051, blow-up 57.289962 at 89 degrees); chord stepper (4 parts, Ptolemy's entries 37;4,55 / 60;0,0 / 1,24;51,10 against 2 sin of half the angle); name-chain stepper (5 hops, chord to jya to jayb to sinus to complementi sinus, Gunter 1620). Sources grew 10 to 13 with the expansion.
- Steppers: rule-5 arrows 46px, tops anchored at the anchor element's midway (JS-measured), terminal arrows display:none, tap-stage advances, dispatched-pointer swipes move both ways, dots and counts track.
- Mechanism cards: 6, first open by default, third card toggles through its real header button, chevron SVG renders at 20px, card bodies contain rendered KaTeX. Every card body opens with a styled .cviz visual (asserted first child, wide, paper background, border); card 1's cos/sin chips dim the other coordinate group and update the readout.
- Display math centering: every visible .eqbox's .katex center sits within 6px of the box center, asserted at load, at the squeeze box, and at derivative steps 2 and 5 (the .katex-display flex rule in the page's own style block).
- KaTeX stylesheet loaded and .katex-mathml computed position absolute (the rotation-matrices lesson).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` in the draft dir, with the draft's css-audit-allow.txt (feel-physics allowlist minus nokatex). This page's head is the feel-physics superset head copied through </head>; its own style block authors .sc-panel/.sc-cap, .uc-wrap/.uc-svg, .sc-reads, .sqbar/.sq-fill/.sq-mark/.sq-labs, .tblwrap/.tbl, .worked/.wlab/.wstep.
- Card, voice, and timeline builders use the donor dialect exactly: fcard > button.fhead (ftag, ftitle, svg.chev at 20px) + .fbody toggled by inline display; voice > .v-name/.v-role/.v-text/.v-link; timeline children .tl-yr/.tl-title/.tl-b. An earlier build of this page used fc-top/vhead/tl-t classes that the head does not define; the audit caught it. Do not reintroduce them.
