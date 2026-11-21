# AGENTS.md

Guidance for AI coding agents (and people) working in this repository.

## What this repo is

`better-oss` is a Claude Code plugin plus a small npx installer. It helps a
contributor find, claim, plan and ship a pull request to someone else's open
source repo, and holds each draft to a written rubric before it goes out. A
human posts everything; the tools only grade and draft.

Pipeline: `issue-scout` -> `issue-select` -> `repro-check` -> `plan-check` ->
`pr-precheck`, plus two hooks (voice-guard, ship-gate) and a read-only
`pr-monitor`.

## Layout

- `skills/<name>/`: one skill each: `SKILL.md`, `rubric.md`, `scope.md`,
  `references/evidence-guide.md` (plus `procedure.md` / `CONTRACT.md` where present).
- `core/`: stdlib-only Python. `paths.py` (where code vs. user files live),
  `voice_guard/`, `ship_gate/`, `pr_monitor/`, `init.py`.
- `hooks/hooks.json` and `commands/`: plugin wiring.
- `defaults/`: prefilled example files users copy and rewrite. `examples/`: a real worked run.
- `cli/`: the npx installer (Node 18+, no dependencies).
- User files live in `~/.claude/better-oss/` (or `$BETTER_OSS_HOME`), never in the plugin folder.

## Commands to run before a PR

```text
ruff check .                          # Python lint (targets Python 3.9)
python3 -m pytest                     # scripts, hooks, skills, docs (no model calls)
python3 scripts/leak_check.py         # no home paths, emails, tokens or symlinks
cd cli && npm test                    # installer tests (node --test)
claude plugin validate .              # plugin manifest
claude plugin validate skills         # skill files
python3 core/init.py --check          # prerequisites on your machine
```

Try a change for real: `claude --plugin-dir .`, then `/reload-plugins` after edits.
Run hooks directly by piping JSON, with an empty `BETTER_OSS_HOME` so your own
files are not read:

```text
echo '{"tool_name":"Bash","tool_input":{"command":"gh issue comment 1 --web"},"cwd":"."}' \
  | BETTER_OSS_HOME=$(mktemp -d) python3 core/voice_guard/check_voice.py   # exits 2
```

To test an install, set `CLAUDE_CONFIG_DIR` to an empty folder so your real
Claude config is untouched.

## Conventions

- Commit messages: `[add] ...`, `[update] ...`, `[fix] ...`; one logical change per commit.
- Python 3.9+, standard library only. Add no dependency without an issue first.
- Keep the `SKILL.md` frontmatter (`name`, `description`) and the `pr-precheck`
  file layout in `skills/pr-precheck/CONTRACT.md`: the ship-gate reads those paths.

## Hard rules

- **Live mode only.** The tools work on real repos: keep practice-repo scopes, eval-only
  files, and tutorial-specific wording out.
- **The Sonnet pin is deliberate.** The rubrics were tuned and checked on Sonnet.
  Do not add a model flag or swap the model without evidence it still grades the same.
- **Rubric changes need evidence.** Show a before/after verdict on a real case in the PR.
  Only change check names, pass conditions, or the verdict rule on purpose.
- **`defaults/` stay prefilled** and keep their `EXAMPLE:` banner comment.
- **No symlinks, home-directory paths, emails, or tokens** in committed files.
- **Never write to a user's `~/.claude` from the code** except through `core/init.py`
  and the installer, and never edit their `settings.json`.
- **The monitor never posts.** Keep its `READONLY_GH` allowlist as is.

## AI use

If AI helped with a change, say how in the PR description, in your own words,
as `pr-precheck` itself asks of the people who use it. Do not commit, push or
open a PR unless the person you are working for asked you to.
