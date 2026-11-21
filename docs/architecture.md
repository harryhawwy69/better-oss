# Architecture

How better-oss is put together, and why. For how to use it, see the
[README](../README.md).

## Two kinds of files, kept apart

```text
the plugin (replaced on every update)        your folder (never touched by updates)
~/.claude/plugins/.../better-oss/            ~/.claude/better-oss/   (or $BETTER_OSS_HOME)
  skills/    the five rubrics                  voice-guide.md   fit-profile.md
  core/      hooks + scripts                   search-strategy.md   playbook.md
  defaults/  shipped examples  --copied-->     guard-log.md  gate-log.md  monitor-log.md
  hooks/  commands/                            run-report.md  drafted-move.md
```

`core/paths.py` is the one place that knows this split. Everything resolves a
personal file with `paths.user_file(name)`: your copy if it exists, otherwise the
shipped example in `defaults/`. That is why a fresh install works before you
have written anything, and why an update can never overwrite your voice guide.

Every shipped example opens with an `EXAMPLE:` comment. While that comment is
still in a file, the tools say so in their output. Delete it when the file is
yours.

## The skills

A skill is a folder of plain markdown that Claude Code loads on demand:

| File | Role |
|---|---|
| `SKILL.md` | The frame: what to read, in what order, what to refuse, what to output. |
| `rubric.md` | The judgment: a table of checks (evidence, pass condition, weight) and a verdict rule. |
| `scope.md` | The field of view: which repos or issues are in play, and the rules for working there. |
| `references/evidence-guide.md` | Where each kind of proof lives, and what good looks like there. |
| `procedure.md` | (`plan-check`, `pr-precheck`) The step-by-step operating procedure. |
| `CONTRACT.md` | (`pr-precheck`) The fixed interface the ship-gate depends on. |

The separation matters. The **rubric decides**, the **procedure decides how**,
the **evidence guide says where**, and the model executes them. When a grade is
wrong, the fix is in the rubric, not in the run. Every skill ends with the same
JSON block (`item`, `checks`, `verdict`), where each check has a
`pass | fail | unclear` grade and a one-line piece of evidence. The verdict is
binary: `accept` or `reject`. `unclear` counts as a fail.

The skills never post anything. They read GitHub through `gh`, read your drafts,
and report.

## The hooks

Both hooks are `PreToolUse` hooks on the `Bash` tool, registered in
`hooks/hooks.json`. Claude Code runs them with the tool call as JSON on stdin
before the command executes; exit code 2 blocks the command and shows the
hook's message.

**voice-guard** (`core/voice_guard/check_voice.py`) finds outgoing
`gh issue|pr comment|create` commands, extracts the body (from `--body` or
`--body-file`), and makes one small Sonnet call that holds the body against your
voice guide. It returns `pass`, or `stop` quoting the rule and the offending
line. Commands that send nothing pass through at no cost. It can also be run by
hand on a draft file (`--draft FILE`) for comments you will post from the
browser.

**ship-gate** (`core/ship_gate/check_gate.py`) finds `gh pr create`, then:

1. reads `ship-manifest.md` from the clone and runs each check in a fresh
   shell, stopping at the first failure;
2. gathers the diff, plan, test evidence, PR template, contributing docs and
   issue thread;
3. runs the `pr-precheck` skill on all of it (one Sonnet call) and blocks unless
   the verdict is `accept`.

A pass by hand lasts 30 minutes. Fingerprints of the commit, base, title,
description, manifest, plan and evidence are logged, so opening the PR within
the window with nothing changed lets it through without re-running. Through
the hook the run stops itself at 29 minutes, because Claude Code ends a hook at
30 and an ended hook lets the command through.

Both hooks **fail closed**. Claude Code only blocks on exit 2, and a crash exits
1, so every unexpected error is caught and turned into a stop. Both are also
honest about their reach: they only see commands that go through Claude Code. A
PR opened in the browser skips them, the same as not running a skill.

**pr-monitor** (`core/pr_monitor/monitor.py`) is a script you run, not a hook.
It reads your PR through an allowlist of read-only `gh` calls
(`READONLY_GH`; anything else is refused in code), classifies its state, and
makes one Sonnet call that drafts the matching move from your `playbook.md` and
`move-forms.md`. Two answers are free because there is nothing to draft: "no PR
yet" and "nothing new since the last run".

## The installer and the plugin

`cli/` is a tiny Node program (no dependencies). `npx better-oss-cli init` checks
prerequisites, runs `claude plugin install better-oss --marketplace
mobeloper/better-oss`, and copies the four personal example files into your
folder without overwriting. It never edits `settings.json`; the plugin's hooks
come with the plugin itself. `core/init.py` (behind `/better-oss:init`) does the
file copying for people who installed through the plugin directly, and the two
file lists are kept in sync by a test.

## Why these choices

- **Markdown rubrics, not code.** The judgment is meant to be read, argued with
  and changed by the people it affects. A check you cannot read is a check you
  cannot trust.
- **Pinned model.** Pass bars only mean something against the model the rubrics
  were tuned on, so the model is a constant (`MODEL = "sonnet"`), not a setting.
- **Grade, do not act.** Posting is the one thing that cannot be taken back, so
  it stays with the human, and the two guards sit exactly on the commands that
  post.
- **Standard library only.** The Python needs nothing installed beyond Python
  3.9+; the installer needs nothing beyond Node 18+. Fewer moving parts, and
  nothing to audit in a tool that runs shell commands on your machine.
