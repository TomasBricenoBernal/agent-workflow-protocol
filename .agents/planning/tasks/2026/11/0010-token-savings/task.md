# Task

- `task_id`: `0010-token-savings`
- `title`: `Cut per-task bookkeeping, make current state a snapshot, and trim the always-on protocol`
- `status`: `Done`
- `related_feature_path`: `.agents/planning/features/0001-workflow-protocol-foundation/`
- `owner`: `Claude`
- `created_on`: `2026-11-14`
- `next_step`: `Create or point to the next active task before starting new non-trivial work.`

## Goal

Reduce token use without removing any real check: one file per task, no
hand-kept duplicates of what git records, a capped current-state snapshot, and
niche rules moved out of the always-on protocol.

## Scope

- In scope:
  - Task and feature templates, `review_rules.json`, the validator
  - `.agents/context/` (snapshot, removal of the `TASK.md` mirror)
  - Protocol modules 01, 02, 03, 05, 07, 08, 09, 11 and new on-demand modules 12, 13
  - Agent reading lists, `README.md`
- Out of scope:
  - Migrating legacy tasks 0001–0009 to the single-file format
  - QA model tiering, `context-manager` activation, subagent briefs, trimming `AGENTS.md`
  - The `Low` budget limits

## Acceptance Criteria

- A new task needs only `task.md`; the validator reads the QA record from it. — verify: copy the template to a folder and run `validate_task_docs.py` on it
- Legacy tasks with a separate `qa.md` still validate. — verify: `python .agents/planning/scripts/validate_task_docs.py .agents/planning/tasks/2026/05/0008-add-ml-and-ai-agents/`
- No protocol file, template, or agent refers to `TASK.md` or a hand-kept `modified_files.md`. — verify: `grep -rn "TASK\.md\|modified_files" .agents/protocol .claude .agents/planning/tasks/_templates` returns nothing
- `current_state.md` is a snapshot with a stated cap and a no-history rule. — verify: read `.agents/context/current_state.md` header and `02-task-tracking.md` completion rule
- Data/ML rules and review governance load on demand, and the QA agent is told to read the governance module. — verify: `01-foundations.md` lists modules 12 and 13; `.claude/agents/qa.md` Read First names module 13
- Every QA rule that existed before still exists somewhere the reviewer is directed to. — verify: compare `git show HEAD:.agents/protocol/05-agent-roles.md` with `13-review-governance.md`

## Notes

- This task is the first one recorded in the single-file format.

## QA

- `review_depth`: `Standard`
- `status`: `Done`
- `reviewed_on`: `2026-11-14`

### Checks

- Acceptance criteria: each checked against the working tree.
- Main behavior: validator run on all ten task folders, both formats.
- Invalid inputs and edge cases: a task with neither a `## QA` section nor `qa.md` reports an error instead of passing silently.
- Regression risk: searched protocol, templates, agents, and README for references to the removed files.
- Tests run: `validate_task_docs.py` on every task folder; `build_agents.py`. The validator has no automated tests.

### Findings

- Always-on protocol went from about 5,570 to about 4,190 tokens (estimated at 4 characters per token), a cut of roughly 25%, not the half that was proposed.
- The review was done by the implementing agent in the main thread, not by the `qa` subagent.
- The new format has not been exercised by an agent in a real project.
- Legacy feature `0001` keeps its old `modified_files.md`; it is no longer updated.

## Follow-Up Review Decision

- `additional_review_needed`: `No`
- `review_task_required`: `No`
- `review_agents`:
- `review_depth`:
- `review_reason`: `The change touches protocol text, templates, and the local doc validator; it does not alter application behavior, security boundaries, or persistence logic.`
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
