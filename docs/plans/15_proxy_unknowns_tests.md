# Proxy Sandbox Unknowns Test Plan

**Goal:** Settle the open questions plan 14 depends on (repo creation, attaching a repo that doesn't exist yet, network egress, what a read attachment allows, the read-to-push upgrade, and the auto permission mode) with a short series of claude.ai web sessions.

**Originating conversation:** [docs/convos/20261010_proxy_only_cutover.md](../convos/20261010_proxy_only_cutover.md)

**Context:** Plan 14 moves the web template to the proxy sandbox only. Its startup and push design rests on six test runs; its BOOTSTRAP rewrite rests on behaviour nobody has tested on the proxy sandbox: whether a session can create repos, what happens when it attaches a repo that doesn't exist, and whether the old network-egress step still applies. These tests run before plan 14 Phase 3 (BOOTSTRAP), and their results feed it directly.

**Confidence:** Exploratory. Each test asks a factual question about Anthropic's sandbox; any answer is useful. The classifier is not deterministic, so a single refusal or approval is weak evidence where a test involves it; tests that touch it say how many repeats to run.

**Architecture:** Dan drives each test in a fresh claude.ai web chat inside a dedicated scratch Project, pasting the prompt given here and pasting the agent's report back to a CLI session, which records results in the convo. A throwaway repo, `danparshall/proxy-scratch`, takes all writes. No template files change until the results are in.

**Branch:** `proxy-only` (results recorded in `docs/convos/`; plan 14 updated from them).

**Tech Stack:** claude.ai web chat (proxy sandbox, auto permission mode unless a test says otherwise); GitHub REST; git.

---

## Setup (Dan, once)

1. **Scratch Project** on claude.ai named `proxy-scratch`, with these Project Instructions, so no claude_researcher startup runs and the agent only does what each message asks:

   ```markdown
   # Project Instructions — proxy sandbox tests

   This Project is for testing how the claude.ai sandbox handles GitHub access. It does not use the claude_researcher workflow: don't clone the template, read RESEARCHER.md, or run any startup sequence.

   Do only what each message asks. For every step, report what you ran, the outcome, and the exact text of any refusal or error, including which check refused it (GitHub, the GitHub proxy, or the auto-mode permission classifier). Don't retry a refused step in a different form, and don't print file contents unless asked.

   USERNAME="danparshall"
   ```

2. **Permission mode:** auto, for every test except T6's check.
3. **Claude GitHub App installation:** note whether it is set to "All repositories" or "Only select repositories", and which repos are selected. Several results depend on it.
4. **Don't create `proxy-scratch` yet.** T2 tries to create it from a session; if that fails, Dan creates it on github.com (private, no README), then adds it to the App installation.

Record for every test: date/time, model, the permission mode, the agent's report verbatim (at least every refusal text), and the App installation scope at the time.

## T1 — Attaching a repo that doesn't exist

**Feeds:** BOOTSTRAP Step 3 (checks whether `claude_research_config` exists; on the proxy sandbox an unattached repo can't be queried, so the check has to go through the add-repository tool).

**Prompt (fresh chat):**

> I'm testing the GitHub proxy. Use the add-repository tool to request read access to `danparshall/proxy-nonexistent-test`, a repo that does not exist. Then try `GET https://api.github.com/repos/danparshall/proxy-nonexistent-test`. Report each reply verbatim.

**Outcomes to distinguish:** a clear "not found" from the tool (Step 3 can use it as the existence check); a generic refusal indistinguishable from "not installed" (Step 3 must ask the user instead); a classifier refusal (repeat once in a new chat).

## T2 — Creating a repo from a session

**Feeds:** BOOTSTRAP Step 6 (currently creates repos with `POST /user/repos`).

**Prompt (fresh chat):**

> I want you to create a private GitHub repo for me named `danparshall/proxy-scratch`, description "proxy sandbox tests", initialized with a README. Use `POST https://api.github.com/user/repos` with `-H "Content-Type: application/json"`. Report the HTTP status and response message verbatim. If it is created, then try to attach it with the add-repository tool (push access) and report that reply too.

**Outcomes:**
- **201 Created:** Step 6 can keep agent-created repos. Then note whether the attach worked. With "Only select repositories", a brand-new repo is outside the installation, so expect it to fail until Dan adds it. If so, Step 6 must tell the user to add each new repo to the installation.
- **403 or similar from the proxy:** Step 6 becomes "user creates repos on github.com". Record the message for `resolve-runtime-issue`.
- **Classifier refusal:** repeat once. If still refused, try once more after Dan types in chat "I authorize creating this repo." Record whether that clears it.

**Afterwards:** if the session couldn't create it, Dan creates `proxy-scratch` on github.com (private, with README) and adds it to the App installation, ready for T4 and T5.

## T3 — Network egress

**Feeds:** BOOTSTRAP Step 1 (egress probe and settings walkthrough).

**Prompt (fresh chat, no repos attached):**

> Network test, nothing else. Run each of these and report the status line or error verbatim:
> 1. `curl -sI https://api.github.com/zen`
> 2. `curl -sI https://github.com`
> 3. `curl -sI https://raw.githubusercontent.com/danparshall/claude_researcher/main/README.md`
> 4. `curl -sI https://arxiv.org`
> 5. `curl -sI https://example.com`
> Also report whether any of these produced an approval prompt instead of running.

**And Dan, in the claude.ai UI:** does `https://claude.ai/settings/capabilities` still show a network-egress setting, and what is it set to?

**Outcomes:**
- GitHub hosts reachable and non-GitHub hosts governed by the setting: Step 1 stays, but only matters for paper sources. Its GitHub domain list can go.
- Everything reachable whatever the setting: Step 1 can shrink to a note.
- `api.github.com/zen` refused without an attached repo: the 1a probe is no longer a valid check and needs replacing.

## T4 — What a read attachment allows

**Feeds:** plan 14's "don't treat read access as a boundary" rule and the push-at-first-commit step.

**Prompt (fresh chat):**

> Use the add-repository tool to request **read** access to `danparshall/proxy-scratch`, and report the reply. Then clone it, create a branch `t4-read-push`, add a file `t4.txt` containing the current UTC time, commit, and `git push -u origin t4-read-push`. Don't request push access. I'm asking for this push as a test of what read access permits. Report the push output verbatim.

**Outcomes:** push lands (a read attachment permits push; consistent with run 5); push refused by the proxy (read is enforced; run 5's push went through for another reason); classifier refusal (record, and note it's the action, not the access, being judged). Run twice, in separate chats.

## T5 — Upgrading read to push

**Feeds:** plan 14's push-at-first-commit wording ("already attached" handling).

**Prompt (fresh chat):**

> Use the add-repository tool to request **read** access to `danparshall/proxy-scratch`; report the reply. Then clone it, create a branch `t5-upgrade`, commit a file `t5.txt` with the current UTC time, and before pushing, request **push** access to the same repo with the add-repository tool. I want this commit pushed. Report the second reply verbatim, then push and report the output.

**Outcomes:** the second reply's exact wording (does it say "already attached", report an upgrade, or show an approval box?); whether the push lands. Run twice. If T4 showed read permits push, T5's push result says nothing new; the reply text is the point.

## T6 — The auto permission mode

**Feeds:** BOOTSTRAP's recommendation of auto mode.

**Dan, in the UI (no prompt needed):**
1. Where is the permission mode set: per chat, per Project, or per account? What are the options called?
2. Set auto in one chat, open a new chat in the same Project, and in a different Project. Is it still auto?
3. Optional: run T4's prompt once in a non-auto mode and note what the user sees (one approval box per repo? per action?), so BOOTSTRAP can describe the alternative accurately.

## Results and follow-through

1. Record each test in a new convo `docs/convos/<date>_proxy_unknowns_results.md`: a results table (test, runs, outcome, verbatim refusal texts), then what each result means for plan 14.
2. Update plan 14: Phase 3 Step 1, Step 3 and Step 6 per T1–T3; Phase 1's push-at-first-commit wording per T4–T5; the BOOTSTRAP auto-mode text per T6. Remove the answered items from its Questions.
3. Add `resolve-runtime-issue` entries for any new refusal texts.
4. Cleanup (Dan): delete `proxy-scratch` from github.com when plan 14 Phase 6 no longer needs it, and remove it from the App installation. The proxy rejects branch and repo deletion from the sandbox.

---

**Testing Details** This plan is itself the test: each item asks one factual question of the live sandbox, with a fixed prompt, a fresh chat, and stated outcomes to tell apart. Tests involving the classifier run at least twice.

**Implementation Details**
- Fresh chat per test, so no earlier in-chat authorization or attachment carries over.
- All writes go to `proxy-scratch` on branches, never to a real repo.
- Every REST write sends `Content-Type: application/json`.
- The scratch Project's instructions disable the claude_researcher startup, so its classifier noise doesn't mix into the results.
- Record verbatim refusal texts; paraphrases cost us a round-trip on 2026-10-10.
- T2 runs before T4/T5 because it may create the scratch repo.

**What could change:** If T4 shows read attachments permit push, plan 14 may simplify further, but should still request push before pushing until Anthropic documents the behaviour. If T2 shows creation works but new repos fall outside a select-repos installation, BOOTSTRAP may recommend "All repositories" or add an "add it to the installation" step; that is Dan's call.

**Questions**
- Is "All repositories" an acceptable recommendation for new users, given it widens what a session can request? Dan's call after T2.
- Should T4 and T5 also run on a novice-style setup? Probably not; access behaviour shouldn't depend on the user's profile.

---
