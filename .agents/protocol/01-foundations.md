## Project Purpose

This repository serves as a reusable base for agent-assisted software work across different project types.

Priorities:

- Correctness.
- Maintainability.
- Clarity.
- Reusability.
- Security.
- Low token usage.

---

## Project Setup Gate

Before any other work, check whether `.agents/context/project_profile.md` exists.

If it does not, the mandatory first task is project setup: read
`.agents/protocol/11-project-setup.md`, ask the user for the project objective
and the tools to be used, and configure the subagents the project needs. Do not
start other non-trivial work until the profile exists.

Skip the gate only when the user states that the work is maintenance of this
template itself rather than a project built from it.

---

## Core Instruction

Do not inspect the whole repository by default.

Use the smallest context required for the task.

Read these first:

1. `.agents/planning/tasks/active_task.md`
2. `.agents/context/current_state.md`
3. The active task's `task.md`

Then read these if present (they are created on demand, not by default):

- `.agents/context/project_profile.md` (objective, tools, installed agents)
- `.agents/context/context_manifest.md`
- `.agents/context/source_map.md`
- `.agents/context/known_decisions.md`

For database tasks, also read `.agents/context/database_map.md` if present.

Then read only files related to the active task.

If a required task or feature file does not exist, create it using the repository conventions.

---

## On-Demand Modules

Not loaded by default (neither imported by `CLAUDE.md` nor inlined in
`AGENTS.md`) to keep the always-on protocol small. Read the file only when the
task matches:

- `.agents/protocol/07-database.md` — any task that changes schema, migrations, persistence, relationships, or important queries.
- `.agents/protocol/08-feature-tracking.md` — when creating or updating a feature folder under `.agents/planning/features/`.
- `.agents/protocol/12-data-ml-rules.md` — Excel/CSV processing, data transformations, or machine-learning work.
- `.agents/protocol/13-review-governance.md` — when performing QA or moving a task to `In Review`.
- `.agents/planning/docs/lessons/{area}.md` — before working in an area, if the file exists (past mistakes and the rule that prevents each).
- `.agents/protocol/11-project-setup.md` — when `.agents/context/project_profile.md` does not exist, or when installing or removing subagents.

---

## Create-On-Demand Rule

Do not create documentation files just because they exist in the convention.

Create a file only when:

- The current task needs it.
- The information will be reused.
- The file helps reduce future context.
- The feature is becoming hard to track.

If a required file does not exist, create it using the standard template.

---

