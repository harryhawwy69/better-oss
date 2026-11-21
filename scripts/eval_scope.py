#!/usr/bin/env python3
"""Which skill evaluations does a pull request need?

  python3 scripts/eval_scope.py BASE HEAD     prints `none`, `all`, or a comma-separated skill list

A change under skills/<name>/ needs that skill's evals. A change to the harness,
the cases or bases, the ship-gate (which runs pr-precheck), or this workflow
needs all of them. Anything else needs none. A skill with no cases (today,
issue-scout) is skipped and named on stderr so the gap stays visible.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALL_TRIGGERS = re.compile(r"^(evals/|scripts/eval_scope\.py$|core/ship_gate/check_gate\.py$|\.github/workflows/evals\.yml$)")


def skills_with_cases(root=ROOT):
    return sorted(p.name for p in (root / "evals" / "cases").iterdir() if p.is_dir() and any(p.glob("*.json")))


def scope(files, available):
    if any(ALL_TRIGGERS.match(f) for f in files):
        return sorted(available), []
    touched = {m.group(1) for f in files if (m := re.match(r"^skills/([^/]+)/", f))}
    return sorted(touched & set(available)), sorted(touched - set(available))


def main():
    base, head = sys.argv[1:3]
    files = subprocess.run(["git", "diff", "--name-only", f"{base}...{head}"], capture_output=True, text=True, check=True).stdout.split()
    available = skills_with_cases()
    run, skipped = scope(files, available)
    for s in skipped:
        print(f"eval_scope: skills/{s} changed but has no eval cases", file=sys.stderr)
    print("none" if not run else ("all" if run == available else ",".join(run)))


if __name__ == "__main__":
    main()
