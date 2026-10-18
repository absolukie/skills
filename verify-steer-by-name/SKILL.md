---
name: verify-steer-by-name
description: Verify the poteto principles primer (lukezhang.si/blog/steer-by-name/, "Steer by Name") against its feature map by running the Playwright harness, which drives the real UI (measured principle index explorer, steering lab, mechanism cards, Bend2 stepper with gestures, timeline) and asserts computed styles, rendered geometry, and the measured line-count data.
---

# Verify Steer by Name

Feature map: `~/workspace/blog-drafts/steer-by-name/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/steer-by-name/verify/verify.py` (local port 8952)

Run it:

```
python3 ~/workspace/blog-drafts/steer-by-name/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's data is measured, not typed from memory: the 24 principle files in cursor/plugins (pstack/skills/principle-*) counted with wc on October 14, 2026 total 455 lines, median 18.5, min 9 (exhaust-the-design-space), max 34 (boundary-discipline). If the repo changes, re-count before trusting the harness's px checks. The steering lab's character counts are computed live from the displayed strings; its ratio check accepts 3.0 to 6.5.

Invariants the harness guards:
- Index explorer: 24 rows under All, 5 under Verification. Multi-open inline expansion (rebuilt 2026-10-15 per explainer-tools rule 8, replacing the old single shared detail panel): tapping a row expands its text under its own header, opening never closes a sibling, tapping an open row closes only it, expansion never scrolls or moves another header, Attack the Premise (23 lines) starts open, open state survives filter round-trips, and Open all / Close all act on the currently filtered set. Boundary Discipline's bar fills its track (it is the max), name column at least 160px wide at 390px.
- Steering lab: name version 1 mentions subtract-before-you-add; the displayed character count equals the string's real length.
- Mechanism cards: 6, third card toggles through its real header, chevron SVG renders at 20px (shell .chev rule).
- Bend2 stepper: 6 rows light cumulatively, the census row's fill measures about 96 percent of its track (the fill rule is scoped #bendRows in the page's own style block; the shell only defines it for #blendRows and .sb-row), terminal next arrow hides, dispatched-pointer swipe goes back one, arrows are 46px and document-stable.
- Stepper arrows are placed by the page's placeArrows script at the anchor midway (timeline anchor = first entry's measured height unless it exceeds 1.5x the smallest, with the card min-height set to the anchor). The harness asserts the timeline arrow's center sits on the card and its bottom stays off the count row.
- Timeline: 8 entries, starts at "Start of 2026", ends at "Twenty, then twenty-four", count reads 8 of 8 (inner_text is CSS-uppercased; compare lowercase).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (cards, fhead, voices, xicon, fn, tl). No KaTeX on this page by design (no math; counts are arithmetic in prose and live-computed), so there are no katex checks.
