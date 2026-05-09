# claude_researcher v1 Implementation Plan

**Goal:** Build `claude_researcher`, a fork-downstream of the Nori researcher Skillset adapted for the claude.ai web UI, so non-CLI-savvy collaborators on locked-down work machines can use the research-first workflow with browser-only setup.

**Originating conversation:** [docs/convos/20260508_claude_ai_researcher_design.md](../convos/20260508_claude_ai_researcher_design.md)

**Context:** Dan's Nori researcher profile only works in Claude Code on a developer's local machine. Collaborators (scientists, professors, economists) often work on locked-down employer machines where they cannot install Claude Code. The design conversation established that claude.ai's Project + GitHub PAT + REST API pattern (already used by Dan via `_PROJECT_INSTRUCTIONS.md`) is sufficient infrastructure to host the researcher workflow on the web UI, provided skills that shell out to `git` are adapted to the GitHub Contents API and the whole setup is wrapped in a self-onboarding bootstrap.

**Confidence:** Exploratory–medium. The architecture is settled (Option α: centralized upstream-fetched skills, dual-repo collaborator setup). Specific friction points — claude.ai custom-instructions length limits, fine-grained PAT scopes for cross-org issues, pypdf availability in the sandbox — are open questions that may force small revisions during implementation.

**Architecture:** This dev repo (`~/code/claude_researcher`) contains `template/` (eventual public content) and `docs/` (research process). When `template/` is sufficiently complete and tested, its contents are pushed to a public `github.com/danparshall/claude_researcher` repo, which collaborators read from at bootstrap time and at runtime (via `raw.githubusercontent.com`). Each collaborator ends up with a `<USERNAME>/basic_config` repo (lifetime personal config) and one `<USERNAME>/research-<topic>` repo per research project, plus one claude.ai Project per research repo.

**Branch:** main (this is a new repo; no branches yet).

