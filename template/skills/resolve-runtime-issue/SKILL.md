---
name: resolve-runtime-issue
description: Diagnose and recover from the common runtime failure modes of `claude_researcher`'s claude.ai runtime — GitHub proxy refusals (repo not attached, repo not found, API path not available, GitHub not connected, app not installed, blocked `gh` commands), refused permission checks, network errors, non-fast-forward pushes (with the safe append-conflict recovery), protected-branch pushes, lost sandbox state, missing config, stale raw-CDN reads. Consult this skill when something in a session-start fetch, a git operation, or a REST call fails in a way that isn't self-explanatory.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

## When to use

Fire on any of: a `curl` returning 401/403/404/415 from `api.github.com`; a `git clone` / `git push` / `git pull` failing; a `gh` command or the add-repository tool refusing; the sandbox filesystem coming back empty mid-session; a file WebFetched from `raw.githubusercontent.com` disagreeing with what a recent commit implies; STATUS.md missing a field the runtime expects; SKILL_INDEX.md unreachable.

The workflow is: look up the failure signature below → apply the recovery → surface to the user if the recovery requires their action or if the failure is unfamiliar.

# Recovery table

## Repo not attached to this session (403)

Symptom: `git push` fails with `access denied by the git proxy: <owner>/<repo> is not in this session's authorized repository set`, or a REST call returns 403 with `GitHub access to this repository is not enabled for this session. Use add_repo to request access.` Clone and fetch may still succeed, so it can look like a push-only fault.

Cause: the proxy only serves repos attached to this session. No credential in the URL or a header changes that.

Recovery: RESEARCHER.md §2.0c — attach the repo with the add-repository tool (read to read it; push before the first push), then retry. Commits made in the meantime are still local; push them with `git push -u origin HEAD`.

## Add-repository says the repo was not found

Symptom: the add-repository tool replies `repository "<owner>/<repo>" was not found on github.com, or this session's GitHub credential doesn't have access to it.`

Cause: the message can't tell a missing repo from one the Claude GitHub App can't see. Usual causes: a typo in the owner or name, the repo doesn't exist yet, or the App's "Only select repositories" list leaves it out.

Recovery: call `list_repos` with part of the name as `query`. If it lists the repo, call add-repository again with the exact owner/repo it shows. If not, ask the user whether the repo exists and whether the App can see it (github.com → Settings → Applications → Installed GitHub Apps → Claude → Configure → Repository access).

## "This GitHub API path is not available" (403)

Symptom: a REST call returns 403 with `This GitHub API path is not available: sessions are bound to their configured repositories. Use repository-scoped endpoints (repos/{owner}/{repo}/...).`

Cause: the proxy serves only paths under `repos/{owner}/{repo}/...`. Creating a repo (`POST /user/repos`), `/user`, and the search API are all refused. Not an access problem, and attaching more repos doesn't help.

Recovery: use a repository-scoped path (see `template/reference/GH_TO_REST.md`). If the step has no such path (for example, creating a repo), the user does it on github.com.

## GitHub not connected ("link your GitHub account")

Symptom: the add-repository tool returns `permission_denied: link your GitHub account`, or a REST call returns 403 with `No linked GitHub account`.

Recovery: the user connects GitHub to their Claude account (claude.ai Settings → Connectors → GitHub), then you request the repo again. The same chat picks the connection up; no fresh chat is needed.

## Connected, but pushes refused ("Claude doesn't have GitHub access")

Symptom: the add-repository reply says pushes "will be refused", or `git push` fails with `remote: Claude doesn't have GitHub access to <owner>/<repo>` and a link to install the Claude GitHub App. Clone, fetch and REST reads work.

Cause: the account is connected but the Claude GitHub App is not installed on the account that owns the repo, or its "Only select repositories" list leaves this repo out.

Recovery: the user installs the app from the link in the error (or adds the repo to the existing installation), then you retry the push. If it is still refused, the user reconnects GitHub from claude.ai settings, as the error suggests, to re-link the installation.

## `gh` fails with "GraphQL is not available" (403), or a REST write returns 415

Symptom: `gh issue …`, `gh pr …`, `gh label list` or `gh repo view` returns `HTTP 403: GitHub GraphQL is not available from Claude Code sessions`; or a `curl -X POST` / `PATCH` / `PUT` returns 415 `Request bodies must declare Content-Type: application/json`.

