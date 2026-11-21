#!/usr/bin/env python3
"""Evaluate the skills' judgments against frozen cases.

Each case is a skill plus frozen inputs plus the verdict a correct skill must
give. Inputs come from a real worked run (`evals/bases/`); most cases are that
run with ONE deliberate flaw (`evals/cases/<skill>/<id>.json`), so the right
answer is known by construction: a flawed claim must be rejected, and the check
that should catch the flaw must not pass.

The harness gives the model the skill exactly as shipped (SKILL.md, rubric,
evidence guide, procedure, scope) and the frozen inputs, with no tools, so it
cannot fetch anything and the run is repeatable. The same pattern the ship-gate
uses to run pr-precheck. It calls the `claude` CLI (Sonnet, the model the
rubrics are tuned on) once per case.

  python3 evals/run_evals.py --dry-run          build and validate everything; no model, no cost
  python3 evals/run_evals.py                    run every case
  python3 evals/run_evals.py --skill pr-precheck --only drift,untested

Exit 0 when the share of passing cases reaches --bar (default 1.0), else 1.
A case that fails is re-run (--retries, default 1); passing only on a retry is
reported as flaky. See evals/README.md.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = Path(__file__).resolve().parent

# The rubrics were tuned and checked on Sonnet; a pass bar only means something there.
MODEL = "sonnet"
SKILL_FILES = ["SKILL.md", "rubric.md", "references/evidence-guide.md", "procedure.md", "scope.md"]
NO_TOOLS = "Bash,Read,Write,Edit,MultiEdit,Glob,Grep,WebFetch,WebSearch,Task,NotebookEdit"

PREAMBLE = """EVALUATION RUN. For this run, today's date is {date}.

