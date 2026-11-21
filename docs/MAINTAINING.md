# Maintaining better-oss

For the maintainer (and anyone who becomes one). Contributors: see
[CONTRIBUTING.md](../CONTRIBUTING.md).

## One-time repository setup

Do these by hand in the GitHub UI or with `gh`; none of it can live in the repo.

**Settings (Settings tab)**

- General: enable **Discussions** (the issue form and `SUPPORT.md` link to it;
  or `gh repo edit --enable-discussions`).
- Code security: enable **Private vulnerability reporting** (`SECURITY.md` and
  the Code of Conduct send reports there), **Dependabot alerts** and
  **Dependabot security updates**.
- Branches: add a rule for `main` that requires a pull request before merging.
  When CI exists, also require its status checks. Pick one merge style and keep
  it (the history so far uses merge commits).

**Labels.** `bug`, `enhancement`, `question`, `documentation`, `good first
issue` and `help wanted` already exist on a new repo. Create the rest:

```text
gh label create rubric    --color 5319e7 --description "A rubric, procedure or evidence-guide change"
gh label create hooks     --color d93f0b --description "voice-guard or ship-gate"
gh label create installer --color 0e8a16 --description "npx better-oss-cli init"
gh label create monitor   --color 1d76db --description "pr-monitor"
gh label create needs-repro --color fbca04 --description "Waiting for steps to reproduce"
for s in issue-scout issue-select repro-check plan-check pr-precheck; do
  gh label create "skill:$s" --color c5def5 --description "The $s skill"
done
```

**Description and topics**

```text
gh repo edit --description "Skills and guardrail hooks for making robust, reliable open source contributions (a Claude Code plugin)"
gh repo edit --add-topic claude-code --add-topic claude-code-plugin --add-topic agents \
             --add-topic open-source --add-topic automation
```

## Triage

1. Reproduce it, or ask for the missing piece and add `needs-repro`.
2. Label it: its type (`bug`, `enhancement`, `question`, `documentation`), its
   area (`rubric`, `hooks`, `installer`, `monitor`, or `skill:<name>`), and
   `good first issue` or `help wanted` when it fits.
3. Close duplicates with a link. Close "a skill graded my issue wrongly"
   reports that have no case and no verdicts, asking for the rubric-change form.
4. Answer questions in Discussions, and turn a repeated question into docs.

## Reviewing a pull request

Always: the PR template is filled in, the checks in `AGENTS.md` pass, the diff
is one change, and this holds:

```text
git ls-files -s | awk '$1==120000'      # no symlinks (must print nothing)
grep -rIn '/[U]sers/\|/[h]ome/' . --exclude-dir=.git --exclude-dir=node_modules
```

By area:

- **Rubrics, procedures, evidence guides.** The PR must show the case, the
  verdict before and after, and a case that was already right and still is. Re-run
  at least the failing case yourself with `claude --plugin-dir .`. Check names,
  weights and the verdict rule must change only on purpose, because the
  evidence guides and the ship-gate refer to them by name. Look for a wording
  change that fixes the one case by making the check easier to pass in general.
- **Hooks (`core/voice_guard`, `core/ship_gate`).** Every new path that can raise
  must end in exit 2. Pipe a few commands into the script (see `AGENTS.md`). A
  hook must never print a pass for something it could not read.
- **pr-monitor.** The `READONLY_GH` allowlist must not grow. A new `gh` call needs
  an issue first.
- **Installer.** It must not write `settings.json`, and must not overwrite a file
  without `--force`. `cd cli && npm test` covers both.
- **`defaults/`.** Still prefilled, still carrying the `EXAMPLE:` banner, and
  still generic wording (no personal paths or names beyond the author fields).
- **Skills.** `SKILL.md` frontmatter intact; the `pr-precheck` layout in
  `skills/pr-precheck/CONTRACT.md` unchanged.

## Releasing

Releases are manual until a release workflow exists.

1. Decide the version (`X.Y.Z`). Set it in **both** `.claude-plugin/plugin.json`
   and `cli/package.json`; they must match. Move the `Unreleased`
   entries in `CHANGELOG.md` under a new dated `X.Y.Z` heading.
2. Run every check in `AGENTS.md`, and `cd cli && npm pack --dry-run` (the
   `prepack` step copies `defaults/` into the package; the list should show it).
3. Test a clean install against an empty config, from the working tree:

   ```text
   export CLAUDE_CONFIG_DIR=$(mktemp -d)
   node cli/bin/better-oss.js init --home $(mktemp -d) --marketplace "$PWD"
   claude plugin list
   ```

4. Merge to `main`, then tag and release on GitHub: tag `vX.Y.Z` on the merge
   commit, with the notes written from the merged pull requests.
5. Publish the installer: `cd cli && npm publish` (needs `npm login` and your
   second factor). Then check `npx better-oss-cli@latest --version`.
6. Users get the plugin update with `claude plugin update better-oss`.

## Dependabot

Dependabot opens weekly pull requests for the installer's npm dependencies
(there are none today) and for GitHub Actions once workflows exist. Treat them
like any other pull request: the tests must pass.
