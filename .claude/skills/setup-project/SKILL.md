---
name: setup-project
description: Run the mandatory project setup - ask the user for the project objective and tools, design the project's team of subagents (rewriting catalog drafts or creating new roles), redraw the organization chart, configure the check commands, and write the project profile. Use when .agents/context/project_profile.md does not exist, or to add, change, or remove subagents later.
---

# Project setup

Follow `.agents/protocol/11-project-setup.md` exactly; it is the single source
for this procedure. Read it now.

Before finishing:

1. Run `python3 .agents/planning/scripts/build_org.py` so the organization chart
   in `README.md` shows only this project's team.
2. Run `python3 .agents/planning/scripts/check.py` and make it pass.
3. Tell the user to restart Claude Code so the new subagents register.
