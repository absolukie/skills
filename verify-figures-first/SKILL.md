---
name: "verify-figures-first"
description: "Verify the Figures First primer (lukezhang.si/blog/figures-first/): run its Playwright harness against the feature map and read the report. Use before and after changing the primer, or when Luke asks whether it still works."
---

# Verify: Figures First primer

Live URL: https://lukezhang.si/blog/figures-first/
Draft source: ~/workspace/blog-drafts/figures-first/ (index.html assembled by splice.py from body.html + extra.css + the softmax primer's shell; regenerate with `python3 splice.py` after editing body.html or extra.css, never edit index.html directly).

Feature map: ~/workspace/blog-drafts/figures-first/verify/FEATURE_MAP.md
Harness: ~/workspace/blog-drafts/figures-first/verify/verify.py (Python Playwright, real UI, 390x844)
Report: ~/workspace/blog-drafts/figures-first/verify/REPORT.md (rewritten every run)

Run locally: `cd ~/workspace/blog-drafts/figures-first/verify && python3 verify.py`
Run against live: `python3 verify.py https://lukezhang.si/blog/figures-first/`

Coverage (44 checks): hero/tags/images, storyboard stepper (5 steps, arrow anchoring, terminal arrows hidden), 7 rule cards, cue lab (4 scenarios with the paper's exact values and bar widths), KaTeX pass@k formula with worked numbers, design lab (spacing gap swap, color shuffle), timeline (14 stops), voices/camps/takeaways counts, explore cards, sources count, zero page errors, no horizontal overflow.

Quirks:
- Numbers come in two author-published sets (paper vs project page). The primer deliberately uses the paper's runs and says so on the page; do not "fix" this.
- The BusinessWire Leo release URL bot-blocks scripted fetches (curl 000, text fetch 500) but loads fine in a real browser (verified 2026-10-13). Do not declare it dead from scripted fetches; check it in the managed browser. The Sources section cites both the release and the BioRender Leo product page.
- KaTeX is vendored inside the primer folder (katex/), same as sibling primers.
- Layout repairs 2026-10-13 (Luke's screenshots): the step-1 .br rows crushed their text beside the verdict chips, the rule-card headers crushed title and teaser beside a viewBox-only chevron SVG that ballooned to fill the row, and the stepper viz sat tight against the following paragraph. Fixes live as CSS overrides after the .branch rules: .br wraps with its text span at flex 1 1 190px, the fcard title span flexes with min-width 0, .fchev is pinned to 20px, .branch bottom margin is 14px, and #ffStepperViz carries 36px bottom margin. The harness asserts the geometry (br text at least 150px, chevron 14 to 26px, card title at least 170px, viz-to-next-paragraph gap at least 30px); total 48/48. Generalized as visualizers cross-pattern rule 17.
