# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/) (pre-1.0, so anything may change).

## [Unreleased]

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
- `npx better-oss init`: checks prerequisites, installs the plugin, and copies the
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
