---
name: verify_signin_blockers_before_relaying
description: When a scheduled, background, or delegated run reports a sign-in or account-action blocker, verify it in the live session and finish the work yourself before relaying any blocker to Luke.
skill_improvement:
  managed: true
  status: active
  evidence_handles:
  - d0144a5e-f023-4682-88ec-8122cc655012
  - 9e2296d3-195e-4a07-a9cf-9404dfa00feb
  - 9b8c087a-c483-467b-8524-10d6fa4bf4a3
  - 0f481a51-d57f-4def-a9c0-334e7d5ef148
  - 181868e2-57d2-4aca-9f3a-8ae8804c263a
  - message:bed12b49-73bd-47e3-892f-9fa79d3ba7a7
  - assistant-msg-f6c42df3-78aa-4587-9b35-2fcf463a9bd5
  - assistant-msg-6fda0bc6-5c23-6713-aee6-56c461bf4157
  - assistant-msg-391325f0-6b8f-41e3-a047-fefa015d2dae
  measurement:
    proxy_metric_id: objective_success_rate
    success_criterion: Over the 14-day window, zero sign-in blockers from scheduled or background runs are relayed to Luke without a recorded live-session verification in the same handling, and every blocker that the live check proves false ends with the main agent completing the original task in that same slot rather than leaving it to the run's automatic retry.
    window_days: 14
  needs_review: false
  rationale: 'Three cron workers in this window paused on ElevenLabs sign-in claims (work ids d0144a5e, 9e2296d3, 9b8c087a), matching the two failed IRS call runs 0f481a51 and 181868e2. In conversation the same pattern repeated three times in one day: a scheduled run reported a session-expired or password wall and placed no call, Luke had to restate his standing sign-in permission (message:bed12b49), and each direct live check then found the session active all along, after which the main agent placed the call itself (assistant-msg-f6c42df3, assistant-msg-6fda0bc6). The existing outbound_calling skill already tells the actor placing a call to check the dashboard before assuming a blocker and to sign back in via Google SSO without asking Luke first, but nothing codifies the receiving agent''s duty when a scheduled worker hands it a blocker: the main agent improvised that wake-and-do-it-myself fallback in chat (assistant-msg-391325f0) and it was never banked as a reusable procedure. This skill banks exactly that relay-layer step, scoped to services with standing sign-in permission, without duplicating the calling skill''s call mechanics. Other in-window failure families were checked and not proposed: the primer unstyled-class, flex-row, and oversized-icon failures are already banked as visualizers cross-pattern rules 17 and 18 with the css_audit.py guard, and the stale-tree clobber recurrence is already covered by existing AGENTS.md surgical-push rules.'
  review_after: 2026-10-28T20:36:21.289575+00:00
  reviewed_at: 2026-10-14T20:36:21.289575+00:00
  run_id: sirun_bf96b2d55ee94ffd9c73798d446c2b20
---

# Verify Sign-In Blockers Before Relaying

## Purpose
A background worker's claim that a service is signed out is a report to verify, not a fact to relay. Scheduled workers can land in a stale or separate browser state while Luke's live session is active, and relaying their blocker unchanged wastes a time-critical slot and makes Luke re-state a permission he already granted.

## Workflow
1. When a scheduled, background, or delegated run finishes paused or failed with a sign-in, session-expired, or account-action blocker, do not relay that blocker to Luke yet.
2. Check the service directly in the live managed browser session. Look at the actual signed-in state of the named service, not the worker's screenshot, summary, or saved-credential attempt.
3. If the session is active, treat the blocker as false. Do the original task yourself in the live session, in the same slot the scheduled run was meant to fill, using the skill that governs that task (for ElevenLabs calls, the `outbound_calling` skill). Report the completed outcome, not the worker's blocker.
4. If the session is genuinely signed out, sign in yourself under Luke's standing sign-in permission before asking him for anything: use the service's SSO route with his standing account, select remember-me / trust-this-device where offered, and then do the original task yourself in step 3.
5. Escalate to Luke only when sign-in truly needs an action only he can take, such as a phone tap approval, a one-time code he must supply, or a password or account change. Name that exact action and what you already tried.
6. When you report, state plainly that the scheduled run reported a blocker, what the live check actually found, and what you did. Never present the worker's unverified blocker as the current state.

## Output Contract
The report for a run that claimed a sign-in blocker contains: the service named, the live-session state found on direct check, whether sign-in was needed and completed, the original task's outcome (done, or the one specific user-only action still required), and the run handle of the blocked run.

## Operating Rules
1. This applies to any service with a standing sign-in permission, not only ElevenLabs. ElevenLabs is the proven case: sign in via Google SSO as his standing account; it usually goes straight through without a confirmation prompt.
2. A saved email/password rejection inside a worker does not prove the live session is signed out. Workers have reported both a password prompt and a rejected saved login on days when every direct check found the session signed in all along.
3. Do not retry the failed scheduled run as the fix, and do not wait for its automatic retry. The live-session check and the work happen in the main session, now.
4. Never store or repeat credentials while doing this. Use the live session and its SSO flow only.
5. If the original task is time-critical and pre-authorized (for example a scheduled call attempt with a daily cap), completing it yourself after a false blocker stays inside that authorization. Do not expand it to new destinations, purposes, or extra attempts beyond the pre-authorized sequence.
