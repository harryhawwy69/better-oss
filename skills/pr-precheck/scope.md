# Scope: where your pull request lives, and the rules for other people's repos

A scope tells your tool which repos it may check and what rules apply
there. Your rubric still decides whether a pull request is ready.

## Where your pull request lives

Any public repository. Your pull request lands in front of real
maintainers, and asking a stranger to spend review time on your work is
exactly what this tool exists to make safe.

## Rules for other people's repos

- **The repo's conventions outrank yours.** Branch names, commit style,
  PR size, target branch: read the repo's contributing docs and follow
  those. The `fix/<issue>-<slug>` habit is a good default only where the
  repo states nothing.
- **From your fork, always.** You have no push access to a stranger's
  repository: the branch you ship lives on your fork of it, and the
  pull request points from there at the branch the repo's contributing
  docs name as the target (its default branch unless they say
  otherwise; some repos take pull requests on `dev`).
- **One PR per issue is a courtesy to reviewers, not a rule.** If a
  maintainer asks you to split or combine work, the maintainer is right.
- **A parallel PR is a real cost.** Check the issue's linked PRs before
  opening yours. If someone's fix is already up, review or test theirs
  instead of racing it.
- **Deviations go in the PR description.** Your plan is never posted
  on the issue, so the PR description is the only place a maintainer
  learns your approach. If your diff materially departs from your
  plan, update `plan.md` and say what changed and why in the PR
  description. No note on the issue thread is needed.
- **Disclosure follows the repo's stated policy, always.** This
  workflow is AI-assisted by design; where a repo asks for AI-use
  disclosure, the disclosure appears, in your own words, every time.
  Where a repo bans AI-assisted contributions outright, that repo is
  out of scope: pick another issue.
