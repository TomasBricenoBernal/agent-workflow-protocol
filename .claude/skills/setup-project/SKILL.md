---
name: setup-project
description: Run the mandatory project setup - ask the user for the project objective and tools, install and tailor the needed subagents from the catalog, configure the check commands, and write the project profile. Use when .agents/context/project_profile.md does not exist, or to add or remove subagents later.
---

# Project setup

Follow `.agents/protocol/11-project-setup.md` exactly; it is the single source
for this procedure. Read it now.

Before finishing:

1. Run `python3 .agents/planning/scripts/build_org.py` so the organization chart
   in `README.md` shows which agents are installed.
2. Run `python3 .agents/planning/scripts/check.py` and make it pass.
3. Tell the user to restart Claude Code so the new subagents register.
