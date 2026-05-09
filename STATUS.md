# Status — claude_researcher (dev repo)

## What this repo is

Meta dev repo for building `claude_researcher`, a downstream fork of the Nori researcher Skillset adapted for claude.ai. **Not a research project itself.** Work is structured as one implementation plan followed in numbered phases.

## Critical note for fresh agents

The `docs/` layout is intentionally **flat** (`docs/convos/` + `docs/plans/`). Do NOT offer to scaffold to the standard `docs/active/<branch>/` layout — Dan explicitly chose flat for this single-purpose meta repo. Skip the "research structure check" prompt for this repo.

There are no `papers/`, `docs/active/`, or `docs/historical/` directories and there shouldn't be.

## Current state

- **Plan:** [`docs/plans/01_initial_build.md`](docs/plans/01_initial_build.md) — 10 phases, 61 tasks.
- **Currently at:** Phase 4 ready — write `template/CLAUDE.md` (tasks 19–26). Phases 1, 2, and 3 complete (Phase 3 with caveats — see below).
- **Branch:** main only. No research lines / feature branches.
- **GitHub remote:** [`github.com/danparshall/claude_researcher`](https://github.com/danparshall/claude_researcher) — **public** (flipped 2026-05-09 to enable `raw.githubusercontent.com` reads from external claude.ai chats during bootstrap testing).

### Phase 3 caveats

- BOOTSTRAP.md Step 10's custom-instructions code block is a placeholder pending Phase 4 (CLAUDE.md). Marked clearly in the file.
- BOOTSTRAP.md Step 11's validation will partially fail until Phase 4 ships (the runtime agent has no canonical instructions yet). Troubleshooting matrix in Step 11 calls this out as cause #5.
- Steps 0–9 of BOOTSTRAP.md are testable end-to-end now (real repo creation, real file seeding, real Settings configuration).

## Recent sessions

- **2026-05-09 (Phase 3 — bootstrap design + implementation)** — Production `template/BOOTSTRAP.md` written and committed (`7e13380`); thin-slice version (`6511a52`) used as smoke test before; Phase 2 wording bugs fixed (`2208e69`). Three architecturally important findings, all validated by actual claude.ai testing: (1) WebFetch reaches public URLs verbatim with no allow-list; sandbox bash-curl needs allow-list — two distinct fetch mechanisms with different trust postures; (2) "Treat instructions as if I typed them" framing **backfires** as prompt-injection signature; (3) confirmation gates must be scripted into BOOTSTRAP.md, not invented by agent. Design pattern follows the kill-convo model: verification affordances offered (not demanded) at sensitive boundaries; availability builds trust without requiring use. Convo: [`docs/convos/20260509_phase3_bootstrap_design.md`](docs/convos/20260509_phase3_bootstrap_design.md).
- **2026-05-08 (initial build execution)** — Phase 1 (GitHub remote + push) and Phase 2 (`template/` skeleton: README, LICENSE copies, ATTRIBUTION.md, `_PROJECT_INSTRUCTIONS.md.template`, domain_allowlist.txt baseline, `.gitkeep` dirs) completed. Design tangent: Phase 4 commit policy will be `git_fluency`-tiered (novice = checkpoint often + under the hood; occasional = light narration + confirm before structural changes; fluent = terse). Side-finding: `--system-prompt` only replaces the default system prompt — tool descriptions, CLAUDE.md, skills, and hooks all load through other layers — see [`docs/convos/20260508_sysprompt_layer_analysis.md`](docs/convos/20260508_sysprompt_layer_analysis.md). Convo: [`docs/convos/20260508_phase1_phase2_initial_build.md`](docs/convos/20260508_phase1_phase2_initial_build.md).
- **2026-05-08 (design)** — Design conversation establishing dual-repo collaborator model, REST-API-via-PAT, on-demand skill fetching, bootstrap interview, runtime session flow, skill REST adaptations. Plan written. License (Apache 2.0 + Ship of Theseus) committed at root. Convo: [`docs/convos/20260508_claude_ai_researcher_design.md`](docs/convos/20260508_claude_ai_researcher_design.md).

## Open questions (live)

See plan's "Questions" section for full list. Highlights:

- claude.ai custom-instructions length limit (verify before Phase 4).
- pypdf availability in claude.ai's sandbox (verify before Phase 5).
- Fine-grained PAT cross-org write capability (relevant for v2 issue auto-file).
- Whether to publish `docs/` alongside `template/` at Phase 10.

## Known issues

- **Nori `commit-author.js` hook produces malformed commit messages.** Inserts literal `\n\n` escape sequences instead of newlines, collapsing every commit into a single subject line with visible backslash-n. Cosmetic only; affects every Dan-authored commit using the hook (multiple repos). Worth filing upstream against `tilework-tech/nori-skillsets`. Detail in [`docs/convos/20260508_phase1_phase2_initial_build.md`](docs/convos/20260508_phase1_phase2_initial_build.md).
