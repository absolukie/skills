---
name: "verify-training-checkpoints"
description: "Re-run verification for the primer 'Pausing and Resuming a Training Run' at lukezhang.si/blog/training-checkpoints/: feature map, Playwright harness, and last report live in the draft's verify folder."
---

# Verify: Pausing and Resuming a Training Run

Live URL: https://lukezhang.si/blog/training-checkpoints/
Draft (canonical source): `~/workspace/blog-drafts/training-checkpoints/index.html`
Illustration: `images/train.webp` in the draft folder (Codex ink illustration: bellows camera photographing a freight train loaded with metal plates, photographic plates stacked beside).

## Run it

```bash
cd ~/workspace/blog-drafts/training-checkpoints/verify
python3 verify.py            # local draft on a throwaway server
python3 verify.py <url>      # any served URL
```

The harness drives the real UI at 390x844: Fig 1 anatomy stepper (5 steps, running totals to 840 GB), Fig 2 Llama 3 census stepper (4 steps), Fig 3 size explorer (chips 7B/70B/405B recomputing 4 rows, checking 84 GB, 840 GB, 4.86 TB, 810 GB), 6 mechanism cards, the no-controlled-A/B callout, the 6-step timeline with arrows measured at the stage's vertical midway, voices/camps/takeaways counts (7/2 agree + 2 versus/6), section order, 7 sources, computed-style and content-inset assertions, zero pageerrors, zero horizontal overflow. It writes `REPORT.md` and screenshots to `shots/` on every run.

Feature map: `~/workspace/blog-drafts/training-checkpoints/verify/FEATURE_MAP.md`
Last report: `~/workspace/blog-drafts/training-checkpoints/verify/REPORT.md`

## Content invariants (do not let an edit break these)

- Byte anatomy: BF16 weights 2 B/param, FP32 4, canonical AdamW resumable checkpoint 12 (FP32 master 4 + m 4 + v 4), 14 with the BF16 working copy. 70B worked example: 140 / 280 / 840 / 980 GB. 405B full checkpoint 4.86 TB.
- Llama 3 census is counts, not the paper's printed percentages: 466 total interruptions (419 unexpected + 47 planned) in 54 days on 16,384 H100s, faulty GPU 148, HBM3 72, CPU 2, only 3 needing significant intervention, over 90 percent effective training time (arXiv:2407.21783).
- PaLM protocol: rewind about 100 steps, skip 200 to 500 batches; same-batch replay often did not reproduce the spike (arXiv:2204.02311).
- SOSP 2023 Gemini is Microsoft Research's system, not Google's Gemini model; the page states this explicitly.
- No controlled pause-vs-no-pause quality A/B exists in the primary literature; the page presents "pausing is free" as operational consensus, never as a measured result.

## Quirks

- Playwright against the live URL fails through this VM's proxy (ERR_TUNNEL_CONNECTION_FAILED). Live proof is curl: page, image, and /primers/ return 200, and served page bytes equal the draft plus exactly 248 bytes (Luke's analytics beacon).
- The Microsoft Research publication page refuses scripted curl (403 bot wall); content confirmed in a browser during research.
- Arrows use the template's car-arrow system: buttons live inside a .tl-stage wrapper and their top is set by JS to the stage's vertical midway on every render. Stepper totals must equal the data-row counts exactly (a +1 here once made the counter promise a step that shows nothing new).
- Repairs 2026-10-13 night (Luke's screenshots): (1) Figure 3's bars never rendered: renderSz sets each fill's --w inline, but the only width rule was .sb-row.on .fn-fill, and the standalone explorer's rows are not inside a stepper row, so every bar sat at width 0 while labels and values rendered fine. Fixed with a scoped #szRows .fn-fill{width:var(--w)} rule; the harness now asserts all four fills render, strictly proportional, with the largest filling its track (measured at 405B after a 700ms settle). (2) Rule-16 swipe and tap gestures added to all three steppers (#anatStage, #faultStage, #tlBody) via wireStepper goNext/goPrev, with dispatched-PointerEvent suites in the harness. Total 90/90. General lesson: a component copied out of a stepper into a standalone viz loses any activation rule scoped to the stepper's row classes; harness checks must assert rendered geometry for bars, not just labels.
