---
name: "swipe-cards"
description: "Tinder-style swipeable card deck: drag a card left/right to decide, it flings off with rotation; buttons and arrow keys as fallback; undo, progress, and an end-of-deck results screen. Built for triaging a list — keep vs skip — one card at a time."
---

# Swipe Cards Skill

## Purpose
Whenever Luke needs a swipe-through deck — triaging todos, rating ideas, going through a list one card at a time — build this exact pattern. One card on top of a peeking stack, drag left to dismiss / right to keep (or the reverse if he says so), card follows the finger with rotation, KEEP/SKIP stamps fade in with the drag, release past the threshold flings it off. He commissioned this on 2026-10-04 after the carousel and step-through skills: "tinder style cards that you need to swipe right to go through."

## When to use it
- Triage flows: a long list the user works through with binary decisions (todos, ideas, quotes, designs).
- "Go through the deck" experiences where each item deserves a full card and a deliberate gesture.
- Never for browsing without decisions — that's the carousel skill. Never for multi-select — that's decision boards.

## Structure
```html
<div class="deck-zone">
  <div class="deck" id="deck"><!-- top 3 cards injected by JS --></div>
</div>
<div class="actions">
  <button class="abtn nope" id="btnNope" aria-label="Skip">✕</button>
  <button class="abtn undo" id="btnUndo" aria-label="Undo">↺</button>
  <button class="abtn like" id="btnLike" aria-label="Keep">♥</button>
</div>
```
Top card:
```html
<div class="scard top">
  <div class="stamp like">KEEP</div>
  <div class="stamp nope">SKIP</div>
  <div class="snum">#247 <span class="batch">batch a</span></div>
  <p class="stext">…card content…</p>
</div>
```

## CSS essentials
- Deck zone: fixed height (`clamp(400px, 56vh, 540px)`), `position:relative`.
- Card: absolutely positioned, `left:0; right:0; margin:0 auto; width:min(420px,100%)` — centers without touching `transform`, which the drag owns. Rounded 22px, shadow, `user-select:none`, `will-change:transform`.
- **Top card gets `touch-action:none`** so the drag never scrolls the page (per the draggable rule). Cards behind get `pointer-events:none`.
- Behind cards: `translateY(k*10px) scale(1 - k*0.045)`, dimmed (opacity .85 / .55) — the peek-a-boo stack.
- Stamps: absolute top corners, 4px bordered labels rotated ±14°, `opacity:0`; JS drives opacity from drag distance.
- Buttons: 72px circles (like button 84px), `touch-action:manipulation`, `:active{transform:scale(.9)}`.

## JS controller
- Pointer events unified (`pointerdown/move/up/cancel` + `setPointerCapture`) — one code path for mouse and touch.
- On move: `dx,dy` from start; `transform = translate(dx,dy) rotate(clamp(dx*rot, ±20deg))`; stamp opacity = `min(1, |dx|/90)` on the matching side.
- On release: decision if `|dx| > 120` **or** flick velocity `> 0.55 px/ms` with `|dx| > 40` (velocity from last ~80ms of moves). Otherwise spring back with the feel's easing.
- Fling: transition per feel, fly to `x = dir * (innerWidth*0.75 + 200)`, `y = dy*1.6`, `rotate(dir*24deg)`; on timeout record decision, splice from remaining, render next.
- `busy` flag blocks input during the fling; buttons disabled while busy.
- Undo: pop history, delete decision, unshift index back to remaining, re-render.
- Keyboard: `←` skip, `→` keep (ignored when typing in an input).
- Render only the top 3 cards; recycle DOM on every advance.
- Persist decisions in localStorage so a 1000-card deck survives sessions; on boot, filter out decided cards.

## Feels (the lab lets him pick)
- **Snappy**: 200ms fling `cubic-bezier(.3,.6,.6,1)`, rotation factor 0.05, 200ms ease-out spring-back.
- **Buttery** (default): 320ms fling `cubic-bezier(.3,.7,.3,1)`, rotation 0.07, 380ms spring-back with slight overshoot `cubic-bezier(.2,.9,.25,1.25)`.
- **Floaty**: 500ms ease-in-out fling, rotation 0.10, 500ms spring-back.

## Output Contract
- Dragging the top card moves it 1:1 with the finger, with rotation; stamps fade in on the correct side.
- Release past threshold (or a fast flick) flings the card off and advances; short drags spring back to center.
- Buttons and arrow keys produce the identical fling as a drag.
- Undo restores the exact card to the top; progress and kept-count stay correct.
- End of deck → results screen: kept/skipped counts, kept list, copy button, restart.
- Desktop 1280px and mobile 390×844: no horizontal page overflow, deck centered, buttons reachable by thumb.

## Operating Rules
1. **`touch-action:none` on the draggable card, `touch-action:manipulation` on every button.** Drag never scrolls; taps never double-tap-zoom.
2. **Never fight the transform.** Card centering uses `left:0; right:0; margin:auto` — never `translateX(-50%)`, because JS owns `transform`. Entrance animations use fill `backwards` (never `both`/`forwards`), and `pointerdown` clears any running transition.
3. **One decision per gesture.** The `busy` flag plus disabled buttons prevent double-fires during the fling.
4. **Velocity matters.** A fast flick under the distance threshold still counts — otherwise quick triaging feels dead.
5. **Persist progress.** Any deck over ~50 cards saves decisions per card id in localStorage and resumes on load.
6. **Results screen is part of the pattern.** Counts, the kept list, copy-to-clipboard, and start-over — a deck that just ends feels broken.

## QA checklist (run before calling it done)
- Drag right past threshold → KEEP stamp, card flings right, kept count +1, next card rises.
- Drag left → SKIP stamp, flings left.
- Short drag → springs back to center, no decision recorded.
- Fast flick under threshold → still decides.
- Buttons ✕/♥ and ←/→ keys → same fling as drag.
- Undo → exact card back on top, counts correct; undo button disables when history empty.
- Reload mid-deck → resumes where left off.
- Finish deck → results screen with correct counts, kept list, working copy button, restart.
- 390px mobile: card fits, drag smooth, no page scroll during drag, no horizontal overflow.
- Zero console errors.
