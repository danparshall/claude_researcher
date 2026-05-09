# claude_researcher — Phase 4: CLAUDE.md + SKILL_INDEX stub

**Date:** 2026-05-09 (same day as Phase 3 production)
**Repo:** claude_researcher
**Plan:** [docs/plans/01_initial_build.md](../plans/01_initial_build.md) — Phase 4 (tasks 19–26) + Phase 6 task 43 (SKILL_INDEX stub) + Phase 4.5 (new v1.1 stub authored this session)

## Summary

Wrote the production `template/CLAUDE.md` for Phase 4 — the runtime spine every research session loads. 7 numbered sections (calibration, session-start fetch, branch resolution, project confusion, runtime workflow, wrap-up, issue reporting) plus appendix and a known-v1-limitations section. Brainstorming surfaced one architecture pivot during execution: **the PAT and curl recipes belong in the Project's Custom Instructions field, not in an uploaded `_PROJECT_INSTRUCTIONS.md` file** — the consequence flowed through to BOOTSTRAP.md (Step 10 collapsed onto a single Custom Instructions paste; the file-upload subsection deleted; Step 11 cause list updated) and to the canonical CLAUDE.md (which now treats Custom Instructions as the authoritative credential location). Also wrote a `SKILL_INDEX.md` manifest stub so CLAUDE.md's session-start fetch sequence has a real target while per-skill SKILL.md files wait for Phase 6, and authored a new Phase 4.5 plan section spec'ing collaborator mode for v1.1 (direct-collaborator on private repo, narrower than fork-based or org-based alternatives).

The session followed Phase 3's pattern: brainstorm-first (3 question rounds plus a real-time scope correction), then ship the MVP. Dan's "let's do MVP and see what feedback we get" mid-session signal locked in solo-only v1 with collaborator support cleanly deferred.

## Work Done

- **Brainstorming convo (3 question rounds):**
  - Round 1: branch model — Model A (git branches per research line) is default; Model B (main_only) is an opt-in for solo repos. Field lives in research repo's STATUS.md as a top-of-file `workflow_mode` value (default `branches` if absent).
  - Round 2: section order (Order B — calibration first) and calibration style (centralized + inline tier reminders).
  - Round 3: PAT placement (Custom Instructions, not file). This turned into a real architecture pivot.
  - Real-time scope correction: Dan flagged that the grad-student/professor model breaks the OWNER==USERNAME assumption. Discussed three collaborator paths (direct-collaborator vs fork vs GitHub org) and settled on direct-collaborator for v1.1 with the other two as later options.
- **Phase 4 production (`681ed9d`):**
  - `template/CLAUDE.md` — ~330 lines. Calibration-first ordering. `(novice: explain X; fluent: just do it)` inline reminders at branch creation, file delete, archive, PR merge, and force-op gates. Forward-compat hedge in §6 step 2: 405/422 from PR-merge stops the flow gracefully, so collaborator mode is a small additive change in v1.1 rather than a rewrite. Known v1 limitations explicitly listed: no collaborator mode, no atomic commits, no auto branch protection, skills pinned to `main`.
  - `template/skills/SKILL_INDEX.md` — manifest stub. URLs 404 until Phase 6 ports each skill, but the contract (name + trigger + URL, grouped by lifecycle role) is locked. Listed: 3 lifecycle, 3 knowledge-management, 9 working-style; plus 7 explicitly-not-ported with rationale.
  - `template/BOOTSTRAP.md` Step 10 collapsed onto Custom Instructions paste — file-upload subsection deleted, "don't upload as file" call-out added, verification affordance switched to "spot-check no literal placeholders remain".
  - `template/BOOTSTRAP.md` Step 11 cause list updated — removed "file not uploaded" cause and the "Phase 4 hasn't shipped" cause; added "CLAUDE.md upstream URL unreachable" with CDN propagation note.
  - `template/_PROJECT_INSTRUCTIONS.md.template` — URL fix: `/main/CLAUDE.md` → `/main/template/CLAUDE.md` to match BOOTSTRAP.md and the still-unsettled Phase 10 publish strategy.
  - `docs/plans/01_initial_build.md` — task 26 wording updated to reflect the architecture pivot; new Phase 4.5 section appended spec'ing v1.1 collaborator mode (6 sub-tasks: OWNER/USERNAME split, BOOTSTRAP joining-vs-creating branch, branch protection in seed_repo.py, role field in personal_info.md, wrap-up flow split, PAT scope guidance for collaborators).

