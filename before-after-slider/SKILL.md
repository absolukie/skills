---
name: "before-after-slider"
description: "Before/after comparison slider for photos and edits: drag a divider 1:1 with the finger, tap anywhere to glide there, arrow keys nudge. Unedited left, edited right. The container never changes size, so dragging can't shift the page.

**Reference implementation:** https://comparison-lab.pages.dev/refine.html (section 01, "Thin-bar diff slider") — this is the locked final spec. The design doc capturing his decisions: https://design-docs-88y.pages.dev/docs/comparison-slider/"
---

# Before/After Slider Skill

## Purpose
Show two states of the same image — unedited vs edited, before vs after, raw vs processed — with a draggable divider. The reader drags to compare; the interaction itself is the explanation. Luke's lead use case (2026-10-04): showing photo edits.

## Structure
```html
<div class="ba" role="slider" aria-valuemin="0" aria-valuemax="100" tabindex="0">
  <img src="after.jpg" alt="Edited photo">                    <!-- base: AFTER, right side -->
  <img class="ba-before" src="before.jpg" alt="Unedited photo"> <!-- top: BEFORE, clipped -->
  <div class="ba-divider"><div class="ba-line"></div><div class="ba-handle">‹ ›</div></div>
  <span class="ba-tag tag-before">Unedited</span>
  <span class="ba-tag tag-after">Edited</span>
</div>
```
Convention: **before on the left, after on the right**, divider starts at 50%.

## The chosen dragger: Notch
Luke chose the **Notch** on 2026-10-04 after comparing twelve designs (https://before-after-lab.pages.dev/draggers.html): a 6×24px white tick straddling a 2px divider line — no circle, no chevrons, no background. The gallery page stays up for future comparisons.

## Operating Rules
1. **The container never changes size.** Fixed `aspect-ratio` (match the photos, e.g. 3/2), `overflow:hidden`. Divider and clip move in pixel space only — divider via `transform: translateX(x px)`, the before image via `clip-path: inset(0 <w-x>px 0 0)`. No layout, ever; dragging can't shift the page.
2. **Grabbable at any time — even mid-scroll.** The slider owns every touch from `pointerdown` (`touch-action:none` + `setPointerCapture`), so it answers while the page is scrolling, not just when it's still. After 12px of movement the gesture locks by direction: mostly-horizontal drives the divider; mostly-vertical scrolls the page 1:1 itself, with momentum on release. This is the rule he stated when the first version felt dead mid-scroll.
3. **1:1 finger tracking.** Horizontal moves set position directly from the pointer x (rAF-throttled). No smoothing, no lag — direct manipulation is the feel.
4. **Tap glides.** A press with <6px movement and <300ms duration counts as a tap even before the direction lock engages: the divider animates to the tap point with an ease-out (~380ms). Grabbing mid-glide cancels it.
5. **Clamped travel.** Divider range is 2%–98% — the handle never half-clips at the edges.
6. **Manual scroll fallback.** Because `touch-action:none` disables native touch scrolling over the slider, vertical drags must scroll the page manually (`window.scrollTo`, 1:1) with velocity-tracked momentum on release, clamped to the page bounds. Mouse wheel is unaffected (wheel ignores touch-action).
7. **Handle affordance.** The Notch: 6×24px white rounded tick, subtle shadow, grows ~1.35× while dragging via transform only.
8. **Keyboard**: `←`/`→` nudge ±4%, `Home`/`End` jump to the clamped extremes. Proper `role="slider"` with `aria-valuenow`.
9. **Labels**: small "Unedited"/"Edited" chips in the top corners; a "drag" hint chip that fades permanently after the first grab.
10. Images: same dimensions, same crop, `object-fit:cover`, `draggable="false"`, `pointer-events:none` so the browser never hijacks the gesture.

## QA checklist
- Drag end to end: divider and clip stay in sync, no jitter at 60fps.
- Tap left/right: glides and lands within 2% of the tap point.
- Container bounding box identical before, during, and after drags (desktop + 390px).
- Keyboard nudges, Home/End respect the 2%/98% clamp.
- Vertical page scroll works when swiping up/down starting on the image.
- Both images load (no broken states); zero console errors; no horizontal overflow.
