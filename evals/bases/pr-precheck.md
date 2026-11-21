evaluation_date: 2026-11-21
=== Draft PR title ===
test: add successive-release fixture and per-release kanon_report k test

=== Draft PR description ===
# Pull Request

## Description
Adds a small synthetic fixture with two releases of one population, generalized differently, so later composition tests have a known example, and a test that checks each release alone with `kanon_report`. Neither release isolates a unit by itself, but joining them on the privacy-unit key does. `kanon_report` already measures one release at a time, so no library code changes.

Fixes #5295

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [x] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [x] Test addition/improvement

## Changes Made
- `tests/fixtures/risk/successive_releases_v1.jsonl` (new): a `meta` row and two releases of 24 synthetic rows each. Every row has `synthetic: true`, a `release` label, an opaque `privacy_unit_id` shared by both releases, and the quasi-identifiers `age_band` and `area`. Release 1 uses ten-year age bands and a town, release 2 uses five-year age bands and a district. All values are invented, with no real names, dates or places. `meta.expected` commits the per-release k and the intersection result.
- `tests/unit/risk/test_successive_release_fixture.py` (new): checks every row is synthetic and each release has 20-40 rows, then runs `kanon_report` on each release alone, with `privacy_unit_id` left out of the quasi-identifiers, and asserts the committed k (3 for `release_1`, 2 for `release_2`).
- `tests/fixtures/risk/README.md`: documents the row format and the expected intersection result for later composition tests. Joining the releases on `privacy_unit_id` and combining both releases' quasi-identifiers gives k 1, with `pu-03`, `pu-04` and `pu-21` each alone in their class.

## Testing
- [x] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
  - Not fully: the 3 new tests and all 543 tests in `tests/unit/risk` pass, but the full suite has 6 failures in 2 unrelated tests that also fail on `master` (see Notes for Reviewers).
- [ ] I have tested this change with different models/inputs
  - N/A: the change is an offline fixture and a test, with no model or input handling.

Before, on `master` (`e8325586e`):

```text
$ ls tests/fixtures/risk/successive_releases_v1.jsonl tests/unit/risk/test_successive_release_fixture.py
ls: tests/fixtures/risk/successive_releases_v1.jsonl: No such file or directory
ls: tests/unit/risk/test_successive_release_fixture.py: No such file or directory

$ .venv/bin/python -m pytest tests/unit/risk/test_successive_release_fixture.py -q
ERROR: file or directory not found: tests/unit/risk/test_successive_release_fixture.py
no tests ran in 0.07s
```

After, on this branch, in the environment CONTRIBUTING asks for (`uv sync --frozen --extra dev`):

```text
$ uv run --frozen --extra dev pytest tests/unit/risk/test_successive_release_fixture.py -q
...                                                                      [100%]
3 passed in 0.16s

$ uv run --frozen --extra dev pytest tests/unit/risk -q
543 passed, 308 subtests passed in 2.81s

$ uv run --frozen --extra dev pytest tests/ -q
6 failed, 35040 passed, 405 skipped, 4 xfailed, 61 warnings, 11711 subtests passed in 816.01s (0:13:36)

$ make format
uv run --frozen --extra dev ruff check --fix .
All checks passed!
uv run --frozen --extra dev ruff format .
3623 files left unchanged

$ make lint
uv run --frozen --extra dev ruff check .
All checks passed!
uv run --frozen --extra dev python scripts/security/check_effect_paths.py --check
effect_paths_verified

$ make format-check
uv run --frozen --extra dev ruff format --check .
3623 files already formatted

$ make type-check
uv run --frozen --extra dev mypy
Success: no issues found in 4 source files

$ python3 scripts/release/check_repo_policy.py --commits origin/master HEAD
Commit attribution policy passed: 3 commits checked
```

Measured values, from `kanon_report` on each release alone and a throwaway join on `privacy_unit_id` that is not committed:

```text
release_1 24 rows  k 3  classes 8  sizes [3, 3, 3, 3, 3, 3, 3, 3]
release_2 24 rows  k 2  classes 8  sizes [3, 3, 3, 3, 3, 3, 2, 4]
intersection k 1  isolated ['pu-03', 'pu-04', 'pu-21']
```

With one release-1 row moved into a one-row area, the k check fails with `assert 1 == 3`.

## Documentation
- [x] I have updated the documentation accordingly
  - The fixture format and its expected intersection result are in `tests/fixtures/risk/README.md`.
