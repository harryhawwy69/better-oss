# Evidence guide: where evidence lives in a plan package

A plan package is your `plan.md` plus the draft plan comment, read
against the issue and the reproduction evidence the plan builds on.
Plan files usually have these parts:

1. The cause of the bug (a diagnosis).
2. The scope: what changes and what does not.
3. The files and approach.
4. The test plan.

The issue-side evidence is on GitHub: the issue (title, opener, labels,
body), its thread (maintainer and contributor comments, each with an
author association such as COLLABORATOR or NONE), your posted repro
comment (environment, numbered steps with results, a control run when
there is one, Expected/Actual), and the repo facts: `CONTRIBUTING.md`,
the `.github/` templates, and releases.

**Plan headings are not standard.** Match sections by the role they
play, not the label. Variants seen so far:

| Role | Variant A | Variant B | Variant C |
|---|---|---|---|
| Cause | `### Diagnosis` | `### Diagnosis` | `Cause:` paragraph |
| Scope | `### Scope` | `### Scope` | `In:` / `Out:` inside `Change:` |
| Files/changes | `### Files`, `### Approach` | `### Changes` (numbered) | `Change:` (names one file) |
| Test | `### Test plan` | `### Test plan` | `Test:` paragraph |

If a role has no matching section anywhere in the plan, that evidence is
absent and the check that needs it fails.

## Diagnosis and grounding

- **Where it lives.**
  - *In your drafts:* the plan's cause statement (`### Diagnosis` or `Cause:`).
    Read it against, in this order: the issue title; the
    repro evidence steps, especially the control run and the
    Actual line; and the issue thread, in case the plan borrows
    its cause from a comment.
  - *On GitHub:* the same plan section against your repro comment
    and the issue thread.
- **What good looks like.** The cause names a specific mechanism or code
  location, cites a repro fact that supports it, explains the behavior
  the issue title names, and contradicts nothing in the repro evidence.
  A cause taken from a thread comment is only as good as the repro
  evidence behind it: check that a repro step shows it.
