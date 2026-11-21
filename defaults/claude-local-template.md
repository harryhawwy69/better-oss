<!--
EXAMPLE: a filled repo-memory file for a fictional repo, showing the shape.
Copy it to the root of YOUR CLONE of the target repo as CLAUDE.local.md and
rewrite it. CLAUDE.local.md is Claude Code's documented personal memory file:
it is loaded into every session you run in that repo, next to any CLAUDE.md
the repo itself ships, and it is never checked in. It pays for orientation
once and reads it back free.

STEP 0, before you write anything: check what the repo already ships.

  - A root CLAUDE.md: the maintainers' own conventions. Claude Code loads it
    next to this file automatically. Read it; do not duplicate it here.
  - A root AGENTS.md: also the maintainers' conventions, but Claude Code does
    not read AGENTS.md natively. Keep the @AGENTS.md import below as this
    file's first content line.
  - Both: the CLAUDE.md already loads and the two are usually near-twins;
    delete the import line rather than loading the same text twice.
  - Neither: delete the import line.

  Either way, read the repo's CONTRIBUTING.md end to end first. It is the
  source for the conventions section, and you are held to it whether you read
  it or not.

SIZE DISCIPLINE. This file loads into every session in the repo, so it is a
cache of distilled conclusions, not a filing cabinet: aim for under about 60
lines of your own content, and delete this whole comment when you are done.

SCOPED ORIENTATION, once, after reading CONTRIBUTING.md: run one agent over
ONLY the subsystem your issue touches (the directory, its key files, how they
connect, where the tests live). Never map the whole repo: you are fixing one
issue, not writing a guidebook. Distill the result into the subsystem section
below. A prompt that works, from the clone root:

  claude "Read only <the folder your issue touches>. Tell me where <the
  behavior in my issue> lives, the 2-4 files that matter, how they connect,
  and where their tests are."

KEEP IT OUT OF YOUR PR DIFF. You cannot add ignore rules to a stranger's
.gitignore. The local mechanism is .git/info/exclude (works like .gitignore,
never leaves your clone). From the clone root:

  echo CLAUDE.local.md >> .git/info/exclude

Then run `git status`: the file should not appear.
-->

@AGENTS.md

<!-- ^ Keep this line only if the repo ships a root AGENTS.md. -->

# My notes on example-org/example-lib (local, never committed)

Issue #123 (`parse_config` crashes on an empty file), claimed 2026-01-15.

## Conventions from CONTRIBUTING.md

- One PR per issue, branched from `main`, named `fix/<issue>-<slug>`.
- PRs need a test and a CHANGELOG line under "Unreleased" when behavior changes.
- Keep PRs under about 400 changed lines; larger changes need a design issue first.
- Commit messages are imperative and prefixed (`fix:`, `test:`, `docs:`).

## The subsystem my issue touches

- `src/example_lib/config.py`: `parse_config()` reads the file and builds the
  `Config` object; the crash is in `_load_sections()`.
- `src/example_lib/errors.py`: where the `ConfigError` types live.
- Tests: `tests/unit/test_config.py`, with fixtures in `tests/fixtures/config/`.

## Build and test commands

```text
uv sync --frozen --extra dev
uv run pytest tests/unit/test_config.py -q
uv run ruff check . && uv run ruff format --check .
```

## House style and stated AI policy

- Type hints required on public functions; docstrings in Google style.
- AI policy (CONTRIBUTING.md, verbatim): "AI-assisted contributions are welcome
  if you disclose the tool and how it was used in the PR description."
  If a repo states no policy, write "none stated" and disclose honestly anyway,
  in your own words.
