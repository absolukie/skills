---
name: "verify-seedream-layers"
description: "Verify the Seedream layers primer at lukezhang.si/blog/seedream-layers: feature map and Playwright harness that drive the real UI (Separate slider, solo chips, subject swap and removal, mechanism cards, 9 step timeline)."
---

# Verify: Seedream Layers Primer

- Live URL: https://lukezhang.si/blog/seedream-layers/
- Draft: ~/workspace/blog-drafts/seedream-layers/index.html
- Feature map: ~/workspace/blog-drafts/seedream-layers/verify/FEATURE_MAP.md
- Harness: ~/workspace/blog-drafts/seedream-layers/verify/verify.py
- Last report: ~/workspace/blog-drafts/seedream-layers/verify/REPORT.md

Run it:
```
python3 ~/workspace/blog-drafts/seedream-layers/verify/verify.py            # live URL
python3 ~/workspace/blog-drafts/seedream-layers/verify/verify.py <path>     # local file
```

Quirks: the timeline uses visualizers rule 5 carousel arrows (46px edge straddling circles), not buttons: the next arrow must be display none at step 9, never disabled, arrow bounding boxes must be identical across steps, and the arrow centre must sit at the anchor card vertical midway. The remove subject check looks for the invented region wording in the readout plus the INPAINTED label in the figure, because the word inpainted lives in the figure, not the readout.

History: shipped 2026-10-12 with a Back and Next pill row that Luke flagged; replaced with the carousel arrows the same day (commit 0c22389), harness extended with three carousel checks, 13/13 green, live verified by curl.
