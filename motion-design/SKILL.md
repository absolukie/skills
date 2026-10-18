---
name: "motion-design"
description: "Motion design system for explainer films and animated web pieces: story-arc timing bands, a motion language where movement carries meaning, scene-spec format, visual-system tokens, copy/sound/accessibility rules, an animation performance section (frame budget, composite-only properties, jank diagnosis, from Emil Kowalski), and a verification checklist. Distilled from the @0xMovez motion-studio post (prompt by @0xCarnagee, principles from Meaghan Choi, ex-Meta/Anthropic designer). Use when building any explainer video, animated hero, or scroll-driven animated page, and whenever an animation is janky or drops frames."
---

# Motion Design Skill

## Purpose
A complete, opinionated system for motion pieces that teach one thing. Covers the full arc from discovery to verified render. Source: the motion-studio prompt in https://x.com/0xMovez/status/2107515767986217026 (prompt wording by @0xCarnagee; principles are Meaghan Choi's from her public talks). The teachings below are paraphrased into working rules.

## Core principles
1. **Shape before polish.** Settle the one idea and the viewer's mental model first. Polish is the last pass, never the first.
2. **Ask review questions before designing.** Who is it for? What exactly is being communicated? Does this thing need a name, or can it stay invisible?
3. **Never start from nothing.** Anchor to the brand, the product, and real screenshots. This is what separates a designed piece from the generic look every model produces by default.
4. **Go wide, then choose.** Produce 3–4 directions side by side in one page. The page doubles as the decision log: mark the winner and write down why.
5. **Restraint is taste.** Cut whatever does not serve the idea. If a move does not teach, it goes.

## Discovery (before any drawing)
- Write the **one question** the piece answers, in the viewer's own words.
- Split facts into a **must-know list** and a **cut list**. The cut list stays out, no matter how interesting.
- Find the **hook**: the belief most viewers already hold that turns out to be wrong. Open there.
- Use a metaphor **only if it makes the idea more accurate**. Otherwise show the real thing.

## Story arc: timing bands
For a 30–90 second piece. Percentages are of total runtime.

| Band | % | Job |
|---|---|---|
| Question | 0–10 | Open on the thing people get wrong, as an image, not a title card |
| Model | 10–50 | Build the smallest correct picture of how it works, one element at a time |
| Proof | 55–75 | Run the model on a real case; let cause and effect play out on screen |
| Turn | 75–90 | Change one variable and show what follows. Understanding clicks here |
| Payoff | 90–100 | The opening image again, now read correctly, plus one next step |

Note the gap at 50–55: a breath between building the model and proving it. Pacing needs air.

## Motion language
Motion is not decoration. Every move must carry meaning, and it carries exactly four kinds:
- **Grouping** (these things belong together)
- **Order** (this happens before that)
- **Cause** (this made that happen)
- **Scale** (this is bigger / smaller / more important)

Rules:
1. **One focal action at a time.** Everything else holds still. Two moving things means the viewer watches neither.
2. **Transform, don't replace.** Keep objects alive across scenes: a dot becomes a node, a label becomes an axis. Continuity is comprehension.
3. **Ease like it settles.** Custom easing that decelerates into rest. No bounce unless bounce is the lesson.
4. **Camera reframes between ideas, never during reading.** Move the camera to signal "new idea"; hold it still while text is being read.
5. **Enter, key action, settle, exit.** Every scene's motion is these four beats in this order. If you cannot name the key action, the scene has none and should be cut.

## Visual system
1. **Tokens before drawing.** Pull palette, type, and spacing from the brand into tokens first. No drawing until tokens exist.
2. **The kit:** warm neutral ground, one accent color, two typefaces, one grid. That is the whole system.
3. **Prefer the real thing.** Real UI, real data, clean diagrams beat illustration every time for explainers.
4. **Banned list.** Neon glow. Stock 3D blobs. Gradient title cards. Floating particles. These are the four horsemen of generic.

## Scene spec (write one per scene)
```
[ID] + time range (e.g. S3 · 0:12–0:20)
Teaches: the one thing this scene adds (one sentence)
Frames:  what's on screen, in order of importance
Motion:  enter → key action → settle → exit
Words:   on-screen text, max 8 words per line (anchors, not transcript)
Sound:   the cue marking the key action
Check:   what the viewer can now say that they couldn't before
```
If a scene's "Teaches" duplicates another scene's, merge them.

## Copy rules
- Max **two lines** of text on screen at once.
- **Plain words before jargon.** If the jargon must stay, the plain word introduces it.
- **Never put the full voice line on screen.** On-screen words are anchors; the voice carries the sentence.
- **One name per thing**, used every time. No synonyms.
- **Every number needs a source** or it goes.

