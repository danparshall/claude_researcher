# Status — claude_researcher (dev repo)

## What this repo is

Meta dev repo for building `claude_researcher`, a downstream fork of the Nori researcher Skillset adapted for claude.ai. **Not a research project itself.** Work is structured as one implementation plan followed in numbered phases.

## Critical note for fresh agents

The `docs/` layout is intentionally **flat** (`docs/convos/` + `docs/plans/`). Do NOT offer to scaffold to the standard `docs/active/<branch>/` layout — Dan explicitly chose flat for this single-purpose meta repo. Skip the "research structure check" prompt for this repo.

There are no `papers/`, `docs/active/`, or `docs/historical/` directories and there shouldn't be.

## Current state

- **Plan:** [`docs/plans/01_initial_build.md`](docs/plans/01_initial_build.md) — 10 phases, 61 tasks.
- **Currently at:** Phase 1 — create the GitHub remote and push.
- **Branch:** main only. No research lines / feature branches.
- **GitHub remote:** not yet created (Phase 1 task 1).

## Recent sessions

- **2026-05-08** — Design conversation establishing dual-repo collaborator model, REST-API-via-PAT, on-demand skill fetching, bootstrap interview, runtime session flow, skill REST adaptations. Plan written. License (Apache 2.0 + Ship of Theseus) committed at root. Convo: [`docs/convos/20260508_claude_ai_researcher_design.md`](docs/convos/20260508_claude_ai_researcher_design.md).

## Open questions (live)

See plan's "Questions" section for full list. Highlights:

- claude.ai custom-instructions length limit (verify before Phase 4).
- pypdf availability in claude.ai's sandbox (verify before Phase 5).
- Fine-grained PAT cross-org write capability (relevant for v2 issue auto-file).
- Whether to publish `docs/` alongside `template/` at Phase 10.