- **Examples.**
  - A passing case: the cause (the post-push refresh misses the
    branch-commits view, so push-status flags stay stale) matches repro
    steps 3 and 4 (color stale until the view is re-entered) and the
    issue title (push does not refresh the color).
  - A failing case: the plan's cause is the pager's key-binding
    registration, taken from a thread comment ("As identified in this
    thread"). Repro step 3 runs with `--paging=never` (no pager at all)
    and still takes 25.8 s, and step 4 with color off takes 0.2 s: the
    repro points at syntax highlighting. The plan's own Scope even
    calls highlighting "unrelated". Cause contradicts the repro.
  - Another failing case: the plan calls the Python-version difference a "red
    herring", while the repro shows the same command passing on 3.13.5
    and failing on 3.11.15.

## Scope

- **Where it lives.**
  - *In your drafts:* the plan's in-scope and out-of-scope statements
    (`### Scope`, or `In:` / `Out:`), plus the files named under
    `### Files` / `### Changes` / `Change:`. Compare the file list with
    the files the diagnosis implicates, and with maintainer comments in
    the issue thread about what is wanted.
  - *On GitHub:* the same in `plan.md`, plus the issue thread.
- **What good looks like.** Every file to be changed is named (or, where
  exact files are not yet known, the specific module, component, or code
  path, an area a stranger could locate), an
  explicit not-touching statement excludes something real (something
  someone could plausibly be tempted to change), and a reason is given
  for what the changes are for. The Changes/Approach steps stay inside
  the Scope statement.
- **Examples.**
  - A passing case: names one file
    (`pkg/gui/controllers/sync_controller.go`), says Out: "any change to
    how push status is computed, or to other views' refresh behavior",
    and says why (add the commits context to the post-push refresh).
  - In the pager case above, the Scope statement is well formed (one file, highlighting
    pipeline excluded), but what it excludes is exactly what the repro
    implicates; that is a diagnosis failure, not a form failure. Grade
    the Scope check on its own condition and let `diagnosis` carry the
    failure.
  - A passing case without file names: it names the reattach handshake
    on Unix clients in `zellij-server`'s client connection handling and
    `zellij-client`'s query issuance, says the exact functions will be
    pinned after tracing, defers the Windows variant with reasons, and
    states what the change is for. A bounded area with honest
    uncertainty is enough; "the codebase" is not.
  - In the Python-version case, the Scope says "rewrite the request-item tokenizer": a
    rewrite signals a larger change than the reproduced bug needs; read
    it together with the Changes check.

## Executability

(This family supplies the evidence for the rubric's `changes` check.)

- **Where it lives.**
  - *In your drafts:* the files and steps part of the plan (`### Files` and
    `### Approach`, `### Changes`, or `Change:`). Look for: each file
    and why it is modified, any file added or deleted and why, and
    words that signal size ("rewrite", new modules, many files).
    Check named files and symbols against the repro
    evidence.
  - *On GitHub:* the same in `plan.md`, with the named paths checkable in the
    repo.
- **What good looks like.** A stranger could start without asking the
  author: files or functions are named, each change is a concrete
  action ("call `generate_default_bindings()` before registering bat's
  custom bindings") rather than "improve handling", any added or deleted
  file has a stated justification, and the described work is small
  enough to stay under 500 lines changed. Estimate size from what the
  plan describes; a one-callback change or a few numbered steps is far
  under 500, a "rewrite" or new subsystem is not.
- **Examples.**
  - Good: one file, one concrete change (add the commits context
    to the push callback's refresh scope); small.
  - Good: three numbered concrete steps in one file plus a smoke
    test; executable and small, even though the diagnosis is wrong.

## Test plan

- **Where it lives.**
  - *In your drafts:* the plan's test section (`### Test plan` or `Test:`) and
    any step in Changes that adds a test (change 3 of the pager plan: "Add a
    pager-integration smoke test"). Read it against the repro evidence's
    steps and Expected/Actual.
  - *On GitHub:* the same in `plan.md` against your repro comment.
- **What good looks like.** The plan has a decisive test: it adds an
  automated test (a new or extended case that names where it goes), or,
  when automation is not practical (terminal, SSH, GUI behavior), a
  repeatable check taken from the repro steps with an observable pass
  result (output, exit code, a visible change) that would differ on the
  unfixed code. "Run the existing or full test suite" or "verify it
  works" is not a test for this fix.
- **Examples.**
  - A passing case: a smoke test asserting the default binding set
    is registered (Changes step 3), plus a manual shift+G check.
  - A passing case: no automated test, but its repro steps are
    re-run and step 3 must show the pushed color without leaving the
    view: a repeatable, observable check.
  - A passing case: five consecutive SSH reattach cycles with no `rgb:`
    strings, fresh create still clean, and the cache control becoming
    "always clean".
  - A passing case: new tokenizer cases in `tests/test_cli.py`.
  - A failing case: the test plan is "run the full test suite", with
    no observable outcome for the fix itself.

## Honesty

Not graded by the rubric; it never changes the verdict. Use it for
summary notes.

- **Where it lives.**
  - *In your drafts:* risks, unknowns, or assumptions in the plan and the plan
    comment, and the confidence of the cause's wording compared with the
    repro evidence.
  - *On GitHub:* the same in `plan.md` and the draft comment; a mid-build
    deviation is recorded in `plan.md` (what changed and why), not only
    in the diff.
- **What good looks like.** Claims are as strong as the evidence:
  anything not reproduced or checked is stated as an unknown. Example of
  the opposite: the pager plan's comment says "I traced this to..." when the
  cause was only taken from a thread comment.

## Comms

This family supplies the evidence for the rubric's `comms` check. Also
read it alongside the voice guide.

- **Where it lives.**
  - *In your drafts:* the draft plan comment read against the issue
    thread (maintainer direction, other people's claims or PRs) and
    the repo's contribution policy (including any AI-use
    rule). Read the policy line first and note who a disclosure rule
    covers: comments, pull requests only, or all AI use. Every plan is
    treated as AI-assisted.
  - *On GitHub:* the draft comment against the issue thread, `CONTRIBUTING.md`,
    `.github/` templates, and any AI policy file.
- **What good looks like.** The comment engages what maintainers asked
  for or settled, does not duplicate someone's claimed effort, matches
  the plan rather than overstating it, and states any AI-use disclosure
  the policy requires for comments or plans.
- **Examples.**
  - A passing case: it responds to CONTRIBUTING's review-bandwidth
    note ("keeping it minimal").
  - A passing case: its comment states the fix "will be AI-assisted
    with me reviewing", as the repo's AI policy asks.
  - A passing case without disclosure in the comment: that policy asks
    for the tool and extent in the pull request only.
  - A failing case: an excellent plan that follows the maintainer's
    direction, but ghostty's policy requires all AI usage to be
    disclosed (tool and extent) and the comment contains none.
  - A failing case: the comment never engages the owner's explicit
    direction in the thread.
  - The pager plan's comment repeats a cause that another contributor
    already claims is fixed in PR #3836, without acknowledging that PR.
