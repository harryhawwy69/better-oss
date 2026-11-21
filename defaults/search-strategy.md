<!--
EXAMPLE: this is the shipped example search strategy. Copy it to
~/.claude/better-oss/search-strategy.md (`npx better-oss init` does this)
and rewrite the queries for yourself. issue-scout runs exactly the
queries and filters below, nothing else.

How to edit it:
1. Queries: each is a real `gh search issues` command. Trace each one to
   a sentence of your fit-profile.md; if you cannot say which sentence
   produced a query, it is probably not yours. Prefer generous --limit
   values and let the ranking filters do the narrowing.
2. Ranking filters: conditions and orderings over the fields the search
   already returned (labels, assignees, comment count, dates, repo). If
   a filter would need opening the issue page, it belongs in rubric.md.
   Keep at least one ordering or a tie-break, so the graded list is
   traceable to you.
3. Dates: write `{90_DAYS_AGO}` where a query needs a "recently updated"
   cutoff. The scout replaces it with today's date minus 90 days
   (YYYY-MM-DD) before running, so the strategy never goes stale.
-->

# Search strategy: where your scout looks, and why

## Queries

Every query asks for the same JSON fields (the ranking filters need them)
and ends with `-- -linked:pr` so issues that already have a linked pull
request are left out.

# Profile: "python" + "reputable agentic AI tools and libraries" + "small bug fixes" (large agentic AI orgs, python bugs)
gh search issues --owner langchain-ai,openai,modelcontextprotocol,crewAIInc,run-llama,BerriAI,letta-ai,langfuse --label bug --language python --state open --limit 500 --no-assignee --updated ">{90_DAYS_AGO}" --json title,repository,labels,assignees,commentsCount,createdAt,updatedAt,url -- -linked:pr

# Profile: "javascript, and typescript" + "reputable agentic AI tools and libraries" + "Both frontend and backend issues" + "small bug fixes" (same orgs, typescript bugs)
gh search issues --owner langchain-ai,openai,modelcontextprotocol,crewAIInc,run-llama,BerriAI,letta-ai,langfuse,mastra-ai --label bug --language typescript --state open --limit 500 --no-assignee --updated ">{90_DAYS_AGO}" --json title,repository,labels,assignees,commentsCount,createdAt,updatedAt,url -- -linked:pr

# Profile: "python" + "easy difficulty" (good-first-issue labelled issues in the same orgs; rare but the best signal)
gh search issues --owner langchain-ai,openai,modelcontextprotocol,crewAIInc,run-llama,BerriAI,letta-ai,langfuse --label "good first issue" --language python --state open --limit 500 --no-assignee --updated ">{90_DAYS_AGO}" --json title,repository,labels,assignees,commentsCount,createdAt,updatedAt,url -- -linked:pr

# Profile: "python" + "reputable agentic AI tools and libraries" + "small bug fixes" (named repos from orgs too broad to scope by owner; anthropics is listed by SDK repo because anthropics/claude-code is an issue tracker with no source to fix and would fill the result cap)
gh search issues --repo anthropics/anthropic-sdk-python,anthropics/anthropic-sdk-typescript,pydantic/pydantic-ai,huggingface/smolagents,microsoft/autogen,google/adk-python,microsoft/agent-framework --label bug --language python --state open --limit 500 --no-assignee --updated ">{90_DAYS_AGO}" --json title,repository,labels,assignees,commentsCount,createdAt,updatedAt,url -- -linked:pr

# Profile: "large established open-source orgs: pytorch, open-telemetry, apache" + "good first issue" label + listed languages
gh search issues --owner pytorch,open-telemetry,apache --label "good first issue" --language python --state open --limit 500 --no-assignee --updated ">{90_DAYS_AGO}" --json title,repository,labels,assignees,commentsCount,createdAt,updatedAt,url -- -linked:pr

# Profile: "large established open-source orgs: pytorch, open-telemetry, apache" + "help wanted" label (unclaimed work; gh ANDs repeated labels, so each label needs its own query)
gh search issues --owner pytorch,open-telemetry,apache --label "help wanted" --language python --state open --limit 500 --no-assignee --updated ">{90_DAYS_AGO}" --json title,repository,labels,assignees,commentsCount,createdAt,updatedAt,url -- -linked:pr

## Ranking filters

Applied in the order written, using only the fields the searches returned.

- drop any result with an assignee (the queries already pass `--no-assignee`; recheck the field)
- drop any result not updated in the last 90 days (supports "an active repo project")
- drop any result with more than 15 comments (long threads are rarely "small" or "easy")
- drop any result whose title starts with `Feature` or `[Feature`, or case-insensitively with `feat(`, `feat:`, `[feat`, `enhancement` or `[enhancement` (profile: "not a new feature")
- drop any result whose labels include `question`, `feature`, `feature request` or `discussion`
- drop any result whose labels include `documentation`, `docs` or any label containing `doc`, unless its title also contains a code or test word (`test`, `bug`, `fix`, `error`, `crash`, `fails`)
- drop any result whose title or labels name a non-macOS platform without also naming macOS (`windows`, `win32`, `wsl`, `powershell`, `linux`, `ubuntu`, `android`, `ios`; profile: "avoid any issue that is Windows-only or tied to another OS")
- order what remains, in this priority: (1) a bug label together with a beginner label (`good first issue`, `help wanted`, `easy`); (2) a bug label alone; (3) a beginner label without a bug label; (4) a help label alone; within the same tier, fewest comments first, then most recently updated
- tie-break: if still tied, prefer the repo with the most total results across all queries (a busy repo is more likely to answer questions)
- spread the top of the list across repos: take each repo's best-ranked issue first, then its second, and so on (round-robin), so one busy repo cannot fill every graded slot

## How many to grade

Grade the top **5** ranked results per scan. Grading costs model time
(roughly $0.20 per candidate), so a scan of five is about $1 and you can
iterate the strategy several times cheaply. You need one good issue, not
ten. If you raise this number, say why in a sentence and name the cost
you are accepting.
