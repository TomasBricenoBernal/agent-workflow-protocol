# Task

- `task_id`: `0009-project-setup-gate`
- `title`: `Make project setup a mandatory first task that installs the needed agents`
- `status`: `Done`
- `related_feature`: `0001-workflow-protocol-foundation`
- `related_feature_path`: `planning/features/0001-workflow-protocol-foundation/`
- `owner`: `Claude`
- `created_on`: `2026-11-14`
- `parent_task`:
- `review_requested_by`:
- `review_agents`:
- `next_step`: `Create or point to the next active task before starting new non-trivial work.`

## Goal

Stop shipping all 13 subagents as active. A project built from the template must
start with a mandatory setup task in which the user states the objective and the
tools, and the agent installs and tailors only the subagents that project needs.

## Scope

- In scope:
  - `.agents/protocol/` (setup gate, new on-demand module, role map notes)
  - `.agents/agent-catalog/` (optional subagents moved out of `.claude/agents/`)
  - `README.md`
  - Task, feature, and context tracking updates
- Out of scope:
  - Changing the content of any subagent file
  - Validator enforcement of the project profile
  - Trimming the always-on protocol

## Acceptance Criteria

- Only `qa`, `security`, and `context-manager` remain in `.claude/agents/`.
- The other 10 subagents are available unchanged in `.agents/agent-catalog/`.
- The always-on protocol blocks non-trivial work until `.agents/context/project_profile.md` exists.
- The setup module tells the agent what to ask, how to record it, and how to choose, install, and tailor agents.
- `README.md` documents the setup step.

## Review Relationship

- `is_review_task`: `No`
- `review_scope`:
- `review_reason`:

## Notes

- The template repo itself ships without a profile on purpose; the gate has an explicit exception for template maintenance.
