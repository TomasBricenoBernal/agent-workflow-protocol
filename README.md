# Project name

Describe your project here.

---

This repository uses the **Agent Workflow Protocol**: a low-token operating
protocol for coding agents (Claude Code, Codex, opencode). Everything it needs
lives in hidden folders so the root stays free for the project's code.

- Guide: [.agents/README.md](.agents/README.md)
- First session: tell the agent the project objective and the tools you will
  use; it installs the subagents and checks the project needs.
- Enable the git hook once per clone: `git config core.hooksPath .agents/hooks`
- Run all checks: `python .agents/planning/scripts/check.py`
