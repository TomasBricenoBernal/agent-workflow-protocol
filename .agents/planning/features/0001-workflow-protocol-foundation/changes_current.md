# Current Changes

Summarize only the current feature-relevant behavior changes.

- Added a shared task-tracking structure for non-trivial work.
- Added review gates requiring QA before `Done`, with Security review only when risk triggers apply.
- Added reusable Claude role files aligned with the shared protocol.
- Added minimal templates for tasks, features, and reusable docs.
- Added explicit token consumption strategies and activation ceilings for agent orchestration.
- Added clear limitation boundaries for each agent to reduce overlap.
- Added a dedicated DevOps specialization and clarified how delivery work enters the methodology.
- Added a prioritized token-efficiency model with low-effort, medium-effort, and structural improvements.
- Added single-lead stage ownership plus structured handoffs to reduce duplicate context reading.
- Added QA-by-evidence and trigger-based Security review rules to lower review token cost.
- Added QA-driven follow-up review scheduling with explicit rationale and assigned review agents.
- Added task and feature template fields to track review-task relationships and scheduled specialist reviews.
- Added mandatory QA follow-up decisions before task closure.
- Added non-negotiable review triggers plus an expanded trigger matrix with `other` and required justification.
- Made `qa.md` required for non-trivial tasks.
- Balanced closure gating so normal tasks stay light while high-signal review failures still block completion.
- Added a config-driven local validator for task and QA documents.
- Added a documented command for validating non-trivial task docs before moving them to `Done`.
- Added a dedicated `Machine Learning` Claude agent specialization.
- Added a dedicated `AI Integrations` Claude agent specialization for AI APIs, prompts, and automations.
- Added a mandatory project setup task: the agent asks for the objective and tools, then installs and tailors only the needed subagents.
- Reduced the default installed subagents to `qa`, `security`, and `context-manager`; the other 10 moved to `.agents/agent-catalog/`.
- Merged the QA record into `task.md`; removed hand-kept `modified_files.md` and the `TASK.md` mirror.
- Made `current_state.md` a capped snapshot instead of a running log.
- Moved data/ML rules and review governance to on-demand modules 12 and 13.
- QA now runs on sonnet and escalates to opus only for `Deep` reviews.
- `context-manager` is activated on demand instead of at the start of every task.
- Delegation briefs carry goal, acceptance criteria, and state so subagents skip repeated reads.
- `AGENTS.md` now inlines only the modules `CLAUDE.md` imports.
- Added `check.py`, one command that runs the project checks and the task validator and prints only failures; wired to a Stop hook, pre-commit, and CI.
- Acceptance criteria now require a `verify:` step, enforced by the validator.
- Added test-first, search-before-editing, and lessons rules, plus unit tests for the scripts.
- Moved planning data, scripts, git hooks, and the guide under `.agents/`, and `CLAUDE.md` into `.claude/`, leaving a minimal root.
