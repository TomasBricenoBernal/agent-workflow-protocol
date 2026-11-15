#!/usr/bin/env python3
"""Run every project check and print only what failed.

One entry point for agents, the pre-commit hook, and CI:

    python planning/scripts/check.py

It runs, in order:

1. The commands listed in `.agents/config/checks.json` (lint, types, tests,
   build - whatever the project defined during setup).
2. The task-doc validator on every task whose status is `Done`.
3. The project-profile check, when `require_project_profile` is true.

Passing checks print one summary line. Failing checks print the tail of their
output, so an agent reads a few lines instead of a full log.

`--hook` is for the Claude Code Stop hook: it stays silent on success, skips the
run when nothing changed since the last passing run, and exits with code 2 on
failure so the failure text is handed back to the agent.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG = ROOT / ".agents" / "config" / "checks.json"
PROFILE = ROOT / ".agents" / "context" / "project_profile.md"
VALIDATOR = ROOT / "planning" / "scripts" / "validate_task_docs.py"
TASKS_DIR = ROOT / "planning" / "tasks"
STATE_FILE_NAME = "agent_check_state"
TAIL_LINES = 40
STATUS_RE = re.compile(r"^\s*-\s+`status`:\s*`([^`]*)`")


def run(command, shell: bool = False) -> Tuple[int, str]:
    proc = subprocess.run(
        command, shell=shell, cwd=ROOT, capture_output=True, text=True
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def tail(text: str) -> str:
    lines = text.splitlines()
    if len(lines) <= TAIL_LINES:
        return text
    return f"... ({len(lines) - TAIL_LINES} earlier lines omitted)\n" + "\n".join(lines[-TAIL_LINES:])


def load_config() -> dict:
    if not CONFIG.exists():
        return {"commands": [], "require_project_profile": False}
    try:
        return json.loads(CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {CONFIG}: {exc}") from exc


def task_status(task_md: Path) -> str:
    """Status from the root block of task.md (before the first `## ` heading)."""
    for line in task_md.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            break
        match = STATUS_RE.match(line)
        if match:
            return match.group(1)
    return ""


def done_task_folders() -> List[Path]:
    folders = []
    for task_md in sorted(TASKS_DIR.glob("*/*/*/task.md")):
        if task_status(task_md) == "Done":
            folders.append(task_md.parent)
    return folders


def run_checks() -> Tuple[int, List[Tuple[str, str]]]:
    """Return (number of checks run, list of (name, output) failures)."""
    config = load_config()
    failures: List[Tuple[str, str]] = []
    count = 0

    for entry in config.get("commands", []):
        name = entry.get("name", "unnamed")
        command = entry.get("run", "").replace("{python}", f'"{sys.executable}"')
        if not command:
            failures.append((name, "checks.json entry has no `run` command"))
            continue
        count += 1
        code, output = run(command, shell=True)
        if code != 0:
            failures.append((name, f"$ {command}\n{tail(output)}"))

    folders = done_task_folders()
    if folders:
        count += 1
        code, output = run([sys.executable, str(VALIDATOR), *[str(f) for f in folders]])
        if code != 0:
            errors = "\n".join(l for l in output.splitlines() if not l.startswith("OK:"))
            failures.append(("task-docs", tail(errors)))

    if config.get("require_project_profile"):
        count += 1
        if not PROFILE.exists():
            failures.append((
                "project-profile",
                f"{PROFILE.relative_to(ROOT)} is missing: run project setup "
                "(.agents/protocol/11-project-setup.md) before other work",
            ))

    return count, failures


def format_failures(failures: List[Tuple[str, str]]) -> str:
    blocks = [f"FAILED: {name}\n{output}" for name, output in failures]
    return "\n\n".join(blocks)


def tree_state() -> Optional[str]:
    """Fingerprint of the working tree, or None outside a git repository."""
    parts = []
    for args in (["git", "rev-parse", "HEAD"], ["git", "status", "--porcelain"], ["git", "diff", "HEAD"]):
        code, output = run(args)
        if code != 0:
            return None
        parts.append(output)
    code, untracked = run(["git", "ls-files", "--others", "--exclude-standard"])
    if code == 0:
        for name in untracked.splitlines():
            path = ROOT / name
            if path.is_file():
                stat = path.stat()
                parts.append(f"{name}:{stat.st_size}:{stat.st_mtime_ns}")
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def state_file() -> Optional[Path]:
    code, git_dir = run(["git", "rev-parse", "--git-dir"])
    if code != 0:
        return None
    path = Path(git_dir)
    return (path if path.is_absolute() else ROOT / path) / STATE_FILE_NAME


def hook_mode() -> int:
    if not sys.stdin.isatty():
        try:
            payload = json.load(sys.stdin)
        except (json.JSONDecodeError, ValueError):
            payload = {}
        # Already continuing because of this hook: do not block again.
        if payload.get("stop_hook_active"):
            return 0

    state = tree_state()
    cache = state_file()
    if state is not None:
        code, status = run(["git", "status", "--porcelain"])
        if code == 0 and not status:
            return 0  # nothing changed since the last commit
        if cache is not None and cache.exists() and cache.read_text().strip() == state:
            return 0  # same tree already passed

    _, failures = run_checks()
    if failures:
        print(
            "Project checks failed. Fix them before finishing, or say why they cannot be fixed.\n\n"
            + format_failures(failures),
            file=sys.stderr,
        )
        return 2
    if state is not None and cache is not None:
        cache.write_text(state)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run project checks; print only failures.")
    parser.add_argument("--hook", action="store_true", help="Claude Code Stop-hook mode.")
    args = parser.parse_args()

    if args.hook:
        return hook_mode()

    count, failures = run_checks()
    if failures:
        print(format_failures(failures))
        print(f"\n{len(failures)} of {count} checks failed")
        return 1
    print(f"OK: {count} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
