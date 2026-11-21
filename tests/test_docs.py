import re
import subprocess

from conftest import ROOT

COMMUNITY = ["README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md",
             "GOVERNANCE.md", "CHANGELOG.md", "LICENSE", "AGENTS.md", "CLAUDE.md",
             "docs/architecture.md", "docs/adding-a-skill.md", "docs/MAINTAINING.md",
             ".github/PULL_REQUEST_TEMPLATE.md", ".github/CODEOWNERS", ".github/dependabot.yml"]


def tracked_markdown():
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT, text=True, capture_output=True).stdout.split()
    return [ROOT / p for p in out if not p.startswith("defaults/")]


def test_community_and_docs_files_exist():
    for rel in COMMUNITY:
        assert (ROOT / rel).is_file(), rel


def test_claude_md_imports_agents_md_first():
    first = next(ln for ln in (ROOT / "CLAUDE.md").read_text().splitlines() if ln.strip())
    assert first.strip() == "@AGENTS.md"


def test_agents_md_stays_short():
    assert len((ROOT / "AGENTS.md").read_text().splitlines()) <= 100


def test_every_relative_markdown_link_resolves():
    broken = []
    for f in tracked_markdown():
        for url in re.findall(r"\]\(([^)\s]+)\)", f.read_text()):
            if re.match(r"(https?:|mailto:|#)", url):
                continue
            if not (f.parent / url.split("#")[0]).resolve().exists():
                broken.append(f"{f.relative_to(ROOT)} -> {url}")
    assert not broken, broken


def test_readme_installs_the_plugin_and_names_the_installer_package():
    text = (ROOT / "README.md").read_text()
    assert "/plugin install better-oss --marketplace mobeloper/better-oss" in text
    assert "npx better-oss-cli init" in text
    assert len(text.split()) >= 40


def test_no_doc_still_says_the_old_npm_name():
    for f in tracked_markdown() + [ROOT / ".github/ISSUE_TEMPLATE/bug_report.yml"]:
        assert not re.search(r"npx better-oss(?!-cli)\b", f.read_text()), f
