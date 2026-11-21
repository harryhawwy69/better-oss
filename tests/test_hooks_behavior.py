"""The guards, run as Claude Code runs them: JSON on stdin, exit code out.
Exit 2 blocks the command; anything else lets it through. No model calls."""

import json

from conftest import GATE, MONITOR, VOICE, hook_input


def test_voice_guard_ignores_commands_that_send_nothing(run_script):
    r = run_script(VOICE, stdin=hook_input("ls -la"))
    assert (r.returncode, r.stdout, r.stderr) == (0, "", "")


def test_voice_guard_ignores_other_tools(run_script):
    assert run_script(VOICE, stdin=hook_input("gh issue comment 1 --web", tool="Read")).returncode == 0


def test_voice_guard_stops_what_it_cannot_read(run_script):
    for cmd in ("gh issue comment 1 --web", "gh pr comment 1 --body-file nope.md", "gh issue create --title t"):
        r = run_script(VOICE, stdin=hook_input(cmd))
        assert r.returncode == 2 and "voice-guard: STOP" in r.stderr, cmd


def test_voice_guard_logs_to_the_users_folder_not_the_plugin(run_script, home):
    run_script(VOICE, stdin=hook_input("gh issue comment 1 --web"))
    assert "browser posting skips the guard" in (home / "guard-log.md").read_text()


def test_ship_gate_ignores_other_commands(run_script):
    r = run_script(GATE, stdin=hook_input("git status"))
    assert (r.returncode, r.stdout, r.stderr) == (0, "", "")


def test_ship_gate_stops_forms_it_cannot_check(run_script):
    for cmd in ("gh pr create --web", "gh pr create", "gh pr create --fill", "gh pr create --title t"):
        r = run_script(GATE, stdin=hook_input(cmd))
        assert r.returncode == 2 and "ship-gate: STOP" in r.stderr, cmd


def test_ship_gate_outside_a_clone_stops_and_says_why(run_script, tmp_path):
    r = run_script(GATE, stdin=hook_input("gh pr create --title t --body hello", cwd=tmp_path), cwd=tmp_path)
    assert r.returncode == 2 and "not inside a git clone" in r.stderr


def test_ship_gate_fails_closed_on_a_crash(run_script):
    """A hook that crashes exits 1 and Claude Code would let the PR through, so
    every unexpected error must come out as a stop (exit 2)."""
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": "gh pr create --title t --body b"}, "cwd": 5})
    r = run_script(GATE, stdin=payload)
    assert r.returncode == 2 and "crashed" in r.stderr


def test_ship_gate_by_hand_needs_a_branch_flag(run_script):
    assert run_script(GATE, args=["--title", "x"]).returncode == 2


def test_monitor_state_outside_a_clone_stops(run_script, tmp_path):
    r = run_script(MONITOR, args=["--state"], cwd=tmp_path)
    assert r.returncode == 2 and "not inside a git clone" in r.stderr


def test_monitor_only_allows_read_only_gh_calls():
    import re
    from conftest import ROOT
    src = (ROOT / "core/pr_monitor/monitor.py").read_text()
    allow = re.search(r"^READONLY_GH = (\{.*\})", src, re.M).group(1)
    assert allow == '{("auth", "status"), ("pr", "view"), ("repo", "view")}'
