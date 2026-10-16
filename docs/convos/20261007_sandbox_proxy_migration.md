# Sandbox proxy migration

**Date:** 2026-10-07
**Branch:** sandbox-proxy-migration
**Surface:** claude.ai
**Machine:** sandbox
**Session:** Dan (web, claude_researcher, 20261007T0753, fable-5.1) · — · https://claude.ai/code/session_014mTVCm1KcqVXZ39HdZ3B2s

## Summary

Dan opened with "Anthropic just changed their backend sandbox, and fragged my workflow." The session ran the normal session-start sequence to find where it broke. Clone and read steps still worked with the PAT from Project Instructions, but every `git push` and every `api.github.com` call was refused with a 403. The refusals came from the sandbox, not from GitHub: web chat now runs on Anthropic's cloud-session infrastructure, where a GitHub proxy holds credentials outside the sandbox and only serves repos approved for the session.

Getting push working took three user-side steps, found one error at a time: connect GitHub to the Claude account, install the Claude GitHub App on the repos, and approve each repo in the session when the agent asks for it. After that, clone, push and REST calls all worked with no token at all. The auto-push hook worked unchanged and the per-session codename survived as commit author.

With that confirmed, the session changed the template so it supports both sandboxes, chosen by an environment check: `RESEARCHER.md` gained a proxy-sandbox path, and `resolve-runtime-issue` gained recovery entries for the new refusals. The token path is unchanged. `BOOTSTRAP.md`, the Project Instructions template, and the skills exported from dotfiles were left for follow-up (tracked in #72).

## Topics Explored

- Which session-start steps survive in the new sandbox, tested step by step
- Why pushes fail with a valid PAT (the proxy answers git's first, unauthenticated request with its own 403, so git never offers the token; REST is blocked even with the token attached)
- Whether the claude.ai "Connectors" GitHub option is new (it is not; what changed is the sandbox behind it)
- The August `github-mcp-migration` records (verification report, design doc, plan 13) and what today changes about them
- Which `gh` commands and REST calls work through the proxy
- Commit attribution in the new sandbox: codename, signing, and the two trailers the sandbox asks for

## Provisional Findings

Verified by running it in this session:

- **Token path, proxy sandbox:** clone, fetch, and private-repo reads over git work. `git push` fails with `access denied by the git proxy: <repo> is not in this session's authorized repository set`. REST calls fail with `GitHub access to this repository is not enabled for this session. Use add_repo to request access.`
- **Three separate preconditions, three separate errors:** not connected → `link your GitHub account`; connected but app not installed → repo attaches, reads work, push refused with `Claude doesn't have GitHub access to <repo>`; repo not approved for the session → the two errors above.
- **After all three:** token-free clone (full history, 338 commits, about 1 second), push via the hook, REST reads on approved repos, issue create and edit.
- **Read-level approval was enough for REST reads** on two private repos (config file contents, issue listing).
- **The proxy replaces the `Authorization` header.** A request with a dummy token returned 200 on an approved repo, so existing recipes that send the PAT header keep working.
- **REST writes need `Content-Type: application/json`**; without it the proxy returns 415.
- **GraphQL is blocked.** `gh issue list`, `gh issue create`, `gh issue edit`, `gh pr list`, `gh label list`, `gh repo view` all fail; `gh api <REST path>` works.
- **Commits show as "Unverified" on GitHub** (`reason: unknown_key`): the sandbox signs with its own key.
- **The search API is refused outright**, even scoped to one approved repo ("sessions are bound to their configured repositories"). `task-triage`'s cross-repo search has no equivalent there; it can only list issues repo by repo for approved repos.
- **Environment markers observed:** `IS_SANDBOX=1` (the template checked for `yes`), `CLAUDECODE=1`, `GITHUB_TOKEN=proxy-injected`, `/mnt/skills/public` present. The old surface check passed only through the `/mnt/skills/public` test.
- **Connecting GitHub mid-chat was picked up by the same chat.** The connection is tied to the Claude account; Dan did the linking from a different browser profile than the one running the chat.

From reading, not run here:

- Anthropic's cloud-environment docs say the proxy rejects branch deletions and tag pushes, and serves only a fixed set of GraphQL operations.
- An issue thread (anthropics/claude-code#76248) reports an Anthropic engineer calling the block on pasted credentials "intended behavior". Read through a page summary, not first-hand.
- Reports from 2026-09-22 to 09-25 describe chat-Project sessions with no add-repository tool at all. This session had one, so it may have shipped since; the rollout state for other users is unknown.

Later in the session, PR creation through the proxy worked (PR #73, opened over REST; view and check-runs calls also returned 200).

Not tested: closing or commenting on an issue; deleting a branch. (Merging a PR was tested at the end of the session; see Pull Request below.)

## Decisions Made

- **Support both sandboxes** until everyone has moved, chosen by an environment check (Dan).
- **Check used:** inside the claude.ai branch, `GITHUB_TOKEN=proxy-injected` means proxy sandbox. Picked because Anthropic documents that placeholder as "the GitHub proxy authenticates for this session".
- **Commit trailers:** keep the `Claude-Session:` link, drop `Co-Authored-By:` (Dan). The model is already in the author slot via the codename, and the codename rule lives in the template, so this rule sits beside it in `RESEARCHER.md`, with `personal_info.md` able to override.
- **`gh` → REST translation lives in `RESEARCHER.md`**, not in the skills. The task skills and `finishing-a-research-branch` are exported from dotfiles and must not be hand-edited here; their surface note already points at `RESEARCHER.md` for sandbox specifics.
- **The agent declined to send the PAT in a way that slips past the proxy.** A pre-authenticated request got through on the push handshake; forcing git to do that was not attempted, because the proxy had explicitly refused the push.
- **Commit signing left as the sandbox sets it**; the "Unverified" badge is documented, not worked around. Still open for Dan (see #72).

## Results

- `d063b6b` — `template/RESEARCHER.md`: surface check, token-free clone, new section on proxy-sandbox GitHub access (setup, per-session approval, REST rules, `gh` → REST table), trailer rule, notes on the `personal_info.md` fetch and the reminder check
- `4b2177c` — `template/skills/resolve-runtime-issue/SKILL.md` and `SKILL_INDEX.md`: four proxy-sandbox recovery entries
- Each new command block in `RESEARCHER.md` was run as written in the proxy sandbox; the surface check was also run with the token-sandbox and CLI conditions simulated.
- A second agent that had not seen the work read the edited files cold and reported 13 findings. Ten were fixed in a follow-up commit: the no-add-repository-tool fallback contradicted the "REST is blocked" finding; the Contents API fallback was offered where it cannot work; the `gh` → REST table was fenced off from token-sandbox agents who need it too; the shallow-clone deepening command would have left line branches unreachable; the label check could miss past 30 labels; `task-triage`'s search had no entry; and four smaller wording gaps. Three were left open (below).

## Open Questions

- **Rollout:** are all template users on the proxy sandbox, or only some? This decides when the token path can be retired.
- ~~PR merge through the proxy is untested.~~ Resolved: PR #73 merged over REST from the proxy sandbox.
- **`BOOTSTRAP.md` and `_PROJECT_INSTRUCTIONS.md.template`** still describe PAT setup only. A change to `BOOTSTRAP.md` also needs the README pin moved.
- **Skills exported from dotfiles** carry sandbox notes that assume the PAT and omit the JSON content type on writes (`finishing-a-research-branch`). The fix belongs in the dotfiles source, then a re-export.
- **`github-mcp-migration`:** the proxy does what the token dispenser (plan 13) was designed to do, without a token entering the chat. If that holds, the branch can be closed out as superseded.
- **Claude GitHub App permissions** were not recorded. The dispenser design limited its app to contents, issues, pull requests and metadata; the Claude app's list is Anthropic's choice.
- **Approval prompts:** with the session's permission setting on "Manual", each web fetch and each repo request stops for a click. Whether another setting persists across chats is unknown.
- **The old PAT** is now unused on the proxy sandbox. It still sits in the instructions of about ten Projects; revoke once none of them run on the token sandbox.
- **Leftover:** branch `sandbox-push-probe-20261007T0753` on origin is a throwaway from the push test. The sandbox reportedly cannot delete branches, so it needs deleting by hand.
- **Old `IS_SANDBOX` value** on the token sandbox could not be re-checked from here; the template's `yes` test was left as it was.
- **Review findings left open:**
  - The surface check tells the proxy sandbox from the CLI only by `/mnt/skills/public`. The proxy sandbox also sets `CLAUDE_CODE_REMOTE=true`, which could serve as a second test, but it is unknown what other cloud surfaces set it, so it was not added.
  - The trailer rule lives in an upstream template file. The sandbox's instruction defers to "the user's own instructions"; a careful agent might not count a fetched template as that and keep `Co-Authored-By`. Putting the preference in `personal_info.md` as well would remove the doubt. Dan chose to wait and measure: #74 checks a week of web-session commits.
  - `_PROJECT_INSTRUCTIONS.md.template` says to stop on "missing values", which is read before `RESEARCHER.md` excuses a missing `TOKEN`. It only matters once someone removes the token from their Project Instructions; fix with the rest of that template.

## Captured Tasks

- [#72: Migrate web workflow to the new sandbox's token-free GitHub access](https://github.com/danparshall/claude_researcher/issues/72) — captured 2026-10-07
- [#74: [2026-10-14] Check whether web-session commits still carry Co-Authored-By](https://github.com/danparshall/claude_researcher/issues/74) — captured 2026-10-07

## Pull Request

- [#73: RESEARCHER.md: support the proxy sandbox (token-free GitHub access) alongside the token sandbox](https://github.com/danparshall/claude_researcher/pull/73) — merged 2026-10-07 on Dan's go-ahead, real merge commit `079c0ab`, done over REST from the proxy sandbox (`PUT …/pulls/73/merge`)
