# 20261015_docs_sync_and_branch_cleanup

**Date:** 2026-10-15
**Branch:** docs-sync-1015
**Surface:** claude-code
**Machine:** Dans-MacBook-Pro
**Session:** Dan (pro, claude_researcher, 20261015T2312, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-claude-researcher/b7bad3d6-60a9-435c-a291-65cd4769f449.jsonl · —

## Summary

Dan asked for a merged-and-synced check, then for the docs to be brought up to date on the repo and on clauderesearch.ai. Local `main` matched `origin/main` and the site repo (`site-claude-researcher`) was clean and synced. The finding: the site was *ahead* of this repo. On 2026-10-13 it shipped the proxy-only setup screenshots and the "All or Only select repositories" choice for the Claude GitHub App, but the repo still required "Only select" in README, BOOTSTRAP 6b and RESEARCHER §2.0c (#87), and held only the egress screenshot plus the retired PAT one (#85). The site needed no change; the newer repo material (the `Session:` line, announced convo names, the plan-in-one-chat tip) is HUMANS.md material, not front-door material.

Branch `docs-sync-1015` / [PR #92](https://github.com/danparshall/claude_researcher/pull/92): #87 wording in all three files (both choices, with the tradeoff); the five site screenshots copied into `template/reference/screenshots/`, logged in CAPTURED.md and shown in README "Setup at a glance" (the optional Auto permission-mode shot included, as on the site); `github_pat_read_write_flip.png` deleted at Dan's OK; HUMANS.md skill count 19 → 35; BOOTSTRAP repinned with `tools/repin.py` (template URLs → `a230b45`, README entry → `df9b02c`), commits authored with the session codename via `GIT_AUTHOR_NAME`/`GIT_COMMITTER_NAME` because the script calls plain `git commit`.

An agent error, corrected before merge: the agent asked Dan whether STATUS.md's "Recent sessions" list had been retired without checking, Dan said to backfill it, and eight entries went into the PR. At close-out the agent found the repo-root `RESEARCH_LOG.md` already logs every session from 10-04 to 10-15. The list had been retired by the "sessions don't write STATUS" convention. Dan chose to drop the backfill; STATUS.md is unchanged by this branch.

## Topics Explored

- Branch and worktree inventory across local, remote, and open PRs.
- Site vs repo drift since the site's last commit (`b8b5d5a`, 2026-10-13).
- Branch cleanup within the permission rules (agents cannot run `git worktree remove`).

## Provisional Findings

- The site can run ahead of the repo when Dan edits it directly; check the site's git log against open issues, not just the repo against the site.
- The clean-worktrees `worktree_inventory.py` reports a branch with zero commits ahead of main as "Merged: YES", even with live uncommitted work (it did so for `docs-sync-1015`). "Merged" alone is not a safe deletion signal.
- The new BOOTSTRAP pin has not been exercised by a fresh setup run.

## Decisions Made

- Offer both App repository-access choices everywhere (Dan's #87 decision, now upstream).
- Delete the retired PAT screenshot (Dan).
- Repin BOOTSTRAP rather than leave the old pin serving "Only select" only (Dan).
- Drop the STATUS.md backfill; RESEARCH_LOG.md is the session record (Dan).
- Branch cleanup: deleted 9 remote branches — 7 merged (`ci-informational-workflow`, `convo-name-announce`, `convo-name-no-md`, `humans-plan-handoff-tip`, `pi-version-header`, `proxy-only`, `session-identity-lock`) plus `sandbox-push-probe-20261007T0753` (self-labelled throwaway) and `aitaxbid-skills-audit` (content on main). The 8 merged local worktrees are removed by a one-off script Dan runs from his terminal, which refuses any worktree with changes or not an ancestor of `origin/main`.

## Results

- PR #92 (closes #85, #87).

## Open Questions

- Unmerged branches awaiting Dan's call: `github-mcp-migration` (shelved), `precompact-update-docs` (#42 probes; #42 reminder fired 2026-08-03), `convo-clauderesearcher-site-build` and `claude/claude-researcher-github-workflow-4zbkxm` (each holds a convo doc never merged to main), `add-clawxiv-reference`, `tighten-section-0`, `project-instructions-framing`, PR #76 (`andrea-incoming-starter-v2.5`).
- Fired reminders not yet handled: claude_researcher #42, #36; dotfiles #109, #70, #91, #68, #42, #35.
- Should `worktree_inventory.py` distinguish "zero commits ahead" from "merged"? (dotfiles skill source.)
