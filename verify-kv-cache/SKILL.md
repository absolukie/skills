---
name: "verify-kv-cache"
description: "Re-verify the KV Cache primer (lukezhang.si/blog/kv-cache/): feature map, style-aware real-UI harness (49 checks), link check. Trigger on: 'verify kv-cache', 're-check the KV cache primer'."
---

# Verify: KV Cache primer

- Draft: `~/workspace/blog-drafts/kv-cache/index.html`; images in `images/` (hero.webp, paging.webp, Codex-generated).
- Feature map: `~/workspace/blog-drafts/kv-cache/verify/FEATURE_MAP.md`.
- Harness: `verify/qa.mjs` (playwright-core; a node_modules/playwright-core symlink to the e2e-liverpool install lives in verify/). Run: `cd ~/workspace/blog-drafts/kv-cache/verify && node qa.mjs`. Asserts computed styles and layout (wrap, h1 inset, fcard display flips, stat stacking, styled card backgrounds) plus calculator math (Llama 3 8B at 128K = 16.0 GiB), stepper counts, terminal arrows hidden, 46px arrows, zero pageerrors, scrollWidth <= 390. Screenshots: `verify/shots/01..10`.
- Chromium: Playwright headless shell build 1243 at `~/.cache/ms-playwright/chromium_headless_shell-1243/...`.
- Last local result: 67/67 (2026-10-12, after notebook values + Kimi K2 deep panel additions). Link check: `verify/link-check.md`.
- Template family: specialist/moats shell. Never rebuild in a different class system (see AGENTS.md 2026-10-12 rule).
