# claude_researcher v1 Implementation Plan

**Goal:** Build `claude_researcher`, a fork-downstream of the Nori researcher Skillset adapted for the claude.ai web UI, so non-CLI-savvy collaborators on locked-down work machines can use the research-first workflow with browser-only setup.

**Originating conversation:** [docs/convos/20260508_claude_ai_researcher_design.md](../convos/20260508_claude_ai_researcher_design.md)

**Context:** Dan's Nori researcher profile only works in Claude Code on a developer's local machine. Collaborators (scientists, professors, economists) often work on locked-down employer machines where they cannot install Claude Code. The design conversation established that claude.ai's Project + GitHub PAT + REST API pattern (already used by Dan via `_PROJECT_INSTRUCTIONS.md`) is sufficient infrastructure to host the researcher workflow on the web UI, provided skills that shell out to `git` are adapted to the GitHub Contents API and the whole setup is wrapped in a self-onboarding bootstrap.

**Confidence:** Exploratory–medium. The architecture is settled (Option α: centralized upstream-fetched skills, dual-repo collaborator setup). Specific friction points — claude.ai custom-instructions length limits, fine-grained PAT scopes for cross-org issues, pypdf availability in the sandbox — are open questions that may force small revisions during implementation.

**Architecture:** This dev repo (`~/code/claude_researcher`) contains `template/` (eventual public content) and `docs/` (research process). When `template/` is sufficiently complete and tested, its contents are pushed to a public `github.com/danparshall/claude_researcher` repo, which collaborators read from at bootstrap time and at runtime (via `raw.githubusercontent.com`). Each collaborator ends up with a `<USERNAME>/basic_config` repo (lifetime personal config) and one `<USERNAME>/research-<topic>` repo per research project, plus one claude.ai Project per research repo.

**Branch:** main (this is a new repo; no branches yet).

