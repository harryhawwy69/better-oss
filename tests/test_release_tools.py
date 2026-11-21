import subprocess
import sys

from conftest import ROOT

TOOL = ROOT / "scripts" / "release_tools.py"


def run(*args):
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True)


def test_current_version_is_consistent():
    import json
    version = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())["version"]
    r = run("check", f"v{version}")
    assert r.returncode == 0, r.stderr


def test_a_mismatched_tag_is_rejected():
    r = run("check", "v9.9.9")
    assert r.returncode == 1 and "plugin.json says" in r.stderr and "CHANGELOG.md has no" in r.stderr


def test_a_malformed_tag_is_rejected():
    assert run("check", "0.0.1").returncode == 1
    assert run("check", "release-1").returncode == 1


def test_notes_come_from_the_changelog_and_end_with_the_install_line():
    r = run("notes", "0.0.1")
    assert r.returncode == 0
    assert "### Added" in r.stdout and r.stdout.strip().endswith("(https://github.com/mobeloper/better-oss#readme).")
    assert "better-oss-cli init" in r.stdout


def test_notes_for_an_unknown_version_fail():
    assert run("notes", "9.9.9").returncode == 1
