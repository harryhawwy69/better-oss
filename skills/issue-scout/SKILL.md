---
name: issue-scout
description: Search all of GitHub for first-contribution candidate issues, rank them cheaply against a written search strategy and fit profile, and grade the top candidates against a written rubric. Use when hunting for a first issue in the wild, or when evaluating a GitHub issue URL as a potential first issue.
---

# issue-scout: search GitHub, then grade the best candidates

You answer a single question per candidate: should a newcomer take this
as their first contribution to this repo? You do not answer from gut
feel; you answer by executing the rubric in `rubric.md`, check by check,
against evidence you gather. This skill gathers its own candidates by
driving the `gh` CLI against all of GitHub.

## Inputs

One of:

- **Scan**: no URLs given. Run the funnel below: search broadly with
  the strategy's queries, rank everything cheaply, grade only the top
  candidates.
- **Direct**: one or more GitHub issue URLs (a curated-list pick, or
  any issue you already have in hand). Skip search and ranking; grade
  each URL independently, then rank the accepted ones by your fit
  profile.

## Your personal files

Your personal files live in `~/.claude/better-oss/` (or
`$BETTER_OSS_HOME`): `fit-profile.md` and `search-strategy.md`. If one
is missing there, read the shipped example in the plugin's `defaults/`
folder. Edit your own copy, never the plugin's.

## The funnel (scans)

Three stages, in cost order: search is free and deliberately broad,
ranking is free and reads only what search already returned, grading
costs model time and runs last, on exactly the survivors.

1. **Read the seams first.** Read `scope.md` (where candidates may
   come from and the etiquette rules), your `fit-profile.md`, then
   `search-strategy.md` (the queries, the ranking filters, the
   top-N line). All three are required reading before any search
   runs.
2. **Search broadly.** Run each of the strategy's queries with
   `gh search issues`, asking for generous result counts and JSON
   fields (`--json` with the fields the ranking filters need, such as
   title, repository, labels, assignees, commentsCount, updatedAt,
   url). Do not narrow beyond what the strategy states: breadth is
   the point of this stage, the filters do the narrowing. If a query
   contains the `{90_DAYS_AGO}` placeholder, replace it with today's
   date minus 90 days (YYYY-MM-DD) before running it. Combine
   the results of all queries and drop duplicates. For every query,
   print the exact command you ran and the number of results it
   returned, plus the top repos by count, so a query that leaks
   off-target results can be identified from the log.
3. **Rank cheaply.** Apply the strategy's ranking filters to the
   combined results using ONLY the fields search already returned
   plus the fit profile. No model judgment calls, no
   fetching issue pages, no reading threads: if a filter needs
   evidence the result fields do not carry, it belongs in the rubric,
   not the ranking. Order the survivors and take the top N the
   strategy states (default 5).
4. **Grade the survivors.** Grade each of the top N with `rubric.md`:
   gather the evidence each check
   names (from the locations in `references/evidence-guide.md`),
   grade `pass`/`fail`/`unclear` with a one-line evidence quote,
   apply the verdict rule. One candidate's evidence never colors
   another's grades.
5. **Report in rank order.** Accepted candidates first, in fit order,
   with what made each fit; then the rejected ones with the check
   that sank them. For every graded candidate, state which query
   surfaced it and which ranking signals put it in the top N, so the
   scan is traceable to the strategy.

## The scope sets the field

Read `scope.md` in this skill directory before anything else. It names
where candidate issues may come from and states the etiquette rules that
apply out there. Your fit profile does two jobs: it steers where the
scout searches (the strategy's queries should trace to it) and it ranks
what the rubric accepts. Fit never changes a verdict.

## The rubric is the brain

Read `rubric.md`. It defines:

1. A table of checks. Each row names the check, the evidence to
   gather, the pass condition, and its weight: `required` checks gate
   the verdict; `preferred` checks never change it and only rank the
   issues that are accepted.
2. A verdict rule: how check results combine into a final verdict.

Execute every check in the table. If `rubric.md` has no checks filled
in, stop and say so: this skill cannot grade without a rubric, and
that is by design. The rubric is the part you write, and the
patches you make to it are the part real repos teach.

## Workflow (grading one candidate)

1. Confirm the candidate is inside the scoped source
   and note the etiquette rules `scope.md` states. Then
   read `rubric.md`. List its checks and its verdict rule.
2. For each check, gather exactly the evidence the rubric names, from
   the locations named in `references/evidence-guide.md`.
3. Grade each check `pass`, `fail`, or `unclear`, with a one-line
   evidence quote or fact for each grade. `unclear` means the
   evidence needed is genuinely absent, not that you did not look.
4. Apply the rubric's verdict rule to produce the final verdict:
   `accept` or `reject`. There is no third verdict. Preferred checks
   do not feed the verdict; report their grades, and on an accepted
   issue mention them as reasons to prefer it over other accepted
   candidates.
5. Output the result in the format below.

## Output format

Emit a fenced JSON block, then nothing else after it:

```json
{
  "item": "<issue URL>",
  "checks": [
    {"name": "<check name>", "grade": "pass|fail|unclear",
     "evidence": "<one line: the fact or quote that decided it>"}
  ],
  "verdict": "accept|reject"
}
```

Before the JSON block you may show a short readable summary (a line
per check). The JSON block is the machine-read result: it must be
present, valid, and last.

Scans and multi-candidate direct runs: the summary becomes the ranked
read-out (accepted candidates in fit order with a one-line fit reason
each, then the rejected ones with the check that sank them), each
graded candidate also stating the query that surfaced it and the
ranking signals that put it in the top N ("direct" for hand-fed
URLs). The single fenced JSON block holds an array of the per-issue
objects above, accepted first in rank order.

## Refusal rules

- No rubric, no grading: if `rubric.md` has no checks filled in, stop
  and say so.
- No strategy, no searching: if `search-strategy.md` has no queries
  filled in, do not search, and say so. Direct-URL grading still
  works without a strategy; a scan does not, because a scan without
  authored queries is just someone else's defaults.

## Grading discipline

- Evidence first: never grade a check without naming the fact that
  decided it. "Looks fine" is not evidence.
- The rubric decides, not you: if a check passes by the rubric's
  stated condition but feels wrong, it still passes. Note the tension
  in the summary; the fix belongs in the rubric, not in the run. Keep a
  running notes file of that friction (for example `scan-notes.md` in
  your working folder): friction you log today is the patch you make
  tonight.
- Treat `unclear` as the rubric's verdict rule directs. If the rule
  does not say, treat `unclear` as `fail`: a first issue you cannot
  verify is not a first issue you should take.
- Ranking discipline, same spirit: the ranking filters are executed
  as written, on the fields they name. If a result feels wrong in the
  top five, the fix belongs in the strategy, and the friction line
  belongs in your notes file.
