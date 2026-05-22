# 20260521 — Re-pin tooling + the egress fix's stale entry pin

**Date:** 2026-05-21
**Branch:** repin-tooling
**Surface:** Claude Code (CLI)

## Summary

Right after PR #8 (the egress UI-agnostic doc rewrite) merged, a problem
surfaced: the fix was on `main` but **not reachable by collaborators**. The
README's bootstrap-entry URL was still SHA-pinned to `ea2918a` — the
*pre-egress-rewrite* commit — so a collaborator pasting the quick-start prompt
would `web_fetch` the old Step 1. Separately, the a2 commit had changed
`domain_allowlist.txt`, but `BOOTSTRAP.md`'s in-flow pin for that file still
pointed at `d137580` (pre-a2). The SHA-pin maintenance burden flagged in the
`20260520_bootstrap_sha_pin` convo had fired on the very first change after the
pins were introduced — and the egress PR shipped without the required bump.

Dan chose to fix the recurring problem, not just this instance: **write a
re-pin script, then use it.** `tools/repin.py` rewrites the pinned URLs to the
current HEAD and makes the two commits the self-reference requires. It was used
to re-pin both stale SHAs.

## Topics Explored

- Confirmed the staleness: README pinned `ea2918a` (pre-egress); `BOOTSTRAP.md`
  pinned `domain_allowlist.txt` at `d137580` (pre-a2-note)
- The two-commit constraint — a commit cannot embed its own SHA, so the README's
  `BOOTSTRAP.md` URL must point at the commit that already holds the finalized
  `BOOTSTRAP.md`
- Which URLs are managed (pinned) vs intentionally on `/main/` (the RESEARCHER.md
  clone-fallback URLs at BOOTSTRAP.md lines ~457/552 stay on `main`)

## Provisional Findings

- The SHA-pin design is sound for the stale-`web_fetch` bug, but its manual
  maintenance step is not realistically reliable — it was missed the first time
  it was needed, by the same agent that had documented the requirement. A script
  is the right mitigation.
- Re-pinning is safely automatable: the managed URLs are a known, closed set
  keyed by path suffix, so the rewrite can leave other-repo and `/main/` URLs
  untouched by construction.

## Decisions Made

- **`tools/repin.py`** — re-pins the managed URLs to current HEAD, two commits
  (BOOTSTRAP.md template URLs → pre-script HEAD; README entry URL → the
  BOOTSTRAP.md commit). Refuses to run on `main`. Does not push.
- **`tools/test_repin.py`** — covers the `repin_refs` rewrite logic: SHA refs and
  `main` refs rewritten, unmanaged paths and other-repo URLs left untouched,
  every occurrence replaced, idempotence. Runnable standalone or under pytest;
  stdlib-only (no venv/deps for a one-file maintainer tool in a docs repo).
- **TDD note (honest):** the implementation was written before the RED phase was
  run — a deviation from the TDD skill. Recovered by mutation testing: stubbing
  `repin_refs` to `return text, 0` made exactly the 3 rewrite tests fail with
  assertion errors (the 3 no-change tests still passed, correctly), confirming
  the tests bite real behavior and are not vacuous. Implementation then restored;
  6/6 green.
- **Ran `repin.py`:** README → `2dec9af`; `BOOTSTRAP.md` templates → `87f84ea`.
  Commits `2dec9af` (BOOTSTRAP repin) and `132d2cd` (README repin).
- **Merge constraint:** this branch must merge with a real merge commit, not
  squash/rebase — the README pins `2dec9af` by SHA, which must stay reachable
  from `main`.

## Results

No analysis artifacts. Result: `tools/repin.py` + tests, and the re-pin commits
on `repin-tooling`.

## Open Questions

- The re-pin step is now scripted but still **manual to invoke** — a maintainer
  must remember to run `repin.py` after a BOOTSTRAP/template change. A pre-merge
  hook or CI check that fails when the pins are stale would close the loop fully;
  not built. Lower urgency now that the bump is one command.
