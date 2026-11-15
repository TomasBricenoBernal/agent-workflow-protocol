## Task Tracking

Features are larger capabilities: `.agents/planning/features/{id}-{feature-name}/`.

Tasks are units of work that can be implemented, reviewed, and closed
independently: `.agents/planning/tasks/YYYY/MM/{task-id}-{task-name}/`.

`.agents/planning/tasks/active_task.md` is the single pointer to the current task.

Create a task folder when the work:

- Affects more than one file or belongs to a feature.
- Requires QA or review, or may need handoff across sessions.
- Involves database, security, data processing, architecture, or deployment.

Do not create a task folder for trivial one-line or single-file changes unless explicitly requested.

Task files:

- `task.md` — required. One file holds the goal, scope, acceptance criteria, and the QA record. Copy `.agents/planning/tasks/_templates/task.md`.
- `plan.md`, `handoff.md`, `notes.md` — optional; create only when needed.

Every acceptance criterion ends with `verify:` and how it is checked: a command,
a test name, or one concrete manual step. A criterion nobody can check is not a
criterion; rewrite it or drop it.

Do not keep a hand-written list of changed files. Use `git status` and
`git diff --name-only`; they are the record.

Review task rule:

- QA may create a dedicated review task when a follow-up needs a separate specialist pass (`Security`, `Database`, or cross-task QA).
- The review task must record why it was created and which agents must participate.

---

## Statuses and Review Flow

Use only: `Planned`, `In Progress`, `Blocked`, `In Review`, `Done`.

- `Planned`: exists, not started or intentionally postponed.
- `In Progress`: started and expected to continue.
- `Blocked`: started but stopped by a dependency, decision, or external issue.
- `In Review`: implementation complete; QA, and Security if applicable, pending.
- `Done`: implementation, required review, and close-out are complete.

Review flow:

- Implementation completion moves the task to `In Review`, never directly to `Done`.
- QA review is required before `Done`. Read `.agents/protocol/13-review-governance.md` when performing it.
- A non-trivial task cannot move to `Done` while the `## QA` section or the follow-up review decision in `task.md` is incomplete.
- If review finds issues, move the task back to `In Progress` or `Blocked`.

QA review depth:

- `Light`: small local changes with low regression risk.
- `Standard`: normal functional changes, validations, services, operator-facing behavior.
- `Deep`: database, migrations, security-sensitive changes, Excel/CSV, calculations, machine learning, public APIs, or high-regression-risk work.

The lead agent picks the depth from these criteria before delegating to `qa`.
`Light` and `Standard` run on the `qa` default model; for `Deep`, delegate with
the model overridden to opus. If `qa` answers `Escalate to Deep`, re-run it that way.

Security review is required only when the task touches:

- Authentication, authorization, roles, or permissions.
- File upload or file handling.
- Secrets, credentials, or sensitive configuration.
- Public endpoints or externally exposed integrations.
- Sensitive data in fields, logs, errors, or traces.
- Validation or database changes that affect trust boundaries or sensitive fields.

---

## Task Completion Rule

A non-trivial task is not complete until:

- The `## QA` section of `task.md` records checks, findings, tests run or not run, and the follow-up review decision.
- Required Security review is completed when security triggers apply.
- `handoff.md` is written if the task is paused, handed off, or blocked.
- The related feature's `changes_current.md` is updated if behavior changed.
- `.agents/context/current_state.md` is updated only if what is true about the project changed. It is a snapshot: replace the affected lines, do not append history.
- `python .agents/planning/scripts/check.py` passes. It runs the project's own checks (`.agents/config/checks.json`) and validates the docs of every `Done` task, and prints only failures.
- `.agents/planning/tasks/active_task.md` shows the final status or the next task.

---
