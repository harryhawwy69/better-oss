import os
import subprocess
import sys

from conftest import ROOT

LEAK = ROOT / "scripts" / "leak_check.py"


def make_repo(tmp_path, files):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    for name, text in files.items():
        (tmp_path / name).write_text(text)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    return tmp_path


def leak(root, env=None):
    return subprocess.run([sys.executable, str(LEAK), str(root)], capture_output=True, text=True,
                          env={**os.environ, **(env or {})})


def test_the_repository_itself_is_clean():
    r = leak(ROOT)
    assert r.returncode == 0, r.stdout


def test_leak_check_catches_each_kind(tmp_path):
    # Built from pieces so this file does not trip the check itself.
    path = "/Us" + "ers/alice/project"
    mail = "alice" + "@" + "corp.io"
    token = "gh" + "p_" + "a" * 36
    repo = make_repo(tmp_path, {"a.md": f"see {path}/x\n", "b.md": f"mail {mail}\n", "c.md": f"key {token}\n"})
    r = leak(repo)
    assert r.returncode == 1
    for kind in ("home-directory path", "email address", "token"):
        assert kind in r.stdout
    assert token not in r.stdout, "tokens are masked in the report"


def test_leak_check_allows_safe_lookalikes(tmp_path):
    repo = make_repo(tmp_path, {
        "ok.md": "git clone git" + "@" + "github.com:o/r.git\nmail a" + "@" + "example.com\n"
                 "~/.claude/x and /ho" + "me/runner/work\n"})
    assert leak(repo).returncode == 0


def test_leak_check_flags_symlinks(tmp_path):
    repo = make_repo(tmp_path, {"real.md": "hello\n"})
    (repo / "link.md").symlink_to("real.md")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    r = leak(repo)
    assert r.returncode == 1 and "symlink" in r.stdout


def test_private_terms_come_from_the_environment_not_the_repo(tmp_path):
    repo = make_repo(tmp_path, {"a.md": "contains zebra here\n", "b.md": "also zebra\n"})
    assert leak(repo).returncode == 0
    flagged = leak(repo, {"LEAK_EXTRA_PATTERNS": "zebra"})
    assert flagged.returncode == 1 and "a.md" in flagged.stdout
    exempt = leak(repo, {"LEAK_EXTRA_PATTERNS": "zebra", "LEAK_ALLOW_FILES": "a.md,b.md"})
    assert exempt.returncode == 0


def test_allow_marker_skips_a_line(tmp_path):
    path = "/Us" + "ers/alice/x"
    assert leak(make_repo(tmp_path, {"a.md": f"{path}  leak-check: allow\n"})).returncode == 0


def test_no_tracked_symlinks_in_this_repo():
    out = subprocess.run(["git", "ls-files", "-s"], cwd=ROOT, text=True, capture_output=True).stdout
    assert not [ln for ln in out.splitlines() if ln.startswith("120000")]
