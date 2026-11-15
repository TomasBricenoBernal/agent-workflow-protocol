## Development Methodology

Use this repository workflow for normal delivery:

1. Start from the core reading order. Activate `Context` only when the reading path is unclear, the context has grown large, or work is drifting into unrelated files.
2. Open or point to a task when the work is non-trivial or crosses files.
3. Assign one lead agent for the current stage and keep other agents inactive unless triggered.
4. Add specialist agents only when their trigger conditions are reached.
5. When ownership changes, write a short structured handoff instead of re-explaining full context.
6. Record reusable decisions in shared context or feature files instead of repeating them in chat.
7. Move the task to `In Review` after implementation, then run QA from diff, acceptance criteria, and nearby regression risk.
8. During QA, explicitly decide whether a dedicated follow-up review task is needed and record the rationale.
9. If a follow-up review is needed, create a new review task and assign the required review agents and depth.
10. Run Security or Database review directly only when QA determines a separate review task is unnecessary and the protocol still requires a local pass.
11. Run `python .agents/planning/scripts/check.py` before closing a non-trivial task; read only what it reports as failed.
12. Move to `Done` only after tracking, QA, validation, and any scheduled follow-up reviews are complete.

Test-first rule: for `Standard` and `Deep` tasks in a project with a test runner,
write the failing test from the acceptance criteria before the implementation.
Let machines check what machines can check (`check.py`); spend review effort on
whether the task solved what was asked, edge cases, and risk.

---

## Documentation Rule

Documentation is not a default agent.

Use documentation as a closing responsibility when:

- A decision will be reused.
- A schema change requires traceability.
- A feature is becoming hard to track.

Rules:

- Document decisions, not conversations.
- Avoid duplication.
- Update only relevant docs.
- Keep docs short.

---

