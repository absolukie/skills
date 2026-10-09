---
name: "step-through-animator"
description: "Step-through animator for explainers: walk an algorithm or process one operation at a time with a big satisfying Next button, Back, step counter, and progress bar. Luke chose the Glide feel on 2026-10-04. Hard rule: the Next button never moves between presses — its resting position is pixel-identical on every step."
---

# Step-Through Animator Skill

## Purpose
For explainers where the reader should watch a process happen one operation at a time — BPE merges, algorithm steps, pipeline stages, state transitions. A stage shows the current state, a big **Next** button advances exactly one step, **Back** retreats, and a counter plus progress bar show where you are. The button itself is the product: it must feel good enough to tap fifty times.

## The chosen feel: Glide
Luke picked **Glide** on 2026-10-04 after comparing three personalities in the feel lab (https://step-through-lab.pages.dev):
- **Glide (default)** — soft 160ms press to scale(.96), calm 300ms ease-out release, chips crossfade in sequence, low synth thock. For narrative pacing.
- Pop — deep squash, spring overshoot, chips jump. Playful explainers.
- Crisp — tight 90ms press, merged element flashes once. Precise technical walkthroughs.

New animators ship with Glide unless he asks otherwise. The feel lab stays up for A/B comparisons.

## Structure
```html
<div class="stage">
  <div class="chips" id="chips"></div>      <!-- current state -->
  <p class="caption" id="caption"></p>       <!-- what just happened -->
  <div class="prog"><i id="progFill"></i></div>
</div>
<div class="controls">
  <button id="backBtn">← Back</button>
  <button id="nextBtn">Next →</button>
</div>
```
Steps are data: `[{parts:[...], merged:'en', rank:262, note:'...'}, ...]` — real algorithm output, never mocked.

## Operating Rules
1. **THE NEXT BUTTON CANNOT MOVE BETWEEN PRESSES.** Its resting bounding box must be pixel-identical on every step, desktop and 390px mobile, including after rapid-fire taps. This is the rule he stated when commissioning the skill. Three things conspire to break it — handle all three:
   - *Variable content height*: captions and chip rows differ per step. Fix: measure every step's rendered height in a hidden probe at the real stage width on init (and on resize), then pin `min-height` to `ceil(max) + 1px` on each region. The +1 absorbs sub-pixel rendering differences between the probe and the real element.
   - *Press transform residue*: the press uses `transform: scale()`, which never affects layout, and the release transition always returns to exactly `none`. Verify with bounding-box sampling, not by eye.
   - *Wrapping rows*: on narrow screens chips wrap to two rows on some steps. The pinned min-height covers the tallest wrap state.
2. **Press starts on `pointerdown`, never `click`.** The squash visual begins the instant the finger lands; `preventDefault()` to skip focus ring/delay. Release (`pointerup`) springs back and advances the step. `pointercancel`/`pointerleave` only release the visual, never advance.
3. **`touch-action: manipulation`** on every control. Rapid taps must never double-tap-zoom.
4. **Keyboard works**: `→` next, `←` back. Buttons also handle Enter/Space with the same press visual.
5. **Wrap-around ending**: the last step's button reads Finish → then becomes Replay, which returns to step 0. Back is disabled at step 0.
6. **Progress + counter always visible**: `N / total` and a filling bar. The bar's motion matches the feel (Glide: 400ms ease).
7. **Sound is garnish**: a tiny per-feel synth blip (WebAudio, created on first gesture) is allowed, but there is always a visible toggle, and it never blocks the step.
8. **Rapid taps are safe**: advance is synchronous and idempotent per press; no animation queue can stack up or strand the state.
9. Real data or clearly labeled simulation. Steps come from the actual algorithm.

## QA checklist (run before calling it done)
- Sample the Next button's `getBoundingClientRect().top` on every step, after full release settle, desktop + 390px mobile: all samples identical to the pixel.
- Ten rapid taps: button still exactly home, step index correct (wraps properly).
- Resize mid-session: min-heights re-pin, button still home.
- Full walk forward and back; Replay wraps to step 0; Back disabled at step 0.
- Keyboard arrows advance/retreat.
- Sound toggle on/off; no errors with sound on or off.
- Zero console errors, zero horizontal overflow on mobile.
