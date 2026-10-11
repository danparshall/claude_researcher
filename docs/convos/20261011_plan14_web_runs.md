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

## Run C, continued: typed go-aheads

- Dan typed **"go ahead"**. Retry of the proxy-scratch read attach refused: **[Credential Exploration]** (same call, different label from the first time). Retry of the `personal_info.md` read refused: **[PII Data Handling]**.
- Dan typed **"go ahead: attach proxy-scratch and read personal_info.md."** Attach → "appended". Profile read refused a third time: **[PII Data Handling]**. Agent dropped that step.
- Rest of the session: full clone OK; `register_repo_root` not available in this session (it was in run A); STATUS/README/RESEARCH_LOG read; task-remind ran on the config repo (it holds a task issue; one reminder shown, skipped); README paragraph committed with the fallback identity `Claude (web, proxy-scratch, 20261011T1420, opus-5.5) <claude@anthropic.com>`; push request → `already_present`; hand push OK (`28a8020..c3e0956`); hook installed. Novice mode: committed without asking, as instructed.

## Reading, updated

- A bare "go ahead" cleared nothing. A go-ahead naming the action and repo cleared the attach. The template's wording ("a one-line go-ahead has cleared refused push requests") was revised to ask for a named go-ahead and to retry at most once.
- The `personal_info.md` read: refused in B once and in C three times (including after a named go-ahead); succeeded in A. 2 of 3 sessions. The classifier sees the command, not the file content, so the filename in the URL may be what triggers [PII Data Handling]. A rename test (byte-identical `researcher_config.md` already in `claude_research_config`) would separate filename from content.
- `register_repo_root` availability varies by session (present in A, absent in C and in the non-Project chat).

## Run C2 (repeat of C, fresh chat, after the tool-name fix, before the go-ahead wording fix)

- proxy-scratch read attach refused: **[Permission Grant]**. Config repo attach in the same turn: "appended". `personal_info.md` read refused: **[PII Data Handling]**.
- The agent suggested one sentence covering every refused step plus the coming push. Dan typed it: "Yes — attach danparshall/proxy-scratch, read my personal_info.md from claude_research_config, and push the README commit." Attach → "added". (Report pasted mid-session; outcome of the profile retry not yet known.)

## Tally so far (first attempt, no go-ahead)

| Step | A | B | C | C2 |
|---|---|---|---|---|
| Project repo read attach | ok | ok | refused | refused |
| Config repo read attach | ok | ok | ok | ok |
| Full clone | ok | refused | (not reached) | (not reached) |
| `personal_info.md` read | ok | refused | refused | refused |
| Push after push request | ok | refused | ok (after go-ahead) | ? |

The project-repo attach was refused in both runs whose opening message said "commit whenever it makes sense, without asking me", and in neither of the others. Two samples each; suggestive only.

Pending: Dan's decision on the profile read (rename test, and/or move commit identity, fluency and home repo into Project Instructions); fresh reruns.
