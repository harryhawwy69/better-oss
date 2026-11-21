evaluation_date: 2026-11-21
=== Issue ===
title: Add a synthetic successive-release fixture for composition tests
author: maziyarpanahi (repo owner)  created: 2026-11-07
labels: help wanted, good first issue, improvement, P2, roadmap-v4

## Problem and existing coverage

Composition across releases needs a small, known example: the same synthetic population released twice with different generalizations so that intersecting the two isolates some rows. `tests/fixtures/risk/` has QI uniqueness and negation-trap fixtures but nothing with two releases.

## Implementation

- Add `tests/fixtures/risk/successive_releases_v1.jsonl` with a `meta` row and two releases (20-40 rows each) of one synthetic population, plus a keyed privacy-unit column.
- Describe the format in `tests/fixtures/risk/README.md`.
- Add a test that checks each release alone with `kanon_report` and asserts the committed per-release k values.

## Acceptance criteria

- [ ] Every row is marked synthetic and contains no real names, dates or places.
- [ ] Each release alone meets the k recorded in the fixture's expectations.
- [ ] The README documents the expected intersection result for later composition tests.
- [ ] `.venv/bin/python -m pytest tests/unit/risk/test_successive_release_fixture.py -q` passes.

## Independent development boundary

Fixture and per-release test only; composition scoring is separate.

## Starting points and validation

`tests/fixtures/risk/successive_releases_v1.jsonl` (new), `tests/fixtures/risk/README.md`, `openmed/risk/kanon.py`, `tests/unit/risk/test_successive_release_fixture.py` (new).

Add focused offline unit and integration tests for this slice and document the public behavior. Use synthetic fixtures, injected transports/clocks/providers where needed, and negative controls. Record exact validation commands in the implementation PR.

## For first-time contributors

Read `tests/fixtures/risk/README.md` and `quasi_identifier_uniqueness.jsonl` for the format, and `kanon_report` in `openmed/risk/kanon.py`. Expect one fixture file, a README paragraph and a test of about 40 lines. Run `.venv/bin/python -m pytest tests/unit/risk/test_successive_release_fixture.py -q`.

Comment on this issue if anything is unclear; questions are welcome.

## Privacy and release limits

Keep local-first defaults. Diagnostics and evidence contain only controlled codes, counts, offsets, opaque references and digests; never raw PHI, credentials, private paths or source payloads. Do not bundle restricted data or weights. This task adds no autonomous clinical action, model-training prerequisite or publication authorization, and no implicit network egress: any remote call is opt-in, policy-checked and receives redacted content only.

---
Release: v4.3 · Priority: P2 · Size: S

State: open. Assignees: none. Comments: none. Linked pull requests: none.

=== Repository facts ===
Repository: maziyarpanahi/openmed (Apache-2.0). Default branch: master. Stars: 5832. Archived: no.
Newest five default-branch commits: 2026-11-20 merge of PR #5699 from an outside contributor; 2026-11-20 merge of master into that contributor's branch; 2026-11-20 merge of PR #5701 from an outside contributor; 2026-11-20 merge of PR #5703 from an outside contributor; 2026-11-19 docs commit by the maintainer.
Latest release: v3.3.0, published 2026-11-13.
Maintainer first-response sample (recent issues opened by someone other than the maintainer): #5509 opened 2026-11-08 by an outside contributor, the owner replied 2026-11-11; #5702 opened 2026-11-19 by an outside contributor, no reply yet (two days old).
This issue was opened by the repository owner, who labelled it `help wanted` and `good first issue`.

=== The repo's contribution rules (CONTRIBUTING.md) ===
# Contributing to OpenMed

Thanks for helping improve OpenMed — bug reports, features, docs, and
translations are all welcome. By participating you agree to our
[Code of Conduct](CODE_OF_CONDUCT.md).

> [!IMPORTANT]
> **Security and privacy come first.** OpenMed de-identifies PHI. **Never** open
> a public issue for a vulnerability, and **never** include real patient data in
> an issue, pull request, test, or fixture — see [SECURITY.md](SECURITY.md). Any
> test data committed to the repository must be synthetic.

This page is a quick start. The full tooling, documentation, and release guide
lives in **[docs/contributing.md](docs/contributing.md)**.

## Development setup

