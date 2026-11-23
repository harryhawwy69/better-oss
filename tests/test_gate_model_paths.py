"""The ship-gate's own paths, with a fake `claude` on PATH.

Issue #20: the model paths could not be tested without a real model. Here the
fake CLI answers pr-precheck from the environment, so a rejected pull request,
an accepted one, and a failing repo check are all reachable with no network and
no credentials. Exit 2 blocks the pull request; 0 lets it through.
"""

import json
import os
import subprocess
from pathlib import Path

import pytest

from conftest import GATE

FAKEBIN = Path(__file__).resolve().parent / "fakebin"

MANIFEST = """# Ship manifest: example-org/example-lib

## Must pass before a ship

| Check | Command | Source |
|---|---|---|
| {name} | `{cmd}` | CONTRIBUTING.md, "Running tests" |

## Excluded, with a dated reason

| Check | Command | Date | Why it doesn't count against this PR |
|---|---|---|---|
"""


def _git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True,
                          capture_output=True, text=True)


@pytest.fixture
def clone(tmp_path):
    """A real clone: a main branch and a feature branch one commit ahead."""
    root = tmp_path / "clone"
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    (root / "README.rst").write_text("base\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    _git(root, "checkout", "-q", "-b", "feature")
    (root / "README.rst").write_text("changed\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "change")
    (root / "ship-manifest.md").write_text(MANIFEST.format(name="Tests", cmd="true"))
    return root


def gate(home, root, verdict=None, json_body=None, exit_code=None):
    """Run the ship-gate by hand, with the fake CLI first on PATH."""
    env = {**os.environ, "BETTER_OSS_HOME": str(home),
           "CLAUDE_CONFIG_DIR": str(home / "claude"),
           "PATH": f"{FAKEBIN}:{os.environ['PATH']}"}
    if verdict is not None:
        env["FAKE_CLAUDE_VERDICT"] = verdict
    if json_body is not None:
        env["FAKE_CLAUDE_JSON"] = json.dumps(json_body)
    if exit_code is not None:
        env["FAKE_CLAUDE_EXIT"] = str(exit_code)
    return subprocess.run(
        [os.environ.get("PYTHON", "python3"), str(GATE), "--branch"],
        cwd=root, env=env, text=True, capture_output=True, timeout=120,
    )


def _precheck(verdict, checks=None):
    return {"verdict": verdict, "checks": checks or []}


def test_a_failing_repo_check_blocks_before_the_model_runs(home, clone, fake_claude):
    """The manifest's own check runs first; a red one stops the PR."""
    (clone / "ship-manifest.md").write_text(
        MANIFEST.format(name="Tests", cmd="false"))

    r = gate(home, clone)

    assert r.returncode == 2
    assert "the repo's own check `Tests` failed" in r.stderr
    assert "`false` exited 1" in r.stderr


def test_a_rejected_pr_precheck_blocks_and_quotes_the_failing_checks(home, clone):
    r = gate(home, clone, json_body=_precheck("reject", [
        {"name": "Tests are attached", "grade": "fail",
         "evidence": "no test file in the diff"},
        {"name": "Scope", "grade": "pass", "evidence": "one file"},
    ]))

    assert r.returncode == 2
    assert "pr-precheck rejected" in r.stderr
    assert "Tests are attached [fail]: no test file in the diff" in r.stderr
    assert "Scope [pass]" not in r.stderr


def test_an_accepted_pr_precheck_passes(home, clone):
    r = gate(home, clone, json_body=_precheck("accept", [
        {"name": "Tests are attached", "grade": "pass",
         "evidence": "test_hooks_model_paths.py"},
    ]))

    assert r.returncode == 0, r.stderr
    assert "ship-gate: PASS" in r.stdout
    assert "Tests are attached [pass]" in r.stdout


def test_a_model_that_errors_blocks(home, clone):
    """Fail closed: pr-precheck that cannot run must not wave the PR through."""
    r = gate(home, clone, exit_code=1)

    assert r.returncode == 2
    assert "pr-precheck could not finish its run" in r.stderr


def test_a_reject_treated_as_a_pass_would_be_caught(home, clone):
    """The mutation the issue asks for: reject must not read as accept."""
    r = gate(home, clone, json_body=_precheck("reject"))
    assert r.returncode == 2
    assert "ship-gate: PASS" not in r.stdout
