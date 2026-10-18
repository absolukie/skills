---
name: verify-be-more-ambitious
description: Verify the "How to Be More Ambitious With Models" primer (be-more-ambitious): re-run the Playwright harness (87 checks, 390x844, real UI) against the live page or the local draft, and know where the feature map, shots, and report live. Trigger on: "verify be-more-ambitious", "re-check the ambition primer", "did the ambitious primer break".
---

# Verify: How to Be More Ambitious With Models primer

The primer: Felix Rieseberg's "How to be more ambitious" tutorial (13 October
2026) and the research under it: four ambition types, the QBR ambition ladder,
Locke and Latham's goal-setting effect sizes, METR's time horizon, the jagged
frontier, Bandura's self-efficacy sources, 7 voices, 3 future camps.

- **Live:** https://lukezhang.si/blog/be-more-ambitious/ (local draft until the coordinator publishes)
- **Source:** `~/workspace/blog-drafts/be-more-ambitious/` (`body.html` + `extra.css` + `splice.py` regenerates `index.html` from the softmax shell; never edit index.html directly)
- **Facts:** `~/workspace/research_notes/be-more-ambitious-with-ai-20261014-0625/report.md` is the only fact source. Numbers never come from memory.
- **Feature map:** `verify/FEATURE_MAP.md` beside this skill's harness (in the draft folder)
- **Harness:** `~/workspace/blog-drafts/be-more-ambitious/verify/verify.py`
- **Report and shots:** `verify/REPORT.md`, `verify/shots/` (12 screenshots)

## Re-run

```bash
cd ~/workspace/blog-drafts/be-more-ambitious
python3 verify/verify.py                      # local draft on port 8937
python3 verify/verify.py https://lukezhang.si/blog/be-more-ambitious/   # live
```

Last full run: **87/87** (14 October 2026, local draft). The harness serves the
draft folder itself on port 8937; pass a URL to test the deployed page instead.
Note the port: parallel harnesses collide on shared ports, keep 8937 for this one.

## What it checks (87)

- Hero: title, tags exactly [ai, culture], hero image loads, "Researched October 2026", no horizontal overflow.
- Four type cards: count, toggle flips computed display and aria-expanded, chevron pinned at 20px, title at least 170px wide.
- Ladder stepper: step order and titles, count "1 / 4" to "4 / 4", prev hidden at start, next hidden at end, arrows 46px, straddling the stage edge, centered at the anchor card's midway, stable top across steps; tap advances one step; synthetic swipe advances exactly one; a click within 400ms after a consumed swipe does not double-step; a real mouse drag advances exactly one; arrow keys move steps both ways.
- Goal lab: KaTeX rendered in the display formula, no raw "$$" visible, symbol legend is the formula's immediate next sibling, worked numbers present (0.6, 56, 0.42), default readouts d = 0.60 / 73rd percentile / 73% / Inside, marker at 50% of the scale; slider low gives Below, slider high gives Above.
- METR lab: KaTeX rendered, worked numbers, defaults 12 months / about 37 hours / 6.9x / 2,214 min; GPT-5 chip gives 1,481 min; 196-day chip with GPT-5 gives 778 min; Opus with 196 gives 1,163 min; exactly one chip pressed per group; Home key gives 0 months with the measured-point insight; End key gives 24 months and a days readout.
- Jagged frontier: 6 bars inside with values [100, +12.2%, 100, over +40%, 100, 74.9] and widths matching the stated scale; 3 bars outside [84%, 70%, 60%]; insight lines flip; exactly one chip pressed; rapid toggling settles.
- Story cards: 3 cards, first toggles, the callout names verbal persuasion.
- Timeline: 13 stops; first is Dantzig; the 10 July 2025 stop pairs 19 percent with the February 2026 update; last names Rieseberg; count "13 / 13"; next hidden at the end.
- Voices and camps: 7 voice cards, voice title 18px computed, Tao note says the original could not be verified, 3 camps, agree camp names METR and Amodei, split camp has exactly 2 sides, bet camp is marked as Rieseberg's alone, camp names bold (700).
- Takeaways: exactly 5 bullets; conclusion paragraph word count between 60 and 80 (harness counts live).
- Explore and sources: 4 explore cards each with a link-out SVG, explore title 17px computed, 21 source cards, source links bold (600), ridge image loads and sits above the frontier section.
- Health: zero page errors, scrollWidth at most 390 at the end.

## Link health

The REPORT.md carries the last curl sweep: 24 of 25 external URLs return 200.
The YouTube keynote link is bot-blocked for scripted fetches (429 plus the
google.com/sorry redirect); it is the exact URL from the research report, kept
deliberately. Do not swap it on a scripted-fetch failure alone.
