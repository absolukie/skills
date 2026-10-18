---
name: verify-new-model-skill-check
description: Re-verify the "New Model, Old Skills" primer at lukezhang.si/blog/new-model-skill-check/ (delta testing agent skills on model upgrades). Use when Luke reports a problem with that page or asks to re-check it.
---

# Verify: New Model, Old Skills primer

Canonical source: `~/workspace/blog-drafts/new-model-skill-check/index.html`.
Live URL: https://lukezhang.si/blog/new-model-skill-check/

Feature map: `~/workspace/blog-drafts/new-model-skill-check/verify/FEATURE_MAP.md` (read it first;
it is the contract). Harness: `verify/qa.mjs` loads the LOCAL draft over file:// in headless
Chromium at 390x844 with real clicks (puppeteer-core from moonblinked-studio's node_modules +
the Playwright chromium headless shell, build 1243). Run: `node verify/qa.mjs` from the verify
dir. Expect 30/30. Screenshots land in `verify/shots/` (shots2.mjs adds per-section shots).
The harness asserts COMPUTED STYLES and margins, not just DOM counts and clicks: v1 of this page
shipped with a mismatched template shell (no .wrap, unstyled sections) and passed a DOM-only
harness. The page body must stay in the moats/specialist template markup (wrap, hero, fcard with
fbody, voice, camp, src, xlink, takeaways) that its CSS was written for.

Content invariants: Fig 1 is illustrative (labeled in its figcaption) with old-model deltas
plus 5 (no-skill 5 of 12, with-skill 10 of 12) and new-model delta plus 1 (9 to 10). Measured
numbers on the page are SkillsBench's: +16.6 pts v4 (33.9 to 50.5, 87 tasks), 16 of 84 negative
(v3), focused +18.6 vs comprehensive +5.9, self-generated minus 1.3, Haiku 4.5 with skills 27.7%
vs Opus 4.5 alone 22.0% (v3). Anthropic's pass^k example: 75% per try becomes about 42% at
pass^3. Never mix SkillsBench v3 and v4 figures.

The page carries the tall-stage arrow tracker (visualizers rule 5, tall case): both stages
measure short, so anchors hold; the harness asserts the Fig 1 arrow stays at its anchor top
after scrolling. If a stage ever exceeds ~0.9x viewport height, arrows must ride viewport middle.

If the live page and the draft ever disagree, the draft is canonical: re-push
blog/new-model-skill-check/index.html surgically and re-verify served bytes.
