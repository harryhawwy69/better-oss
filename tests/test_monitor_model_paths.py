"""The pr-monitor's drafting path, with fake `claude` and `gh` on PATH.

Issue #20: the model paths could not be tested without a real model, and the
monitor was the last one uncovered. It reads PR state through `gh`, which the
code already restricts to a read-only allowlist, so a fake can answer every
form it is allowed to run and refuse the rest.
"""

import json
import os
import subprocess

import pytest

from conftest import FAKEBIN, MONITOR

# A PR quiet long enough that the monitor drafts a polite nudge rather than
# reporting nothing-new or feedback-in.
def _pr_json(**overrides):
    pr = {
        "number": 7,
        "title": "Add a thing",
        "url": "https://github.com/example-org/example-lib/pull/7",
        "state": "OPEN",
        "isDraft": False,
        "author": {"login": "someone"},
        "baseRefName": "main",
        "headRefName": "feature",
        "headRefOid": "abc123",
        "mergeable": "MERGEABLE",
        "mergeStateStatus": "CLEAN",
        "reviewDecision": "",
        "createdAt": "2026-11-01T00:00:00Z",
        "updatedAt": "2026-11-01T00:00:00Z",
        "closedAt": None,
        "mergedAt": None,
        "statusCheckRollup": [],
        "comments": [],
        "reviews": [],
        "commits": [{"messageHeadline": "Add a thing"}],
        "body": "A change.",
    }
    pr.update(overrides)
    return json.dumps(pr)


@pytest.fixture
def pr_clone(tmp_path):
    """A clone on a branch, with a filled playbook and both fakes on PATH."""
    root = tmp_path / "clone"
    root.mkdir()

    def git(*args):
        subprocess.run(["git", *args], cwd=root, check=True,
                       capture_output=True, text=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "test@example.com")
    git("config", "user.name", "Test")
    (root / "README.rst").write_text("base\n")
    git("add", "-A")
    git("commit", "-q", "-m", "base")
    git("checkout", "-q", "-b", "feature")

    home = tmp_path / "home"
    home.mkdir()
    (home / "playbook.md").write_text(
        "# Playbook\n\n## Response rules\nAnswer within two days.\n\n"
        "## Staleness thresholds\nNudge after seven quiet days.\n\n"
        "## Nudge etiquette\nOne nudge, then stop.\n\n"
        "## Walk-away criteria\nWalk away after thirty days.\n"
    )
    return root, home


def monitor(root, home, *, pr_json=None, no_pr=False, draft=None,
            draft_text=None, gh_login="someone"):
    env = {
        **os.environ,
        "BETTER_OSS_HOME": str(home),
        "CLAUDE_CONFIG_DIR": str(home / "claude"),
        "PATH": f"{FAKEBIN}:{os.environ['PATH']}",
        "FAKE_GH_LOGIN": gh_login,
    }
    if pr_json is not None:
        env["FAKE_GH_PR_JSON"] = pr_json
    if no_pr:
        env["FAKE_GH_NO_PR"] = "1"
    if draft_text is not None:
        env["FAKE_CLAUDE_TEXT"] = draft_text
    elif draft is not None:
        env["FAKE_CLAUDE_JSON"] = json.dumps(draft)
    return subprocess.run(
        ["python3", str(MONITOR)], cwd=root, env=env,
        text=True, capture_output=True, timeout=120,
    )


def _draft(home) -> str:
    return (home / "drafted-move.md").read_text(encoding="utf-8")


def test_a_quiet_pr_gets_a_draft_file_and_never_posts(pr_clone):
    root, home = pr_clone

    r = monitor(root, home, pr_json=_pr_json())

    assert r.returncode == 0, r.stderr
    # The draft lands in a file the author posts by hand; nothing is sent.
    assert "A DRAFT" in _draft(home)
    assert "polite nudge" in r.stdout.lower()


def test_the_draft_is_marked_as_not_posted(pr_clone):
    """The monitor's whole contract: it drafts, the author posts."""
    root, home = pr_clone

    monitor(root, home, pr_json=_pr_json())

    assert "Nothing has been posted" in _draft(home)


def test_no_pr_yet_is_free_and_writes_no_new_draft(pr_clone):
    root, home = pr_clone

    r = monitor(root, home, no_pr=True)

    assert r.returncode == 0, r.stderr
    assert "NO PR YET" in (home / "run-report.md").read_text()


def test_someone_elses_pr_stops_before_any_model_call(pr_clone):
    """Drafting a reply to someone else's PR is the monitor's hard line."""
    root, home = pr_clone

    pr = _pr_json(author={"login": "someone-else"})
    r = monitor(root, home, pr_json=pr, gh_login="me")

    assert r.returncode == 2
    assert "opened by someone-else" in r.stderr


def test_an_unparseable_gh_answer_stops_rather_than_guessing(pr_clone):
    root, home = pr_clone

    r = monitor(root, home, pr_json="{not json")

    assert r.returncode == 2
    assert "could not parse" in r.stderr


def test_a_draft_that_names_another_move_is_reported_as_written(pr_clone):
    """`move_from_draft` decides the move from the MOVE line the model wrote."""
    root, home = pr_clone

    r = monitor(root, home, pr_json=_pr_json(),
                draft_text="MOVE: rebase plan\n\nThe branch is behind main.")

    assert "drafted move (rebase plan (via the polite nudge form))" in r.stdout
