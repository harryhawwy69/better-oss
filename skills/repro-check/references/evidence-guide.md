# Evidence guide: where proof lives in a reproduction package

This is the map `repro-check` uses. For every kind of proof a rubric
check names, it says where to find it (in your drafts and on GitHub) and
what good looks like. A rubric check whose evidence this guide cannot
locate is a check nobody else can execute; if you add a check, add its
map entry here.

A package is two drafts, a claim comment and a repro report, read
against the issue they belong to. Issue-side facts come from the issue
page and the repo; candidate-side facts come only from what the drafts
contain and quote.

## Family 1: Names the issue

Does the package show it understands the reported problem and the work
required?

| Signal | Where |
|---|---|
| What the issue reports | the issue title and body on the issue page; the error message or symptom quoted there |
| What the claim says it will do | the claim draft: the sentence naming the behavior and the planned change |
| Thread context | the issue's comments: maintainer replies, labels, linked PRs, anything that narrows the ask |

Good looks like: the claim restates the issue's symptom in its own words
or quotes the exact error, says what change it expects to make, and does
not contradict a maintainer's later comment in the thread.

## Family 2: Environment

| Signal | Where |
|---|---|
| Versions and OS the repo asks for | the repo's bug-report issue template (`.github/ISSUE_TEMPLATE/`) and `CONTRIBUTING.md` |
| Versions the issue targets | the issue body, its version field, or the release the reporter names |
| Versions the report used | the environment block in the repro draft |

Good looks like: the report names the product version (or commit), the
language runtime, and the OS the template asks for, and either matches
the version the issue targets or says plainly why it differs.

## Family 3: Steps

| Signal | Where |
|---|---|
| Preparation | the repro draft: clone or install commands, setup, fixtures, config |
| Trigger | the repro draft: the exact commands or code that cause the behavior |
| Starting state | the repro draft: branch, commit, or release the steps begin from |

Good looks like: a stranger can start from a clean checkout, run the
steps in order with no guessing, and reach the trigger. Commands are
copy-pasteable, and anything not obvious (a flag, a data file) is stated.

## Family 4: Behavior shown (expected and actual)

| Signal | Where |
|---|---|
| Expected behavior | the repro draft's expected-outcome line; the docs or issue text it is based on |
| Actual behavior | the repro draft's output excerpt, log, or screenshot description |
| Match to the issue | the issue body's described symptom, compared with the actual outcome |

Good looks like: the actual output is pasted or quoted, not summarized,
and it is the same behavior the issue describes, not an adjacent one.
An evidenced "cannot reproduce" (what was tried, on which version, with
what output) is a pass; a confident report of a different problem is not.

## Family 5: Honesty and analysis

| Signal | Where |
|---|---|
| What was actually done | the repro draft: steps and results, compared with the claims in the claim comment |
| Findings | the repro draft's analysis section, if present: suspected cause, narrowing steps, next steps |

Good looks like: every claim in the comments is backed by something in
the report. Analysis is labeled as a hypothesis unless it was verified,
and unfinished work is described as unfinished.

## Family 6: Comms

| Signal | Where |
|---|---|
| Repo conventions | `CONTRIBUTING.md`, issue and PR templates, and `CODE_OF_CONDUCT.md` |
| AI-use policy | `CONTRIBUTING.md`, an `AI_POLICY.md`-style file, or template checkboxes; an `AGENTS.md` file is instructions for agents, not a policy |
| Existing thread | the issue's comments: is a reproduction already posted, is the issue already claimed |

Good looks like: the comments are specific to this issue, follow the
templates and any disclosure the repo asks for, and add something new
instead of "same here". A claim states what you plan to do and roughly
when; it does not overpromise.
