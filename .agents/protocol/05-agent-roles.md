## Agent Roles

Full role specifications live as Claude Code subagents in `.claude/agents/*.md`.
That directory is the single source of truth for each role's purpose, triggers,
rules, limitations, tools, and model. The main agent delegates to a subagent by
name (see the activation table in Work Modes); each subagent runs in its own
isolated context, so its work does not consume the main thread's tokens.

Do not duplicate role specifications here. Update the subagent file instead.

`qa`, `security`, and `context-manager` are core and always installed. The other
roles ship in `.agents/agent-catalog/` and are installed into `.claude/agents/`
by project setup (`11-project-setup.md`) according to the project's objective
and tools.

Role label (used in the activation table and in QA `review_agents`) → subagent:

| Role label | Subagent | Model | Installed |
|---|---|---|---|
| Architect | `architect` | opus | on setup |
| Backend | `backend` | sonnet | on setup |
| Database | `database` | opus | on setup |
| Data | `data-analytics` | sonnet | on setup |
| Machine Learning | `machine-learning` | opus | on setup |
| AI Integrations | `ai-integrations` | sonnet | on setup |
| Frontend | `frontend-ui` | sonnet | on setup |
| QA | `qa` | sonnet (opus for `Deep`) | core |
| Security | `security` | opus | core |
| DevOps | `devops` | sonnet | on setup |
| Context | `context-manager` | haiku | core |
| Innovation | `innovation` | haiku | on setup |
| (optional UI critic) | `ux-operational` | haiku | on setup |

---

Review governance (QA scheduling, non-negotiable triggers, proportionality, the
`other` rationale) lives in `.agents/protocol/13-review-governance.md`, read on
demand when performing QA.

---
