import subprocess
import sys

import paths
from conftest import ROOT


def test_plugin_root_holds_the_shipped_folders():
    assert paths.PLUGIN_ROOT == ROOT
    assert (paths.SKILLS_DIR / "issue-select" / "SKILL.md").is_file()
    assert (paths.DEFAULTS_DIR / "voice-guide.md").is_file()


def test_user_file_prefers_yours_and_falls_back_to_the_example(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, "DATA_DIR", tmp_path)
    assert paths.user_file("voice-guide.md") == paths.DEFAULTS_DIR / "voice-guide.md"
    (tmp_path / "voice-guide.md").write_text("mine")
    assert paths.user_file("voice-guide.md") == tmp_path / "voice-guide.md"


def test_home_override_is_honored(tmp_path):
    code = "import paths; print(paths.DATA_DIR)"
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT / "core", text=True, capture_output=True,
                         env={"BETTER_OSS_HOME": str(tmp_path), "PATH": ""}).stdout.strip()
    assert out == str(tmp_path)


def test_is_example_detects_the_banner():
    assert paths.is_example("<!--\nEXAMPLE: copy me\n-->\n# x")
    assert paths.is_example("# title\n\n<!-- EXAMPLE: later in the file -->")
    assert not paths.is_example("# my own guide\n<!-- a normal comment -->")
