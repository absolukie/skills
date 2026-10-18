---
name: "maintain-verification-skill"
description: "Keep one project's verification system truthful as the app changes: detect drift between the app and its feature map, update the map and harness, re-run the full verification against the live URL, and report only real drift or failures. Modeled on poteto's /maintain-verification-skill from pstack (hers runs as a daily automation). Trigger on: 'maintain verification for X', 'check X for drift', 're-verify X', or from a scheduled run for a project that has a verify skill."
---

# Maintain Verification Skill

Apps change; feature maps quietly go stale; checks keep passing against a product that no longer exists. This skill is the upkeep loop for the verification system built by the create-verification-skill: find the drift, refresh the map and harness, re-prove the app, and stay silent unless something actually needs Luke.

## Inputs
The project's verify skill (`~/workspace/skills/verify-<project>/SKILL.md`), its `verify/FEATURE_MAP.md`, its `verify/verify.py`, and its last `verify/REPORT.md` with its date. If a project has no verification system yet, say so and offer the create skill instead of improvising one here.

## Procedure

### 1. Detect change
Establish what changed since the last report:
- The project's repo history (commits and changed files since the report date).
- A live crawl of the project's routes and pages, compared against the map's feature list.
- Any notes in the project's workspace or the daily logs describing shipped changes.

Classify every difference: feature added, feature changed, feature possibly removed, or no user-facing change.

### 2. Update the map
- Added features: exercise them through the real UI first (the create skill's rule: observed, not inferred), then write map entries in the same format.
- Changed features: update the entry's steps and expectations, with a dated correction note inside the entry.
- Possibly removed features: never delete on suspicion. Mark the entry `POSSIBLY REMOVED` with the date and evidence, and surface it to Luke in the report. Removal becomes final only when he confirms or the evidence is unambiguous (the page itself is gone).
- No user-facing change: leave the map untouched.

### 3. Update the harness
Add or adjust checks so every current map entry has exactly one matching check, still driving the real UI, still failing on any `pageerror`, still saving the promised screenshots. Syntax-check before running. Remove checks only for features whose removal is confirmed, and say so in the run note.

### 4. Re-run everything, live
Run the full harness against the **live URL** (not only a local server), after any deploy lag has settled. Regenerate `verify/REPORT.md`: date, target, per-feature results, and a drift section listing (a) in the app but was not in the map, (b) in the map but failing, (c) marked possibly removed. Save a short run note in the project's verify folder either way, so the next run knows where it stands.

### 5. Report, flag loud or stay silent
- All green and no drift: no message to Luke. The refreshed report is the record.
- Failures or drift: one short report, most urgent first: what broke or changed, the screenshot or report link, and what would fix it. Fixes are separate work; this skill never edits the app.
- A harness that can no longer run at all (site down, harness broken by a redesign) is always reported, never left as a silent gap.

## Cadence
Designed to run as a daily automation per project (that is how poteto runs hers), but scheduling is Luke's call: propose the cron, do not install it unasked. Manual runs on request are always in scope.

## Standing cautions
- Verification is an approximation and maps decay between runs; the drift section exists to say exactly how much.
- Never weaken a check to restore green without a dated note in the map entry explaining the intentional behavior change behind it.
- Real UI paths only, always. A maintenance run that starts calling handlers directly has stopped verifying the product.
