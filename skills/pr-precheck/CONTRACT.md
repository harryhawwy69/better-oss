# Contract: the fixed interface of pr-precheck

`pr-precheck` is called by people and by the ship-gate hook, so its
interface is fixed. You can change what the rubric and procedure say;
do not change the layout, the verdict space, or the output schema.

## The question

pr-precheck answers exactly one question about exactly one PR package:
**is this ready to submit?** A PR package is a candidate pull request
(title, description, commits, diff, test evidence), read against the
plan it claims to implement and the issue that plan belongs to. The
tool never answers a different question, never grades more than one
package per run, and never answers from gut feel: it executes the
components in this directory.

## The layout

Every file sits at exactly this path inside the skill directory:

    SKILL.md                     the frame: what the tool does, and how
    rubric.md                    the checks and the verdict rule
    procedure.md                 the operating steps
    scope.md                     where the tool may operate
    references/
      evidence-guide.md          where evidence lives in a PR package

The ship-gate inlines `SKILL.md`, `rubric.md`, `procedure.md`, and
`references/evidence-guide.md` from these exact paths; a file somewhere
else does not exist as far as the interface is concerned. Your voice
guide is not part of the skill: it lives in your personal folder
(`~/.claude/better-oss/voice-guide.md`).

## Inputs

Your own submission, checked before it goes out: your `plan.md`
(deviation notes included), the diff on your branch, your draft PR
title and description, and your test evidence, read against your issue.
Issue-side evidence comes from the real repo (the thread, the PR
template, the stated contribution policy).

## Verdict space

Binary: `accept` (ready to submit) or `reject` (hold). There is no
third verdict, no "accept with reservations", no score. Reservations
belong in check evidence lines, not in the verdict.

## Output

The tool's reply ends with a fenced JSON block, and nothing follows
it. The schema is fixed and may not be altered, extended, or
reordered:

```json
{
  "item": "<PR URL>",
  "checks": [
    {"name": "<check name>", "grade": "pass|fail|unclear",
     "evidence": "<one line: the fact or quote that decided it>"}
  ],
  "verdict": "accept|reject"
}
```

Callers parse the last fenced JSON block in the output. A readable
per-check summary may come before the block; the block is the
machine-read result and must be present, valid, and last.

## The scope seam

The tool reads `scope.md` before anything else. The scope names where
the PR may live and the rules of that environment; the tool refuses to
grade work outside the scoped repos. It never guesses a scope.

## The voice seam

The tool also reads your `voice-guide.md` and holds the outgoing PR
text, the title and the description, against those rules, reporting any
rule the draft breaks in the summary. The voice guide never changes the
verdict on its own unless the rubric has a check that reads it.

## The refusal rule

A tool with no rubric content or no procedure content refuses to grade
and says so, by design. An empty tool that invents checks at runtime is
worse than no tool, because its verdicts look like judgment and are
noise. Comments inside the files are guides, not content: only written
text counts.

## Grading discipline (contract terms)

These are interface guarantees, not style advice:

- **Evidence first.** No check is graded without naming the fact or
  quote that decided it. "Looks fine" is not evidence.
- **Grade the thing, not the polish.** A terse complete PR can be
  ready and a beautiful confident one can be hiding drift. Every check
  reads the artifact itself against the plan, the issue, and the
  stated standards, never the formatting.
- **The rubric decides, not the run.** If a check passes by its stated
  condition but feels wrong, it still passes; the fix belongs in the
  rubric, not in the run.
- **The procedure decides how, not the run.** The tool follows
  `procedure.md` as written and reports its gaps instead of silently
  inventing steps.
- **Unclear defaults to fail.** Treat `unclear` as the rubric's
  verdict rule directs; where the rule is silent, an unverifiable
  claim is a failing one. A PR you cannot verify from the package is a
  PR that is not ready to submit.
