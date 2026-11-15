---
name: new-task
description: Start a new non-trivial task - create the next task folder from the template and point active_task.md at it. Use when beginning work that touches more than one file, needs review, or involves database, security, data processing, architecture, or deployment.
---

# New task

1. Create the task with the script; do not create the folder or pick the id by hand:

   ```bash
   python3 .agents/planning/scripts/new_task.py "<short title>" [--feature <feature folder path>]
   ```

   It prints the path of the new `task.md` and updates
   `.agents/planning/tasks/active_task.md`.

2. Fill in `Goal`, `Scope`, and `Acceptance Criteria` in that `task.md`. Every
   criterion ends with `verify:` and a command, a test name, or one manual step.

3. For `Standard` and `Deep` work in a project with a test runner, write the
   failing test from the criteria before the implementation.

Leave the `## QA` section as it is; `/qa-review` fills it when the task reaches
`In Review`.
