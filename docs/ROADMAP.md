# Roadmap

Where better-oss is, what it takes to reach the first production release, and
where to help. Every item is a GitHub issue; the numbers link to them.

## Where we are

- The plugin works: five skills, two hooks (voice-guard, ship-gate), the
  pr-monitor, and the installer. `better-oss-cli@0.0.1` is on npm.
- There are 73 tests, an 18-case evaluation suite (`evals/`), a CI workflow and a
  release workflow.
- **CI on `main` is red.** Two causes, both with an issue: the Python 3.9 job
  cannot start on the new `ubuntu-latest` ([#12](https://github.com/mobeloper/better-oss/issues/12)),
  and a `--dry-run` bug fails the installer tests when `claude` is not installed
  ([#13](https://github.com/mobeloper/better-oss/issues/13)).
- npm never lets a version number be reused, even after unpublishing. So `0.0.1`
  stays as it is, and the production release is a **new version**
  (`0.0.2` or `0.1.0`; the maintainer decides.

## Goal: v0.1.0, the first production release

Done when all of these hold:

1. CI is green on `main`, and the checks that matter are *required* to merge.
2. A pull request is checked for the rules in CONTRIBUTING.md, and a change to a
   rubric is checked by the evals before it can merge.
3. The version, the git tag, the GitHub release and the npm package all agree,
   and publishing is automated and approved by a maintainer.
4. The hooks' decision paths are tested without a real model, so anyone can
   contribute to them without credits.
5. The docs cover setup, troubleshooting and the security model.

## Milestone: v0.1.0

**1. Make CI green (P0).** Start here; nothing else can be trusted until it is.

| Issue | What | Size |
|---|---|---|
| [#12](https://github.com/mobeloper/better-oss/issues/12) | Python 3.9 job cannot start on `ubuntu-latest` | small |
| [#13](https://github.com/mobeloper/better-oss/issues/13) | Installer `--dry-run` hides the command when `claude` is missing | small |
| [#19](https://github.com/mobeloper/better-oss/issues/19) | Lint the workflows with actionlint | small |

**2. Test what is untested (P1).**

| Issue | What | Size |
|---|---|---|
| [#15](https://github.com/mobeloper/better-oss/issues/15) | Tests for `check_pr.py`, `eval_scope.py` and the evals harness | medium |
| [#20](https://github.com/mobeloper/better-oss/issues/20) | Offline tests with a fake `claude` and `gh` (the hooks' model paths) | large |
| [#21](https://github.com/mobeloper/better-oss/issues/21) | pr-monitor fixture tests for every PR state | medium |
| [#22](https://github.com/mobeloper/better-oss/issues/22) | Installer tests for the plugin-install path | small to medium |

**3. Gate contributions (P1).**

| Issue | What | Size |
|---|---|---|
| [#14](https://github.com/mobeloper/better-oss/issues/14) | PR health workflow (`scripts/check_pr.py`) | small to medium |
| [#16](https://github.com/mobeloper/better-oss/issues/16) | Evals as a required merge check | medium to large |
| [#17](https://github.com/mobeloper/better-oss/issues/17) | Write `evals/README.md` | small |
| [#23](https://github.com/mobeloper/better-oss/issues/23) | CodeQL code scanning | small |
| [#24](https://github.com/mobeloper/better-oss/issues/24) | Dependency review, and the failing Dependabot Actions updates | small |

**4. Behavior bugs and docs (P1).**

| Issue | What | Size |
|---|---|---|
| [#7](https://github.com/mobeloper/better-oss/issues/7) | `shipped-recently` passed while quoting 122 days | small |
| [#9](https://github.com/mobeloper/better-oss/issues/9) | Hooks leave a child process behind when killed | medium |
| [#10](https://github.com/mobeloper/better-oss/issues/10) | voice-guard misses comments posted through `gh api` | medium |
| [#25](https://github.com/mobeloper/better-oss/issues/25) | Troubleshooting and FAQ | small to medium |

**5. Release (maintainer).** [#18](https://github.com/mobeloper/better-oss/issues/18)
is the checklist: the version decision, the stale `v0.0.1` tag, the npm trusted
publisher, the GitHub environment and secrets, branch protection, and a
pre-release dry run of the release workflow. It needs npm and admin access, so it
is not for outside contributors.

### Suggested order

`#12`, `#13` first (CI green) -> `#19`, `#15`, `#20` in parallel (tests) ->
`#14`, `#17`, then `#16` (gates; it needs `#15` and benefits from `#20`) ->
the rest of the P1 list -> `#18`.

## Later

Valuable, but after the first production release.

- **Reach:** Windows support for the hooks ([#4](https://github.com/mobeloper/better-oss/issues/4)),
  search-strategy examples for other languages ([#5](https://github.com/mobeloper/better-oss/issues/5)),
  a second worked example ([#6](https://github.com/mobeloper/better-oss/issues/6)),
  a README demo ([#33](https://github.com/mobeloper/better-oss/issues/33)).
- **Evals:** a negative case for every required check ([#32](https://github.com/mobeloper/better-oss/issues/32)),
  cases for `issue-scout` ([#31](https://github.com/mobeloper/better-oss/issues/31)),
  repeat runs, a flakiness report, JUnit output and a cost estimate ([#11](https://github.com/mobeloper/better-oss/issues/11)).
- **Tooling and docs:** a `doctor` command ([#8](https://github.com/mobeloper/better-oss/issues/8)),
  labeler and stale workflows ([#26](https://github.com/mobeloper/better-oss/issues/26)),
  a threat model ([#27](https://github.com/mobeloper/better-oss/issues/27)),
  a pre-commit config ([#28](https://github.com/mobeloper/better-oss/issues/28)),
  a plugin icon and marketplace description ([#29](https://github.com/mobeloper/better-oss/issues/29)),
  a cleaner `repro-check` rubric ([#30](https://github.com/mobeloper/better-oss/issues/30)).
- **Direction:** a standalone CLI that runs the skills outside Claude Code
  ([#34](https://github.com/mobeloper/better-oss/issues/34), a design discussion first).

## How to pick something up

1. Filter issues by [`good first issue`](https://github.com/mobeloper/better-oss/labels/good%20first%20issue)
   or [`help wanted`](https://github.com/mobeloper/better-oss/labels/help%20wanted),
   and by milestone. `priority:p0` and `priority:p1` come first.
2. Comment that you are taking it, so two people do not do the same work.
3. Read [CONTRIBUTING.md](../CONTRIBUTING.md) (setup, branch names, what CI checks).
4. You do not need model credits for most of this. Lint, the tests and the eval
   `--dry-run` need none; issue [#20](https://github.com/mobeloper/better-oss/issues/20)
   will extend that to the hooks. Only running the evals or a skill needs a
   logged-in `claude`.
