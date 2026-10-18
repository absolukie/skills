---
name: verify-saas-you-no-longer-need
description: "Verify 'The SaaS You No Longer Need' primer (lukezhang.si/blog/saas-you-no-longer-need/): feature map, Playwright harness, and report. Run after any edit to the page."
---

# Verify: The SaaS You No Longer Need primer

Live URL: https://lukezhang.si/blog/saas-you-no-longer-need/
Draft source: ~/workspace/blog-drafts/saas-you-no-longer-need/index.html (canonical; deploy by
surgical overlay to blog/saas-you-no-longer-need/ in absolukie/lukezhang-si, plus the image
at blog/saas-you-no-longer-need/images/shelf.webp)

Feature map: ~/workspace/blog-drafts/saas-you-no-longer-need/verify/FEATURE_MAP.md
Harness: ~/workspace/blog-drafts/saas-you-no-longer-need/verify/verify.py
Last report: ~/workspace/blog-drafts/saas-you-no-longer-need/verify/REPORT.md

Run locally: `python3 ~/workspace/blog-drafts/saas-you-no-longer-need/verify/verify.py`

The harness drives the real UI at 390x844: five force cards (tap toggle with
aria-expanded), the stack calculator (typical $326/mo, Levels mode $87.49/mo
with 8 struck lines, flip back restores), 14 verdict rows, the 9-step timeline
(rule 5: 46px arrows anchored at the card midway, terminal arrows display:none,
dots plus count), 8 voice cards with source links, 21 sources, 4 keep-exploring
cards, zero em/en dash scan. A pageerror fails the run. Last run: 30/30.

Quirks: the illustration is generated via the Codex CLI image generator (never
the Muse media pipeline). BusinessWire and Inc. block scripted link checks
(000/403) while serving fine to readers; if the link check flags them, confirm
via a page read before treating them as dead.
