"""Tests for the planning scripts. Run with:

    python -m unittest discover -s .agents/planning/scripts/tests
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

import build_agents  # noqa: E402
import validate_task_docs as v  # noqa: E402

CONFIG = json.loads((v.ROOT / ".agents" / "config" / "review_rules.json").read_text(encoding="utf-8"))

VALID_TASK = """# Task

- `task_id`: `0001-example`
- `title`: `Example`
- `status`: `Done`

## Acceptance Criteria

- The endpoint returns 200 - verify: `pytest tests/test_api.py::test_ok`
- The page shows the total - verify: open /orders and compare with the fixture

## QA

- `review_depth`: `Light`
- `status`: `Done`
- `reviewed_on`: `2026-01-01`

### Checks

- Main behavior: checked.
- Tests run: `pytest tests/test_api.py` passed.

## Follow-Up Review Decision

- `additional_review_needed`: `No`
- `review_task_required`: `No`
- `review_agents`:
- `review_depth`:
- `review_reason`: `Local change with no trust-boundary or persistence impact.`
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
- `other_valid_reason`: `What changed | Concrete risk | Why not covered | Why review is or is not needed`
"""


class ValidatorTests(unittest.TestCase):
    def errors_for(self, text: str) -> list:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp).resolve()
            (folder / "task.md").write_text(text, encoding="utf-8")
            return v.validate_task_folder(folder, CONFIG)

    def test_valid_single_file_task_passes(self):
        self.assertEqual(self.errors_for(VALID_TASK), [])

    def test_task_without_qa_record_fails(self):
        text = VALID_TASK.split("## QA")[0]
        errors = self.errors_for(text)
        self.assertTrue(any("no `## QA` section" in e for e in errors), errors)

    def test_criterion_without_verify_step_fails(self):
        text = VALID_TASK.replace(" - verify: `pytest tests/test_api.py::test_ok`", "")
        errors = self.errors_for(text)
        self.assertTrue(any("has no `verify:` step" in e for e in errors), errors)

    def test_empty_verify_step_fails(self):
        text = VALID_TASK.replace("verify: open /orders and compare with the fixture", "verify:")
        errors = self.errors_for(text)
        self.assertTrue(any("has no `verify:` step" in e for e in errors), errors)

    def test_missing_criteria_fails(self):
        start = VALID_TASK.index("- The endpoint")
        end = VALID_TASK.index("## QA")
        errors = self.errors_for(VALID_TASK[:start] + "\n" + VALID_TASK[end:])
        self.assertTrue(any("has no criteria" in e for e in errors), errors)

    def test_done_qa_without_tests_run_fails(self):
        text = VALID_TASK.replace("- Tests run: `pytest tests/test_api.py` passed.\n", "")
        errors = self.errors_for(text)
        self.assertTrue(any("Tests run" in e for e in errors), errors)

    def test_done_task_with_pending_qa_fails(self):
        text = VALID_TASK.replace("- `review_depth`: `Light`\n- `status`: `Done`", "- `review_depth`: `Light`\n- `status`: `Pending`")
        errors = self.errors_for(text)
        self.assertTrue(any("task is `Done` but QA status" in e for e in errors), errors)

    def test_non_negotiable_trigger_requires_follow_up(self):
        text = VALID_TASK.replace("- `auth_or_login`: `No`", "- `auth_or_login`: `Yes`")
        errors = self.errors_for(text)
        self.assertTrue(any("non-negotiable triggers" in e for e in errors), errors)
        self.assertTrue(any("Security" in e for e in errors), errors)

    def test_generic_other_reason_fails(self):
        text = VALID_TASK.replace("- `other`: `No`", "- `other`: `Yes`").replace(
            "What changed | Concrete risk | Why not covered | Why review is or is not needed", "por si acaso"
        )
        errors = self.errors_for(text)
        self.assertTrue(any("generic phrase" in e for e in errors), errors)

    def test_legacy_task_with_separate_qa_file_passes(self):
        legacy = v.ROOT / ".agents" / "planning" / "tasks" / "2026" / "05" / "0008-add-ml-and-ai-agents"
        if not legacy.exists():
            self.skipTest("example legacy task was removed from this project")
        self.assertEqual(v.validate_task_folder(legacy, CONFIG), [])

    def test_task_template_is_parseable(self):
        template = v.parse_markdown_file(v.ROOT / ".agents" / "planning" / "tasks" / "_templates" / "task.md")
        for section in ("QA", "Follow-Up Review Decision", "Trigger Matrix"):
            self.assertIn(section, template)
        for field in CONFIG["required_trigger_matrix_fields"]:
            self.assertIn(field, template["Trigger Matrix"])


class BuildAgentsTests(unittest.TestCase):
    def test_every_imported_module_exists(self):
        modules = build_agents.always_on_modules()
        self.assertTrue(modules)
        for module in modules:
            self.assertTrue(module.exists(), module)

    def test_agents_md_matches_the_modules(self):
        expected = build_agents.render(build_agents.always_on_modules())
        actual = build_agents.OUTPUT.read_text(encoding="utf-8")
        self.assertEqual(
            actual, expected, "AGENTS.md is stale: run python .agents/planning/scripts/build_agents.py"
        )

    def test_on_demand_modules_are_indexed(self):
        foundations = (build_agents.PROTOCOL_DIR / "01-foundations.md").read_text(encoding="utf-8")
        always_on = set(build_agents.always_on_modules())
        for module in sorted(build_agents.PROTOCOL_DIR.glob("*.md")):
            if module not in always_on:
                self.assertIn(module.name, foundations, f"{module.name} is not listed as on-demand")


if __name__ == "__main__":
    unittest.main()
