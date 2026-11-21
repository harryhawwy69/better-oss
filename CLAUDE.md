@AGENTS.md

# Claude Code notes

- Use plan mode before changing a rubric (`skills/*/rubric.md`) or a procedure:
  these change what the tools decide, so agree the before/after case first.
- Dev loop: `claude --plugin-dir .`, edit, then `/reload-plugins`.
- Do not run `gh pr create`, `gh issue comment` or any other command that posts
  to GitHub unless asked; the hooks in this repo will stop a draft that breaks
  the voice guide, and that is the intended behavior.
- When a skill run is part of the work, run it read-only and say what it
  graded; do not paste its output into a comment as if it were your own words.
