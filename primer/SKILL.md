---
name: "primer"
description: "Build a 'primer': an interactive single-page brief that takes someone from zero to conversant on a topic, grounded in leading voices and the latest research. Trigger on: 'primer', 'add a primer', 'build me a primer', or any request for a topic overview with predictions and expert views."
---

# Primer

## Purpose
Generate a "primer" for any topic: one self-contained HTML page that brings the reader from zero to conversant. A primer is broader and more narrative than a mastery sheet: it covers how something works, where it came from, who the leading voices are, and where it's going. It never presents predictions as fact and never writes from training-data memory alone.

## Rule zero: research first, always
**Every primer begins with fresh research. No exceptions.** Before writing a single section:
1. Run `browser.deep_research` (or targeted `browser.search` passes for narrow topics) on the topic's latest developments and leading voices. The mission must ask for: current state of the art, landmark recent papers/releases with dates, and named expert views with attribution.
2. Write from the research report, not from model memory. If the research is thin on a sub-point, say so in the primer or cut the sub-point. Never fill gaps with plausible-sounding memory.
3. Record the research date visibly on the page ("Researched October 2026"). Predictions and expert views go stale; the date is what keeps the primer honest.

## The 8-section anatomy
1. **The brief.** One paragraph: what this is, why it matters right now. Ends with the single sentence the reader should remember.
2. **How it works.** The 4-6 mechanisms that drive the topic, as tappable cards or a click-per-step stepper. Each mechanism: plain-language explanation, one concrete example, and what changed recently. This is the engine room; budget real design time here.
3. **Timeline.** Landmark moments as an interactive timeline (horizontal scroll or stepper). Each entry: date, what happened, why it mattered. Landmarks only, no filler.
4. **Key voices.** The 4-8 leading researchers/practitioners, each with their attributed view in one or two sentences and a link to the primary source (paper, essay, interview). Include at least one genuine disagreement between voices; consensus-only primers mislead.
5. **Where leaders think this goes (his 2026-10-11 call, revised same day).** He liked the contested/consensus framing but wants it clear who is on which side — group predictions as explicit named camps, never abstract badges:
   - **Where they agree** — consensus items, each naming the leaders who share the view (e.g. "Amodei, Hassabis, and Altman all point to..."). No anonymous consensus; the names ARE the badge.
   - **Where they split** — contested items shown as named camps: Side A (names + their position, venue/date) vs Side B (names + their position, venue/date). Every camp lists its people; no "some say" without names.
   - Single-leader long-shot visions go under the split group as one-person camps, clearly marked as one person's bet rather than a camp.
   Keep the section title "Where leaders think this goes". Date-stamp the section and attribute every item (name, venue, date). Never present a prediction as your own conclusion. No new voices or facts beyond what the research supports.
6. **Takeaways (his 2026-10-10 call).** A concise conclusive summary plus takeaways, its own section placed before Keep exploring (page order: Takeaways → Keep exploring → Sources). One short paragraph that states the conclusion in plain language, then 4 to 6 bullets with bold lead-ins carrying the memorable or actionable points. No new facts here, only the payoff of what the primer already established.
7. **Keep exploring.** Related primers with link-out icons.
8. **Sources.** Every primary source used, each linked. Every factual claim in sections 2-5 must trace to a source here.

## Sourcing rules
- Primary sources only for factual claims: the paper itself, the official docs, the person's own essay/interview, not a blog summarizing them. Link the exact page, never a homepage.
- Attribute every prediction and expert view inline: name, venue, date.
- Show disagreements between voices explicitly ("Amodei expects X by 2027; LeCun disagrees, arguing Y").
- If two sources conflict, say so instead of picking the tidier one.

## Build workflow
1. Pick the slug, working title, and exactly two tags from the taxonomy (ai, llms, engineering, math, infrastructure, design, business, science, tools, language, culture). Never tag "interactive".
2. Start from the primer reference implementation once one exists; until then, start from `~/workspace/blog-drafts/taylor-mastery/index.html` (canonical visual system) and adapt the sections.
3. Research first (rule zero), then write section 2, then 4 and 5 together (voices feed predictions), then the rest.
4. Keep the visual system identical across primers: paper `#f6f1e3` background, `#b3352b` accent, `.viz` cards, `.fcard` tappable cards, `.xlinks` keep-exploring grid, `.btn`/`.btn.ghost` buttons, verdict lede, meta tags, kicker close.

