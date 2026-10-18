---
name: verify-muse-vs-codex
description: Verify the primer 'Muse vs. Codex, Checked' (lukezhang.si/blog/muse-vs-codex/) against its feature map by running the Playwright harness, which drives the real UI (A/B toggle, six mechanism cards with chips, scorecard bars, cost sliders, timeline stepper with gestures and keys, voices, camps) and asserts computed styles, geometry, dark-scheme contrast, and all source links.
---

# Verify Muse vs. Codex, Checked

Feature map: `~/workspace/blog-drafts/muse-vs-codex/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/muse-vs-codex/verify/verify.py` (local port 8953)

Run it:

```
python3 ~/workspace/blog-drafts/muse-vs-codex/verify/verify.py
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

Verified numbers the harness guards (all traced to primary sources; see the primer's Sources section and `~/workspace/research_notes/muse-vs-codex-20261016/notes.md`):
- Artificial Analysis index: Opus 5.5 = 58, Wonder Full = 56, Astra = 53.
- Meta's model card (max effort): DeepSWE 79.0 / 74.2 / 74.1; SWE-Marathon 57.5 / 46.3 / 42.5; Terminal-Bench 59.6 / 59.1 / 57.1 (Opus, Astra, Wonder Full per row as laid out on the page).
- API rates per 1M tokens: Wonder $4 in / $20 out; Opus 5.5 $4 / $20; Sol $2 / $10; Astra $10 / $50. Harness defaults (4M in, 1M out) give $36 / $36 / $18 / $90.

Invariants the harness guards:
- A/B toggle: role=switch, aria-checked mirrors state, Muse and Codex layers crossfade (opacity waits after the 450ms transition), thumb centers on the shown side, works both ways.
- Six mechanism cards, each body containing a visual; memory chips and scoreboard chips rewrite their readouts.
- Scorecard: 12 rows, 4 leaders, fill-width ratios within 0.035 of the printed values.
- Cost sliders: exact recomputed totals at two changed settings.
- Timeline: 46px arrows at stable boxes, terminal arrows hidden, tap and swipe steps, 6 events.
- Voices: 7 cards with links; cost disagreement visible. Camps: 2 agree, 4 split with Side A/Side B and a marked long shot.
- Screenshots of the hero and every section land in `verify/shots/` for a full-size review before publish.
- Dark-scheme pass: card and voice surfaces stay dark while title and keyline ink stays light.
- Link check: x.com URLs return 403/429 to bots; they pass only because the post and article were read firsthand via the fxtwitter API during research.
