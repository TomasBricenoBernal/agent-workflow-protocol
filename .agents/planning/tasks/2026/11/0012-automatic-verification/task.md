# Task

- `task_id`: `0012-automatic-verification`
- `title`: `Move quality checks to tools: one check command, verifiable criteria, hooks, CI, lessons`
- `status`: `Done`
- `related_feature_path`: `.agents/planning/features/0001-workflow-protocol-foundation/`
- `owner`: `Claude`
- `created_on`: `2026-11-14`
- `next_step`: `Create or point to the next active task before starting new non-trivial work.`

## Goal

Raise quality without raising token use by letting tools check what tools can
check, and by making every acceptance criterion checkable.

## Scope

- In scope:
  - `.agents/planning/scripts/check.py`, `.agents/config/checks.json`, script unit tests
  - Validator: verifiable criteria, `Tests run`, paths outside the repo
  - Stop hook in `.claude/settings.json`, `.agents/hooks/pre-commit`, `.github/workflows/checks.yml`
  - Protocol modules 01, 02, 03, 06, 11, 13; `qa` agent; task template; lessons folder; `README.md`
- Out of scope:
  - Real lint or test commands for an application (each project defines them at setup)
  - Migrating legacy tasks 0001–0009

## Acceptance Criteria

- One command runs all checks and prints only failures — verify: `python .agents/planning/scripts/check.py`
- The validator rejects a criterion without a verify step — verify: `python -m unittest discover -s .agents/planning/scripts/tests` (test_criterion_without_verify_step_fails)
- The validator accepts task folders outside the repo instead of crashing — verify: unit tests run on temporary folders
- `AGENTS.md` drift is caught automatically — verify: unit test test_agents_md_matches_the_modules
- The Stop hook is silent on success and returns exit code 2 with the failure text on failure — verify: `echo '{}' | python .agents/planning/scripts/check.py --hook; echo $?` with a passing and a deliberately failing tree
- The pre-commit hook runs the checks — verify: make a commit and read the hook output
- The protocol states test-first, search-before-editing, and the lessons rule — verify: `grep -n "Test-first\|search for its usages\|lessons" .agents/protocol/*.md`

## Notes

- `checks.json` ships with one command, the script unit tests, so the template verifies itself.

## QA

- `review_depth`: `Standard`
- `status`: `Done`
- `reviewed_on`: `2026-11-14`

### Checks

- Acceptance criteria: each run through its verify step, except CI (see findings).
- Main behavior: `check.py` passes on the repo; 14 unit tests pass.
- Invalid inputs and edge cases: hook mode tested with a failing command, with `stop_hook_active`, and with an unchanged tree.
- Regression risk: legacy tasks still validate; criteria and `Tests run` rules apply only to single-file tasks.
- Tests run: `python -m unittest discover -s .agents/planning/scripts/tests` (14 passed); `python .agents/planning/scripts/check.py` (passed).

### Findings

- The GitHub Actions workflow has not run yet; it runs for the first time when this is pushed.
- The Stop hook was exercised by calling the script by hand, not by a live Claude Code stop event.
- The Stop hook adds the duration of the project's checks to the end of a turn whenever files changed; slow test suites will be felt.
- The review was done by the implementing agent in the main thread, not by the `qa` subagent.

## Follow-Up Review Decision

- `additional_review_needed`: `No`
- `review_task_required`: `No`
- `review_agents`:
- `review_depth`:
- `review_reason`: `The change adds local check tooling, a CI workflow that only runs those checks, and protocol text; it does not alter application behavior, security boundaries, or persistence logic.`
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
