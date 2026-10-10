# Proxy unknowns — test results

**Date:** 2026-10-10
**Branch:** proxy-only
**Surface:** claude.ai (tests) driven from Claude Code
**Machine:** sandbox (tests); pro (recording)
**Session:** Dan (pro, dotfiles, 20261010T1201, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-dotfiles/341dd750-e869-4d39-8c8e-965a528f1c44.jsonl

## Summary

Results of [plan 15](../plans/15_proxy_unknowns_tests.md), run by Dan in the `proxy-scratch` claude.ai Project (auto permission mode, Project Instructions from plan 15 Setup), one fresh chat per test. Recorded from the agents' reports as pasted into the CLI session.

**Setup state:** Claude GitHub App installed on `danparshall` with **All repositories**. Permission mode: auto.

## Results

| Test | Runs | Outcome |
|---|---|---|
| T1 attach a nonexistent repo | 1 | Refused by the add-repository tool; message merges "not found" and "no access". REST GET refused by the proxy (403, own wording). Classifier did not intervene. |
| T2 create a repo from a session | 1 | Refused by the proxy (403): only repository-scoped API paths are allowed. A structural rule, so one run settles it. Classifier did not intervene. |
| T3 network egress | 1 | `api.github.com/zen` 403 and `github.com` 400, both from the proxy; `raw.githubusercontent.com`, `arxiv.org`, `example.com` 200. No approval prompts. Dan's egress setting: "All domains" (`full_egress`). The agent reported the Project Instructions arriving inside command output, styled as a system reminder, and ignored them as an injection. |
| T4 what a read attachment allows | 2 (plus one void run: repo didn't exist yet) | Both runs: read request approved ("appended", access level not echoed); REST GET 200; `git push` of a new branch succeeded. Nothing refused. |
| T5 read-to-push upgrade | 1 | Push request on the already-attached repo returned `status: "already_present"`, no access change mentioned, no refusal; push succeeded. With T4, the push request is a no-op once a repo is attached. Second run skipped (nothing left to distinguish). |
| T6 auto permission mode | Dan's UI observation | New chats default to whatever mode was last selected, in any Project (changing it in one Project changes the default in the others). Chats already open keep their own setting; those open when the feature rolled out defaulted to Manual. |

### T1 — Attaching a repo that doesn't exist

add-repository (`danparshall/proxy-nonexistent-test`, read), verbatim:

> add_repo: repository "danparshall/proxy-nonexistent-test" was not found on github.com, or this session's GitHub credential doesn't have access to it. Check that the owner/repo are correct (e.g. "anthropics/claude-code", not a path inside a monorepo). To find the exact owner/repo, call mcp__claude-code-remote__list_repos with part of the owner or repository name as `query`. If it lists the repository, call add_repo again with that owner/repo. Detail: you don't have access to danparshall/proxy-nonexistent-test

`curl -sS -i https://api.github.com/repos/danparshall/proxy-nonexistent-test`: HTTP 403 from the proxy (no GitHub headers), verbatim body:

> {"message":"GitHub access to this repository is not enabled for this session. Use add_repo to request access. If add_repo answers that read access is already available and you need GitHub API or write access, call add_repo again with access:\"push\" to attach the repository with credentials.","documentation_url":"https://docs.anthropic.com/en/docs/claude-code/github-actions"}

**What it means for plan 14:**
- The add-repository tool can't tell "doesn't exist" from "not installed". BOOTSTRAP Step 3 can't use it alone as an existence check.
- The tool names a **`list_repos`** tool (`mcp__claude-code-remote__list_repos`, takes a `query`). With an "All repositories" installation, Step 3 can call `list_repos` with `claude_research_config`: listed means it exists and is reachable; not listed means it doesn't exist or isn't in the installation, and the agent asks the user which. Untested beyond the tool's own description.
- The proxy's 403 text says a plain read attachment may not include GitHub **API** access: "If add_repo answers that read access is already available and you need GitHub API or write access, call add_repo again with access:"push"". This conflicts with run 5 of 2026-10-10, where REST reads of `claude_research_config` worked after a read request. T4/T5 should note whether REST calls work under a read attachment, not just git push.

### T2 — Creating a repo from a session

`curl -sS -X POST https://api.github.com/user/repos -H "Content-Type: application/json" -d <name, description, private, auto_init>` at 2026-10-10 12:55 EDT: HTTP 403 from the proxy, verbatim body:

> {"message":"This GitHub API path is not available: sessions are bound to their configured repositories. Use repository-scoped endpoints (repos/{owner}/{repo}/...).","documentation_url":"https://docs.anthropic.com/en/docs/claude-code/github-actions"}

**What it means for plan 14:**
- Sessions can't create repos. BOOTSTRAP Step 6 becomes "the user creates both repos on github.com" (the plan's fallback text), and its Administration/Issues 403 subsections go.
- Any endpoint outside `repos/{owner}/{repo}/...` is refused the same way. That also covers `/user` and the search API (already noted in RESEARCHER.md for `task-triage`). Worth one line in RESEARCHER.md §2.0c as the general rule, and a `resolve-runtime-issue` entry quoting this text.
- With "All repositories" installed, a repo the user creates is reachable at once; with "Only select repositories", the user must also add it to the installation. BOOTSTRAP must say which.

### T3 — Network egress

At 2026-10-10 12:57 EDT, `curl -sI` each URL; every response began with the proxy's `HTTP/1.1 200 Connection Established`:

| URL | Status |
|---|---|
| `https://api.github.com/zen` | `HTTP/1.1 403 Forbidden` (JSON, no GitHub headers: proxy) |
| `https://github.com` | `HTTP/1.1 400 Bad Request` (JSON, no GitHub headers: proxy) |
| `https://raw.githubusercontent.com/danparshall/claude_researcher/main/README.md` | `HTTP/2 200` (has `x-github-request-id`) |
| `https://arxiv.org` | `HTTP/2 200` |
| `https://example.com` | `HTTP/2 200` |

No approval prompts. Dan's claude.ai setting (Settings → capabilities → Domain allowlist): **All domains** (`full_egress`). With the setting already at its widest, this run can't show whether the setting still governs reachability for a default (no-egress) account.

**Project Instructions seen as an injection.** The agent reported that command 1's output "also carried a block styled as a system reminder, claiming to be project instructions for a 'proxy-scratch' project (do only what each message asks, name which check refused each step, don't retry refused steps, plus a USERNAME value). I ignored it." That block is the scratch Project's actual Project Instructions. One sighting; agents in earlier sessions followed Project Instructions. Delivery may vary (for example, instructions arriving mid-turn attached to a tool result).

