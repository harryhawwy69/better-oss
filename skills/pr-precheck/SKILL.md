---
name: pr-precheck
description: Grade a PR package (a candidate pull request read against the plan it claims to implement and the issue that plan belongs to) and decide whether it is ready to submit. Use when checking your own branch, draft PR title, and description before opening the pull request.
---

# pr-precheck: rubric-driven PR grading

The frontmatter above and the section headings below are fixed
(`CONTRACT.md`'s layout rule); the instructions under each heading are
yours to tune.

## The question

You are grading one PR package to answer a single question: is this
ready to submit? A package is a candidate pull request (its title,
description, commits, diff, and test evidence), read against the plan
it claims to implement and the issue that plan belongs to. Grade
exactly one package per run. Never answer a different question (not
"is this a good idea?", not "is the plan good?", not "is the code
elegant?"), and never answer from gut feel: you answer by executing
`procedure.md`, which applies `rubric.md` to evidence gathered per
`references/evidence-guide.md`.

## Inputs

Your own submission, checked before it goes out. If you have no drafts
yet, the shape to start from is in the plugin's `defaults/templates/`
(`plan.md`, `pr-draft.md`, `test-evidence.md`). Inputs and where each
comes from:

- `plan.md`, including its deviation notes, from your working copy. A
  deviation recorded in the plan is part of the plan and is graded
  against; a deviation that exists only in the diff is not recorded.
- The branch's diff: everything the branch changes relative to the
  repo's default branch. Produce it with `git diff main...HEAD`
  (three dots), run from the working copy; use the repo's actual
  default branch name if it is not `main`.
- The draft PR title and description, as you supply them (a file or
  pasted text). The commits come from `git log main..HEAD`.
- The test evidence: the test output or run notes you supply or quote
  in the description.
- The issue: gather issue-side evidence from the real repo (the
  thread, the PR template, the stated contribution policy) via
  `gh`, the GitHub API, or the web; `references/evidence-guide.md`
  says where each signal lives.

If the pull request is already open, use its URL as `item`, read the
live title and description with `gh pr view`, and read the diff with
`gh pr diff` (or `git diff` against the PR's base branch); grade it the
same way, and say in the summary that the PR was already open.

Read the package the way a maintainer will read the PR: it is what
the diff, the title, and the description contain and quote, not other
files in the working directory.

## The scope seam

Read `scope.md` before anything else, before reading any other input.
It names where the PR may live and the rules of that environment; apply
those rules when reading evidence. Refuse to grade a PR that lives
outside the scoped repos. Never guess a scope.

## The voice seam

After the scope check, read `voice-guide.md`: your own rules for how
you write upstream. Your personal files live in `~/.claude/better-oss/`
(or `$BETTER_OSS_HOME`); if `voice-guide.md` is missing there, read the
shipped example in the plugin's `defaults/` folder. Hold the outgoing PR
text, the title and the description, against those rules. Report each
rule the draft breaks in the readable summary, quoting the rule and the
offending text. The voice guide never changes the verdict on its own,
because voice is personal; it moves the verdict only if `rubric.md` has
a check that reads it.

## Component reads

Read these components and keep their roles separate:

- `rubric.md` defines the checks (each with its evidence, pass
  condition, and weight) and the verdict rule that combines check
  grades into `accept` or `reject`.
- `references/evidence-guide.md` maps where each evidence family
  lives in a PR package and on GitHub and what good looks like there.
- `procedure.md` is the operating procedure: the read order, how each
  evidence family is gathered, how a check executes, and how grades
  become the verdict. Execute it exactly as written.

Where the procedure is silent on a step, do not invent one: note the
gap in your readable summary, because a procedure gap is feedback you
need. If `rubric.md` has no checks written, or `procedure.md` has no
steps written (comments and template text do not count), stop and say
so: this tool refuses to grade without a rubric AND a procedure, by
design. Never invent checks at runtime.

## Verdict and output

The verdict is binary: `accept` (ready to submit) or `reject` (hold).
There is no third verdict, no "accept with reservations", and no
score; put reservations in the check evidence lines. Assemble the
verdict only as `rubric.md`'s verdict rule directs. Before the JSON
block you may show a short readable summary (a line per check, plus
voice-guide notes and procedure gaps). End your reply with the fenced
JSON block below, valid, last, with nothing after it. Use the PR URL as
`item`. Do not alter, extend, or reorder the schema.

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

## Grading discipline

- Evidence first: never grade a check without naming the fact or
  quote that decided it. "Looks fine" is not evidence.
- Grade the thing, not the polish: a terse complete PR can be ready
  and a beautiful confident one can be hiding drift. Read the diff,
  tests, and claims against the plan and the issue, never the
  formatting.
- The rubric decides, not you: if a check passes by its stated
  condition but feels wrong, it still passes. Note the tension in the
  summary if you want; the fix belongs in the rubric, not in the run.
- The procedure decides how, not you: follow `procedure.md` as
  written and report its gaps instead of papering over them.
- Treat `unclear` as the rubric's verdict rule directs. If the rule
  is silent, treat `unclear` as `fail`: a PR you cannot verify from
  the package is a PR that is not ready to submit.
