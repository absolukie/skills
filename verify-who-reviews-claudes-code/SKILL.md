---
name: verify-who-reviews-claudes-code
description: Re-run verification for the primer "Who Reviews Claude's Code?" at lukezhang.si/blog/who-reviews-claudes-code/: feature map, Playwright harness, and last report live in the draft's verify folder.
---

# Verify: Who Reviews Claude's Code?

Primer on Anthropic's Claude Code team code review post (October 15, 2026), from the @claudedevs announcement post.

- Live: https://lukezhang.si/blog/who-reviews-claudes-code/
- Draft: ~/workspace/blog-drafts/who-reviews-claudes-code/index.html
- Feature map: ~/workspace/blog-drafts/who-reviews-claudes-code/verify/FEATURE_MAP.md
- Harness: ~/workspace/blog-drafts/who-reviews-claudes-code/verify/verify.py (port 8956, 390x844)
- Last report: ~/workspace/blog-drafts/who-reviews-claudes-code/verify/results.json
- Screenshots: ~/workspace/blog-drafts/who-reviews-claudes-code/verify/shots/

## Run it

```
python3 ~/workspace/blog-drafts/who-reviews-claudes-code/verify/verify.py
python3 ~/workspace/tools/css_audit.py ~/workspace/blog-drafts/who-reviews-claudes-code/index.html
```

The harness drives the real UI: both panel steppers (life of a change, timeline), the mechanism-card chips, the attention-math sliders (asserts the exact readouts at the default and at the May 2026 anchor), the risk-tier explorer (default, billing, untrusted, docs), and the worked-example stepper. It also asserts computed styles and geometry (46px arrows straddling the stage edge at the active panel's midway, hero image box inside the column, equalized panel heights), a dark-scheme contrast pass, zero em/en dashes, and live status of every external link (X links verified through the fxtwitter API because x.com blocks bots).

## Invariants to keep

- Exactly 3 keylines, exactly 2 tags, 6 mechanism cards each with a visual or interaction.
- Internal Anthropic metrics stay attributed on the page; the curl 8.23.0 sequel stays marked as reported coverage.
- If the page changes, update FEATURE_MAP.md and this skill in the same pass (maintain-verification-skill).
