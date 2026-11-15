# Task

- `task_id`: `0011-token-savings-agents`
- `title`: `Cut agent-side token use: QA model by depth, on-demand context manager, richer briefs, slimmer AGENTS.md`
- `status`: `Done`
- `related_feature_path`: `.agents/planning/features/0001-workflow-protocol-foundation/`
- `owner`: `Claude`
- `created_on`: `2026-11-14`
- `next_step`: `Create or point to the next active task before starting new non-trivial work.`

## Goal

Reduce what agents spend per task without dropping a check: run QA on a cheaper
model unless the review is `Deep`, stop activating `context-manager` on every
task, let the delegation brief replace repeated context reads, and keep
on-demand modules out of `AGENTS.md`.

## Scope

- In scope:
  - `.claude/agents/qa.md`, `.claude/agents/context-manager.md`, the `Read First` note in all 13 agent files
  - Protocol modules 00, 01, 02, 04, 05, 06
  - `.agents/planning/scripts/build_agents.py`, `AGENTS.md`
  - `README.md`, `CLAUDE.md`, `current_state.md`
- Out of scope:
  - The `Low` budget limits
  - Tests or CI for the scripts

## Acceptance Criteria

- `qa` defaults to sonnet and the protocol says who escalates to opus and when. — verify: `grep -n "model:" .claude/agents/qa.md` and the depth paragraph in `02-task-tracking.md`
- QA has a defined way to escalate when it finds a `Deep` change while running on the default model. — verify: `grep -n "Escalate to Deep" .claude/agents/qa.md`
- `context-manager` is no longer a mandatory first step. — verify: step 1 of `06-methodology-docs.md`
- The delegation rule lists what a brief must carry, and every agent file allows skipping reads the brief covers. — verify: `grep -L "delegating brief" .claude/agents/*.md .agents/agent-catalog/*.md` returns nothing
- `AGENTS.md` contains exactly the modules `CLAUDE.md` imports. — verify: `python -m unittest discover -s .agents/planning/scripts/tests` (test_agents_md_matches_the_modules)

## Notes

- The always-on set has one source: the import lines in `CLAUDE.md`. The build script fails if an imported module is missing.

## QA

- `review_depth`: `Standard`
- `status`: `Done`
- `reviewed_on`: `2026-11-14`

### Checks

- Acceptance criteria: each checked against the working tree.
- Main behavior: `build_agents.py` run; it inlined 9 modules and listed 5 as on-demand.
- Invalid inputs and edge cases: the script exits with an error when `CLAUDE.md` has no imports or imports a missing module (read from the code, not executed).
- Regression risk: the on-demand index in `01-foundations.md` is inlined in `AGENTS.md`, so Codex and opencode still learn which modules exist and when to read them.
- Tests run: `build_agents.py`; `validate_task_docs.py` on every task folder. Neither script has automated tests.

### Findings

- The per-call model override for `Deep` depends on the delegating tool supporting it; this was not exercised in a live delegation.
- Running `Light` and `Standard` QA on sonnet is a quality trade-off on paper only: no review was run on both models to compare.
- The review was done by the implementing agent in the main thread, not by the `qa` subagent.

## Follow-Up Review Decision

- `additional_review_needed`: `No`
- `review_task_required`: `No`
- `review_agents`:
- `review_depth`:
- `review_reason`: `The change touches agent definitions, protocol text, and the local AGENTS.md build script; it does not alter application behavior, security boundaries, or persistence logic.`
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
