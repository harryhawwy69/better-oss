<!--
TEMPLATE: captured proof for your PR. pr-precheck reads it against your plan's
test plan. Paste real output, not summaries. Delete this comment.
-->

# Test evidence: <repo> #<issue number>

Run on <date>, <OS>, <runtime and version>. Branch `<branch>`, based on
`<default branch>` at `<commit>`.

## 1. Reproduction before the fix (default branch)

```text
$ <the plan's repro command>
<output>
```

## 2. Reproduction after the fix (this branch)

```text
$ <the same command>
<output>
```

## 3. The repo's own checks

```text
$ <test command>
<output>

$ <lint command>
<output>
```

Notes: anything unexpected (a failing check that also fails on the default
branch, a skipped test) and why it is unrelated.
