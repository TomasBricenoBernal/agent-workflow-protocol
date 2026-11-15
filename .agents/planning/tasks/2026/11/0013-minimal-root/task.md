# Task

- `task_id`: `0013-minimal-root`
- `title`: `Move everything the tools do not require at the root into hidden folders`
- `status`: `Done`
- `related_feature_path`: `.agents/planning/features/0001-workflow-protocol-foundation/`
- `owner`: `Claude`
- `created_on`: `2026-11-14`
- `next_step`: `Create or point to the next active task before starting new non-trivial work.`

## Goal

Leave the repository root with the fewest possible entries so a project built
from the template keeps its root for its own code.

## Scope

- In scope:
  - `planning/` → `.agents/planning/`, `.githooks/` → `.agents/hooks/`
  - `CLAUDE.md` → `.claude/CLAUDE.md`, template `README.md` → `.agents/README.md`
  - A short root `README.md` for the project
  - Every path reference in protocol, scripts, hooks, settings, workflow, and docs
- Out of scope:
  - `AGENTS.md`, `.gitignore`, `.claude/`, `.github/` (their tools require the location)

## Acceptance Criteria

- The root lists only `AGENTS.md`, `README.md`, `.gitignore`, and hidden tool folders — verify: `ls -A`
- All checks pass from the new locations — verify: `python .agents/planning/scripts/check.py`
- No reference to the old locations remains — verify: `git grep -nE "(^|[^/.a-z])planning/|\.githooks" -- . ':!AGENTS.md'` returns nothing
- `AGENTS.md` is built from the imports in `.claude/CLAUDE.md` — verify: `python .agents/planning/scripts/build_agents.py` lists 9 modules
- The pre-commit hook runs from `.agents/hooks` — verify: make a commit and read the hook output

## Notes

- Imports in `.claude/CLAUDE.md` are written relative to that file (`@../.agents/protocol/...`).

## QA

- `review_depth`: `Standard`
- `status`: `Done`
- `reviewed_on`: `2026-11-14`

### Checks

- Acceptance criteria: each run through its verify step.
- Main behavior: scripts resolve the repo root from their new depth; hook, workflow, settings, and `checks.json` point to the new paths.
- Invalid inputs and edge cases: an existing clone keeps `core.hooksPath=.githooks`, which no longer exists; it must be set again to `.agents/hooks`.
- Regression risk: path rewrite was mechanical across all tracked text files, legacy task docs included.
- Tests run: `python .agents/planning/scripts/check.py` (14 unit tests and task-doc validation passed).

### Findings

- Claude Code picked up `.claude/CLAUDE.md` in this session; that the `@../` imports expand was not confirmed in a fresh session.
- The GitHub landing page now shows the short root README instead of the full guide.
- The review was done by the implementing agent in the main thread, not by the `qa` subagent.

## Follow-Up Review Decision

- `additional_review_needed`: `No`
- `review_task_required`: `No`
- `review_agents`:
- `review_depth`:
- `review_reason`: `Files were moved and paths rewritten; no behavior, security boundary, or persistence logic changed.`
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