## Decisions Made

- **CLAUDE.md is calibration-first.** Section §1 reads `git_fluency` (fetched in §2) and sets the verbosity dial before everything else. Inline tier reminders at sensitive boundaries (branch creation, archive, merge, force) act as cheap insurance against drift in long sessions.
- **Novice tier is explicitly pedagogical with promotion path.** Translates every git concept inline ("a branch is like a separate workspace…"), checkpoints under the hood without asking, and after several comfortable sessions can suggest the user update their `git_fluency` to `occasional`. Designed for the professor + grad student model where a new student is novice and the agent slowly upskills them.
- **Workflow modes: `branches` (default) vs `main_only` (opt-in).** Each research line is a git branch by default; solo repos that don't want PRs can flip to `main_only`. The mode is a top-of-file field in the research repo's STATUS.md. Wrap-up §6 has different paths per mode.
- **PAT in Custom Instructions, not file.** Custom Instructions are in every chat's context from the very first message — the agent has credentials and recipes before any fetch happens. Strictly better than file-upload for an authentication-bearing payload. The canonical Custom Instructions text is `_PROJECT_INSTRUCTIONS.md.template` with TOKEN/USERNAME/REPO substituted; the bootstrap WebFetches it, substitutes, and instructs the user to paste.
- **§6 wrap-up handles protected `main` gracefully (forward-compat for v1.1 collaborator mode).** Step 2 of the merge flow distinguishes 200 (proceed) from 405/422 (branch protection, surface PR URL and stop). Solo case = self-merge. Collaborator case = open-and-stop. The directory move to `docs/historical/` is a separate session for the owner. This means v1.1 collaborator mode is additive (split OWNER/USERNAME, add joining-vs-creating bootstrap branch, add branch protection in seed_repo.py) rather than rewriting CLAUDE.md.
- **v1.1 collaborator path is direct-collaborator, not fork or org.** Direct-collaborator (professor adds student as collaborator on their personal repo) keeps a single source of truth (one STATUS.md, one `docs/active/`), works with fine-grained PATs scoped to a repo the user doesn't own, and matches the "shared lab notebook" mental model. Forking is heavier (each fork drifts; cross-fork PRs); GitHub orgs are cleaner at scale (defer to v2.0).
- **`personal_info.md` schema for upskilling: just track current `git_fluency` tier.** Agent observes user comfort and suggests promotion at appropriate moments; user accepts manually. No target field, no session counter — YAGNI for v1.

## Bugs / Friction Surfaced

