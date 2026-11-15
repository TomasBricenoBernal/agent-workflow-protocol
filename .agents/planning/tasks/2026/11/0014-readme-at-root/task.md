# Task

- `task_id`: `0014-readme-at-root`
- `title`: `Put the guide back at the root as README.md and correct what was inaccurate`
- `status`: `Done`
- `related_feature_path`: `.agents/planning/features/0001-workflow-protocol-foundation/`
- `owner`: `Claude`
- `created_on`: `2026-11-14`
- `next_step`: `Create or point to the next active task before starting new non-trivial work.`

## Goal

Make the guide the project's root `README.md` again and make every statement in
it match the repository.

## Scope

- In scope:
  - `README.md` (moved from `.agents/README.md`), `current_state.md`
  - `python` → `python3` in the commands of docs, protocol, and agent files
  - Singular/plural in the `check.py` summary line
- Out of scope:
  - Behavior changes to the protocol or the scripts

## Acceptance Criteria

- The guide is `README.md` at the root and `.agents/README.md` no longer exists — verify: `ls README.md .agents/README.md`
- Every file or folder path the guide names exists — verify: the path-existence script recorded under Checks reports none missing
- The model and edit-tool columns of the agent table match each agent's frontmatter — verify: `grep -H "^model:\|^tools:" .claude/agents/*.md .agents/agent-catalog/*.md`
- The getting-started commands work on a fresh copy, before and after clearing the examples — verify: export `HEAD` to an empty folder, run `build_agents.py` and `check.py`, delete the example folders, run `check.py` again
- Commands in the guide run on a machine without a `python` executable — verify: `grep -n "python " README.md` returns nothing

## Notes

- The repository was renamed on GitHub to `agent-workflow-protocol`; the local remote URL was updated to match.

## QA

- `review_depth`: `Light`
- `status`: `Done`
- `reviewed_on`: `2026-11-14`

### Checks

- Acceptance criteria: each run through its verify step.
- Main behavior: the guide was read in full and each claim compared with the files, agent frontmatter, scripts, and the GitHub template flag.
- Invalid inputs and edge cases: after clearing the examples, the validator run without arguments fails because `active_task.md` points at a deleted task; the guide no longer tells the reader to run it there.
- Regression risk: `python` → `python3` was applied to docs, protocol, agents, hook, and workflow; legacy task docs were left as written.
- Tests run: `python3 .agents/planning/scripts/check.py` (14 unit tests and task-doc validation passed).

### Findings

- Corrected: a reference to a section that does not exist, the "read-only" label for agents that still have `Bash`, the `Low` budget summary, three module descriptions, and a verify step that failed after the recommended cleanup.
- Not checked against a live tool: that `/agents` lists the three core agents, and that the Stop hook fires on a real stop event.
- The review was done by the implementing agent in the main thread, not by the `qa` subagent.

## Follow-Up Review Decision

- `additional_review_needed`: `No`
- `review_task_required`: `No`
- `review_agents`:
- `review_depth`:
- `review_reason`: `Documentation move and corrections plus a wording fix in a script message; no behavior, security boundary, or persistence logic changed.`
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
