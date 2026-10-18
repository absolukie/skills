---
name: verify-what-is-rl
description: "Verify the 'What Is Reinforcement Learning?' primer (lukezhang.si/blog/what-is-rl/): feature map, Playwright harness, and report. Run after any edit to the page."
---

# Verify: What Is Reinforcement Learning? primer

Live URL: https://lukezhang.si/blog/what-is-rl/
Draft source: ~/workspace/blog-drafts/what-is-rl/index.html (canonical; deploy by
surgical overlay to blog/what-is-rl/ in absolukie/lukezhang-si, plus the images
at blog/what-is-rl/images/loop.webp and blog/what-is-rl/images/aha.webp, plus a
card in primers/index.html)

Feature map: ~/workspace/blog-drafts/what-is-rl/verify/FEATURE_MAP.md
Harness: ~/workspace/blog-drafts/what-is-rl/verify/harness.py
Last report: ~/workspace/blog-drafts/what-is-rl/verify/REPORT.md

Run locally: `python3 ~/workspace/blog-drafts/what-is-rl/verify/harness.py`

The harness drives the real UI at 390x844: hero and illustration checks, content
inset measured on the h1 (the .wrap box itself is full width by design), 8
mechanism cards (tap toggle with aria-expanded, styled open body), the 5-step
loop carousel and the 14-step timeline carousel (rule 5: 46px arrows anchored at
the anchor card's midway, arrow box identical across steps, terminal arrows
display:none, dots plus count, arrow-key advance with guards), the 7-step
worked-math carousel (one supervised gradient step and one policy-gradient step
with real numbers, value rows asserted inside the card), the 5-step
R1-Zero scoreboard (rows light progressively, the 71.0 percent fill measured
against the track width), 8 voice cards, 5 camps, 6 takeaways, 4 keep-exploring
cards, 26 source cards, zero pageerrors. Last run: 54/54.

Quirks: illustrations come from the Codex CLI image generator (never the Muse
media pipeline). OpenAI pages refuse scripted fetches (403) while opening fine
in a browser; if the link check flags them, confirm via a page read before
treating them as dead. PubMed returns its abstract page with a non-200 code to
scripts.
