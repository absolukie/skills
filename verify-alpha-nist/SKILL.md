---
name: "verify-alpha-nist"
description: "Verify the AlphaNIST primer (lukezhang.si/blog/alpha-nist/, 'The Robot That Taught Itself Assembly'): run its Playwright harness against the feature map and read the report. Use before and after changing the primer, or when Luke asks whether it still works."
---

# Verify AlphaNIST primer

The primer ships two custom video players modeled on the AlphaNIST project page, a KaTeX reward formula, a sampling stepper, a comparison, and a dot grid. Verification lives with the draft:

- Feature map: `~/workspace/blog-drafts/alpha-nist/verify/FEATURE_MAP.md`
- Harness: `~/workspace/blog-drafts/alpha-nist/verify/verify.py`
- Last report: `~/workspace/blog-drafts/alpha-nist/verify/REPORT.md`
- Draft: `~/workspace/blog-drafts/alpha-nist/` (body.html + extra.css + splice.py; run splice.py after any body/CSS edit, never edit index.html directly)
- Live URL once published: https://lukezhang.si/blog/alpha-nist/

## Run it

```
python3 ~/workspace/blog-drafts/alpha-nist/verify/verify.py            # local server on the draft folder
python3 ~/workspace/blog-drafts/alpha-nist/verify/verify.py https://lukezhang.si/blog/alpha-nist/
```

The harness drives the real UI at 390x844: it plays and seeks both videos through their chips, toggles the close-up inset, steps both carousels by arrows, swipe, tap, and keys, and asserts computed styles, KaTeX clipping, bar widths, and dot counts. Screenshots land in `verify/shots/`.

## Project quirks

- Both films are hotlinked from alpha-nist.github.io (GitHub Pages) and must never be rehosted. The harness asserts the exact source URLs on the shipped page.
- Environment note (found 2026-10-14): this VM's Playwright Chromium cannot load ANY HTTPS URL (every one fails with ERR_TUNNEL_CONNECTION_FAILED through the sandbox egress, verified against example.com and arxiv.org too), so remote readyState cannot be proven from here. The harness therefore runs in two phases: phase 1 is the shipped page with remote checks recorded as BLOCKED (with curl/ffprobe evidence the sources return 200 with the right codec and duration), and phase 2 runs the full player mechanics against /tmp/an-vids/index-mirror.html, a copy whose only change is pointing the two video sources at byte-identical local downloads served with Range support. On an open network, phase 1's remote checks run strictly and nothing is blocked.
- The close-up inset is the same video element source zoomed with a CSS transform (scale 2.5), muted, and kept in sync by the page script (seek mirroring plus drift correction at 0.3 seconds). The harness checks main and inset currentTime agree within 0.6 seconds after a chip seek.
- Video buffering over the network is the slow part of the run; the playable-state waits allow 60 seconds each.
- KaTeX is vendored in the draft's katex/ folder; the harness asserts the stylesheet is loaded and .katex-mathml computes to position absolute (the double-render guard).