- [ ] I have added docstrings to new functions/classes
  - N/A: the new code is two test functions and a loader helper; the test module has a docstring.
- [ ] I have updated the CHANGELOG.md
  - N/A: no behavior changes, and the earlier risk fixture PR (#351) did not add an entry.

## Code Quality
- [x] I ran `make format`, `make lint`, and `make format-check`
  - All three pass with output above, and `make format` changed no files. I also ran `make type-check`, which passes.
- [ ] For Swift/OpenMedKit changes, I ran `make format-swift` and `make lint-swift`
  - N/A: no Swift or OpenMedKit changes.
- [x] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
  - N/A: the new test code is a loader and two short assertions, with nothing hard to follow, so it has a module docstring and no inline comments.
- [x] My changes generate no new warnings

## Dependencies
- [x] I have not added any new dependencies
- [ ] OR I have added new dependencies and they are justified because: N/A

## Checklist
- [x] I have read the [contributing guide](https://github.com/maziyarpanahi/openmed/blob/master/CONTRIBUTING.md), [Code of Conduct](https://github.com/maziyarpanahi/openmed/blob/master/CODE_OF_CONDUCT.md), and [maintainer guide](https://github.com/maziyarpanahi/openmed/blob/master/MAINTAINERS.md)
- [x] My commits have clear, descriptive messages
- [x] I have squashed/organized my commits appropriately
  - Three commits: the fixture, the test, then the README.

## Related Issues
Fixes #5295

## Screenshots/Examples
N/A: no UI or docs-site change. The measured values are above.

## Notes for Reviewers
- Full suite: `pytest tests/ -q` in the locked environment shows 6 failures in 2 tests, neither in `tests/unit/risk` and neither touching this change: `tests/fuzz/test_deidentify_fuzz.py::test_malformed_iscii_preserves_clinical_text_and_identifier_spans` (4 subtest failures, "masked clinical text mismatch") and `tests/unit/structured/test_decision_server.py::test_local_media_is_scrubbed_and_sent_only_to_loopback[video]` (a `DecisionMediaError` on the video case, which uses a local ffmpeg). I ran the same two tests on `master` (`e8325586e`) in the same environment and the same 6 failed, so they fail without my commits. I did not fix them: they are outside this issue.
- Left out on purpose, per the issue's boundary: composition scoring. The test checks per-release k only. The intersection result is documented in the README and `meta.expected` and is not asserted in code.
- AI-use statement: not included, following this repo's `AGENTS.md`: "Do not include assistant/tool/vendor names, co-author trailers, generation footers, or worker attribution in issue text, branch names, commit messages, PR titles, PR bodies, or labels."
- Nothing under `openmed/risk/` changes.
- Small differences from my plan: the test file is 54 lines, the `meta` row also carries `quasi_identifiers` and `privacy_unit_column` so the test reads the column names from the fixture, and the README paragraph is 24 lines. The scope did not change.

=== Commit list ===
8be36858a docs: describe the successive-release fixture and its intersection result
dccd6f463 test: check each successive release alone with kanon_report
389623968 test: add synthetic successive-release fixture for composition tests

=== Diff stat ===
tests/fixtures/risk/README.md                      | 24 ++++++++++
 tests/fixtures/risk/successive_releases_v1.jsonl   | 49 ++++++++++++++++++++
 tests/unit/risk/test_successive_release_fixture.py | 54 ++++++++++++++++++++++
 3 files changed, 127 insertions(+)

=== The diff ===
diff --git a/tests/fixtures/risk/README.md b/tests/fixtures/risk/README.md
index 20bf0cdf6..3d8688770 100644
--- a/tests/fixtures/risk/README.md
+++ b/tests/fixtures/risk/README.md
@@ -22,6 +22,30 @@ Record rows for `quasi_identifier_uniqueness.jsonl` contain:
 - `record_id`: stable fixture identifier
 - quasi-identifier fields consumed by `openmed.risk.risk_report`
 
+Record rows for `successive_releases_v1.jsonl` contain:
+
+- `kind`: `record`
+- `record_id`: stable fixture identifier
+- `synthetic`: must be `true`
+- `release`: `release_1` or `release_2`
+- `privacy_unit_id`: opaque key naming the same synthetic unit in both
+  releases; it is not a quasi-identifier
+- `age_band` and `area`: the quasi-identifiers, generalized differently in
+  each release (`release_1` uses ten-year age bands and a town, `release_2`
+  uses five-year age bands and a district)
+
+The meta row names `quasi_identifiers` and `privacy_unit_column`, and commits
+the expectations under `expected`. Each release has 24 rows. Running
+`openmed.risk.kanon_report` on one release alone gives `k` 3 for `release_1`
+and `k` 2 for `release_2`.
+
+Expected intersection result for later composition tests: joining the two
+releases on `privacy_unit_id` and combining both releases' quasi-identifiers
+gives `k` 1. Units `pu-03`, `pu-04` and `pu-21` each end up alone in their
+equivalence class, even though neither release isolates them by itself.
+`successive_releases_v1.jsonl` does not score composition; it only fixes the
+known example.
+
 The suites intentionally avoid gated corpus rows and controlled-vocabulary
 payloads. Future grounding/context work can extend negation-trap rows with
 condition assertions while keeping the existing leakage fields stable.
diff --git a/tests/fixtures/risk/successive_releases_v1.jsonl b/tests/fixtures/risk/successive_releases_v1.jsonl
new file mode 100644
index 000000000..fd28d04fd
--- /dev/null
+++ b/tests/fixtures/risk/successive_releases_v1.jsonl
@@ -0,0 +1,49 @@
+{"kind":"meta","version":1,"suite":"successive_releases_v1","synthetic":true,"description":"One synthetic population released twice with different generalizations. Each release alone is k-anonymous, but joining the releases on privacy_unit_id isolates some units.","privacy_unit_column":"privacy_unit_id","quasi_identifiers":["age_band","area"],"expected":{"k":{"release_1":3,"release_2":2},"intersection":{"k":1,"isolated_privacy_unit_ids":["pu-03","pu-04","pu-21"]}}}
+{"kind":"record","record_id":"r1-01","synthetic":true,"release":"release_1","privacy_unit_id":"pu-01","age_band":"30-39","area":"Alderbrook"}
+{"kind":"record","record_id":"r1-02","synthetic":true,"release":"release_1","privacy_unit_id":"pu-02","age_band":"30-39","area":"Alderbrook"}
+{"kind":"record","record_id":"r1-03","synthetic":true,"release":"release_1","privacy_unit_id":"pu-03","age_band":"30-39","area":"Alderbrook"}
+{"kind":"record","record_id":"r1-04","synthetic":true,"release":"release_1","privacy_unit_id":"pu-04","age_band":"30-39","area":"Fernwick"}
+{"kind":"record","record_id":"r1-05","synthetic":true,"release":"release_1","privacy_unit_id":"pu-05","age_band":"30-39","area":"Fernwick"}
+{"kind":"record","record_id":"r1-06","synthetic":true,"release":"release_1","privacy_unit_id":"pu-06","age_band":"30-39","area":"Fernwick"}
+{"kind":"record","record_id":"r1-07","synthetic":true,"release":"release_1","privacy_unit_id":"pu-07","age_band":"40-49","area":"Alderbrook"}
+{"kind":"record","record_id":"r1-08","synthetic":true,"release":"release_1","privacy_unit_id":"pu-08","age_band":"40-49","area":"Alderbrook"}
+{"kind":"record","record_id":"r1-09","synthetic":true,"release":"release_1","privacy_unit_id":"pu-09","age_band":"40-49","area":"Alderbrook"}
+{"kind":"record","record_id":"r1-10","synthetic":true,"release":"release_1","privacy_unit_id":"pu-10","age_band":"40-49","area":"Marlowe"}
+{"kind":"record","record_id":"r1-11","synthetic":true,"release":"release_1","privacy_unit_id":"pu-11","age_band":"40-49","area":"Marlowe"}
+{"kind":"record","record_id":"r1-12","synthetic":true,"release":"release_1","privacy_unit_id":"pu-12","age_band":"40-49","area":"Marlowe"}
+{"kind":"record","record_id":"r1-13","synthetic":true,"release":"release_1","privacy_unit_id":"pu-13","age_band":"50-59","area":"Fernwick"}
+{"kind":"record","record_id":"r1-14","synthetic":true,"release":"release_1","privacy_unit_id":"pu-14","age_band":"50-59","area":"Fernwick"}
+{"kind":"record","record_id":"r1-15","synthetic":true,"release":"release_1","privacy_unit_id":"pu-15","age_band":"50-59","area":"Fernwick"}
+{"kind":"record","record_id":"r1-16","synthetic":true,"release":"release_1","privacy_unit_id":"pu-16","age_band":"50-59","area":"Marlowe"}
+{"kind":"record","record_id":"r1-17","synthetic":true,"release":"release_1","privacy_unit_id":"pu-17","age_band":"50-59","area":"Marlowe"}
+{"kind":"record","record_id":"r1-18","synthetic":true,"release":"release_1","privacy_unit_id":"pu-18","age_band":"50-59","area":"Marlowe"}
+{"kind":"record","record_id":"r1-19","synthetic":true,"release":"release_1","privacy_unit_id":"pu-19","age_band":"60-69","area":"Alderbrook"}
+{"kind":"record","record_id":"r1-20","synthetic":true,"release":"release_1","privacy_unit_id":"pu-20","age_band":"60-69","area":"Alderbrook"}
+{"kind":"record","record_id":"r1-21","synthetic":true,"release":"release_1","privacy_unit_id":"pu-21","age_band":"60-69","area":"Alderbrook"}
+{"kind":"record","record_id":"r1-22","synthetic":true,"release":"release_1","privacy_unit_id":"pu-22","age_band":"60-69","area":"Fernwick"}
+{"kind":"record","record_id":"r1-23","synthetic":true,"release":"release_1","privacy_unit_id":"pu-23","age_band":"60-69","area":"Fernwick"}
+{"kind":"record","record_id":"r1-24","synthetic":true,"release":"release_1","privacy_unit_id":"pu-24","age_band":"60-69","area":"Fernwick"}
+{"kind":"record","record_id":"r2-01","synthetic":true,"release":"release_2","privacy_unit_id":"pu-01","age_band":"30-34","area":"North"}
+{"kind":"record","record_id":"r2-02","synthetic":true,"release":"release_2","privacy_unit_id":"pu-02","age_band":"30-34","area":"North"}
+{"kind":"record","record_id":"r2-03","synthetic":true,"release":"release_2","privacy_unit_id":"pu-03","age_band":"35-39","area":"North"}
+{"kind":"record","record_id":"r2-04","synthetic":true,"release":"release_2","privacy_unit_id":"pu-04","age_band":"30-34","area":"North"}
+{"kind":"record","record_id":"r2-05","synthetic":true,"release":"release_2","privacy_unit_id":"pu-05","age_band":"35-39","area":"North"}
+{"kind":"record","record_id":"r2-06","synthetic":true,"release":"release_2","privacy_unit_id":"pu-06","age_band":"35-39","area":"North"}
+{"kind":"record","record_id":"r2-07","synthetic":true,"release":"release_2","privacy_unit_id":"pu-07","age_band":"40-44","area":"North"}
+{"kind":"record","record_id":"r2-08","synthetic":true,"release":"release_2","privacy_unit_id":"pu-08","age_band":"40-44","area":"North"}
+{"kind":"record","record_id":"r2-09","synthetic":true,"release":"release_2","privacy_unit_id":"pu-09","age_band":"40-44","area":"North"}
+{"kind":"record","record_id":"r2-10","synthetic":true,"release":"release_2","privacy_unit_id":"pu-10","age_band":"45-49","area":"South"}
+{"kind":"record","record_id":"r2-11","synthetic":true,"release":"release_2","privacy_unit_id":"pu-11","age_band":"45-49","area":"South"}
+{"kind":"record","record_id":"r2-12","synthetic":true,"release":"release_2","privacy_unit_id":"pu-12","age_band":"45-49","area":"South"}
+{"kind":"record","record_id":"r2-13","synthetic":true,"release":"release_2","privacy_unit_id":"pu-13","age_band":"50-54","area":"North"}
+{"kind":"record","record_id":"r2-14","synthetic":true,"release":"release_2","privacy_unit_id":"pu-14","age_band":"50-54","area":"North"}
+{"kind":"record","record_id":"r2-15","synthetic":true,"release":"release_2","privacy_unit_id":"pu-15","age_band":"50-54","area":"North"}
+{"kind":"record","record_id":"r2-16","synthetic":true,"release":"release_2","privacy_unit_id":"pu-16","age_band":"55-59","area":"South"}
+{"kind":"record","record_id":"r2-17","synthetic":true,"release":"release_2","privacy_unit_id":"pu-17","age_band":"55-59","area":"South"}
+{"kind":"record","record_id":"r2-18","synthetic":true,"release":"release_2","privacy_unit_id":"pu-18","age_band":"55-59","area":"South"}
+{"kind":"record","record_id":"r2-19","synthetic":true,"release":"release_2","privacy_unit_id":"pu-19","age_band":"60-64","area":"North"}
+{"kind":"record","record_id":"r2-20","synthetic":true,"release":"release_2","privacy_unit_id":"pu-20","age_band":"60-64","area":"North"}
+{"kind":"record","record_id":"r2-21","synthetic":true,"release":"release_2","privacy_unit_id":"pu-21","age_band":"65-69","area":"North"}
+{"kind":"record","record_id":"r2-22","synthetic":true,"release":"release_2","privacy_unit_id":"pu-22","age_band":"65-69","area":"North"}
+{"kind":"record","record_id":"r2-23","synthetic":true,"release":"release_2","privacy_unit_id":"pu-23","age_band":"65-69","area":"North"}
+{"kind":"record","record_id":"r2-24","synthetic":true,"release":"release_2","privacy_unit_id":"pu-24","age_band":"65-69","area":"North"}
diff --git a/tests/unit/risk/test_successive_release_fixture.py b/tests/unit/risk/test_successive_release_fixture.py
new file mode 100644
index 000000000..aae3eb811
--- /dev/null
+++ b/tests/unit/risk/test_successive_release_fixture.py
@@ -0,0 +1,54 @@
+"""Per-release k checks for the synthetic successive-release fixture."""
+
+from __future__ import annotations
+
+import json
+from pathlib import Path
+
+import pytest
+
+from openmed.risk import kanon_report
+
+FIXTURE = (
+    Path(__file__).resolve().parents[2]
+    / "fixtures"
+    / "risk"
+    / "successive_releases_v1.jsonl"
+)
+
+
+def _load() -> tuple[dict, dict[str, list[dict]]]:
+    rows = [
+        json.loads(line)
+        for line in FIXTURE.read_text(encoding="utf-8").splitlines()
+        if line.strip()
+    ]
+    meta = rows[0]
+    assert meta["kind"] == "meta"
+    releases: dict[str, list[dict]] = {}
+    for row in rows[1:]:
+        assert row["kind"] == "record"
+        assert row["synthetic"] is True
+        releases.setdefault(row["release"], []).append(row)
+    return meta, releases
+
+
+def test_fixture_is_synthetic_with_two_releases_of_20_to_40_rows() -> None:
+    meta, releases = _load()
+
+    assert meta["version"] == 1
+    assert meta["synthetic"] is True
+    assert sorted(releases) == ["release_1", "release_2"]
+    for rows in releases.values():
+        assert 20 <= len(rows) <= 40
+
+
+@pytest.mark.parametrize("release", ["release_1", "release_2"])
+def test_each_release_alone_meets_its_committed_k(release: str) -> None:
+    meta, releases = _load()
+
+    report = kanon_report(
+        releases[release], quasi_identifiers=meta["quasi_identifiers"]
+    )
+
+    assert report["k"] == meta["expected"]["k"][release]

=== plan.md ===
## Solution Approach

**Analysis**

The cause is a coverage gap, not a defect in code. `kanon_report` in `openmed/risk/kanon.py` takes one table, builds equivalence classes from the quasi-identifiers (`_equivalence_key`) and returns `k` (smallest class size) and `class_count`. It has no notion of a release, so it measures one release at a time, and my repro showed it works (35 tests pass). What is missing sits in test data: `tests/fixtures/risk/` has `quasi_identifier_uniqueness.jsonl` (one table, 4 records) and `negation_traps.jsonl`, and neither has a release field or a privacy-unit key. `tests/unit/risk/test_regression_suites.py` only loads those two files, and `tests/fixtures/risk/README.md` documents only their formats. So later composition work has no committed example where two releases are each safe alone but isolate rows when intersected.

**Proposed Solution**

Add exactly what issue #5295 asks for and change no library code.

- `tests/fixtures/risk/successive_releases_v1.jsonl`: a `meta` row (same shape as the existing fixtures, with the committed per-release k in `expected`) and two releases of one synthetic population, 20-40 rows each, plus a keyed privacy-unit column (`privacy_unit_id`) shared by both releases. The two releases generalize the quasi-identifiers differently. Every row is marked `synthetic: true` and holds invented values only: no real names, dates or places.
- `tests/unit/risk/test_successive_release_fixture.py` (about 40 lines): loads the fixture, checks every row is marked synthetic, runs `kanon_report` on each release alone with explicit `quasi_identifiers` (so the ID column stays out), and asserts the committed k for each.
- `tests/fixtures/risk/README.md`: a paragraph describing the format and the expected intersection result for later composition tests.

I am not changing `openmed/risk/` (composition scoring is out of scope per the issue), the existing fixtures, or the existing tests, and I am not adding anything the issue does not list: no extra test helpers, no CHANGELOG entry, no docs beyond the README paragraph.

**Implementation Plan**

1. Branch from the latest `master`: `test/issue-5295-successive-release-fixture`.
2. Design the population on paper: about 24 units, each with a `privacy_unit_id`. Release 1 and release 2 generalize the quasi-identifiers differently, so each release alone has k of at least 2 and the intersection leaves at least one unit alone in its class. Confirm the k values and the intersection with `kanon_report` and a throwaway script I do not commit.
3. Write the fixture with the per-release k in `meta.expected`.
4. Write the test file.
5. Add the README paragraph, including the expected intersection result.
6. Run `.venv/bin/python -m pytest tests/unit/risk/test_successive_release_fixture.py -q`, then my manifest checks (`ruff check`, `ruff format --check`, `pytest tests/unit/risk -q`) and `python scripts/release/check_repo_policy.py --commits origin/master HEAD`.
7. Commit with imperative `test:` and `docs:` messages, then open one PR with `Closes #5295`, following `.github/PULL_REQUEST_TEMPLATE.md` and listing the exact validation commands.

[Record deviations here as they happen: what changed mid-build and
why. A recorded deviation is honest work; silent drift is not.]

=== Test evidence ===
# Test evidence: openmed #5295 (successive-release fixture)

Run on 2026-11-17, macOS, Python 3.13.9, `.venv` from `pip install -e ".[dev]"`.
Branch `test/issue-5295-successive-release-fixture` (3 commits on `master`
`e8325586e`, which equals `upstream/master`).

## 1. Reproduction before the fix (`master`, `e8325586e`)

The issue reports a gap, not a crash: the fixture, its README contract and the
per-release test do not exist. Same steps as my story's Reproduction Process.

```text
$ ls tests/fixtures/risk/successive_releases_v1.jsonl tests/unit/risk/test_successive_release_fixture.py
ls: tests/fixtures/risk/successive_releases_v1.jsonl: No such file or directory
ls: tests/unit/risk/test_successive_release_fixture.py: No such file or directory

$ .venv/bin/python -m pytest tests/unit/risk/test_successive_release_fixture.py -q
ERROR: file or directory not found: tests/unit/risk/test_successive_release_fixture.py

no tests ran in 0.07s

$ grep -n -i "successive\|intersect" tests/fixtures/risk/README.md
(no output)

$ .venv/bin/python -m pytest tests/unit/risk/test_regression_suites.py tests/unit/risk/test_kanon.py -q
........uuu.....................uuuu.uu.....                             [100%]
35 passed, 9 subtests passed in 1.30s
```

A repo-wide `grep -rIl "successive_release"` on `master` matched only my
untracked local files (`CLAUDE.local.md`, `plan.md`, `plan-comment.md`) and
the pytest cache, and no tracked file.

## 2. Reproduction after the fix (branch, `8be36858a`)

```text
$ ls tests/fixtures/risk/successive_releases_v1.jsonl tests/unit/risk/test_successive_release_fixture.py
tests/fixtures/risk/successive_releases_v1.jsonl
tests/unit/risk/test_successive_release_fixture.py

$ .venv/bin/python -m pytest tests/unit/risk/test_successive_release_fixture.py -q
...                                                                      [100%]
3 passed in 0.13s

$ grep -n -i "successive\|intersect" tests/fixtures/risk/README.md
25:Record rows for `successive_releases_v1.jsonl` contain:
42:Expected intersection result for later composition tests: joining the two
46:`successive_releases_v1.jsonl` does not score composition; it only fixes the

$ .venv/bin/python -m pytest tests/unit/risk/test_regression_suites.py tests/unit/risk/test_kanon.py -q
........uuu.....................uuuu.uu.....                             [100%]
35 passed, 9 subtests passed in 0.98s
```

The issue's validation command (`.venv/bin/python -m pytest
tests/unit/risk/test_successive_release_fixture.py -q`) passes, and the 35
existing tests still pass.

## 3. The committed values, measured

`kanon_report` run on each release alone with `quasi_identifiers=["age_band",
"area"]`, and a plain join on `privacy_unit_id` (a throwaway script, not
committed) for the intersection:

```text
release_1 24 rows  k 3  classes 8  sizes [3, 3, 3, 3, 3, 3, 3, 3]
release_2 24 rows  k 2  classes 8  sizes [3, 3, 3, 3, 3, 3, 2, 4]
intersection k 1  isolated ['pu-03', 'pu-04', 'pu-21']
```

These match `meta.expected` in the fixture (`k` 3 and 2, intersection `k` 1,
isolated `pu-03`, `pu-04`, `pu-21`) and the README paragraph.

## 4. The test fails when the data is wrong

With one release-1 row changed (`pu-04` moved from `Fernwick` to a one-row
area), the k check fails:

```text
E       assert 1 == 3
FAILED tests/unit/risk/test_successive_release_fixture.py::test_each_release_alone_meets_its_committed_k[release_1]
1 failed, 2 passed in 0.13s
```

With the fixture file removed, all 3 test cases failed with a missing-file
error. I restored the file after both runs; the tree is clean.

## 5. Checks from my ship manifest (branch, `8be36858a`)

```text
$ .venv/bin/ruff check .
All checks passed!

$ .venv/bin/ruff format --check .
3623 files already formatted

$ .venv/bin/python -m pytest tests/unit/risk -q
.............uuuu................uuu................uuuuuu.              [100%]
543 passed, 308 subtests passed in 2.22s

$ python3 scripts/release/check_repo_policy.py --commits origin/master HEAD
Commit attribution policy passed: 3 commits checked

$ .venv/bin/python -m pytest tests/unit/risk/test_successive_release_fixture.py -v
...::test_fixture_is_synthetic_with_two_releases_of_20_to_40_rows PASSED [ 33%]
...::test_each_release_alone_meets_its_committed_k[release_1] PASSED [ 66%]
...::test_each_release_alone_meets_its_committed_k[release_2] PASSED [100%]
3 passed in 0.12s
```

Not run: `.venv/bin/mypy`. It is in my manifest's excluded table because it
fails on `master` before my change (numpy stubs need Python 3.12 syntax in
this `.venv`), and this change adds only a fixture, a test and a README
paragraph.

## 6. Diff

```text
 tests/fixtures/risk/README.md                      | 24 ++++++++++
 tests/fixtures/risk/successive_releases_v1.jsonl   | 49 ++++++++++++++++++++
 tests/unit/risk/test_successive_release_fixture.py | 54 ++++++++++++++++++++++
 3 files changed, 127 insertions(+)
```

Nothing under `openmed/risk/` changed.

=== The repo's PR template ===
# Pull Request

## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Test addition/improvement

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have tested this change with different models/inputs

## Documentation
- [ ] I have updated the documentation accordingly
- [ ] I have added docstrings to new functions/classes
- [ ] I have updated the CHANGELOG.md

## Code Quality
- [ ] I ran `make format`, `make lint`, and `make format-check`
- [ ] For Swift/OpenMedKit changes, I ran `make format-swift` and `make lint-swift`
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings

## Dependencies
- [ ] I have not added any new dependencies
- [ ] OR I have added new dependencies and they are justified because: ____

## Checklist
- [ ] I have read the [contributing guide](https://github.com/maziyarpanahi/openmed/blob/master/CONTRIBUTING.md), [Code of Conduct](https://github.com/maziyarpanahi/openmed/blob/master/CODE_OF_CONDUCT.md), and [maintainer guide](https://github.com/maziyarpanahi/openmed/blob/master/MAINTAINERS.md)
- [ ] My commits have clear, descriptive messages
- [ ] I have squashed/organized my commits appropriately

## Related Issues
Closes #(issue number)
Related to #(issue number)

## Screenshots/Examples
If applicable, add screenshots or example outputs to help explain your changes.

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

=== The issue thread ===
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

Thread at the time of the PR: the author's claim comment, then the plan comment; the owner assigned the issue to the author and asked that follow-ups stay on the pull request.

=== The ship manifest, as the gate ran it ===
Must-pass checks the gate ran, in order (all green): lint, format check, and the risk unit tests (`pytest tests/unit/risk -q`). Checks excluded by the author: none.
