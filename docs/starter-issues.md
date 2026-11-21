# Starter issues (drafts)

Drafts of issues to create so first-time contributors have somewhere to start.
Create each one on GitHub with the labels shown, then **delete this file**. They
come from real gaps found while building the project.

---

### 1. Make the hooks run on Windows
Labels: `help wanted`, `hooks`, `installer`

`hooks/hooks.json` runs `python3 "${CLAUDE_PLUGIN_ROOT}/core/..."`. On a stock
Windows install the interpreter is usually `python` or `py`, so the hooks
probably cannot start. The ship-gate also runs manifest commands with
`shell=True` and builds paths for a POSIX shell.

Done when voice-guard and ship-gate both run on Windows (a documented launcher
or a fallback to `python`), tested on a Windows machine, with the setup
documented. Start by finding out what actually fails and reporting it here.

### 2. Add search-strategy examples for other languages
Labels: `good first issue`, `documentation`

`defaults/search-strategy.md` searches Python and TypeScript repos. Add
`examples/search-strategy-<language>.md` for a language you know (Go, Rust,
Java, ...): the same format, a handful of `gh search issues` queries, and
ranking filters.

Done when every query runs, each query has a comment naming the sentence of a
fit profile it comes from, and the file keeps the `{90_DAYS_AGO}` placeholder
instead of a fixed date.

### 3. Add a second worked example to `examples/`
Labels: `good first issue`, `documentation`

`examples/openmed-5295/` follows one real contribution through every stage. Add
one from a different repo or language, started from the files in
`defaults/templates/`. A run where a skill rejected the issue or the draft is as
useful as one that ended in a merge.

Done when it has the same files as the existing example (claim, repro, plan,
test evidence, PR draft, and the skills' outputs), no private data, and a short
note on what it teaches.

### 4. `shipped-recently` graded "pass" while quoting 122 days
Labels: `rubric`, `help wanted`, `skill:issue-scout`

Seen on 2026-11-21, running `issue-scout` on `pytorch/ignite#3940`. The
preferred check `shipped-recently` ("a release within the last 90 days") was
graded `pass` with the evidence "release v0.5.5 published 2026-07-22 (within 90
days of 2026-11-21? no: 122 days)". The model computed the right number and
still passed it.

Propose a wording change to the check (and the same check in `issue-select`)
that makes the arithmetic explicit: state the release date, compute today minus
that date, and pass only when the result is 90 or less. Use the rubric-change
form and include the before/after run.

### 5. Add a `doctor` command to the installer
Labels: `good first issue`, `installer`

`python3 core/init.py --check` prints whether `git`, `gh`, `claude` and the `gh`
login are in place, and `npx better-oss init` runs the same checks as part of
installing. Add `npx better-oss doctor`, which runs only the checks and exits
non-zero when something is missing.

Done when `doctor` changes nothing on disk, has a test in `cli/test/`, and is
mentioned in `cli/README.md`.

### 6. Make hooks clean up after themselves when Claude Code kills them
Labels: `help wanted`, `hooks`

Both hooks start a `claude -p` process. When a hook times out on its own, the
child is killed with it (`subprocess.run(..., timeout=...)`). But if the hook
process itself is killed from outside, for example when Claude Code ends a hook
at its timeout, the child is left running: a cut-short ship-gate run was seen
leaving a `claude -p` process with parent PID 1.

Done when a killed hook leaves no child process behind (for example by running
the child in its own process group and killing the group when the parent gets a
termination signal), with a test that shows it.

### 7. voice-guard: check comments posted through `gh api`
Labels: `help wanted`, `hooks`

The voice-guard only parses `gh issue comment|create` and `gh pr comment|create`.
A raw `gh api` POST to a comments endpoint walks around it (the honesty note in
`core/voice_guard/check_voice.py` says so). Handle the common `gh api` comment
forms, or make the hook stop an unparsable `gh api` write instead of passing it.

Done when the common comment POSTs are checked or stopped, plain `gh api` reads
still pass untouched, and the hook still fails closed.

### 8. A dev-only evaluation harness for one skill
Labels: `help wanted`, `rubric`

The skills have no automated tests: a rubric change is judged on manual before
and after runs. Design (in this issue, before any code) a small script that runs
one skill over a folder of frozen cases with expected verdicts and prints
agreement. It should live outside the plugin so users do not install it.

Done when the design is agreed here, and a first version works for one skill
with a handful of cases.
