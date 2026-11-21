# Governance

better-oss is a single-maintainer project. This file says how decisions are
made so contributors know what to expect.

## Roles

- **Maintainer:** [@mobeloper](https://github.com/mobeloper). Owns the
  direction, reviews and merges pull requests, cuts releases, and enforces the
  [Code of Conduct](CODE_OF_CONDUCT.md).
- **Contributors:** anyone who opens an issue, a pull request, or helps someone
  else in a discussion.

## How decisions are made

- Small changes (bug fixes, docs, examples) are decided in the pull request.
- Changes to **rubrics**, the **hooks**, or the **pipeline** (adding or removing
  a skill) are discussed in an issue first, because they change what the tools
  decide for everyone who installs them. Evidence beats opinion: a rubric
  change is judged on the before/after cases in the pull request
  (see [CONTRIBUTING.md](CONTRIBUTING.md)).
- When contributors disagree, the maintainer decides and says why in the thread.
- The pins that protect users (the model pin, the monitor's read-only
  allowlist, hooks that fail closed, live-mode only) change only with an issue
  that makes the case.

## Becoming a maintainer

There is one maintainer today and that is a risk for the project. If you have
sent several good pull requests, reviewed others' work well, and want to help
carry the project, say so in an issue or a discussion. Maintainers are added by
the current maintainer, and access is granted for the part of the project the
person has shown they understand.

## Changing this document

By pull request, like anything else.
