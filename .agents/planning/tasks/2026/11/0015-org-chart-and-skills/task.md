# Task

- `task_id`: `0015-org-chart-and-skills`
- `title`: `Add a generated organization chart, task-creation script, and three skills`
- `status`: `Done`
- `related_feature_path`: `.agents/planning/features/0001-workflow-protocol-foundation/`
- `owner`: `Claude`
- `created_on`: `2026-11-14`
- `next_step`: `Create or point to the next active task before starting new non-trivial work.`

## Goal

Show who the lead agent can delegate to and who reviews whom as a chart that is
generated from the agent files, and turn the three recurring procedures into
Claude Code skills backed by scripts.

## Scope

- In scope:
  - `.agents/config/org.json`, `build_org.py`, the chart block in `README.md`
  - `new_task.py`; skills `setup-project`, `new-task`, `qa-review`
  - Pre-commit hook, protocol modules 02, 05, 11, unit tests
- Out of scope:
  - Area leads as an extra delegation layer
  - Workflows, a session-start hook, packaging as a plugin

## Acceptance Criteria

- The chart lists every agent file exactly once, with its model and whether it is installed — verify: unit tests `BuildOrgTests`
- A stale chart fails the checks — verify: unit test `test_readme_chart_matches_org_and_agent_files`
- The chart renders on GitHub — verify: open `README.md` on GitHub after pushing and look at the Organization chart section
- A new task is created with the next id, the template, and the active pointer in one command — verify: unit tests `NewTaskTests`
- The three skills exist with a name and a description — verify: `head -4 .claude/skills/*/SKILL.md`
- The skills point at the protocol modules instead of repeating them — verify: read `.claude/skills/setup-project/SKILL.md`

## Notes

- This task folder was created with `new_task.py`.
- Areas only group roles; the lead agent still delegates directly, so the chart adds no delegation cost.

## QA

- `review_depth`: `Standard`
- `status`: `Done`
- `reviewed_on`: `2026-11-14`

### Checks

- Acceptance criteria: run through their verify steps, except the GitHub rendering (see findings).
- Main behavior: `build_org.py` wrote the chart; `new_task.py` created this task folder and updated the active pointer.
- Invalid inputs and edge cases: an agent missing from `org.json`, an agent listed twice, a review line to an unknown target, and a title with no letters are covered by tests or by an explicit error.
- Regression risk: the pre-commit hook now also rewrites `README.md`; it only touches the block between the ORG markers.
- Tests run: `python3 .agents/planning/scripts/check.py` (21 unit tests and task-doc validation passed).

### Findings

- The Mermaid chart was not rendered locally; whether GitHub draws it as intended is unverified until it is pushed.
- The skills were not invoked in a live Claude Code session; only their files and the scripts they call were checked.
- The review was done by the implementing agent in the main thread, not by the `qa` subagent.

## Follow-Up Review Decision

- `additional_review_needed`: `No`
- `review_task_required`: `No`
- `review_agents`:
- `review_depth`:
- `review_reason`: `Adds local scripts, documentation, and skill files; no application behavior, security boundary, or persistence logic changed.`
- `proposed_task_path`:

## Trigger Matrix

- `auth_or_login`: `No`
- `authorization_or_permissions`: `No`
- `sensitive_data`: `No`
- `public_exposure_or_external_integration`: `No`
- `file_upload_or_file_handling`: `No`
- `secrets_or_sensitive_configuration`: `No`
- `schema_or_migration_change`: `No`
- `integrity_sensitive_query_or_constraint`: `No`
- `other`: `No`
- `other_valid_reason`: `What changed | Concrete risk | Why standard triggers do not cover it | Why extra review is or is not needed`

## Recommendation

- `Done`
