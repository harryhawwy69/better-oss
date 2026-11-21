# Scope: where to look, and who is looking

Like every scope file, this one is the skill's field of view: the rubric
(`rubric.md`) decides whether an issue is GOOD; the scope decides which
issues are candidates at all, and the strategy (`search-strategy.md`)
decides where the scout actually walks.

## Where candidates come from

Any public repository. The field is all of GitHub, and your fit profile
is what keeps that searchable. Read it from `fit-profile.md` in your
personal folder (`~/.claude/better-oss/`, or `$BETTER_OSS_HOME`); if it
is missing there, read the shipped example in the plugin's `defaults/`
folder. Start from repos in the languages and tools it names, and let
the profile steer where you search, not just how results are ranked.

**Claims count.** A claim comment or an assignee is a stranger who got
there first, and you have no channel to coordinate with them. Read claim
signals exactly as the rubric's checks state them; do not claim over
someone.

**Claim upstream the moment you commit.** The rule cuts both ways:
the instant you decide to take an issue, say so on the issue itself
(a short comment: what you plan to do and roughly when). You are now
the claim signal someone else's skill will read. Deciding privately
and claiming later is how two strangers do the same work twice.

## How the fit profile is used

Besides ranking the issues your rubric accepts, the fit profile steers
WHERE the scout searches: your `search-strategy.md` queries should each
trace to a sentence in it, so name the languages, tools, and project
areas you actually want to work in, and anything you want to avoid. It
still never changes a verdict: fit cannot rescue an issue your rubric
rejects, and cannot sink one it accepts.
