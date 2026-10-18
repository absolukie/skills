---
name: verify-pyramid-drawn-by-circles
description: Verify the primer "A Pyramid Drawn by Circles" (lukezhang.si/blog/pyramid-drawn-by-circles/) against its feature map by running the Playwright harness, which drives the real UI (Figure 1 epicycle machine with its example gallery and custom drawing pad, mechanism cards, build stepper, error lab, timeline) and asserts the page's Fourier coefficients and worst-miss tables against independently computed values.
---

# Verify A Pyramid Drawn by Circles

Feature map: `~/workspace/blog-drafts/pyramid-drawn-by-circles/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/pyramid-drawn-by-circles/verify/verify.py` (local port 8955)

Run it:

```
python3 ~/workspace/blog-drafts/pyramid-drawn-by-circles/verify/verify.py            # local draft
python3 ~/workspace/blog-drafts/pyramid-drawn-by-circles/verify/verify.py https://lukezhang.si/blog/pyramid-drawn-by-circles/   # live
```

The page rebuilds Math Pulse's October 16, 2026 video from its construction: square pyramid, base corners (±1, 0, ±1), apex (0, √2, 0), one closed 11-beat route (10 legs, two base edges retraced), one real Fourier chain per coordinate. Numbers the harness pins, all computed independently in Python (research_notes/mathpulse-image-20261016/compute.py):

- Chain anchors (means): x = z = 1/11 ≈ 0.0909, y = 2√2/11 ≈ 0.2571.
- First circles: x: a₁ = 0.9496, b₁ = 0.1395 (R₁ = 0.9598); y: a₁ = −0.1361, b₁ = 0.1571 (R₁ = 0.2079).
- The 11th harmonic is exactly zero for every axis (the route's 11-beat rhythm cancels it).
- Worst miss, percent of the base diagonal 2√2, 8,192-point grid: N = 1 → 48.52, N = 10 → 5.94, N = 100 → 0.68. The post's printed claims are 48.3 / 5.86 / 0.666; the page prints both sets and explains the grid gap.

If a check fails after an edit, compare against those values before assuming the harness is wrong: the coefficients come from the exact slope-jump formula and were cross-validated against an 8,192-point FFT to 3e-8.

Since the October 16, 2026 generalization, Figure 1 is a general closed-path machine: 14 built-in examples (5 solids as genuine closed edge trails, 4 space curves, 5 flat drawings) plus two custom modes (a pointer drawing pad resampled to 240 points with Flat/Dome/Twist lifts, and a paste-points box). The pyramid core above is untouched and still feeds the cards, the build stepper, and the error lab; the gallery runs on a parallel engine (`coefFromKnots` / `errFromKnots`) using the same slope-jump math, with every path centered and scaled so its own diameter is 2√2. Extra pins the harness checks, computed independently in Python from the same path definitions (4,096-point grid): cube (16 trail points) worst miss 59.211 / 3.982 / 0.942 percent at N = 1 / 24 / 100, mean 0.894 at N = 24, first x circle a = 0.3106, b = 0.4648; torus knot (720 points) worst 0.002 and heart (720 points) worst 0.001 at N = 24. Smooth curves converge almost immediately; corners are what cost circles.
