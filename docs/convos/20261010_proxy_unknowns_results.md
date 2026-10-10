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
