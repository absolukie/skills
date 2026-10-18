---
name: "dr"
description: "Run a Design Review (DR): walk through any piece of work — a blog post, a website, a design, a plan, anything needing a decision — piece by piece, asking Luke about every part. Builds a tappable review board where he makes the final calls. Trigger on: 'DR', 'design review', 'run a DR on this', 'review this', 'put this through a DR'."
---

# DR — Design Review

## Purpose
A DR is the standing format for reviewing anything that needs Luke's decision. Kit walks through the work piece by piece and asks about every part; Luke taps his calls. One block per unit of the work, in original order, each with a clear question and options. Luke makes every final call.

## Scope: one DR, one goal
- **One goal per board.** Every DR carries exactly one well-defined, clear goal, stated on its intro step in one sentence. If the goal cannot be stated in one sentence, it is more than one DR. (Set 2026-10-17.)
- **Never bundle unrelated calls.** A board answers the questions its one goal raises, in order, and nothing else. If a review surfaces a second goal along the way, that goal becomes its own DR instead of joining this board.
- **Subjects accumulate focused DRs over time.** Boards are organized by subject (a channel, an app, a post), and each subject collects small single-goal DRs as the work comes up, rather than one growing board that tries to hold everything about the subject.
- **Example, in Luke's terms (Your Soup Is Typing):** one DR for creating the channel's background image; one DR for creating a tool to help make videos, and what features to add to it; one DR for generating Monday's video, with many options to pick from; one DR for future video ideas for the channel. Four goals, four boards, one subject.

## Trigger
- "DR this", "run a DR", "design review", "put this through a DR", "review this"
- Any blog post, website, design, copy, or plan nearing a ship/revise/kill decision.

## Workflow
1. **Read the source in full.** Every word and every diagram goes into the DR, in original order. Nothing omitted, nothing summarized away. (Standing rule 2026-10-05.)
2. **Break it into review blocks.** One card per paragraph / section / screen / decision point, in reading order.
3. **Pre-vet honestly.** For each block: what's strong (protect it), what's weak (flag it), what needs his call. Write 2–3 genuine alternatives per block — real options, never filler.
4. **Build the board** per the output contract below.
5. **Deploy and verify.** Serve it live, check it renders, send him the link.
6. **When he submits**, report back verdict-first: his picks, his notes, then what happens next. Save durable decisions to memory.
7. **Reading his answers.** Kit pulls them from `GET /api/decision/responses?slug=X&key=DD_READ_KEY` on the projects router (the key lives in the public worker.js; it is obscurity-level, fine for low-sensitivity picks). Returns newest-first plus the latest autosaved draft. When he says "added some notes", read this endpoint, dedupe repeat submits, and report verdict-first: picks, then notes, then what changes.

## Privacy rule (boards are gated, never anonymized)
DR boards are private. Every board path and the design-docs section sit behind the "DR Boards" Cloudflare Access application (app id 06ee5f0f-23dd-4c4a-9e5e-a6c8245796f3, Luke only: allow absolukie@gmail.com, one-time PIN login, 24-hour sessions), gated 2026-10-17 at Luke's direction so boards never need anonymizing again. Because only Luke can open a board, board content is never anonymized or redacted: the full source goes on the board exactly as written, real names and intimate content included, and no privacy note is needed. (This replaces the 2026-10-05 unlisted-boards rule, under which names were redacted to initials on the board itself.) The coverage inventory and per-path verification results live in ~/workspace/design-docs-gate/COVERAGE.md. The /api/decision/* endpoints stay ungated on purpose: board pages POST submits there and the read endpoint is key-protected.