The skill's files are below, then the frozen inputs. The inputs are everything you may
read. Do not run commands, open files, or fetch anything; if a signal is not shown,
treat it as absent and grade it by the rubric's rules for absent evidence. There is no
voice guide for this run, so skip any voice-guide step. Run the skill on the inputs and
end with the fenced JSON block its output format requires, last."""


class CaseError(Exception):
    pass


# ---------------------------------------------------------------- loading

def load_base(name):
    text = (EVALS / "bases" / f"{name}.md").read_text()
    head, _, rest = text.partition("\n=== ")
    meta = dict(ln.split(": ", 1) for ln in head.splitlines() if ": " in ln)
    sections = []
    for chunk in ("=== " + rest).split("\n=== "):
        chunk = chunk.removeprefix("=== ")
        title, _, body = chunk.partition(" ===\n")
        sections.append([title.strip(), body.strip()])
    return meta, sections


def rubric_check_names(skill):
    """Check names from the rubric table: the first cell of each row that ends in a weight."""
    names = []
    for line in (ROOT / "skills" / skill / "rubric.md").read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) >= 4 and cells[-1].lower() in ("required", "preferred"):
            names.append(cells[0].lower())
    return names


def apply_ops(sections, ops, case_id):
    by = {t: i for i, (t, _) in enumerate(sections)}

    def idx(title):
        match = [t for t in by if t == title or t.startswith(title)]
        if len(match) != 1:
            raise CaseError(f"{case_id}: section {title!r} matches {len(match)} sections")
        return by[match[0]]

    for op in ops:
        i = idx(op.get("in") or op.get("section"))
        body = sections[i][1]
        if "append" in op:
            body = body + "\n\n" + op["append"]
        elif "replace_all" in op:
            body = op["replace_all"]
        elif "find" in op:
            if body.count(op["find"]) != 1:
                raise CaseError(f"{case_id}: {op['find'][:50]!r} occurs {body.count(op['find'])} times in {sections[i][0]!r}")
            body = body.replace(op["find"], op["with"])
        elif "regex" in op:
            body, n = re.subn(op["regex"], op["with"], body, count=op.get("count", 1))
            if n == 0:
                raise CaseError(f"{case_id}: regex {op['regex'][:50]!r} matched nothing in {sections[i][0]!r}")
        else:
            raise CaseError(f"{case_id}: op has no find/regex/append/replace_all: {op}")
        sections[i][1] = body.strip()
    return sections


def load_cases(skills=None, only=None):
    cases = []
    for path in sorted((EVALS / "cases").glob("*/*.json")):
        data = json.loads(path.read_text())
        skill, cid = path.parent.name, path.stem
        if skills and skill not in skills:
            continue
        if only and cid not in only:
            continue
        meta, sections = load_base(data["base"])
        sections = apply_ops(sections, data.get("ops", []), f"{skill}/{cid}")
        cases.append({"skill": skill, "id": cid, "describe": data.get("describe", ""),
                      "date": meta["evaluation_date"], "sections": sections, "expect": data["expect"]})
    return cases


def validate(case):
    exp, skill, label = case["expect"], case["skill"], f"{case['skill']}/{case['id']}"
    if exp.get("verdict") not in ("accept", "reject"):
        raise CaseError(f"{label}: expect.verdict must be accept or reject")
    known = set(rubric_check_names(skill))
    for key in ("must_pass", "must_not_pass"):
        for name in exp.get(key, []):
            if name.lower() not in known:
                raise CaseError(f"{label}: {name!r} is not a check in skills/{skill}/rubric.md ({sorted(known)})")
    if exp["verdict"] == "reject" and not exp.get("must_not_pass"):
        raise CaseError(f"{label}: a reject case must name the check that should catch the flaw")
    if exp["verdict"] == "accept" and exp.get("must_not_pass"):
        raise CaseError(f"{label}: an accept case cannot list must_not_pass")


# ---------------------------------------------------------------- running

def build_prompt(case):
    skill_dir = ROOT / "skills" / case["skill"]
    parts = [f"=== Skill: {case['skill']} ==="]
    for rel in SKILL_FILES:
        p = skill_dir / rel
        if p.is_file():
            parts.append(f"----- {rel} -----\n{p.read_text().strip()}")
    parts.append("=== FROZEN INPUTS ===")
    for title, body in case["sections"]:
        parts.append(f"### INPUT: {title}\n{body}\n### END INPUT: {title}")
    parts.append(PREAMBLE.format(date=case["date"]))
    return "\n\n".join(parts)


def last_json_block(text):
    blocks = re.findall(r"```(?:json)?\s*\n(.*?)```", text, flags=re.DOTALL)
    if not blocks:
        raise ValueError("no fenced JSON block in the output")
    data = json.loads(blocks[-1])
    if isinstance(data, list):
        data = data[0]
    if not isinstance(data, dict) or "verdict" not in data:
        raise ValueError("the JSON block has no verdict")
    return data


def call_model(prompt, timeout):
    # cwd is an empty temp folder so no repo CLAUDE.md or settings are loaded.
    with tempfile.TemporaryDirectory() as cwd:
        proc = subprocess.run(["claude", "-p", "--model", MODEL, "--disallowedTools", NO_TOOLS,
                               "--setting-sources", "project"],
                              input=prompt, capture_output=True, text=True, timeout=timeout, cwd=cwd)
    if proc.returncode != 0:
        raise RuntimeError(f"claude exited {proc.returncode}: {(proc.stderr or proc.stdout)[-300:]}")
    return proc.stdout


def judge(data, expect):
    """Return a list of reasons the result is wrong (empty means it passed)."""
    why = []
    verdict = str(data.get("verdict", "")).lower()
    if verdict != expect["verdict"]:
        why.append(f"verdict was {verdict!r}, expected {expect['verdict']!r}")
    grades = {str(c.get("name", "")).lower(): str(c.get("grade", "")).lower() for c in data.get("checks", []) if isinstance(c, dict)}
    for name in expect.get("must_not_pass", []):
        if grades.get(name.lower()) == "pass":
            why.append(f"check {name!r} passed, but the flaw should have failed it")
        elif name.lower() not in grades:
            why.append(f"check {name!r} was not graded")
    for name in expect.get("must_pass", []):
        if grades.get(name.lower()) != "pass":
            why.append(f"check {name!r} was {grades.get(name.lower(), 'not graded')}, expected pass")
    return why


def run_case(case, retries, timeout):
    prompt = build_prompt(case)
    attempts = []
    for attempt in range(retries + 1):
        try:
            data = last_json_block(call_model(prompt, timeout))
            why = judge(data, case["expect"])
            grades = {c.get("name"): c.get("grade") for c in data.get("checks", []) if isinstance(c, dict)}
            attempts.append({"verdict": data.get("verdict"), "grades": grades, "why": why})
        except (RuntimeError, ValueError, subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            why = [f"run failed: {e}"]
            attempts.append({"verdict": None, "grades": {}, "why": why})
        if not why:
            break
    passed = not attempts[-1]["why"]
    return {"skill": case["skill"], "id": case["id"], "describe": case["describe"],
            "expected": case["expect"], "passed": passed, "flaky": passed and len(attempts) > 1,
            "attempts": attempts}


# ---------------------------------------------------------------- report

def summary_markdown(results, bar, rate):
    lines = ["## Skill evaluation", "",
             f"**{sum(r['passed'] for r in results)} of {len(results)} cases passed** ({rate:.0%}; bar {bar:.0%}).", "",
             "| Skill | Case | Expected | Got | Result |", "|---|---|---|---|---|"]
    for r in results:
        got = r["attempts"][-1]["verdict"] or "error"
        mark = "flaky (passed on retry)" if r["flaky"] else ("pass" if r["passed"] else "FAIL")
        lines.append(f"| {r['skill']} | {r['id']} | {r['expected']['verdict']} | {got} | {mark} |")
    failed = [r for r in results if not r["passed"]]
    if failed:
        lines += ["", "### Failures", ""]
        for r in failed:
            lines.append(f"- **{r['skill']}/{r['id']}**: " + "; ".join(r["attempts"][-1]["why"]))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Evaluate the skills against frozen cases.")
    ap.add_argument("--skill", help="comma-separated skills to run")
    ap.add_argument("--only", help="comma-separated case ids to run")
    ap.add_argument("--limit", type=int, default=0, help="run at most N cases")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--retries", type=int, default=1, help="re-runs of a failing case (default 1)")
    ap.add_argument("--bar", type=float, default=1.0, help="share of cases that must pass (default 1.0)")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--dry-run", action="store_true", help="build and validate only; no model calls")
    ap.add_argument("--list", action="store_true", help="list the cases")
    ap.add_argument("--root", help="repo folder whose skills/ and evals/ data to evaluate (default: this repo). "
                                   "CI runs trusted harness code against a pull request's data this way.")
    ap.add_argument("--out", help="write full results as JSON")
    ap.add_argument("--summary", help="write a markdown summary (for $GITHUB_STEP_SUMMARY)")
    args = ap.parse_args()
    global ROOT, EVALS
    if args.root:
        ROOT = Path(args.root).resolve()
        EVALS = ROOT / "evals"

    try:
        cases = load_cases(args.skill.split(",") if args.skill else None, set(args.only.split(",")) if args.only else None)
        for c in cases:
            validate(c)
    except CaseError as e:
        print(f"evals: invalid case: {e}", file=sys.stderr)
        return 2
    if args.limit:
        cases = cases[:args.limit]
    if not cases:
        print("evals: no cases selected", file=sys.stderr)
        return 2
    if args.list or args.dry_run:
        for c in cases:
            print(f"{c['skill']:<13} {c['id']:<22} expect {c['expect']['verdict']:<7} prompt {len(build_prompt(c)):>6} chars  {c['describe']}")
        print(f"evals: {len(cases)} case(s) valid" + ("" if args.list else " (dry run, no model calls)"))
        return 0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_case, c, args.retries, args.timeout) for c in cases]
        results = []
        for f in futures:
            r = f.result()
            results.append(r)
            tag = "ok  " if r["passed"] else "FAIL"
            print(f"{tag} {r['skill']}/{r['id']}" + ("  (flaky: passed on retry)" if r["flaky"] else ""), flush=True)
            if not r["passed"]:
                for w in r["attempts"][-1]["why"]:
                    print(f"       - {w}")
    rate = sum(r["passed"] for r in results) / len(results)
    md = summary_markdown(results, args.bar, rate)
    print("\n" + md)
    if args.out:
        Path(args.out).write_text(json.dumps(results, indent=2))
    if args.summary:
        Path(args.summary).write_text(md)
    return 0 if rate >= args.bar else 1


if __name__ == "__main__":
    sys.exit(main())
