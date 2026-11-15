# Current State

Snapshot of what is true now. Replace lines instead of appending history, and
keep it under 20 bullets. History lives in git and in the task files.

- Purpose: reusable template that gives coding agents a low-token working protocol.
- Layout: the root holds only `AGENTS.md`, `README.md`, `.gitignore`, and the tool folders; hooks, planning data, and scripts live under `.agents/`. The root `README.md` is the template guide.
- Protocol: modules in `.agents/protocol/`. `.claude/CLAUDE.md` imports the always-on ones (00–06, 09, 10); 07, 08, 11, 12, 13 are read on demand.
- `AGENTS.md` is generated from the modules `CLAUDE.md` imports (on-demand ones are left out) by `.agents/planning/scripts/build_agents.py`; the pre-commit hook in `.agents/hooks/` regenerates it. Never edit it by hand.
- Agents: `qa`, `security`, `context-manager` are installed in `.claude/agents/`; 10 generic draft agents and `_template.md` wait in `.agents/agent-catalog/`; setup designs the project's team from them or from scratch.
- `qa` runs on sonnet; the lead agent overrides it to opus for `Deep` reviews. `context-manager` is activated only when the reading path is unclear or context grows.
- Delegation briefs carry goal, acceptance criteria, and relevant state, so subagents skip their `Read First` list.
- Organization chart: areas and review lines live in `.agents/config/org.json`; `build_org.py` writes the Mermaid chart into `README.md` (the pre-commit hook regenerates it). Areas only group roles. Without a project profile the chart shows installed agents plus catalog drafts; with one it shows only the project's team.
- Skills in `.claude/skills/`: `setup-project`, `new-task` (backed by `new_task.py`), `qa-review`.
- Setup gate: until `.agents/context/project_profile.md` exists, the first task is to ask the user for objective and tools and install the needed agents. This template repo has no profile on purpose.
- Tasks: one `task.md` per non-trivial task holds goal, scope, acceptance criteria, and the QA record. Changed files come from git, not from a hand-kept list.
- Legacy tasks 0001–0009 keep separate `qa.md` and `modified_files.md`; the validator accepts both formats.
- Verification: `.agents/planning/scripts/check.py` runs the commands in `.agents/config/checks.json` plus the task-doc validator and prints only failures. It runs from the Claude Code Stop hook, the pre-commit hook, and GitHub Actions.
- Acceptance criteria must end with a `verify:` step; the validator rejects those that do not (single-file tasks only).
- `Standard` and `Deep` tasks are test-first when the project has a test runner. Repeatable QA findings go to `.agents/planning/docs/lessons/{area}.md`.
- The scripts have unit tests in `.agents/planning/scripts/tests/`.
- Known gaps: the Stop hook and the CI workflow have not run in a real project; `require_project_profile` is off in the template and turned on by setup.
