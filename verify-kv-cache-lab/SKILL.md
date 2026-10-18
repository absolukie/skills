---
name: "verify-kv-cache-lab"
description: "Verification for the Build a KV Cache lab (projects.lukezhang.si/kv-cache-lab): a from scratch MLA KV cache in one HTML file, with live absorption-equivalence checks. Use to re-verify the lab after any edit."
---

# Verify: kv-cache-lab

- Live: https://projects.lukezhang.si/kv-cache-lab/
- Source: `~/workspace/kv-cache-lab/index.html` (single file, deployed as `sites/kv-cache-lab/index.html` in absolukie/lukezhang-si)
- Feature map: `~/workspace/kv-cache-lab/verify/FEATURE_MAP.md`
- Harness: `~/workspace/kv-cache-lab/verify/qa.mjs` (playwright-core via the node_modules symlink to e2e-liverpool; headless chromium shell 1243). Run: `cd ~/workspace/kv-cache-lab/verify && node qa.mjs`. Live pass: `QA_URL=https://projects.lukezhang.si/kv-cache-lab/ node qa.mjs`.
- Last local result: 43/43 (2026-10-12), including absorption max diff 2.78e-17 read from the page's own readout after real Generate taps, exact +80 numbers per decode step, cell detail with exactly 32 latent + 8 RoPE numbers, and a legend directly under all 4 formula blocks.
- Key invariants to never weaken: cache growth per decode step is exactly 80 numbers (40 per layer x 2 layers); displayed absorption diff must stay under 1e-9; every .fx formula block must keep a .legend as its next sibling (Luke's rule: every symbol defined at the formula itself).
- Quirks: weights are seeded, so the cache is deterministic across runs; generated tokens are gibberish by design and labeled as such. Screenshots land in `verify/shots/`; review them, do not just count passes.
