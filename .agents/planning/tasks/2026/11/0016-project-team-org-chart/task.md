# Task

- `task_id`: `0016-project-team-org-chart`
- `title`: `Redraw the organization chart with the team designed for each project`
- `status`: `Done`
- `related_feature_path`: `.agents/planning/features/0001-workflow-protocol-foundation/`
- `owner`: `Claude`
- `created_on`: `2026-11-14`
- `next_step`: `Create or point to the next active task before starting new non-trivial work.`

## Goal

The catalog agents are generic defaults, not final agents. Setup must design
the team each project needs from its objective and tools, and the organization
chart must show that team instead of the default one.

## Scope

- In scope:
  - `build_org.py` template and project modes; `.agents/agent-catalog/_template.md`
  - Step 3 of `11-project-setup.md`, the `setup-project` skill, `05-agent-roles.md`, `README.md`
  - Unit tests for both chart modes
- Out of scope:
  - Improving the content of the ten catalog drafts
  - Area leads as an extra delegation layer

## Acceptance Criteria

- With a project profile, the chart shows only the agents in `.claude/agents/` — verify: unit test `test_project_mode_shows_only_the_projects_team`
- Without a profile, the chart shows installed agents plus catalog drafts — verify: unit test `test_template_mode_shows_catalog_drafts_dashed`
- An installed agent missing from `org.json` stops the build with a clear message — verify: unit test `test_installed_agent_missing_from_org_is_reported`
- A role the catalog lacks can be created and appears in the chart — verify: in a copy of the repo, add a profile, create `payments` from `_template.md`, rewrite `org.json`, run `build_org.py`
- Setup tells the agent to design roles from the objective and tools and to rewrite every agent — verify: read step 3 of `.agents/protocol/11-project-setup.md`

## Notes

- `_template.md` is skipped by every script that lists agents (names starting with `_`).

## QA

- `review_depth`: `Standard`
- `status`: `Done`
- `reviewed_on`: `2026-11-14`

### Checks

- Acceptance criteria: each run through its verify step.
- Main behavior: in a scratch copy with a profile, a `payments` agent created from `_template.md`, and a rewritten `org.json`, the chart listed only `backend`, `payments`, `qa`, `security`, and `context-manager`.
- Invalid inputs and edge cases: an area left without agents and review lines pointing at absent agents are dropped; `org.json` naming an agent with no file is an error.
- Regression risk: the template's own chart is unchanged, because the repo has no profile.
- Tests run: `python3 .agents/planning/scripts/check.py` (26 unit tests and task-doc validation passed).

### Findings

- The setup procedure itself was not run by an agent in a real project; only the scripts it relies on were exercised.
- How well an agent rewrites the drafts for a project depends on the model following step 3; nothing checks that the generic text was replaced.
- The review was done by the implementing agent in the main thread, not by the `qa` subagent.

## Follow-Up Review Decision

- `additional_review_needed`: `No`
- `review_task_required`: `No`
- `review_agents`:
- `review_depth`:
- `review_reason`: `Changes a local chart generator, protocol text, and a skill description; no application behavior, security boundary, or persistence logic changed.`
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