- **`_PROJECT_INSTRUCTIONS.md.template` had wrong CLAUDE.md URL** (`/main/CLAUDE.md` instead of `/main/template/CLAUDE.md`). Fixed in this session's commit. Caught by the "verify URL consistency across files" pre-draft scan.
- **STATUS.md "Phase 3 caveats" subsection is now stale** — the caveats (Step 10 placeholder, Step 11 cause #5) are resolved by Phase 4 shipping. Should be removed in this session's STATUS.md update.
- **Nori `commit-author.js` hook still mangles commit messages** with literal `\n\n` instead of newlines. Persistent across all today's commits. Cosmetic only. Upstream issue still un-filed; tracked across multiple repos.

## Open Questions (carry-forward)

- **Phase 5 vs Phase 6 ordering.** Phase 5 = Python helper scripts in `template/scripts/` (`rest_helpers.py`, `create_repo.py`, `seed_repo.py`, `extract_pdf_text.py`). Phase 6 = port each upstream Nori SKILL.md and adapt to REST. The two phases interleave: skills call the helpers, but skills also stand on their own as documents. Likely sensible to do Phase 5 first (so skills have helpers to call) but worth confirming when next session opens.
- **Real-world test of CLAUDE.md.** Phase 3's lesson was that incognito claude.ai chats validate orchestration patterns surprisingly well, and that "treat as if I typed" framing backfires. Phase 4's CLAUDE.md needs a similar smoke test before Phase 5/6 build on top of it. Likely a ~30-minute session: open a fresh claude.ai chat in a Project, paste the canonical Custom Instructions text (with real PAT/USERNAME/REPO), and see whether the agent fetches CLAUDE.md, follows the §2 sequence, and greets the user correctly. Surfaced behaviors will inform any §1 / §2 fixes.
- **Collaborator mode v1.1 timing.** Phase 4.5 spec is committed but not scheduled. The natural trigger is when Dan's first real collaborator (a grad student or professor) needs the workflow. Until then, v1 ships with the limitation documented and collaborators wait. Not a v1 blocker.
- **Phase 10 publish strategy still undecided.** URLs throughout BOOTSTRAP.md, CLAUDE.md, SKILL_INDEX.md, and `_PROJECT_INSTRUCTIONS.md.template` use `.../main/template/<file>` paths. Phase 10 picks between flipping dev repo as-is, restructuring (`template/` → root + dev files into `_dev/`), or separate public repo. Punt continues.
- **Skill SHA pinning vs. `main`.** SKILL_INDEX.md URLs point at `main`. If a skill ships a breaking change, in-flight Project files keep their CLAUDE.md fetch from `main` and could break. YAGNI for v1; revisit when first real bug surfaces.

## What's Next

**Phase 5 — helper scripts (`template/scripts/`)** is the natural next phase. Then Phase 6 — port and adapt skills. Phase 5 first means skills have working helpers to call; Phase 6 first means skill bodies are written and helpers slot in later. Slight preference for Phase 5 first, but worth confirming.

**Real-world test of CLAUDE.md** is a smaller pre-Phase-5 session — paste the Custom Instructions into a fresh claude.ai Project and watch the runtime agent's first session unfold. Same shape as Phase 3's incognito-chat smoke tests. Likely surfaces small fixes to §1 / §2 / §3 before the heavier Phase 5/6 work builds on top.

---

## Update — Smoke-Test Findings and Iterations (same-day, 2026-05-09 evening)

After the initial Phase 4 commit (`681ed9d`) and finish-convo (`39de6c1`), an end-to-end smoke test ran against incognito claude.ai chats. Two test runs surfaced multiple empirical findings that drove substantial restructuring of `BOOTSTRAP.md`. Final commit of the day: `42648a4`.

### Empirical findings (load-bearing)

1. **Egress changes do NOT propagate to already-open chats.** This was the load-bearing unknown going into the test. Confirmed in the second test run: agent's `curl -sI https://api.github.com/zen` failed with `403 host_not_allowed` even after the user had configured the allow list, until they restarted in a fresh chat. The "fresh-session fallback" therefore needs to be the default expected handling, not an edge-case escape hatch.

2. **Domain Allow List UI doesn't accept bulk paste.** The original wording assumed claude.ai's allow-list field accepted newline- or comma-separated values. It does not — domains are entered one at a time, each followed by a per-domain "Add" button which commits immediately. There's no separate "Save" button. The pre-test instruction "paste these domains, one per line" was fundamentally wrong about the UI shape.

3. **Egress restriction is on Anthropic's server-side VM, NOT on the user's machine.** The pre-test framing said things like "If your machine's policies allow it" — implying that locked-down work-machine populations might not be permitted to enable broad egress. That's wrong. The egress restriction is on the bash sandbox where the agent's tool runs (Anthropic-side); the user's local machine network policy is independent and irrelevant to this choice. The trade-off between "All" and "Package Managers Only + specific domains" is purely defense-in-depth on Anthropic's VM, not user-machine-permission-driven. Drove the VM-mental-model rewrite, which the test agent then internalized cleanly.

4. **"Package Managers Only" preset enables on-the-fly `pip install`** for skills like `add-paper` (which will need `pypdf`) and any custom `requests` work in Phase 5/6. Should be the recommended preset by default. Adopted.

5. **claude.ai's user-level memory ("Things to know about you") is auto-loaded into the agent's context at chat start** — there's no separate "fetch" step needed. The pre-test Step 3 ("Read user preferences if available") was a step-shaped concept for something that's already free in agent context. Deleted.

6. **PAT lifecycle was not documented.** The setup PAT is broadly scoped ("All repositories") because it has to create repos that don't yet exist. After bootstrap, the user has options (keep broad / rotate to narrow / per-project). The first commit didn't address this; the test agent in run 2 had to reason through what was acceptable for ephemeral-scratch token handling. Drove Step 2b's token-handling rewrite and Step 8's PAT-lifecycle subsection.

### Restructure shipped in response

The bootstrap evolved from 13 steps (0–12) to 11 steps (0–10), with cleaner conceptual hierarchy: **meta → user → project**.

| Final step | What | Level |
|---|---|---|
| 0 | Open with user, plan recap, CONFIRMATION GATE | meta |
| 1 | Egress probe + walkthrough + fresh-chat hand-off | meta |
| 2 | GitHub readiness (username + PAT) | user |
| 3 | `basic_config` existence check | user |
| 4 | Interview (first-time only — gated on Step 3) | user |
| 5 | Topic + repo name | project |
| 6 | Create repos | project |
| 7 | Seed files | project |
| 8 | Project setup (Custom Instructions paste, PAT lifecycle discussion) | project |
| 9 | Validation | meta |
| 10 | Done | meta |

Two key reorderings during the evolution:

- **Egress moves to Step 1** (before mode check, before everything). Otherwise the bootstrap wastes user-input cycles on questions whose answers get lost when the fresh-chat restart kicks in.
- **Interview moves before Topic** (was after, in initial Phase 4 design). The interview captures persistent user-level prefs (`basic_config`); topic is project-specific. User-level info comes first ("let's set up your prefs, then we can make a repo for your project"). Aligns with the principle "user-level checks first, then project-level checks, getting more granular over time."

Two structural deletions:

- **Mode check folded into Interview Batch 3** (`claude.ai-only | also-local`). It's a user-level preference like `git_fluency` and `paper_naming`, so it belongs in `personal_info.md`, not as a standalone step before the user is even identified.
- **"Read user preferences" deleted entirely.** claude.ai memory auto-loads; no step needed. The interview's prose mentions using whatever's visible as a pre-fill source for first-time users.

### Other refinements during this iteration cycle

- **Paper-naming convention upgraded.** Default is now `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf` (was `{year}_{first_author}_{slug}`). Both first and last authors carry information for ML/CS papers where the senior PI is conventionally last. Plus a common-surname disambiguation rule: use `SurnameF` (surname + first-name initial, no separator) for Anglo (Smith, Jones, Patel, Singh) and East Asian (Wang, Li, Chen, Zhang, Liu, Kim, Park, Choi, Tanaka, Suzuki, Sato) surnames. Applies independently to first-author and last-author. Captured as canonical text in `personal_info.md`'s `Paper naming format` field.
- **PAT scope and lifecycle subsection added to Step 8.** Three options for ongoing use: keep the broad PAT, rotate to narrow per-project PAT, or new PAT per project going forward. Purely informational; user decides their hardening posture later. v1 runs identically under any.
- **Token-handling rules clarified in Step 2b.** "Don't write to any file" was over-strict. New wording explicitly permits ephemeral-scratch (`/home/claude/.bootstrap_env` with `chmod 600`, removed at Step 8) — the rule is about user-visible / repo-committed surfaces, not the agent's VM scratch.
- **`personal_info.md.template` schema** gained a `Mode` field (`claude.ai-only | also-local`) in Operating preferences.
- **CLAUDE.md §2b session-start fetch** updated to read the new `Mode` field and use it for verbosity calibration about claude.ai-specific quirks.
- **Phase 4.5 v1.1 collaborator-mode plan stub** added during the initial Phase 4 commit (681ed9d); remains the documented path for direct-collaborator support.

### Smoke-test agent observations (worth carrying forward as design validation)

The test agent's behavior was largely excellent and worth noting as evidence the orchestration patterns are working:

- **Pre-Step-0 meta-summary.** Before starting Step 0, the agent wrote its own "here's what I read in BOOTSTRAP.md, here's where I'll add my own checks" recap. Emergent behavior, not required by the doc; a sign that "if anything feels off, surface it" framing is generating the right reflexes.
- **Prompt-injection scrutiny resolved correctly.** The agent recognized "fetch and follow external instructions" as a potential injection signature, then traced the safety case (explicit user direction, public files, user-controlled operations, scoped API token vs. password) and proceeded confidently. The contrast with credit-card-pasted-in-chat as a different category was the agent's own reasoning, not in the doc.
- **VM mental model internalized after the rewrite.** After the framing change to "I have a virtual machine that Anthropic spins up for this chat...", the agent paraphrased it back to the user verbatim with their own framing in run 2. The metaphor lands.
- **Token handling under ambiguity.** The agent paused at the "don't write to any file" rule, reasoned through what counts as "a file", proposed both alternatives (ephemeral scratch + inline) to the user, and asked rather than deciding silently. Drove the Step 2b clarification.

### Commits chronology (initial + 8 iterations)

| SHA | Description |
|---|---|
| `681ed9d` | Phase 4 initial: CLAUDE.md + SKILL_INDEX.md stub; BOOTSTRAP.md Step 10 collapsed onto Custom Instructions; v1.1 collaborator-mode plan |
| `39de6c1` | finish-convo: Phase 4 done — convo + STATUS update |
| `e8f7abf` | Swap BOOTSTRAP Steps 5/6; add fresh-session fallback; www. prefix note |
| `c644479` | Correct fresh-session fallback — PAT must be re-pasted in new chat |
| `59c9b27` | Restructure with egress-first flow; fix UI mechanics; correct VM mental model |
| `21fbf06` | Update default paper_naming to `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf` |
| `c2d770b` | Add common-surname disambiguation rule (SurnameF) |
| `7c60902` | Swap egress and mode-check ordering — egress runs first |
| `4009766` | Restructure to user-then-project ordering; fold mode-check into interview; drop user-prefs check |
| `42648a4` | Clarify PAT lifecycle and ephemeral-scratch token handling |

### Open questions still standing

- **Bootstrap end-to-end has not been tested past Step 2b yet.** The most recent smoke test stopped at the agent's "env-file or inline?" question (which is now resolved by the doc). Steps 3–10 (existence check, interview, topic+repo, create, seed, Project setup, validation, done) are still untested with the latest doc. Next session picks up from there.
- **Phase 5 vs 6 ordering** still undecided. Carry-forward from initial Phase 4 finish-convo. Slight preference for Phase 5 (helper scripts) first.
- **Phase 10 publish strategy** still undecided. URLs throughout `BOOTSTRAP.md` / `CLAUDE.md` / `SKILL_INDEX.md` still use `.../main/template/<file>` paths.
- **Skill SHA pinning vs. `main`** still YAGNI for v1.

### What's Next (revised)

**Resume the smoke test from Step 3 onward** in a fresh session, using the latest cache-busted URL (`?v=42648a4`). Token handling is now explicitly documented; the previous pause point shouldn't recur. Walk through repo creation, file seeding, Project setup, and validation — each is a new failure surface that hasn't been exercised end-to-end.

After the bootstrap is end-to-end clean, **Phase 5 (helper scripts in `template/scripts/`)** is the natural next phase, then Phase 6 (skill ports). Slight preference for Phase 5 first so skills have working helpers to call.

### Update 2 — Three more fixes after the handoff was started (commit `a238635`)

Smoke test resumed past Step 2b and surfaced three more issues, all fixed before final handoff:

1. **Administration permission was missing on the PAT.** GitHub's PAT-creation UI defaults all permissions to "No access"; users click through Step 2b without setting Administration to Read and write, then hit 403 on `POST /user/repos` in Step 6. Step 2b now has a `⚠️` warning callout calling Administration "THE MOST-SKIPPED PERMISSION" and an explicit confirmation prompt before proceeding.

2. **403 recovery was over-aggressive.** The doc said "re-create the PAT" — but fine-grained PATs are editable in place; the token value stays the same. Added an "If you skipped Administration" subsection to Step 6 with the exact edit-recipe (Settings → PAT → set Administration → Update). The smoke-test agent figured this out on its own; we just captured it as canonical guidance.

3. **First-repo UX was project-only.** Step 5 assumed the user has a specific research project in mind. New users who just want to start using the workflow now have a knowledge-base path: Step 5 split into 5a (ask which) / 5b (research-`<topic>`) / 5c (`knowledge_base`). Same seed structure either way; `knowledge_base` is just untyped accumulation space until ideas crystallize.

Final commit of the day: `a238635`. Bootstrap end-to-end has now been smoke-tested through Step 6's repo creation (with the 403-then-fix path exercised). Steps 7–10 (seeding, Project setup, validation) still untested.
