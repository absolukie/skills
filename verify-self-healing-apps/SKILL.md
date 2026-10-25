---
name: verify-self-healing-apps
description: Re-run verification for the primer "The App That Heals Itself" at lukezhang.si/blog/self-healing-apps/: feature map, Playwright harness, and last report live in the draft's verify folder.
---

# Verify: The App That Heals Itself

Primer on Mustafa Ali's October 19, 2026 post: Shopify's mobile apps going self-healing, agents watching production crashes 24x7, reproducing, fixing, verifying, and cutting a 52-second explainer video an engineer reviews and ships. Production sibling of the Who Reviews Claude's Code primer.

- Live: https://lukezhang.si/blog/self-healing-apps/
- Draft: ~/workspace/blog-drafts/self-healing-apps/index.html
- Feature map: ~/workspace/blog-drafts/self-healing-apps/verify/FEATURE_MAP.md
- Harness: ~/workspace/blog-drafts/self-healing-apps/verify/verify.py (port 8960, 390x844)
- Last report: ~/workspace/blog-drafts/self-healing-apps/verify/results.json
- Screenshots: ~/workspace/blog-drafts/self-healing-apps/verify/shots/
- Research: ~/workspace/research_notes/shopify-self-healing-20261019/ (post.json, video, transcript.txt, findings.md)

## Run it

```
python3 ~/workspace/blog-drafts/self-healing-apps/verify/verify.py
python3 ~/workspace/tools/css_audit.py ~/workspace/blog-drafts/self-healing-apps/index.html
```

The harness drives the real UI: the worked-example cumulative stepper (6 rows, 7 notes, Next hides at the end), the 8-panel timeline carousel (46px arrows at the anchor midway, terminal arrows hidden, dots and count), the mechanism-card toggles, card 5's patch picker flipping verdicts both ways, and the zoom bars filling to their data widths with the 500 and 50 per-100,000 readouts. It also asserts computed styles and geometry (hero image box inside the column, hero under 200 KB), a dark-scheme contrast pass, zero em/en dashes, exactly 8 keylines and 2 tags, and live status of every source link (the X post through the fxtwitter API because x.com blocks bots).

## Invariants to keep

- The crash loop and every number inside the video stay flagged on the page as Shopify's own account, demonstrated once, unaudited. No fix rate, acceptance rate, or time saved may be added without a published Shopify source.
- Exactly 8 keylines (one per argument section), exactly 2 tags (AI, Engineering), 6 mechanism cards each with a visual or interaction, 3 voices (the cap), 5 takeaway bullets, takeaways conclusion 60 to 80 words.
- Hero is the Codex illustration (robotic arm stitching a cracked phone screen at night), webp under images/, under 200 KB.
- If the page changes, update FEATURE_MAP.md and this skill in the same pass (maintain-verification-skill).
