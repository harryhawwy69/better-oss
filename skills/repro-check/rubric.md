# Rubric: is this reproduction package ready to post?

<!-- Add a row for every proof family in references/evidence-guide.md. Each row needs a short check name (used in the output JSON), the evidence to gather, a pass condition someone else could apply, and a weight (`required` gates the verdict; `preferred` never changes it). -->

## Checks

| Check | Evidence | Pass condition | Weight |
|---|---|---|---|
|names-the-issue|quotes the error message from the issue body|describes the issue and behavior and work required| required|
|environment-detail |Candidate repro report repo version and OS| names the version and OS the repo's bug template asks for, and matches the issue's version or says why it doesn't| required |
|steps-rerunnable| Candidate repro report reproduction or preparation steps | describes what the person did to prepare with specific steps to reproduce or make it rerunnable | required |
|Analysis-claim  | Candidate repro report findings of analysis | Provides description of what the author found when reproducing the issue it might describe next steps | preferred |
|expected-behaviour| Candidate repro report expected outcome | mentions what is expected during reproduction | preferred |
|actual-behaviour| actual outcome | honestly tells what actually happen during reproduction | required |
|communication|issue comments|Communication respects repo, comments are issue-specific, honest about completed work, and follow applicable repo rules |preferred|

## Verdict rule

Accept if every required check passes; preferred checks never change the verdict, they rank accepted issues; unclear counts as fail.
