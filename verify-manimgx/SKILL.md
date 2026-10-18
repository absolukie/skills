---
name: "verify-manimgx"
description: "Re-verify the ManimGX primer (lukezhang.si/blog/manimgx/): feature map, style-aware real-UI harness (60 checks), link check, live byte check. Trigger on: 'verify manimgx', 're-check the ManimGX primer'."
---

# Verify: ManimGX: Manim's API at GPU Speed, Checked primer

- Draft: `~/workspace/blog-drafts/manimgx/index.html`; images in `images/` (hero.webp, compat.webp, both Codex-generated; studio-trial.mp4, the first-party trial render); KaTeX vendored in `katex/` (auto-render lives at `katex/contrib/auto-render.min.js`).
- Research: `~/workspace/research_notes/manimgx-primer-20261013/report.md` and `notes/key-facts.md` (only source of facts for this page; anything flagged unverified there stays out or stays labeled).
- Feature map: `~/workspace/blog-drafts/manimgx/verify/FEATURE_MAP.md`. QA results: `verify/qa-results.md`. Link check: `verify/link-check.md`.
- Harness: `verify/qa.mjs` (playwright-core; node_modules is a symlink to the kv-cache verify node_modules). Run: `cd ~/workspace/blog-drafts/manimgx/verify && node qa.mjs`. Real taps only. Asserts: wrap and h1 inset at 390px, scrollWidth <= 390, hero tags, every one of the 8 .fx blocks immediately followed by a .fx-key symbol legend with KaTeX rendered, fcard expand/collapse display flips, Fig 1 bench toggle row counts (5 headline / 10 per-scene) with 178.9x and 6.3x present, Fig 2 calculator exact values (defaults 5.1 s / 24.6 s / 96.3 min; 720p30 1.1 s / 5.5 s / 21.4 min; L=5 and L=120 endpoints), Fig 3 compat stepper verdicts per step (step 4 Does not convert, step 5 Silently ignored with colour=RED), Fig 4 engine stepper order, timeline stepper endpoints, trial video attrs, section counts (7 claims, 4 voices, 3 camps, 19 sources), zero pageerrors, and a guard that neither of Luke's private channel/studio names appears in the rendered text.
- Formula width probe: `verify/shots4.mjs` asserts every .fx scrollWidth equals clientWidth at 390px (two formulas were split during the build after this probe caught overflow).
- Screenshots: `verify/shots/` (10 section shots + targeted figure shots), reviewed at full size before publish.
- Chromium: Playwright headless shell build 1243 at `~/.cache/ms-playwright/chromium_headless_shell-1243/...`.
- Last local result: 60/60 (2026-10-12). Link check: 21/21 alive, see verify/link-check.md.
- Key numbers frozen from the research (do not change without re-reading the report): benchmark totals GX 3.078 / GL 35.284 / CE 278.826 / WB 57.611 / EEVEE 601.395 s over 36.2 s of video on an M4 Pro; ratios 90.59 / 11.46 / 18.72 / 195.38 recomputed; per-scene vs CE 178.9 / 19.8 / 6.3 / 48.4 / 88.0; calculator rates vendor 3.078/36.2, independent 4.1/10 (base M4 orbit), ours 731.7/7.6 (CPU llvmpipe, 2-core VM, 1080p60, 285 MB venv).
- Privacy rule for this page: never print Luke's YouTube channel name or the studio name anywhere on it; the trial is "our test bench" / "this machine".
- Template family: softmax-alternatives shell (head + CSS + body markup system from the same sibling). Note this template's fcards start closed and toggle via `.fcard > button` with `.fbody`; the `$` helper is NOT in the template, define it locally if used.
- Published 2026-10-12: commits `3d9ed061` (page + images + katex) and `caf2902c` (primers index entry, newest first under October 2026). Live-verified: https://lukezhang.si/blog/manimgx/ returns HTTP 200 with served bytes 93,142 = local 92,894 + 248 beacon; /primers/ contains the entry; all checked assets (both WebPs, the trial MP4, KaTeX css/js/auto-render, fonts) return 200.
