# Ship manifest: example-org/example-lib

<!--
EXAMPLE: the shipped example ship manifest, prefilled for a fictional Python
repo. The ship-gate runs every command in the first table, in order, before
your pull request opens, and stops the PR if one fails. You choose the checks;
the ship-gate runs them. A manifest belongs to ONE repo: copy this file to the
root of your clone as ship-manifest.md and rewrite it. Keep it out of your PR
by adding it to the clone's exclude file:

  echo ship-manifest.md >> .git/info/exclude

1. Title. Replace example-org/example-lib above with the ORIGINAL repo's owner
   and name from your issue's link, not your fork.

2. First table. List the two to four checks the project asks you to run before
   a PR, usually its tests and lint. Take each one from the project instead of
   making one up, and write where you found it in the Source column:
   CONTRIBUTING.md, a CI file in .github/workflows/, or the Build and test
   commands in your CLAUDE.local.md. If the checks fail in a fresh terminal
   until a setup step runs (like `uv sync`, `.venv/bin/pip install -e ".[dev]"`,
   or `npm install`), make that step the first row.

3. Commands. The ship-gate runs each command in a fresh terminal at the top
   folder of your clone, without your virtual environment. Write the form that
   works there: `uv run pytest` if the project uses uv, `.venv/bin/pytest` if
   you made a virtual environment, `npx eslint .` for an npm project. To test
   one, open a new terminal, cd into your clone without activating anything,
   and run it.

4. Second table. A check that fails for a reason your fix does not touch goes
   here, with today's date and the reason. The usual reasons: it already fails
   on the default branch, it needs a tool or service you cannot run here, or it
   changes files when it runs (like a formatter) and would add them to your PR.
   Move a check here instead of deleting it, so pr-precheck can see what you
   skipped and why. If nothing goes here, leave the table empty.

If the project names no checks at all, write one row in the first table with
the command `none`, and say in Source where you looked.
-->

## Must pass before a ship

| Check | Command | Source |
|---|---|---|
| Install dev dependencies | `uv sync --frozen --extra dev` | CONTRIBUTING.md, "Setup" |
| Unit tests | `uv run pytest tests/unit -q` | CONTRIBUTING.md, "Running tests" |
| Lint | `uv run ruff check .` | .github/workflows/ci.yml, lint job |
| Format check | `uv run ruff format --check .` | .github/workflows/ci.yml, lint job |

## Excluded, with a dated reason

| Check | Command | Date | Why it doesn't count against this PR |
|---|---|---|---|
| Integration tests | `uv run pytest tests/integration -q` | 2026-01-15 | Needs a hosted service and an API key; also skipped on `main` in CI for forks |
