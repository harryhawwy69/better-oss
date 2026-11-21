#!/usr/bin/env python3
"""init: set up your better-oss folder and check what the tools need.

Copies the shipped example files you are meant to make your own into
~/.claude/better-oss/ (or $BETTER_OSS_HOME), without overwriting anything
you already have, then reports whether the programs the tools call are
available.

  python3 init.py            create missing files, check prerequisites
  python3 init.py --force    overwrite your files with the shipped examples
  python3 init.py --check    check prerequisites only, create nothing

It never edits Claude Code's settings.json: the plugin's hooks come with
the plugin itself.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

# The personal files: yours to edit, read from your folder first.
PERSONAL_FILES = ["fit-profile.md", "search-strategy.md",
                  "voice-guide.md", "playbook.md"]

# Per repo, so init does not copy them: you place these in a clone.
PER_REPO_HINT = """Per repository, when you start work in a clone:
  cp {defaults}/ship-manifest.md <your clone>/ship-manifest.md
  cp {defaults}/claude-local-template.md <your clone>/CLAUDE.local.md
  echo ship-manifest.md >> <your clone>/.git/info/exclude
  echo CLAUDE.local.md >> <your clone>/.git/info/exclude
Then rewrite both for that repo and delete their EXAMPLE comments."""


def seed(force: bool) -> int:
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"better-oss folder: {paths.DATA_DIR}")
    for name in PERSONAL_FILES:
        src = paths.DEFAULTS_DIR / name
        dst = paths.DATA_DIR / name
        if not src.is_file():
            print(f"  MISSING shipped file {src} (reinstall the plugin)")
            return 1
        if dst.exists() and not force:
            print(f"  kept     {name} (already there)")
            continue
        shutil.copyfile(src, dst)
        print(f"  {'replaced' if dst.exists() and force else 'created '} "
              f"{name} (an EXAMPLE you should rewrite)")
    return 0


def _run(cmd: list[str]):
    try:
        return subprocess.run(cmd, capture_output=True, text=True,
                              timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return None


def check_tools() -> int:
    problems = 0
    print("prerequisites:")
    for tool, why in (("git", "reads your branch and diff"),
                      ("gh", "searches and reads GitHub"),
                      ("claude", "runs the model passes (Sonnet)")):
        if shutil.which(tool):
            print(f"  ok       {tool}")
        else:
            print(f"  MISSING  {tool}: {why}")
            problems += 1
    if shutil.which("gh"):
        proc = _run(["gh", "auth", "status"])
        if proc is not None and proc.returncode == 0:
            print("  ok       gh is logged in")
        else:
            print("  MISSING  gh login: run `gh auth login`")
            problems += 1
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Set up your better-oss folder.")
    ap.add_argument("--force", action="store_true",
                    help="overwrite your files with the shipped examples")
    ap.add_argument("--check", action="store_true",
                    help="check prerequisites only; create nothing")
    args = ap.parse_args()
    status = 0
    if not args.check:
        status = seed(args.force)
    problems = check_tools()
    if not args.check and status == 0:
        print()
        print(PER_REPO_HINT.format(defaults=paths.DEFAULTS_DIR))
    return 1 if (status or problems) else 0


if __name__ == "__main__":
    sys.exit(main())
