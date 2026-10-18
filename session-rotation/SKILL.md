---
name: "session_rotation"
description: "Stop context-bloat token burn: detect when a long-lived session is resending too much context and rotate it at a phase boundary with a tight handoff brief. Trigger on 'rotate the session', heavy-context mega-projects, or usage-breakdown bottleneck findings."
---

# Session Rotation

## Purpose
Long-lived root sessions resend their full context on every turn, so input tokens dominate cost (observed case: 95.3M tokens on one mega-project, 98.2% of it input from context resend). This skill rotates the session at phase boundaries: the old session writes a handoff brief, a fresh session continues from the brief alone.

## Workflow
1. **Detect.** Check context fill with `muse.session_status`.
   - Over ~80% full: rotate at the next safe stopping point.
   - 60-80%: plan the rotation at the upcoming phase boundary; do not start a new phase in this session.
   - Under 60%: no action.
2. **Phase-gate.** Never rotate mid-phase. Finish the current unit of work (or reach a clean checkpoint), then rotate before starting the next phase.
3. **Write the handoff brief.** Save it where the next session will find it: the project's workspace (e.g. `HANDOFF.md`) or the queue file. Keep it under ~2KB: pointers, not transcripts. See Output Contract.
4. **Rotate.** Continue in a genuinely fresh session: a new side chat, or a handoff the user opens fresh. The new session reads the brief and the referenced files, nothing else.
5. **Verify.** The new session restates the goal and the next step in one line before doing work. If it cannot, the brief was too thin: thicken it and retry.

## Output Contract
The handoff brief contains, in this order:
- Goal: one line, the durable outcome.
- Done: completed phases with links (commits, URLs, file paths).
- Decisions: choices made and why, one line each.
- State: the exact current position (e.g. "stroke 12 of 58 extracted, candidates in sites/bihua/strokes/").
- Next: the single next phase and its definition of done.
- Traps: things tried that failed, so they are not retried.

## Operating Rules
1. Briefs carry pointers (paths, commit SHAs, URLs), never pasted file contents or logs.
2. One phase per session is the ideal; two at most before rotating.
3. Spawning a subagent does not shed bloat: children inherit the parent's context. Rotation means a fresh root session, not a subagent.
4. If the user is mid-conversation in this chat, say you are rotating and where the brief lives; do not silently switch context on them.
5. Record the rotation in the daily log so the usage breakdown can attribute tokens per phase.
6. Quick Q&A sessions never need rotation; this skill is for multi-phase build/debug work.
7. Prevention beats rotation: batch work (skill A/B component trials, batch builds, other repeatable units) starts in a fresh short-lived root per batch instead of inside a long-lived root, so the bloat never accumulates. The coordinating root gets the summary plus file paths only. (Luke approved 2026-10-12; rule lives in the autonomous-deep-work skill, section 2.)
