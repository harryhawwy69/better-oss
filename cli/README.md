# better-oss-cli

Installer for the [better-oss](https://github.com/mobeloper/better-oss) Claude
Code plugin: skills and guardrail hooks for making robust, reliable open
source contributions.

```sh
npx better-oss-cli init
```

`init` does three things, and changes nothing else:

1. **Checks** that `python3` (3.9+), `git`, `gh` (logged in) and `claude` are
   available, and says which are missing.
2. **Installs the plugin** with the `claude` CLI
   (`claude plugin install better-oss --marketplace mobeloper/better-oss`).
3. **Copies the example files** you are meant to make your own into
   `~/.claude/better-oss/`: `voice-guide.md`, `fit-profile.md`,
   `search-strategy.md` and `playbook.md`. Existing files are never
   overwritten unless you pass `--force`.

It never edits your Claude Code `settings.json`. If an older, hand-installed
copy of the voice-guard or ship-gate hook is registered there, it warns you,
because the plugin brings its own copies and each guard would run twice.

## Options

| Option | |
|---|---|
| `--home <dir>` | your better-oss folder (default: `$BETTER_OSS_HOME` or `~/.claude/better-oss`) |
| `--no-plugin` | only copy the example files; skip the plugin install |
| `--force` | overwrite your files with the shipped examples |
| `--dry-run` | show what would happen; change nothing |
| `--scope <scope>` | plugin scope: `user` (default), `project` or `local` |
| `--marketplace <src>` | where to install the plugin from (default `mobeloper/better-oss`; a git URL or local path also works) |

Without npm, run `/plugin install better-oss --marketplace mobeloper/better-oss`
inside Claude Code, then `/better-oss:init` to copy the example files.

Requires Node 18 or newer. No dependencies. 

Apache-2.0. Copyright Eric Michel
