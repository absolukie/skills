---
name: "decision-board"
description: "Tappable decision boards. When Luke needs to review options, answer questions, or give feedback, build an interactive decision board (checkboxes, option pickers, autosaved notes fields) instead of a doc or a wall of chat text. He calls this flow 'goated'."
---

# Decision Board Skill

> **Note (2026-10-05):** Luke renamed this flow a **DR (Design Review)**. The `dr` skill is now the canonical playbook — same mechanics, current name. This file stays as the detailed mechanics reference (footer patterns, toast, submit-to-KV, autosave).

## Purpose
Luke makes the final call on creative and decision work. Whenever he needs to review options, answer a set of questions, or give feedback, don't send a document or ask him to reply in prose — build something he can tap: a checklist of decisions with checkboxes/pickers plus free-text notes fields that autosave as he types.

## Workflow
1. Detect the trigger: he's choosing between options (designs, names, directions), reviewing work (critique, survey), or working through a list of questions.
2. Pick the surface:
   - Small set (roughly ≤ 6 questions), answerable in chat: use `widget.create` with kind `html` — tappable checkbox/radio rows plus a notes textarea per question. Keep state in the widget state bridge (`window.hatchWidget.getState` / `setState`) so input survives; show a subtle "saved" indicator.
   - Big surveys, persistent or shareable decisions: build a web artifact with the artifact tools — same checklist pattern, autosave to localStorage, optional summary view of his picks.
3. Structure: one block per question — a clear label, the options as large tappable rows (single- or multi-select as appropriate), and an always-present notes field under each. Big tap targets, `touch-action: manipulation`, iPhone-friendly.
4. Never require a submit click to preserve input — autosave continuously. If there is a "done" action, it only confirms; nothing is ever lost before it.
5. When he responds, report back verdict-first: his picks, his notes, then what happens next. Save durable decisions to memory.

## Output Contract
- Every decision is tappable — never "reply with option B".
- Every question has an optional notes field.
- Input survives refresh, navigation, and interruption.
- Works one-handed on iPhone.
- Every text input and textarea uses 16px+ font — iOS Safari auto-zooms on focus for anything smaller. (Added 2026-10-04: he flagged the zoom on the design-docs notes fields.)

## Operating Rules
1. Creative work always shows multiple distinct options; he picks the winner. Never present a single take as the answer.
2. Never route decision feedback through Google Docs browser automation or any heavy external flow — the checklist is the whole interface.
3. Keep it fast: checklist first, explanation second.
4. Summaries lead with the verdict, reasons after.
5. The copy/export-answers action lives on a sticky footer, always visible no matter how far he's scrolled — never buried at the end of a long page. (Added 2026-10-02: he asked for it mid-flow.) Implement it as a true viewport-fixed bar: `position: fixed; bottom: 0; left: 0; right: 0;` with a solid background, high z-index, iPhone safe-area padding (`env(safe-area-inset-bottom)`), and enough bottom padding on the page body so content never hides under it.
6. Every board ends with an "Other notes" section — a large free-text field (autosaved like the rest) for anything the questions didn't cover. It sits after the last question and above the summary, if there is one. (Added 2026-10-04: he flagged its absence mid-review.)
7. Notes are per-question, not per-section. Every question block gets its own optional notes field directly beneath its options — always. Never collapse these into one shared notes box per section or per page. The "Other notes" section at the end is only a catch-all for things no question covered, never a replacement for per-question notes. (Added 2026-10-04: he corrected a board that had section-level notes.)
8. Every design doc gets an obvious notes field, no matter the doc type. Decision boards have per-question notes (rule 7); every other doc type (sifters, brainstorm tools, surveys, galleries) gets a doc-level notes field in a fixed bottom dock — thumb-reachable, always visible no matter how far he's scrolled, never a scroll away. Labeled, full-width, autosaved like everything else, included in any copy/export output. The dock's notes field is collapsible (a slim bar until tapped), and focusing it must NOT scroll the page away from what he was looking at — on tap, preventDefault + focus({preventScroll:true}) so iOS never does its scroll-to-bottom, and never scrollTo afterward: racing the keyboard animation breaks fixed positioning, and continuously pinning the scroll locks the page (both bit us 2026-10-04). The page needs `interactive-widget=resizes-content` on the viewport meta so the fixed dock lifts above the keyboard via layout resize instead of depending on Safari's native focus path. No doc ships without a place to put notes. (Added 2026-10-04: he flagged the theme-names sifter had nowhere to put notes, then asked for it fixed at the bottom near his thumb, then asked that tapping it not yank him away from the options.)
9. Delivery: projects.lukezhang.si, in the design docs section. New decision boards ship as their own top-level folders on the projects router (NOT the old design-docs-88y.pages.dev site): create `sites/<slug>/index.html` in the `absolukie/lukezhang-si` repo, add the slug to `SITES` in `worker.js`, and add an entry to `sites/design-docs/docs.json` (slug, title, subtitle, date, question count, storageKey) so it shows up in the design docs section at projects.lukezhang.si/design-docs/. Push via gh_push.py, then verify the live URL. The board's back link points to `../design-docs/`. (Changed 2026-10-05: Luke moved all decision docs off the standalone design-docs site to top-level router folders — one source of truth.)
10. Copy actions pop a toast. Every copy/export button shows a transient toast popup ("✓ Answers copied") bottom-center above the footer — a pill with the board's accent color that slides/fades in and auto-dismisses after ~2.2s — so it's unmistakable the copy worked. Don't rely on swapping the button label or savebar text alone. (Added 2026-10-05: he asked for it after copying his swipe-cards verdicts.)
11. Autosave indicator lives in the sticky footer. A small status pill in the footer bar (not buried in page content) shows "Saving…" with a pulsing dot while debouncing and "Saved h:mm" with a green dot after the write lands. (Added 2026-10-05: he asked for it on the black-hole-post-doc.)
12. Submit shows a loading state. While the POST is in flight, the Submit button disables itself and shows a CSS spinner + "Submitting…", then restores. Never leave him tapping a dead button wondering if it worked. (Added 2026-10-05: he asked for it on the black-hole-post-doc.)

## Submit-to-KV pattern (added 2026-10-05)
- Every decision board ships with a **Submit** button next to Copy. Answers must reach Kit, not just sit in the user's browser localStorage.
- Backend: `POST /api/decision/submit` on the projects.lukezhang.si router (in absolukie/lukezhang-si worker.js) stores `{slug, picks, notes}` in Cloudflare KV (`DD_KV` binding, `dd:` key prefix). `GET /api/decision/responses?slug=X&key=DD_READ_KEY` returns newest-first; the key is obscurity-level (it lives in the public repo) — fine for low-sensitivity picks, not for secrets.
- The page POSTs `{slug, picks: state.picks, notes: state.notes}` same-origin on submit and toasts "Submitted — Kit can read it now".
- Slug convention: the board's router folder name (e.g. `redemption-post-doc`).

## Autosave pattern (added 2026-10-05)
- Boards autosave to the server, not just localStorage. Debounce ~2s after the last change, then `POST /api/decision/autosave` `{slug, picks, notes}`. It overwrites a single `dd:draft:<slug>` key in KV (rate limit 120/hr per IP; manual Submit keeps its own 20/hr limit and appends to the response index).
- Show it subtly: the existing savebar dot/text cycles `Saving…` → `Saved` (local) → `Autosaving…` → `Autosaved`. On failure show `Saved on this device`, never an error popup.
- `GET /api/decision/responses?slug=X&key=DD_READ_KEY` returns `{responses: [...], draft}` — when reading, newest wins per key between the latest manual submit and the draft.
