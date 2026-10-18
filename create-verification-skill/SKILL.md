---
name: "create-verification-skill"
description: "Build a verification system for one of Luke's projects: a feature map written from the user's point of view, a runnable harness that drives the real UI and produces screenshot proof, and a per-project verify skill so any future session can re-run it cold. Modeled on poteto's /create-verification-skill from pstack, adapted to this workspace's stack and standing QA rules. Trigger on: 'create a verification skill for X', 'give X a feature map', 'set up verification for X'."
---

# Create Verification Skill

Verification is the entry point to the agentic loop: an agent that can run the product like a real user and prove its work does not have to be believed, it can be checked. This skill builds that ability for one project.

**Standing policy (Luke, 2026-10-12): verification is built at creation time for every NEW project, primer, and blog visualizer. Existing projects are not migrated or backfilled unless he asks.** The primer skill, the blog decision doc skill, and cross-pattern rule 15 in the visualizers skill all route new builds here. First pilot: Bihua, 2026-10-12 (19 of 20 checks green; the one failure was a local mirror gap, not the app).

It produces three artifacts:

1. `<project>/verify/FEATURE_MAP.md` — every user-facing feature, from the user's point of view.
2. `<project>/verify/verify.py` — a Playwright harness that exercises the map through the real UI and emits proof.
3. `~/workspace/skills/verify-<project>/SKILL.md` — a small skill pointing at the map and harness so future sessions and the maintain skill can find and run them.

## Procedure

### 1. Recon
Read the project's code, routes, and README. Establish: how it runs locally, its live URL, its entry points and pages, and every interactive element (buttons, inputs, gestures, game actions, forms). Note anything account-gated or stateful. Do not write the map from code alone; code tells you intent, not behavior.

### 2. Drive it like a user
Load the app (local server first, then the live URL) in Playwright at 390x844, desktop second. Click everything clickable, submit every form, play the actual flow. Attach a `pageerror` listener from the start. Screenshot as you explore. **Real UI paths only, never call handlers or functions directly**: a green suite that bypasses the UI proves nothing (the 2026-10-09 Aftermath lesson, where 67 of 67 checks passed while photo import was dead).

### 3. Write the feature map
One entry per feature, in the user's language, never the code's:

```
## <Feature name>
As a <user>, I <action> and <visible result>.
Steps: 1. ... 2. ...
Expect: <what must be visibly true, including counts, labels, and states>
Proof: shots/<feature-slug>.png
Edges: <empty state, error state, double-tap, refresh, back button, as applicable>
```

Rules:
- If you did not personally exercise it, mark the entry `UNVERIFIED` and say why. Never write an expectation you only inferred from code as if it were observed.
- Cover the unhappy paths a user will actually hit: empty states, invalid input, rapid repeated taps, reload mid-flow.
- The map is the contract. Later runs compare the app against the map, not against memory.

### 4. Build the harness
`verify.py` uses Python Playwright (the house stack). Requirements:
- One check per map entry, named after the feature slug, each driving the real UI (locators, taps, fills, real file choosers for uploads).
- A `pageerror` listener that fails the run on any uncaught error.
- Screenshots saved to `verify/shots/` with the exact filenames the map promises.
- A `verify/REPORT.md` written at the end of every run: date, target (local or live URL), per-feature pass/fail, and the failure detail for any fail. No summary-only reports; the per-item list is the deliverable.
- Viewport 390x844 by default; add a desktop pass when the project is desktop-first.
- Syntax-check before running (`python3 -m py_compile`), and after any JS edit inside it, extract and `node --check`.

### 5. Run it and reconcile
Run the harness. For every failure, decide which side is wrong:
- App behaves contrary to its evident intent: the failure stands; report it as a bug with the screenshot.
- App intentionally behaves differently than the map says: fix the map, and note the correction and its date inside the map entry.
- Intent is genuinely ambiguous: ask Luke. Never weaken or delete a check just to make the run green; a check removed without a map note is a silent coverage loss.

Then run the harness once more against the **live URL**. A local-only pass is not done: "live" means the served page at the real address behaves, verified after deploy lag settles.

### 6. Register the per-project skill
Create `~/workspace/skills/verify-<project>/SKILL.md` with frontmatter naming the project, and a body that states: the live URL, how to run the harness, where the map and last report live, and any project-specific quirks (accounts, seeded data, timing). Keep it short; it is a pointer, not a copy of the map.

### 7. Deliver
Report to Luke: features mapped, checks passing, proof screenshots (attach or link the report), anything left UNVERIFIED and why, and any real bugs found, most important first. No em dashes in the report.

## Standing cautions
- Verification is an approximation. A green run means the mapped flows worked once, under test conditions; say so when it matters, and never present a screenshot of a frozen state as proof of motion or timing behavior.
- Do not fold app fixes into this skill's run. Verification finds and proves; fixing is separate work Luke can green-light.
- Respect the anonymization and privacy rules for anything public-facing the harness touches.
