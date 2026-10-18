---
name: verify-drone-geometric-control
description: Verify the drone geometric control primer (lukezhang.si/blog/drone-geometric-control/, "Flying on the Sphere") against its feature map by running the Playwright harness, which drives the real UI (attitude lab slider/flip/recover/gimbal-lock readouts, mechanism cards, control-cycle stepper with gestures, allocation lab presets, timeline) and asserts computed styles and geometry readouts.
---

# Verify Flying on the Sphere

Feature map: `~/workspace/blog-drafts/drone-geometric-control/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/drone-geometric-control/verify/verify.py` (local port 8948)

Run it:

```
python3 ~/workspace/blog-drafts/drone-geometric-control/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's Figure 1 recovery integrates the real moment law reduced to one tilt axis (M = -0.55 sin(theta) - 0.2 omega, J = 0.02). Its readouts must reproduce the geometric error arithmetic: at 30 degrees, |e_R| = 0.500 and Psi = 0.134; at exactly 180 degrees Psi = 2.000 with |e_R| = 0.000, and Recover does nothing there until a nudge. At 90 degrees of pitch the Euler readout must flag gimbal lock. The allocation lab must give a pure M1 of +0.250 N m on the Roll preset and a pure M3 of +0.032 N m on the Yaw preset, with hover tau at 14.72 N for the 1.5 kg FDCL machine.

Invariants the harness guards:
- Hero image: the img carries the hero-img class and its rendered box fits the .wrap column at 390px wide. (2026-10-15 fix: the img shipped wearing the section class "hero", so no width rule applied and it rendered at its intrinsic 1200px, clipped off the right edge on phones, while document scrollWidth still read clean. The harness now asserts the hero's bounding box directly.)
- Attitude lab: 2 axis chips; slider sets tilt; Flip lands on 170; Recover brings tilt back to 0.0 within a few seconds; gimbal lock chip appears at 90 degrees pitch.
- Mechanism cards: 6, third card toggles through its real header, chevron SVG renders at 20px.
- Cycle stepper: 6 rows light cumulatively, terminal next arrow hides, dispatched-pointer swipes move both ways.
- Allocation lab: 4 sliders; hover/Yaw/Roll preset readouts match the allocation matrix.
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt. SVG rotor classes (rot-disc, rot-base, rot-lab, rot-val) are defined in the page's own style block; the fn-fill width rule is scoped to #cycRows.
