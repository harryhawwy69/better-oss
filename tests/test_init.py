import re

from conftest import INIT, ROOT


def test_init_seeds_the_four_files_without_overwriting(run_script, home):
    r = run_script(INIT)
    for name in ("fit-profile.md", "search-strategy.md", "voice-guide.md", "playbook.md"):
        assert (home / name).is_file()
    assert "created" in r.stdout
    (home / "voice-guide.md").write_text("mine\n")
    again = run_script(INIT)
    assert (home / "voice-guide.md").read_text() == "mine\n"
    assert re.search(r"kept\s+voice-guide.md", again.stdout)


def test_init_force_replaces(run_script, home):
    run_script(INIT)
    (home / "playbook.md").write_text("mine\n")
    run_script(INIT, args=["--force"])
    assert "EXAMPLE:" in (home / "playbook.md").read_text()


def test_init_never_writes_outside_its_folder(run_script, home):
    run_script(INIT)
    assert not (home / "claude" / "settings.json").exists()


def test_installer_and_init_agree_on_the_file_list():
    js = (ROOT / "cli/bin/better-oss.js").read_text()
    py = (ROOT / "core/init.py").read_text()
    js_files = re.findall(r"'([\w-]+\.md)'", re.search(r"const PERSONAL_FILES = \[(.*?)\];", js, re.S).group(1))
    py_files = re.findall(r'"([\w-]+\.md)"', re.search(r"PERSONAL_FILES = \[(.*?)\]", py, re.S).group(1))
    assert js_files == py_files
