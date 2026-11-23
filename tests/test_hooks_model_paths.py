"""The guards' model paths, with a fake `claude` on PATH.

Everything here runs with no model, no network and no credentials: the fake
CLI answers from the environment, so a deliberately wrong verdict makes a
test fail (issue #20). Exit 2 blocks the command; anything else lets it
through.
"""

import json
import os
from pathlib import Path

import pytest

from conftest import VOICE, hook_input

FAKEBIN = Path(__file__).resolve().parent / "fakebin"


@pytest.fixture
def fake_claude(run_script):
    """Put the fake CLI first on PATH and return a helper for its verdict."""
    assert os.access(FAKEBIN / "claude", os.X_OK), "tests/fakebin/claude is not executable"

    def run(script, args=(), stdin="", cwd=None, verdict=None, json_body=None,
            exit_code=None, env_extra=None):
        env = {**os.environ, "PATH": f"{FAKEBIN}:{os.environ['PATH']}"}
        if verdict is not None:
            env["FAKE_CLAUDE_VERDICT"] = verdict
        if json_body is not None:
            env["FAKE_CLAUDE_JSON"] = json.dumps(json_body)
        if exit_code is not None:
            env["FAKE_CLAUDE_EXIT"] = str(exit_code)
        env.update(env_extra or {})
        return run_script(script, args=args, stdin=stdin, cwd=cwd, env_extra=env)

    return run


def _run(fake_claude, command, **verdict):
    return fake_claude(VOICE, stdin=hook_input(command), **verdict)


def test_a_clean_draft_passes(fake_claude):
    r = _run(fake_claude, "gh issue comment 1 --body 'I could not reproduce this.'")

    assert r.returncode == 0
    assert "voice-guard: pass" in r.stdout


def test_a_draft_that_breaks_a_rule_stops_with_the_rule_quoted(fake_claude):
    r = _run(
        fake_claude,
        "gh issue comment 1 --body 'this is a draft'",
        json_body={
            "verdict": "stop",
            "rule": "State the version you tested.",
            "where": "this is a draft",
        },
    )

    assert r.returncode == 2
    assert "voice-guard: STOP" in r.stderr
    assert "State the version you tested." in r.stderr
    assert "this is a draft" in r.stderr


def test_a_stop_verdict_with_no_rule_quotes_the_placeholder(fake_claude):
    """The guard must not invent a rule the checker did not send."""
    r = _run(fake_claude, "gh issue comment 1 --body 'x'", verdict="stop")

    assert r.returncode == 2
    assert "(rule not quoted)" in r.stderr


def test_a_failing_checker_fails_closed(fake_claude):
    """A model that errors blocks the post: an unread draft must not pass."""
    r = _run(fake_claude, "gh issue comment 1 --body 'x'", exit_code=1)

    assert r.returncode == 2
    assert "the check could not run" in r.stderr
    assert "claude exited 1" in r.stderr


def test_the_manual_mode_uses_the_same_contract(fake_claude, home):
    draft = home / "draft.md"
    draft.write_text("I could not reproduce this.\n")

    r = fake_claude(VOICE, args=("--draft", str(draft)))

    assert r.returncode == 0
    assert "voice-guard: pass" in r.stdout


def test_a_broken_decision_is_caught_by_the_tests(fake_claude):
    """The mutation the issue asks for: a reject read as a pass must fail.

    If someone changed `check_draft` to treat a stop verdict as a pass, this
    is the test that goes red.
    """
    r = _run(
        fake_claude,
        "gh issue comment 1 --body 'x'",
        json_body={"verdict": "stop", "rule": "Never say this."},
    )
    assert r.returncode == 2, "a stop verdict must block the command"
    assert r.stdout == "", "a blocked draft must not print the pass line"
