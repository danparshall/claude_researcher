# Convo slug HHMM leak fix + "Push early and often" rule + auto-push hook (PR #49)

**Date:** 2026-08-15
**Repo:** `claude_researcher` (meta dev repo, flat `docs/`)
**Surface:** claude-code (CLI, on Dans-MacBook-Air)
**Main:** advanced `468005a` → `d819fe4` (PR #49 merge)

## Summary

Three-commit RESEARCHER.md hygiene sweep, all landed on the `convo-slug-date-only` branch and merged as [PR #49](https://github.com/danparshall/claude_researcher/pull/49) (real merge commit `d819fe4`). Started as a one-line fix — Dan flagged that the recent `SESSION_TS=YYYYMMDDThhmm` change (intended for the git codename per §2.0b) had leaked into convo filenames via §2e, producing `20260810T1442_managed_retreat_planning.md` instead of the intended `YYYYMMDD_<slug>.md`. Scope grew mid-session in two steps: first Dan pushed back on a hallucinated rationale I'd propagated ("the branch already carries the date" — never a design decision, just an unexamined assertion in the pre-existing §2e text), which forced a real look at *why* the mode-distinction existed and confirmed it should be collapsed universally to date-first; then Dan asked for the "push early and often" discipline to be spec'd, which grew into a tracked post-commit hook that auto-installs in the web sandbox at §2.0b (rather than relying on agent memory of a procedural rule).

Secondary thread: Dan called out that I'd batched commits waiting for a "should I push?" round-trip after the first edit — exactly the anti-pattern the new §5 rule kills. That behavior was rooted in the local Bash tool's built-in "never commit without permission" description (not in Dan's dotfiles or Nori profile, which has "Push regularly" as a branch-hygiene rule). Nothing to change in the tool description (Anthropic-owned), but I should be leaning on Nori's "Push regularly" rule instead of the Bash-tool caveat when working in Dan's repos.

## Topics Explored

- **§2e convo-name handshake leak.** `SESSION_TS=$(date -u +%Y%m%dT%H%M)` was captured in §2.0b for the git codename (`Dan (web, canary-policy, 20260810T1442)`), and §2e reused the same variable in convo filenames (`${SESSION_TS}_<slug>.md` for `main_only`, `<slug>_${SESSION_TS}.md` for `branches`). Introduced `SESSION_DATE=$(date -u +%Y%m%d)` alongside `SESSION_TS`; convo filenames now use `SESSION_DATE`, codename still uses `SESSION_TS`.
- **Mode distinction collapse.** Prior `branches`-mode ordering was slug-first with the pre-existing rationale "the branch already carries the date, so the slug leads." Dan flagged that no such design decision was ever made — real branch names like `convo-slug-date-only` don't encode dates. Grep confirmed the claim only occurred in that one spot; my first edit had already scrubbed it via the mode collapse. Both modes now use `${SESSION_DATE}_<slug>.md`.
- **Cross-file lockstep.** `template/skills/update-docs/SKILL.md` step 1 description (format spec) and `template/skills/write-a-plan/SKILL.md` plan-header pointer both referenced `SESSION_TS`-in-filename for `git log` join. Updated: filename join is now by date + slug; git-log join happens via `git log --author="<codename>"` (the codename still carries HHMM). RESEARCH_LOG session header `## Session: YYYYMMDDTHHMM — [convo-name]` intentionally kept the full timestamp — it's inside a doc, and it's the remaining cross-reference to the codename's HHMM.
- **"Push early and often" as a §5 working convention.** Added as a fourth universal rule alongside "Don't infer — ask", "Show before committing", "Codify after the third repetition". Applies on any surface (web sandbox ephemerality; CLI worktree drift under concurrent agents). Explicitly notes that the confirmation gates below still apply to what a commit *contains* (deletions, archives, merges, force ops) — the push-after-commit round-trip is what's being killed, not the pre-commit narration.
- **Post-commit hook, tracked in the repo.** Ships `template/hooks/post-commit` (mode 100755) with full rationale comments. §2.0b copies it to `.git/hooks/post-commit` per session (sandbox-local — `.git/hooks/` isn't versioned). Fallback for the §2.0a WebFetch-degraded path: inline-writes the same two-line script (`git push -u origin HEAD 2>&1`). Failure model: loud stderr, no retry, no force — the commit is already local when the hook runs, so a failed push doesn't undo it; the agent must read commit output tails to catch failures. Called out in both §2.0b install text and the §5 rule.

## Provisional Findings

- **The mode distinction on convo filenames was justified by an unexamined assertion**, not a real design tradeoff. Collapsing to a single format (`${SESSION_DATE}_<slug>.md` for both modes) matches the format this very repo has been using in `docs/convos/` all along, which is corroborating evidence for "date-first is what the workflow actually wants."
- **The auto-push hook is durability insurance, not a permission to stop watching.** RESEARCHER.md text is explicit that agents must still read commit output tails — a silent "committed = safe" assumption is exactly the failure mode the loud-stderr design targets. Whether the hook actually fires on the web sandbox is unverified from this session (I have no way to spawn a real sandbox from CLI); first fresh web session will tell us definitively via `ls -la .git/hooks/post-commit` after §2.0b runs.
- **Agent-side compliance is the real gating factor for adoption.** Existing web sessions won't retrofit — they've already passed §2.0b. Only sessions starting after `d819fe4` will run the new install step. For the fleet-of-sessions case, we're a session-turnover away from full coverage.

## Decisions Made

- **Convo filenames** are `${SESSION_DATE}_<slug>.md` for both `main_only` and `branches` modes (universal, no mode distinction).
- **RESEARCH_LOG session header** keeps `## Session: YYYYMMDDTHHMM — [convo-name]` — the format-inside-a-doc remains the cross-reference to the codename's HHMM.
- **`## Session: YYYYMMDDTHHMM` vs filename**: filename is the join key across artifacts (STATUS → RESEARCH_LOG → convo → plan); codename+HHMM is the join key for `git log` disambiguation of concurrent sessions. Two separate keys, two separate purposes.
- **Post-commit hook lives in `template/hooks/post-commit`** (tracked, executable). Copy-with-inline-fallback install pattern in §2.0b. Not a symlink — simpler, well-understood, resilient to template-path changes.
- **PR #49 merged with a real merge commit** (`d819fe4`) preserving SHA-pin reachability of the three ship commits (`ec0b63b`, `e584c5e`, `b1eafb3`). Branch `convo-slug-date-only` deleted on origin and locally per §6 default.

## Results

Landed on `main`:
- `d819fe4` — Merge PR #49 (real merge commit).
- `ec0b63b` — SESSION_DATE introduced; convo filenames drop HHMM; mode distinction collapsed; update-docs + write-a-plan skills updated in lockstep.
- `e584c5e` — §5 gains "Push early and often" as fourth universal working convention.
- `b1eafb3` — `template/hooks/post-commit` tracked at mode 100755; §2.0b install block with WebFetch-fallback inline-write; §5 rule cross-references the hook.

Repo state at session close: zero open PRs; local `main` at `d819fe4` + this convo commit, in sync with origin.

## Open Questions

- **Hook actually fires on the web sandbox.** Standard git behavior, but I have no way to prove it without spawning a real claude.ai session. Next fresh web session should confirm via `ls -la .git/hooks/post-commit` (expect `-rwxr-xr-x`) and observing that the first commit auto-pushes.
- **Executable bit preservation across the template clone path.** `git clone` preserves mode 100755 (verified — the merge commit output showed `create mode 100755`). Defensive `chmod +x` after the `cp` covers any edge case where a fetch path strips it. WebFetch fallback writes the script inline and chmods, so that path is safe too. But no live test yet.
- **Retrofit for in-flight sessions.** Sessions that started before `d819fe4` have already passed §2.0b and won't install the hook. Could be surfaced as a manual-install snippet the user pastes mid-session if they notice a long-running session missing the hook. YAGNI unless it becomes a real friction point.
- **Whether "Push early and often" needs a companion codification in the Nori profile.** Dan's local Nori block already has "Push regularly" as branch hygiene; the new RESEARCHER.md rule is for web sessions specifically. If cross-surface consistency matters, the two rules could be phrased in lockstep.

## Process notes

- `gh pr create` with a heredoc body was hard-failed by the `block_newline_hash_in_quoted_arg` hook (markdown `## Summary` header inside quoted arg) — same as documented in the 2026-07-19 convo. Write-then-`--body-file` worked first try. Should probably promote this to a "known Bash gotcha" note somewhere durable (Nori block? RESEARCHER.md process-notes appendix?) — it's bitten at least twice now.
- Session opened as an IDE-open file notification on `template/RESEARCHER.md`. The Nori block's multi-terminal-safety rule flags these as "may not be relevant" — this one was, because Dan's opening message referenced the exact file. Worth noting: when the IDE-notification file and the user's message clearly match, ignore-by-default can be relaxed.
- Codified the "hallucinated rationale" self-critique inline rather than deferring — Dan's "this kind of hallucination is why I left Opus5" landed as feedback worth acting on same-turn, not filed away.
