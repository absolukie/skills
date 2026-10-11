---
name: "testing"
description: "Luke's testing discipline: e2e tests only on new builds (trial), real UI paths for every QA run, page-error listeners, free-running animation checks, and the e2e patterns that make suites fast and precise."
---

# Testing Skill

## The rule (trial, set 2026-10-09)

New code gets **e2e tests only. No unit tests, ever.** This is a trial while building, not a forever rule, and it applies to new stuff only: **no migrations.** Existing suites stay exactly as they are.

No unit tests means: no test files that import functions and assert on them, no `node -e` logic probes, no test-only harnesses. Drive the real page in a real browser (Playwright) or don't test it.

`node --check` on inline scripts is a syntax check, not a unit test. It stays mandatory (rule 3 below).

Why: two experiments (Pomodoro timer, bill splitter) showed e2e suites catch real bugs, including pure-logic ones, and the discipline that matters is test quality, not test level. E2e-only also pushes good design: untestable-through-UI logic becomes real features (configurable durations, on-screen invariant readouts) instead of test hooks.

Revisit when: a bug slips through that a unit test would clearly have caught faster, or suite runtime becomes painful.

## Hard QA rules (always)

1. **Exercise the real UI path.** Never call handlers directly in tests. A suite that bypasses the file input, the real tap, or the real form submit proves nothing. (Bitten on Aftermath: 67/67 "verified" while the actual photo import was dead.)
2. **Page-error listener on every run.** After any JS change, run a real interaction pass with `pageerror` + console-error listeners attached. Zero errors is the bar.
3. **Syntax-check after every edit.** `node --check` every inline `<script>` after each edit, not just before deploy.
4. **Animations verified free-running.** Screenshot the loop at two wall-clock timestamps and confirm it advances. Frozen `?t=` screenshots are not proof of motion.

## E2e patterns that work

- **Drive the UI, no test hooks.** If a flow can't be driven through the UI (25-minute timer in a test), add a real user-facing feature (URL params for short rounds, a settings panel), not a `window.__test` backdoor.
- **Put invariants on screen, assert on them.** The bill splitter shows "adds up exactly" in the UI; tests assert that string. The product carries its own oracle.
- **Name tests like sentences.** `penny_split_three_ways_adds_up`, not `test_7`. No comments needed when names say it.
- **Timing assertions get slop.** Assert a range ("dropped 1-3s in 2.2s"), never an exact tick count.
- **`inner_text()` lies about case.** It returns CSS-transformed text (`text-transform: uppercase` turns "Focus" into "FOCUS"). Use `text_content()` for raw DOM text in assertions.
- **Mutation-check new suites.** Plant one real bug (drop the penny allocation, break a transition), run the suite, and confirm exactly the right tests fail. A suite that never fails on a real bug is decoration.
- **Fresh context per test** (clean localStorage), except the tests that specifically verify persistence across reload.

## What e2e doesn't replace

- Hand-computing expected values is where the bugs hide: twice the app was right and the test's arithmetic was wrong. Double-check expectations, not just code.
- E2e tells you *what* broke, not *where*. Diagnosing still means probing internals.
- Heavy pure logic (pricing engines, parsers) remains the case most likely to end the trial. Note it if it happens.
