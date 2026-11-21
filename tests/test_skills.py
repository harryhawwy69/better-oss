import re

import pytest

from conftest import ROOT, SKILLS

REQUIRED = ["SKILL.md", "rubric.md", "scope.md", "references/evidence-guide.md"]


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    assert m, "no frontmatter"
    return dict(line.split(": ", 1) for line in m.group(1).splitlines() if ": " in line)


def test_exactly_the_five_skills_exist():
    assert sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir()) == sorted(SKILLS)


@pytest.mark.parametrize("skill", SKILLS)
def test_skill_files_and_frontmatter(skill):
    base = ROOT / "skills" / skill
    for rel in REQUIRED:
        assert (base / rel).is_file(), f"{skill}/{rel}"
    fm = frontmatter((base / "SKILL.md").read_text())
    assert fm["name"] == skill
    assert len(fm["description"]) > 40 and "Use when" in fm["description"]


@pytest.mark.parametrize("skill", SKILLS)
def test_rubric_has_checks_and_a_verdict_rule(skill):
    text = (ROOT / "skills" / skill / "rubric.md").read_text()
    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    rows = [ln for ln in body.splitlines() if ln.startswith("|")]
    checks = [r for r in rows if [c.strip().lower() for c in r.strip("|").split("|")][-1] in ("required", "preferred")]
    assert checks, "no check rows with a required/preferred weight"
    assert any(re.search(r"\|\s*required\s*\|?\s*$", r, re.I) for r in checks), "needs a required check"
    verdict = body.split("## Verdict rule", 1)
    assert len(verdict) == 2 and verdict[1].strip(), "no verdict rule"


@pytest.mark.parametrize("skill", SKILLS)
def test_skill_ends_with_the_json_contract(skill):
    text = (ROOT / "skills" / skill / "SKILL.md").read_text()
    for field in ('"checks"', '"verdict"', "accept|reject", "pass|fail|unclear"):
        assert field in text, f"{skill}: output contract is missing {field}"


def test_pr_precheck_keeps_the_layout_the_gate_reads():
    gate = (ROOT / "core/ship_gate/check_gate.py").read_text()
    for rel in re.findall(r'"(?:skill|rubric|procedure|evidence)": "([^"]+)"', gate):
        assert (ROOT / "skills/pr-precheck" / rel).is_file(), rel
    assert (ROOT / "skills/pr-precheck/CONTRACT.md").is_file()


def test_skills_never_read_a_personal_file_from_inside_the_plugin():
    """Personal files live in the user's folder; the skills may only name them
    as a user file with a fallback to defaults/."""
    for skill in SKILLS:
        text = (ROOT / "skills" / skill / "SKILL.md").read_text()
        for name in ("fit-profile.md", "voice-guide.md", "search-strategy.md"):
            if name in text:
                assert "~/.claude/better-oss" in text, f"{skill} names {name} without saying where it lives"
