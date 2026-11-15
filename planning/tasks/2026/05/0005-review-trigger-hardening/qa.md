# QA

- `task_id`: `0005-review-trigger-hardening`
- `review_depth`: `Light`
- `status`: `Done`
- `reviewed_on`: `2026-05-24`

## Checks

- Confirm `AGENTS.md` and `CLAUDE.md` stay synchronized in all shared sections.
- Confirm mandatory follow-up decision rules are explicit.
- Confirm the QA template includes the expanded trigger matrix and required rationale fields.

## Findings

- `AGENTS.md` and `CLAUDE.md` remain aligned in the shared protocol sections.
- QA follow-up decisions are now explicitly mandatory before task closure.
- The trigger matrix now includes non-negotiable review triggers and an `other` path with required rationale.

## Follow-Up Review Decision

- `additional_review_needed`: `No`
- `review_task_required`: `No`
- `review_agents`:
- `review_depth`:
- `review_scope`: `Protocol documentation and templates only.`
- `review_reason`: `Backfilled to the current qa.md format. The change only touches protocol documentation, agent role files, and templates; it does not alter application behavior, security boundaries, or persistence logic.`
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
