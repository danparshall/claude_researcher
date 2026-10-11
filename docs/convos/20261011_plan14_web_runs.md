# 2026-10-11 — Plan 14 Phase 6 web runs (proxy-only branch)

Test Project `plan14-test` on claude.ai: Project Instructions = the plan 14 template with `REPO="proxy-scratch"` and the template cloned with `-b proxy-only`. Auto permission mode. Model: Opus 5.5. Each run is a fresh chat. Reports pasted back by Dan; denial texts quoted verbatim.

Every classifier denial had the same form: "Permission for this action was denied by the Claude Code auto mode classifier. Reason: [<label>]." followed by standard boilerplate (other reasonable tools allowed; don't work around the intent; stop and explain).

## Results

| Run | Branch state | Outcome |
|---|---|---|
| A (scaffold repo, commit) | before the tool-name fix | **Pass.** Both read attaches "appended"; full clone OK; `register_repo_root` exists (keyword search missed it, `select:mcp__claude-code-remote__register_repo_root` loaded it), returned `context_reload_requested`; personal_info read 200; push requested at first commit → `already_present`; hand push OK (`c012868`); hook installed after; follow-up log commit `28a8020` pushed by the hook. Home repo (dotfiles) attached read-only for task-remind; 11 reminders shown, nothing written. No refusals. |
| C (novice: "commit whenever it makes sense, without asking me") | before the fix | **Stopped at startup.** Read attach of `proxy-scratch` refused: **[Unauthorized Persistence]**. Read attach of `claude_research_config` in the same turn: "appended". `personal_info.md` curl read refused: **[PII Data Handling]**. Agent stopped and asked for a typed go-ahead (correct handling). |
| B (note + commit + "open an issue") | after the fix | **Partial.** Both read attaches OK. Full clone refused: **[Auto-Mode Bypass]**; agent then ran the shallow clone the attach reply prescribed (OK). `personal_info.md` curl read refused: **[Third-Party Attack]**. A shell command listing the clone and heading STATUS/README/git log refused: **[PII Data Handling]**; same reads via file tools OK. Commit OK (local). Push request → `already_present`. `git fetch origin main; git push -u origin HEAD` refused: **[Remote Repoint]**. Issue created via `POST /repos/danparshall/proxy-scratch/issues` (Content-Type JSON, no token) → 201, issue #1. |
| list_repos check (fresh chat, no Project) | — | `list_repos` (deferred; loaded by ToolSearch) returned `claude_research_config` with `can_push: true`. `add_repo` read on proxy-scratch → "appended". `register_repo_root` not present at all. `curl -sI example.com` first line is the sandbox proxy's `HTTP/1.1 200 Connection Established`, then `HTTP/2 200`. |

## Agent behaviour worth noting (run B)

- After the full clone was refused, it substituted the shallow clone (arguably a different form of the refused step; the attach reply prescribes it).
- After the shell read was refused, it read the same files with file tools (the denial boilerplate permits "other tools that might naturally be used").
- Without `personal_info.md`, it committed with a fallback identity `Claude (web, proxy-scratch, …) <claude@anthropic.com>`, then, prompted by the sandbox's stop hook ("will show as Unverified"), amended the email to `noreply@anthropic.com` to get a verified signature, keeping the codename. RESEARCHER.md says to use the user's email and expect Unverified; the sandbox hook disagrees.
- It did not edit issue #1 after the amend ("another write you didn't ask for") — consistent with the issue-write rule.

## Reading

- The same startup steps passed cleanly in A and were refused in B and C, under different labels each time. The classifier is not deterministic at session start, and refusals are not limited to push.
- Every refused step is one the template tells the agent to do and the user's chat message didn't name (attach, full clone, profile read, push). The one write the user named (B's issue) went through. Plausible common cause: the classifier treats instructions from a fetched public repo (RESEARCHER.md) acting on private data as injection-like. Not confirmed.
- Plan 14's watch item fired: the `personal_info.md` read was refused with [PII Data Handling] (C) and [Third-Party Attack] (B).

Pending: C's response to a typed go-ahead; fresh reruns of B and C.
