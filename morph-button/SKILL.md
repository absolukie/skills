---
name: "morph-button"
description: "A button that performs its primary action, then smoothly morphs into the natural next-step action (copy → share, download → open, send → track). Luke commissioned it 2026-10-04 from the lukezhang.si draw pad — he loved the springy icon morph and had the dark tint removed."
---

# Morph Button Skill

## Purpose
For sequential two-step actions where the second step only makes sense right after the first: copy → share, download → open, save → send. One button does the primary action; on success it animates into the secondary action; it morphs back the moment context changes. No extra chrome, no mode confusion.

Reference implementation: the draw pad at https://lukezhang.si/draw/ (repo `absolukie/lukezhang-si`, `draw/index.html`, `#dlBtn` block) — crib the WAAPI choreography from there.

## The pattern
- **State A (default, always):** primary action. Icon A, normal styling.
- **User taps → primary action succeeds → morph to State B:** secondary action. Icon B. A short confirmation (pill/toast like "copied") fires alongside.
- **Morph back to A on any context change:** new input, undo, clear, secondary action completed or dismissed.

## Operating Rules
1. **Default state is always the primary action.** The button must never load in, or get stuck in, State B.
2. **Morph only fires right after the primary action succeeds.** Never spontaneously, never on a timer.
3. **Morph back the instant context changes.** New input, undo, clear, share completed/dismissed — all revert. A stale State B is the failure mode.
4. **Both glyphs stay mounted and stacked.** Absolutely-positioned spans sharing one center; crossfade + transform between them. Never `innerHTML`-swap the icon — the eye must be able to track the change.
5. **Choreograph with the Web Animations API, not setTimeout.** Outgoing: ~180ms, fades/scales/rotates slightly out. Incoming: ~400ms, springs in with a subtle overshoot (scale ~1.06, ±1° rotate) using per-keyframe easing. Button itself does a gentle 1 → 1.06 → 1 pop on entry only. Transform and opacity only — 60fps.
6. **Interruptible by construction.** On every `setMode` call: read the current rendered pose first (including mid-flight), cancel running animations, commit the new state, then animate from the captured pose to the new resting pose. Rapid toggles must never desync or strand a half-visible icon.
7. **Tint is optional and usually wrong.** He had the dark State-B tint removed — the icon morph plus the animation already carries the state change. If a tint is ever used, its transition must run in sync with the icon motion, never snap.
8. **Labels always match the mode.** `aria-label`/`title` update on every morph; the icon wrapper is `aria-hidden`.
9. **`touch-action: manipulation`** on the button. No double-tap zoom, ever.
10. **`prefers-reduced-motion`: instant swap.** No WAAPI, no transitions — just the state change. Also cancel in-flight animations if the setting flips mid-morph.
11. **If the primary action can fail** (clipboard refused, etc.), fall back to performing the secondary action directly on that tap — never leave the user with a dead button and no feedback.

## What sucked before (don't regress)
The first version used a `setTimeout`-driven two-phase swap: icon shrank to 0.3, `innerHTML` hard-swapped at max shrink, then popped back — it read as collapse → teleport → pop. The background tint snapped instantly while the icon was mid-scale. Easing was dead `ease` over 130ms. A re-tap mid-flight could desync the timeout from the class toggle. Every one of these is fixed by rules 4–6.

## QA checklist (run before calling it done)
- Mid-morph, computed opacities of both icons sit strictly between 0 and 1 (real crossfade, not sequential).
- Settled: incoming opacity exactly 1, outgoing exactly 0, zero running animations on the button.
- Trigger revert mid-morph (new input during the animation): ends exactly in State A, labels correct, no stuck halves.
- Ten rapid primary taps: state stays coherent, no desync, no errors.
- `prefers-reduced-motion` emulated: instant swap, `getAnimations()` empty, no errors.
- Zero console errors, 390px mobile, no layout shift around the button.
