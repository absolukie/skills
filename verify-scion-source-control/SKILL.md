---
name: "verify-scion-source-control"
description: "Re-run verification for the primer 'When Agents Outgrew Git' (Scion / agent-scale source control) at lukezhang.si/blog/scion-source-control/: feature map, Playwright harness, and last report live in the draft's verify folder."
---

# Verify: When Agents Outgrew Git

Live URL: https://lukezhang.si/blog/scion-source-control/
Draft (canonical source): `~/workspace/blog-drafts/scion-source-control/index.html`
Illustration: `images/archive.webp` in the draft folder (Codex ink illustration: archive tower of tiny drawers, paper-bird couriers carrying single pages, a book cart stuck in mud, rust-red gate).

## Run it

```bash
cd ~/workspace/blog-drafts/scion-source-control/verify
python3 verify.py            # local draft on a throwaway server
python3 verify.py <url>      # any served URL
```

The harness drives the real UI at 390x844: Fig 1 pressure stepper (7 steps, 6 gauge rows), Fig 2 checkout stepper (6 steps, 3 stage rows, cache bars), Fig 3 precedents explorer (4 chips, Scion default), 6 mechanism cards, the vendor-caveat callout, the 10-step timeline with rule-5 anchored arrows, swipe and tap-to-advance gesture checks on all three steppers, voices/camps/takeaways counts (7 voices, 4 camps, 2 versus, 6 bullets), section order (takeaways, explore, sources), 13 sources, computed-style and content-inset assertions, and zero pageerrors. It writes `REPORT.md` and screenshots to `shots/` on every run. Last result: 76/76.

Feature map: `~/workspace/blog-drafts/scion-source-control/verify/FEATURE_MAP.md`
Last report: `~/workspace/blog-drafts/scion-source-control/verify/REPORT.md`

## Content invariants (do not let an edit break these)

- Every scale figure is the publishing company's own claim, labeled as such on the page: Anthropic (2,500 to 30,000+ merges/day May to Sep 2026, ~100 GB history, 25+ GB working copy, ~25M CI checkouts/day, 600+ PB naive traffic as 25M x 25 GB = 625 PB, several hundred mirrors, 200x smaller infra, seconds-not-minutes checkouts, 25% CI CPU win, Mythos rewrite 20x memory / 4x speed), Piper (Jan 2015 data: 86 TB, ~1B files, 35M commits, 40,000 commits/day, CitC under 10 files), GVFS (Windows 3.5M files, 270+ GB, clone 12+ hrs to minutes, checkout 2-3 hrs to 30 s, status ~10 min to 4-5 s), GitHub (7.38B commits Sep 2026, up to 35x write throughput, internal benchmarks).
- The Cursor post's byline (Vicent Marti) is attributed via The Register and flagged secondary wherever it appears; Simon Willison's voice is labeled commentary, not reportage.
- Anthropic's team byline is initials-only in the source (Nick G. and the source control team); do not invent full names. Martin von Zweigbergk has NO Scion statement; his voice is framed as the standing alternative, never as a reaction.
- Scion is never presented as a general git replacement or a public product; the vendor caveat callout carries Anthropic's own framing.

## Quirks

- All three steppers (Fig 1 #ccStage, Fig 2 #fnStage, timeline #tlBody) ship with the visualizers rule-16 gesture contract from the start: horizontal swipe steps like an arrow tap (at least 48px, at least 1.5x horizontal dominance), a plain card tap steps forward, touch-action pan-y set via JS so vertical page scroll stays native, no animation or affordance, and a click within 400ms after a consumed swipe is swallowed so one flick is never two steps.
- The Fig 2 "all rows revealed" expectation differs by design: cc has 6 rows for 6 steps (5 lit at the end, the last row's note carries it), fn has 3 stage rows for 6 steps (all 3 lit). The harness encodes this as min(rows, steps - 1).
- Playwright against the live URL fails through this VM's proxy (ERR_TUNNEL_CONNECTION_FAILED). Live proof is curl: page, image, and /primers/ return 200, and served page bytes equal the draft plus exactly 248 bytes (Luke's analytics beacon injected before the closing body tag).
- Research: `~/workspace/research_notes/scion-agent-scale-source-control-20261013-2329/report.md` (deep research) plus a full first-party read of the Anthropic post. Twitter-as-precedent and other-AI-lab VCS claims were unverifiable and are excluded in the footer note.
- Shell-family invariant (Luke caught the violation on his phone, 2026-10-13): in the cc/fn cumulative-row steppers, notes must equal rows + 1, because rows light for j < idx. Scion's Fig 1 shipped with 6 notes and 6 rows, so the last row ("the workaround stack") could never light and the stepper read as stuck on the final step. Fixed the same day by adding a seventh wrap note; the harness's all-rows check now asserts all 6 rows lit at the end. When cloning this shell, count rows and notes before writing copy.