Recovery: neither is an access problem. Use the REST equivalent from `template/reference/GH_TO_REST.md` (`gh api <REST path>` or `curl`), and add `-H "Content-Type: application/json"` to every write.

## Permission check refused a step (auto-mode classifier)

Symptom: a tool call is denied with a message naming a permission check rather than GitHub or the proxy — for example, a refused add-repository push request, or a refused issue, PR or label write.

Cause: in auto mode, a classifier refuses actions it can't tie to something the user asked for. Project Instructions don't count as the user asking; a line the user types in chat does.

Recovery: show the user the denial text and ask. Don't retry the same step, and don't route around it (a different tool, a read attachment in place of push). For a refused push request, a one-line go-ahead typed by the user in chat ("yes, request push for <repo>") has worked. See RESEARCHER.md §2.0c, Permission checks.

## Connection error on `api.github.com` or `git clone`

Symptom: network unreachable, DNS failure, `curl: (6) Could not resolve host`, `git clone` hangs or fails to connect.

Recovery: network access isn't enabled for this claude.ai account, or its domain list leaves out the host that failed. Re-check Settings per BOOTSTRAP Step 1. A 403 from the GitHub proxy is not this; see the entries above. **If the change was made in this same chat session, the user must start a fresh chat to pick it up** — network-access changes are empirically NOT propagated in-chat.

## `git push` rejected — non-fast-forward

Symptom: `! [rejected]` from `git push`, message includes `non-fast-forward` or `fetch first`.

Cause: the remote branch advanced since the §2.0b clone (or since the last pull) — typically because the user pushed from another session or their laptop, or, on `main`, another agent ran a STATUS-writing ceremony concurrently.

Recovery: `git pull --rebase origin <branch>`, then re-push. If the rebase has conflicts:

- **Default:** surface conflicts to the user; do NOT auto-resolve.
- **One carve-out (append-on-top ledgers):** if every conflict region sits in one of the append-on-top ledgers below, AND inspecting the conflict markers confirms **both sides only added lines** (no shared line deleted or edited by either side), resolve by keeping both with `python3 {{skills_dir}}/finish-convo/resolve_append_conflict.py <file>`, then `git add <file>`, `git rebase --continue`, and re-push. Read the script's docstring before first use — it carries the full safety gate.

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

Recovery: surface to user. Most likely the repo is not attached to the session (see the entries above); fix that first, because the Contents API fallback is refused for an unattached repo too. Second most likely, a `<REPO>` mismatch in Project Instructions. As a **degraded fallback**, operate against the Contents API per-file using the legacy recipes still documented at RESEARCHER.md §2c, §3, and inside `finishing-a-research-branch`. Tell the user you're in degraded mode: one commit per file, no `git diff` introspection, the noisy-history problem that the clone-first architecture was designed to fix.

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

Symptom: the user references a repo that isn't the `<REPO>` in Project Instructions.

Recovery: RESEARCHER.md §4. Not an error: the Project's repo is a default, not a limit. Confirm which repo and why in one sentence, attach it read-only, and request push before writing to it (RESEARCHER.md §2.0c). Don't carry content between repos without the user's say-so.

## Project Instructions look truncated

Symptom: `USERNAME` or `REPO` is missing from your context.

Recovery: stop. The bootstrap may not have completed correctly. Walk the user through re-pasting Project Instructions per BOOTSTRAP Step 8.

## `main` protected and merge fails (405 / 422)

Symptom: `finishing-a-research-branch` Step 3 (PR merge) returns 405 or 422.

Recovery: the collaborator-mode case. Stop, surface the PR URL to the user, wait for the owner to review and merge in the GitHub web UI. The archive steps (directory move + STATUS update) wait for a future session — typically the owner will do them after merging.

## Stale content from `raw.githubusercontent.com`

Symptom: content WebFetched from `raw.githubusercontent.com` doesn't match what `STATUS.md` or a recent commit implies should be there.

Cause: GitHub's raw CDN can serve stale content for **24+ hours** after an upstream write (empirically observed 2026-05-11; the previously-published ~5-minute estimate was wrong by orders of magnitude). This is why RESEARCHER.md §2.0a makes the local clone the primary architecture — `git clone` against `github.com` and reads against the Contents API don't suffer the same staleness.

Recovery: if you've fallen through to the WebFetch fallback and the content looks wrong, retry against the Contents API URL (`https://api.github.com/repos/danparshall/claude_researcher/contents/PATH`) for time-sensitive reads, or run the §2.0a clone now if it never succeeded.
