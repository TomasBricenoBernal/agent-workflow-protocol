## Project Setup (Mandatory First Task)

Read this module when `.agents/context/project_profile.md` does not exist. Setup
runs once per project and decides which subagents the project actually needs.

### 1. Ask the user

Ask, in one message, and wait for the answers. Do not guess them from the
repository and do not start other work meanwhile:

1. **Objective** — what the project must achieve and for whom.
2. **Tools** — languages, frameworks, database, hosting/deployment, external
   services or AI APIs, and any tool already decided.
3. **Constraints** (optional) — deadlines, team size, things to avoid.

If an answer is too vague to choose agents, ask one follow-up question.

### 2. Record the profile

Create `.agents/context/project_profile.md`:

```markdown
# Project Profile

- `status`: `Configured`
- `configured_on`: `YYYY-MM-DD`
- `objective`: one or two sentences, in the user's words
- `tools`: comma-separated stack
- `constraints`: or `None`

## Installed Agents

- `agent-name`: why this project needs it

## Not Installed

- `agent-name`: why it is not needed yet
```

### 3. Install the agents

Core agents are always installed in `.claude/agents/`: `qa`, `security`,
`context-manager`. Optional agents live in `.agents/agent-catalog/` and are
inert until copied.

| Catalog agent | Install when the project has |
|---|---|
| `architect` | Several modules or services, or a non-trivial design to plan |
| `backend` | Server-side code: APIs, services, business rules |
| `frontend-ui` | A user interface |
| `database` | A database, migrations, or persisted data |
| `data-analytics` | Excel/CSV processing, transformations, or metrics |
| `machine-learning` | Model training or evaluation |
| `ai-integrations` | AI APIs, prompts, or automations |
| `devops` | Deployment, CI/CD, or runtime environments to manage |
| `innovation` | A user who wants improvement proposals |
| `ux-operational` | Operator-facing workflows worth critiquing |

Steps:

1. Propose the list of agents to install with a one-line reason each, and wait
   for the user's confirmation.
2. Copy each confirmed agent from `.agents/agent-catalog/` to `.claude/agents/`.
   Leave the catalog intact so agents can be added later.
3. Tailor each installed agent to the stated tools: name the real stack in its
   `description` and rules (for example the framework, ORM, or test runner).
   Keep the file's structure and limits.
4. If the project needs a role the catalog lacks, create a new subagent file
   following the same structure, and add it to the role map in
   `05-agent-roles.md`.
5. In `04-work-modes-activation.md` and `05-agent-roles.md`, delete the table
   rows for roles that were not installed, so the always-on protocol only
   describes this project. Re-add a row when its agent is installed later.
6. Run `python3 .agents/planning/scripts/build_org.py` so the organization chart
   shows the installed agents. A new role must also be added to an area in
   `.agents/config/org.json`.
7. Tell the user to restart Claude Code so the new subagents register.

### 4. Configure verification

Write the project's check commands to `.agents/config/checks.json`, one entry per
tool the stack really has (lint, type check, tests, build), and confirm them
with the user:

```json
{
  "require_project_profile": true,
  "commands": [
    {"name": "lint", "run": "npm run lint"},
    {"name": "tests", "run": "npm test"}
  ]
}
```

- Set `require_project_profile` to `true`.
- Keep the template's `script-tests` entry while `.agents/planning/scripts/` is in use.
- If the project has no test runner yet, propose one; the test-first rule needs it.
- Add the toolchain install step to `.github/workflows/checks.yml`.
- Run `python3 .agents/planning/scripts/check.py` and make it pass before closing setup.

### 5. Close setup

- Track setup as a normal task (`{id}-project-setup`) with QA depth `Light`.
- Update `.agents/context/current_state.md` with the objective and stack.
- Point `.agents/planning/tasks/active_task.md` at the next task.

### Later changes

When a task needs a role that is not installed, say so, install it from the
catalog with the user's confirmation, and update `project_profile.md`. When the
objective or the tools change, update the profile and review the installed set.

---
