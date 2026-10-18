---
name: verify-transformer-vs-neural-network
description: "Verify the 'Transformer vs. Neural Network' primer (lukezhang.si/blog/transformer-vs-neural-network/): feature map, Playwright harness, and report. Run after any edit to the page."
---

# Verify: Transformer vs. Neural Network primer

Live URL: https://lukezhang.si/blog/transformer-vs-neural-network/
Draft source: ~/workspace/blog-drafts/transformer-vs-neural-network/index.html (canonical; deploy by
surgical overlay to blog/transformer-vs-neural-network/ in absolukie/lukezhang-si, plus the images
at blog/transformer-vs-neural-network/images/family.webp and blog/transformer-vs-neural-network/images/attention.webp,
plus the vendored katex/ folder, plus a card in primers/index.html)

Feature map: ~/workspace/blog-drafts/transformer-vs-neural-network/verify/FEATURE_MAP.md
Harness: ~/workspace/blog-drafts/transformer-vs-neural-network/verify/harness.py
Last report: ~/workspace/blog-drafts/transformer-vs-neural-network/verify/REPORT.md

Run locally: `python3 ~/workspace/blog-drafts/transformer-vs-neural-network/verify/harness.py`

The harness drives the real UI at 390x844: hero and illustration checks, content
inset on the h1, 6 mechanism cards (tap toggle with aria-expanded), the same-terms comparison
board (8 fixed terms, 14 sentence positions, 3 wiring cards with identical row
labels), KaTeX
rendering (at least 4 display formulas, no raw $$ left), the 5-step attention
carousel (worked numbers 0.401 / 5.056 / [0.802, 0.599], rule-5 arrows, arrow
keys), the Fig. 2 wiring calculator (defaults 8.4M / 33.6M / 100.7M at n = 128;
8.59B at n = 4096), the Fig. 3 parameter counter (defaults 1.05M / 2.10M /
18.87M; 16,384 at width 64), the 14-step timeline, 6 voice cards, 5 camps,
6 takeaways, 4 keep-exploring cards, 26 source cards, zero pageerrors.

Quirks: illustrations come from the Codex CLI image generator (never the Muse
media pipeline). DOI resolver, OpenReview, YouTube, and VentureBeat refuse or
rate-limit scripted link checks (403/429) while opening fine in a browser; the
research pass read them directly, so do not treat those codes as dead links.
