## Summary

What changed and why, in two or three sentences.

Closes #

## Changes

- `path/to/file`: what changed

## Testing

Paste the commands you ran and their output (not "tested locally"):

```text

```

## Rubric change evidence (only if you changed a `rubric.md`, `procedure.md` or evidence guide)

- **The case:**
- **Before** (verdict and check grade, from a real run):
- **After** (same case, with this change):
- **A case that already graded correctly, unchanged:**

## Notes for reviewers

- Anything that differs from what the linked issue asked for, and why.
- **AI use:** how AI was used on this change, in your own words (or "none").

## Checklist

- [ ] `ruff check core` passes
- [ ] `cd cli && npm test` passes
- [ ] `claude plugin validate .` and `claude plugin validate skills` pass
- [ ] No symlinks, local paths, emails or tokens in committed files
- [ ] `defaults/` files still carry their `EXAMPLE:` banner
- [ ] Hooks I touched still fail closed (a crash stops the command)
