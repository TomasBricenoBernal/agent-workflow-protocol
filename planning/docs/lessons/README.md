# Lessons

One file per area (`backend.md`, `database.md`, `frontend.md`, ...), created only
when the first lesson for that area appears.

A lesson is a mistake that already happened and the rule that prevents it. QA
adds one when a finding could repeat. Read the file for an area before working
in it, if the file exists.

Rules:

- One line per lesson: `- <rule> — because <what went wrong> (task <id>)`.
- At most 15 lessons per file. When full, merge or drop the least useful one.
- If a lesson can be enforced by a test or a lint rule, add the check to
  `.agents/config/checks.json` and delete the lesson.
