---
name: "verify-open-cad-kernel"
description: "Verify the Open CAD Kernel primer (NVIDIA open-sourced SMLib, lukezhang.si/blog/open-cad-kernel/): run its Playwright harness against the feature map and read the report. Use before and after changing the primer, or when Luke asks whether it still works."
---

# Verify: Open CAD Kernel primer

Live URL (after the coordinator publishes): https://lukezhang.si/blog/open-cad-kernel/
Draft source: ~/workspace/blog-drafts/open-cad-kernel/ (index.html assembled by splice.py from body.html + extra.css + the softmax primer's shell; regenerate with `python3 splice.py` after editing body.html or extra.css, never edit index.html directly).

Feature map: ~/workspace/blog-drafts/open-cad-kernel/verify/FEATURE_MAP.md
Harness: ~/workspace/blog-drafts/open-cad-kernel/verify/verify.py (Python Playwright, real UI only, 390x844, local server on port 8947)
Report: ~/workspace/blog-drafts/open-cad-kernel/verify/REPORT.md (rewritten every run; the notes appendix at the end is hand-appended, re-add it after a re-run if it matters)

Run locally: `cd ~/workspace/blog-drafts/open-cad-kernel/verify && python3 verify.py`
Run against live: `python3 verify.py https://lukezhang.si/blog/open-cad-kernel/`

Coverage (109 checks, all passing 2026-10-14): hero/tags/images and the legacy-license lede line; all 5 mechanism cards open and close with computed display flips and aria-expanded; cube stepper all 5 stages with running counts, 46px edge-straddling arrows at a stable top, terminal arrows display:none, dots plus count, tap-to-step exactly once, a real-mouse 100px swipe stepping exactly once with the 400ms post-swipe click guard verified, arrow keys stepping on screen and doing nothing while the slider has focus; NURBS KaTeX formula with legend and worked numbers (denominator 1.5, C(0.5) = (1, 0.667)); NURBS lab driven by Home/End/arrow keys and a track click (w=0 switched-off insight, w=0.70 exact-circle insight, w=2.00 after a keyboard nudge giving exactly (1.000, 0.667), canvas red-pixel paint check, slider touch-action pan-y); Euler lab all 5 shapes with substitution strings, exactly one aria-pressed chip, monospace computed style, and the through-hole trap (16 − 24 + 10 − 2 = 0 against 2(1 − 1) = 0); license wall both years with only the SMLib chip flipping and Parasolid byte-identical; honesty callout (remove_fillet, 1.4 percent); timeline all 16 stops both directions with the May 2022 acquisition flagged secondary; 7 voices with the Hemmelgarn timing caveat, 3 camps, 2 versus sides, the no-analyst-forecast note; takeaways (5 bullets, conclusion 76 words); 4 explore cards with link-out icons and live slugs; 23 source cards; zero page errors; scrollWidth at most 390.

Quirks:
- The NURBS slider is an integer range 0 to 300 in steps of 5, divided by 100 in code, so one arrow press is exactly 0.05 and keyboard values are exact. A track click lands within a step or two of the target, never exactly on it: the harness clicks near two-thirds, asserts w lands in 1.9 to 2.1, then nudges with arrow keys to exactly 2.00 before asserting the (1.000, 0.667) midpoint. Do not "fix" the page for this; it is input physics, not a bug.
- The NURBS insight priority order in code: exact circle first (|w − 0.7071| ≤ 0.03), then w < 0.05, w < 0.95, w ≤ 1.05, else above 1. At w = 0.70 the readout midpoint is (1.000, 0.412), not 0.4142, because the slider's 0.05 step cannot land on 0.7071 itself; the insight text names cos(45 degrees) as the exact value.
- Canvas midpoint x is always 1.000 by symmetry; y at u = 0.5 is w / (1 + w).
- The swipe test must use real mouse input (Playwright mouse.down/move/up), not touchscreen taps: the page listens on pointer events, and the click synthesized right after mouse.up is exactly what the 400ms guard exists to swallow. The harness then clicks deliberately inside the guard window (must not step) and again after it (must step).
- Euler substitution strings use the U+2212 minus sign (&#8722; in the JS template); the harness compares with the same character.
- The Siemens Parasolid product page failed curl and text fetch during research and is deliberately NOT cited; the Sources entry is the Siemens PLM Components brochure PDF (HTTP 200). All 23 source URLs and the 4 keep-exploring slugs were curl-verified 200 on 2026-10-14.
- KaTeX is vendored inside the draft folder (katex/), same as sibling primers. Illustrations are Codex-generated webp in images/ (hero 1200x800, curve 1200x675).
