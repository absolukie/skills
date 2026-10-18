---
name: verify-why-one-agent-isnt-enough
description: Verify the primer "Why One Agent Isn't Enough" at lukezhang.si/blog/why-one-agent-isnt-enough/ (Flows / dynamic workflows in Claude Managed Agents, from the October 16, 2026 AI Engineer workshop by CJ Avilla and Harrison Stall) against its feature map by running the Playwright harness, which drives the real UI (org-chart stepper, outage dot grid, mechanism cards with off-switch chips, judge toggle and budget meter, coordination slider with measured score chart, planted-bug zoom bars, timeline stepper) and pins every numeric readout.
---

# Verify Why One Agent Isn't Enough

Feature map: `~/workspace/blog-drafts/why-one-agent-isnt-enough/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/why-one-agent-isnt-enough/verify/verify.py` (local port 8958)

Run it:

```
python3 ~/workspace/blog-drafts/why-one-agent-isnt-enough/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

Numbers the harness pins (research ledger: `~/workspace/research_notes/many-agents-20261017/findings.md`):
- Dot grid: single agent 35 checked / 15 missed; same-context recheck 35 / 15; flow 50 / 0. The 35 is the talk's story number; 50 of 50 is labeled on the page as the design's promise.
- Coordination slider: channels C(n) = n(n-1)/2 at n = 1, 10, 36, 100, 1000 = 0, 45, 630, 4,950, 499,500; layered links n-1. Measured scores exist only at 1 / 10 / 30 / 100 = 0.53 / 0.70 / 0.71 / 0.74 (Anthropic Opus 5.5 system card via The Decoder); every other size must read "not a tested size". Score bar rect heights are pinned proportional (38 / 50 / 51 / 53 px) because flex shrink once squashed them silently.
- Bug bars: single agent 14 / 15 / 27 of 70 (recall 20.0 / 21.4 / 38.6 percent), workflow 66 of 70 every run (94.3 percent); bar widths pinned to found/70.
- Budget meter state machine: phases $1.35 + $1.55 + $1.45 + $0.65 pause at exactly $5.00 (budget reached, work kept, raise offered); raise to $10 resumes; final phase $1.20 completes at $6.20. Amounts are labeled illustrative on the page; the pause/keep/resume behavior is the docs'.

Invariants the harness guards:
- Steppers (topology and timeline): 46px arrows at the anchor panel's midway, identical arrow boxes across steps, terminal arrows display:none, drawing or text changes every step, swipe and card tap step (tap test waits out the 400ms post-swipe guard), arrow keys step but are guarded while the range slider has focus.
- Mechanism cards are multi-open and every card body contains a visual or interactive element; off-switch chips answer ON / keeps stored / OFF for null / omitted / disabled; judge toggle flips the verdict text.
- KaTeX: stylesheet loaded, exactly 2 .katex (1 display in the eqbox, 1 inline in its legend; no other formulas on the page), .katex-mathml position absolute, display formula centered in its box, and prose dollar amounts are never mathified (single-$ delimiters are forbidden on this page; the Exa primer defect).
- Structure counts: 6 keylines, 6 cards, 8 voices, 13 sources, 2 tags, 5 takeaway bullets, conclusion 60 to 80 words.
- Dark-scheme contrast pass on card surfaces plus hero_img_fits (the hero's own box inside the column).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` is clean with no allowlist file.
