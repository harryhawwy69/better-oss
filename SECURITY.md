# Security policy

## Reporting a vulnerability

Please report security problems **privately**, not in a public issue:

1. Open [a private security advisory](https://github.com/mobeloper/better-oss/security/advisories/new).
2. Describe what you found, how to reproduce it, and what you think it allows.

You can expect an acknowledgement as soon as the maintainer sees it, and a fix
or a plain explanation after that. This is a single-maintainer project, so
there is no guaranteed response time, but a report is never ignored.

## Supported versions

better-oss is pre-1.0. Only the latest release (and `main`) receives fixes.

## What is in scope

better-oss runs code on your machine, so the interesting problems are about
that code:

- **The hooks.** `core/voice_guard/check_voice.py` and
  `core/ship_gate/check_gate.py` run before Bash commands in Claude Code. They
  parse the command Claude is about to run, read files named in it, and run the
  commands in your `ship-manifest.md`. Command injection, path traversal, or any
  way to make a hook run something it should not is in scope.
- **The scripts.** `core/pr_monitor/monitor.py` and `core/init.py` shell out to
  `gh`, `git` and `claude`. The monitor is meant to be read-only on GitHub (its
  allowlist is `READONLY_GH` in `monitor.py`); a way around that is in scope.
- **The installer.** `cli/bin/better-oss.js` copies files and calls
  `claude plugin install`. It must never edit your Claude Code `settings.json`
  and must never overwrite your files without `--force`.
- **Leaked local data.** Committed files that contain a local path, a token, or
  another person's private data.

## What is out of scope

- Behavior of the `claude`, `gh` or `git` programs themselves.
- Model output quality (a skill grading an issue wrongly is a rubric bug; open a
  normal issue using the rubric-change form).
- Problems that need an attacker to already control your machine or your
  `~/.claude/better-oss/` folder.

## A note on trust

The ship manifest (`ship-manifest.md`) is a list of shell commands the
ship-gate runs for you. Only use manifests you wrote or have read, the same as
you would with a Makefile.
