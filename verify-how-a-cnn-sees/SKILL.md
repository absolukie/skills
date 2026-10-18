---
name: verify-how-a-cnn-sees
description: Verify the CNN primer (lukezhang.si/blog/how-a-cnn-sees/) against its feature map by running the Playwright harness, which drives the real UI (live network, sample chips, real file upload, inspector, steppers) and asserts the in-browser network's parity with the torch-trained manifest.
---

# Verify Watch a CNN See

Feature map: `~/workspace/blog-drafts/how-a-cnn-sees/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/how-a-cnn-sees/verify/verify.py` (local port 8925)

Run it:

```
python3 ~/workspace/blog-drafts/how-a-cnn-sees/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The network: trained by `~/workspace/cnn-train/train.py` (PyTorch CPU, CIFAR-10 from Hugging Face parquet mirrors after the Toronto download crawled), 30 epochs, final test accuracy 0.769. weights.json (1.3 MB) and samples/ (6 test photos + manifest with torch predictions) ship beside the page. Parity was proven twice: numpy forward from weights.json reproduces the torch manifest to 4 decimals, and the harness's sample_parity_all_6 check makes the page's own JS agree on all six samples through real chip clicks. The upload path is exercised with a real file through the real input (set_input_files), never by calling handlers.

Invariants the harness guards:
- Probabilities sum to 100 (within rounding); 10 prediction rows; 6 sample chips; 3 stage blocks; 16 filter canvases; 80 pre-pool map cells.
- Inspector: stage 1 map tap shows 3 patch grids of standardized values whose stated arithmetic agrees with the cell value (normalization is part of the computation; showing raw 0-255 patches would not reproduce it).
- Parameter stepper: 5 layers light cumulatively to 81,290; FC1 bar renders wide (guards the scoped .fn-fill width trap: widths only apply under #paramRows .fn-row.on / #raceRows and fills need display:block).
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson).
- Card chevron SVG renders at 20px (mech_chev_sized): the shell's .chev rule sets no size, so without the page's own .chev{width:20px;height:20px} rule the icon renders at full card width (Luke's 2026-10-14 screenshot; the same fix shipped to 8 sibling primers).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (cards, fhead, voices, xicon, meta, nokatex).
