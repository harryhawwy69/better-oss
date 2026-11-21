---
description: Read your open pull request and draft your next move (a review reply, a nudge, or a wait note)
allowed-tools: Bash(python3:*), Bash(gh:*), Bash(git:*), Read
argument-hint: "[--state]"
---

Run the PR monitor from the clone I am in, on my PR's branch, and report its
output as it prints:

```
python3 "${CLAUDE_PLUGIN_ROOT}/core/pr_monitor/monitor.py" $ARGUMENTS
```

`--state` prints the state for free, with no model call. A full run drafts the
matching move into `drafted-move.md` in my better-oss folder. The monitor never
posts: tell me the draft is a draft, and that I should rewrite it in my own
words and post it through Claude Code so the voice-guard hook checks it.
