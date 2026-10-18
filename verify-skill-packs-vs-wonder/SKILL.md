---
name: "verify-skill-packs-vs-wonder"
description: "Re-run verification for the primer 'Skill Packs vs. Muse Wonder, Checked' at lukezhang.si/blog/skill-packs-vs-wonder/: feature map, Playwright harness, and last report live in the draft's verify folder."
---

# Verify: Skill Packs vs. Muse Wonder, Checked

Live URL: https://lukezhang.si/blog/skill-packs-vs-wonder/
Draft (canonical source): `~/workspace/blog-drafts/skill-packs-vs-wonder/index.html`
Illustration: `images/stall.webp` in the draft folder (Codex ink illustration: market stall piled with labeled persona boxes vs a workbench with three tools).

## Run it

```bash
cd ~/workspace/blog-drafts/skill-packs-vs-wonder/verify
python3 verify.py            # local draft on a throwaway server
python3 verify.py <url>      # any served URL
```

The harness drives the real UI at 390x844: Fig 1 claim-check stepper (8 steps, 7 claims with verdict chips), Fig 2 head-to-head stepper (5 steps, planted-bug bars), 6 mechanism cards, the Anthropic callout, the 13-step timeline with rule-5 anchored arrows, voices/camps/takeaways counts (8 voices, 4 camps, 6 bullets), section order (takeaways, explore, sources), 21 sources, computed-style and content-inset assertions, and zero pageerrors. It writes `REPORT.md` and screenshots to `shots/` on every run.

Feature map: `~/workspace/blog-drafts/skill-packs-vs-wonder/verify/FEATURE_MAP.md`
Last report: `~/workspace/blog-drafts/skill-packs-vs-wonder/verify/REPORT.md`

## Content invariants (do not let an edit break these)

- Fig 2 numbers are the primer's own measured run (Oct 12, 2026): 8 planted bugs, all three arms found 8 of 8; totals 11 (plain) vs 13 (Osmani skill) vs 13 (agency persona); zero false positives. The grading key and reviews live in `~/workspace/angel-headtohead/`.
- SkillsBench figures never mix versions on the page: v4 headline is +16.6 points (33.9 to 50.5, 87 tasks); v1 supplies the domain spread (+51.9 healthcare, +4.5 software engineering), 16 of 84 negative, focused +18.6 to +20 vs 4+ at about +5, self-generated about minus 1.3.
- Star counts are GitHub API readings of Oct 13, 2026: agency-agents 159,564; wshobson/agents 40,519; knowledge-work-plugins 29,367 (live page); claude-quickstarts 17,938; addyosmani/agent-skills 105,707.

## Quirks

- All three steppers on this page (Fig 1 #ccStage, Fig 2 #fnStage, timeline #tlBody) accept horizontal swipes AND plain card taps that act exactly like arrow taps (Fig 1 added 2026-10-13 at Luke's request, Fig 2 and the timeline added the same day when he widened it to "all carousels here"; the pattern is now visualizers cross-pattern rule 16): pointerdown/pointerup handler, touch-action pan-y set via JS so vertical page scroll stays native, a gesture steps when |dx| is at least 48px and at least 1.5x |dy|, left = next, right = prev, a tap steps forward, no swipe animation or visual affordance, and a click within 400ms after a consumed swipe is swallowed so one flick is never two steps. The harness covers all three with dispatched-PointerEvent and real-input checks (71/71 total).
- Playwright against the live URL fails through this VM's proxy (ERR_TUNNEL_CONNECTION_FAILED). Live proof is curl: page, image, and /primers/ return 200, and served page bytes equal the draft plus exactly 248 bytes (Luke's analytics beacon injected before the closing body tag).
- Meta Newsroom sources (about.fb.com) return 403 to scripted curl but load in a real browser fetch; both Muse articles were confirmed reading correctly before publish.
