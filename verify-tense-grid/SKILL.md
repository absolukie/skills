---
name: verify-tense-grid
description: Verify the tense grid primer (lukezhang.si/blog/tense-grid/, "The Tense Grid: Twelve Forms, Two Choices") against its feature map by running the Playwright harness, which drives the real UI (12-cell board with drawn timelines, sentence builder, stack stepper with gestures, 8-question quiz, timeline) and asserts exact conjugation strings and rendered geometry.
---

# Verify The Tense Grid

Feature map: `~/workspace/blog-drafts/tense-grid/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/tense-grid/verify/verify.py` (local port 8930)

Run it:

```
python3 ~/workspace/blog-drafts/tense-grid/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's content invariants: the board's 12 formulas and BNC shares come from Divjak and colleagues (Cognitive Linguistics, 2022; 7,006,666 verb phrases); the future perfect continuous is 30 cases, shown as "30 in 7M". The builder must conjugate the full matrix; the harness pins six exact sentences, including the brief's two: she + past + perfect continuous + paint = "She had been painting the fence for hours before the rain started." and they + future + perfect + paint = "They will have painted the fence by Friday." The builder's verbs (paint, drive, swim) deliberately differ from the board's locked studying example (Luke's 2026-10-15 call: each exhibit gets its own example).

Invariants the harness guards:
- Board: 12 cells, all formulas asserted exactly (corners included); a span cell's drawn bar exceeds 28 percent of the stage width after animation; the stage gets its .go class.
- Builder: chip groups switch by data-v; formula chips count is 4 for the full stack (will, have, been, main verb).
- Stack stepper: 5 cumulative rows, terminal next arrow display none, dispatched-pointer swipe advances.
- Quiz: a wrong first answer scores 0 with "Not quite." feedback and the right option highlighted; finishing gives 7 of 8; after Restart a clean run gives "scored 8 of 8".
- Timeline: 6 entries, card tap advances, terminal next arrow display none.
- No KaTeX on this page by design (Reichenbach orderings are plain notation); the shell head's katex stylesheet link is stripped. Do not re-add it.
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (copied from feel-physics) must report 0 unexplained orphans. The page's own style block defines the tb-*, stage-*, qz-*, fpart classes.
- Note: #tlCount text must be read via textContent, not inner_text (CSS uppercase). The .car-arrow elements take their vertical position from the shell's static-position pattern, matching sibling primers.
