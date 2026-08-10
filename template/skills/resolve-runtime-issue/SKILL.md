---
name: resolve-runtime-issue
description: Diagnose and recover from the common runtime failure modes of `claude_researcher`'s claude.ai runtime — expired PAT, network errors, non-fast-forward pushes (with the safe append-conflict recovery), protected-branch pushes, lost sandbox state, missing config, stale raw-CDN reads. Consult this skill when something in a session-start fetch, a git operation, or a REST call fails in a way that isn't self-explanatory.
---

## When to use

Fire on any of: a `curl` returning 401/403/404 from `api.github.com`; a `git clone` / `git push` / `git pull` failing; the sandbox filesystem coming back empty mid-session; a file WebFetched from `raw.githubusercontent.com` disagreeing with what a recent commit implies; STATUS.md missing a field the runtime expects; SKILL_INDEX.md unreachable.

The workflow is: look up the failure signature below → apply the recovery → surface to the user if the recovery requires their action or if the failure is unfamiliar.

# Recovery table

## PAT expired or insufficient scope (401, 403)

Symptom: `curl` returns 401/403 against `api.github.com`, or `git clone` / `git push` errors with `fatal: Authentication failed`.

Recovery: re-bootstrap RESEARCHER.md §2b — the user rotates the PAT and re-pastes Project Instructions. Most common cause of session-start failure.

## Connection error on `api.github.com` or `git clone`

Symptom: network unreachable, DNS failure, `curl: (6) Could not resolve host`, `git clone` hangs or fails to connect.

Recovery: network access isn't enabled on this claude.ai Project, or doesn't permit `github.com` / `api.github.com`. Re-check Settings per BOOTSTRAP Step 1. **If the change was made in this same chat session, the user must start a fresh chat to pick it up** — network-access changes are empirically NOT propagated in-chat.

## `git push` rejected — non-fast-forward

Symptom: `! [rejected]` from `git push`, message includes `non-fast-forward` or `fetch first`.

Cause: the remote branch advanced since the §2.0b clone (or since the last pull) — typically because the user pushed from another session or their laptop, or, on `main`, another agent ran a STATUS-writing ceremony concurrently.

Recovery: `git pull --rebase origin <branch>`, then re-push. If the rebase has conflicts:

- **Default:** surface conflicts to the user; do NOT auto-resolve.
- **One carve-out (append-on-top ledgers):** if every conflict region sits in one of the append-on-top ledgers below, AND inspecting the conflict markers confirms **both sides only added lines** (no shared line deleted or edited by either side), resolve by keeping both with `python3 /home/claude/.claude_researcher_template/template/scripts/resolve_append_conflict.py <file>`, then `git add <file>`, `git rebase --continue`, and re-push. Read the script's docstring before first use — it carries the full safety gate.

  Append-on-top ledgers:
  - STATUS.md `## Active Research Lines` table
  - STATUS.md `## Archived Research Lines` table
  - STATUS.md `## Recent Sessions` (`main_only` mode only)
  - `docs/active/<branch>/RESEARCH_LOG.md` newest-first entries

- **Not the append-only shape:** any conflict that isn't exactly this shape — e.g., a merge ceremony's Active-row *deletion* tangled with a neighboring edit, where keep-both would resurrect the deleted row — goes to the user.

## `git push` rejected — protected branch (403, "protected branch hook declined")

Symptom: push to `main` fails with 403 or the "protected branch hook declined" message.

Cause: the user has branch protection on `main` and the agent tried to push directly. This is the same case as the merge-time collaborator-mode block.

Recovery: don't push to `main`. Open a PR via the Pulls API (see `finishing-a-research-branch` skill Step 2), or hand the change off to the user to merge in the web UI if they don't want you to open a PR from an agent-authored branch.

## `git clone` fails for the project repo (§2.0b)

Symptom: RESEARCHER.md §2.0b clone errors out.

Recovery: surface to user. Most likely PAT expiry (see above), second most likely a `<REPO>` mismatch in Project Instructions. As a **degraded fallback**, operate against the Contents API per-file using the legacy recipes still documented at RESEARCHER.md §2c, §3, and inside `finishing-a-research-branch`. Tell the user you're in degraded mode: one commit per file, no `git diff` introspection, the noisy-history problem that the clone-first architecture was designed to fix.

## Sandbox state lost between turns / `/home/claude/${REPO}/` gone

Symptom: paths that existed earlier in the session return `No such file or directory`; `pwd` from inside the working tree fails.

Cause: the claude.ai sandbox filesystem can reset on some session paths.

Recovery: re-run the §2.0b clone to recover. **Any unpushed commits in the prior working tree are lost.** If you're uncertain whether a write completed, `git log --oneline -10` on the fresh clone tells you what's actually on the remote.

## STATUS.md missing `workflow_mode` field

Symptom: the top-of-file `workflow_mode: <value>` line is absent.

Recovery: assume `branches` (the v1 default). Don't error. Proceed with the branches-mode paths for `start-research-line`, `finish-convo`, `finishing-a-research-branch`.

## SKILL_INDEX.md unreachable

Symptom: DNS failure, 404, or timeout on the SKILL_INDEX read from both the local template clone and the WebFetch fallback.

Recovery: operate without skills. Surface to user. The session degrades to "you have my judgment but no shared toolkit" — the user may want to wait for upstream to recover before doing skill-shaped work.

## User-named repo doesn't match Project Instructions

Symptom: user's first message references a `<REPO>` that isn't the one in Project Instructions.

Recovery: RESEARCHER.md §4. **Don't proceed.** State the mismatch; ask whether to continue with this Project's `<REPO>` or stop so the user can switch Projects. Never write to a repo the Project isn't bound to.

## Project Instructions look truncated

Symptom: `TOKEN`, `USERNAME`, `REPO`, or the recipe blocks are missing from your context.

Recovery: stop. The bootstrap may not have completed correctly. Walk the user through re-pasting Project Instructions per BOOTSTRAP Step 8.

## `main` protected and merge fails (405 / 422)

Symptom: `finishing-a-research-branch` Step 3 (PR merge) returns 405 or 422.

Recovery: the collaborator-mode case. Stop, surface the PR URL to the user, wait for the owner to review and merge in the GitHub web UI. The archive steps (directory move + STATUS update) wait for a future session — typically the owner will do them after merging.

## Stale content from `raw.githubusercontent.com`

Symptom: content WebFetched from `raw.githubusercontent.com` doesn't match what `STATUS.md` or a recent commit implies should be there.

Cause: GitHub's raw CDN can serve stale content for **24+ hours** after an upstream write (empirically observed 2026-05-11; the previously-published ~5-minute estimate was wrong by orders of magnitude). This is why RESEARCHER.md §2.0a makes the local clone the primary architecture — `git clone` against `github.com` and reads against the Contents API don't suffer the same staleness.

Recovery: if you've fallen through to the WebFetch fallback and the content looks wrong, retry against the Contents API URL (`https://api.github.com/repos/danparshall/claude_researcher/contents/PATH`) for time-sensitive reads, or run the §2.0a clone now if it never succeeded.
