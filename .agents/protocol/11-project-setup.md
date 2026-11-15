## Project Setup (Mandatory First Task)

Read this module when `.agents/context/project_profile.md` does not exist. Setup
runs once per project and designs the team of subagents the project needs.

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

## Team

- `agent-name` (area): what it owns in this project
```

### 3. Design the team

The agents in `.agents/agent-catalog/` are generic defaults, not finished
agents. Treat them as starting drafts: the project's team is designed from its
objective and tools, and every agent is rewritten for this project.

Core agents are always installed in `.claude/agents/`: `qa`, `security`,
`context-manager`. Tailor them too.

Drafts available in the catalog:

| Draft | Covers |
|---|---|
| `architect` | Module boundaries, integration plans, refactors |
| `backend` | Server-side code: APIs, services, business rules |
| `frontend-ui` | User interface |
| `database` | Schema, migrations, persisted data |
| `data-analytics` | Excel/CSV processing, transformations, metrics |
| `machine-learning` | Model training and evaluation |
| `ai-integrations` | AI APIs, prompts, automations |
| `devops` | Deployment, CI/CD, runtime environments |
| `innovation` | Improvement proposals |
| `ux-operational` | Critique of operator-facing workflows |

Steps:

1. From the objective and the tools, list the roles this project needs. Start
   from the work, not from the catalog: a role may match a draft, combine two,
   split one (for example `mobile` and `web` instead of `frontend-ui`), or be
   something the catalog does not have (for example `payments` or `game-design`).
   Keep the team as small as the project allows.
2. Group the roles into areas and decide who reviews whom. Show the user the
   proposed team - role, one-line purpose, model, area, reviewer - and wait for
   confirmation or changes.
3. Create each confirmed agent in `.claude/agents/`: copy the matching draft, or
   `.agents/agent-catalog/_template.md` when there is none. Then rewrite it for
   this project: the real stack, folders, and conventions in its `description`,
   responsibilities, and limits. Do not leave generic text. Pick the model by
   the judgment the role needs (opus for design and risk, sonnet for
   implementation, haiku for light routing). Leave the catalog untouched.
4. Rewrite `.agents/config/org.json` with this project's areas, agents, and
   review lines. Every installed agent must be in exactly one area.
5. Update the tables in `04-work-modes-activation.md` and `05-agent-roles.md` so
   they list exactly this project's roles: remove rows for roles the project
   does not have and add rows for the new ones.
6. Run `python3 .agents/planning/scripts/build_org.py`. Once the profile exists,
   the organization chart in `README.md` shows only this project's team.
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

When a task needs a role the team lacks, say so, create it the same way (draft
or `_template.md`, rewritten for the project) with the user's confirmation, add
it to `org.json`, regenerate the chart, and update `project_profile.md`. When
the objective or the tools change, update the profile and review the team.

---
