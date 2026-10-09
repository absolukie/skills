---
name: "mastery-sheet"
description: "Build a 'mastery sheet': an interactive single-page visualizer that takes someone from zero to fluent on one topic. Trigger on: 'mastery sheet', 'master this topic', 'build me a mastery visualizer', or any request to learn a topic deeply through an interactive study page."
---

# Mastery Sheet

## Purpose
Generate a "mastery sheet" for any topic: one self-contained HTML page with 8 sections that moves the reader from zero to fluent. Distilled from the Taylor series mastery sheet (https://projects.lukezhang.si/taylor-mastery-draft/, local source `~/workspace/blog-drafts/taylor-mastery/index.html`), which is the canonical reference implementation. Read it before starting a new sheet.

## The 8-section anatomy
1. **The one idea.** One framing sentence + the general formula/statement. KaTeX if math. This is the whole topic in one breath.
2. **The core set.** The 4-6 essential cases as tappable cards. Each card: formula/statement, a small canvas sparkline or diagram showing it working, and badges for gotchas. Tap to expand/collapse.
3. **The "why" stepper (the heart of the sheet).** A first-principles walkthrough with Next/Back that derives the key mechanism step by step. Example: on the Taylor sheet, differentiating x to the fourth four times while the multiplier accumulation (4 x 3 x 2 x 1 = 4!) is shown building. This section is what makes the topic click. Budget the most design time here.
4. **The shortcut.** The pattern-recognition trick experts use (on Taylor: odd/even symmetry). If a related sheet already demonstrates it, link there with a button instead of rebuilding.
5. **When to use it.** Three cards: computing, approximating, understanding something deeper. At least one card gets a live interactive: slider + true/approx/miss readouts + an insight line that names the takeaway.
6. **The failure mode.** Where the idea breaks (on Taylor: radius of convergence). A slider-driven canvas plot that shows the breakdown happening live, with an insight line explaining why.
7. **Self-test flashcards.** Exactly 6 tap-to-flip cards (3D flip), each with "Knew it" / "Still learning" buttons and a live x/6 score. Flip on card tap; score-button taps must not flip the card (stopPropagation).
8. **Keep exploring.** 3-4 cards linking related sheets, each with the link-out icon. End with one kicker-close line that ties the topic together.

## Build workflow
1. Pick the slug, working title, and exactly two tags from the taxonomy (ai, llms, engineering, math, infrastructure, design, business, science, tools, language, culture). Never tag "interactive".
2. Copy `~/workspace/blog-drafts/taylor-mastery/index.html` to `~/workspace/blog-drafts/<slug>/index.html` as the starting skeleton, then replace section by section. Copy `~/workspace/blog-drafts/katex-vendor/katex` into the draft as `katex/` when formulas are used (relative paths).
3. Write section 3 first. Everything else supports it.
4. Keep the visual system identical across sheets: paper `#f6f1e3` background, `#b3352b` accent, `.viz` cards, `.fcard` tappable cards, `.flash` flashcards, `.xlinks` keep-exploring grid, `.btn`/`.btn.ghost` buttons, verdict lede, meta tags, kicker close.

## Operating rules
- Re-read `~/workspace/skills/visualizers/SKILL.md` before building (slider spec: 34px input, 4px track, 16px visible knob via radial-gradient, 50px invisible hit box, `touch-action: pan-y`, `filter: drop-shadow` never `box-shadow`; never the transparent-border thumb trick).
- **Hide terminal stepper buttons; never disable them.** At the first step hide Back, at the final step hide Next/Done (`display:none`). A greyed-out button reads as broken on mobile.
- **Cross-article buttons carry a link-out icon.** Small bespoke external-link SVG (inline, `currentColor`, 14px, never emoji) on every button/card that navigates to another sheet. Icon markup lives in the Taylor reference.
- Simple language, his voice, dry humor, no em dashes or en dashes anywhere. Inputs 16px minimum. `touch-action: manipulation` on all taps. Bespoke SVG icons, never emoji in UI chrome. Zero third-party requests (KaTeX vendored).
- KaTeX: explicit single-dollar and double-dollar delimiters, `throwOnError: false`, `ignoredClasses: ["nokatex"]` for literal dollar amounts. Re-run `renderMathInElement` on dynamically injected nodes. Wide formulas scroll internally (`overflow-x: auto` on `.formula`); the page itself never overflows. Grid/flex parents of formulas need `min-width: 0` / `minmax(0,1fr)` so KaTeX can't stretch columns.
- Flashcards: `.flash.flipped .inner { transform: rotateY(180deg) }`, `prefers-reduced-motion: reduce` kills the transition. Score buttons stopPropagation. Live x/6 in `.scorebar`.
- Canvas plots: devicePixelRatio-aware sizing from `clientWidth`, `drawLine`/`drawAxes` helpers from the Taylor reference. Redraw on `resize`.
- `"use strict"` in the IIFE. No top-level `var` named after a `window` API (`history`, `name`, `status`, `location`, `top`, `self`, `event`, `length`, `closed`).

## QA checklist
- HTML tag balance check (scripted), zero em/en dash assertion (scripted), `node --check` on extracted JS.
- Playwright at 390x844: exercise EVERY interactive end to end (all cards expand, full stepper forward AND back with 300ms+ waits, all sliders across range, all 6 flashcards flip + both score paths, retake/reset), zero `pageerror`s, `document.documentElement.scrollWidth <= 390`, screenshots of hero + each interactive reviewed at full size.

## Deploy
- Push `sites/<slug>/` (index.html + katex/) to `absolukie/lukezhang-si` via **surgical overlay only**: fetch current head, one blob per file, new tree on `base_tree` = head tree, commit, then re-read the ref and PATCH only if it still points at the head you built on (compare-and-swap; abort if it moved). Never a full-tree push.
- worker.js SITES entry: re-fetch worker.js fresh from the GitHub API into a NEW temp file every time (never edit a stale /tmp copy), confirm the existing SITES entries are present, add the new slug, push with the same compare-and-swap guard.
- Verify live: the served URL returns HTTP 200 and the response HTML contains the page's title and key section markers. Only then report the link.
