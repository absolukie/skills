---
name: "skill-test-suite"
description: "Run Luke's paired skill test suite: fixed cases with frozen rubrics, with-skill vs without-skill arms, 3 trials each, deterministic grading, per-check deltas and keep/trim/retire verdicts. Use when a new model lands, when Luke asks whether a skill still helps or hurts, or to add a case for a skill. Suite home: ~/workspace/skill-test-suite (repo: absolukie/skill-test-suite)."
---

# Skill Test Suite

The standing implementation of the method in the primer "New Model, Old Skills" (lukezhang.si/blog/new-model-skill-check/). Suite files live in `~/workspace/skill-test-suite/`: frozen cases in `cases/`, runs in `runs/<run-id>/`, grader per run.

## When to run
- A new LLM model arrives (the main event): re-run every case on the new model, both arms.
- A skill is heavily edited: run its case before and after.
- Luke asks whether a specific skill is good or hurting.

## Protocol (do not improvise)
1. Freeze first: case task wording and rubric (binary checks, each tied to a skill rule or a generic-quality bar) are written in `cases/<name>.md` BEFORE any run. Never edit a rubric mid-run; grader bugs may be fixed, rubric meanings may not.
2. Two arms, identical task wording: WITHOUT (task only, runner must not read any skill files) and WITH (task plus the full SKILL.md, followed exactly; where defaults conflict, the skill wins).
3. 3 trials per arm. Runners should be clean-context agents. KNOWN PILOT LIMITATION: runners inheriting a conversation that has seen the skills bias the WITHOUT arm upward, so deltas read conservative. Say so in the results.
4. Grade deterministically first: static rubric checks on each output file, plus a headless-browser behavior pass for anything clickable. Grade on a quiet machine: behavior checks flaked under heavy parallel load in the pilot and produced false fails.
5. Audit surprising grades against the actual output files before believing them. The pilot found 3 grader bugs this way (a substring check matching the wrong text, a count matching a JS string, a broken flip-back baseline). Fix the grader, never the rubric, then re-grade everything.
6. Report per-check results, never just totals: score per arm per case, the delta, and which specific checks the without arm missed.
7. Verdicts: delta clearly positive beyond noise = KEEP. Delta about zero because the base model already passes those checks = the prose is decoration, trim or retire or re-baseline. Delta negative = the skill is hurting: diagnose the stale compensatory prose before blaming the model. If new-model-without matches old-model-with, re-baseline the case.

## Adding a case
Pick a skill with at least five binary, checkable rules. Write the task so a competent generic build plausibly misses half of them (the ab-toggle pilot case worked because generic builds produce a two-button segmented control, violating the skill's one-switch contract). Freeze it, then run.

## Pilot results on file (2026-10-12, Muse Wonder)
- carousel: without 58%, with 100% (delta plus 4.7 checks). KEEP.
- ab-toggle: without 11%, with 100% (delta plus 8.0). KEEP, the standout.
- before-after-slider: without 50%, with 100% (delta plus 5.0). KEEP.
Full detail: `~/workspace/skill-test-suite/runs/pilot-2026-10-12/results.md`.
