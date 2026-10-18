---
name: "verify-kimi-architecture"
description: "Re-run verification for the primer 'How Kimi Is Built' at lukezhang.si/blog/kimi-architecture/: feature map, Playwright harness, and last report live in the draft's verify folder."
---

# Verify: How Kimi Is Built

Live URL: https://lukezhang.si/blog/kimi-architecture/
Draft (canonical source): `~/workspace/blog-drafts/kimi-architecture/index.html`
Illustration: `images/tower.webp` in the draft folder (Codex ink illustration: tower of expert doors, a few open and rust red, ribbons braiding into a scroll).

## Run it

```bash
cd ~/workspace/blog-drafts/kimi-architecture/verify
python3 verify.py            # local draft on a throwaway server
python3 verify.py <url>      # any served URL
```

The harness drives the real UI at 390x844: Fig 1 KV-arithmetic stepper (5 steps, bars, verdict chips), Fig 2 K2-to-K3 stepper (6 steps), Fig 3 cache explorer (4 context chips recompute totals: 128K gives 262 GB baseline / 3.6 GB hybrid; 1M gives 2.1 TB / 29.0 GB), 6 mechanism cards, the optimizer-fight callout, the 10-step timeline with arrows measured at the stage's vertical midway, voices/camps/takeaways counts (8/2 agree + 2 versus/6), section order, 9 sources, computed-style and content-inset assertions, zero pageerrors, zero horizontal overflow. It writes `REPORT.md` and screenshots to `shots/` on every run.

Feature map: `~/workspace/blog-drafts/kimi-architecture/verify/FEATURE_MAP.md`
Last report: `~/workspace/blog-drafts/kimi-architecture/verify/REPORT.md`

## Content invariants (do not let an edit break these)

- Fig 1 arithmetic is worked at K2's published shape (64 heads, dim 128, 61 layers, bf16): MHA 32 KiB/token/layer and about 2 MB/token total; GQA-8 244 KiB/token; MLA (512 latent + 64 RoPE) about 69 KiB/token, matching DeepSeek's reported ~70 KB/token for V3. Explorer totals are decimal GB/TB computed from those per-token figures (128K MHA = 262 GB; 1M hybrid = 29.0 GB).
- Muon is presented as claimed, not settled: Moonshot/Moonlight at-scale claims on one side, controlled spectral studies finding no significant edge on the other; no neutral at-scale A/B exists.
- Artificial Analysis scores are never compared across index versions on the page (57 at launch under one version, far lower under v4.3.2); DeepSWE's 67 to 69 percent is the independent coding placement.
- K3 specs (2.8T/104B, 93 layers = 69 KDA + 24 Gated MLA, 896 experts, 1,048,576 context) trace to the kimi.com launch post and the Hugging Face model card.

## Quirks

- The K2-to-K3 stepper (kc) also accepts horizontal swipes on its stage (added at Luke's request, 2026-10-12): a flick of 48px or more, at least 1.5x wider than tall, steps it exactly like the arrows; vertical drags keep scrolling the page (stage touch-action is pan-y). No visual swipe affordance, by his instruction. The other steppers are tap-only unless he asks to widen it.
- Playwright against the live URL fails through this VM's proxy (ERR_TUNNEL_CONNECTION_FAILED). Live proof is curl: page, image, and /primers/ return 200, and served page bytes equal the draft plus exactly 248 bytes (Luke's analytics beacon).
- The kimi.com blog refuses scripted curl (403 bot wall) but was confirmed reading correctly in a browser during research; the Hugging Face card carries the same specs and returns 200.
- Arrows use the template's car-arrow system: buttons live inside a .tl-stage wrapper and their top is set by JS to the stage's vertical midway on every render. If arrows ever anchor to the body, check the wrapper structure first.
