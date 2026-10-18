---
name: verify-unlimited-ocr
description: "Verify the 'Unlimited OCR, Checked' primer (lukezhang.si/blog/unlimited-ocr/): feature map, Playwright harness, and report. Run after any edit to the page."
---

# Verify: Unlimited OCR, Checked primer

Live URL: https://lukezhang.si/blog/unlimited-ocr/
Draft source: ~/workspace/blog-drafts/unlimited-ocr/index.html (canonical; deploy by
surgical overlay to blog/unlimited-ocr/ in absolukie/lukezhang-si, plus the image
at blog/unlimited-ocr/images/ribbon.webp)

Feature map: ~/workspace/blog-drafts/unlimited-ocr/verify/FEATURE_MAP.md
Harness: ~/workspace/blog-drafts/unlimited-ocr/verify/verify.py
Last report: ~/workspace/blog-drafts/unlimited-ocr/verify/REPORT.md

Run locally: `python3 ~/workspace/blog-drafts/unlimited-ocr/verify/verify.py`
Run live: `python3 ~/workspace/blog-drafts/unlimited-ocr/verify/verify.py https://lukezhang.si/blog/unlimited-ocr/`

The harness drives the real UI at 390x844: the 5-step claim-check stepper (verdict
sequence asserted label by label, terminal arrows hidden with display:none, arrows
straddling the panel at its midway and stable across steps), five mechanism cards,
the 7-row OmniDocBench bar table, the 6-row cost card, the 15-step timeline
(rule 5 anchor measurement), voices/camps/takeaways counts, explore links,
17-plus sources (18 since the build section was added), the zero em/en dash scan, and arrow-key routing to whichever stepper
is on screen. A pageerror fails the run.

Quirks: two steppers share one keydown handler by design; it routes by which
panel is on screen. The illustration is generated via the Codex CLI image
generator (never the Muse media pipeline); the figure ships unhidden only when
images/ribbon.webp exists.