## Sound
- One **tempo-locked bed** with **one motif** that returns on the key idea. The viewer should feel the motif land.
- **SFX only on actions that carry meaning.** If the motion doesn't teach, it doesn't get a sound.
- Duck the bed under voice. Target around **-16 LUFS** integrated.
- Check it **muted** (does the motion still teach?) and **audio-only** (does the sound still make sense?).

## Accessibility (non-negotiable)
- Contrast at least **4.5:1** on all text.
- Captions **burned in** and shipped as a separate `.srt`.
- **Color is never the only signal.** Pair every color cue with shape, label, or position.
- No flashes above **3 per second**.
- Ship a **reduced-motion cut** that keeps the same sequence of ideas with the motion removed.

## Web translation (for scroll pages, not video)
Luke's explainers are scroll pages, not films. Map the system:
- **Timing bands → scroll sections.** Question = hero/verdict. Model = the interactive diagram. Proof = the live demo. Turn = the what-if control. Payoff = the kicker restating the opening.
- **Camera reframes → scroll-triggered transitions.** A section entering the viewport is a reframe: animate the transition in, then hold still while the reader reads.
- **window.seek(t) → scroll position.** The render contract (every frame a pure function of t) maps directly to scroll-driven animation: element state = f(scrollY). Seeded randomness only, so replays are identical.
- **Reduced-motion cut → `prefers-reduced-motion` media query.** Same content, motion removed. The ideas must survive without animation.
- **Verification stills → 390px screenshots.** Every beat must read on a phone screen; text legible, no overflow.

## Animation performance (frame budget)
Distilled 2026-10-12 from Emil Kowalski's `animation-performance` skill (MIT, https://github.com/emilkowalski/skills, announced https://x.com/emilkowalski/status/2109277388437868623). His framing: performance is not a polish pass after the motion is good, it is what lets good motion register at all. Sonner at 30fps is the same code and nobody cares.

**The budget.** 60fps gives the browser 16.7ms per frame. On a 120Hz screen, now most phones, it is 8ms. Design against the smaller number. A layout recalculation on a complex page can take over 100ms: that is not one missed frame, it is a dozen. Never conclude "it's fine" from a fast laptop; the bar is a mid-range phone. Luke's pages are phone-first, so this is the default case, not the edge case.

**Hard rules.**
1. **`transform` and `opacity` by default.** Anything else needs a reason. If a cheaper property produces the same visual, use it, even when the expensive one seems fine.
2. **Name the cause before changing code.** Every fix states which cause below it addresses. "Added `will-change`, seems smoother" is not a diagnosis.
3. **Never `transition: all`.** List the exact properties. `all` animates whatever changes next, including layout properties nobody intended.
4. **Don't trade correctness for a best-effort optimization.** Hardware acceleration is something the browser may grant; which properties you animate is something you control. Spend effort on the second. Percentage transforms (`translateY(100%)`) stay the right call for elements of unknown size even though browsers have historically not accelerated them.

**Property tiers.** To show a visual change the browser runs layout (measure size and position), paint (draw into layers), composite (put layers on screen). Every property enters at one point, and the cost differs by an order of magnitude:
- **Composite only (cheapest):** `transform`, `opacity`, and in current Chrome/Firefox also `filter`, `clip-path`, `background-color`. Promoted to their own layer.
- **Paint + composite:** `box-shadow`, `border-radius`, `color`. No re-measuring, but a redraw every frame.
- **Layout + paint + composite (most expensive):** `width`, `height`, `padding`, `margin`, `top`, `left`, `border-width`. One growing element can move everything around it.

