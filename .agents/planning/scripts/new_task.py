#!/usr/bin/env python3
"""Create the next task folder from the template and point active_task.md at it.

    python3 .agents/planning/scripts/new_task.py "add login form" [--feature PATH]

Picks the next task id, creates `.agents/planning/tasks/YYYY/MM/{id}-{slug}/task.md`
from the template with id, title, date, and status filled in, and rewrites
`.agents/planning/tasks/active_task.md`. Prints the new task path.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not slug:
        raise SystemExit("The task title needs at least one letter or digit")
    return slug[:50].rstrip("-")


def next_task_id(tasks_dir: Path) -> str:
    ids = [
        int(match.group(1))
        for folder in tasks_dir.glob("*/*/*")
        if folder.is_dir() and (match := re.match(r"(\d{4})-", folder.name))
    ]
    return f"{max(ids, default=0) + 1:04d}"


def set_field(text: str, field: str, value: str) -> str:
    pattern = re.compile(rf"^- `{re.escape(field)}`:.*$", re.MULTILINE)
    if not pattern.search(text):
        raise SystemExit(f"The task template has no `{field}` field")
    return pattern.sub(f"- `{field}`: `{value}`", text, count=1)


def create_task(root: Path, title: str, feature: str = "", today: date | None = None) -> Path:
    today = today or date.today()
    tasks_dir = root / ".agents" / "planning" / "tasks"
    task_id = f"{next_task_id(tasks_dir)}-{slugify(title)}"
    folder = tasks_dir / f"{today:%Y}" / f"{today:%m}" / task_id
    folder.mkdir(parents=True)

    text = (tasks_dir / "_templates" / "task.md").read_text(encoding="utf-8")
    text = set_field(text, "task_id", task_id)
    text = set_field(text, "title", title)
    text = set_field(text, "status", "In Progress")
    text = set_field(text, "created_on", today.isoformat())
    if feature:
        text = set_field(text, "related_feature_path", feature)
    (folder / "task.md").write_text(text, encoding="utf-8")

    rel = folder.relative_to(root).as_posix() + "/"
    lines = [
        "# Active Task",
        "",
        f"- `task_id`: `{task_id}`",
        "- `status`: `In Progress`",
        f"- `path`: `{rel}`",
    ]
    if feature:
        lines.append(f"- `related_feature`: `{feature}`")
    lines += [f"- `current_goal`: `{title}`", "- `next_step`: `Fill in goal, scope, and acceptance criteria.`", ""]
    (tasks_dir / "active_task.md").write_text("\n".join(lines), encoding="utf-8")
    return folder


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the next task folder from the template.")
    parser.add_argument("title", help="Short task title, e.g. 'add login form'.")
    parser.add_argument("--feature", default="", help="Related feature folder path, if any.")
    args = parser.parse_args()
    folder = create_task(ROOT, args.title, args.feature)
    print(folder.relative_to(ROOT).as_posix() + "/task.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
