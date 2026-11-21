# Rubric: is this pull request ready to submit?

<!--
Failure families this rubric covers: silent drift (the diff silently
does more or less than the posted plan, or the description claims
fidelity the diff contradicts), not tested (the evidence proves nothing
observable, or the repo's own checks were never run), unreviewable
(debris or unrelated hunks bury the change), and standards wall (the
repo's stated template and disclosure asks are ignored). Judge the
outcome, never the write-up's shape. Honest-outcome rule: a PR that
honestly discloses a shortfall can be ready; a rubric that equates
"less than everything" with "hold" fails.
-->

## Checks

The checks follow the PR's anatomy: the title (what changed, and
where), the description (why should I believe it), the commits (how
did it get here), the diff (what exactly moved), and the evidence (how
do I see it work). Each check is tied to one failure family: silent
drift (diff-matches-plan, description-matches-diff), not tested
(test-evidence, repo-checks), unreviewable (clean-diff), and standards
wall (template-complete, ai-disclosure).

| Check | Evidence | Pass condition | Weight |
|---|---|---|---|
| diff-matches-plan | The diff's changed files and hunks read against the plan's stated files and not-in-scope list (`plan.md`) and any deviation notes (`## Deviations` in `plan.md`). See "Plan fidelity" in `references/evidence-guide.md`. | Passes if every changed file and behavior change in the diff falls inside the plan's stated files and boundary or is named in a deviation note, AND nothing the plan says it will do is missing from the diff, unless a deviation note or the description discloses the omission. Fails if the diff adds a change the plan scopes out or never mentions (a new option, a refactor, an extra file) or silently drops a planned step, with no deviation note or disclosure. A disclosed shortfall or deviation passes. | required |
| description-matches-diff | The description's Summary and Changes bullets (and any "implements the plan exactly" claim) read against the diff and the commit list. See "Plan fidelity" in `references/evidence-guide.md`. | Passes if every change the description claims is visible in the diff, every behavior change in the diff is described, and any fidelity claim ("matches the plan", "no other changes") is true of the diff. Fails if the description claims something the diff does not contain, omits a behavior change the diff makes, or claims fidelity the diff contradicts. | required |
| test-evidence | The test-evidence section (`test_evidence.md` and the Testing section of `pr_draft.md`) read against the plan's test plan and the repro steps and Expected/Actual in the plan context. See "Test evidence" in `references/evidence-guide.md`. | Passes if the evidence shows the repro or planned test run on the change with an observable result that would differ without the fix (a before and an after output, a new test that fails on the old code, a named behavior with its expected value), AND it exercises the path the diff changes. Fails if the evidence is only a claim ("tested locally", "tests pass", "works now") with nothing observable, shows only the after, or exercises code the diff does not touch. | required |
| repo-checks | The test-evidence section's record of the repo's own checks, read against the repo's PR-template checks (the checks listed in `.github/PULL_REQUEST_TEMPLATE.md`, such as unit tests, lint, typecheck). See "Test evidence" in `references/evidence-guide.md`. | Passes if every check the repo's template or docs ask for is shown with its result pasted, or its absence is explained (for example "no tests ran" pasted as is), and any failing check is reported with its reason rather than hidden. Fails if a stated check is never run or never shown, or a failure is hidden or contradicted by the evidence. The CI box left unticked pending the PR does not fail. | required |
| clean-diff | The unified diff and commit list: every hunk read for debris and for relevance to the plan. See "Diff quality" in `references/evidence-guide.md`. | Passes if every hunk serves the planned change and the fix is visible at a glance. Fails if the diff contains debug prints or leftover logging, commented-out or dead code, formatting or whitespace churn on lines the fix does not need, or unrelated hunks (a cleanup, rename, or extra file) folded in, whether or not the description mentions them. Commit count and message style are not graded. | required |
| template-complete | The description read against the repo's PR-template asks (`.github/PULL_REQUEST_TEMPLATE.md`, and the repo's `CONTRIBUTING.md`): each section, the issue link, the checklist, and other stated asks such as a changelog or whatsnew entry. See "Standards and comms" in `references/evidence-guide.md`. | Passes if every section the template asks for has real content (Summary, Issue as a closing keyword (`Closes #N`, `Fixes #N` or `Resolves #N`) naming the plan's issue, one Changes bullet per change, Testing with ticked boxes that are true, Screenshots / Demo with content or an N/A reason, Notes for Reviewers), AND every other required ask the repo states (a checklist, a changelog entry that must appear in the diff) is met or visibly answered. Fails if a required section is missing, empty, or a placeholder, the issue link is absent or names a different issue, a ticked box is contradicted by the evidence, or a required ask is ignored. Where the repo has no PR template, passes if the description states what changed, why, and the issue, and follows any stated contribution asks. | required |
| ai-disclosure | The description's Notes for Reviewers (or wherever the description discloses AI use) read against the repo's contribution policy line (`CONTRIBUTING.md` and the template). See "Standards and comms" in `references/evidence-guide.md`. | Passes if the description states in the author's own words how AI was used on the change where the repo's stated policy requires disclosure. Treat every package as AI-assisted. Fails if the policy requires AI disclosure and the description has none, or the disclosure is boilerplate that says nothing about how AI was used. Exception (the repo's rule outranks the disclosure ask): also passes when the repo's own agent or contributor rules (`AGENTS.md`, `CONTRIBUTING.md`) forbid AI, tool, vendor or generation attribution in PR text, AND the description quotes that rule in one line and contains no AI or tool attribution; the PR then carries no disclosure by the repo's own rule, and the author records the AI-use disclosure in their own notes instead. If the repo has no such rule, or the description quotes it but still attributes AI, the exception does not apply. | required |
| title-and-issue | The PR title and the description's Issue line (the first line of `pr_draft.md` and the branch name) read against the diff and the issue. See "Standards and comms" in `references/evidence-guide.md`. | Passes if the title says what changed and where, in terms the diff bears out, and the PR names the issue it closes. Fails if the title is vague ("fix bug", "updates") or describes a change the diff does not make. | preferred |

## Verdict rule

Ready (`accept`) if every `required` check passes. If any `required`
check fails, the verdict is `reject`. `unclear` counts as `fail`: a PR
that cannot be verified from the package is not ready to submit.
`preferred` checks never change the verdict; report their grades in
the output only. Honest outcomes rule: a PR that discloses a shortfall
(an omitted step, a failing check with its reason, a deviation
recorded in the plan) can still pass the check that shortfall touches,
so do not fail a check merely because the PR does less than the whole
plan; fail it when the shortfall is silent.
