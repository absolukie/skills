---
name: verify-ten-pendulums-one-cart
description: Verify the cartpole primer (lukezhang.si/blog/ten-pendulums-one-cart/, "Ten Pendulums, One Cart") against its feature map by running the Playwright harness, which drives the real UI (coupled-cart pole-count slider, shove and nudge, coupling-proof hooks, mechanism cards, worked-step stepper with gestures, live ES trainer with reset, timeline) and asserts computed styles, rendered geometry, and the page's own state hook.
---

# Verify Ten Pendulums, One Cart

Feature map: `~/workspace/blog-drafts/ten-pendulums-one-cart/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/ten-pendulums-one-cart/verify/verify.py` (local port 8929, distinct from sibling primers' ports)

Run it:

```
python3 ~/workspace/blog-drafts/ten-pendulums-one-cart/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page is an independent implementation of Gymnasium CartPole dynamics (g 9.8, cart 1.0 kg, pole 0.1 kg, half-length 0.5 m, tau 0.02, Euler). Ground truth measured in the workspace (research: ~/workspace/research_notes/cartpole-ten-pendulum-20261014/): the worked step from state (0.10, 0.20, 0.10, -0.30) at F = +10 N gives temp 9.091, theta-acc -12.98 rad/s^2, x-acc 9.68 m/s^2, next state (0.104, 0.394, 0.094, -0.560). LQR gains K = [-3.1623, -5.9155, -49.5072, -12.8444] (scipy CARE, Q = diag(1,1,10,1), R = 0.1) held 300 of 300 random starts for 60 s offline. The evolution strategies trainer (mirrored pairs, pop 16, sigma 0.5, alpha 0.25, fitness = return difference over 2 episodes per candidate, center eval 5 episodes) is deterministic in-page via a seeded stream starting at 20261014: first-generation eval about 90, crosses the 475 solved bar around generation 12 (490), exactly as the harness's trainer screenshot shows.

Figure 1 ground truth (rebuilt 2026-10-15 as one cart with N coupled poles; do not regress to the old fleet of independent cartpoles): the sim integrates the Lagrangian system for a cart (1.0 kg) carrying N point-mass poles (0.1 kg each) on light rods, lengths on a log-spaced ladder from about 1.57 m down to 0.39 m (natural frequencies 2.5 to 5.0 rad/s), solving the full mass matrix each 0.02 s step; one force (cap 20 N) from one linear state-feedback law per pole count. Gains were solved offline from the linearized model (discrete Riccati, Q angle weight 40, R = 0.1): scipy in double precision at 1-2 poles, extended precision (mpmath Kleinman) at 3-8 poles, a weighted blend of per-pole LQR designs at 9-16 poles, because the coupled Riccati solve is numerically uncontrollable past that (controllability condition number passes 1e15 around 8 poles, and even the exact LQR law at 4 poles demands a mean of about 735 N from random starts, so no static linear law holds many parallel poles from generic starts; that cliff is the page's printed claim, measured with the shipped gains and seed: 300 starts, tilts/spins to 0.05, full minute: 300/300 at 1 and 2 poles, 120/300 at 3, 0/300 at 10, median first topple about 0.8 s). Shove is a cart velocity kick of 1.6 m/s (recovers cleanly at up to 3 poles); Nudge is a coherent 0.35 rad/s gust on a few poles. A pole past 0.65 rad folds flat for 0.7 s, counts as a topple, and is re-raised at a random tilt to 0.05; while folded it is out of the controller and the dynamics but its mass still rides the cart.

Invariants the harness guards:
- Coupled cart: hero_img_fits asserts the hero image's own bounding box fits the .wrap column at 390 px (the 2026-10-15 class bug: img carried class "hero", a padding rule, instead of "hero-img"). Slider taps/keys change the pole count for real (10 default, 16, 1, 3, back to 10) via `window.__cp.fleetCount()` plus chip text in poles-on-one-cart units; `poleBases()` all equal `cartState().x` plus fixed mount offsets before and after a shove; a shove moves the cart and swings at least two poles; `nudgePole(i, dw)` on one pole moves the cart (coupling proof); the topples chip tracks the page's counter.
- Trainer: pressing Train advances generations/episodes (~69 episodes per generation), best average return beats the first generation by 30+ and reaches 250+ within the bounded run; Reset zeroes episodes and retraining resumes. Assert improvement, not a fixed endpoint: ES eval noise is real.
- Steppers: 5 worked-step rows light cumulatively, terminal arrows display:none, tap on stage advances, dispatched-pointer swipe advances, timeline count text is uppercase ("2 OF 9") so compare case-insensitively.
- Stepper fill trap: the shell's base `.fn-fill` is an inline span; each container must add its own `#rowsId .fn-fill{display:block}` rule or the progress bars render empty (caught on this page's first harness run).
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson); the two-acceleration display is split into two eqboxes because the combined line overflows a phone viewport.
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` clean with the draft's css-audit-allow.txt copied from feel-physics.
