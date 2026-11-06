# Plan 18 — Refused session-start steps: prompt the user once, don't leave it to memory

Branch (suggested): `session-start-refusals`. Follows Plan 17 (profile rename) and its "Watch" request.

## Why

Dan put the session-start steps in Project Instructions so he would not have to remember them. In auto permission mode the sandbox's classifier refuses actions it can't tie to something the user typed in this chat; instructions text doesn't count (RESEARCHER.md §2.0c, "Permission checks"). So some session-start steps will be refused, and the template can't change that.

What the template can control is what happens next. Today it lets the agent note the refusal and carry on, and §2b tells it **not** to ask for a go-ahead on the config read. The result: the user finds out mid-session, and only if they notice. Dan's requirement (2026-11-03): **he should never have to remember to ask.** At most, the agent prompts him once, with a line he can paste.

## Evidence (web session `Dan (web, verification, 20261102T1656, opus-5.5)`)

| When (UTC) | Step | Outcome | Exact text |
|---|---|---|---|
| 2026-11-02 16:15 | First Bash call (`date` + template clone) | Not run; repeat ran | "Bash did not run. The server-side auto mode classifier gave no verdict because it was not shown this call … Repeat the identical Bash call once now" |
| 2026-11-02 16:16 | `add_repo` `danparshall/verification`, read | Attached | `"status":"appended"` |
| 2026-11-02 16:16 | `add_repo` `danparshall/claude_research_config`, read, **same turn, in parallel with the call above** | **Refused** | "Permission for this action was denied by the Claude Code auto mode classifier. Reason: The server-side auto mode classifier judged this action dangerous (it gave no explanation)." |
| 2026-11-02 ~16:40 | Running Rahman's simulator from an external clone (`python3 -I -c 'import evasion_calculator'`) | Refused | "[Code from External]" |
| 2026-11-03 11:32 | Retry of the same config `add_repo`, after Dan wrote in chat that not loading the repo the instructions specify was unreasonable (not a templated go-ahead) | **Attached** | `"status":"appended"` |
| 2026-11-03 11:32 | §2b read of `researcher_config.md` (curl, `Accept: application/vnd.github.raw`, not the base64 recipe) | **Read** | — |

The agent's own miss: it told Dan once, mid-reply, that the config attach was refused, and carried on. It showed no denial text and no paste-able go-ahead, though §2.0c asks for both. §2b's "don't ask for one" made skipping easier.

This contradicts §2b's current note ("a typed go-ahead didn't clear it, so don't retry it or ask for one"). That note was about the **read**, after Plan 17's tests; this refusal was the **attach**. One session is one data point, not a rate.

## Changes

1. **RESEARCHER.md §2e: a "Blocked at start" line, mandatory.** If any session-start step was refused (an attach, the §2b read, the home-repo attach), the first reply carries, directly under the fixed `Session:` line:
   - the step and the exact denial text (one line each, trimmed);
   - **one sentence the user can paste** that names every refused action and repo, e.g. "Yes, attach danparshall/claude_research_config read-only and read researcher_config.md."

   Make it a checklist item in §2e, not a sentence in §2.0c, so it can't be skipped when the user's first message is a substantive task. Answer the user's message in the same reply; don't block on the paste.

2. **§2b and §2.0c "Permission checks": drop "don't ask" for the config read.** Replace with: offer the paste line (change 1), retry each refused step once after it, and record the outcome (change 6). Keep the honest history: reads have been refused even after a named go-ahead (Plan 17's tests); an attach cleared after a chat request on 2026-11-03.

3. **After the paste, retry and confirm in one line.** Retry each refused step once, in the same form; never a different tool or recipe. Then report the outcome in one line ("Config read: ok" or the new denial text). If it is still refused, carry on with the Project Instructions copies as today and don't ask again that session.

4. **Low-confidence experiment: attach the config repo in its own call, before the project repo, not in parallel.** In the evidence above, the parallel pair split (project ok, config refused). Untested whether order or parallelism matters. Log it; drop it if 5 sessions show no difference.

5. **HUMANS.md and LITE.md.** HUMANS.md: tell users, in two sentences, that under auto mode Project Instructions can't authorize steps with outside effects, so a session may ask them to paste one line, and why. LITE.md "Refused steps": the same paste-line pattern in condensed form. Also check whether claude.ai sessions expose a permission setting other than auto, which would turn refusals into one-click approvals. If one exists, document it in HUMANS.md. **Unverified; check before writing it.**

6. **Record outcomes (Plan 17 "Watch").** Add the evidence table above to `RESEARCH_LOG.md`. For the next 5 web sessions, record attach outcome, read outcome, whether the first reply carried the paste line, and whether the retry cleared it.

## Out of scope

Changing the classifier, and any workaround that runs a refused step in another form.

## Acceptance

Over the next 5 web sessions: every session-start refusal shows up in the first reply with denial text and a paste line (5/5), and the attach/read/retry outcomes are logged. Then revisit change 4, and §2b's wording on read refusals.

## Files

`template/RESEARCHER.md` (§2.0c "Permission checks", §2b, §2e), `template_lite/LITE.md` ("Refused steps"), `HUMANS.md`, `RESEARCH_LOG.md`, this plan as `docs/plans/18_session_start_refusals.md`.

## Implementation status

Built 2026-11-06 on branch `session-start-refusals` (changes 1-5; change 6 is this section). Change 5's question, whether claude.ai sessions offer a permission setting other than auto, is **not checked**: it needs a web session. HUMANS.md says nothing about it.

**Amended 2026-11-06 (Dan):** a session-start refusal now **stops** the first reply instead of being answered alongside it. The reply is the fixed line plus a capitalized "⚠️ SESSION START BLOCKED" announcement and the paste line, nothing else; the agent answers the first message after the retry. Reason: agents write long first replies, and a refusal mentioned partway through is easy to miss. This replaces change 1's "don't block on the paste".

## Watch log (5 web sessions)

The evidence table above is the baseline. One row per web session after the build:

| Date | Codename | Attach outcomes | Config read | First reply stopped with the SESSION START BLOCKED announcement? | Retry after paste cleared it? | Notes |
| --- | --- | --- | --- | --- | --- | --- |
