# Walkthrough: one real contribution, end to end

This follows one real contribution through every stage of the `better-oss`
pipeline: [openmed issue #5295][issue], "Add a synthetic successive-release
fixture for composition tests", which became [pull request #5698][pr]. The
files referenced are in [`openmed-5295/`](openmed-5295/). They are the actual
drafts and tool outputs, unedited except for wording that did not belong in a
public repo.

The contribution is deliberately small: a test fixture, a short test, and a
README paragraph, with no library code changed. That is the kind of issue the
rubrics are built to find, and the kind a newcomer can finish.

| Stage | Skill or hook | What happened | Files |
|---|---|---|---|
| 1. Find | `issue-scout`, `issue-select` | A multi-query scan of agentic-AI repos matching the [fit profile](../defaults/fit-profile.md) surfaced the issue; direct grading with `issue-select` then accepted it as "straightforward". Every required check passed; only the preferred `has-repro` check failed. | |
| 2. Claim | `repro-check` (claim-only) | Drafted a claim comment that names the first concrete step and promises no date. The skill graded the claim-only draft: the checks needing a repro report came back `unclear` ("not yet applicable") and the verdict was `accept` for the claim itself. | [claim-draft.md](openmed-5295/claim-draft.md), [claim-check-output.json](openmed-5295/claim-check-output.json) |
| 3. Reproduce | `repro-check` (full package) | The issue reports a gap, not a crash, so the reproduction shows the gap: the fixture and test files do not exist on `master`, and the existing 35 related tests pass. The skill graded all seven checks `pass`. | [repro-draft.md](openmed-5295/repro-draft.md), [repro-check-output.json](openmed-5295/repro-check-output.json) |
| 4. Plan | `plan-check` | Wrote a plan with a diagnosis (a coverage gap, not a defect), an explicit "not touching" list, three named files, and a decisive test. `plan-check` graded diagnosis, scope, changes, test and comms. | [plan.md](openmed-5295/plan.md), [plan-comment.md](openmed-5295/plan-comment.md), [plan-check-output.md](openmed-5295/plan-check-output.md) |
| 5. Build | (your editor and tests) | Implemented the plan on a branch, recording deviations in `plan.md` as they happened, and captured before and after output as it went. | [test_evidence.md](openmed-5295/test_evidence.md) |
| 6. Ship | `pr-precheck`, ship-gate hook | Drafted the PR description against the repo's own template. `pr-precheck` graded eight checks, including that the diff matches the plan and the claimed test evidence is observable. The ship-gate then re-ran the repo's own checks and `pr-precheck` and let `gh pr create` through. | [pr_draft.md](openmed-5295/pr_draft.md), [ship-gate-output.md](openmed-5295/ship-gate-output.md) |
| 7. Follow up | `pr-monitor` | Watches the open PR and drafts the next move (a review reply or a single nudge) from your [playbook](../defaults/playbook.md). Nothing is posted for you. | |

## What to notice

- **The human posts; the tools grade.** Every draft was held against a
  written rubric before it went anywhere. No stage posts on your behalf.
- **The repo's rules outrank the tool's.** This repo's `AGENTS.md` forbids
  tool or AI attribution in PR text. `pr-precheck` has an explicit exception
  for that case: the description quotes the rule in one line and carries no
  attribution, instead of failing the AI-disclosure check. See the
  `ai-disclosure` check in
  [`skills/pr-precheck/rubric.md`](../skills/pr-precheck/rubric.md).
- **Honest deviations pass; silent ones do not.** The plan has a
  `## Deviations` section, and the PR description reports the small
  differences from the plan (a longer test, extra metadata keys). `pr-precheck`
  grades a disclosed deviation as fine and an undisclosed one as drift.
- **The skills catch real things.** Re-running them later on these same
  artifacts, once the PR was open, flagged that the claim comment had gone
  stale and that a ticked "no new warnings" box had no baseline behind it.

## Try it on your own issue

1. Copy the defaults you need with `/better-oss:init`, then edit your
   [fit profile](../defaults/fit-profile.md) and
   [search strategy](../defaults/search-strategy.md).
2. Run `/better-oss:issue-scout` for a scan, or `/better-oss:issue-select`
   with an issue URL you already have.
3. Start each draft from [`defaults/templates/`](../defaults/templates/) and
   run the matching skill before you post.

[issue]: https://github.com/maziyarpanahi/openmed/issues/5295
[pr]: https://github.com/maziyarpanahi/openmed/pull/5698
