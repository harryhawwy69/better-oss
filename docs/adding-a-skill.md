# Adding a skill

A skill here is a small, readable judgment: a rubric a model executes and a
frame that says what to read and what to output. Before you build one, open an
issue so we can agree it belongs in the pipeline
(`issue-scout` -> `issue-select` -> `repro-check` -> `plan-check` ->
`pr-precheck`). [`skills/issue-select/`](../skills/issue-select/) is the
smallest complete example; read it first.

## 1. The folder

```text
skills/<name>/
  SKILL.md                       required: frontmatter + the frame
  rubric.md                      required: the checks and the verdict rule
  scope.md                       required: where it may work, and the rules there
  references/evidence-guide.md   required: where each proof lives
  procedure.md                   optional: step-by-step operating procedure
```

Plugin skills are discovered from `skills/<name>/SKILL.md` and run as
`/better-oss:<name>`. Nothing else needs registering.

`SKILL.md` starts with frontmatter that Claude uses to decide when the skill
applies, so write the description as "what it does, and when to use it":

```markdown
---
name: <name>
description: Grade <the thing> against a written rubric and decide whether <the decision>. Use when <the moment>.
---
```

## 2. The rubric

`rubric.md` is the part that carries the judgment. It has a table and a verdict
rule:

```markdown
## Checks

| Check | Evidence | Pass condition | Weight |
|---|---|---|---|
| names-the-issue | the claim draft and the issue body | restates the symptom in its own words or quotes the error | required |

## Verdict rule

Accept if every required check passes; preferred checks never change the
verdict; unclear counts as fail.
```

- **Check:** a short name. It is the key in the output JSON and other files
  refer to it, so renaming one later is a breaking change.
- **Evidence:** exactly what to look at and where ("the diff's changed files
  read against the plan's stated boundary", never "the PR").
- **Pass condition:** a rule about the *outcome* that someone else could apply
  and get your answer. Judge the thing itself, never its shape (how long, how
  many commits).
- **Weight:** `required` checks gate the verdict; `preferred` checks never
  change it and only rank what is accepted.
- The verdict is binary, `accept` or `reject`. State how `unclear` is treated.

Write a check for what actually gets bad work posted, not for what is easy to
measure.

## 3. The frame (`SKILL.md`)

Follow the shape of the existing skills. In the imperative, tell the model what
to read first (`scope.md`, then `rubric.md`), how to gather evidence (from the
places the evidence guide names), how to grade (`pass`, `fail` or `unclear`,
each with a one-line quote or fact), and how to assemble the verdict. Keep these
rules:

- **Evidence first.** No grade without the fact that decided it.
- **The rubric decides, not the run.** If a check passes by its stated
  condition but feels wrong, it passes, and the fix belongs in the rubric.
- **Refuse rather than invent.** If `rubric.md` has no checks, stop and say so.
- **Grade, never act.** A skill reads and reports. It does not post, claim,
  push, or open anything.
- **End with the JSON block, last, and nothing after it:**

  ```json
  {
    "item": "<issue or PR URL>",
    "checks": [
      {"name": "<check name>", "grade": "pass|fail|unclear",
       "evidence": "<one line: the fact or quote that decided it>"}
    ],
    "verdict": "accept|reject"
  }
  ```

## 4. Scope and evidence guide

`scope.md` names where the skill may work (here, any public repository) and the
rules for working in other people's repos (a stranger's claim blocks you; the
repo's own contributing docs outrank yours). `references/evidence-guide.md`
maps each rubric check to the places its proof lives, with a "good looks like"
line, so a check no one else could execute never ships.

## 5. Personal files

If your skill reads something the user should make their own (a profile, a
guide, a list), do not put it in the skill folder. A plugin update would
overwrite it. Instead:

1. Add a prefilled example to `defaults/`, opening with an `EXAMPLE:` comment
   that says how to use and edit it.
2. Tell the skill to read it from `~/.claude/better-oss/` first and fall back to
   the plugin's `defaults/` folder (copy the sentence from `issue-select`).
3. Add the filename to the list in `core/init.py` **and** `cli/bin/better-oss.js`.
   A test fails if the two lists disagree.

## 6. Test it for real

```text
claude plugin validate skills
claude --plugin-dir .          # then, after each edit:  /reload-plugins
```

Run the skill on at least one real input per verdict: something it should
accept, and something it should reject. Check that every grade quotes a real
fact, that the JSON block is last and valid, and that the skill never asks to
run anything that posts. The rubrics have no automated evaluation suite yet, so
paste those runs in your pull request.

## 7. Finish

- Add the skill to the table in the [README](../README.md) and the layout in
  [AGENTS.md](../AGENTS.md).
- Keep wording generic: no personal paths, names or emails, and no mention of
  where the rubric came from.
- Add a line under `Unreleased` in the [CHANGELOG](../CHANGELOG.md).
- Open the pull request using the template; it asks for the same evidence.
