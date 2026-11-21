"""Shared helpers. Nothing here calls a model, and every subprocess gets a
throwaway BETTER_OSS_HOME so a test can never touch a real user folder."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core"))

VOICE = ROOT / "core" / "voice_guard" / "check_voice.py"
GATE = ROOT / "core" / "ship_gate" / "check_gate.py"
MONITOR = ROOT / "core" / "pr_monitor" / "monitor.py"
INIT = ROOT / "core" / "init.py"
SKILLS = ["issue-scout", "issue-select", "repro-check", "plan-check", "pr-precheck"]


@pytest.fixture
def home(tmp_path):
    """An empty better-oss folder."""
    d = tmp_path / "better-oss-home"
    d.mkdir()
    return d


@pytest.fixture
def run_script(home):
    def run(script, args=(), stdin="", cwd=None, env_extra=None):
        env = {**os.environ, "BETTER_OSS_HOME": str(home), "CLAUDE_CONFIG_DIR": str(home / "claude")}
        env.update(env_extra or {})
        return subprocess.run([sys.executable, str(script), *args], input=stdin, text=True,
                              capture_output=True, cwd=cwd or home, env=env, timeout=60)
    return run


def hook_input(command, cwd=".", tool="Bash"):
    return json.dumps({"tool_name": tool, "tool_input": {"command": command}, "cwd": str(cwd)})
