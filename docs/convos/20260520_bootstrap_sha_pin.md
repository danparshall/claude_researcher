# 20260520 — Bootstrap SHA-pin (stale `web_fetch` serving the thin slice)

**Date:** 2026-05-20
**Branch:** pin-bootstrap-fetch-shas
**Surface:** Claude Code (CLI)

## Summary

Dan reported that a test bootstrap run "was still using the thin check" and asked
to make the kit usable for collaborators. Session opened ambiguously — the CLI
checkout was on `tighten-section-0`, and the report could have been about a
different repo (a claude-exit session-start hook was also active). After
confirming the report was about `claude_researcher`, the investigation traced a
real bug: a fresh claude.ai chat following the README quick-start prompt received
the **55-line thin-slice smoke-test BOOTSTRAP** instead of the 579-line production
bootstrap.

The repo itself was not at fault. `git` on every branch, a live `curl` of the raw
CDN (`x-cache: MISS`, fresh), and a Claude Code `WebFetch` all returned the
production file. A user-supplied screenshot was decisive: the claude.ai agent
literally announced *"This is a thin-slice test"* and paraphrased commit
`6511a52`'s content. Root cause: **claude.ai's `web_fetch` tool served an
~11-day-stale cached snapshot** of `…/main/template/BOOTSTRAP.md` — the thin slice
occupied that path for a few hours on 2026-05-09 (`6511a52` → superseded same day
by `7e13380`), and `web_fetch`'s retrieval layer cached that window and never
refreshed. This is the stale-fetch issue the 2026-05-11 dogfooding session logged
as a Known Issue, except landing on the entry-point file and ~11 days stale.

Fix shipped: SHA-pin the four agent-fetched `/main/` raw URLs so an immutable
commit-SHA URL is served correct content even from a stale cache. The README's
own delivery was never the problem — a human reads it in a browser, not via
`web_fetch`; only the URL it hands the agent needed pinning.

## Topics Explored

- Multi-terminal disambiguation — confirmed (via `AskUserQuestion`) the report was
  about `claude_researcher`, not claude-exit or another tab
- Grep for "thin" across the repo; `git log --all` for the probe/check commits
- Verified the runtime-detection probe (`0802ec8`, `1edbbc1`) is already current on
  `origin/main` — ruled out as the "thin check"
- Confirmed `template/BOOTSTRAP.md` is 579 lines (production) on `main`,
  `origin/main`, `tighten-section-0`, `aitaxbid-skills-audit`, and the working tree
- Live `curl` of the raw CDN URL: HTTP 200, 579 lines, fresh cache headers
- Live Claude Code `WebFetch` of the same URL: full production (Steps 0–10)
- `git show 6511a52:template/BOOTSTRAP.md` — the 55-line thin slice, header
  "# claude_researcher Bootstrap — Thin Slice Test", matches the screenshot's
  agent output almost verbatim
- `gh pr list` — no open PRs; Dan's "PR waiting for merge?" hypothesis ruled out
- Grepped `BOOTSTRAP.md` for in-flow `/main/` raw URLs — found three template
  fetches (lines 378, 382, 499) plus a `RESEARCHER.md` fallback (line 552)

## Provisional Findings

- The bug is in **claude.ai's `web_fetch` cache**, a layer not visible from CLI.
  The raw CDN (Fastly) and GitHub `main` are both current; only `web_fetch`'s
  snapshot is stale. A SHA-pinned URL is a cache key `web_fetch` has never seen,
  forcing a fresh fetch — and is correct even if later re-cached, because the
  commit is immutable.
- "The version on GitHub" ≠ "the version `web_fetch` hands the agent." The repo
  was always fine; the delivery layer was broken. Earlier in the session the agent
  over-claimed that collaborators were "already unblocked" — corrected once the
  screenshot showed the agent genuinely received thin-slice content.
- The three in-flow template fetches (`personal_info.md.template`,
  `domain_allowlist.txt`, `_PROJECT_INSTRUCTIONS.md.template`) are the same buggy
  path — agent `web_fetch` calls — at lower severity (stale templates seed
  out-of-date starter files rather than blocking onboarding).

## Decisions Made

- **SHA-pin four agent-fetched URLs** to remove `web_fetch`-cache exposure:
  - `README.md` → `BOOTSTRAP.md` entry URL — pinned to `ea2918a`
  - `BOOTSTRAP.md` → 3 template URLs (378, 382, 499) — pinned to `d137580`
- **Two commits, by necessity** — a commit cannot embed its own SHA, so the README
  must point at the commit that already contains the finalized BOOTSTRAP.md:
  - [`ea2918a`](https://github.com/danparshall/claude_researcher/commit/ea2918a) —
    BOOTSTRAP.md template URLs pinned to `d137580`
  - [`a5b4793`](https://github.com/danparshall/claude_researcher/commit/a5b4793) —
    README entry URL pinned to `ea2918a`
- **Merge strategy must be a merge commit, not squash/rebase.** The README pins
  `ea2918a` by SHA; that commit must stay permanently reachable from `main`'s
  history or the raw URL eventually 404s after garbage collection. A real merge
  commit keeps `ea2918a` as a parent. Squash/rebase would orphan it onto the
  feature branch only.
- **Line 552 (`RESEARCHER.md` fallback) deliberately left on `/main/`** — it is a
  fallback whose primary path (clone-first) is already fresh; pinning a fallback
  freezes it. Flagged as a separate decision, not an oversight.
- **No inline maintenance comments** in BOOTSTRAP.md — it is agent-facing
  instructions; maintainer notes would pollute it. The SHA-bump obligation is
  recorded in commit messages, this convo, and STATUS.md instead.

## Results

No analysis artifacts. The result is the two-commit fix on `pin-bootstrap-fetch-shas`,
verified: the pinned entry URL serves the 579-line production bootstrap (zero
"Thin Slice" occurrences) with all three internal template URLs pinned; all four
SHA-pinned URLs return HTTP 200.

## Open Questions

- **SHA-bump maintenance has no enforcement.** Whenever `BOOTSTRAP.md` changes the
  README SHA must be bumped; whenever a template changes its SHA must be bumped. A
  maintainer who forgets silently reintroduces the same bug. Wants a release
  checklist or a "rewrite all pinned SHAs to HEAD" script — not yet captured as a
  task/issue.
- **Line 552 fallback** — left floating; revisit if the clone-first primary path
  ever proves unreliable.
- The deeper question — whether the kit should rely on `web_fetch` at all for
  upstream content, vs. always cloning — is unresolved. Clone-first cannot help
  the pre-egress entry fetch, so SHA-pinning is the right fix there regardless.
