# 20261014_session_identity_lock_build

**Date:** 2026-10-14 (closed 2026-10-15)
**Branch:** session-identity-lock (claude_researcher and dotfiles; both merged)
**Surface:** claude-code
**Machine:** pro
**Session:** Dan (pro, claude_researcher, 20261014T2059, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-claude-researcher/e9687eba-1660-47a6-9615-18b46468e2b0.jsonl · —

## Summary
This session implemented plan 16 (`docs/plans/16_session_identity_lock.md`, from `docs/convos/20261014_session_identity_lock.md`): one codename per session, fixed at start, announced in a fixed greppable `Session:` line. First it cleared some setup confusion. A stray claude_researcher worktree `session-identity-lock` had been made earlier by another session by mistake; Dan removed it, and its merged local branch was deleted. The morning's PR #88 (convo-name rule and plan 16 docs) had not been merged, so Dan merged it and the work started fresh from 820ee40.

The web half (claude_researcher PR #90, merged as cf4ac40) adds `template/hooks/commit-msg`, a guard that refuses any commit whose author is not the identity file's `CODENAME`, or when the file or session id is missing. Six real-commit tests are in `tools/test_commit_msg_guard.py`. RESEARCHER.md §2.0b now has a write-once identity file on `/home/claude`, per-clone identity and the guard installed at clone time, and never global git identity. §2e has the fixed `Session:` line, and only `CONVO` is ever rewritten. HUMANS.md explains the line. The CLI half (dotfiles PR #123, merged as 637fcba) rewrites `claude-hooks/session_identity.py`. It sets the launch repo from the git common dir (else the cwd's name), writes the file once with single-quoted values, reuses an existing file, never uses the `unknown` session id, prints the fixed line, and has `<MODEL>` filled once if the payload lacks a model. It also updates personal_info.md, the Nori AGENTS.md startup step, and the update-docs and finish-convo skill sources. Tests: 34 in the hook test file; the full dotfiles suite of 1152 passed.

Dan had no time for the manual web acceptance run, so both PRs were merged without it ("YOLO the PRs and I'll check later"). Issue #89 holds the acceptance steps and reminder #74's Co-Authored-By check. `install.sh` ran on pro, so the live CLAUDE.md and the hook are current there.

## Topics Explored
- Whether the handoff was still valid; the stray worktree and the unmerged #88
- Plan 16's five Questions (answered by Dan; recorded in the plan)
- Where finish-convo/update-docs edits belong: `template/skills/` is exporter output, so they moved to dotfiles (plan Task 5 → CLI Task 4b)
- Skill exporter only runs on the Air (`~/.claude_researcher.publisher`, per dotfiles `notes/profile_skill_export.md`)

## Provisional Findings
- Editing `template/skills/` by hand here would be overwritten by the next export; skill changes have to go through dotfiles.
- On pro, `install.sh` does not export skills (silent no-op without the publisher flag). claude_researcher's `template/skills/update-docs` and `finish-convo` still carry the old text until the Air runs `/sync-dotfiles` and `install.sh`.
- The web mechanics have not been checked end to end. They rest on the two probe chats in the 2026-10-14 convo and on the automated guard tests.

## Decisions Made
- Dan's answers to the Questions: freeze the model slot; rule only for new clones (no re-install into existing ones); directory name for the no-repo CLI slot; guard checks name only; accept the one-time break for sessions already running.
- Merged #90 and dotfiles #123 without the acceptance run; plan 16 says so explicitly.
- Subagents commit under the parent's codename (my inference from "freeze", written into personal_info; Dan can revise).
- dotfiles STATUS row `session-identity-lock` stays active until #89 passes.
- This convo doc and log line are committed straight to main, following the precedent for no-line sessions here (e.g. 11bfdf7, 0e4014c).

## Results
- claude_researcher PR #90 (cf4ac40), dotfiles PR #123 (637fcba); issue #89

## Open Questions
- Acceptance run (#89, dated 2026-10-16): Project move, idle reboot, second clone, `Claude`-author refusal, Co-Authored-By check.
- Air (and tarragon): `/sync-dotfiles` + `install.sh` to export the skills and update CLAUDE.md there.
- Known gap: the web identity-file heredoc breaks on a display name containing an apostrophe (the CLI hook handles it).
- This session ran under the old hook, so its own commits used the per-commit repo slot (claude_researcher vs dotfiles).
- Leftover merged worktrees for Dan to remove: claude_researcher `convo-name-announce` and `session-identity-lock`, dotfiles `session-identity-lock`.
