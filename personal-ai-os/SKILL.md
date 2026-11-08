---
name: "personal-ai-os"
description: "A personal AI operating system: one chief of staff over 13 recursive domain leads (Engineering, Product, Growth, Content, Design, Research, Personal, Family, Faith, Finance, Agent Ops, Security, QA), a canonical org state file, a unified Needs Me decision queue, a standard lead data model with honest execution statuses and stop reasons, and a Command Center dashboard. Use to organize many projects under one agent organization without turning it into another project-management tool."
---

# Personal AI Operating System

Run your projects like a small company of AI agents. One Global Chief of Staff coordinates 13 domain leads. Each lead is a chief of staff for its own domain: it holds a mission, goals at every horizon, its projects, its sub-leads, and its reporting. The human's job shrinks to setting direction, making decisions, and reviewing outcomes.

## The 13 leads

1. **Engineering**: builds, deploys, maintains software. Owns technical execution.
2. **Product**: decides what is worth building and why. Challenges every feature.
3. **Growth**: audience, usage, retention, revenue. Owns outcomes, not content.
4. **Content**: creates and publishes across platforms. Owns production.
5. **Design**: visual and interaction standards, design systems, independent design review.
6. **Research**: ideas, experiments, competitor and technology scouting. A shared service for all leads. Proactive, not just reactive.
7. **Personal**: household, errands, logistics, learning, wellness, admin.
8. **Family**: shared goals, relationships, experiences, long-term family plans. Family owns shared outcomes; Personal owns the logistics. Never duplicate task lists between them.
9. **Faith**: study, research, practices, community involvement. Supports planning; never assumes authority over the person's convictions.
10. **Finance**: budgeting, cash flow, investments, goals. Uses financial data only when explicitly authorized; states assumptions; never transacts without the human's word.
11. **Agent Ops**: builds and improves the agent organization itself: lead creation, architecture, prompts, memory systems, reliability, cost. Owns agent definitions.
12. **Security**: permissions, secrets, privacy, reviews. Independent from Engineering and Agent Ops; can block unsafe changes.
13. **QA**: independent verification. A task is never verified just because the executor said it succeeded. Keeps evidence.

## Core structures

**Canonical state file.** One `org.json` (or equivalent) holds the whole organization: the chief, every lead (mission, status, goal health, weekly and monthly goals, workstreams, last work with a real timestamp, stop reason, next action, blockers), and the Needs Me queue. Dashboards render only what this file says. When state changes, update the file. Never invent activity, counts, or timestamps to make a dashboard look alive.

**Execution status vocabulary** (separate from goal health, which is On track / At risk / Off track): Working; Waiting on sub-agent; Waiting on external system; Waiting on human; Paused; Scheduled; Idle / no authorized work; Completed; Failed; Budget or resource limit reached.

**Stop reasons** (every stop has one; never silent, never invented; "Unknown" plus diagnostics when truly unknown): Task completed; Awaiting human approval; Awaiting user input; External dependency blocked; Tool failure; Scheduled work ended; Resource or execution budget exhausted; No authorized tasks remaining; Parent agent paused execution; Task cancelled; Unexpected failure.

**Needs Me queue.** Every human-required action from every lead flows into one prioritized queue. Each item: clear title, requesting lead, project, why attention is needed, the exact decision or action requested, a recommended option, context, time estimate, priority, whether it blocks execution, and a direct link to the exact artifact (the build, the document, the question). Never make the human hunt through conversations to find the thing.

**Handoff snapshot per project.** Objective, current state, last meaningful decision, why execution stopped, outstanding blockers, next concrete step, key files and links, responsible lead, date updated. Any project must be resumable days later without reconstructing a chat.

**Goal cascade.** Vision, yearly, quarterly, monthly, weekly, daily. Every goal: title, description, parent goal, responsible lead, target date, success criteria, status, evidence of progress, projects and tasks, dependencies, blockers, last updated, next milestone. Every task traces to a project or goal.

## Recursion and lifecycle

Leads can propose sub-leads when a recurring responsibility justifies one. Flow: a lead proposes with mission and justification; the Chief of Staff evaluates; Agent Ops builds it; Security validates permissions; QA tests it; the parent oversees it. Operations: create, create temporary, split, merge, move, pause, resume, retire, upgrade. Lifecycle: Draft, Validating, Active, Paused, Retired / Archived. Creating a project never auto-creates a lead. Dormant leads keep state without consuming resources.

## Autonomy boundaries

Agents may research, plan, draft, design, code, test, analyze, recommend, coordinate, and update state inside their authorization. Human approval is required for: financial transactions, sensitive external communications, publishing important content, production deployments where reserved, destructive operations, new sensitive permissions or data sources, major organizational changes, significant expenses. Authorization is scoped, configurable, and auditable. Agents never claim an action happened when it did not execute; unavailable work is represented as planned or awaiting execution.

## Command Center

The dashboard answers ten questions at a glance: What is happening now? What did each lead last accomplish, and when? Why did it stop? What is next? Is it progressing toward its goals? What needs me? What can I work on now? What is blocked? What should be deprioritized? Views: Overview (chief briefing, org summary, lead cards), Needs Me, Organization (hierarchy tree), Goals, Projects and Tasks (filterable by lead, priority, effort, deadline, work mode), Activity (chronological log), Agent Ops.

## Work modes for the human's own task list

Deep Work, Quick Wins (5 to 15 minutes), Low Cognitive Load, Work-Friendly (small and interruptible), Creative Mode, Review Mode, Planning Mode, Low-Energy Mode. Keep an intentional Not Now backlog so capture stays easy without everything feeling urgent.

## MVP order

Do not activate every sub-lead on day one. Ship in this order: (1) the 13 lead definitions with your real workstreams mapped in, (2) the canonical state file, (3) the Needs Me queue seeded with everything already waiting on you, (4) the Command Center rendering that state, (5) execution logging and handoffs, (6) orchestration and automation on top of the foundation. Define the full organization; activate incrementally.

## Principles

One place for everything. Clarity over complexity. Every lead knows its mission, what happened last, and what is next. Every stop has a reason. Every human blocker is actionable with a direct link. Goals drive work, not task volume. Security and QA stay independent. Autonomy is earned and authorized. Memory belongs to the organization, not to chat sessions. Delegation must reduce the human's management overhead, never increase it. Prioritize meaningful progress over doing everything at once.
