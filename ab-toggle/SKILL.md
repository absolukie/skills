---
name: "ab-toggle"
description: "Single-button A/B toggle for comparisons: one switch, every tap flips — no side-picking. Sliding thumb shows the active side, stage crossfades between versions."
---

# A/B Toggle Skill

## Purpose
The A/B comparison toggle for design docs and blog posts. One switch, one stage: the user taps the whole button and the comparison flips. There is deliberately no way to "pick a side" — tapping the active side flips too, so rapid taps always do something.

**Reference implementation:** https://comparison-lab.pages.dev (section 03, "A/B toggle"). The design doc capturing his decisions: https://design-docs-88y.pages.dev/docs/ab-toggle/

## Structure
- A single `<button role="switch" aria-checked="false">` — the entire button is the tap target (`touch-action: manipulation`).
- Inside: a sliding `.thumb` plus two labels (A left, B right). The thumb covers the active side.
- Below: a `.stage` with two absolutely-positioned layers (`.va`, `.vb`), crossfading via opacity.

## Behavior
1. **Every tap flips.** No selected-side state to "re-pick" — each click toggles. Spamming the button alternates A/B/A/B with no dead taps.
2. **Sliding thumb.** The thumb is absolutely positioned at `left:5px; width:calc(50% - 5px)`; the flipped state moves it to `left:50%`. Transition ~280ms with a slight overshoot (`cubic-bezier(.5,0,.2,1.15)`). Active label is light on the dark thumb; inactive label is muted.
3. **Stage crossfade.** `.va`/`.vb` toggle `opacity` 1/0 with a ~450ms ease. `prefers-reduced-motion` disables both transitions.
4. **Keyboard and SR.** It's a native `<button>`, so Space/Enter flip for free. `aria-checked` mirrors the state; `aria-label` names both sides ("Flip between X and Y").
5. **Self-contained init.** The wiring function takes only the root element and references nothing outside itself, so it can be stringified into a copy-paste embed snippet (same contract as the before-after-slider skill).

## Operating Rules
1. Never split it into two pick-a-side buttons — the single-switch behavior is the whole point (his call 2026-10-05: "just hitting the entire button should flip it").
2. The thumb must always indicate the *currently shown* side, not the side a tap would show.
3. Keep the tap target generous: full-width up to ~420px, 16px+ labels, `touch-action: manipulation` so rapid taps never zoom.
4. Don't put the toggle inside the stage — the button sits above it, the stage below, so a tap never confuses "flip" with "interact with content."
5. **Thumb labels get internal horizontal margin** (his 2026-10-10 call: on the how-models-learn primer the "Predict representations" label touched the thumb edges). Each label needs breathing room inside the thumb: minimum ~14px of horizontal margin on each side. Size the thumb and track so the longest label fits comfortably — shrink the label font, widen the thumb, or both, but never let label text touch the thumb edge. Verify with a screenshot at 390px: if any glyph grazes the pill boundary, it fails.
