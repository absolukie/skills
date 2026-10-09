---
name: "motion-design"
description: "Motion design system for explainer films and animated web pieces: story-arc timing bands, a motion language where movement carries meaning, scene-spec format, visual-system tokens, copy/sound/accessibility rules, and a verification checklist. Distilled from the @0xMovez motion-studio post (prompt by @0xCarnagee, principles from Meaghan Choi, ex-Meta/Anthropic designer). Use when building any explainer video, animated hero, or scroll-driven animated page."
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

## Verification checklist
- [ ] Render one frame twice and diff it. Identical, or the pipeline is not deterministic.
- [ ] A still at every beat: every line readable at 590px wide (phone: 390px, no overflow).
- [ ] Watch it muted, then listen audio-only. Both must hold up.
- [ ] A design-revise pass asking the review questions from Principles #2.
- [ ] Accessibility pass: contrast, captions, no-flash, reduced-motion cut.
- [ ] Every fix ships with a **before/after frame pair**. No "trust me" fixes.

## What sucked before (distilled 2026-10-06)
- Generic output comes from thin briefs, not weak models. "Centered text on a gradient, everything fading in, logo at the end" is what you get when you give the model no reference. Anchor to brand + real screenshots or accept the slop.
- A prompt this long gets lost in bookmarks. Save the system as a skill (this file), not a chat artifact.
- Polish-first is the classic failure mode: a beautiful piece that teaches nothing. Shape first, always.
