---
name: "explainer-tools"
description: "Luke's family of explainer UI tools: the reusable interactive patterns for his explainer sites and posts. Start here when building anything that teaches — pick the right tool, then read its skill."
---

# Explainer Tools

## Purpose
Luke is building a family of reusable explainer UI tools — one per pattern, each with its own skill, feel lab, and hard-won interaction rules. When he asks for an explainer, a teaching widget, or "one of my UI tools," start here, pick the pattern that fits, then read that tool's SKILL.md and build to its rules.

## The family
| Tool | Skill | Status |
|------|-------|--------|
| **Carousel** — one-card-at-a-time snap gallery: swipeable, ‹ › arrows, N/total counter, filter chips, tap-card acts in place | `carousel` | Shipped |
| **Step-through animator** — walk a process one operation at a time; big satisfying Next button (Glide feel), Back, counter, progress | `step-through-animator` | Shipped |
| **Before/after slider** — drag a divider 1:1 to compare two states (unedited vs edited photos); grabbable even mid-scroll | `before-after-slider` | Shipped |
| **Visualizers** — four data patterns from the SPF post: zoom bars (magnified inset for tiny deltas), dot-grid simulator (staggered probability re-runs), live formula slider (what-if readouts + insight line), estimator + caveat card (estimate beside its overriding warning) | `visualizers` | Shipped |
| **Analogy bridge** — analogy beside the real thing, hovering one highlights the matching part of the other | — | Queued ("huge") |
| **Misconception flip** — "everyone thinks X" card, tap to flip to "actually Y, here's proof" | — | Queued ("huge") |

Feel labs (live iteration pages): step-through https://step-through-lab.pages.dev, before/after https://before-after-lab.pages.dev (+ `/draggers.html` for handle designs).

## Shared rules — every tool obeys all of these
1. **No shift, no bounce.** Selecting, stepping, or dragging never moves unrelated UI. Reserve space for the tallest content state; transforms fully reset; track/divider moves use transform only, never layout.
2. **Real data or clearly labeled simulation.** Steps come from the actual algorithm; photos are real pairs; a mock says it's a mock.
3. **`touch-action: manipulation`** on every tap target (no double-tap zoom). Full-area drag surfaces use `touch-action:none` with a manual direction lock so vertical drags still scroll the page.
4. **Pointer-first interactions.** Press visuals start on `pointerdown`, not `click`. Pointer capture on drags. Keyboard equivalents for everything (`←`/`→`, Home/End).
5. **Bespoke chrome, no emoji.** UI icons are inline SVG. No emoji as controls, ever.
6. **Mobile is the primary viewport.** Every tool is QA'd at 390×844: no horizontal overflow, no dead zones, no trapped scrollers.
7. **Zero console errors** before calling anything done.

## Workflow
1. Match the teaching goal to a tool (browsing examples → carousel; watching a process → stepper; comparing two states → slider; busting a myth → misconception flip; bridging intuition → analogy bridge).
2. Read that tool's SKILL.md — its Operating Rules are the spec, including the exact feel Luke chose.
3. If no tool fits, propose the new pattern as a feel lab first (like step-through-lab): real content, one interaction, iterate on feel with him before skill-ifying it.
4. Ship feel labs as standalone Cloudflare Pages sites; write the SKILL.md when the feel is locked.
