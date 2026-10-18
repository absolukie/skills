---
name: verify-exa-search-for-agents
description: Re-run verification for the primer 'The Search Engine Your Agent Calls' (Exa) at lukezhang.si/blog/exa-search-for-agents/: feature map, Playwright harness, and last report live in the draft's verify folder.
---

# Verify: The Search Engine Your Agent Calls (Exa primer)

## Where things live
- Draft: `~/workspace/blog-drafts/exa-search-for-agents/index.html`
- Feature map: `~/workspace/blog-drafts/exa-search-for-agents/verify/FEATURE_MAP.md`
- Harness: `~/workspace/blog-drafts/exa-search-for-agents/verify/verify.py` (serves the draft on port 8957, drives the real UI at 390x844)
- Results: `verify/results.json`, screenshots in `verify/shots/`, summary in `verify/REPORT.md`
- Live: https://lukezhang.si/blog/exa-search-for-agents/

## Run it
```bash
cd ~/workspace/blog-drafts/exa-search-for-agents && python3 verify/verify.py
```
Expect 42/42. Any failure names the feature that drifted; fix the page (or the check, if the page changed on purpose) and re-run until green.

## What it proves
- Page loads with zero page errors, no horizontal overflow, hero image's own box inside the column, two tags (ai, tools), "Researched October 2026", exactly one key line in each of the eight content sections, no paragraph walls, zero em/en dashes in rendered text.
- Both KaTeX display formulas render centered within 6px, and prose prices are never mathified (the page drops the single-$ delimiter; inline math uses \( \) only). The prose_prices_not_mathified check guards this: keyline, takeaway bullet, card 2 example, timeline panel, source item, and Figure 2 note all keep plain $ amounts with no .katex and no literal backslashes.
- Figure 1 stepper: arrows 46px and stage-relative stable, terminal arrows display:none, drawing and note change per step, swipe and tap both advance.
- All six mechanism cards open on tap and each carries a visual or interaction; card 1's chip toggle flips the winner (0.982 to 0.998), card 2's Deep gear reads $12, card 3's Summary layer, card 4's Companies record, card 5's mini stepper hides Next at step 3.
- Figure 2 reprices exactly ($140 at 20k Fast; $700 at 100k Fast; $400 at 100k Instant) with a computed insight line. Figure 3 has the five locked rows ($7/$8/$5/$5/$14 per 1k).
- Timeline steps 1 of 6 to 6 of 6 ending at May 2026; six voices with links; camps 2 agree + 4 split with Side A, Side B, and the marked long shot; takeaways conclusion 60 to 85 words with 5 bullets; 11 linked sources.
- A dark-scheme pass asserts card text/background contrast and saves a dark screenshot.

## After any page edit
Re-run the harness, view the fresh screenshots (hero, fig1-step4, cards-open, fig2-lab, dark-cards at minimum), then re-publish surgically and confirm served bytes equal draft bytes + 248.
