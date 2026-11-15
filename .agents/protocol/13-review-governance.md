## Review Governance

These rules govern the QA-led review workflow and are enforced by
`.agents/planning/scripts/validate_task_docs.py` against `.agents/config/review_rules.json`.
Read this module when performing QA or moving a task to `In Review`. Agent labels here (`Security`, `Database`) are the
values written in the QA `review_agents` field.

The QA record, follow-up decision, and trigger matrix live in the task's
`task.md` (`## QA`, `## Follow-Up Review Decision`, `## Trigger Matrix`).

QA scheduling rule:

- After each non-trivial task review, QA must explicitly decide whether an additional review task is needed.
- If needed, QA schedules a new task and names the required agents such as `Security`, `Database`, or additional `QA`.
- If not needed, QA must record why no follow-up review was scheduled.
- If the follow-up decision fields are incomplete, the task stays `In Review`.
- If a non-negotiable trigger is present, QA cannot close the task without scheduling the required follow-up review.
- If `other` is marked `Yes`, QA cannot close the task without a valid, specific rationale.

Schedule triggers:

- Schedule `Security` review for auth, permissions, secrets, uploads, public exposure, sensitive data, or trust boundaries.
- Schedule `Database` review for schema, migrations, constraints, integrity-sensitive queries, or persisted sensitive fields.
- Schedule combined review tasks when the risk crosses multiple areas and a single task-level review is too narrow.

Non-negotiable triggers:

- `Security` follow-up review is mandatory for login, authentication, authorization, roles, permissions, file upload, secret handling, new public endpoints, external integrations, or persisted sensitive data.
- `Database` follow-up review is mandatory for schema changes, migrations, constraints, persisted sensitive fields, or integrity-sensitive query changes.

Proportionality rule:

- `Light`: local, bounded risk that does not change a core trust boundary.
- `Standard`: normal functional cross-file changes needing extra verification but not the deepest risk class.
- `Deep`: authentication, permissions, trust boundaries, migrations, sensitive data handling, public APIs, or other high-regression surfaces.

`other` rationale rule:

- If `other` is `Yes`, `other_valid_reason` must state: what changed | what concrete risk exists | why the listed triggers do not already cover it | why extra review is needed or why it is still safe not to schedule one.
- Generic reasons such as `por si acaso`, `por seguridad`, or `mejor revisar` are not valid.

Verification rule:

- Run `python3 .agents/planning/scripts/check.py` once and read only its failures. Do not re-derive by reading what it already checked (build, lint, types, tests).
- Check each acceptance criterion through its `verify:` step. A criterion without one goes back to `In Progress`.
- Spend the review on what tools cannot judge: whether the task solved what was asked, edge cases, invalid inputs, and regression risk.

Lessons rule:

- When a finding could repeat, add one line to `.agents/planning/docs/lessons/{area}.md` (format in `.agents/planning/docs/lessons/README.md`).
- If the lesson can be enforced by a test or lint rule, add that check instead of the lesson.

---
