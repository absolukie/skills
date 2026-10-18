---
name: verify-hugging-face-incident
description: Verify the Hugging Face incident primer (lukezhang.si/blog/hugging-face-incident/, "The Exam That Broke Out") against its feature map by running the Playwright harness, which drives the real UI (chain stepper with gestures, mechanism cards, census dot grid, exposure explorer, timeline) and asserts computed styles, rendered geometry, and the page's sourced numbers.
---

# Verify The Exam That Broke Out

Feature map: `~/workspace/blog-drafts/hf-incident/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/hf-incident/verify/verify.py` (local port 8943)

Run it:

```
python3 ~/workspace/blog-drafts/hf-incident/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's numbers must match the primary sources: 17,613 recovered actions (Hugging Face per-day table: 3,779 / 1,135 / 7,677 / 3,892 / 1,130); phase census sums to 16,521 with dropper 6,972 and recon 6,191 (79.7 percent of the itemized total together); 198 of 898 ExploitGym tasks unsolved (22 percent); 136 keys in one secret object; 41 production dataset workers (OpenAI count). Where the companies conflict (customer content scope, detection dates), the page shows both accounts attributed; do not "fix" one side away.

Invariants the harness guards:
- Chain stepper: 8 panels, click-per-step via Next, card tap, dispatched-pointer swipes both ways, and arrow keys; terminal arrows display:none; dots + "n of 8" count track position.
- Mechanism cards: 6, first open, third card toggles through its real header, chevron SVG renders at 20px.
- Census: 100 dots; July 11 chip fills exactly 44; caption carries the exact per-day counts; 9 phase rows with dropper bar widest.
- Explorer: 4 chips swap the panel; verdict line changes per category.
- Timeline: 13 panels, terminal next arrow hides.
- Voices 8, camps 3 agree + 3 split (each split has 2 sides), takeaways conclusion 55 to 85 words with 5 bullets, 3 keep-exploring links with icons, 11 sources.
- No KaTeX on this page by design (arithmetic worked panel instead); the harness asserts no .katex nodes exist.
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (copied from feel-physics; the page's own style block covers dg, xp, calc, flagbox hooks).
