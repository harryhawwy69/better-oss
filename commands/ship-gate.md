---
description: Run the ship-gate by hand on your branch: your repo's checks, then pr-precheck
allowed-tools: Bash(python3:*), Bash(git:*), Bash(gh:*), Read
argument-hint: --title "PR title" --body-file pr_draft.md
---

Run the ship-gate on the current branch of the clone I am in, without opening
a pull request. Run exactly this and report its output as it prints:

```
python3 "${CLAUDE_PLUGIN_ROOT}/core/ship_gate/check_gate.py" --branch $ARGUMENTS
```

If I gave no arguments, ask me for the PR title and the path of the
description file first (the gate needs both). Do not run `gh pr create`.

A pass lasts 30 minutes. Tell me that, and that opening the PR through Claude
Code with nothing changed lets it through without re-running.
