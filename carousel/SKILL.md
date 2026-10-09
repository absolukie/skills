---
name: "carousel"
description: "Luke's one-card-at-a-time snap carousel, from the america.gov PII detector: swipeable track, circular ‹ › arrow buttons, per-slide N/total counter, optional group filter chips, tap-a-card to act on it. Zero layout shift — selecting never scrolls the page, every card is equalized to the tallest card's height."
---

# Carousel Skill

## Purpose
Whenever Luke needs a carousel — example galleries, option pickers, card decks — build this exact pattern, not a generic slider library and not a dots-and-peek design. One full-width card visible at a time, swipeable with mandatory snap, circular overlaid ‹ › arrows, a centered `N/total` counter under each card, and optional filter chips above. Tapping a card acts on it in place. He asked for this as a standing UI skill on 2026-10-04, with the explicit bar: it must not shift or bounce.

## When to use it
- Galleries of examples, prompts, designs, or options the user steps through one at a time.
- Any "pick one" flow where each option deserves a full card (decision boards use checklists instead; carousels are for browsing, not multi-select).
- Never for hero banners or auto-playing marketing rotators — if it moves on its own, it isn't this.

## Structure
```html
<div class="car-filters" id="carFilters" aria-label="Groups"></div>   <!-- optional -->
<div class="tcar">
  <div class="ttrack" id="ttrack" aria-label="Examples"></div>        <!-- slides injected by JS -->
  <button class="tnav prev" id="tprev" aria-label="Previous">‹</button>
  <button class="tnav next" id="tnext" aria-label="Next">›</button>
</div>
```
Each slide is a full-width card plus its own counter:
```html
<div class="tslide">
  <button class="tslide-card">…card content…</button>
  <p class="tcount">3/50</p>
</div>
```

## CSS essentials
- Track: `display:flex; overflow-x:auto; scroll-snap-type:x mandatory;` hidden scrollbar (`scrollbar-width:none` + `::-webkit-scrollbar{display:none}`), `overscroll-behavior-x:contain` so edge swipes never bounce the page, `border-radius` to match cards.
- Slide: `flex:0 0 100%; scroll-snap-align:center; scroll-snap-stop:always;` — `always` is what keeps rapid arrow taps from stranding the track between cards.
- Arrows: 46px circles, absolutely positioned at the track's vertical center, sitting in side gutters (`padding:0 30px` on the carousel wrapper, arrows at `left:0`/`right:0`) — never overlapping card text. Backdrop blur, subtle shadow.
- Counter: centered, mono, tabular numbers, `N/total`.
- Filters (if used): horizontal scroll row of pill chips, active chip accented.

## JS controller
- `load(i)`: wraps the index (`((i % n) + n) % n` — prev from first goes to last), applies the selection (loads content into the tool above / shows the detail), then `track.scrollTo(i * track.clientWidth, 0)` — instant, never smooth.
- Arrows call `load(idx - 1)` / `load(idx + 1)`.
- Card tap calls `load(i)` — the whole card is the tap target.
- Track scroll updates `idx` via rAF-throttled `Math.round(scrollLeft / clientWidth)`.
- iOS backstop: after scrolling stops (180ms timeout + `scrollend` where supported), snap to the nearest slide if more than 2px off. This only fires when a tap interrupts a glide mid-flight; when the browser's native snap already settled, it's a no-op.

## Output Contract
- One card visible at a time, always.
- Every slide shows its own `N/total` counter.
- Arrows and swipe both work on desktop and 390px mobile; no horizontal page overflow.
- Zero console errors.

## Operating Rules — the no-shift, no-bounce bar
These are the rules he set when commissioning this skill. Every carousel ships with all of them:
1. **Selecting never scrolls the page.** No `scrollIntoView`, no smooth scrolling to a tool above. Put the carousel adjacent to what it drives and update in place. Tapping 50 cards in a row must leave `window.scrollY` untouched.
2. **Every card is the same height.** After every render (and after every filter change), measure all cards and pin each to the tallest card's height. Re-run on debounced window resize. Swiping between a tall card and a short card must not move a single pixel vertically.
3. **Track moves are instant, never smooth.** Arrow taps use instant `scrollTo`. Only the user's own finger swipe animates, driven by the browser's native mandatory snap.
4. **Contain overscroll.** `overscroll-behavior-x:contain` on the track so edge swipes don't rubber-band the page.
5. **`touch-action:manipulation` on every tap target** — arrows, cards, filter chips — so rapid taps never double-tap-zoom.
6. **Arrows live in gutters, not over content.** Give the carousel wrapper side padding and park the arrows in it; verify with bounding boxes that no arrow overlaps card text at 1280px and 390px.
7. Keep `scroll-snap-stop:always` and the iOS settle backstop — they prevent the stranded-between-cards state, not bounce.

## QA checklist (run before calling it done)
- Arrow next/prev through the full set, including wrap-around both directions.
- Tap a card → correct content applied, `scrollY` unchanged.
- Filter (if present) → slide count and counters update, heights re-equalized.
- Manual swipe to a fractional offset → settles on the nearest slide.
- Rapid repeated arrow taps → never stranded between cards.
- Desktop 1280px and mobile 390×844: no horizontal overflow, arrows clear of text, all cards equal height.
- Zero page errors.
