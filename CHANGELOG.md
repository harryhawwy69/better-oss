# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/) (pre-1.0, so anything may change).

## [Unreleased]

## [0.1.0] - 2026-11-23

First production release.

### Added

- A test suite (`pytest`, no model calls) covering the hooks' exit
  codes and fail-closed behavior, the plugin and hook manifests, every skill's
  structure and rubric, the shipped defaults, the docs and their links, and the
  release tooling.
- CI on every push and pull request: `ruff` and `pytest` on Python 3.9 and 3.13,
  the installer tests on Node 18 and 22, and a personal-data and symlink check.
- `scripts/leak_check.py`: fails on home-directory paths, email addresses, tokens
  and symlinks; project-private terms are supplied through environment variables,
  not committed.
- A release workflow: on a `vX.Y.Z` tag it verifies the version everywhere,
  creates the GitHub release from this changelog, and publishes the installer to
  npm after a maintainer approves it.
- `ruff.toml` (targets Python 3.9) and `pytest.ini`.
- An evaluation suite in `evals/`: 18 frozen cases, each a real worked run with one
  deliberate flaw, with a harness that checks the skills catch it
  (`python3 evals/run_evals.py`; `--dry-run` needs no model).
- Tests for the installer's `claude plugin install` path, for the guards' model
  decision paths using a fake `claude`, and for the pr-monitor's drafting path,
  all runnable without credentials (thanks to @volt69506-eng).
- A public roadmap (`docs/ROADMAP.md`) and the open issues it links to.

### Fixed

- `better-oss-cli init --dry-run` now shows the plugin command even when `claude`
  is not installed (@snehaapratap).
- CI: the Python 3.9 job is pinned to a runner that still ships Python 3.9
  (@volt69506-eng).
- The leak check no longer mistakes a package version for an email address
  (@volt69506-eng).

## [0.0.1] - 2026-11-21

First public release.

### Added

- A Claude Code plugin with five skills: `issue-scout`, `issue-select`,
  `repro-check`, `plan-check` and `pr-precheck`, each a rubric with an evidence
  guide and a scope for working in other people's repositories.
- Two hooks, registered in `hooks/hooks.json`: **voice-guard**, which holds
  outgoing `gh` comments and PR bodies against your voice guide, and
  **ship-gate**, which runs your repository's checks and `pr-precheck` before
  `gh pr create`. Both fail closed.
- **pr-monitor**, a read-only script that reads your open PR and drafts your next
  move from your playbook.
- Slash commands `/better-oss:init`, `/better-oss:ship-gate` and
  `/better-oss:monitor`.
- `npx better-oss-cli init`: checks prerequisites, installs the plugin, and copies the
  example files into `~/.claude/better-oss/` without overwriting yours.
- Prefilled example files in `defaults/` (voice guide, fit profile, search
  strategy, playbook, ship manifest, repo-memory template) and six input
  templates in `defaults/templates/`.
- A worked example in `examples/`: one real contribution followed through every
  stage.
- Project documentation: README, architecture, adding a skill, contributing,
  maintaining, governance, security, support and a code of conduct, plus issue
  forms and a pull request template.

### Known limits

- Built and tested on macOS; the hooks call `python3`, so Windows is untested.
- No automated evaluation suite for the rubrics; changes are judged on manual
  before and after runs.
- The voice-guard only checks the `gh issue|pr comment|create` forms.
