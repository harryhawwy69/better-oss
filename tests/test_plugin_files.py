import json
import re

from conftest import ROOT


def load(rel):
    return json.loads((ROOT / rel).read_text())


def test_manifests_are_valid_and_agree():
    plugin = load(".claude-plugin/plugin.json")
    market = load(".claude-plugin/marketplace.json")
    assert plugin["name"] == "better-oss"
    assert market["plugins"][0]["name"] == plugin["name"]
    assert market["plugins"][0]["source"] == "./"


def test_plugin_and_installer_versions_match():
    assert load(".claude-plugin/plugin.json")["version"] == load("cli/package.json")["version"]


def test_installer_package_shape():
    pkg = load("cli/package.json")
    assert pkg["name"] == "better-oss-cli"
    assert pkg["bin"] == {"better-oss-cli": "bin/better-oss.js"}
    assert "dependencies" not in pkg, "the installer has no dependencies"
    assert pkg["engines"]["node"].startswith(">=18")


def hook_commands():
    data = load("hooks/hooks.json")
    out = []
    for group in data["hooks"]["PreToolUse"]:
        assert group["matcher"] == "Bash"
        for h in group["hooks"]:
            assert h["type"] == "command"
            out.append(h)
    return out


def test_hooks_point_at_real_scripts():
    cmds = hook_commands()
    assert len(cmds) == 2
    for h in cmds:
        m = re.search(r'\$\{CLAUDE_PLUGIN_ROOT\}/(core/[\w/.-]+\.py)', h["command"])
        assert m, h["command"]
        assert (ROOT / m.group(1)).is_file(), m.group(1)
        assert isinstance(h["timeout"], int) and h["timeout"] > 0


def test_hook_timeouts_leave_room_for_the_scripts():
    """Claude Code ends a hook at its timeout and an ended hook lets the command
    through, so each script must finish (or stop itself) before that."""
    by_script = {re.search(r"/(\w+)\.py", h["command"]).group(1): h["timeout"] for h in hook_commands()}
    gate = (ROOT / "core/ship_gate/check_gate.py").read_text()
    budget = int(re.search(r"^HOOK_BUDGET_S = (\d+)", gate, re.M).group(1))
    assert budget < by_script["check_gate"]
    voice = (ROOT / "core/voice_guard/check_voice.py").read_text()
    per_call = int(re.search(r"timeout=(\d+)\)", voice).group(1))
    assert 2 * per_call < by_script["check_voice"], "two attempts must fit inside the hook timeout"


def test_the_model_is_pinned_everywhere():
    for rel in ("core/voice_guard/check_voice.py", "core/ship_gate/check_gate.py", "core/pr_monitor/monitor.py"):
        assert re.search(r'^MODEL = "sonnet"$', (ROOT / rel).read_text(), re.M), rel


def test_commands_exist_and_have_descriptions():
    for name in ("init", "ship-gate", "monitor"):
        text = (ROOT / "commands" / f"{name}.md").read_text()
        assert text.startswith("---\n") and "description:" in text.split("---")[1]
