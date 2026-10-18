---
name: "verify-softmax-alternatives"
description: "Re-verify the Softmax primer (lukezhang.si/blog/softmax-alternatives/): feature map, style-aware real-UI harness (80 checks), link check. Trigger on: 'verify softmax-alternatives', 're-check the softmax primer'."
---

# Verify: Softmax, and Everything Trying to Replace It primer

- Draft: `~/workspace/blog-drafts/softmax-alternatives/index.html`; images in `images/` (hero.webp, tiles.webp, Codex-generated); KaTeX vendored in `katex/`.
- Research: `~/workspace/research_notes/softmax-alternatives-20261013/report.md` (only source of facts for this page).
- Feature map: `~/workspace/blog-drafts/softmax-alternatives/verify/FEATURE_MAP.md`.
- Harness: `verify/qa.mjs` (playwright-core; a node_modules/playwright-core symlink lives in verify/). Run: `cd ~/workspace/blog-drafts/softmax-alternatives/verify && node qa.mjs`. Asserts computed styles and layout (wrap, h1 inset, fcard display flips, styled card backgrounds) plus exact math: temperature lab at T = 1 / 0.5 / 2 (0.665/0.245/0.090 at T = 1), alternatives lab values and sums for all five methods (sparsemax [1, 0, 0], 1.5-entmax [0.831, 0.169, 0], sigmoid sum 2.564), online stepper counts and final weights, sink toggle bar counts and sums, KaTeX node count and zero raw $$, and a programmatic assertion that every one of the 21 .fx blocks is immediately followed by a .fx-key symbol legend. Terminal stepper arrows display none, arrows 46px on a shared anchor line, zero pageerrors, scrollWidth <= 390. Screenshots: `verify/shots/01..15`.
- Chromium: Playwright headless shell build 1243 at `~/.cache/ms-playwright/chromium_headless_shell-1243/...`.
- Last local result: 80/80 (2026-10-12). Link check: `verify/link-check.md`, 33/33 alive.
- Published 2026-10-12: commits `1eb243ef` (page) and `d1a8364e` (primers index); live byte-verified (served = local + 248 beacon) at https://lukezhang.si/blog/softmax-alternatives/ .
- Template family: specialist/moats shell copied from the KV cache primer. Never rebuild in a different class system (see AGENTS.md 2026-10-12 rule).
