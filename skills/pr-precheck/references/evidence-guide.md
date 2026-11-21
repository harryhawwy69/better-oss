# Evidence guide: where evidence lives in a PR package

This is the map `pr-precheck` uses. For every kind of evidence a rubric
check names, it says where to find it in a PR package and what good
looks like there. The four families below map to the ways a PR gets
submitted too early: plan fidelity (silent drift), test evidence (not
tested), diff quality (unreviewable), and standards and comms (the
repo's stated asks ignored). A package that fails none of them is ready.

A rubric check whose evidence this guide cannot locate is a check
nobody else can execute. If you add a check, add its map entry here.

Where things live in your working copy and on GitHub:

- the plan: `plan.md` and its `## Deviations` section;
- the change: `git diff main...HEAD` (three dots, from the working
  copy; use the repo's real default branch name) and `git log main..HEAD`;
- the claims: your draft PR title and description (`pr_draft.md`);
- the proof: your captured test output (`test_evidence.md`);
- the repo's asks: `.github/PULL_REQUEST_TEMPLATE.md`, `CONTRIBUTING.md`,
  any AI-policy file, and the issue thread.

## Plan fidelity (silent drift)

**Where it lives**

The plan is `plan.md`: its files, its scope (In scope / Not in scope),
its approach, and its `## Deviations`, which is where a recorded change
from the plan lives. Plan headings are not standard: match sections by
the role they play, not the label, as the shipped `plan.md` template
names them. The change is the output of
`git diff main...HEAD`; the files it touches are the `--- a/...`
headers, and `git diff main...HEAD --stat` gives the file list. The
claims to test are in the draft description (Summary, Changes bullets,
any "implements the plan exactly" line, any checklist) and in the
commits.

**What good looks like**

- Every file in the diff's headers is a file the plan names, or is
  named in a deviation note. Every planned file and step shows up in
  the diff, or its omission is disclosed. Example: a plan names one
  statement printer, its tests, and a changelog, but the diff also
  rewrites an unrelated property printer that the plan never mentions
  and its `Not in scope` rules out. That is silent drift, and a
  description claiming "no changes beyond the plan" contradicts the
  diff.
- Silent drift runs both ways: more than the plan (an extra file, a new
  option, a rewrite) or less (a planned step missing) with no deviation
  note or disclosure. An honest deviation re-ties the mismatch: a
  change recorded in `plan.md` under `## Deviations`, or disclosed in
  the description, is not drift. A deviation that exists only in the
  diff is.
- Each description claim is true of the diff, and every behavior change
  in the diff is described. The description's fidelity claims count
  here: "implements the plan exactly" is a claim checked against the
  file list, not a comms nicety.
- A small gap between plan wording and diff (a branch name, a few lines
  of difference in size) is not drift when the behavior and the files
  match. A branch rename recorded under Deviations is honest and
  passes.

## Test evidence (not tested)

**Where it lives**

The proof is `test_evidence.md` (the repro re-run before and after, plus
the output of the repo's own checks), echoed in the Testing section of
the draft description. It is read against the plan's `## Test plan` and
the repro steps it quotes, and against the checks listed in the repo's
`.github/PULL_REQUEST_TEMPLATE.md` and contributing docs. A new test is
in the branch's diff.

**What good looks like**

- Decisive evidence shows an observable result that would differ
  without the fix: a before and an after output for the repro, or a new
  test that fails on the old code and passes on the new. It names the
  behavior and states the expected value (for example, the issue's
  input run before and after, with the after matching the expected
  output byte for byte).
- The evidence exercises the path the diff changes. Output from code the
  diff does not touch proves nothing.
- Every check the template or docs ask for appears with its result
  pasted, or its absence is explained (for example, a test target
  printing "no tests ran", pasted as is). A failing check reported with
  the reason still counts as evidence; a hidden one does not. An
  unticked CI box before the PR is open is not a gap. A ticked box the
  evidence contradicts is.
- Not decisive: "tested locally", "tests pass", "works now", an after
  with no before, or a suite run with nothing named. Record the quote
  and mark it as no observable result.
- Read each check's output as the repo prints it. Know the tool's own
  vocabulary: for example, in pytest an `xfailed` count is expected
  failures and not a failure, while a `failed`, `error`, or
  `XPASS(strict)` line is one; a runner that exits non-zero because the
  repo has no tests of that kind ("no tests ran") is not a hidden
  failure. A check whose exit line is blank is read from its own output
  lines.
- When a checkbox claims something about the diff (a marker or skip
  removed, a snapshot updated), read the claim against the diff itself.
  A `grep` that finds nothing does not show whether a line was removed;
  the proof is the diff deleting it. If the diff does not show it while
  the description ticks the box, the box is contradicted.
- Count the repro itself as evidence only when the before and after
  runs of the plan's repro steps are shown. A full-suite pass alone does
  not show the new test fails on unfixed code.
- Check that `test_evidence.md` is real captured output. A file that
  holds some other tool's summary, not the repro and the checks, is
  not test evidence for this PR.

## Diff quality (unreviewable)

**Where it lives**

The output of `git diff main...HEAD` (read hunk by hunk, using the
`--- a/` and `@@` lines to see which file and area each hunk belongs
to), `git diff main...HEAD --stat` for the file list, and
`git log main..HEAD` for what each commit says it does. Only committed
changes count. Working notes (`plan.md`, `comment.md`, `pr_draft.md`,
`test_evidence.md`) must not appear in the diff.

**What good looks like**

- Every hunk serves the planned change, and the fix is visible at a
  glance: the code change, its test, and nothing else.
- Debris tells, each of which fails the diff whether or not the
  description mentions it: debug prints or leftover logging; commented-
  out or dead code; formatting or whitespace churn on lines the fix does
  not need; a rename, cleanup, or refactor with no link to the plan
  (for example, a hunk that rewrites a function the issue does not
  mention, burying the real one-hunk fix); a stray file.
- A hunk that rewrites working lines into a different but equivalent
  form is churn, not part of the fix, even when it looks tidier.
- Commit count and message style are not evidence of quality; read the
  hunks, not the log's shape.

## Standards and comms (the repo's asks)

**Where it lives**

The repo's asks are in `.github/PULL_REQUEST_TEMPLATE.md` (its
sections and checklist), `CONTRIBUTING.md` (including any AI policy),
any dedicated AI-policy file, and the issue thread (maintainer
direction). The answers are your draft: the title on line one, each
section, the `Closes #` line, the ticked boxes, and wherever the
AI-use disclosure goes (Notes for Reviewers, if the template has no
section for it). Required entries, such as a changelog file, must
appear in the diff. The branch name (a type prefix, the issue number, a
short description) is a `git branch` read.

**What good looks like**

- Every template section has real content: Summary says what and why,
  Issue is a closing keyword (`Closes #N`, `Fixes #N`) naming the plan's issue, Changes has one bullet
  per change in the diff, Testing ticks only true boxes and pastes
  results, any screenshot or demo section has an image or "N/A" with a
  reason, and Notes for Reviewers is filled. A heading left empty, a
  placeholder comment, or a section deleted is a visibly ignored ask.
- Every other stated ask is met in the package: if the repo requires a
  changelog entry, a docs update, or a checklist, the diff or the
  description shows it. A PR whose template names a required entry that
  is absent from the diff does not meet it.
- AI disclosure is present in the author's own words and says how AI
  was used on this change, wherever the repo's policy requires it. A
  one-word "AI-assisted" or a boilerplate line is not disclosure.
  Treat every package as AI-assisted.
- Maintainer direction in the thread is engaged, not skipped, and a PR
  does not duplicate someone else's claimed effort.
- Compliant means the asks are answered with content. Boilerplate that
  only reuses the template's own words does not count, and a polished
  description does not cover a missing ask.