The canonical development environment is managed by [uv](https://docs.astral.sh/uv/).
From the repository root, run:

```bash
uv sync --frozen --extra dev    # create .venv and install from uv.lock
# stack extras as needed, e.g. --extra hf for Hugging Face model work
uv run --frozen --extra dev pre-commit install  # auto-format staged files on commit
```

Use `uv run --frozen --extra dev <command>` or the Makefile targets so commands
run inside the locked environment. If uv is unavailable, the supported fallback
is a regular virtual environment and editable pip install:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/pre-commit install
```

The pre-commit hooks also run the Gitleaks secret scanner on staged changes.
See [Secret Scanning](docs/security/secret-scanning.md) for local use, CI
behavior, and baseline maintenance.

## Run the checks before opening a PR

```bash
uv run --frozen --extra dev pytest tests/ -q
make format                              # apply canonical Ruff formatting
make lint                                # lint
make type-check                          # scoped public-module type check
make format-check                        # CI-parity format check
```

Ruff is the single source of truth for Python lint, import ordering, and
formatting; the pinned mypy gate checks the annotated public-module scope. CI
runs both gates. Do not run Black, isort, or flake8. For Swift changes under
`swift/OpenMedKit`, run `make format-swift` and `make lint-swift`.

`make lint`, the local pre-commit `effect-paths` hook and the CI lint job also
run `python scripts/security/check_effect_paths.py --check`. New or removed
HTTP/database effect candidates require an explicit review of
`scripts/security/effect_paths.json`; do not regenerate classifications without
reviewing the path. Built-in MCP, REST, CLI and Journey dependencies must not
reach the legacy FHIR/OpenMRS writers. See the
[agent boundary limits](docs/security/agent-threat-model.md#effect-path-inventory).

## Pull requests

- Keep each PR focused on a single feature or fix; avoid unrelated formatting
  churn.
- Name branches `<type>/issue-<number>-<short-kebab-slug>`, using a suitable type
  such as `feat`, `fix`, `docs`, `test`, `chore`, or `refactor`; for example,
  `docs/issue-280-maintainers`.
- Write clear, imperative commit messages (the project uses concise prefixes
  such as `fix:`, `feat:`, and `docs:`).
- Reference the issue you are closing and complete the
  [pull request template](.github/PULL_REQUEST_TEMPLATE.md).
- Update `CHANGELOG.md` and the docs when behavior changes.
- For privacy-sensitive paths, add tests for direct-identifier recall, critical
  leakage, and span integrity (see [docs/contributing.md](docs/contributing.md)).

## Reporting issues

- **Bugs and features:** use the
  [issue templates](https://github.com/maziyarpanahi/openmed/issues/new/choose).
- **Security vulnerabilities** (including redaction bypass or PHI/PII leakage):
  report privately per [SECURITY.md](SECURITY.md) — never as a public issue.

For the complete contributor and release workflow, see
**[docs/contributing.md](docs/contributing.md)**.

=== The repo's commit and PR rules (AGENTS.md excerpt) ===
## Commit & Pull Request Guidelines

Recent history uses concise imperative commits, often with prefixes such as `fix:`. Keep commits and PRs focused on the requested change. Use the repo-owner Git identity. Do not include assistant/tool/vendor names, co-author trailers, generation footers, or worker attribution in issue text, branch names, commit messages, PR titles, PR bodies, or labels. In particular, never use `codex` or `claude` in branch names, PR titles, PR bodies, issue titles, issue bodies, labels, or other repository metadata. Do not assign issues or PRs unless explicitly asked.

Before pushing or merging, run `python scripts/release/check_repo_policy.py
--commits origin/master HEAD` (substitute the actual target branch when needed).
This checks every incoming commit, including merge side parents, for forbidden
author/committer identities and attribution footers. Checking only the PR opener,
primary author, latest commit, or first-parent log is insufficient. Preserve
human contributor identity when correcting metadata. Never bypass the required
`Commit attribution policy` status. Its trusted base-branch validator runs in the
Secret Scan workflow and posts the result on the exact PR head; it never executes
PR code. Keep the repository ruleset active, with no bypass actors, for `master`
and `release/**` branches. A missing or failed check must block the merge.

Pull requests should follow `.github/PULL_REQUEST_TEMPLATE.md`: description, change type, tests run, docs or changelog updates when applicable, dependency justification, linked issue, and screenshots or example output for UI/docs changes.
