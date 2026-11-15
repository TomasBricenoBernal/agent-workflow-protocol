"""Tests for the planning scripts. Run with:

    python3 -m unittest discover -s .agents/planning/scripts/tests
"""

import json
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

import build_agents  # noqa: E402
import build_org  # noqa: E402
import new_task  # noqa: E402
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
            actual, expected, "AGENTS.md is stale: run python3 .agents/planning/scripts/build_agents.py"
        )

    def test_on_demand_modules_are_indexed(self):
        foundations = (build_agents.PROTOCOL_DIR / "01-foundations.md").read_text(encoding="utf-8")
        always_on = set(build_agents.always_on_modules())
        for module in sorted(build_agents.PROTOCOL_DIR.glob("*.md")):
            if module not in always_on:
                self.assertIn(module.name, foundations, f"{module.name} is not listed as on-demand")


class BuildOrgTests(unittest.TestCase):
    ORG = {
        "lead": "Lead",
        "areas": [
            {"name": "Build", "agents": ["backend", "payments"]},
            {"name": "Data", "agents": ["data-analytics"]},
            {"name": "Review", "agents": ["qa"]},
        ],
        "reviews": [
            {"from": "qa", "to_area": "Build", "label": "reviews"},
            {"from": "qa", "to_area": "Data", "label": "reviews"},
            {"from": "qa", "to": "data-analytics", "label": "checks data"},
        ],
    }

    def agent_dirs(self, tmp: str) -> tuple:
        installed_dir, catalog_dir = Path(tmp, "installed"), Path(tmp, "catalog")
        installed_dir.mkdir()
        catalog_dir.mkdir()
        for name, model in (("qa", "sonnet"), ("payments", "opus")):
            (installed_dir / f"{name}.md").write_text(f"---\nname: {name}\nmodel: {model}\n---\n")
        for name in ("backend", "data-analytics"):
            (catalog_dir / f"{name}.md").write_text(f"---\nname: {name}\nmodel: sonnet\n---\n")
        (catalog_dir / "_template.md").write_text("---\nname: role-name\nmodel: sonnet\n---\n")
        return build_org.agent_files(installed_dir), build_org.agent_files(catalog_dir)

    def test_template_mode_shows_catalog_drafts_dashed(self):
        with tempfile.TemporaryDirectory() as tmp:
            installed, catalog = self.agent_dirs(tmp)
            chart = build_org.render(self.ORG, installed, catalog, configured=False)
        self.assertIn('backend["backend<br/>sonnet"]', chart)
        self.assertIn('payments["payments<br/>opus"]', chart)
        self.assertIn("class backend,data_analytics catalog", chart)

    def test_project_mode_shows_only_the_projects_team(self):
        with tempfile.TemporaryDirectory() as tmp:
            installed, catalog = self.agent_dirs(tmp)
            chart = build_org.render(self.ORG, installed, catalog, configured=True)
        self.assertIn('payments["payments<br/>opus"]', chart)
        self.assertIn('qa["qa<br/>sonnet"]', chart)
        self.assertNotIn("backend", chart)
        self.assertNotIn("data_analytics", chart)
        self.assertNotIn("area_Data", chart)  # empty area and its review lines are dropped
        self.assertNotIn("catalog", chart)
        self.assertIn('qa -. "reviews" .-> area_Build', chart)

    def test_template_file_is_not_an_agent(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, catalog = self.agent_dirs(tmp)
        self.assertNotIn("_template", catalog)

    def test_org_naming_an_agent_without_a_file_is_an_error(self):
        org = {"lead": "Lead", "areas": [{"name": "Build", "agents": ["ghost"]}], "reviews": []}
        with self.assertRaises(SystemExit):
            build_org.render(org, {}, {}, configured=False)

    def test_installed_agent_missing_from_org_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            installed, _ = self.agent_dirs(tmp)
        org = {"lead": "Lead", "areas": [{"name": "Review", "agents": ["qa"]}], "reviews": []}
        self.assertEqual(build_org.unplaced_agents(org, installed), ["payments"])

    def test_repo_org_places_every_installed_agent_once(self):
        org = build_org.load_org()
        listed = [name for area in org["areas"] for name in area["agents"]]
        self.assertEqual(len(listed), len(set(listed)), "an agent is listed in two areas")
        self.assertEqual(build_org.unplaced_agents(org, build_org.agent_files(build_org.INSTALLED_DIR)), [])
        self.assertLessEqual(set(listed), build_org.agent_names(), "org.json names an agent with no file")

    def test_readme_chart_is_current(self):
        readme = build_org.README.read_text(encoding="utf-8")
        self.assertIn(
            build_org.block(build_org.load_org()),
            readme,
            "The organization chart is stale: run python3 .agents/planning/scripts/build_org.py",
        )

    def test_agent_template_has_the_required_frontmatter(self):
        text = (build_org.CATALOG_DIR / "_template.md").read_text(encoding="utf-8")
        for field in ("name:", "description:", "tools:", "model:"):
            self.assertIn(field, text)


class NewTaskTests(unittest.TestCase):
    def make_root(self, tmp: str) -> Path:
        root = Path(tmp).resolve()
        templates = root / ".agents" / "planning" / "tasks" / "_templates"
        templates.mkdir(parents=True)
        shutil.copy(v.ROOT / ".agents" / "planning" / "tasks" / "_templates" / "task.md", templates)
        return root

    def test_first_task_gets_id_0001(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            folder = new_task.create_task(root, "Add login form!", today=date(2027, 3, 9))
            self.assertEqual(folder.relative_to(root).as_posix(), ".agents/planning/tasks/2027/03/0001-add-login-form")

    def test_next_id_follows_the_highest_existing_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            (root / ".agents" / "planning" / "tasks" / "2026" / "05" / "0007-old").mkdir(parents=True)
            folder = new_task.create_task(root, "next", today=date(2027, 3, 9))
            self.assertEqual(folder.name, "0008-next")

    def test_task_file_and_active_pointer_are_filled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            folder = new_task.create_task(root, "Add login form", today=date(2027, 3, 9))
            task = v.parse_markdown_file(folder / "task.md")["root"]
            self.assertEqual(task["task_id"], "0001-add-login-form")
            self.assertEqual(task["status"], "In Progress")
            self.assertEqual(task["created_on"], "2027-03-09")
            active = v.parse_markdown_file(root / ".agents" / "planning" / "tasks" / "active_task.md")["root"]
            self.assertEqual(active["path"], ".agents/planning/tasks/2027/03/0001-add-login-form/")

    def test_title_without_letters_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            with self.assertRaises(SystemExit):
                new_task.create_task(root, "!!!")


if __name__ == "__main__":
    unittest.main()
