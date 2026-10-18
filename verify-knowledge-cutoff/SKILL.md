---
name: "verify-knowledge-cutoff"
description: "Re-run verification for the primer 'Why Models Go Stale' at lukezhang.si/blog/knowledge-cutoff/: feature map, Playwright harness, and last report live in the draft's verify folder."
---

# Verify: Why Models Go Stale

Live URL: https://lukezhang.si/blog/knowledge-cutoff/
Draft (canonical source): `~/workspace/blog-drafts/knowledge-cutoff/index.html`
Illustration: `images/clocks.webp` in the draft folder (Codex ink illustration: frozen book-iceberg, library shelves refilled from a conveyor of loose pages, rust-red telegraph key with fresh slips on a wire).

## Run it

```bash
cd ~/workspace/blog-drafts/knowledge-cutoff/verify
python3 verify.py            # local draft on a throwaway server
python3 verify.py <url>      # any served URL
```

The harness drives the real UI at 390x844: Fig 1 freshness-stack stepper (5 steps), Fig 2 price-of-an-update stepper (5 steps), Fig 3 cutoff explorer (5 chips: default Claude 4 two-date panel, GPT-4.1 June 1 2024, Llama 4 August 2024), 6 mechanism cards, the editing callout, the 7-step timeline with arrows measured at the stage's vertical midway, voices/camps/takeaways counts (8/2 agree + 2 versus/6), section order, 10 sources, computed-style and content-inset assertions, zero pageerrors, zero horizontal overflow. It writes `REPORT.md` and screenshots to `shots/` on every run.

Feature map: `~/workspace/blog-drafts/knowledge-cutoff/verify/FEATURE_MAP.md`
Last report: `~/workspace/blog-drafts/knowledge-cutoff/verify/REPORT.md`

## Content invariants (do not let an edit break these)

- Dates are the labs' published figures for those versions: GPT-4.1 cutoff June 1, 2024; GPT-4o mini October 1, 2023; Gemini 2.5 Pro January 2025; Llama 4 August 2024. Claude 4 always shows BOTH dates (training cutoff March 2025 per Anthropic's table; reliable cutoff end of January 2025 per the system prompt), with the discrepancy sourced as secondary reporting of Anthropic's own documents.
- DeepSeek-V3 ledger: total $5.576M / 2.788M H800 hours at $2 per hour; pretrain $5.328M (2.664M hrs, 14.8T tokens); context extension $0.238M (119K hrs); post-training about $0.010M (about 5K hrs).
- FreshQA: 600 questions, over 50,000 human judgments, all tested models weak on fast-changing and false-premise questions, search augmentation substantially helped (Vu et al., arXiv:2310.03214).
- Continual pretraining recipe: LR re-warm + re-decay + about 5 percent replay removes most forgetting in the reported shifts (Ibrahim et al., TMLR 2024). RETRO: 2T-token database, comparable performance with 25x fewer parameters. LoRA: 10,000x fewer trainable parameters than GPT-3 full fine-tuning.
- Frontier cutoffs for the newest generations (GPT-5 family beyond 4.1, Claude 4.5, Gemini 3) are deliberately NOT stated: official pages could not be sourced, and the page footer says so.

## Quirks

- Playwright against the live URL fails through this VM's proxy (ERR_TUNNEL_CONNECTION_FAILED). Live proof is curl: page, image, and /primers/ return 200, and served page bytes equal the draft plus exactly 248 bytes (Luke's analytics beacon).
- Arrows use the template's car-arrow system: buttons live inside a .tl-stage wrapper and their top is set by JS to the stage's vertical midway on every render. Stepper totals must equal the data-row counts exactly.
- The Fig 3 explorer reuses the .dv-panel/.dv-h/.dv-p classes; their CSS is not in the shared shell head and is added per page. If the panel ever renders unstyled, check for that block first.
