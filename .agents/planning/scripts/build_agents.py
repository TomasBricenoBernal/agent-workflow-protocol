#!/usr/bin/env python3
"""Flatten .agents/protocol/*.md into AGENTS.md.

`CLAUDE.md` stays modular: it uses `@import`, which Claude Code expands at load
time. Codex and opencode read `AGENTS.md` as plain text and do not expand
imports, so this script inlines the always-on protocol modules into `AGENTS.md`.

The always-on set is whatever `CLAUDE.md` imports, so both entry files carry the
same modules. On-demand modules are left out; `01-foundations.md` lists them and
says when to read each one.

Run after editing any protocol module:

    python .agents/planning/scripts/build_agents.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL_DIR = ROOT / ".agents" / "protocol"
OUTPUT = ROOT / "AGENTS.md"
INDEX = ROOT / ".claude" / "CLAUDE.md"
IMPORT_RE = re.compile(r"^@\.\./\.agents/protocol/([\w.-]+\.md)\s*$", re.MULTILINE)

HEADER = """# AGENTS.md

<!-- GENERATED FILE - do not edit by hand.
     Source of truth: .agents/protocol/*.md
     Regenerate:      python .agents/planning/scripts/build_agents.py
     CLAUDE.md stays modular via @import (Claude Code expands it). This file is
     the flattened protocol for tools that read AGENTS.md as plain text
     (Codex, opencode). -->

This is the global protocol for this repository, flattened from
`.agents/protocol/` so any tool that reads `AGENTS.md` as plain text receives the
always-on content. On-demand modules stay in `.agents/protocol/` and are read
only when a task matches (see "On-Demand Modules" below). To change a rule, edit the relevant module under
`.agents/protocol/` and regenerate this file."""


def always_on_modules() -> list:
    names = IMPORT_RE.findall(INDEX.read_text(encoding="utf-8"))
    if not names:
        raise SystemExit(f"No protocol imports found in {INDEX}")
    modules = [PROTOCOL_DIR / name for name in names]
    missing = [m.name for m in modules if not m.exists()]
    if missing:
        raise SystemExit(f"`.claude/CLAUDE.md` imports missing modules: {', '.join(missing)}")
    return modules


def render(modules: list) -> str:
    parts = [HEADER]
    for module in modules:
        parts.append(module.read_text(encoding="utf-8").strip())
    return "\n\n".join(parts) + "\n"


def main() -> int:
    modules = always_on_modules()
    OUTPUT.write_text(render(modules), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} from {len(modules)} modules:")
    for module in modules:
        print(f"  - {module.name}")
    skipped = sorted(set(PROTOCOL_DIR.glob("*.md")) - set(modules))
    if skipped:
        print("On-demand (not inlined): " + ", ".join(m.name for m in skipped))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
