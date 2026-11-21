#!/usr/bin/env python3
"""Release helpers used by .github/workflows/release.yml (and runnable by hand).

  release_tools.py check vX.Y.Z    the tag, plugin.json, cli/package.json and the
                                   CHANGELOG heading must all agree on X.Y.Z
  release_tools.py notes X.Y.Z     print the release notes for that version
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALL_LINE = (
    "Install: `npx better-oss-cli init`, or `/plugin install better-oss --marketplace "
    "mobeloper/better-oss` inside Claude Code. See the "
    "[README](https://github.com/mobeloper/better-oss#readme)."
)


def versions() -> dict:
    return {
        "plugin.json": json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())["version"],
        "cli/package.json": json.loads((ROOT / "cli" / "package.json").read_text())["version"],
    }


def changelog_section(version: str):
    text = (ROOT / "CHANGELOG.md").read_text()
    m = re.search(r"^## \[" + re.escape(version) + r"\][^\n]*\n(.*?)(?=^## \[|\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else None


def check(tag: str) -> int:
    m = re.fullmatch(r"v(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)", tag)
    if not m:
        print(f"release: tag {tag!r} is not vX.Y.Z", file=sys.stderr)
        return 1
    version, problems = m.group(1), []
    for name, found in versions().items():
        if found != version:
            problems.append(f"{name} says {found}, the tag says {version}")
    if changelog_section(version) is None:
        problems.append(f"CHANGELOG.md has no '## [{version}]' heading")
    for p in problems:
        print(f"release: {p}", file=sys.stderr)
    if not problems:
        print(f"release: {tag} matches plugin.json, cli/package.json and CHANGELOG.md")
    return 1 if problems else 0


def notes(version: str) -> int:
    body = changelog_section(version)
    if body is None:
        print(f"release: no CHANGELOG section for {version}", file=sys.stderr)
        return 1
    print(body + "\n\n" + INSTALL_LINE)
    return 0


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in ("check", "notes"):
        print(__doc__, file=sys.stderr)
        return 2
    return check(sys.argv[2]) if sys.argv[1] == "check" else notes(sys.argv[2])


if __name__ == "__main__":
    sys.exit(main())
