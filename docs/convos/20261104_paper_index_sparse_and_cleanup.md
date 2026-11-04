# 20261104_paper_index_sparse_and_cleanup

**Date:** 2026-11-04
**Branch:** convo-20261104-paper-index-sparse (code in dotfiles `paper-index-sparse`, merged)
**Surface:** claude-code
**Machine:** Dans-MacBook-Air
**Session:** Dan (air, claude_researcher, 20261104T1443, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-claude-researcher/ade46131-62cb-41b4-845c-b5fec755122c.jsonl · —

## Summary

Dan asked for a look at this repo's open code tasks (skipping dotfiles' own issues) and a plan. The agent ranked them: the paper-index pair #108 (sparse worktrees miscount) and #109 (hook fires on any staged PDF) as the best first job; #104 and #96 as code-done, needing only acceptance runs; #79, #107, #77 and #66 as larger or web-gated. Only #21 (task label color) was judged a quick pass, so it was folded in. Dan approved.

The paper-index source lives in dotfiles (`nori-researcher/skills/paper-index/`, with tests); `template/skills/` here is the exporter's copy. Work was done TDD in a dotfiles worktree, merged to dotfiles `main` as `546ae8e`, and reached this repo via the exporter on Dan's `/sync-dotfiles` (export commit `1c76e32`, trailer `dotfiles@79f84ac`, which contains `546ae8e`). The REST half of #21 (`template/reference/GH_TO_REST.md`, not exporter-owned) was merged here as `c51c84d`. #108, #109 and #21 are closed with summary comments.

The rest of the session was cleanup: a survey of worktrees in both repos, removal commands for Dan (agents can't run `git worktree remove`), merging the stranded Oct 19 convo branch (`2907870`, RESEARCH_LOG conflict resolved by keeping both entries), and a handoff prompt for a later agent to clean up the ~30 stale branches.

## Topics Explored

- #108 design: count a file as present if it's on disk **or** has git's skip-worktree bit (`git ls-files -t`, tag `S`). This is narrower than the issue's "all tracked files are present", which would hide a PDF deleted by hand in a full checkout.
- #109 design: the hook keeps its cheap shell prefilter, then pipes staged paths (`-z`) to a new `paper_index.py hook-filter` subcommand, which reads `paper_index.toml` at commit time. This replaces the issue's suggestion to bake `extra_pdf_dirs` into the hook at print time, which would go stale when the config changes. If an older tool lacks the subcommand, the hook runs the check rather than skipping it.
- The hand fix in verification (`*papers/*.pdf*`) is itself buggy. In a shell `case`, `*` matches newlines, so `papers/text/a.txt` plus `deliverables/r.pdf` still matched, as did `otherpapers/x.pdf`.
- A subagent reviewed the test quality. Adopted: tests for `git rm` of a paper PDF, a PDF name with spaces and accents, and a collection in a repo subdirectory. Rejected: its claim that the deleted-PDF test can't catch over-counting. It does catch it; it's a guard test, not a RED test.
- How the export reaches here: `install.sh` → `update_claude_permissions.py` → `export_profile_skills.auto_export`. It runs only on the Air (flag `~/.claude_researcher.publisher`) and is silent when blocked, so check for the export commit afterwards.

## Provisional Findings

- Tests: paper-index 125 passed, 1 skipped (12 new); paper_migrate 206 passed.
- `/sync-dotfiles` updates the tool and the template, not each repo's committed `.githooks/pre-commit`. Old hooks call the updated tool, so they already get #108, but not #109's narrower trigger. That needs `--print-hook` re-run per repo.
- `git fetch` without `--prune` left stale refs for remote branches already deleted (`tarragon-os-aware-setup`, `proxy-only`). The agent's survey reported them as pushed, and one missing ref made each multi-branch `push --delete` reject the whole push. Corrected commands were given.
- Worktree folder names can differ from their branch: `.worktrees/skillset-sync-phase4` held `hookspath-auto-push`. The agent's first removal command used the branch name and missed it.

## Decisions Made

- Fix in dotfiles and let the exporter carry it, rather than hand-copying into a branch here, which would fight the exporter's manifest.
- Merge dotfiles `paper-index-sparse` (Dan: yes), merge #21's REST line (Dan: yes), merge the Oct 19 convo branch (Dan: yes).
- Stale-branch cleanup handed off to a later agent (handoff prompt given in chat; the key points are under Open Questions).

## Results

- dotfiles `546ae8e`: `count_papers.py` (`sparse_absent_files`), `paper_index.py` (`hook-filter`, new hook text), paper-index SKILL.md, `test_paper_index.py`, task-create SKILL.md (`--color 0052CC`).
- claude_researcher: export `1c76e32`, #21 REST merge `c51c84d`, Oct 19 convo merge `2907870`.

## Open Questions

- **Undecided:** file a task for `paper_index.py check` to warn when a repo's `.githooks/pre-commit` differs from `--print-hook`, so committed hooks don't go stale after future changes.
- verification's hook still has the buggy hand-edited pattern. Re-run `--print-hook` there (another repo; ask first).
- #108 follow-ups not done: a sparse-checkout step in `using-git-worktrees` (with the `git add --sparse` note), and dropping the "full checkout for collection branches" exception in general-ai-abilities' CLAUDE.md.
- Stale branches: claude_researcher has ~16 local and ~30 remote branches besides `main`; dotfiles has 6 remote. For the handoff: run `fetch --prune` first, and check for squash merges via `gh pr list --state merged --head <branch>`, because `merge-base --is-ancestor` misses them. Dan removes worktrees himself.
- #104 and #96 still await their acceptance runs (web-surface run; fresh-session `/model` test).
