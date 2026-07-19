# F5.e wiring (PR #41) + Nori-block disappearance forensics

**Date:** 2026-07-17 → 2026-07-19 (wiring landed 07-17; Nori investigation 07-19)
**Repo:** `claude_researcher` (meta dev repo, flat `docs/`)
**Main:** advanced `3b8ae17` → `0098856` (PR #41 merge)

## Summary

Picked up the F5.e handoff from the 07-17 reconciliation convo: read the freshly-merged lifecycle-only §6 to locate the real append-on-top conflict surfaces, then wired `resolve_append_conflict.py` into them. Key correction to the handoff's framing: in the template there is no merge-ceremony *skill* to wire into — §6's PR-and-merge flow is inline in RESEARCHER.md (`finishing-a-research-branch` is Dan's personal `~/.claude/skills/` skill, not a template artifact). The load-bearing wiring point turned out to be the Appendix's "`git push` rejected (non-fast-forward)" entry — the single choke point all STATUS push races funnel through — which until now said "surface to the user; don't auto-resolve" with no carve-out, directly blocking the script's documented intended use. Full wiring landed as PR #41, merged with a real merge commit (`0098856`). **F5 is now 5/5 closed.**

Second arc, triggered by Dan asking "did you use the Nori workflow for this?": the honest answer was no, and checking *why* revealed that the `# BEGIN NORI-AI MANAGED BLOCK` section is entirely absent from `~/.claude/CLAUDE.md` on the MacBook Air — the researcher-profile runtime instructions haven't been loaded by any session on this machine since early June. Forensics via the `.bak` trail bracketed the loss to the Jun 4 AGENTS.md-rename fallout session and identified a structural asymmetry: the two dotfiles-managed blocks self-heal on every sync run, but the Nori block's only writer is a manual `sks switch researcher` — so a one-time wipe stayed invisible for six weeks. Handed off to a dotfiles-repo agent for remediation.

## Topics Explored

- **F5.e surface analysis under lifecycle-only §6.** STATUS.md writers in `branches` mode are exactly two, both on `main`: `start-research-line` Step 3 (Active-row append) and §6 step 4 (Active→Archived move). Conflict shapes: ceremony×ceremony (both append Archived rows — safe for keep-both), start×start (both append Active rows — safe), anything involving §6's Active-row *deletion* (NOT safe — keep-both would resurrect the deleted row).
- **Recent Sessions is retired only in `branches` mode.** In `main_only` mode, `update-docs` step 5 still appends capped one-liners — the script's original canonical case survives there (concurrent web+laptop sessions racing `main`). The 07-17 convo's "retired" phrasing was mode-incomplete.
- **RESEARCH_LOG.md races** (same branch from two sessions, the Appendix:534 scenario) are a third live surface, already named in the script's docstring.
- **Nori-block forensics.** Timeline from `~/.claude/CLAUDE.*.bak` (both dotfiles sync scripts keep 10 timestamped backups): Jun 3 06:54 — 48.7KB, block present. Jun 5 09:29 — 7.1KB, *only* the permissions block; personal-info and Nori both gone. Jul 9 16:44 — 24.3KB, personal-info restored (by `update_claude_personal_info.py` during the install.sh run), Nori still absent. The loss window lands exactly on the NORI_NOTES-documented Jun 4 session: `sks switch` re-hit the 0.20 "AGENTS.md (or CLAUDE.md) is required at the root" symlink bug, sks was upgraded to 0.26, `sks upload` was verified — but no successful post-upgrade *switch* is recorded. `purge_redundant_skills.py`'s docstring documents the mechanism: "sks switch is destructive — it rewrites the entire NORI-AI managed block from scratch."
- **False leads discarded during forensics:** the May 6/24 `~/.dotfiles_backup/` CLAUDE.md files are the *profile-level* instructions file (pre-rename AGENTS.md), not the runtime `~/.claude/CLAUDE.md` — they don't prove runtime-block state. `purge_redundant_skills.py` itself is well-guarded (splices only inside the block, only when the "Found N skills:" listing is present) and can't have gutted the file. Both splice functions in the sync scripts preserve surrounding content.

## Provisional Findings

- **The Appendix push-rejected entry is the right single wiring point,** with pointed one-liners at the three write sites (§6 step 4, `start-research-line` Step 3, `finish-convo` step 4) so agents see the recovery path where the race actually bites. The shape-gate travels with every mention: both-sides-added-lines only; deletions and order-as-semantics conflicts still surface to the user.
- **`resolve_append_conflict.py` had never been exercised** — first functional run was this session's smoke test (synthetic two-ceremony Archived-table conflict: both rows kept, markers removed, exit 0).
- **Self-healing asymmetry is the real lesson from the Nori incident.** `update_claude_permissions.py` and `update_claude_personal_info.py` re-splice their blocks on every run, so the Jun 4 wipe was invisible for them within a day. The Nori block's restore is install.sh *manual step 6* — no writer, no watchdog, no detection. Same failure shape the claude-exit registration guard exists for, different registration. Root-cause attribution to the Jun 4 failed switch is circumstantial (timing + documented failure that morning + documented destructive-rewrite behavior) but no competing hypothesis survived.
- **Six weeks of sessions on the Air ran without the researcher-profile runtime instructions** and nobody — humans or agents — noticed. Sessions can't miss context they never saw; detection came from a workflow question, not from any degradation signal.

## Decisions Made

- **Full wiring scope** (Dan): Appendix carve-out + all three pointed notes + docstring modernization. Personal `finishing-a-research-branch` skill deliberately skipped — template-scoped session.
- **PR #41 merged** with a real merge commit (`0098856`; SHA-pin `38517e9` reachable). Branch `f5e-append-conflict-wiring` deleted on origin and locally per §6 default.
- **Nori-block remediation delegated** to a dotfiles-repo agent (handoff written at session close): `sks switch researcher` + purge re-run (Dan-interactive), install.sh detection warning, NORI_NOTES incident entry, other-machines check.

## Results

Landed on `main`:
- `0098856` — Merge PR #41: Appendix carve-out (RESEARCHER.md:534 region), §6 step 4 push-race note, `start-research-line` Step 3 note, `finish-convo` step 4 note, `resolve_append_conflict.py` docstring rewritten mode-aware.

Repo state at session close: zero open PRs; local `main` at `0098856` + this convo commit, in sync with origin.

## Open Questions

- **Other machines' Nori-block state.** Was the Jun 4 wipe Air-only? `grep -c "NORI-AI MANAGED BLOCK" ~/.claude/CLAUDE.md` on Dans-MacBook-Pro and tarragon (expect ≥2 markers if healthy; the Air shows only the prose pointer). Owned by the dotfiles handoff.
- **What wrote `~/.claude/CLAUDE.md` on Jul 18 22:39?** Most plausibly `update_claude_permissions.py` via a `pclaude` launch; benign either way (the block was already gone by 07-17 session start), but unattributed.
- **Carried over from 07-17, still open:** promote the real-merge-commit convention somewhere durable (`.github/PULL_REQUEST_TEMPLATE.md` or RESEARCHER.md contributor note); econ-impact plan Phase-4 retirement check (belongs to an econ-impact session).
- **Personal `finishing-a-research-branch` wiring** — deliberately unscoped this session; untracked unless Dan captures a task.

## Process notes

- claude-exit `prove_termination_works` ceremony ran cleanly at session start (child spawned/verified/killed via shared `_dispatch_terminate`; target PID + UID match confirmed). One unacknowledged invocation since 07-14 surfaced to Dan.
- `gh pr create` with a heredoc body was hard-failed by the `block_newline_hash_in_quoted_arg` hook (markdown `#` headers inside quoted arg) — Write-then-`--body-file` worked first try, as the hook's nastygram prescribes.
- Session spanned a date rollover (started 07-17, closed 07-19).
