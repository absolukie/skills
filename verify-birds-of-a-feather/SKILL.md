---
name: "verify-birds-of-a-feather"
description: "Re-run verification for the primer 'Birds of a Feather, Playable' at lukezhang.si/blog/birds-of-a-feather/: feature map, Playwright harness (including a full real-tap playthrough of the playable demo), and last report live in the draft's verify folder."
---

# Verify: Birds of a Feather, Playable

Live URL: https://lukezhang.si/blog/birds-of-a-feather/
Draft (canonical source): `~/workspace/blog-drafts/birds-of-a-feather/index.html`
Illustration: `images/nests.webp` in the draft folder (Codex ink illustration: birds carrying blank cards to three nests, one hesitant bird in a rust-red scarf).
The game itself: https://birds-of-a-feather.pages.dev/ (private repo absolukie/birds-of-a-feather; local source `~/workspace/birds-of-a-feather/`).

## Run it

```bash
cd ~/workspace/blog-drafts/birds-of-a-feather/verify
python3 verify.py            # local draft on a throwaway server
python3 verify.py <url>      # any served URL
```

The harness drives the real UI at 390x844. The demo suite plays the miniature level with real taps: asserts 4 nests, 12 cards, 1 ambiguity dot at the default knob, makes a deliberate wrong placement (feather drops to 2), calls the Oracle (message check), then homes every remaining card via its data-home attribute (the harness reads board state, never calls handlers) to the win panel; then turns ambiguity to 3 (3 dots), switches to stock mode (8 open cards), draws (waste top appears), homes the waste card. Plus: Fig 2 deduction stepper (5 steps), Fig 3 band explorer (5 chips, endgame panel), 6 mechanism cards, fairness callout, 5-step timeline, voices/camps/takeaways counts (5/2 agree + 2 versus/6), section order, 3 sources, computed-style and content-inset assertions, zero pageerrors, zero horizontal overflow. Writes `REPORT.md` and screenshots to `shots/` on every run.

Feature map: `~/workspace/blog-drafts/birds-of-a-feather/verify/FEATURE_MAP.md`
Last report: `~/workspace/blog-drafts/birds-of-a-feather/verify/REPORT.md`

## Content invariants (do not let an edit break these)

- The game's certified numbers: quota-elimination prover passes 200 of 200 Journey levels and 90 of 90 sampled daily seeds; par is A*-proven per level (8 at level 1, 35 at the endgame) and ships in a content-hashed table; band stats come from the project's QA notes (61-80 about 20.25 cards/3.70 ambiguous, 81-120 22.77/5.25, 121-160 24.77/6.28, 161-200 25/8.05 with 54 three-flock cards); level 6 has exactly one ambiguous card (orange), level 60 has 7 ambiguous of 25 cards and 3 feathers; the semantic review removed 60+ weak links across 34 pools; the field guide holds 478 pixel-art portraits over 477 unique words.
- The demo must keep its honesty properties: every deal is certified by the in-page two-rule prover (quota elimination to fixpoint, assignment equals intended homes) before render; ambiguous cards are marked with the rust dot; the footer lists the miniature's simplifications (12 cards, one redeal instead of two, Oracle names a guaranteed home rather than the A*-optimal move).
- Felt fairness of the endgame is stated as UNVERIFIED (the project's own QA caveat). Do not upgrade that claim.
- birds-of-a-feather.pages.dev does not answer curl from this VM (connection failure, 000) though it loads in browsers and was independently fetched in an earlier session; do not treat the 000 as downtime.

## Quirks

- Playwright against the live URL fails through this VM's proxy (ERR_TUNNEL_CONNECTION_FAILED). Live proof is curl: page, image, and /primers/ return 200, and served page bytes equal the draft plus exactly 248 bytes (Luke's analytics beacon).
- The band panel heading renders uppercase via CSS, so text assertions on it must be case-insensitive (inner_text returns the transformed text).
- Stepper arrows use the template's car-arrow system (buttons inside a .tl-stage wrapper, tops set by JS to the stage midway on every render). Stepper totals must equal data-row counts exactly.
- The demo re-renders its card and nest DOM on every state change; harnesses must re-query locators per action, and selection clears on draw/redeal by design.
- Retrofits 2026-10-13 (Luke: the page was not applying the new skill rules): (1) the full compatibility style layer for the shell's other markup dialect (voices, camps, splits, chips, timeline card, keep-exploring, notes, callout label, mechanism headers), same repair as the streaming primer; the static guard python3 ~/workspace/tools/css_audit.py now reports 0 unexplained orphans with css-audit-allow.txt covering the six benign hooks. (2) Rule-16 swipe and tap gestures on both steppers (#dedStage, #tlBody) via wireStepper goNext/goPrev; the playable game surface deliberately has NO stepper gestures. Harness grew to 73/73 with computed-style assertions for the styled components and dispatched-PointerEvent gesture suites. Note: parallel harness runs can collide on the local server port and serve the wrong page (seen tonight against knowledge-cutoff); rerun before believing a loads_clean failure.
