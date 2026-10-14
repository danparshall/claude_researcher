# Session Identity Lock Implementation Plan

**Goal:** Every session, on web and CLI, gets one codename for its whole life, announced in one fixed greppable line, and a web commit cannot go out under any other author.

**Originating conversation:** [`docs/convos/20261014_session_identity_lock.md`](../convos/20261014_session_identity_lock.md)

**Context:** A web chat moved between claude.ai Projects rebuilt its codename after the sandbox rebooted, never announced it, and kept committing; Dan spent a long time tracing it. His rule: a session never changes its codename, even when its repo slot is no longer correct — the stale repo still says where to look. The CLI rules currently do the opposite on purpose (repo slot recomputed per commit).

**Confidence:** High for the web mechanics — every piece was tested across a real Project move and VM reboot (see the convo's Provisional Findings). Medium on the reboot trigger (two observations) and on the chat-link derivation (one chat).

**Architecture:** One write-once identity file per session holds date, ids, chat link, codename and convo name. On web it lives on `/home/claude` (survives the reboot), and every clone gets a per-repo `user.name` from it plus a `commit-msg` guard that refuses any other author. On CLI the existing `session_identity.py` startup hook writes the same fields, including the launch repo, and the commit template reads fixed values instead of recomputing.

**Branch:** web half on `session-identity-lock` in `claude_researcher` (worktree `/Users/dan/code/claude_researcher/.worktrees/session-identity-lock`), branched from main after the convo-name rule merged (PR #88). CLI half on a new dotfiles branch `session-identity-lock` (worktree `/Users/dan/code/dotfiles/.worktrees/session-identity-lock`, create with the using-git-worktrees skill).

**Tech Stack:** POSIX sh (sandbox hook), bash snippets in RESEARCHER.md, Python 3.12 + pytest (dotfiles hook and a hook test here).

---

## The fixed line

Both surfaces, first reply, first line:

```
Session: 2026-10-14 · <session id> · <chat link | transcript path> · <codename> · convo <name | pending>
```

- Date: UTC, from the session-start timestamp; never re-run.
- Web: `CLAUDE_CODE_SESSION_ID` and `https://claude.ai/code/session_<X>` where `CLAUDE_CODE_REMOTE_SESSION_ID=cse_<X>`. CLI: session id and transcript path.
- Codename: `<display name> (<web|host tag>, <repo>, <SESSION_TS>, <model>)`. Repo = the repo at session start (web: the Project's `REPO`; CLI: the launch directory's repo).
- Convo: `pending` until named. Named once; finish-convo may rename it once more. Each change rewrites only the `CONVO` field and re-shows the line.
- Re-show the line verbatim after: a Project move, any new clone, a compaction, a convo rename.
- Purpose stated to the agent: Dan greps for these values across chats, logs and commits; they never change within a session, even if the session is reassigned to another Project or repo.

## Testing Plan

**claude_researcher — `tools/test_commit_msg_guard.py` (pytest, runs the real hook in temp repos):**
- Commit by the codename author succeeds.
- Commit with `-c user.name=Claude` is refused, exit non-zero, and stderr names the expected codename and the identity file path.
- Identity file missing → commit refused with a message saying to restore identity (never silently allowed: an unguarded commit is the failure we're preventing).
- Codename containing parentheses, commas and spaces round-trips (the real format).
- Works when `core.hooksPath=.githooks` and the hook is installed there (paper-collection repos).

**dotfiles — extend `claude-hooks/test_session_identity.py`:**
- Launch cwd inside a repo → identity file and context line carry that repo's name; from a linked worktree, the main repo's name.
- Launch cwd not in a repo → repo slot is the directory basename.
- Context line contains the fixed `Session:` line with date, session id, transcript path, codename, `convo pending`.
- An existing identity file for the same session id is left unchanged (write-once), and its values are what the context line shows.
- Payload without a model → codename carries `<MODEL>` and the context line tells the agent to fill it once and write it to the file.

**Acceptance (manual, web):** repeat the two-message probe from the convo with the real RESEARCHER.md: start in Project A, commit, move to Project B, idle ≥5 min, confirm the reboot (`boot_id` changed), clone B's repo per the new rule, commit in both clones. Expect: one codename on every commit, the fixed line repeated unchanged, a `Claude`-author commit refused.

NOTE: I will write *all* tests before I add any implementation behavior.

## Tasks — web (claude_researcher, branch `session-identity-lock`)

1. Write `tools/test_commit_msg_guard.py` per the testing plan. Run; confirm it fails (hook absent).
2. Add `template/hooks/commit-msg` (sh): source `/home/claude/.session-identity/$CLAUDE_CODE_SESSION_ID.env`; compare `git var GIT_AUTHOR_IDENT` name with `CODENAME`; refuse with a one-line fix (`git config user.name "<codename>"`). Header comment: why it exists, link to this plan. Run tests; pass. Commit.
3. RESEARCHER.md §2.0b "Per-session codename": replace the build-and-set block with:
   - If `/home/claude/.session-identity/$CLAUDE_CODE_SESSION_ID.env` exists: source it; do not rebuild. Otherwise write it once (fields: `SESSION_DATE`, `SESSION_TS`, `SESSION_ID`, `REMOTE_SESSION_ID`, `CHAT_LINK`, `CODENAME`, `COMMIT_EMAIL`, `CONVO=pending`), values single-quoted.
   - In every clone (the session's first and any later one): `git config user.name/user.email` from the file; install `commit-msg` into `$(git rev-parse --git-path hooks)` at clone time (not after first push, unlike post-commit); same tracked-hook and `.git/info/exclude` handling as post-commit.
   - Never `git config --global` for identity: `/root` is re-provisioned on reboot.
   - State why: Project moves reboot the VM lazily; only `/home/claude` survives.
4. RESEARCHER.md §2e: first reply opens with the fixed line; the re-show triggers; the "never change, even if reassigned" sentence. Fold the convo-name rule from `db93874` into it (convo field; `pending` allowed).
5. ~~finish-convo and update-docs skills~~ — **moved to the CLI half (CLI Task 4b).** `template/skills/` here is generated by the dotfiles skill exporter (`.export_manifest.json`), so a hand edit would be overwritten on the next export. Found during implementation, 2026-10-14.
6. HUMANS.md: one paragraph explaining the line and what to grep.
7. Commit, push, run the manual acceptance test with Dan.

## Tasks — CLI (dotfiles, new branch `session-identity-lock`)

1. Write the new tests in `claude-hooks/test_session_identity.py`. Run; confirm failures.
2. `session_identity.py`: capture the launch repo (`git rev-parse --git-common-dir` from the hook's cwd, else cwd basename); write `REPO`, `CODENAME`, `CONVO=pending` to the env file, write-once; emit the fixed line and a commit template using `CODENAME` verbatim; remove "computed fresh per commit". Run tests; pass. Commit.
3. `claude/personal_info.md` "Session identity on CLI commits" and the "User display name" bullet: codename read from the env file, never recomputed; drop the per-commit repo recipe and its rationale paragraph. Re-run `install.sh` so the managed block updates; check `sync_check.py` (C8 compares slot count against personal_info.md).
4. `nori-researcher/AGENTS.md` startup checklist: first reply opens with the fixed line; convo-name step points at the `CONVO` field.
4b. (Moved from web Task 5.) finish-convo and update-docs skill sources in dotfiles: read codename and chat link / transcript path from the identity file (web `/home/claude/.session-identity/<id>.env`, CLI `~/.claude/session-identity/<id>.env`); finish-convo's rename updates `CONVO` only and re-shows the fixed line. Drop finish-convo's "model slot reflecting the model you are running as now" (the model slot is frozen). Keep its model-change note on the sentinel line, since it still records which model did the work; drop only its "list commits with the old model slot" part, because every commit now carries the start model. Re-run `install.sh` so the exporter carries them to claude_researcher `template/skills/`.
5. Full test suite; push; PR.

**Testing Details** The guard test drives real `git commit` calls in temp repos and checks only outcome (commit exists or not) and the message the agent will act on. The hook tests call `main()` with a payload and a cwd and check the env file and printed line — the two things later agents read — not internal helpers.

**Implementation Details**
- Web identity file: `/home/claude/.session-identity/<CLAUDE_CODE_SESSION_ID>.env`; CLI stays `~/.claude/session-identity/<id>.env`. Same field names.
- Write-once everywhere; only `CONVO` is ever rewritten.
- Guard is `commit-msg`, not `pre-commit`: paper-collection repos track a `pre-commit` in `.githooks`.
- Per-repo identity, never global, on web.
- `git commit -n` skips the guard; accepted (an agent doing that is deliberate, not drifting).
- The sandbox signs commits with a key independent of `user.name`; the codename does not affect signing.
- LITE mode (`template_lite/LITE.md`) builds no codename today; out of scope.
- RESEARCHER.md is unpinned; no BOOTSTRAP repin needed unless `_PROJECT_INSTRUCTIONS.md.template` changes.

**What could change:**
- The reboot trigger (idle ~5 min, two observations) — the design doesn't depend on it, but the acceptance test does.
- The chat-link derivation (one chat). If it fails, fall back to the agent copying the link from its `Claude-Session` system reminder.
- Platform changes to `/home/claude` persistence would break the web half; the guard would then refuse commits loudly rather than mis-attribute them.

**Questions**
1. Model slot: freeze it too (your literal rule: never change), or keep tracking `/model` on CLI? Default in this plan: freeze — the codename shows the model at session start.
2. New clone after a move: the rule depends on the agent running setup in it. Acceptable, or should the guard also be installed into every existing clone at each session-start check so a forgotten setup is caught at first commit? (It can't be installed into a clone that doesn't exist yet.)
3. CLI repo slot when launched outside any repo (e.g. `~`): directory basename (`dan`)? Or `none`?
4. Should the guard also check the email, or only the name?
5. Existing sessions mid-flight when this ships have no identity file: web setup will create one on their next setup pass, possibly with a new timestamp. Acceptable one-time break?

**Answers (Dan, 2026-10-14):** 1. Freeze. 2. Rule only; no re-install into existing clones. 3. Directory basename. 4. Name only (no objection raised to the default). 5. Accept the one-time break.

---
