# Proxy-only Web Template Implementation Plan

**Goal:** Remove the token (PAT) path from the web template so it supports only the proxy sandbox, with read-only repo access at startup and push requested at the first commit, and trim the Project Instructions to match.

**Originating conversation:** [docs/convos/20261010_proxy_only_cutover.md](../convos/20261010_proxy_only_cutover.md)

**Context:** Anthropic has moved every claude.ai web user to the proxy sandbox, where a GitHub proxy holds credentials and each repo must be attached to the session. PR #73 added the proxy path alongside the token path (issue #72). In six test sessions on 2026-10-10, the web sandbox's auto-mode permission classifier refused add-repository requests for push made at startup, whatever the Project Instructions said, while read requests mostly passed and a push requested at the first commit, right after the user asked for it, went through.

**Confidence:** Moderate for the access design (one clean run of read-at-startup / push-at-first-commit; the classifier is not deterministic), high for removing the token path (Dan: the change applies to everyone). Phase 6 exists to firm up the access design before merge.

**Architecture:** Prose-only edits to `template/RESEARCHER.md`, `template/BOOTSTRAP.md`, both Project Instructions templates, `template_lite/LITE.md`, `README.md`, and the web-only skills in this repo; one fix to a dotfiles-sourced skill, carried here by the dotfiles exporter. No new code. The access design is: startup attaches the project repo and `claude_research_config` read-only; the agent asks for push with the add-repository tool at the first commit; the auto-push hook is installed only after the first push succeeds.

**Branch:** `proxy-only` in `danparshall/claude_researcher` (worktree `.worktrees/proxy-only`). The dotfiles fix goes on dotfiles `main`.

**Tech Stack:** Markdown; `git`; GitHub REST through the proxy; dotfiles `export_profile_skills.py`; pytest for the existing test suites in both repos.

---

## Background the implementer needs