**Swap down a tier:**
| Instead of | Animate |
|---|---|
| `width` / `height` / `padding` to grow or shrink | `scale()` |
| `top` / `left` / `margin` to move | `translate()` (percentages are relative to the element's own size) |
| `display` / `visibility` swaps | `opacity` |
| `box-shadow` | `filter: drop-shadow(...)` |

The last one is the one people miss: an animated shadow looks harmless but repaints the element every frame. Layout animations do not always drop frames (an absolutely positioned element with few children can get away with `padding`), but a `padding` animation and a `scale()` animation look the same and only one cannot regress on a slower device. Pick the one with no downside. Layout properties also move the wrong things: animating a sidebar's `margin-left` pushes the content beside it every frame; `translateX` does not.

**Where it runs.** JavaScript animation via `requestAnimationFrame` always runs on the main thread and competes with everything else the page is doing; when the main thread is busy, the frame is late. CSS transitions/keyframes and the Web Animations API (`element.animate()`) can be hardware-accelerated off the main thread. Reliably accelerated: `transform` and `opacity`. The trap pattern is motion that plays while the page is busy: route changes, tab indicators during navigation, anything firing alongside fetching or hydration. Vercel's dashboard animated its tab indicator with a JS shared-layout animation while the next page loaded and dropped frames; moving it to CSS fixed it. Working split: CSS for simple motion and anything that plays while the page is busy; JS animation for complex, interruptible, gesture-driven motion. (Framer Motion note, for React work: the `x`/`y`/`scale` shorthands are implemented with CSS variables and are not accelerated; animate the full `transform` string when the motion must survive a busy main thread.)

**Don't animate through React state.** A hand-rolled animation that calls `setState` every frame re-renders the component every 16.7ms and the render alone blows the budget. Write to `ref.current.style` (or a motion value) instead. Look for state updates inside `requestAnimationFrame`, `pointermove`, `scroll`, or drag handlers.

**Two traps that look correct.** Both use `transform` and still drop frames:
- **Inherited CSS variables.** Vaul's drag got laggier once a drawer held more than about 20 items, with no re-renders: the drag distance was written to a CSS variable that `translateY()` read. Variables inherit, so changing one on a parent recalculates styles for every descendant, every frame. The more content, the slower each frame. Fix: set `transform` directly on the element. Suspect this whenever a transform animation degrades as content grows.
- **Blur.** `filter: blur()` gets expensive fast, especially in Safari. Keep animated blur under 20px; 2 to 5px is enough to soften a crossfade.

**`will-change` is the last step, not the first.** A browser can hand an animation from CPU to GPU mid-flight, and that hand-off can shift the element by a pixel at the start or end. `will-change: transform` promotes the element up front so no hand-off happens. Add it only once you see the shift or measured dropped frames: browsers already promote elements animating `transform` or `opacity`, and every promoted layer costs GPU memory. Put it on the element that animates, never on `*` or large containers. It earns its place on expensive paints, like a large blurred or filtered element; promote it and keep the layer small.

**Symptom table (start here):**
| Problem | Solution |
|---|---|
| Animation stutters | Animate `transform`/`opacity`, not `width`/`height`/`top`/`margin` |
| Shadow animation is choppy | `filter: drop-shadow()` |
| Jank only during navigation or loading | Move the animation to CSS or WAAPI so it runs off the main thread |
| Hand-rolled animation drops frames in React | Write to `ref.current.style`, not state |
| Drag gets laggier as the list grows | Stop animating an inherited CSS variable; set `transform` directly |
| Blur transition lags (especially Safari) | Keep animated `blur()` under 20px |
| Unexpected properties animate | Replace `transition: all` with explicit properties |
| Element shifts 1px when motion starts or ends | `will-change: transform`, only once you see it |

**Diagnose in this order** (most frequent cause first): (1) which properties animate, layout first, then `box-shadow`/`border-radius`; (2) does the jank coincide with the page being busy (navigation, fetching, hydration); (3) is React re-rendering per frame; (4) does it get worse as content grows (inherited variable, or too many nodes animating); (5) is a CSS variable animated at all; (6) any animated `blur()` above 20px; (7) still shifting, now add `will-change`. Confirm with a recording, not by feel: DevTools Performance panel for dropped frames and long tasks, Animations panel to slow motion down, and profile on a real mid-range phone. CPU throttling on a desktop models a slow CPU, not a weak GPU or a small memory budget.

## Verification checklist
- [ ] Render one frame twice and diff it. Identical, or the pipeline is not deterministic.
- [ ] A still at every beat: every line readable at 590px wide (phone: 390px, no overflow).
- [ ] Watch it muted, then listen audio-only. Both must hold up.
- [ ] A design-revise pass asking the review questions from Principles #2.
- [ ] Accessibility pass: contrast, captions, no-flash, reduced-motion cut.
- [ ] Performance pass: every animated property is `transform`/`opacity` or has a named reason; no `transition: all`; animated blur under 20px; no inherited CSS variable in a per-frame loop; `will-change` only where a shift was actually seen.
- [ ] Every fix ships with a **before/after frame pair**. No "trust me" fixes.

## What sucked before (distilled 2026-10-06)
- Generic output comes from thin briefs, not weak models. "Centered text on a gradient, everything fading in, logo at the end" is what you get when you give the model no reference. Anchor to brand + real screenshots or accept the slop.
- A prompt this long gets lost in bookmarks. Save the system as a skill (this file), not a chat artifact.
- Polish-first is the classic failure mode: a beautiful piece that teaches nothing. Shape first, always.
