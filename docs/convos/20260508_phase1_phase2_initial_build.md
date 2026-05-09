# claude_researcher — Phase 1 + Phase 2 Initial Build

**Date:** 2026-05-08
**Repo:** claude_researcher (this repo)
**Plan:** [`docs/plans/01_initial_build.md`](../plans/01_initial_build.md) — Phases 1 and 2

## Summary

First execution session against the implementation plan. Phase 1 (GitHub remote + push) and Phase 2 (`template/` skeleton) completed. Two design discoveries surfaced along the way: (a) the existing `_PROJECT_INSTRUCTIONS.md.template` had a latent URL bug — `repos/$REPO/...` was missing the owner prefix, so any user filling in `REPO="my-research"` would hit 404s; fixed during the rewrite; (b) Claude Code's "ask before committing" behavior comes from the Bash tool's description field, not from the system prompt or Dan's CLAUDE.md, which informed the upcoming Phase 4 commit-policy decision. One bug surfaced in passing: the Nori `commit-author.js` hook produces malformed commit messages on every commit.

## Work Done

- **Phase 1 (task 1).** Created `github.com/danparshall/claude_researcher` (private), pushed all four prior commits via `gh repo create ... --source=. --remote=origin --private --push`. Confirmed design convo and plan visible on github.com.
- **Phase 2 (tasks 2–8).**
  - `template/README.md` — short intro paragraph + copy-pasteable bootstrap-prompt code block + repo map + license pointer.
  - `template/LICENSE`, `template/LICENSE-ADDENDUM.txt` — verbatim copies of root files (`diff -q` confirmed identical).
  - `template/ATTRIBUTION.md` — Nori → Dan → collaborator chain with the exact copyright line specified in the plan.
  - `template/_PROJECT_INSTRUCTIONS.md.template` — rewrote: plain-language sandbox/allowlist explanation replacing egress-proxy jargon; placeholders normalized to `<TOKEN>` / `<USERNAME>` / `<REPO>` per the plan's literal spec; URL bug fixed (curl now uses `repos/$USERNAME/$REPO/...`); GitHub API headers added (`Accept: application/vnd.github+json`, `X-GitHub-Api-Version: 2022-11-28`) per plan's "Implementation Details" section.
  - `template/templates/domain_allowlist.txt` — 8-domain baseline, sorted, comment headers split workflow-required (4) from paper-source (4) domains.
  - `template/{skills,scripts,reference}/.gitkeep` — empty placeholder dirs.
  - Single commit `f8b8e1b` — pushed.

## Decisions Made

- **Phase 4 commit-policy will be `git_fluency`-tiered.** Most claude.ai users in the target audience are not git-savvy; the natural model is "the agent saves your work for you" rather than "the agent asks before saving." But experienced users would find that intrusive. The plan already captures `git_fluency` as a 3-tier interview field (novice / occasional / fluent) and CLAUDE.md task 24 already uses the same tier for terminology calibration. Extending the same tier to commit eagerness slots in cleanly:
  - **novice** — checkpoint often and under the hood. Brief narration ("saved.") rather than seeking permission. Frequent commits protect users from losing work.
  - **occasional** — commit at natural breakpoints; light narration; ask only before structurally large operations (e.g., `docs/active → docs/historical` archive moves, branch merges).
  - **fluent** — terse; ask only when truly destructive. Trust the user to drive.
  - Across all tiers, the Contents API model means each `write_*` is its own commit; this isn't optional. The tier governs how chatty the agent is about it, and which compound operations it batches vs. confirms.
- **Sysprompt-layer findings extracted to a standalone reference note** at [`docs/convos/20260508_sysprompt_layer_analysis.md`](20260508_sysprompt_layer_analysis.md) rather than buried in this convo. The findings are general (true regardless of this project) and worth being directly reachable.

## Bugs Surfaced

- **Nori `commit-author.js` hook produces malformed commit messages.** The `PreToolUse:Bash` hook at `/opt/homebrew/lib/node_modules/nori-skillsets/build/src/cli/features/claude-code/hooks/config/commit-author.js` rewrites Claude Code's default attribution footer into Nori's, but inserts literal `\n\n` escape sequences in the `-m` argument. Bash does not expand `\n` to newline inside double-quoted strings, so the commit message collapses into a single subject line with visible backslash-n characters. This has been mangling commits across multiple of Dan's repos for at least a week (`lobby_analysis`, `econ-impact`, `websites/danparshall`, now `claude_researcher`). Fix would be multiple `-m` flags or a heredoc instead of escape sequences. Worth filing upstream against `tilework-tech/nori-skillsets`. **Decision:** leave the existing `f8b8e1b` commit as-is (cosmetic only; private repo; no PR risk).

## Open Questions (carry-forward)

- claude.ai custom-instructions length limit — must verify before Phase 4 (affects whether `template/CLAUDE.md` is uploaded as Project text or fetched at runtime).
- pypdf availability in claude.ai's sandbox — must verify before Phase 5 task 31.
- Fine-grained PAT cross-org write capability — relevant for v2 issue auto-file.

## Next

Phase 3 — write `BOOTSTRAP.md`. Plan tasks 9–18.
