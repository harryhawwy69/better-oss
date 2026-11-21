<!--
EXAMPLE: the shipped example playbook. Copy it to
~/.claude/better-oss/playbook.md (`/better-oss:init` does this) and
rewrite every rule so it is yours. The PR monitor drafts your next move from
this file, so until you edit it the monitor follows the rules below, not
yours. It will not draft while any of the four sections is empty, because a
nudge with no threshold behind it would be the monitor's call, not yours.

Keep the four section headings exactly as they are: the monitor finds them by
name. Keep the file under a page: a few rules you mean, each concrete enough to
decide a real case. Delete this comment when you are done.

Tuning the staleness numbers for a repo: check CONTRIBUTING.md for a stated
wait, then look at five recent merged PRs from outside contributors (skip ones
a maintainer or bot opened, since those merge fast) and how many days each
waited for a first comment, review, or merge. Pick a number a few days past the
usual wait. The monitor counts quiet days as days since anyone but you
commented.
-->

# Playbook: example contributor

## Response rules

- Open with the answer to the reviewer's point (done, not doing it and why, or one clarifying question), never with thanks or an apology.
- Cite the commit or line that changed, e.g. "Fixed in `abc1234`: the fixture now ...". Never argue, never say "as I said", never promise a later change without saying when.
- Follow the repo's AI policy in replies and PR text: disclose when it asks, and add no tool names or co-author trailers when it forbids them.

## Staleness thresholds

- First review: nudge after 4 quiet days. Stalled review (I pushed changes or answered and heard nothing): nudge after 4 quiet days from my last reply. Quiet days means days since anyone but me commented. (Tuned to a repo where maintainers usually answer within a few days; check the repo's own rhythm before keeping these numbers.)

## Nudge etiquette

- One nudge, as a comment on the PR. It says in a sentence what the PR does, what changed since the last activity, and asks one thing, e.g. "Is this still wanted, or should I change anything?"
- Tag only the reviewer who last engaged, or the maintainer who offered the issue. Never tag a group handle or a bot, and never write "bump", "ping" or "any update?".
- No second nudge. After a nudge, wait 7 more quiet days, then use the walk-away rules.

## Walk-away criteria

- Close my own PR if a maintainer says no, if another PR or commit fixes the issue, or if 11 quiet days pass with one nudge sent.
- Close note, short and with no blame: "Closing this since <reason>. Happy to reopen or rebase if it's still wanted. Thanks for the look." Then leave the issue comment so someone else can claim it.
