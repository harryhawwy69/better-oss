#!/usr/bin/env python3
"""Hygiene check: fail on personal data in tracked files.

Flags, in every tracked text file:
  - home-directory paths (a path under /Users or /home spells out a username)
  - email addresses
  - secret tokens (GitHub, npm, Anthropic, AWS keys, private key blocks)
and flags any tracked symlink (it dangles on other machines and leaks the
path it points at).

A line containing `leak-check: allow` is skipped.

The maintainer can add project-private terms WITHOUT committing them:

  LEAK_EXTRA_PATTERNS   a regex (case-insensitive) of extra terms to flag
  LEAK_ALLOW_FILES      comma-separated repo paths exempt from those extras
                        (for example a file that carries an author credit)

Usage: python3 scripts/leak_check.py [repo root]      exit 1 if anything is found
"""

import os
import re
import subprocess
import sys
from pathlib import Path

HARD = {
    "home-directory path": re.compile(r"/(?:Users|home)/(?!runner/)[A-Za-z0-9._-]+/"),
    "token": re.compile(
        r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|npm_[A-Za-z0-9]{30,}"
        r"|sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{40,}|AKIA[0-9A-Z]{16}"
        r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    ),
}
EMAIL = re.compile(r"(?<![\w.+-])([\w.+-]+)@([\w-]+(?:\.[\w-]+)+)")
FAKE_EMAIL_DOMAINS = ("example.com", "example.org", "example.net", "users.noreply.github.com")
ALLOW_MARK = "leak-check: allow"
SELF = "scripts/leak_check.py"


def tracked_files(root: Path):
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True).stdout
        return [p for p in out.decode().split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        skip = {".git", "node_modules", "__pycache__"}
        return [str(p.relative_to(root)) for p in root.rglob("*")
                if not (skip & set(p.parts)) and (p.is_file() or p.is_symlink())]


def mask(text: str) -> str:
    return text if len(text) < 12 else text[:6] + "..." + text[-2:]


def scan(root: Path):
    extra = os.environ.get("LEAK_EXTRA_PATTERNS", "").strip()
    extra_re = re.compile(extra, re.IGNORECASE) if extra else None
    exempt = {p.strip() for p in os.environ.get("LEAK_ALLOW_FILES", "").split(",") if p.strip()}
    hits = []
    for rel in tracked_files(root):
        path = root / rel
        if path.is_symlink():
            hits.append((rel, 0, "symlink", os.readlink(path)))
            continue
        if rel == SELF or not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(lines, 1):
            if ALLOW_MARK in line:
                continue
            for kind, rx in HARD.items():
                m = rx.search(line)
                if m:
                    hits.append((rel, n, kind, mask(m.group(0))))
            for m in EMAIL.finditer(line):
                local, domain = m.group(1), m.group(2).lower()
                if local == "git" or domain.endswith(FAKE_EMAIL_DOMAINS):
                    continue
                hits.append((rel, n, "email address", mask(m.group(0))))
            if extra_re and rel not in exempt:
                m = extra_re.search(line)
                if m:
                    hits.append((rel, n, "private term", mask(m.group(0))))
    return hits


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    hits = scan(root)
    for rel, n, kind, what in hits:
        print(f"{rel}:{n}: {kind}: {what}")
    print(f"leak-check: {len(hits)} problem(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
