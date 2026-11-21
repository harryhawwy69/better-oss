---
description: Set up your better-oss folder (voice guide, fit profile, search strategy, playbook) and check prerequisites
allowed-tools: Bash(python3:*)
argument-hint: "[--force | --check]"
---

Run the better-oss setup script and report its output as it prints, without
paraphrasing the file list or the prerequisite lines:

```
python3 "${CLAUDE_PLUGIN_ROOT}/core/init.py" $ARGUMENTS
```

If a prerequisite is reported MISSING, say how to fix it in one line. Then
remind me that the copied files are EXAMPLES I should rewrite, starting with
`voice-guide.md`, because the voice-guard hook enforces it on my outgoing
comments.