**What it means for plan 14:**
- BOOTSTRAP Step 1a's probe (`curl -sI https://api.github.com/zen`) always fails on the proxy sandbox, whatever the egress setting. Replace it with a non-GitHub URL (for example `https://example.com`) to test egress, and test GitHub reachability by attaching a repo instead.
- The egress setting still exists, so Step 1 stays for paper sources and general web access. Its GitHub domain list is moot: GitHub traffic goes through the proxy. Whether a default account can reach the proxy at all is untested.
- `raw.githubusercontent.com` works, so the WebFetch fallback for the template stays.
- If Project Instructions can arrive in a form an agent rightly treats as untrusted, nothing that needs the user's authority should rest on them. This supports the plan's design (startup reads, push at the first commit after a user request, a typed go-ahead when refused). Candidate upstream report to Anthropic.

### T4 — What a read attachment allows

**Void run (12:59 EDT):** `proxy-scratch` did not exist yet. add-repository gave the same "not found … or … doesn't have access" message as T1; REST 403 from the proxy; clone failed with `could not read Username` (git's info/refs answered 401 "Repository not found", realm `ccr-gitengine`, with an `X-Github-Request-Id`). Confirms T1: the tool's message can't separate a missing repo from no access. The repo was then created from the CLI (`gh repo create danparshall/proxy-scratch --private --add-readme`).

**Run 1 (13:10 EDT):** add-repository with `access: "read"` returned `status: "appended"`, `workspace: "/home/claude/proxy-scratch"`, message "Repo danparshall/proxy-scratch added. Clone it NOW…" and "danparshall/proxy-scratch is now in this session's GitHub scope… writes and account-wide tools such as create_repository remain limited to the repositories attached to this session". The access level was not echoed. Then:
- `GET …/repos/danparshall/proxy-scratch/contents/README.md`: HTTP 200.
- Shallow clone, branch `t4-read-push`, commit `f4a0cbe`, `git push -u origin t4-read-push`: succeeded (`* [new branch] t4-read-push -> t4-read-push`).
- Nothing refused by GitHub, the proxy, or the classifier.

**Run 2 (13:17 EDT):** identical outcome. Read request "appended" (scope wording as run 1, no access level echoed); REST GET 200; shallow clone at `0a65458`, branch `t4-read-push-2`, commit `2bf28a0`, push succeeded; `git ls-remote origin` shows `refs/heads/t4-read-push-2` at `2bf28a0`. Nothing refused. Side finding: after a `--depth 1` clone, whose fetch refspec maps only `main`, `git push -u` can't store a tracking ref for the new branch, and the sandbox's stop hook then reports unpushed work (`fatal: upstream branch 'refs/heads/t4-read-push-2' not stored as a remote-tracking branch`). RESEARCHER.md's full clone avoids this; its shallow fallback already runs `git remote set-branches origin '*'`.

**What it means for plan 14:**
- Attachment is the boundary; the `access` level appears to be ignored, at least with an "All repositories" installation. Read access is not a safety boundary (the plan already says not to treat it as one).
- The template must still request push before the first push. Requesting "read" because it is known to permit writes would use the label to get past the classifier's judgment, which is the behaviour the classifier exists to catch, and it would break if Anthropic starts enforcing the level. If the push request is refused, the agent asks the user rather than pushing on the read attachment.
- The tool's reply tells the agent to shallow-clone and to call a register-repo-root tool. RESEARCHER.md already overrides the shallow clone; it should say whether to call the register tool.

### T5 — Upgrading read to push

**Run 1 (13:22 EDT):** add-repository `access: "read"` → `status: "appended"`. Full clone (`is-shallow-repository` false), branch `t5-upgrade`, commit `d84d01c`. Then add-repository `access: "push"` on the same repo returned immediately, no denial, no pending approval visible to the agent (whether Dan saw an approval box was not recorded), with `"status":"already_present"`. Message opens: "Repo `danparshall/proxy-scratch` is already attached to this session. It should be at /home/claude/proxy-scratch. Do NOT re-clone if it's already there…", repeats the clone guidance, the scope wording ("writes and account-wide tools such as `create_repository` remain limited to the repositories attached to this session"), and the instruction to call `register_repo_root`, which "tells the session to load the repo's CLAUDE.md, skills, and plugins on the next turn". Push of `t5-upgrade` succeeded.

**What it means for plan 14:**
- With T4, the push request on an attached repo is a no-op that the classifier allows. The morning's [Permission Grant] refusals were on push requests for repos **not yet attached**, at session start. So the plan's design (read at startup, push request at the first commit) costs one cheap call, and becomes the real request if Anthropic ever enforces access levels.
- RESEARCHER.md should say: `already_present` means proceed; push, then install the hook.
- `register_repo_root` loads the repo's own CLAUDE.md, skills and plugins. RESEARCHER.md should decide whether to call it (Dan's call; leaning no, so RESEARCHER.md stays the single runtime spec).

