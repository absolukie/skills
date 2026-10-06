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

## Output contract
- **Every block is a card, in order.** Each card shows: the current content verbatim, 2–3 tappable alternatives, an explicit decision question ("Your call: which wording ships?"), a "Kit's take" pre-vet note, and a per-block notes field ("My wording").
- **Title pick first** (for posts) or the equivalent framing decision, with real alternatives.
- **Final call card at the end**: ship / revise / kill (or the decision's equivalent options).
- **Other notes** catch-all after the last question.
- **Everything autosaves.** Debounced writes to localStorage under a per-DR storage key. The sticky footer carries the autosave status pill: "Saving…" with a pulsing amber dot while debouncing, "Saved h:mm" with a green dot after the write lands.
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
6. Notes are per-block, not per-section. Every block gets its own notes field directly beneath its options, always.
7. Summaries lead with the verdict, reasons after.

## Deployment (Luke's setup)
DRs ship as their own top-level folders on the projects router: create `sites/<slug>/index.html` in the `absolukie/lukezhang-si` repo, add the slug to `SITES` in `worker.js` (fetch it fresh from the GitHub API immediately before editing — never edit a stale `/tmp` copy), and add an entry to `sites/design-docs/docs.json` (slug, title, subtitle, date, question count, storageKey) so it lists in the design docs section at `https://projects.lukezhang.si/design-docs/`. The board's back link points to `../design-docs/`. Push via `~/workspace/skills/github/bin/gh_push.py`, then verify the live URL returns 200 and the mechanics work.
