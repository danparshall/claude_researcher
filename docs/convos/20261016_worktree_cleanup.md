# 20261016_worktree_cleanup

**Date:** 2026-10-16
**Branch:** convo-20261016-worktree-cleanup (session worked on main, `github-mcp-migration`, `precompact-update-docs`)
**Surface:** claude-code
**Machine:** Dans-MacBook-Pro
**Session:** Dan (pro, claude_researcher, 20261016T1103, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-claude-researcher/07d4aa37-c0f8-4ce0-9c83-6ae004c20a46.jsonl · —

## Summary

Dan asked for the worktrees to be cleaned up. The clean-worktrees inventory found 11 feature worktrees. Nine were merged, clean, had no `data/` directory, and their remote branches were already deleted: `ci-informational-workflow`, `convo-20261014-site-sync`, `convo-name-announce`, `convo-name-no-md`, `docs-sync-1015`, `humans-plan-handoff-tip`, `pi-version-header`, `proxy-only`, `session-identity-lock`. Two were unmerged but clean and pushed: `github-mcp-migration` and `precompact-update-docs`. No running process had its working directory in a worktree. Dan approved removing all 9 merged ones. `git worktree remove` is denied for agents, so he runs the removal commands himself.

Dan ruled `github-mcp-migration` overtaken by events. Anthropic moved web-session GitHub access behind a sandbox proxy that holds the credentials (#72), and PR #75 removed the template's PAT path, so neither the MCP connector nor the token dispenser has anything left to do. The line was retired with a note and merged as a record ([PR #93](https://github.com/danparshall/claude_researcher/pull/93), merge commit `b9c5c46`): RETIRED banners on plan 13, the design doc, the verification report and the briefing, plus a retirement note on the STATUS Branch line. `tools/fill_project_instructions.py` was dropped before the merge; it remains in history at `d79763e`.

`precompact-update-docs` held one file, the F1–F10 PreCompact probe results. It was merged as a record ([PR #94](https://github.com/danparshall/claude_researcher/pull/94), merge commit `d5f0c2b`) with a close-out note. The hook work now lives in dotfiles #116, which got a comment linking the doc and summarising the key finding. #42 was closed in its favour.

## Topics Explored
- Worktree inventory: data symlinks, untracked and ignored files, PR state, remote branches
- Whether #72 and dotfiles #116 had overtaken the two parked branches
- Where session records go now: root `RESEARCH_LOG.md`, not STATUS Recent sessions (per `c58c670`)

## Provisional Findings
- The probe doc's linked sidecar convo (`docs/convos/20260813_precompact_update_docs_hook.md`) was never committed on any branch, so that link has never resolved. This is now noted in the doc.
- `precompact-update-docs` never had a STATUS entry, so closing it needed no STATUS edit.
- The clean-worktrees skill's final step (`git worktree remove`) conflicts with Dan's permission denies. Every agent run of the skill ends with a hand-off to Dan.

## Decisions Made
- Retire `github-mcp-migration` permanently and merge its docs as a record, without the paste-helper (Dan).
- Merge the `precompact-update-docs` probe doc as a record, and move the hook work to dotfiles #116 (Dan: "merge them").
- Remove the 9 merged worktrees (Dan). Removing the two newly merged worktrees and deleting all the local branches is still to do.

## Results
- None (no analysis outputs).

## Open Questions
- Overdue reminders surfaced and not yet handled: claude_researcher #36; dotfiles #109, #70, #91, #68, #42, #35.
- Local branches still to delete with `git branch -d` once Dan removes the worktrees: the 9 above, plus `github-mcp-migration`, `precompact-update-docs`, and this convo branch once it merges.
