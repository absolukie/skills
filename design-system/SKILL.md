---
name: "design-system"
description: "Build a design system before building the UI. Pick a preset, generate the full foundation (colors, tokens, type scale, elevation), style the primitives and blocks, then build something unique on top. Seeded from @shadcn's Oct 9 2026 post on shadcn/ui skills that are 'really good at DESIGN.md'."
---

# Design System Skill

## Purpose
Every UI build starts with a design system, not with screens. Ask for a design system: pick a preset, then generate everything from it — colors, tokens, type scale, elevation, styled primitives and blocks. Start with a solid foundation and build something unique.

Source: https://x.com/shadcn/status/2108574564586332615 (Oct 9, 2026) — "Ask for a design system and it picks a preset, then builds everything: colors, tokens, type scale, elevation, styles the primitives and blocks. Start with a solid foundation and build something unique."

## When to use it
- Starting any new app, site, or visualizer: generate the design system first, screens second.
- Restyling an existing build that looks "default" — the foundation is missing.
- Not for one-off tweaks to a single component; use the component's own pattern instead.

## The pipeline

### 1. Pick a preset
Choose one aesthetic direction and commit to it. Name it in plain words (e.g. "warm paper editorial", "arcade neon", "ink-wash minimal"). The preset is the seed; everything below derives from it. When Luke is picking, show several rendered presets and let him choose — never a single take.

### 2. Build the foundation
Generate these five, in this order, as CSS custom properties plus a short DESIGN.md:

- **Colors**: a tight palette with semantic roles — background, panel, panel-raised, line/border, ink (text), muted, faint, one accent, one danger. Dark-first unless the preset says otherwise. Accent and danger keep consistent semantics everywhere (accent = good/majority/primary action, danger = warning/destructive).
- **Tokens**: spacing scale (4px base), radius scale, border widths, shadow/elevation steps, font stacks (one text face, one mono face for numbers/labels).
- **Type scale**: 4–6 steps with exact px sizes and line-heights, each with a named job (display, title, body, caption, mono-label). Body text never below 16px.
- **Elevation**: 2–4 levels — how a card lifts off the background (border + shadow + fill shift). Every elevated surface uses a level, never ad-hoc shadows.
- **Motion tokens** (if the build animates): one easing curve, 2–3 durations, `prefers-reduced-motion` kill switch. See the motion-design skill for the full system.

### 3. Style the primitives
Buttons, inputs, sliders, toggles, chips, cards, badges — each primitive gets its default, pressed, disabled, and focus states from the foundation tokens only. No hardcoded colors outside the tokens.

### 4. Style the blocks
Composed sections (hero, stat row, list item, empty state, paywall sheet) built from the primitives. Blocks are where the preset's personality shows.

### 5. Build something unique
Only now: the actual screens. The foundation makes them coherent for free.

## Operating rules
1. **Foundation before screens, always.** If a build starts looking generic, the design system step was skipped — go back and do it.
2. **Tokens are the only source of color, spacing, radius, and shadow.** A hex code outside the token block is a bug.
3. **His standing UI rules ride along**: 16px minimum on all inputs (iOS zoom rule), `touch-action:manipulation` on every tap target, bespoke SVG icons never emoji in chrome, modern-memeable naming, math-cute surface over deep machinery.
4. **Mobile-first**: design at 390px, verify no horizontal overflow, then scale up.
5. **Ship the DESIGN.md with the build** — the next session (or agent) restyles from it instead of guessing.
6. **Cite the preset's inspiration** when it borrows from a real system (shadcn/ui, a named aesthetic) — link the source, don't claim it.

## QA checklist
- Every color on screen traces to a token; grep for stray hex codes.
- All four primitive states render (default/pressed/disabled/focus).
- Type scale: each step used at least once, nothing sized ad hoc.
- 390×844 and 1280px: no overflow, tap targets ≥44px, inputs 16px+.
- Zero console errors.