**Tech Stack:** Markdown for everything human-facing. Python 3.12 for `scripts/` (run in claude.ai's sandbox via Bash). GitHub REST API (Contents endpoint primarily; Git Data API for the v2 atomic-commit helper). No build step, no package manager, no test framework — this is a content-and-prose repo.

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

## Phase 1: Populate the `template/` skeleton

1. Write `template/README.md`. Top of file: human-readable explanation of what this repo is + the copy-pasteable bootstrap prompt the collaborator pastes into claude.ai. Include the rendered prompt in a code block so it's clearly copyable.
2. Write `template/LICENSE` (MIT, copyright Dan Parshall + acknowledgment that this is a downstream fork of Nori skillsets).
3. Write `template/ATTRIBUTION.md` documenting the Nori → Dan → collaborator chain.
4. Write `template/_PROJECT_INSTRUCTIONS.md.template` with `<TOKEN>`, `<USERNAME>`, `<REPO>` placeholders + a plain-language "Why this uses the GitHub API" section pointing to Settings > Capabilities > Allow Network Egress > Domain Allow List.
5. Write `template/templates/domain_allowlist.txt` with baseline domains: `api.github.com`, `raw.githubusercontent.com`, `github.com`, `codeload.github.com`, `arxiv.org`, `www.biorxiv.org`, `www.medrxiv.org`, `doi.org`. One domain per line, sorted, with comment lines marking workflow-required vs paper-source domains.
6. Create empty directories with `.gitkeep` files: `template/skills/`, `template/scripts/`, `template/reference/`. (Subdirectories created when files are added.)
7. Commit: `Phase 1: skeleton — top-level files, license, attribution, allowlist baseline`.

## Phase 2: Write `BOOTSTRAP.md`

The bootstrap doc is the orchestration script the agent follows during the one-time setup chat. Each numbered step below corresponds to a section in `BOOTSTRAP.md`.

8. Write the skeleton: title, audience (a Claude session reading this), section headers for each step.
9. Write the mode-check section. Single question: "Will you only use claude.ai, or also work locally on a non-locked machine?" Branch on answer.
10. Write the GitHub readiness section. Sub-flows for: (a) no GitHub account → walk them through creating one, (b) account but no PAT → hand them `reference/PAT_SETUP.md`, wait for paste-back.
11. Write the project-topic + repo-name section. Suggest-with-Enter pattern: agent proposes `research-<slug>` from the topic.
12. Write the interview section. Fields: name, current role, academic history, work history, programming languages/tools, general research areas, interaction style notes, **git_fluency tier** (3-tier multiple choice: fluent/occasional/novice), **paper_naming format** (template with placeholder explanation, default `{year}_{first_author}_{slug}`).
13. Write the basic_config existence-check branch. If `<USERNAME>/basic_config` already exists, skip the interview and re-use the existing personal_info.md + domain_allowlist.txt; only create the research repo. If not, run the full interview and create both repos.
14. Write the sandbox-scripts orchestration section. Sequence: `create_repo.py` (basic_config if needed) → `seed_repo.py` (basic_config initial files) → `create_repo.py` (research repo) → `seed_repo.py` (research repo initial files).
15. Write the claude.ai Project setup walkthrough. Steps: New Project → name → paste custom instructions (provided as a code block) → upload `_PROJECT_INSTRUCTIONS.md` (provided as a code block) → open Project Settings → Capabilities → Allow Network Egress → Domain Allow List → paste from `<USERNAME>/basic_config/domain_allowlist.txt`.
16. Write the validation section. "Open a new chat in your Project and say 'hi'. The agent should greet you by name and reference your background."
17. Commit: `Phase 2: BOOTSTRAP.md — orchestration for one-time setup chat`.

## Phase 3: Write `CLAUDE.md`

The runtime instructions every working session loads.

18. Write the skeleton: session-start sequence, branch resolution, runtime workflow, end-of-session, issue reporting.
19. Write the session-start fetch sequence: read `_PROJECT_INSTRUCTIONS.md`, fetch `basic_config/personal_info.md`, fetch `basic_config/domain_allowlist.txt` (for awareness, not action), fetch `STATUS.md` and `README.md` from the research repo.
20. Write the branch-resolution logic: (a) direct name match against STATUS.md inventory, (b) indirect-via-path match for `docs/active/<X>/...`, (c) if neither, list open research lines and ask the wrap-up question.
21. Write the project-confusion handling section: when user names a repo that doesn't match `_PROJECT_INSTRUCTIONS.md`'s REPO, state mismatch and steer to switch Projects.
22. Write the wrap-up / merge-to-main path: open PR via REST → merge → `git mv docs/active/<branch> docs/historical/<branch>` → update STATUS.md "Archived Research Lines" table.
23. Write the git-fluency calibration section: read `git_fluency` from personal_info.md, calibrate terminology and verbosity (novice → "research line" not "branch", explain merges as "finalizing into the permanent record"; fluent → terse).
24. Write the issue-reporting section: when user reports a problem, compose pre-filled URL `https://github.com/danparshall/claude_researcher/issues/new?title=<X>&body=<Y>`, include git_fluency tier and CLAUDE.md SHA, never include PAT or personal_info contents beyond the tier.
25. Commit: `Phase 3: CLAUDE.md — runtime session orchestration`.

## Phase 4: Write helper scripts in `template/scripts/`

26. Write `rest_helpers.py` with: `read_file(repo, path, ref=None)`, `list_dir(repo, path, ref=None)`, `write_new(repo, path, content, message)`, `write_update(repo, path, content, message)` (handles sha lookup), `delete_file(repo, path, message)`. All use the Contents API. Type hints, docstrings, sensible error handling on 404/403/422.
27. Write `create_repo.py`: `POST /user/repos` with sensible defaults (private, no auto-init since we'll seed manually). Takes name + description from CLI args.
28. Write `seed_repo.py` for `basic_config`: pushes `personal_info.md` (from interview), `domain_allowlist.txt` (from baseline + any extras), `README.md`, `.gitignore` (excludes `_PROJECT_INSTRUCTIONS.md`).
29. Write `seed_repo.py` for research repo: pushes `STATUS.md` (with the standard sections), `RESEARCH_LOG.md` (empty), `README.md`, `.gitignore` (excludes `_PROJECT_INSTRUCTIONS.md`), placeholder `papers/.gitkeep`, `papers/text/.gitkeep`, `docs/active/.gitkeep`, `docs/historical/.gitkeep`. Decide: one script with a `--type basic_config|research` flag, or two separate scripts. Prefer one script with flag (DRY).
30. Write `extract_pdf_text.py`: pypdf wrapper, reads a PDF, writes `.txt` to specified path. Used by add-paper.
31. Add a TODO note at the top of `rest_helpers.py` for the v2 `commit_files()` atomic-commit helper using the Git Data API. Don't implement; document the API call sequence as a comment.
32. Commit: `Phase 4: helper scripts — REST wrappers, repo creation, seeding, PDF extraction`.

## Phase 5: Adapt and carry over skills

For each skill, copy from `~/.claude/skills/<skill>/SKILL.md` into `template/skills/<skill>/SKILL.md`, then adapt as noted. Adaptation = replace git-CLI calls with calls to `scripts/rest_helpers.py`. Keep the `<required>` checklist structure that the Nori skill format requires.

33. Port `finish-convo`. Replace `git add` / `git commit` / `git push` with sequential `write_update()` calls (or `write_new()` for first-time files). Note: produces 3 commits per session-end on Contents API; flag in skill body that this is acceptable v1 behavior.
34. Port `update-docs`. Same as finish-convo but no separate "commit and push" step (every write is a commit on REST).
35. Port `add-paper` — **download mode**. PDF download via curl in sandbox → `extract_pdf_text.py` → write PDF as base64 via `write_new()` → write extracted text → `write_update()` PAPER_INDEX.md and PAPER_SUMMARIES.md. Read `paper_naming` format from `personal_info.md` to decide filename.
36. Port `add-paper` — **orphan ingestion mode**. New flow: list `papers/` → diff against PAPER_INDEX.md → for each orphan, propose rename per `paper_naming` format → confirm with user → rename via Contents API (write_new at new path + delete_file at old path) → extract → index.
37. Port `init-research-repo`. Replaces local `git init` + `mkdir` with `create_repo.py` + `seed_repo.py`. Used during bootstrap; not typically called at runtime.
38. Port `audit-docs`. Read-only — straight `read_file` and `list_dir` calls. Same checks as the local version (orphaned files, missing links, unindexed convos).
39. Port `audit-papers`. Read-only — same as audit-docs but for papers/. Add: detect orphan PDFs and offer to hand them to add-paper's orphan-ingestion mode.
40. Carry over unchanged: `brainstorming`, `test-driven-development`, `systematic-debugging`, `root-cause-tracing`, `receiving-code-review`, `write-a-plan`, `handle-large-tasks`, `testing-anti-patterns`, `creating-debug-tests-and-iterating`. Copy verbatim. Adjust any internal file-path references that assumed local filesystem (most won't have any).
41. Drop entirely: `use-worktree`, `clean-worktrees`, `webapp-testing`, `building-ui-ux`, `using-screenshots` (claude.ai handles images natively), `finishing-a-development-branch` (collapsed into CLAUDE.md's wrap-up path), `updating-noridocs` (no Nori on the web side), `maintaining-decision-docs` (out of scope for v1).
42. Write `template/skills/SKILL_INDEX.md`: a manifest listing each skill with its SKILL.md URL on the public repo, one-line description, and trigger conditions. CLAUDE.md tells the agent to fetch this manifest at session start so it knows what's available.
43. Commit: `Phase 5: skills — REST-adapted and carried over`.

## Phase 6: Reference docs in `template/reference/`

44. Write `WHY_REST.md`: longer-form plain-language explanation of the sandbox + allow list, expanding on the short blurb in `_PROJECT_INSTRUCTIONS.md.template`.
45. Write `PAT_SETUP.md`: step-by-step fine-grained PAT creation. Include exact scope checkboxes needed for both `basic_config` (read) and `research-<topic>` (read/write). Include a screenshot if Dan can capture one; otherwise label the GitHub UI elements precisely.
46. Write `PROJECT_SETUP.md`: claude.ai Project setup walkthrough including Domain Allow List configuration. Include screenshots of: New Project button, custom instructions box, files upload area, Settings > Capabilities > Allow Network Egress > Domain Allow List.
47. Commit: `Phase 6: reference docs — PAT setup, Project setup, REST explanation`.

## Phase 7: Self-walkthrough by Dan

48. Dan creates a fresh GitHub account or uses a sock-puppet account that has never seen this setup. Pretends to be a non-CLI-savvy professor.
49. Pastes the bootstrap prompt into a fresh claude.ai chat.
50. Walks through every step. Notes friction points in `docs/convos/<date>_self_walkthrough.md`.
51. Iterates `BOOTSTRAP.md`, `reference/`, and skills based on findings. Each fix is a separate commit referencing the convo.
52. Repeats until the walkthrough takes <20 minutes start-to-finish.

## Phase 8: Recruit-and-walkthrough with a tame collaborator

53. Identify candidate (one of the AI-policy-coalition collaborators is most likely; should be someone whose research domain Dan understands so the test data feels realistic).
54. Brief them: "I'm testing a setup. I'll watch you do it without helping. Please think out loud about anything confusing."
55. Run them through bootstrap. Capture observations in `docs/convos/<date>_collaborator_walkthrough_<name>.md`.
56. Iterate on documentation and skills. Repeat with second collaborator if the first finds substantial issues.

## Phase 9: Publish

57. Decide publish strategy. Default: push only `template/` contents to `github.com/danparshall/claude_researcher` (public). Keep `docs/` in this dev repo (private or local-only). Alternative to consider: publish whole repo including `docs/` for FOSS transparency.
58. Create the public repo on GitHub. README is the one in `template/`.
59. Push contents.
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
- **pypdf availability in sandbox.** If pypdf is not pre-installed, `extract_pdf_text.py` must `pip install pypdf` at runtime. Verify before Phase 4 task 30.
- **Fine-grained PAT cross-org write capability.** Whether a fine-grained PAT can write issues to `danparshall/claude_researcher` (a repo the user doesn't own) is unclear. If yes, v2 auto-file via `UPSTREAM_TOKEN` is straightforward. If no, we either accept v1 pre-filled URL forever or fall back to a classic PAT with `public_repo` scope.
- **Atomic commits.** v1 ships with multi-commit finish-convo. If users find the commit log ugly, prioritize the Git Data API helper from `rest_helpers.commit_files()` follow-up.
- **Skill SHA pinning.** Currently agents fetch from `main` branch of `claude_researcher`. If breaking changes ever ship, this could break in-flight sessions for users on stale Project files. May want to pin via SHA or tag in the future, but YAGNI for v1.

**Questions**

- **Repo visibility for `basic_config`.** Default private (the design assumes this). But if private, the agent's PAT must have read scope on it — confirm fine-grained PAT supports this.
- **Should the public `claude_researcher` repo include the `docs/convos/` and `docs/plans/` from this dev repo?** Pro: FOSS transparency, downstream contributors can read rationale. Con: noise in the public repo, some convos may have decisions that don't map to the published code. Default: leave them in dev repo only; revisit if collaborators ask "why did you decide X?".
- **What happens when Dan's CLAUDE.md upstream changes mid-session for a user?** A user mid-session won't re-fetch CLAUDE.md unless the skill explicitly does so. Acceptable; no action needed unless we hit a real-world bug.
- **Is `claude_researcher` the right name long-term, or should it be `nori-researcher-web` or similar?** Naming question. Default: stick with `claude_researcher` since that's what Dan picked.

---
