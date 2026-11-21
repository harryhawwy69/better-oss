<!--
EXAMPLE: this is the shipped example fit profile. Copy it to
~/.claude/better-oss/fit-profile.md (`npx better-oss init` does this) and
rewrite it for yourself: your languages, the kinds of repos you like,
what to avoid, how much time you have, and your platform. issue-scout
and issue-select read it to rank issues the rubric already accepts; it
never changes a verdict. Delete this comment when you are done.
-->

# Fit profile

I write python, javascript, typescript, css, scss, html, java, react, and dockerfile languages. Avoid other languages (go, c++, rust). Avoid any issue that needs special hardware (GPU, TPU, accelerators, special devices). I like working with repos about reputable agentic AI tools and libraries, and with large established open-source orgs: pytorch, open-telemetry, apache, opensearch-project, backstage, kubernetes, openedx, and hackforla. I look for issues labelled good first issue, help wanted, bug, or easy. Both frontend and backend issues are interesting to me. I want small bug fixes that I can finish in two weeks or less with easy difficulty, not a new feature. I want an active repo project where people answer questions. I develop on a MacBook Pro (macOS), so avoid any issue that is Windows-only or tied to another OS or platform (Linux-only, Android, iOS, WSL); an issue that also reproduces on macOS is fine. Many repos on my list do not maintain a good first issue label, or have heavy PR competition, so the cleanest path to a merge is an isolated fix: a self-contained bug fix, a schema or input validation tweak, or a test gap, touching one module and needing no design discussion. A docs gap counts only when the ticket also needs a test or code change; documentation-only tickets (docs, docstring, README or typo-only) are excluded.