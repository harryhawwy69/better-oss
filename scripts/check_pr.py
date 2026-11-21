#!/usr/bin/env python3
"""PR health: check a pull request against the rules in CONTRIBUTING.md.

Errors fail the check; warnings are shown but do not. No model calls, and the
untrusted PR title and body are read from the event file, never interpolated
into a shell.

  python3 scripts/check_pr.py --event "$GITHUB_EVENT_PATH" --base <sha> --head <sha>

Errors (draft PRs get warnings instead, so work in progress is not nagged):
  commit-prefix     every commit subject starts with [add], [update] or [fix]
  pr-description    Summary, Testing and "AI use" are filled in, not template text
  rubric-evidence   a rubric/procedure/evidence-guide change fills in all four
                    evidence bullets of the PR template
  changelog         a user-facing change touches CHANGELOG.md (label `skip-changelog` skips)
Warnings:
  linked-issue      the description closes an issue (Closes #N), or says why not
  tests             code under core/ or cli/bin changed with no test, eval or script change
  size              more than 800 changed lines: consider splitting
  sign-off          a commit lacks a Signed-off-by trailer (requested, not enforced)

Bots (dependabot) are exempt from the description, changelog and prefix checks.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PREFIX = re.compile(r"^\[(add|update|fix)\] \S")
RUBRIC_FILES = re.compile(r"^skills/[^/]+/(rubric\.md|procedure\.md|references/evidence-guide\.md)$")
USER_FACING = re.compile(r"^(skills/|core/|hooks/|commands/|defaults/|cli/bin/|cli/package\.json$)")
CODE = re.compile(r"^(core/|cli/bin/)")
TESTISH = re.compile(r"^(tests/|cli/test/|evals/|scripts/)")
SIZE_LIMIT = 800

# Text that ships in the PR template; a section that still says this is unfilled.
PLACEHOLDERS = (
    "what changed and why, in two or three sentences",
    "paste the commands you ran and their output",
    "how ai was used on this change, in your own words",
)
EVIDENCE_BULLETS = ("The case", "Before", "After", "A case that already graded correctly")


@dataclass
class Finding:
    level: str   # "error" | "warning"
    code: str
    message: str


def section(body: str, heading: str) -> str:
    """Text under the first heading that starts with `heading`, up to the next `## `."""
    m = re.search(r"^##+\s*" + re.escape(heading) + r"[^\n]*\n(.*?)(?=^##+\s|\Z)", body, re.S | re.M | re.I)
    return m.group(1).strip() if m else ""


def has_text(chunk: str, min_len: int = 12) -> bool:
    """True if the chunk has real content once comments and the template's own
    instruction lines are removed."""
    chunk = re.sub(r"<!--.*?-->", "", chunk, flags=re.S)
    kept = [ln for ln in chunk.splitlines() if not any(p in ln.lower() for p in PLACEHOLDERS)]
    return len(re.sub(r"[\s`#*_>\-]+", " ", "\n".join(kept)).strip()) >= min_len


def evaluate(title, body, labels, files, commits, changed_lines, draft=False, bot=False):
    """commits: list of (subject, message). Returns a list of Finding."""
    out = []
    err = "warning" if draft else "error"
    labels = {x.lower() for x in labels}
    body = body or ""

    if not bot:
        bad = [s for s, _ in commits if not s.startswith("Merge ") and not PREFIX.match(s)]
        if bad:
            out.append(Finding(err, "commit-prefix",
                               "Commit subjects must start with [add], [update] or [fix]: "
                               + "; ".join(repr(s[:60]) for s in bad[:3]) + ("..." if len(bad) > 3 else "")))

        problems = []
        if not has_text(section(body, "Summary")):
            problems.append("the Summary is empty or still the template text")
        if not has_text(section(body, "Testing")) or "```" in section(body, "Testing") and not re.search(
                r"```[a-z]*\n\s*\S", section(body, "Testing")):
            problems.append("Testing has no pasted commands or output")
        notes = section(body, "Notes for reviewers")
        ai = re.search(r"AI use:?\*{0,2}:?\s*(.+)", notes, re.I)
        if not ai or not has_text(ai.group(1), 3):
            problems.append('Notes for reviewers needs an "AI use:" line (say "none" if none)')
        if problems:
            out.append(Finding(err, "pr-description", "; ".join(problems) + ". See the PR template."))

        if any(RUBRIC_FILES.match(f) for f in files):
            ev = section(body, "Rubric change evidence")
            missing = []
            for name in EVIDENCE_BULLETS:
                m = re.search(r"\*\*" + re.escape(name) + r":?\*\*:?\s*(.*)", ev)
                if not m or len(m.group(1).strip()) < 8:
                    missing.append(name)
            if missing:
                out.append(Finding(err, "rubric-evidence",
                                   "This changes a rubric, procedure or evidence guide, so fill in the "
                                   "'Rubric change evidence' section: missing " + ", ".join(missing)
                                   + ". See 'Changing a rubric' in CONTRIBUTING.md."))

        if any(USER_FACING.match(f) for f in files) and "CHANGELOG.md" not in files and "skip-changelog" not in labels:
            out.append(Finding(err, "changelog",
                               "A user-facing change should add a line under Unreleased in CHANGELOG.md "
                               "(a maintainer can apply the `skip-changelog` label if it does not need one)."))

    if not bot and not re.search(r"\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+#\d+", body, re.I) \
            and not re.search(r"no (linked )?issue", body, re.I):
        out.append(Finding("warning", "linked-issue", "Link the issue this closes (`Closes #N`), or say there is none."))
    if any(CODE.match(f) for f in files) and not any(TESTISH.match(f) for f in files):
        out.append(Finding("warning", "tests", "Code changed but no test, eval or script changed with it."))
    if changed_lines > SIZE_LIMIT:
        out.append(Finding("warning", "size", f"{changed_lines} changed lines; consider splitting into smaller pull requests."))
    if not bot:
        unsigned = [s for s, m in commits if not s.startswith("Merge ") and "Signed-off-by:" not in m]
        if unsigned:
            out.append(Finding("warning", "sign-off", f"{len(unsigned)} commit(s) have no Signed-off-by (use `git commit -s`); requested, not enforced."))
    return out


# --------------------------------------------------------------------------- git + event

def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def gather(base, head):
    files = [f for f in git("diff", "--name-only", f"{base}...{head}").splitlines() if f]
    lines = 0
    for row in git("diff", "--numstat", f"{base}...{head}").splitlines():
        a, d, _ = row.split("\t", 2)
        lines += (int(a) if a.isdigit() else 0) + (int(d) if d.isdigit() else 0)
    commits = []
    for rec in git("log", "--format=%s%x1f%B%x1e", f"{base}..{head}").split("\x1e"):
        if rec.strip():
            subject, _, message = rec.strip().partition("\x1f")
            commits.append((subject.strip(), message))
    return files, lines, commits


def render(findings):
    if not findings:
        return "All pull request health checks passed."
    lines = ["| Level | Check | What to do |", "|---|---|---|"]
    lines += [f"| {f.level} | `{f.code}` | {f.message} |" for f in findings]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--event", required=True, help="path to the pull_request event JSON")
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", required=True)
    args = ap.parse_args()
    pr = json.loads(Path(args.event).read_text())["pull_request"]
    files, lines, commits = gather(args.base, args.head)
    login = (pr.get("user") or {}).get("login", "")
    findings = evaluate(pr.get("title", ""), pr.get("body") or "", [label["name"] for label in pr.get("labels", [])],
                        files, commits, lines, draft=bool(pr.get("draft")), bot=login.endswith("[bot]"))
    for f in findings:
        print(f"::{f.level} title={f.code}::{f.message}")
    text = render(findings)
    print(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as fh:
            fh.write("## Pull request health\n\n" + text + "\n")
    return 1 if any(f.level == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
