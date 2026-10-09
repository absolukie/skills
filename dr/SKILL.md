---
name: "dr"
description: "Run a Design Review (DR): walk through any piece of work — a blog post, a website, a design, a plan, anything needing a decision — piece by piece, asking Luke about every part. Builds a tappable review board where he makes the final calls. Trigger on: 'DR', 'design review', 'run a DR on this', 'review this', 'put this through a DR'."
---

# DR — Design Review

## Purpose
A DR is the standing format for reviewing anything that needs Luke's decision. Kit walks through the work piece by piece and asks about every part; Luke taps his calls. One block per unit of the work, in original order, each with a clear question and options. Luke makes every final call.

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

## Privacy rule (boards are unlisted, not private)
DR boards live on the projects router: unlisted URLs, but anyone with the link can open them. When the subject is private (real names, intimate or personal content), redact ON the board: names become initials, intimate verbatim content stays out, decisions stay fully reviewable. Put a short privacy note at the top of the board naming what was redacted. The underlying work is never redacted, only the board. (Set 2026-10-05 on the "Us" book DR: her name appeared as "G." with a visible note.)

## Output contract
- **Every block is a card, in order.** Each card shows: the current content verbatim, 2–3 tappable alternatives, an explicit decision question ("Your call: which wording ships?"), a "Kit's take" pre-vet note, and a per-block notes field ("My wording").
- **Title pick first** (for posts) or the equivalent framing decision, with real alternatives.
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
DRs ship as their own top-level folders on the projects router: create `sites/<slug>/index.html` in the `absolukie/lukezhang-si` repo, add the slug to `SITES` in `worker.js` (fetch it fresh from the GitHub API immediately before editing — never edit a stale `/tmp` copy), and add an entry to `sites/design-docs/docs.json` (slug, title, subtitle, date, question count, storageKey) so it lists in the design docs section at `https://projects.lukezhang.si/design-docs/`. The board's back link points to `../design-docs/`. Push via `~/workspace/skills/github/bin/gh_push.py`, then verify the live URL returns 200 and the mechanics work.