## Operating rules
- Re-read `~/workspace/skills/visualizers/SKILL.md` before building (slider spec, step-through rules: click-per-step, never autoplay; hide terminal stepper buttons with `display:none`, never disable).
- **Concrete worked examples** (his 2026-10-10 call). Every primer includes at least one fully worked concrete example: the actual prompt, the actual checks or numbers run against it, and the outcome. Abstract mechanism descriptions alone do not land; the reader should see the machinery operating on a specific case. Place it in "How it works" or directly after. Label it honestly when illustrative rather than measured.
- **Scroller/stepper hints state the gesture only** (his 2026-10-11 call). Hint copy says what the thumb does ("Swipe sideways.", "One tap per step, or use the arrow keys.") and never editorializes about autoplay or pacing: "No autoplay, your thumb sets the pace" is unnecessary. If the hint would merely repeat the section intro, drop the hint line instead of repeating it.
- **Body copy never narrates its own format** (his 2026-10-11 call). Cut sentences like "Each view is one or two sentences with the primary source linked" — the reader can see the format. Say what the section is about, not what its items look like. (Interaction hints like "Tap to open" stay; those are affordances, not format narration.)
- **Illustrations come from Codex, never the Muse media pipeline** (his 2026-10-11 call: Muse images are not great). Generate via the Codex CLI built-in `image_gen` on his ChatGPT subscription: run `~/workspace/.codex-0160/package/vendor/x86_64-unknown-linux-musl/bin/codex exec "<image prompt>" < /dev/null` from a git-initialized dir, one call per asset. Codex saves to `$CODEX_HOME/generated_images/...` and reports the path; copy the chosen PNG into the workspace and optimize (max ~1200px wide, under ~200KB) before vendoring under `blog/<slug>/images/`. Never use the `OPENAI_API_KEY` CLI fallback: that key is websites-only.
- 1-3 illustrations per primer at natural breakpoints; each must teach, not decorate. Conceptual flat style matching the visual system (paper `#f6f1e3`, accent `#b3352b`); no photorealistic people, no real persons' likenesses. Prefer looping `<video autoplay muted loop playsinline>` over GIF when motion teaches better. Descriptive alt text, mobile-safe at 390px, zero third-party requests.
- **Cross-article buttons carry a link-out icon.** Small bespoke external-link SVG (inline, `currentColor`, 14px, never emoji).
- Simple language, his voice, dry humor, no em dashes or en dashes anywhere. Math in words in chat, KaTeX only inside the page. Inputs 16px minimum. `touch-action: manipulation` on all taps. Bespoke SVG icons, never emoji in UI chrome. Zero third-party requests (KaTeX vendored, relative paths).
- KaTeX: explicit single/double-dollar delimiters, `throwOnError: false`, `ignoredClasses: ["nokatex"]`. Re-run `renderMathInElement` on dynamic nodes. Wide formulas scroll internally; page never overflows.
- Canvas plots: devicePixelRatio-aware, redraw on resize. `"use strict"` in the IIFE. No top-level `var` named after a `window` API.

## QA checklist
- HTML tag balance check (scripted), zero em/en dash assertion (scripted), `node --check` on extracted JS.
- Every source link returns HTTP 200 (scripted check).
- Playwright at 390x844: every interactive end to end (cards, stepper forward AND back with 300ms+ waits, sliders, toggles both ways), zero `pageerror`s, `document.documentElement.scrollWidth <= 390`, screenshots of hero + each interactive reviewed at full size.

## Deploy
- Push `sites/<slug>/` to `absolukie/lukezhang-si` via **surgical overlay only**: fetch current head, one blob per file, new tree on `base_tree` = head tree, commit, then re-read the ref and PATCH only if it still points at the head you built on (compare-and-swap; abort if it moved). Never a full-tree push.
- worker.js SITES entry: re-fetch worker.js fresh from the GitHub API into a NEW temp file every time (never edit a stale /tmp copy), confirm existing SITES entries are present, add the new slug, push with the same compare-and-swap guard.
- Verify live: served URL returns HTTP 200 and the response HTML contains the page title and key section markers. Only then report the link.
