---
name: qa-review
description: Review the active task before it can move to Done - run the project checks, verify each acceptance criterion, record the QA section and the follow-up review decision, and validate. Use when the implementation of a non-trivial task is complete.
---

# QA review

1. Set the task status to `In Review` in its `task.md` and in
   `.agents/planning/tasks/active_task.md`.
2. Run `python3 .agents/planning/scripts/check.py`. Fix failures first; a task
   with failing checks goes back to `In Progress`.
3. Pick the review depth from `02-task-tracking.md` (`Light`, `Standard`, `Deep`).
4. Delegate to the `qa` subagent. The brief carries: the task goal, the
   acceptance criteria with their `verify:` steps, the changed files
   (`git diff --name-only`), and the depth. Override the model to opus only for
   `Deep`. If `qa` answers `Escalate to Deep`, re-run it on opus.
5. Record the result in the `## QA`, `## Follow-Up Review Decision`, and
   `## Trigger Matrix` sections of `task.md`, following
   `.agents/protocol/13-review-governance.md`.
6. If a non-negotiable trigger is `Yes`, create the follow-up review task with
   `/new-task` before closing.
7. Set the task to `Done` only when QA recommends it, then run
   `python3 .agents/planning/scripts/check.py` again; it validates the task docs.
