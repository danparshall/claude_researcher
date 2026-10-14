# Session identity lock

**Date:** 2026-10-14
**Branch:** convo-name-announce
**Surface:** claude-code
**Machine:** pro
**Session:** Dan (pro, dotfiles, 20261014T1141, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-claude-researcher/c8969ab1-907b-4229-a33f-0831e6fc79a5.jsonl · —

## Summary

Dan hit a web session that was moved between claude.ai Projects mid-chat, then built itself a new codename (new repo slot, new timestamp), never announced it, and kept committing. Tracking down which commits came from which chat took a long time. His rule: an agent never changes its codename. A repo slot that is no longer correct is still useful, because it says where to go looking for the session's other work. He also asked that the first reply carry one fixed, greppable line: date, session id / chat link, codename, convo name.

The CLI side contradicts the rule by design: dotfiles `personal_info.md` and `claude-hooks/session_identity.py` recompute the repo slot at every commit, and the model slot follows `/model`. This session's own codename shows the effect: it launched in `claude_researcher` but its codename says `dotfiles`, the repo of its first commit.

Dan asked to test the web sandbox before committing to a design. Two throwaway web chats (Projects `moosenger` and `daydreaming`) were moved between Projects and probed. The first design ("set the codename as global git config") failed the test; the revised design passed. The session is the dotfiles `researcher-upstream-sync` session (publish of researcher 1.0.30), which branched into this topic; it is recorded here because the work lands in this repo.

## Topics Explored

- Where the codename is built: RESEARCHER.md §2.0b (web, per-repo `git config user.name`), dotfiles `personal_info.md` "Session identity on CLI commits" and `session_identity.py` (CLI, repo slot computed per commit).
- Whether a moved web chat keeps its sandbox, what survives, and what identifiers the sandbox exposes.
- Where a commit guard can live without clashing with existing hooks.

## Provisional Findings

From the two web probes (raw output pasted in the session transcript):

- **A Project move keeps the same container and the same session ids.** `CLAUDE_CODE_SESSION_ID`, `CLAUDE_CODE_REMOTE_SESSION_ID` and `CLAUDE_CODE_CONTAINER_ID` were unchanged across the move.
- **The move triggers a lazy VM reboot**, seen once ~4.5 min and once within ~10 min after the chat went idle. While an agent is busy (it polled for 12 min), no reboot happened. After the reboot, `CLAUDE_PROJECT_UUID` and `boot_id` change; environment variables are fixed per process, so the old UUID is shown until then.
- **`/home/claude` survives the reboot; `/root` does not.** A marker file in `/home/claude` survived. Global git config (`/root/.gitconfig`) was re-provisioned to `user.name=Claude`, `user.email=noreply@anthropic.com`, with commit signing via `/home/claude/.ssh/commit_signing_key.pub`. Likely cause of Dan's incident: after the reboot, a fresh clone had no codename, and the agent re-ran setup instead of reusing its identity.
- **Per-repo config and `.git/hooks` survive the reboot**, because the clone lives under `/home/claude`. Per-repo `user.name` overrides the re-provisioned global one: both test commits after the reboot carried the codename.
- **A pre-commit author guard works across the reboot.** A `git -c user.name=Claude commit` was refused both before and after the move; `core.hooksPath` is unset in the sandbox.
- **The chat link is derivable:** `CLAUDE_CODE_REMOTE_SESSION_ID=cse_<X>` ↔ `https://claude.ai/code/session_<X>`. Seen in one chat, before and after the move.
- **CLI identity file is already stable:** `session_identity.py` is registered with matcher `startup` only, so it does not rewrite `~/.claude/session-identity/<id>.env` on compaction or resume (this session's file is still from 11:41 UTC).
- Paper-collection repos set `core.hooksPath=.githooks` with a tracked `pre-commit`; the guard should be `commit-msg`, installed into `$(git rev-parse --git-path hooks)` like the post-commit hook.

## Decisions Made

- The codename is fixed for the whole session on both surfaces, including the repo slot. (The model slot is an open question; see the plan.)
- First reply opens with one fixed line: date, session id + chat link (web) or transcript path (CLI), codename, convo name. Convo name may be `pending`, is set once, and may be renamed once more at finish-convo; the other fields never change. The line is repeated verbatim after a Project move, a new clone or a compaction.
- Web: identity lives in a write-once file on `/home/claude`; per-repo git identity is set from it in every clone; a `commit-msg` guard refuses commits whose author is not the codename.
- Build on the unmerged `convo-name-announce` branch (Dan: it isn't finished; this change came up while testing it).
- Plan: [`docs/plans/16_session_identity_lock.md`](../plans/16_session_identity_lock.md).

## Results

- None saved as files; probe output is in the transcript.

## Open Questions

- Model slot: freeze it too, or keep it tracking `/model` on CLI?
- A clone made after a move has no per-repo identity or guard until setup runs in it; only the agent rule covers it.
- Is the reboot trigger idleness, or something else? Two observations only.
- An unused worktree `.worktrees/session-identity-lock` (no commits of its own) was created before Dan said to build here; Dan to remove it.
