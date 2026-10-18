---
name: "dr"
description: "Run a Design Review (DR): walk one piece of work (post, site, design, plan) piece by piece on a tappable board where Luke makes every final call. Trigger on: 'DR', 'design review', 'run a DR on this', 'review this', 'put this through a DR'."
---

# DR — Design Review

A DR reviews one work that needs Luke's decisions. Kit walks it piece by piece; Luke taps his calls.

## Scope: one DR, one goal
- One goal per board, stated on the intro step in one sentence. If it takes two sentences, it is two DRs. (Set 2026-10-17.)
- Never bundle unrelated calls. A second goal that surfaces becomes its own DR.
- Subjects (a channel, an app, a post) accumulate small focused DRs over time, never one growing mega-board. Example, Your Soup Is Typing: separate DRs for its background image, its video tool's features, Monday's video, and future video ideas.
- Building a DR includes categorizing it (see Deployment). An uncategorized board is unfinished.

## Trigger
"DR this", "run a DR", "design review", "put this through a DR", "review this"; any post, site, design, copy, or plan nearing a ship, revise, or kill call.

## Workflow
1. Read the source in full. Every word and every diagram goes on the board, in original order, nothing summarized away.
2. Break it into blocks: one card per paragraph, section, screen, or decision point, in order.
3. Pre-vet each block: what is strong, what is weak, what needs his call. Write 2 to 3 genuine alternatives per block, never filler.
4. Build the board per the contract below.
5. Deploy, verify live, send the link.
6. On submit, report verdict-first: his picks, his notes, what happens next. Save durable decisions to memory.
7. Read his answers from `GET /api/decision/responses?slug=X&key=DD_READ_KEY` on the projects router (the key is in the public worker.js; obscurity-level, fine for low-sensitivity picks). Dedupe repeat submits; report picks, then notes, then what changes.

## Privacy: gated, never anonymized
Boards and the design-docs section sit behind the "DR Boards" Cloudflare Access app (id 06ee5f0f-23dd-4c4a-9e5e-a6c8245796f3; absolukie@gmail.com only, one-time PIN, 24-hour sessions), so content goes on the board exactly as written, names included; never redact. Coverage inventory: ~/workspace/design-docs-gate/COVERAGE.md. /api/decision/* stays ungated on purpose: boards POST submits there, and reads are key-protected.

## Output contract
- Block = card, in order: content verbatim, 2 to 3 tappable alternatives, an explicit question ("Your call: ..."), a Kit's take note, a notes field.
- Title pick (or the equivalent framing call) first.
- **Real artifacts, no stand-ins.** (Set 2026-10-17: "I want the actual prototypes not shortcuts.") Every option is the thing itself: videos embedded and playable (full render, or a short true preview render if unproduced); images at full size; designs as mockups or working prototypes; features as working mini-demos where possible; text options in full. If an artifact cannot be produced or embedded, the block says so, gives the reason, and links the live thing. A description never poses as the artifact.
- Step-through, not scroll: one question per screen. Intro, questions in order, Other notes, Final call. Sticky stepbar: progress bar, "Question N of M · K left" counter, Back and Next. Next never moves; Back is disabled, never hidden, on step 0. Dots under the buttons: green when answered, ring on the current one, tap to jump. The final step's Next is Submit. Arrow keys navigate, ignored while typing. Scroll to top on step change. Selecting an option inside a step updates in place and never scrolls the page; the scroll reset belongs to step changes only.
- Autosave: instant and invisible to localStorage under a per-DR key. The server draft (`POST /api/decision/autosave`) and the footer pill debounce together after about 1.2s idle: the pill never flickers per keystroke; it shows "Saving…" (pulsing amber), then "Autosaved h:mm" (green).
- Sticky footer: autosave pill, Copy answers (toast "✓ Answers copied"), Submit (spinner and "Submitting…" while the POST is in flight, then restores and toasts). Submit posts {slug, picks, notes, final, otherNotes} to `POST /api/decision/submit`.
- Mobile-first: inputs 16px minimum, `touch-action: manipulation` on tap targets, safe-area footer padding, back link to the DR overview.
- No em dashes in any copy, ever. Use commas, colons, or periods.

## Board status (overview)
- **Completed:** Luke has submitted, even if some questions are unanswered.
- **Partially complete:** not submitted, but he has started answering one or more questions (a server draft from autosave, or a draft still on his device).
- **Open:** not submitted and nothing answered.
The overview derives these from submissions and drafts on the decision API; there is no separate done flag.

## Operating rules
1. Luke makes every final call. Kit pre-vets, never decides.
2. Creative work shows multiple distinct options, never one take as the answer.
3. Every decision is tappable. Never "reply with option B".
4. Board first, explanation second. The board is the whole interface: no Google Docs, no email threads.
5. Notes are per-block, under the options, on every block, with a Clear notes button (right-aligned, muted); clearing autosaves and offers Undo for 5 seconds. Other notes gets the same.
6. Options toggle: tapping a picked option deselects it. Never trap him in a choice.
7. Summaries lead with the verdict, reasons after.

## Deployment
Create `sites/<slug>/index.html` in absolukie/lukezhang-si; add the slug to `SITES` in worker.js (fetch it fresh from the GitHub API first; never edit a stale copy) and an entry in `sites/design-docs/docs.json` (slug, title, subtitle, date, question count, storageKey, category). That registry is what lists the board on the DR overview; the design-docs page itself is retired and redirects to the overview. The category comes from a fixed set (YouTube, Games, Apps, Business, Writing, Faith, Personal, Systems); pick the closest fit. Add a new category only when none fits, and note the addition in the ship report. Back link: `../dr-overview/` (the DR overview, per Luke's 2026-10-18 ruling). Push via `~/workspace/skills/github/bin/gh_push.py`. Verify the live URL returns 200 and the mechanics work. Then gate before sending the link: add `projects.lukezhang.si/<slug>` as a destination on the DR Boards app and verify an unauthenticated fetch returns 302 to the Access login with zero page bytes. Never send a board ungated.