## Output contract
- **Every block is a card, in order.** Each card shows: the current content verbatim, 2–3 tappable alternatives, an explicit decision question ("Your call: which wording ships?"), a "Kit's take" pre-vet note, and a per-block notes field ("My wording").
- **Title pick first** (for posts) or the equivalent framing decision, with real alternatives.
- **Real artifacts, no stand-ins.** Every option on a board is the thing itself, never a text description of it. (Set 2026-10-17: "I want the actual prototypes not shortcuts.") Videos are embedded in the board, playable: the full render when it exists, or a short true preview render when the option is not yet produced. Images are the rendered images at full size. Designs are rendered mockups or working prototype pages. Features are working mini-demos wherever a demo is possible. Text options are the full text. This extends the workflow rule for source material (every word and every diagram goes on the board in full) to the alternatives themselves: the options get the same full-fidelity treatment as the source. If an artifact genuinely cannot be produced or embedded, the block says so plainly, gives the reason, and links the live thing where one exists; a description is never dressed up as the artifact.
- **Step-through, not scroll.** One question per screen. Flow: intro step ("Start"), the questions in order, Other notes as its own step, Final call last. A sticky bottom stepbar carries: progress bar, a "Question N of M · K left" counter, Back / Next buttons. The Next button never moves between steps (sticky footer; Back is disabled, never hidden, on step 0). Dots below the buttons show every step: green when answered, ring on the current one, tap any dot to jump. On the final step Next becomes Submit. Arrow keys go back/forward (ignored while typing in a field). Scroll to top on every step change. (He asked for it 2026-10-05: "not scrolling, once you answer you move to the next with a click.")
- **Other notes** catch-all after the last question.
- **Everything autosaves.** Instant, invisible writes to localStorage under a per-DR storage key. The server draft (`POST /api/decision/autosave`) and the footer's status pill are debounced together: the pill must NOT flicker "Saving…" on every keystroke. Only after ~1.2s of no input does it show "Saving…" with a pulsing amber dot, then "Autosaved h:mm" with a green dot after the write lands. (He flagged the flickering pill 2026-10-05.)
- **Sticky footer, always visible**: autosave pill + Copy answers + Submit. Copy pops a toast ("✓ Answers copied"). Submit disables itself with a CSS spinner + "Submitting…" while the POST is in flight, then restores and toasts the result.
- **Submit reaches Kit**, not just localStorage: `POST /api/decision/submit` `{slug, picks, notes, final, otherNotes}` (see Submit-to-KV pattern in the decision-board skill).
- **Mobile-first**: 16px minimum on all inputs/textareas (iOS zooms on anything smaller), `touch-action: manipulation` on tap targets, safe-area footer padding, back link to the index.
- **No em-dashes in any copy, ever.** Rewrite with commas, colons, or periods.

## Operating rules
1. Luke makes the final call. Kit pre-vets, never decides.
2. Creative work always shows multiple distinct options; never present a single take as the answer.
3. Every decision is tappable — never "reply with option B".
4. Keep it fast: the board first, explanation second.
5. Never route review feedback through Google Docs, email threads, or any heavy external flow. The board is the whole interface.
6. Notes are per-block, not per-section. Every block gets its own notes field directly beneath its options, always. Each notes field ships with a subtle one-tap **Clear notes** text button beneath it (right-aligned, muted). Clearing wipes that block's notes, updates state, and autosaves like any other edit, then shows a toast with **Undo** (5-second window) that restores the wiped text. The "Other notes" catch-all gets one too. (He asked for it 2026-10-05: a way to wipe a note without selecting all and deleting, then wanted the safety net.)
7. Summaries lead with the verdict, reasons after.
8. Options are toggleable. Tapping a selected option deselects it (clears the pick), so Luke can always change his mind back to undecided. Never trap him in a choice.

## Deployment (Luke's setup)
DRs ship as their own top-level folders on the projects router: create `sites/<slug>/index.html` in the `absolukie/lukezhang-si` repo, add the slug to `SITES` in `worker.js` (fetch it fresh from the GitHub API immediately before editing — never edit a stale `/tmp` copy), and add an entry to `sites/design-docs/docs.json` (slug, title, subtitle, date, question count, storageKey) so it lists in the design docs section at `https://projects.lukezhang.si/design-docs/`. The board's back link points to `../design-docs/`. Push via `~/workspace/skills/github/bin/gh_push.py`, then verify the live URL returns 200 and the mechanics work. Then gate the new board before sending Luke the link: add `projects.lukezhang.si/<slug>` as a public destination on the "DR Boards" Access app, and verify an unauthenticated curl of the board URL returns a 302 to the Access login with zero page bytes. A board is never sent to Luke ungated.
