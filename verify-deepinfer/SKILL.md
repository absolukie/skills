---
name: verify-deepinfer
description: Re-run verification for the primer "DeepSeek Opened the Engine Room" at lukezhang.si/blog/deepinfer/: feature map, Playwright harness, and last report live in the draft's verify folder.
---

# Verify: DeepSeek Opened the Engine Room

Primer on DeepSeek's October 20, 2026 launch of DeepInfer, its in-house inference framework for DeepSeek-V4.1-Flash, published eighteen months after the April 2025 note explaining why the engine would stay closed. The engine, kernels, DSpark, Wide-EP, async scheduler, bounded replay, and batch invariance are in the box; the KV cache system, VE/P/D disaggregation, and replica load balancers stayed internal.

- Live: https://lukezhang.si/blog/deepinfer/
- Draft: ~/workspace/blog-drafts/deepinfer/index.html
- Feature map: ~/workspace/blog-drafts/deepinfer/verify/FEATURE_MAP.md
- Harness: ~/workspace/blog-drafts/deepinfer/verify/verify.py (port 8961, 390x844)
- Last report: ~/workspace/blog-drafts/deepinfer/verify/results.json
- Screenshots: ~/workspace/blog-drafts/deepinfer/verify/shots/
- Research: ~/workspace/research_notes/deepinfer-20261020/ (repo README, deployment Q&A, eval README, April 2025 note, post1.json, the three Pareto chart PNGs, findings.md)

## Run it

```
python3 ~/workspace/blog-drafts/deepinfer/verify/verify.py
python3 ~/workspace/tools/css_audit.py ~/workspace/blog-drafts/deepinfer/index.html
```

The harness drives the real UI: the Figure 1 Pareto explorer (six measured operating points from DeepSeek's published decode chart; chips and chart dots stay in sync; readouts pinned to the chart values, steps per second = per-user speed / 3.25), the DSpark click-per-step verification strip (draft, confidence, verify prefix, kept), the Wide-EP bars at their 84/100 ratio, the scheduler serial/asynchronous toggle, the batch-invariance chips over an unmoving output line, the 6-panel timeline carousel (46px arrows at the anchor midway, tap advances exactly once, terminal arrows hidden), and the mechanism-card toggles. It also asserts computed styles and geometry (hero box inside the column, hero under 200 KB), KaTeX health (stylesheet loaded, .katex-mathml clipped, exactly 7 formulas, visible display formulas centered, no prose price mathified), a dark-scheme contrast pass with alpha-composited backgrounds, zero em/en dashes, exactly 7 keylines, 2 tags, 3 voices, 5 takeaways, a 60-to-80-word takeaways conclusion, and live status of every source link (the X post through the fxtwitter API because x.com blocks bots).

## Invariants to keep

- Every benchmark and production figure stays labeled as DeepSeek's own: chart values read off the repo's published Pareto PNGs (approximate), production figures (155T tokens/day, $38/GPU-hour, 80% balancing, at most 5% kernel gap) from its deployment Q&A. No independent rerun of examples/sweep/run_sweep.sh had been published at research time; do not present any number as independently reproduced.
- The thread's middle posts (2/4, 3/4) were not retrievable verbatim; the page quotes post 1/4 verbatim and the 4/4 closing line only as reported by launch-day coverage, and the foot says so. Do not add verbatim quotes from posts 2 or 3 without a retrieved source.
- Exactly 7 keylines, exactly 2 tags (AI, Infrastructure), 6 mechanism cards each with a visual or interaction, 3 voices (the cap), 5 takeaway bullets.
- Hero is the Codex illustration (open machine, token conveyor, locked door at the end), webp under images/, under 200 KB.
- If the page changes, update FEATURE_MAP.md and this skill in the same pass (maintain-verification-skill).
