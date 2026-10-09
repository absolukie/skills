---
name: "retro"
description: "End-of-session retrospective. Scan the session for inefficiencies, mistakes, and learnings; convert each into an environment change (AGENTS.md rule, automated check, skill update, or MEMORY.md note) so it can't recur. Every finding must trace to a specific moment. Inspired by Matt Pocock's /retro (aihero.dev/skills-retro)."
---

# Retro Skill

Run at the end of every substantive session (main chat or side chat), before the final reply. Skip for trivial Q&A with no work product. The point: change the environment, not the code. A retro that only summarizes the session is a failed retro.

## The scan

Walk the session chronologically and collect candidates in four buckets. Each candidate must name the specific moment (what happened, where) — generic advice is rejected.

1. **Inefficiencies.** Repeated tool calls that could have been one. Slow file/fact hunts. Rework caused by a wrong first read. Work redone after compaction. Waiting on a handoff that could have been parallelized.
2. **Mistakes.** Anything wrong, broken, or misleading — including wrong claims in replies. For each: what check, rule, or test would have caught it? Prefer automated checks over prose rules.
3. **Learnings.** User corrections, restated preferences, decisions, taste calls. These go to MEMORY.md (user facts) or the relevant skill — never left in the transcript alone.
4. **Steering bloat.** AGENTS.md lines that never fire, duplicate other lines, or state the obvious. Delete or compress them. A good retro can make AGENTS.md shorter.

## The fixes (match the finding to the mechanism)

- Slow to find a file/fact → add a navigation pointer in a file already read every session (AGENTS.md, MEMORY.md, or the skill's SKILL.md).
- Mistake a tool could have caught → automated check: `node --check`, a grep assertion, a regression test, a pre-push verification step. Write the check, don't just describe it.
- Judgement call I got wrong → a rule in AGENTS.md or the relevant skill, phrased as the decision to make next time.
- Expensive or redundant tool sequence → streamline it into one call or a helper script.
- Couldn't reach info I needed → widen access: vendor the file, record the API pattern, save the credential location (never the value).
- User corrected me → MEMORY.md, phrased as their standing preference/decision, dated.

## What NOT to record

- Play-by-play of what was built. The transcript already has it.
- Vague resolutions ("be more careful", "double-check next time").
- Anything already covered by an existing rule — link to it instead of duplicating.
- Speculation about what the user might want. Only what they actually said or did.

## It's working if

- Every entry traces to one specific moment in the session.
- Repeat mistakes become failing checks, not longer prose.
- AGENTS.md stays the same length or shrinks; skills gain "what sucked before" entries instead.
- The next session doesn't repeat the inefficiency.

## Session-end procedure

1. Scan (buckets above), silently.
2. Apply: write the AGENTS.md/MEMORY.md/skill edits directly. Small, dated, specific.
3. In the final reply, mention the retro only if it changed something worth his attention — one line, plain. Never a ceremony.
