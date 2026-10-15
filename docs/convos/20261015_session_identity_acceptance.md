# 20261015_session_identity_acceptance

**Date:** 2026-10-15
**Branch:** main (no line; the plan 16 branches are merged)
**Surface:** claude-code (this session drove the test); the test itself ran in one claude.ai web chat
**Machine:** pro
**Session:** Dan (pro, claude_researcher, 20261015T2022, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-claude-researcher/a4ee21e5-0f2c-405d-9e14-e1596a8fd88c.jsonl · —
**Web chat under test:** Dan (web, moosenger, 20261015T2051, opus-5.5) · https://claude.ai/code/session_011iwLUA4nQp5Pf3X5stNLWP

## Summary
This session ran the manual web acceptance test for plan 16 (`docs/plans/16_session_identity_lock.md`), tracked in #89, and the Co-Authored-By check from #74. Both plan 16 halves were merged on 2026-10-14 without this run (`docs/convos/20261014_session_identity_lock_build.md`).

Precondition: the Air had not exported skills since dotfiles #123 merged (last export 8e81408 at 19:22 UTC on 10-14; #123 merged 21:41 UTC). Dan ran `/sync-dotfiles` on the Air; export 726ec8e (`Dan (skill-exporter, air)`, 20:30 UTC on 10-15) brought `template/skills/finish-convo` and `update-docs` to the identity-file text, including the web path `/home/claude/.session-identity/$CLAUDE_CODE_SESSION_ID.env`.

The test: one web chat started in Project `moosenger`, committed on a scratch branch `acceptance-89`, was moved to Project `daydreaming` and left idle, then cloned daydreaming's repo and committed in both clones, and tried a `Claude`-author commit. Message 2 did not tell the agent to set identity or install the guard in the new clone; it did both from RESEARCHER.md §2.0b on its own. **Result: pass on every criterion.**

## Topics Explored
- Whether the skill export had happened (it hadn't; fixed on the Air)
- The two prompts for the web chat, and the idle wait between them
- Checking the pushed commits from here with `gh api`, independent of the web agent's own report

## Provisional Findings
- **One codename on every commit.** Checked on GitHub: `moosenger@acceptance-89` 347417e (commit 1, before the move) and 288395e (commit 3, after), `daydreaming@acceptance-89` 66e2ae0 (commit 2, new clone after the move). All three have author and committer `Dan (web, moosenger, 20261015T2051, opus-5.5) <parshall.dan@gmail.com>`. The daydreaming commit names `moosenger`, which is the intended stale repo slot.
- **Co-Authored-By (#74): absent** from all three web commits. Each carries `Claude-Session: https://claude.ai/code/session_011iwLUA4nQp5Pf3X5stNLWP`. GitHub shows them unverified, as §2.0b expects.
- **Guard refuses a wrong author.** `git -c user.name=Claude commit --allow-empty` in the daydreaming clone exited 1 with the message naming the codename and the identity file; HEAD stayed at 66e2ae0.
- **Reboot confirmed, twice.** boot_id `3f15c7c6…` at start → `d534c1e6…` at 17:07 EDT → `e018dacc…` at 17:15 EDT. The identity file kept its 16:52 mtime and content across both; global git config came back as `Claude <noreply@anthropic.com>` each time without affecting either clone.
- **Session line unchanged:** the web agent reports it repeated it unchanged; the line in its final message matches the identity file field for field. Dan saw the first reply directly.
- **`CLAUDE_PROJECT_UUID` lags the move by one reboot.** At the first reboot (17:07) `project_info` already said daydreaming, but the env var and the agent's Project Instructions were still moosenger's; both updated at the second reboot (17:15). One run only. Nothing in `template/` reads `CLAUDE_PROJECT_UUID` or `project_info` (grep, this session), so no current rule is affected; a future move detector shouldn't rely on the env var alone.
- **Repo attachments outlive a move.** moosenger (and claude_research_config, dotfiles) stayed attached with push access after the move; commit 3 was pushed by the post-commit hook installed before the move. That's what §4 assumes, but a user might not expect a moved chat to keep write access to the old Project's repo.
- **Small doc bug:** the agent stored `CONVO='20261015_acceptance_89.md'`, with the `.md`. RESEARCHER.md §2e gives the convo name format as `${SESSION_DATE}_<short-slug>.md`, mixing up the name and the filename, so the `Session:` line then shows `convo …​.md`.

## Decisions Made
- Commits went on a scratch branch `acceptance-89` in each repo, not `main`.
- Plan 16's acceptance status updated to passed; #89 closed; dotfiles STATUS row `session-identity-lock` moved to Archived.
- Recorded on main, following the precedent for no-line sessions here.

## Results
- Commit evidence is in Provisional Findings (SHAs on GitHub); no results files.

## Open Questions
- Delete the two `acceptance-89` branches (moosenger, daydreaming) on GitHub; the sandbox proxy refuses branch deletion.
- Fix the `.md` in §2e's convo-name format.
- Close #74 now that its check passed?
- Is the two-reboot pattern after a move deterministic? One run.
- Still open from the build convo: the identity-file heredoc breaks on a display name containing an apostrophe; tarragon still needs `/sync-dotfiles` + `install.sh`.
