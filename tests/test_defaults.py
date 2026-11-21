import re

import pytest

from conftest import ROOT

DEFAULTS = ROOT / "defaults"
BANNERED = ["fit-profile.md", "search-strategy.md", "voice-guide.md", "playbook.md",
            "ship-manifest.md", "claude-local-template.md"]


def personal_files_in_init():
    block = re.search(r"PERSONAL_FILES = \[(.*?)\]", (ROOT / "core/init.py").read_text(), re.S).group(1)
    return re.findall(r'"([^"]+)"', block)


@pytest.mark.parametrize("name", BANNERED)
def test_default_is_prefilled_and_keeps_its_example_banner(name):
    text = (DEFAULTS / name).read_text()
    assert re.search(r"<!--\s*EXAMPLE:", text), f"{name} lost its EXAMPLE banner"
    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    assert len(body.strip()) >= 300, f"{name} looks blank"


def test_defaults_are_real_files_not_symlinks():
    for p in DEFAULTS.rglob("*"):
        assert not p.is_symlink(), p


def test_init_only_seeds_files_that_exist_and_are_bannered():
    for name in personal_files_in_init():
        assert (DEFAULTS / name).is_file()
        assert name in BANNERED


def test_templates_are_non_empty_and_marked():
    templates = sorted((DEFAULTS / "templates").glob("*.md"))
    assert len(templates) == 6
    for t in templates:
        assert t.read_text().lstrip().startswith("<!--\nTEMPLATE:"), t.name


def test_search_strategy_uses_the_date_placeholder_not_a_fixed_date():
    text = (DEFAULTS / "search-strategy.md").read_text()
    assert "{90_DAYS_AGO}" in text
    assert not re.search(r'--updated ">\d{4}-\d{2}-\d{2}"', text)
