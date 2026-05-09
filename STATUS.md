# Status — claude_researcher (dev repo)

## What this repo is

Meta dev repo for building `claude_researcher`, a downstream fork of the Nori researcher Skillset adapted for claude.ai. **Not a research project itself.** Work is structured as one implementation plan followed in numbered phases.

## Critical note for fresh agents

The `docs/` layout is intentionally **flat** (`docs/convos/` + `docs/plans/`). Do NOT offer to scaffold to the standard `docs/active/<branch>/` layout — Dan explicitly chose flat for this single-purpose meta repo. Skip the "research structure check" prompt for this repo.

There are no `papers/`, `docs/active/`, or `docs/historical/` directories and there shouldn't be.

## Current state

- **Plan:** [`docs/plans/01_initial_build.md`](docs/plans/01_initial_build.md) — 10 phases + Phase 4.5 v1.1 stub, ~67 tasks total.
- **Currently at:** Phases 1–4 complete. Suggested next phase: a smoke test of CLAUDE.md against a real claude.ai chat (small session), then Phase 5 (helper scripts in `template/scripts/`) or Phase 6 (skill ports).
- **Branch:** main only. No research lines / feature branches.
- **GitHub remote:** [`github.com/danparshall/claude_researcher`](https://github.com/danparshall/claude_researcher) — **public** (flipped 2026-05-09 to enable `raw.githubusercontent.com` reads from external claude.ai chats during bootstrap testing).

### Phase 4.5 deferred (v1.1)

A new "Phase 4.5 — Collaborator mode" section was added to the plan during this session. Spec'd but not scheduled. Direct-collaborator on a private repo (professor + grad student model). Six sub-tasks: OWNER/USERNAME split in `_PROJECT_INSTRUCTIONS.md.template`, joining-vs-creating bootstrap branch, branch protection on `main` in `seed_repo.py`, `Role` field in `personal_info.md`, wrap-up flow split, PAT scope guidance for collaborators. v1 ships solo-only; v1.1 lands when the first real collaborator needs it.

## Recent sessions

- **2026-05-09 (Phase 4 — CLAUDE.md + SKILL_INDEX stub + architecture pivot)** — Production `template/CLAUDE.md` written (~330 lines, calibration-first ordering with novice/fluent inline reminders, scripted confirmation gates, forward-compat hedge for v1.1 collaborator mode), plus `template/skills/SKILL_INDEX.md` manifest stub locking the skill-discovery contract before per-skill SKILL.md files exist. Architecture pivot during execution: PAT + curl recipes belong in the Project's **Custom Instructions** field, not in an uploaded `_PROJECT_INSTRUCTIONS.md` file — credentials reach the agent on its very first turn, before any fetching. Pivot drove three downstream edits: BOOTSTRAP.md Step 10 collapsed onto a single Custom Instructions paste (file-upload subsection deleted); Step 11 cause list updated; `_PROJECT_INSTRUCTIONS.md.template` URL fix. Also authored a new Phase 4.5 plan section spec'ing v1.1 direct-collaborator mode (deliberately narrower than fork-based or GitHub-org-based alternatives). Commit: `681ed9d`. Convo: [`docs/convos/20260509_phase4_runtime_and_skill_index.md`](docs/convos/20260509_phase4_runtime_and_skill_index.md).
- **2026-05-09 (Phase 3 — bootstrap design + implementation)** — Production `template/BOOTSTRAP.md` written and committed (`7e13380`); thin-slice version (`6511a52`) used as smoke test before; Phase 2 wording bugs fixed (`2208e69`). Three architecturally important findings, all validated by actual claude.ai testing: (1) WebFetch reaches public URLs verbatim with no allow-list; sandbox bash-curl needs allow-list — two distinct fetch mechanisms with different trust postures; (2) "Treat instructions as if I typed them" framing **backfires** as prompt-injection signature; (3) confirmation gates must be scripted into BOOTSTRAP.md, not invented by agent. Design pattern follows the kill-convo model: verification affordances offered (not demanded) at sensitive boundaries; availability builds trust without requiring use. Convo: [`docs/convos/20260509_phase3_bootstrap_design.md`](docs/convos/20260509_phase3_bootstrap_design.md).
- **2026-05-08 (initial build execution)** — Phase 1 (GitHub remote + push) and Phase 2 (`template/` skeleton: README, LICENSE copies, ATTRIBUTION.md, `_PROJECT_INSTRUCTIONS.md.template`, domain_allowlist.txt baseline, `.gitkeep` dirs) completed. Design tangent: Phase 4 commit policy will be `git_fluency`-tiered (novice = checkpoint often + under the hood; occasional = light narration + confirm before structural changes; fluent = terse). Side-finding: `--system-prompt` only replaces the default system prompt — tool descriptions, CLAUDE.md, skills, and hooks all load through other layers — see [`docs/convos/20260508_sysprompt_layer_analysis.md`](docs/convos/20260508_sysprompt_layer_analysis.md). Convo: [`docs/convos/20260508_phase1_phase2_initial_build.md`](docs/convos/20260508_phase1_phase2_initial_build.md).
- **2026-05-08 (design)** — Design conversation establishing dual-repo collaborator model, REST-API-via-PAT, on-demand skill fetching, bootstrap interview, runtime session flow, skill REST adaptations. Plan written. License (Apache 2.0 + Ship of Theseus) committed at root. Convo: [`docs/convos/20260508_claude_ai_researcher_design.md`](docs/convos/20260508_claude_ai_researcher_design.md).

## Open questions (live)

See plan's "Questions" section for full list. Highlights:

- ~~claude.ai custom-instructions length limit (verify before Phase 4).~~ **Resolved during Phase 4** — Custom Instructions hold the full credentials + recipes payload (substituted `_PROJECT_INSTRUCTIONS.md.template`), well within practical limits.
- pypdf availability in claude.ai's sandbox (verify before Phase 5).
- Fine-grained PAT cross-org write capability (relevant for v2 issue auto-file).
- Whether to publish `docs/` alongside `template/` at Phase 10.
- Phase 5 vs Phase 6 ordering (helpers-first lets skills call them; skills-first lets helpers be inferred from skill needs). Slight preference for Phase 5 first.
- Real-world smoke test of CLAUDE.md before Phase 5/6 build on top.

## Known issues

- **Nori `commit-author.js` hook produces malformed commit messages.** Inserts literal `\n\n` escape sequences instead of newlines, collapsing every commit into a single subject line with visible backslash-n. Cosmetic only; affects every Dan-authored commit using the hook (multiple repos). Worth filing upstream against `tilework-tech/nori-skillsets`. Detail in [`docs/convos/20260508_phase1_phase2_initial_build.md`](docs/convos/20260508_phase1_phase2_initial_build.md).