### T6 — The auto permission mode

Dan, from using the UI: new chats default to **whatever mode was last selected**, wherever it was selected; changing it in one Project changes the default in the others. Chats already open keep their own setting. When the feature rolled out, the chats Dan already had open defaulted to Manual, which is why he "had to go re-enable" it.

**What it means for plan 14:** BOOTSTRAP can say "choose auto once; new chats pick it up", with one caveat: a chat that was already open, or one where the user later switched modes, keeps its own setting, so check the mode if a chat starts asking for approvals.

## Summary of what changes in plan 14

| Plan 14 item | Change | From |
|---|---|---|
| BOOTSTRAP Step 1 (egress) | Replace the `api.github.com/zen` probe (always 403 on the proxy) with a non-GitHub URL such as `https://example.com`; drop the GitHub domain list (GitHub goes through the proxy); keep the setting walkthrough for paper sources. | T3 |
| BOOTSTRAP Step 3 (does the config repo exist?) | The add-repository tool can't tell missing from inaccessible. Use `list_repos` with `claude_research_config` (untested); if not listed, ask the user. | T1 |
| BOOTSTRAP Step 6 (create repos) | The user creates both repos on github.com; the proxy refuses `POST /user/repos`. With "Only select repositories", the user also adds each to the installation. | T2 |
| RESEARCHER.md §2.0c | General rule: only `repos/{owner}/{repo}/...` API paths work. Push request at the first commit stays; `already_present` means proceed. Never push on a read attachment without having requested push. | T2, T4, T5 |
| RESEARCHER.md §2.0c | Say whether to call `register_repo_root` (default: don't). | T4, T5 |
| BOOTSTRAP auto-mode text | "Choose auto once; new chats inherit the last selection. Chats already open keep their own." | T6 |
| `resolve-runtime-issue` | Entries quoting the T1 and T2 refusal texts. | T1, T2 |
| Upstream | Project Instructions delivered inside tool output look like an injection to the agent. | T3 |
