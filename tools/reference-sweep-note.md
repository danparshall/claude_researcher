# Reference Sweep Note

When sweeping a term or rename across this repo (e.g. `CLAUDE.md` → `RESEARCHER.md`, "Custom Instructions" → "Project Instructions"), verify completeness with an exhaustive search before declaring done.

## Protocol

After applying the sweep:

```bash
# Case-insensitive, recursive
grep -ri "old-term" . --exclude-dir=.git --exclude-dir=node_modules
```

Expect zero hits except for intentional historical references — convo summaries describing what a past session did are the journal, not state, and those stay verbatim. Confirm each remaining hit is intentional before declaring done.

## Why this is here

Plan 04 Task 2 (2026-05-11) swept "Custom Instructions" → "Project Instructions" across 10 files / 31 occurrences but missed a lowercase variant in `ATTRIBUTION.md`. The miss surfaced during a separate audit a few commits later.

Plan 03's similar sweep (2026-05-11) declared completion of a `CLAUDE.md` → `RESEARCHER.md` rename, then over the next several commits three additional references showed up in `SKILL_INDEX.md`, `update-docs/SKILL.md`, and `ATTRIBUTION.md`.

Both misses had the same failure mode: find-and-replace by inspection rather than by exhaustive search.

## Scope

This is a repo-specific note. Actual research repos rarely have repo-wide renames; this dev repo has had several because the project is still finding its terminology. Expect this checklist to be used a few more times before terminology stabilizes, then largely ignored.
