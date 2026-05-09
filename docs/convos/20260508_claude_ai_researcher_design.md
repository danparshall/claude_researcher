# claude.ai Researcher Design

**Date:** 2026-05-08
**Repo:** claude_researcher (new)

## Summary

Design conversation for porting Dan's Nori `researcher` Skillset to claude.ai's web UI, so collaborators on locked-down work machines (scientists, professors, economists) can use the research-first workflow without installing Claude Code locally.

The session walked through four design phases: scoping (who is the worst-case collaborator and what do they have), architecture (where do skills and CLAUDE.md content live), bootstrap flow (the one-time setup interview), runtime flow (what each working session does), and skill adaptations (which skills need REST API porting vs. carry over unchanged). Each phase was validated before moving to the next.

The killer realization was that Dan's existing `_PROJECT_INSTRUCTIONS.md` pattern — claude.ai Project + GitHub PAT + REST API — already solves the GitHub access problem for sandboxed agents. The work to "connect researcher to claude.ai" is bounded: adapt git-CLI-using skills to the Contents API, port CLAUDE.md, and wrap the whole thing in a self-onboarding bootstrap so a non-CLI-savvy researcher can get set up by pasting one prompt into a fresh claude.ai chat.

## Topics Explored

- **Outstanding-task triage.** Confirmed no GitHub issue or note tracked this work; it was an undocumented intention. Captured the design here so it stops being undocumented.
- **Scope of "connecting" researcher to claude.ai.** Three plausible interpretations (re-package as native claude.ai Skill, MCP bridge, REST-API-via-PAT). Settled on REST-API-via-PAT since Dan already uses it.
- **Collaborator profile.** Worst-case is a smart professor who is not CLI-fluent. Has a GitHub account and at least Claude Pro. Needs browser-only setup.
- **Repo model for collaborators.** Three options: one-repo-many-branches (Dan's model), one-repo-per-research-line, one-repo-flat. Chose one-repo-per-research-line — non-git-fluent users think "this project lives in this place" like a Dropbox folder; "branch" adds nothing.
- **Where skills and CLAUDE.md live.** Three options: centralized upstream-fetched (α), bundled in Project (β), bundled in user repo (γ). Chose α — updates flow cleanly, user's repo stays research-artifact-focused, single rule for the agent ("fetch SKILL.md from this URL").
- **Dual-repo collaborator setup.** Each collaborator gets `<USERNAME>/basic_config` (lifetime, holds personal_info.md and domain_allowlist.txt) plus per-project `<USERNAME>/research-<topic>` repos. The basic_config is the "dotfiles for non-CLI folks."
- **Bootstrap interview content.** Modeled on Dan's `personal_info.md`. Captures: academic history, work history, programming languages/tools, research areas, interaction style notes, **git_fluency tier** (drives handholding level), and **paper naming convention** (used by `add-paper`). Spoken languages dropped — Dan-specific. Pushback default — researchers need it.
- **UX patterns.** Suggest-with-Enter-to-accept for repo names, branch/research-line names, convo summary names. Mirrors existing researcher skill conventions.
- **Runtime session flow.** Pre-flight reads from upstream (CLAUDE.md), basic_config (personal_info.md), and the project repo (STATUS.md, README.md). Branch resolution: agent inspects first user message for a branch name OR a path containing `docs/active/<X>/...`; if neither, lists open research lines and asks which is ready to wrap up to main.
- **Project-confusion handling.** When user names a research line that doesn't match the current Project's REPO, agent states the mismatch and steers them to switch Projects rather than silently proceeding.
- **Skill REST adaptations.** `finish-convo`, `update-docs`, `add-paper`, `audit-docs`, `audit-papers`, `init-research-repo` need REST porting. `brainstorming`, `test-driven-development`, `systematic-debugging`, `root-cause-tracing`, `receiving-code-review`, `write-a-plan`, `handle-large-tasks` carry over unchanged. Worktree-related skills (`use-worktree`, `clean-worktrees`) and UI-specific skills are dropped.
- **Atomic commits.** Contents API does one-file-per-commit; finish-convo would produce 3 commits. Decision: ship v1 with Contents API (acceptable noise), put atomic-commit Git Data API helper in `rest_helpers.commit_files()` as a follow-up. Skills don't need to know.
- **Domain Allow List.** claude.ai Settings > Capabilities > "Allow Network Egress" > "Domain Allow List" needs configuring. Baseline list ships in `claude_researcher`, copied to `<USERNAME>/basic_config/domain_allowlist.txt` at bootstrap, user pastes into the Project's settings during setup.
- **Plain-language proxy explanation.** Replace jargon ("egress proxy", "CONNECT tunnel rejected") with sandbox-and-allowlist framing.
- **Manual PDF uploads.** Users will sometimes drag-and-drop PDFs to `papers/` via github.com's web UI. `add-paper` gets an "ingest orphans" mode that detects unindexed PDFs, applies the user's naming convention, extracts text, and updates indices.
- **Issue filing for upstream feedback.** Pre-filled URL approach (markdown-rendered clickable link → GitHub new-issue form pre-filled → user clicks Submit). Two clicks total, no PAT scope expansion. Auto-file via separate `UPSTREAM_TOKEN` is a v2 upgrade if click friction proves too high.

## Provisional Findings

- The `_PROJECT_INSTRUCTIONS.md` pattern is sufficient infrastructure for claude.ai-based research workflows — no need for MCP bridges or custom Anthropic integrations.
- The bootstrap-interview-once / spin-up-projects-many model gives a ~15-minute lifetime onboarding cost and ~2-minute per-project overhead afterward.
- Skill upstream-fetch costs ~one network round-trip per session-start CLAUDE.md fetch + on-demand SKILL.md fetches; acceptable.
- Most researcher skills are git-CLI-agnostic and carry over without modification — the porting work is concentrated in finish-convo, update-docs, add-paper, init-research-repo, and the audit pair.

## Decisions Made

- Repo name: `claude_researcher` (renamed from earlier `research_claude` working name).
- Content folder name in this development repo: `template/`.
- Architecture: centralized upstream-fetched (Option α).
- Repo model for collaborators: one-repo-per-research-line (Option B).
- Atomic commits: Contents API for v1, atomic helper in v2.
- Issue filing: pre-filled URL for v1, separate `UPSTREAM_TOKEN` for v2.
- Implementation plan to follow at `docs/plans/01_initial_build.md`.

## Open Questions

- **Domain Allow List baseline.** Need to confirm exact set of domains required for the standard workflow. Initial guess: `api.github.com`, `raw.githubusercontent.com`, `github.com`, `codeload.github.com`, plus paper sources (`arxiv.org`, `www.biorxiv.org`, `www.medrxiv.org`, `doi.org`). Will discover gaps during testing.
- **Fine-grained PAT viability for cross-org issue filing.** Need to verify whether a fine-grained PAT can write issues to a public repo the user doesn't own. If yes, simplifies the v2 auto-file path; if no, classic PAT with `public_repo` scope is the only option for `UPSTREAM_TOKEN`.
- **claude.ai custom-instructions length limit.** Need to verify current limit (was reportedly increased on Pro/Team plans). If small, CLAUDE.md must be a fetch; if large, can be pasted directly. Affects bootstrap output format.
- **Image attachment workflow.** `add-paper`'s text-extraction step uses pypdf in the sandbox. Need to verify pypdf is available in claude.ai's Python sandbox or if it needs `pip install` at runtime.
- **Test recruit.** Need at least one tame collaborator (a real researcher with the worst-case profile) to walk through bootstrap end-to-end before publishing. Identifying this person is part of the implementation plan.

## Results

None this session — pure design.
