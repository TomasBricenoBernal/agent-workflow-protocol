## Token Budget

Default: Low.

### Low

- Max 3 context files.
- Max 2 source files read in full; beyond that, read only targeted slices.
- Before changing a function, type, route, or schema, search for its usages and read the matching slices. A search is cheap; breaking a caller you never saw is not.
- No open-ended exploration.

### Medium

- Max 5 context files.
- Max 5 source files.

### High

Only for architecture, security, database design, major refactors, or complex bugs.

Explain why broader context is needed.

## Token Consumption Strategy

Use these rules to reduce token usage without losing correctness:

- Read in layers: task file first, compact context second, source files last.
- Read slices before full files when headings or targeted sections are enough.
- Activate the fewest agents possible for the current step.
- Delay QA, Security, and DevOps until their trigger conditions are present.
- Prefer updating reusable context files over re-explaining the same state in every task.
- Summarize decisions once in canonical files instead of duplicating them across notes.
- Escalate from `Low` to `Medium` or `High` only when the task risk truly requires it.
- If broader context is used, record why in the task notes or plan.
- Keep agent outputs short and structured; prefer templates and checklists over free-form text.
- Break multi-surface work into smaller tasks so each agent reads less context.

---
