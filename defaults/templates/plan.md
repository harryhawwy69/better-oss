<!--
TEMPLATE: copy to plan.md in your working folder and fill it in. plan-check
and pr-precheck read it by role, not by exact heading, so you can rename
sections, but every role below must be present. Delete this comment.
-->

# Plan: <repo> #<issue number>, <issue title>

## Diagnosis

What causes the behavior, and the evidence that supports it (a repro step,
a line of code, a log). If you have not verified the cause, say it is a
hypothesis.

## Scope

- **In scope:** what this change does, and why.
- **Not in scope:** what you will deliberately leave alone, including
  anything someone might be tempted to change while they are there.

## Files I will touch

- `path/to/file.ext`: what changes and why
- `tests/path/to/test_file.ext`: the test you add or extend

(If exact files are not known yet, name the module or code path, and say the
exact functions will be pinned after tracing.)

## Approach

Numbered, concrete steps. Each one names a file or function and an action,
not "improve handling". Keep the whole change small (under about 500 lines).

1.
2.
3.

## Test plan

The decisive test: a new or extended automated test (say where it goes), or,
if automation is not practical, a repeatable check from your repro steps with
an observable result that would differ on the unfixed code. "Run the full
suite" is not a test for this fix.

## Deviations

Record every change from this plan as it happens: what changed and why. A
deviation recorded here is honest work; a deviation that only exists in the
diff is silent drift.