**Tech Stack:** Markdown for everything human-facing. Python 3.12 for `scripts/` (run in claude.ai's sandbox via Bash). GitHub REST API (Contents endpoint primarily; Git Data API for the v2 atomic-commit helper). No build step, no package manager, no test framework — this is a content-and-prose repo.

**Status (as of 2026-05-09 evening):** Phases 1–4 complete; Phase 4 smoke-tested end-to-end with Step 9 validation passing in a fresh claude.ai chat. Phase 4.5 (collaborator mode) deferred to v1.1. Phase 4.6 (CLAUDE.md retrofit from AITaxBID audit) and Phase 6 expansions for AITaxBID-sourced skill ports added to this plan during the same session that ran the smoke test. See [`STATUS.md`](../../STATUS.md) for current state and the [`docs/convos/`](../convos/) directory for session records, especially:

- [`20260508_phase1_phase2_initial_build.md`](../convos/20260508_phase1_phase2_initial_build.md) — Phase 1+2 work and the `git_fluency`-tiered commit-policy decision
- [`20260509_phase3_bootstrap_design.md`](../convos/20260509_phase3_bootstrap_design.md) — Phase 3 work and three architectural findings (two fetch mechanisms; "treat as typed" backfires; confirmation gates scripted, not invented)
- [`20260509_phase4_runtime_and_skill_index.md`](../convos/20260509_phase4_runtime_and_skill_index.md) — Phase 4 production CLAUDE.md and the Custom-Instructions architecture pivot
- [`20260509_aitaxbid_skills_audit.md`](../convos/20260509_aitaxbid_skills_audit.md) — survey of Andrea Lopez-Luzuriaga's AITaxBID skills kit; sourced Phase 4.6 and Phase 6 expansion tasks
- [`20260509_phase6_skill_port_planning.md`](../convos/20260509_phase6_skill_port_planning.md) — translation of the audit into concrete plan tasks

**Architectural decisions taken during execution that affect later phases:**

- **Two fetch mechanisms.** WebFetch (claude.ai built-in) reaches public upstream content verbatim with no allow-list configuration; sandbox bash-curl with PAT handles the user's private repos and requires `api.github.com` in user-Settings allow list. CLAUDE.md (Phase 4) and skill ports (Phase 6) should choose the right mechanism per call.
- **Settings is user-wide** (not per-Project) for the Domain Allow List. The `basic_config/domain_allowlist.txt` is a record / portability artifact, not a per-Project paste target.
- **Confirmation gates scripted into orchestration files**, not delegated to agent judgment. CLAUDE.md (Phase 4) should script confirmations at sensitive-action boundaries (merges, archive moves, etc.) rather than expect the agent to invent them.
- **Verification affordances offered, not demanded**, following the kill-convo design pattern. Availability of verification builds trust without requiring use.

---

## Testing Plan

This is primarily a content/prose project, not a software project. The unit-test-first discipline doesn't apply directly. The relevant tests are:

1. **Recruit-and-walkthrough.** Identify a tame collaborator (smart, non-CLI-savvy, has GitHub Pro, has Claude Pro). Walk them through bootstrap end-to-end without intervening. Capture every friction point — missed clicks, ambiguous instructions, broken steps, things that didn't behave as documented. Iterate `BOOTSTRAP.md`, `reference/`, and skills until they get through cleanly.
2. **Self-walkthrough.** Dan does the bootstrap as a "fresh user" before the collaborator test, to catch obvious bugs.
3. **Skill smoke tests.** For each REST-adapted skill, run it once in a real claude.ai chat against a real test repo. Confirm: writes land in the right place with the right content; reads return what the skill expects; error paths (missing file, wrong sha, expired PAT) produce useful messages.
4. **Sandbox dependencies.** Verify the Python packages each script needs (`requests`, `pypdf`, etc.) are available in claude.ai's sandbox or installable via `pip install` at runtime.

Surprising-result thresholds: any step in `BOOTSTRAP.md` that the test collaborator can't complete in <2 minutes is a documentation defect. Any skill that produces a 4xx/5xx from GitHub's API more than once per session is an adapter defect.

NOTE: Because this is a content-first project rather than a code project, I will NOT write code-level tests before content. I will treat the test-collaborator walkthrough as the canonical acceptance test.

---

## Phase 1: Get the dev repo on GitHub

1. Create the GitHub remote and push the current state (initial commit with design convo + plan). Decide visibility (default: private until `template/` is ready to ship; flip to public when Phase 10 publishes). Add the remote with `gh repo create danparshall/claude_researcher --source=. --remote=origin --private --push`. Confirm the design docs are visible on github.com.

## Phase 2: Populate the `template/` skeleton

2. Write `template/README.md`. Top of file: human-readable explanation of what this repo is + the copy-pasteable bootstrap prompt the collaborator pastes into claude.ai (the prompt points Claude at `BOOTSTRAP.md`). Include the rendered prompt in a code block so it's clearly copyable.
3. Copy `LICENSE` (Apache 2.0) and `LICENSE-ADDENDUM.txt` (Ship of Theseus v0.1) verbatim from Nori upstream into `template/`. Both files already exist at the dev repo root and just need to be duplicated into `template/`. The addendum's terms require both files in any derivative work — keep both filenames matching upstream exactly so the link is unambiguous.
4. Write `template/ATTRIBUTION.md` documenting the Nori → Dan → collaborator chain. Include explicit copyright line (`Copyright 2026 Dan Parshall, downstream of Nori (tilework-tech/nori-skillsets) under Apache 2.0 + Ship of Theseus addendum`). This is where attribution lives, since LICENSE itself stays verbatim.
5. Write `template/_PROJECT_INSTRUCTIONS.md.template` with `<TOKEN>`, `<USERNAME>`, `<REPO>` placeholders + a plain-language "Why this uses the GitHub API" section pointing to Settings > Capabilities > Allow Network Egress > Domain Allow List.
6. Write `template/templates/domain_allowlist.txt` with baseline domains: `api.github.com`, `raw.githubusercontent.com`, `github.com`, `codeload.github.com`, `arxiv.org`, `www.biorxiv.org`, `www.medrxiv.org`, `doi.org`. One domain per line, sorted, with comment lines marking workflow-required vs paper-source domains.
7. Create empty directories with `.gitkeep` files: `template/skills/`, `template/scripts/`, `template/reference/`. (Subdirectories created when files are added.)
8. Commit: `Phase 2: skeleton — top-level files, license, attribution, allowlist baseline`.

## Phase 3: Write `BOOTSTRAP.md`

The bootstrap doc is the orchestration script the agent follows during the one-time setup chat. Each numbered step below corresponds to a section in `BOOTSTRAP.md`.

9. Write the skeleton: title, audience (a Claude session reading this), section headers for each step.
10. Write the mode-check section. Single question: "Will you only use claude.ai, or also work locally on a non-locked machine?" Branch on answer.
11. Write the GitHub readiness section. Sub-flows for: (a) no GitHub account → walk them through creating one, (b) account but no PAT → hand them `reference/PAT_SETUP.md`, wait for paste-back.
12. Write the project-topic + repo-name section. Suggest-with-Enter pattern: agent proposes `research-<slug>` from the topic.
13. Write the interview section. Fields: name, current role, academic history, work history, programming languages/tools, general research areas, interaction style notes, **git_fluency tier** (3-tier multiple choice: fluent/occasional/novice), **mode** (`claude.ai-only` or `also-local` — replaces the standalone Step-2 mode-check from earlier drafts; folded into Batch 3 since it's a user-level preference), **paper_naming format** (template with placeholder explanation, default `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf`).
14. Write the basic_config existence-check branch. If `<USERNAME>/basic_config` already exists, skip the interview and re-use the existing personal_info.md + domain_allowlist.txt; only create the research repo. If not, run the full interview and create both repos.
15. Write the sandbox-scripts orchestration section. Sequence: `create_repo.py` (basic_config if needed) → `seed_repo.py` (basic_config initial files) → `create_repo.py` (research repo) → `seed_repo.py` (research repo initial files).
16. Write the claude.ai Project setup walkthrough. Steps: New Project → name → paste custom instructions (provided as a code block) → upload `_PROJECT_INSTRUCTIONS.md` (provided as a code block). The Domain Allow List is a separate user-wide step (`Settings → Capabilities → Allow Network Egress → Domain Allow List`, paste from `<USERNAME>/basic_config/domain_allowlist.txt`) that happens earlier in bootstrap as a one-time configuration, not as part of per-Project setup. See `docs/convos/20260509_phase3_bootstrap_design.md` for the architecture rationale.
17. Write the validation section. "Open a new chat in your Project and say 'hi'. The agent should greet you by name and reference your background."
18. Commit: `Phase 3: BOOTSTRAP.md — orchestration for one-time setup chat`.

## Phase 4: Write `CLAUDE.md`

The runtime instructions every working session loads.

19. Write the skeleton: session-start sequence, branch resolution, runtime workflow, end-of-session, issue reporting.
20. Write the session-start fetch sequence: read `_PROJECT_INSTRUCTIONS.md`, fetch `basic_config/personal_info.md`, fetch `basic_config/domain_allowlist.txt` (for awareness, not action), fetch `STATUS.md` and `README.md` from the research repo.
21. Write the branch-resolution logic: (a) direct name match against STATUS.md inventory, (b) indirect-via-path match for `docs/active/<X>/...`, (c) if neither, list open research lines and ask the wrap-up question.
22. Write the project-confusion handling section: when user names a repo that doesn't match `_PROJECT_INSTRUCTIONS.md`'s REPO, state mismatch and steer to switch Projects.
23. Write the wrap-up / merge-to-main path: open PR via REST → merge → `git mv docs/active/<branch> docs/historical/<branch>` → update STATUS.md "Archived Research Lines" table.
24. Write the git-fluency calibration section: read `git_fluency` from personal_info.md, calibrate terminology and verbosity (novice → "research line" not "branch", explain merges as "finalizing into the permanent record"; fluent → terse). **Also calibrate commit policy by tier:** novice → checkpoint often + under the hood (write each save without asking); occasional → light narration + confirm before structural changes (archives, merges); fluent → terse, ask only when truly destructive. Rationale captured in [`docs/convos/20260508_phase1_phase2_initial_build.md`](../convos/20260508_phase1_phase2_initial_build.md) Decisions Made section.
25. Write the issue-reporting section: when user reports a problem, compose pre-filled URL `https://github.com/danparshall/claude_researcher/issues/new?title=<X>&body=<Y>`, include git_fluency tier and CLAUDE.md SHA, never include PAT or personal_info contents beyond the tier.
26. **Glue + commit.** Replace `template/BOOTSTRAP.md` Step 10's placeholder code block with the canonical custom-instructions text. **Architecture pivot during execution:** the canonical text is the contents of `_PROJECT_INSTRUCTIONS.md.template` itself (with TOKEN/USERNAME/REPO substituted) — pasted into the Project's **Custom Instructions** field, NOT uploaded as a file. The "upload `_PROJECT_INSTRUCTIONS.md`" subsection in Step 10 is therefore deleted; Step 11's troubleshooting cause list is updated to match. Rationale: Custom Instructions are in every chat's context from the very first message, so the agent has credentials + recipes before any fetch happens — strictly better than file-upload for an authentication-bearing payload. Captured in [`docs/convos/20260509_phase4_runtime_and_skill_index.md`](../convos/20260509_phase4_runtime_and_skill_index.md). Commit: `Phase 4: CLAUDE.md + SKILL_INDEX.md stub; BOOTSTRAP.md Step 10 collapsed onto Custom Instructions`.

## Phase 4.5 — Collaborator mode (deferred to v1.1)

`claude_researcher` v1 ships solo-only: it assumes the acting user owns the research repo (`OWNER == USERNAME`). Real research labs typically have a professor + grad student model where the professor owns the repo and students contribute. v1.1 adds direct-collaborator support without the heavier fork-based or org-based alternatives.

**Tracking ticket:** opened during this session; surface as upstream issue when ready to schedule.

**Required changes:**

26.5.1. **OWNER/USERNAME split in `_PROJECT_INSTRUCTIONS.md.template`.** Add `OWNER` env var (defaults to `USERNAME` for solo case). Update read/write recipes to use `$OWNER/$REPO` instead of `$USERNAME/$REPO`. Keep `USERNAME` for `basic_config` location and committer name.

26.5.2. **Bootstrap interview branch.** Add Step 4.5: "Are you starting a new research project, or joining an existing one as a collaborator?" If joining, ask for the owner's username and repo name; verify access via REST (GET on the repo); skip Step 8's repo creation; capture OWNER as separate field.

26.5.3. **Branch protection on `main` for collaborative repos.** Phase 5's `seed_repo.py` adds a `--collaborative` flag. When set, after seeding, calls `PUT /repos/{owner}/{repo}/branches/main/protection` (or the newer Rulesets API) to require review before merge.

26.5.4. **`Role: owner | collaborator` field in `personal_info.md` schema.** New field, set during bootstrap interview. CLAUDE.md uses it to choose between owner-mode wrap-up (PR-and-self-merge) and collaborator-mode wrap-up (PR-only-stop).

26.5.5. **Wrap-up flow split.** CLAUDE.md §6 already handles the merge-blocked case gracefully; v1.1 just makes the collaborator path a first-class flow rather than a fallback. The directory move (`docs/active/<X>/` → `docs/historical/<X>/`) lives on the owner's plate, triggered when the owner next sees the merged PR in their session.

26.5.6. **PAT scope guidance for collaborators.** PAT_SETUP.md (Phase 7 reference doc) gets a section for grad students: how to scope a fine-grained PAT to a repo you don't own (under "Repository access" → "Selected repositories", you can pick repos you've been added to as a collaborator).

**Out of scope for v1.1:** GitHub Organizations as repo owners (defer to v2.0); fork-based workflow (defer indefinitely — direct-collaborator is lighter and matches the lab mental model better).

**Acceptance:** a grad student bootstraps from a fresh claude.ai account, gets added as a collaborator on the professor's repo, completes a research line that the professor merges via the GitHub UI, and the next session by either party correctly archives the line.

## Phase 4.6 — `template/CLAUDE.md` retrofit from AITaxBID audit

The Phase 4 production CLAUDE.md (committed `681ed9d`, restructured through `42648a4`) was written before the AITaxBID skills audit landed (PR #1, merged `6397c33`). The audit identified five Tier B/C patterns worth promoting from per-step practice to universal rules in CLAUDE.md. Each is currently *partially* covered (lives as per-confirmation-gate or per-step practice); the retrofit makes each one a universal rule. Source: [`docs/convos/20260509_aitaxbid_skills_audit.md`](../convos/20260509_aitaxbid_skills_audit.md) and the synthesis convo [`docs/convos/20260509_phase6_skill_port_planning.md`](../convos/20260509_phase6_skill_port_planning.md).

26.6.1. **Tracker-not-past-chats discipline.** Add to `template/CLAUDE.md` as new §1.5 (or top of §2). Verbatim source from Andrea's `writing_skill.md`: *"Do NOT search past chats or conversations. The tracker is the single source of truth for where we left off."* claude.ai-specific because past chats are temptingly available but unreliable. Promote to a top-of-file rule: "Resumption mechanism is STATUS.md + RESEARCH_LOG.md, NOT past chats. If a user references 'last time we said X,' verify against the trackers; do not trust chat memory."

26.6.2. **3+-repetition codification rule.** Add to `template/CLAUDE.md` as a new working-conventions block under §5. Verbatim source from Andrea's `CLAUDE_TEMPLATE.md`: *"If the user asks for the same type of task 3+ times, check whether it should be codified as a rule in this file."* Sharp threshold avoids both premature and too-late codification.

26.6.3. **Parking Lot section.** Add as new §8 (or Appendix) in `template/CLAUDE.md`. Source: Andrea's `CLAUDE_TEMPLATE.md` ships a "Parking Lot (To Be Defined)" section for undecided items; items move out as decided. Currently the runtime CLAUDE.md tracks open questions only via the plan file and convos — adding a Parking Lot to CLAUDE.md gives the runtime instruction set its own home for self-tracked open questions (e.g., the `raw.githubusercontent.com` allow-list finding from the smoke test).

26.6.4. **"Do not infer — ask" universalized.** Add to the new working-conventions block under §5. Existing §3c (no-match branch resolution) and §4 (project-confusion handling) are specific applications. Source: *"A confident output based on wrong assumptions is worse than a quick clarifying question."* Promote to a universal rule.

26.6.5. **Show-before-committing universalized.** Add to the new working-conventions block under §5. Existing CLAUDE.md scripts gates at sensitive boundaries (§3 branch creation, §5 destructive deletes, §6 archive/merge); audit recommends promoting to a universal rule applied to *all* writes. Add: "Before any write to the user's repos, briefly state what you're about to write and why. The user can interject before the commit lands." Reframes per-gate confirmations as the default rather than exceptions.

26.6.6. **Per-skill `Generic skill: ... project-specific implementation` block format (DEFERRED).** Andrea's CLAUDE_TEMPLATE.md uses this format, which is a *per-user-repo* artifact. claude_researcher doesn't currently ship a per-user-repo `CLAUDE.md` template; whether to is a separate design question that depends on whether Phase 6 ports demonstrate (or fail to demonstrate) the need. Tracked in plan-level Open Questions; not in this retrofit.

26.6.7. **Commit:** `Phase 4.6: CLAUDE.md retrofit — universalize tracker discipline, codification, parking lot, do-not-infer, show-before-committing`.

**What could change during retrofit:**

- The exact section numbering (new §1.5 vs. §5 working-conventions block vs. new §8 Parking Lot) is approximate. The author of the retrofit picks the cleanest placement; only the *rules themselves* are load-bearing.
- If §5's "Runtime workflow" gets too dense with the new working-conventions block, consider promoting working conventions to its own §5.5 or making §6 reference them rather than inlining.

## Phase 5: Write helper scripts in `template/scripts/`

27. Write `rest_helpers.py` with: `read_file(repo, path, ref=None)`, `list_dir(repo, path, ref=None)`, `write_new(repo, path, content, message)`, `write_update(repo, path, content, message)` (handles sha lookup), `delete_file(repo, path, message)`. All use the Contents API. Type hints, docstrings, sensible error handling on 404/403/422.
28. Write `create_repo.py`: `POST /user/repos` with sensible defaults (private, no auto-init since we'll seed manually). Takes name + description from CLI args.
29. Write `seed_repo.py` for `basic_config`: pushes `personal_info.md` (from interview), `domain_allowlist.txt` (from baseline + any extras), `README.md`, `.gitignore` (excludes `_PROJECT_INSTRUCTIONS.md`).
30. Write `seed_repo.py` for research repo: pushes `STATUS.md` (with the standard sections), `RESEARCH_LOG.md` (empty), `README.md`, `.gitignore` (excludes `_PROJECT_INSTRUCTIONS.md`), placeholder `papers/.gitkeep`, `papers/text/.gitkeep`, `docs/active/.gitkeep`, `docs/historical/.gitkeep`. Decide: one script with a `--type basic_config|research` flag, or two separate scripts. Prefer one script with flag (DRY).
31. Write `extract_pdf_text.py`: pypdf wrapper, reads a PDF, writes `.txt` to specified path. Used by add-paper.
32. Add a TODO note at the top of `rest_helpers.py` for the v2 `commit_files()` atomic-commit helper using the Git Data API. Don't implement; document the API call sequence as a comment.
33. Commit: `Phase 5: helper scripts — REST wrappers, repo creation, seeding, PDF extraction`.

## Phase 6: Adapt and carry over skills

For each skill, copy from `~/.claude/skills/<skill>/SKILL.md` into `template/skills/<skill>/SKILL.md`, then adapt as noted. Adaptation = replace git-CLI calls with calls to `scripts/rest_helpers.py`. Keep the `<required>` checklist structure that the Nori skill format requires.

34. Port `finish-convo`. Replace `git add` / `git commit` / `git push` with sequential `write_update()` calls (or `write_new()` for first-time files). Note: produces 3 commits per session-end on Contents API; flag in skill body that this is acceptable v1 behavior.
35. Port `update-docs`. Same as finish-convo but no separate "commit and push" step (every write is a commit on REST).
36. Port `add-paper` — **download mode**. PDF download via curl in sandbox → `extract_pdf_text.py` → write PDF as base64 via `write_new()` → write extracted text → `write_update()` PAPER_INDEX.md and PAPER_SUMMARIES.md. Read `paper_naming` format from `personal_info.md` to decide filename. **Fold in AITaxBID's Step 0 academic-vs-institutional triage and Protocol B institutional summary structure** ([`docs/convos/20260509_aitaxbid_skills_audit.md`](../convos/20260509_aitaxbid_skills_audit.md), Tier A finding). Three structural questions decide A vs B: abstract vs executive summary; research question vs no; new estimates vs no. Two-or-more "yes" → Protocol A (academic — Nori's existing flow with light tweaks); two-or-more "no" → Protocol B (institutional — different summary structure: commissioning context / document type / frameworks-and-databases / headline synthesized findings / policy framework / country case studies / position; BibTeX `@techreport`/`@book`/`@inbook` with double-braced institutional author). **Naming reconciliation:** keep Dan's `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf` for Protocol A; document Andrea's `institution_shortTitle_year.pdf` (e.g., `imf_g20RevenueAdmin_2025`) as the Protocol B convention. Both stored in `personal_info.md` as `paper_naming.academic_format` + `paper_naming.institutional_format`. **"Summary evolution principle"** ports verbatim: the (a)–(d) structure is a floor not a ceiling; let summaries grow over time, never trim back to minimal format.
37. Port `add-paper` — **orphan ingestion mode**. New flow: list `papers/` → diff against PAPER_INDEX.md → for each orphan, propose rename per `paper_naming` format → confirm with user → rename via Contents API (write_new at new path + delete_file at old path) → extract → index.
38. Port `init-research-repo`. Replaces local `git init` + `mkdir` with `create_repo.py` + `seed_repo.py`. Used during bootstrap; not typically called at runtime.
39. Port `audit-docs`. Read-only — straight `read_file` and `list_dir` calls. Same checks as the local version (orphaned files, missing links, unindexed convos).
40. Port `audit-papers`. Read-only — same as audit-docs but for papers/. Add: detect orphan PDFs and offer to hand them to add-paper's orphan-ingestion mode.

### Phase 6 — AITaxBID-sourced skill ports (tasks 40a–40c)

These skills come from Andrea Lopez-Luzuriaga's kit at `/Users/dan/code/AITaxBID/skills/`, not from upstream Nori. Port order matches the AITaxBID audit's recommendation (lowest-friction first; sandbox-tooling unknowns surface progressively). Source: [`docs/convos/20260509_aitaxbid_skills_audit.md`](../convos/20260509_aitaxbid_skills_audit.md).

40a. **Port `writing-skill`** to `template/skills/writing-skill/SKILL.md`. Source: `~/code/AITaxBID/skills/writing_skill.md` (169 lines). Two-protocol structure (Protocol 1: Reading/Thinking/Note-Taking — fully interactive, user-driven pace; Protocol 2: Drafting — plan interactively, draft in one pass, revise in chunks; drafting unit is the subsection). Adaptation = strip Andrea-specific examples (any FMM-specific phrasing), normalize frontmatter to Nori's `name:` + `description:` style (`name: writing-skill`), drop the bash-is-fine-for-trivial-things contamination from her CLAUDE.md if it's referenced. Andrea's "Setting up for a new project" tail section becomes the per-user parameter list (source material format, notes structure, tracker, deliverable format, style profiles, version control, subsection sizing, lookup order) — these are parameters the user defines in their research repo's STATUS.md or a future per-user-repo CLAUDE.md. **No REST adaptation needed** — this is a working-style skill with no git/file calls. Estimated effort: ~1 hour, mostly trimming.

40b. **Port `branch-document-review`** to `template/skills/branch-document-review/SKILL.md`. Source: `~/code/AITaxBID/skills/BranchWorkflow_Skill.md` (178 lines). **Highest-value port for the claude.ai-only audience** — bracketed inline comments (`[fix this]`, `[?]`, `[move to slide 8]`) work in any text box, including the GitHub web UI editor. **Real REST adaptation required:** Andrea's skill assumes local `git diff` against the branch-creation commit; the equivalent is read-via-Contents-API at two refs (`?ref=<branch>` and `?ref=main`), then diff in Python sandbox-side, then parse the bracketed-comment delta. Two implementation choices for the diff (decide at port time): (a) GitHub Compare API `GET /repos/{owner}/{repo}/compare/{base}...{head}` returns unified diff per file (slight preference; preserves git-native semantics) or (b) read both refs via Contents API and diff with Python `difflib`. **Light/heavy review distinction** ports verbatim: light fixes silent (typos, accents, capitalization, punctuation, citation formatting) vs. heavy issues flagged (terminology drift, document-internal inconsistency, voice mismatch). Three-section report-back ports verbatim. **Pandoc regeneration step is gated on sandbox-tooling check** (see task 31's pypdf precedent — but pandoc, LaTeX, python-docx are all unverified); ship v1 of skill without regeneration plus a TODO if pandoc unavailable. Frontmatter `name: branch-document-review`. Estimated effort: ~2-3 hours including the diff-parsing helper.

40c. **Read AITaxBID's `document_processing.md` and port as `document-processing`** to `template/skills/document-processing/SKILL.md`. Source: `~/code/AITaxBID/skills/document_processing.md` (277 lines, **not yet read in detail by the audit** — first task of this port is a careful full read). Scope per Andrea's README: legislation, government regulatory documents, terms of reference, consultant deliverables. Pipeline: rename / extract / summarize / classify / index / cross-reference. Configuration parameters: reliability labels (Citable / Validated / Under construction / Working draft / Flagged), confidentiality labels (PUBLIC / INTERNAL / CONFIDENTIAL), folder organization. **Make all configurable parameters optional** — most users won't have an INTERNAL/CONFIDENTIAL distinction; ship sensible defaults (Citable / no-confidentiality) and let users override in personal_info.md or a per-repo config. **Nori has no analog** — this is meaningfully new capability for policy / development / regulation researchers. Frontmatter `name: document-processing`. Estimated effort: ~3-4 hours including the source-read.

41. Carry over unchanged: `brainstorming`, `test-driven-development`, `systematic-debugging`, `root-cause-tracing`, `receiving-code-review`, `write-a-plan`, `handle-large-tasks`, `testing-anti-patterns`, `creating-debug-tests-and-iterating`. Copy verbatim. Adjust any internal file-path references that assumed local filesystem (most won't have any).
42. Drop entirely: `use-worktree`, `clean-worktrees`, `webapp-testing`, `building-ui-ux`, `using-screenshots` (claude.ai handles images natively), `finishing-a-development-branch` (collapsed into CLAUDE.md's wrap-up path), `updating-noridocs` (no Nori on the web side), `maintaining-decision-docs` (out of scope for v1).
43. Write `template/skills/SKILL_INDEX.md`: a manifest listing each skill with its SKILL.md URL on the public repo, one-line description, and trigger conditions. CLAUDE.md tells the agent to fetch this manifest at session start so it knows what's available. **Note:** the manifest stub already exists (Phase 4 task 26 / commit `681ed9d`). This task finalizes by adding entries for any skills that didn't exist when the stub was written — at minimum, the AITaxBID-sourced ports from tasks 40a–40c (`writing-skill`, `branch-document-review`, `document-processing`). Likely groups the AITaxBID ports under a new "Writing & document workflow" section between "Knowledge-management skills" and "Working-style skills."
44. Commit: `Phase 6: skills — REST-adapted and carried over (+ AITaxBID-sourced)`.

## Phase 7: Reference docs in `template/reference/`

45. Write `WHY_REST.md`: longer-form plain-language explanation of the sandbox + allow list, expanding on the short blurb in `_PROJECT_INSTRUCTIONS.md.template`.
46. Write `PAT_SETUP.md`: step-by-step fine-grained PAT creation. Include exact scope checkboxes needed for both `basic_config` (read) and `research-<topic>` (read/write). Include a screenshot if Dan can capture one; otherwise label the GitHub UI elements precisely.
47. Write `PROJECT_SETUP.md`: claude.ai Project setup walkthrough including Domain Allow List configuration. Include screenshots of: New Project button, custom instructions box, files upload area, Settings > Capabilities > Allow Network Egress > Domain Allow List.
48. Commit: `Phase 7: reference docs — PAT setup, Project setup, REST explanation`.

## Phase 8: Self-walkthrough by Dan

49. Dan creates a fresh GitHub account or uses a sock-puppet account that has never seen this setup. Pretends to be a non-CLI-savvy professor.
50. Pastes the bootstrap prompt into a fresh claude.ai chat.
51. Walks through every step. Notes friction points in `docs/convos/<date>_self_walkthrough.md`.
52. Iterates `BOOTSTRAP.md`, `reference/`, and skills based on findings. Each fix is a separate commit referencing the convo.
53. Repeats until the walkthrough takes <20 minutes start-to-finish.

## Phase 9: Recruit-and-walkthrough with a tame collaborator

54. Identify candidate (one of the AI-policy-coalition collaborators is most likely; should be someone whose research domain Dan understands so the test data feels realistic).
55. Brief them: "I'm testing a setup. I'll watch you do it without helping. Please think out loud about anything confusing."
56. Run them through bootstrap. Capture observations in `docs/convos/<date>_collaborator_walkthrough_<name>.md`.
57. Iterate on documentation and skills. Repeat with second collaborator if the first finds substantial issues.

## Phase 10: Publish

58. Decide publish strategy. Default: flip the dev repo from private to public, OR push only `template/` contents to a separate public `github.com/danparshall/claude_researcher` repo. Trade-off: dev-repo-public means convos and plans are visible (FOSS transparency); template-only means the public repo is clean. Choose based on whether convo content has anything Dan wouldn't want public.
59. Update `template/README.md` with the bootstrap prompt URL pointing at the public repo location.
60. Test: from a clean machine, paste the bootstrap prompt into claude.ai and confirm the agent can fetch and follow `BOOTSTRAP.md`.
61. Open a placeholder issue or two on the public repo to validate the issue-filing pre-filled URL works end-to-end.

---

**Testing Details**

End-to-end manual testing only — no unit tests. Acceptance: a non-CLI-savvy collaborator gets through bootstrap in <20 minutes from a fresh claude.ai chat without intervention, and successfully runs at least one working session (read STATUS, work on a research line, finish-convo) afterward. Any step that requires Dan to step in and explain is a documentation defect to be patched in `BOOTSTRAP.md` or `reference/`.

**Implementation Details**

- Use Markdown frontmatter `name:` / `description:` consistent with Nori skill conventions in all SKILL.md files.
- Every script in `template/scripts/` reads `TOKEN`, `USERNAME`, `REPO` from environment variables (set by the agent before running each script). Don't hard-code paths or auth.
- Every REST call sets `Accept: application/vnd.github+json` and `X-GitHub-Api-Version: 2022-11-28` for forward compatibility.
- Bootstrap PAT instructions must specify *fine-grained* PAT with both `basic_config` (read) and `research-<topic>` (read/write) selected explicitly. Classic PATs work but are broader-scoped; only fall back if fine-grained fails.
- `_PROJECT_INSTRUCTIONS.md` MUST be in `.gitignore` of every research repo. The seed_repo.py script must include this in the initial `.gitignore`.
- Issue-filing pre-filled URL: URL-encode title and body; include git_fluency tier + CLAUDE.md SHA in body for triage; never include PAT or personal_info contents beyond the tier.
- Naming consistency: throughout content and skills, use `<USERNAME>` for the GitHub handle, `<REPO>` for the research repo, `<USERNAME>/basic_config` for the lifetime config repo.

**What could change**

- **claude.ai custom-instructions length limit.** If small, CLAUDE.md must be a fetched-at-runtime URL. If large, can be pasted directly into the Project's instructions field. Affects bootstrap output (whether to give the user a CLAUDE.md text block or a "fetch from this URL" pointer).
- **pypdf availability in sandbox.** If pypdf is not pre-installed, `extract_pdf_text.py` must `pip install pypdf` at runtime. Verify before Phase 5 task 31.
- **Fine-grained PAT cross-org write capability.** Whether a fine-grained PAT can write issues to `danparshall/claude_researcher` (a repo the user doesn't own) is unclear. If yes, v2 auto-file via `UPSTREAM_TOKEN` is straightforward. If no, we either accept v1 pre-filled URL forever or fall back to a classic PAT with `public_repo` scope.
- **Atomic commits.** v1 ships with multi-commit finish-convo. If users find the commit log ugly, prioritize the Git Data API helper from `rest_helpers.commit_files()` follow-up.
- **Skill SHA pinning.** Currently agents fetch from `main` branch of `claude_researcher`. If breaking changes ever ship, this could break in-flight sessions for users on stale Project files. May want to pin via SHA or tag in the future, but YAGNI for v1.

**Questions**

- ~~**Nori license confirmation.**~~ **Resolved.** Nori ships Apache 2.0 (`LICENSE`) **plus** a Ship of Theseus addendum (`LICENSE-ADDENDUM.txt`) that explicitly defeats the LLM-cleanroom dodge: "Using any AI tool to produce functionally equivalent software... creates a derivative work subject to the full terms of the primary license." The addendum requires inclusion alongside Apache 2.0 in any derivative work. Both files now live at `claude_researcher/` repo root and will be duplicated into `template/` per Phase 2 task 3.
- **Repo visibility for `basic_config`.** Default private (the design assumes this). But if private, the agent's PAT must have read scope on it — confirm fine-grained PAT supports this.
- **Should the public `claude_researcher` repo include the `docs/convos/` and `docs/plans/` from this dev repo?** Pro: FOSS transparency, downstream contributors can read rationale. Con: noise in the public repo, some convos may have decisions that don't map to the published code. Default: leave them in dev repo only; revisit if collaborators ask "why did you decide X?".
- **What happens when Dan's CLAUDE.md upstream changes mid-session for a user?** A user mid-session won't re-fetch CLAUDE.md unless the skill explicitly does so. Acceptable; no action needed unless we hit a real-world bug.
- **Is `claude_researcher` the right name long-term, or should it be `nori-researcher-web` or similar?** Naming question. Default: stick with `claude_researcher` since that's what Dan picked.
- **Sandbox tooling matrix beyond pypdf.** Phase 5 task 31 verifies `pypdf`. Phase 6 task 40b (`branch-document-review`) needs `pandoc` for the regeneration step. `document-processing` (40c) may want `python-docx`. Worth a single consolidated check in a fresh claude.ai chat, results recorded in `template/reference/SANDBOX_TOOLING.md`, referenced by every subsequent skill port. Pure information gathering; no design decision until results are in.
- **Per-user-repo `CLAUDE_TEMPLATE.md`.** Andrea's pattern of a per-project CLAUDE.md with `Generic skill: ... project-specific implementation` blocks is portable in form, but claude_researcher's design currently has STATUS.md + personal_info.md + the upstream runtime CLAUDE.md serving part of that role. Whether each user's research repo would benefit from its own short project-specific CLAUDE.md (overriding or extending upstream) is a real design question. Tracked here, deferred until Phase 6 ports demonstrate (or fail to demonstrate) the need.
- **`branch-document-review` diff approach (a) vs (b).** GitHub Compare API vs. read-both-and-difflib. Decide at port time (task 40b); slight preference for (a). Captured in [`docs/convos/20260509_phase6_skill_port_planning.md`](../convos/20260509_phase6_skill_port_planning.md) Open Questions.
- **`raw.githubusercontent.com` allow-list miss at BOOTSTRAP Step 8** (smoke-test artifact, May 9). Agent fell back to a stale WebFetch cache when sandbox curl failed allow-list check. Two possibilities: (a) BOOTSTRAP Step 1's paste instructions don't actually result in `raw.githubusercontent.com` being added (UI quirk or instruction defect), or (b) the architectural rule "WebFetch reaches public upstream content" was supposed to mean the agent uses WebFetch (not curl) for `raw.githubusercontent.com` reads — in which case Step 8 needs an explicit "use WebFetch, not curl" callout. Step 9 validation passed end-to-end despite this, so it's a small follow-on, not a blocker. File as upstream issue once investigated.

---
