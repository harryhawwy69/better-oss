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

=== The repo's bug report template (.github/ISSUE_TEMPLATE/bug_report.yml) ===
name: Bug report
description: Report a reproducible problem with OpenMed
title: "[BUG] "
labels:
  - bug
body:
  - type: markdown
    attributes:
      value: |
        Thank you for helping improve OpenMed.

        **Do not include protected health information (PHI), personally identifiable information (PII), secrets, or real patient data.** Use only synthetic or fully de-identified examples. Report security vulnerabilities privately through [GitHub Security Advisories](https://github.com/maziyarpanahi/openmed/security/advisories/new).

  - type: textarea
    id: description
    attributes:
      label: Bug description
      description: Clearly describe what went wrong.
      placeholder: Tell us what happened.
    validations:
      required: true

  - type: textarea
    id: minimal_reproduction
    attributes:
      label: Minimal reproduction
      description: Provide the smallest set of steps or code that reproduces the problem. Use synthetic data only.
      placeholder: |
        1. Install or import ...
        2. Run ...
        3. Observe ...
    validations:
      required: true

  - type: textarea
    id: expected_behavior
    attributes:
      label: Expected behavior
      description: Describe what you expected to happen.
    validations:
      required: true

  - type: textarea
    id: error_output
    attributes:
      label: Error output
      description: Paste the relevant error or traceback after removing PHI, PII, secrets, and patient data.

  - type: input
    id: openmed_version
    attributes:
      label: OpenMed version
      description: Run `python -c "import openmed; print(openmed.__version__)"` if needed.
      placeholder: e.g. 2.1.0
    validations:
      required: true

  - type: input
    id: operating_system
    attributes:
      label: Operating system
      placeholder: e.g. Windows 11, Ubuntu 24.04, macOS 15
    validations:
      required: true

  - type: input
    id: python_version
    attributes:
      label: Python version
      placeholder: e.g. 3.12.4
    validations:
      required: true

  - type: input
    id: model_id
    attributes:
      label: Model ID
      description: Provide the Hugging Face or OpenMed model ID. Enter `N/A` if no model is involved.
      placeholder: e.g. OpenMed/... or N/A
    validations:
      required: true

  - type: input
    id: pytorch_version
    attributes:
      label: PyTorch version
      description: Enter `N/A` if PyTorch is not involved.
      placeholder: e.g. 2.7.0 or N/A

  - type: input
    id: transformers_version
    attributes:
      label: Transformers version
      description: Enter `N/A` if Transformers is not involved.
      placeholder: e.g. 4.53.0 or N/A

  - type: textarea
    id: additional_context
    attributes:
      label: Additional context
      description: Add any other relevant, non-sensitive details.

  - type: checkboxes
    id: privacy_confirmation
    attributes:
      label: Privacy confirmation
      options:
        - label: I confirm that this issue contains no PHI, PII, secrets, or real patient data.
          required: true

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

=== Draft claim comment ===
Hi @maziyarpanahi! I'd like to take this one. Could you assign it to me? (You offered this issue on #5296's thread)

First step: read `tests/fixtures/risk/README.md`, `quasi_identifier_uniqueness.jsonl` and `kanon_report` in `openmed/risk/kanon.py`, then write `successive_releases_v1.jsonl` (a `meta` row and two releases of 20-40 rows each, with a keyed privacy-unit column) and `tests/unit/risk/test_successive_release_fixture.py`. The test will run `kanon_report` on each release alone and assert the committed k values. I'll document the format and the expected intersection result in the README, and leave composition scoring out.

All rows will be synthetic and marked as such, with no real names, dates or places. I'll comment here once `.venv/bin/python -m pytest tests/unit/risk/test_successive_release_fixture.py -q` passes locally, or earlier if the fixture format needs a decision from you.

=== Draft repro report ===
# Repro report: openmed #5295 (no successive-release fixture exists)

Issue: https://github.com/maziyarpanahi/openmed/issues/5295, "Add a synthetic successive-release fixture for composition tests". The issue reports a gap, not a crash: `tests/fixtures/risk/` has QI uniqueness and negation-trap fixtures "but nothing with two releases". I reproduced the gap on current `master`.

## Environment

- macOS 26.5.1 (MacBook Pro), Python 3.13.9. `uv` is not installed, so I used the pip fallback from CONTRIBUTING.md.
- Repo: fork mobeloper/openmed at `master` commit `e8325586e1ce2da73e9e865f34bd0345bb64301a` (2026-11-16), identical to `upstream/master` (`git rev-parse upstream/master` returns the same hash). Package version `openmed` 3.3.0 (`openmed/__about__.py`). The issue's "Release: v4.3" footer is a roadmap milestone, not a version where the behavior was seen. The bug template's Model ID, PyTorch and Transformers fields do not apply to an offline fixture.
- Setup: `python3 -m venv .venv`, `.venv/bin/python -m pip install --upgrade pip`, `.venv/bin/python -m pip install -e ".[dev]"`. It installed with no errors and `import openmed` reports 3.3.0.

## Steps to reproduce

From the repo root, on the commit above:

1. Check that the files the issue asks for are absent:
   `ls tests/fixtures/risk/successive_releases_v1.jsonl tests/unit/risk/test_successive_release_fixture.py`
2. Run the issue's validation command:
   `.venv/bin/python -m pytest tests/unit/risk/test_successive_release_fixture.py -q`
3. Search the repo for any existing successive-release fixture:
   `grep -rIl "successive_release" . --exclude-dir=.venv --exclude-dir=.git` and `grep -n -i "successive\|intersect" tests/fixtures/risk/README.md`
4. Confirm the existing building blocks work: run `kanon_report` on the closest existing fixture, and run the existing risk tests:
   `.venv/bin/python -m pytest tests/unit/risk/test_regression_suites.py tests/unit/risk/test_kanon.py -q`

## Expected behavior

Per the issue's acceptance criteria, the repo should contain `successive_releases_v1.jsonl` (a `meta` row and two releases of 20-40 synthetic rows with a keyed privacy-unit column), a README section describing it and the expected intersection result, and `test_successive_release_fixture.py`, so the pytest command in step 2 passes and asserts each release's k.

## Actual behavior

- Step 1: both files are missing: `No such file or directory` for each.
- Step 2: the pytest command cannot run: `ERROR: file or directory not found: tests/unit/risk/test_successive_release_fixture.py` / `no tests ran in 0.48s`.
- Step 3: no tracked file in the repo matches `successive_release`. The README mentions only "release-gate fixtures", with no successive releases or intersection result. `tests/fixtures/risk/` holds only `dp_budget_scenarios.json`, `negation_traps.jsonl`, `quasi_identifier_uniqueness.jsonl` and `README.md`, and none has a release field.
- Step 4: the building blocks already work, so the gap is only the missing fixture and test. The existing suites pass: `35 passed, 9 subtests passed in 11.96s`. `kanon_report` on `quasi_identifier_uniqueness.jsonl` (4 records, QIs `age`, `city`, `visit_date`) returns `k = 2`, `class_count = 2`: it measures one release at a time, and nothing in the repo supplies a second release to intersect.

## Findings

The issue's description matches the repo today. The missing pieces are the fixture, its README contract and the per-release test, and nothing else is broken. The same `kanon_report` call can measure each release alone, so I do not expect to touch `openmed/risk/`. I have not yet checked the privacy-unit wording in `openmed/risk/population.py`, so the privacy-unit column name is still open.