- **Two repos.** `claude_researcher` holds the public web template. Skills under `template/skills/` come from two places: most are exported from Dan's dotfiles (`~/code/dotfiles/nori-researcher/skills/`, whitelist in `~/code/dotfiles/export_profile_skills.py`) and must be edited **there**, never here; four are web-only and edited here: `branch-document-review`, `start-research-line`, `report-upstream-issue`, `resolve-runtime-issue` (also `add-deliverable`, `audit-status`, `audit-repo-structure`, `init-code-scaffold`, `iterative-writing-workflow`, `paper-processing-*`). Check `template/skills/.export_manifest.json`: a skill listed there is exported.
- **The exporter commits straight to `claude_researcher` `main`** and refuses to run if the checkout is not a plain clone on `main` with no unpushed non-export commits. Run it from the main checkout, not from this worktree, and only on the Pro (the machine with the export flag).
- **RESEARCHER.md's persona block** (between its persona markers) is written by the exporter from dotfiles. Don't edit inside it.
- **The access rules the template must teach** (from the convo's Evidence table):
  - The auto-mode classifier allows actions it can tie to something the user asked for and refuses ones the agent decided on itself. Text in Project Instructions or in this template does not count as the user asking; a line the user types in chat does.
  - Startup: request **read** for `${USERNAME}/${REPO}` and `${USERNAME}/claude_research_config`. Both requests in one turn.
  - First commit: request **push** for `${USERNAME}/${REPO}`. If the reply is "already attached" or otherwise unclear, try `git push`; the push result is the test. Only after a push succeeds, install the post-commit hook.
  - A refused step: show the user the exact denial text and the step it blocked, and ask. Don't retry in a different form, and don't keep committing when nothing can be pushed (the sandbox is wiped at session end).
  - Issue, PR and label writes (create, comment, retitle, close, merge) only when the user asked for that write in this session. Skills that offer a menu (task-remind's close / snooze / skip) already satisfy this: the user's choice is the request.
  - A read-level attachment permits pushes and REST writes (run 5; plan 15 T4). Don't describe read access as a safety boundary. And don't use it: always request push before the first push, and if that request is refused, ask the user rather than pushing on the read attachment. Pushing because the label happens not to be enforced would route around the classifier's judgment, which is exactly what it exists to catch.

## Phase 1 — RESEARCHER.md

1. **"Three fetch mechanisms" (top of file):** rewrite the config-repo bullet to say the proxy authenticates REST for attached repos, no token. Delete the "Two kinds of web sandbox" block. Add one short paragraph naming the proxy sandbox as the only web sandbox and pointing to §2.0c.
2. **§2.0a surface check:** drop the `GITHUB_TOKEN` branch and the `IS_SANDBOX` test. Use `[ -d /mnt/skills/public ]` for claude.ai, then `CLAUDECODE=1` for Claude Code, then "unknown". Keep the "keep the branch order" note, reduced to: the claude.ai sandbox also sets `CLAUDECODE=1`, so test `/mnt/skills/public` first. Reason to give in one clause: a probe that reads token variables is what the classifier refused as [Auto-Mode Bypass].
3. **§2.0b clone:** delete the token-sandbox recipe, the "leave the PAT out of the URL" paragraph, and the PAT-hygiene bullet. Keep the plain clone, preceded by "after the repo is attached read-only (§2.0c)".
4. **§2.0b auto-push hook:** move the hook install out of session start. New text: install it right after the first successful push (§2.0c "Push at the first commit"). Until then, commits are local; push by hand at the first commit. Keep the script and failure-handling text as is.
5. **§2.0b clone-failure fallback:** remove the token-sandbox sentence.
6. **§2.0c:** retitle "GitHub access". Remove the "on the token sandbox, skip this section" opener. Rewrite **Per-session approval**:
   - Startup: read for the project repo and the config repo, one call each, same turn, before §2.0b. The home repo (if distinct): read, straight after §2b.
   - New subsection **Push at the first commit**, carrying the rules from "Background" above.
   - Update the access table: project repo = read at startup, push at first commit.
   - Delete the "No add-repository tool at all" PAT fallback; replace with: surface it, nothing can reach GitHub, stop.
7. **New subsection in §2.0c, "Permission checks":** the classifier rules from "Background" (tie to user request; show denial and ask; no unrequested external writes; no retrying in another form). Five or six sentences; no list of every block seen.
8. **§2a:** drop `TOKEN` from the env-var block and the sentence about it. Project Instructions carry `USERNAME` and `REPO`.
9. **§2b:** drop the `Authorization` header from the curl recipe and the proxy-sandbox note under it. 404/403 text: drop "the PAT lacks access"; keep the add_repo and App-installation causes.
10. **Sweep:** `grep -n -i -E "token|PAT\b|proxy sandbox"` in the file. Remove every remaining "token sandbox" reference; "proxy sandbox" can become "the sandbox" where the contrast no longer exists. The trailer rule and "Unverified" badge paragraphs stay (drop "(proxy sandbox)" from their headings).

## Phase 2 — Project Instructions templates and LITE

1. **`template/_PROJECT_INSTRUCTIONS.md.template`:** replace with the target text below.
2. **`template_lite/_PROJECT_INSTRUCTIONS_LITE.md.template`:** same treatment: framing paragraph adapted to lite mode, `USER`/`REPO` (keep LITE's variable names), no token. LITE does not clone the template; it clones only the project repo and reads `LITE.md` at its root. Keep that, with the clone made token-free and preceded by "attach the repo read-only with the add-repository tool". Replace its `personal_info.md` curl block with "read it over REST as RESEARCHER.md §2b does, after attaching `claude_research_config` read-only", or inline the header-free curl. Add one line: request push at the first commit, then push.
3. **`template_lite/LITE.md`:** session-start step 1, replace the PAT clone with the attach-then-clone sequence and the push-at-first-commit rule; drop "PAT scope" from the 404 note.

Target text for `template/_PROJECT_INSTRUCTIONS.md.template`:

````markdown
# Project Instructions — claude_researcher

This claude.ai Project uses **claude_researcher** (`github.com/danparshall/claude_researcher`), an open-source workflow I chose so Claude can work as my research collaborator, with memory kept in git: each session reads where the work stands from my repo and commits its progress back.

**One repo per Project.** This Project's repo is `<USERNAME>/<REPO>`. The only other repo a session reads is my config repo, `<USERNAME>/claude_research_config`, which holds `personal_info.md`: the profile I wrote so you know who I am, how I work, and which name and email go on commits.

```bash
USERNAME="<USERNAME>"
REPO="<REPO>"
```

## Session start

1. Clone the runtime spec:

   ```bash
   git clone --depth 1 https://github.com/danparshall/claude_researcher.git /home/claude/.claude_researcher_template
   ```

   If the clone fails, WebFetch `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/RESEARCHER.md` instead and tell me you're in degraded mode.

2. Read `template/RESEARCHER.md` and follow its session-start sequence before touching my repos. It takes precedence over everything here except the two values above.

The record of my work is the repo's `STATUS.md` and `RESEARCH_LOG.md`, not past chats; skip `conversation_search` / `recent_chats` at session start. If anything here looks inconsistent with my setup (wrong username, wrong repo, missing values), stop and say so before doing any work.
````

## Phase 3 — BOOTSTRAP.md and README.md

BOOTSTRAP is the onboarding script for new users; most of its token material is in Steps 2, 6, 7, 8 and the appendix.

1. **Step 2b "Personal Access Token", "Token handling", "About PAT scope", "Why each permission":** replace with the two one-time steps from RESEARCHER.md §2.0c (connect GitHub in claude.ai Settings → Connectors; install the Claude GitHub App with "Only select repositories"). Point at §2.0c for the error each missing step produces rather than duplicating it.
2. **Step 6 "Create the GitHub repos":** it creates repos via the REST API with the PAT's Administration permission. Whether the proxy allows repo creation is plan 15 T2. Until it is tested, rewrite Step 6 to have the user create both repos on github.com (exact settings: private, no template, no README so the seed commit is the first), then add them to the Claude GitHub App installation. Delete the "If you skipped Administration" and "If you skipped Pull requests or Issues" subsections.
3. **Step 7 seeding:** the Contents API recipe still works through the proxy once the repo is attached (writes need `-H "Content-Type: application/json"`). Drop the `Authorization` header; add the content-type header to the recipe; note that bootstrap is a user-requested write, and that attaching with push is needed here. Bootstrap is the one place push is requested at the start, because seeding is the user's stated goal.
4. **Step 8:** Project Instructions text = the Phase 2 target. Delete "PAT scope and lifecycle".
5. **Step 10 egress-revisit reminder POST:** drop the token header, add the content-type header.
6. **Appendix:** remove PAT rows; add one row pointing to RESEARCHER.md §2.0c "Permission checks" for a classifier refusal.
7. **Step 1 egress:** rewrite per plan 15 T3; leave unchanged until those results are in.
8. **Recommend the auto permission mode** (Dan, 2026-10-10). Add a short subsection to the one-time setup in Step 2, worded from plan 15 T6's findings (where the setting lives, whether it persists). Content: auto is the recommended setting; in testing, its refusals fell on actions the agent chose for itself (asking itself for push access, closing issues nobody asked to close), so it catches most overreach without a click per action. It is a net, not a guarantee: it let one unrequested issue edit through. When it refuses something you did want, the agent will show you the refusal; a one-line go-ahead typed in chat ("I authorize push access to <repo>") has cleared it every time so far.
9. **Steps 3 and 6** wait on plan 15 T1 and T2; the Step 6 text below is the fallback if T2 shows sessions can't create repos.
10. **`README.md`:** replace "Create a GitHub fine-grained Personal Access Token" and its screenshot with the connect + install steps; drop "PAT handling" from the confirmation-gates sentence. `template/reference/screenshots/CAPTURED.md`: mark the PAT screenshot retired (don't delete the image; Dan decides).

## Phase 4 — Web-only skills (edit here)

1. **`resolve-runtime-issue`:** delete "PAT expired or insufficient scope". Retitle the four "Proxy sandbox: …" entries without the prefix. Add an entry "Permission check refused a step (auto-mode classifier)": show the denial text, ask the user; for a refused push request, a one-line go-ahead typed by the user in chat has worked. Check "`git clone` fails for the project repo" and "Connection error" for token wording.
2. **`start-research-line`** (lines ~112–116) and **`branch-document-review`** (lines ~51, 56, 117, 154, 188): drop `-H "Authorization: token $TOKEN"`; add `-H "Content-Type: application/json"` to every POST/PATCH/PUT; line 188 "assumes the user's PAT has write access" → "assumes push access to the repo (RESEARCHER.md §2.0c)". Where a skill can use local git instead of REST (#33 covers `branch-document-review`), leave that to #33; this plan only removes the token.
3. **`report-upstream-issue`** line 27: drop "The user's PAT (`TOKEN`)" from the list of things to keep out of issue bodies, or reword to "any credential".
4. **`SKILL_INDEX.md`** `resolve-runtime-issue` entry: drop "expired PAT" from its description.

## Phase 5 — dotfiles-sourced skill

1. In `~/code/dotfiles/nori-researcher/skills/finishing-a-research-branch/SKILL.md` line ~131: replace "using the PAT from Project Instructions" with the REST calls through the proxy (no token header, `Content-Type: application/json` on writes), pointing at RESEARCHER.md §2.0c's `gh` → REST table.
2. In dotfiles, fix the two prose mentions: `nori-researcher/_MAINTENANCE.md` line ~53 ("fetch via the user's PAT" → "fetch through the sandbox's GitHub proxy") and `notes/researcher_profile_maintenance.md` lines ~200, 231, 267 (substrate-mechanics examples).
3. Run the dotfiles tests listed in dotfiles `CLAUDE.md` (at least `tests/test_export_profile_skills.py` and `tests/test_skill_surface_note.py`) with `uvx --python 3.12 pytest`. Commit on dotfiles `main`, push.
4. On the Pro, from the main `claude_researcher` checkout on `main`, run the exporter (`python3 ~/code/dotfiles/export_profile_skills.py`) so the fix lands on `claude_researcher` `main`; then merge `main` into `proxy-only`.

## Phase 6 — Validation on web

No code, so no unit tests. The checks are a grep gate, the existing suites, and real web sessions.

1. **Grep gate.** In this worktree, excluding `docs/`: `grep -rIn -i -E "x-access-token|Authorization: token|\\bPAT\\b|token sandbox|\\$TOKEN" --exclude-dir=.git --exclude-dir=docs .` returns nothing, other than deliberate history (`ATTRIBUTION.md`, `CAPTURED.md` retirement note). Same pattern in dotfiles `nori-researcher/`.
2. **Existing suites:** `uvx --python 3.12 pytest tools/` in this worktree (`test_repin.py`, `test_skill_manifest.py`).
3. **Web runs**, with the template served from this branch. RESEARCHER.md is read from the clone of `main`, so either merge first behind Dan's go-ahead and revert if a run fails, or have the test Project's instructions clone `-b proxy-only`. Prefer the second.
   - **Run A (full template, fluent user):** fresh session; opening task that ends in a commit. Pass = both reads approved at startup with no chat authorization; push requested at the first commit and the push lands; hook installed after; no issue writes the user didn't ask for.
   - **Run B (repeat of A)** in another fresh session, because the classifier is not deterministic.
   - **Run C (novice-style):** a Project whose `personal_info.md` copy has `Git fluency: novice` (or tell the agent to act as one), so commits happen without being asked. Pass = the push request at the first such commit is approved, or a refusal is surfaced with the denial text and the agent stops committing.
   - **Run D (LITE):** one session on a lite-mode Project, same pass criteria as A.
   - **Run E (BOOTSTRAP read-through):** a fresh agent reads the revised BOOTSTRAP cold and reports contradictions with RESEARCHER.md. A live bootstrap needs a fresh GitHub account; that is Dan's call.
   Record each run in the convo with the exact denial text of anything refused.
4. **Close-out:** update issue #72's checklist; record the result in `RESEARCH_LOG.md`; open the PR. Don't merge without Dan's explicit go-ahead.

## Housekeeping (Dan, outside the template)

- Paste the Phase 2 Project Instructions (filled in) into each of Dan's web Projects after merge.
- Delete the test copies `researcher_profile.md` and `researcher_config.md` from `danparshall/claude_research_config`. An agent copying that file was refused by the classifier; deleting may be too, so Dan may need to run it.
- Close the `github-mcp-migration` line (token dispenser, plan 13) as superseded; Dan removes its worktree from his terminal.

---

**Testing Details** No code changes, so no new tests. Behaviour is checked where it happens: web sessions (Phase 6 runs A–D) that exercise startup attachment, the push request at the first commit, hook installation and refusal handling, each judged by what the session did and the exact text of any refusal. The grep gate and the existing manifest and repin suites catch leftovers and broken skill manifests.

**Implementation Details**
- Edit dotfiles-sourced skills in dotfiles, never in `template/skills/`; the exporter overwrites them.
- Don't touch RESEARCHER.md's persona block.
- The exporter commits to `claude_researcher` `main` from the main checkout on the Pro; merge `main` into `proxy-only` afterwards.
- Every proxy REST write needs `-H "Content-Type: application/json"` (415 otherwise).
- GraphQL (`gh issue …`, `gh pr …`) stays blocked; the `gh` → REST table in §2.0c stays.
- Startup requests read only; BOOTSTRAP is the one exception, because seeding is the user's stated goal.
- The hook installs after the first successful push, not at startup.
- Keep `personal_info.md` as the filename.
- Don't describe read access as a safety boundary.

**What could change:**
- If runs A–C show push requests refused even at the first commit, fall back to the agent asking the user for a one-line go-ahead in chat before requesting push (the only thing that worked every time so far), and say so in §2.0c.
- If a read attachment reliably permits push, the push request may become unnecessary; keep it anyway unless Anthropic documents that behaviour.
- If the proxy allows repo creation, BOOTSTRAP Step 6 can go back to agent-created repos.

**Questions**
- Repo creation, attaching a nonexistent repo, network egress, what a read attachment allows, the read-to-push reply, and where the auto mode is set: all go to [plan 15](15_proxy_unknowns_tests.md), which runs before Phase 3.
- Settled 2026-10-10: BOOTSTRAP recommends the auto permission mode (Phase 3 item 8).
- The convo-name handshake and §2e are unaffected, but the `Claude-Session:` trailer rule awaits #74's measurement (2026-10-14).

---
