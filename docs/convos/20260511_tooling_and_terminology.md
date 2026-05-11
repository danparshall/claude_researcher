# Tooling and terminology

**Date:** 2026-05-11
**Branch:** main
**Surface:** claude.ai

## Summary

Plan 04 execution session — all four tasks shipped (sandbox tooling matrix, "Custom Instructions" → "Project Instructions" sweep, `Surface` field in convo template, human-readable chat title at §2e handshake), plus audit-driven Plan 03 follow-ups, plus two larger items added mid-session: a §0 Persona section in `RESEARCHER.md` and a refactor of `init-research-repo` to stop duplicating persona-level content into per-repo `CLAUDE.md`. Total: ~20 commits.

Task 1 collapsed the medium-confidence risk in Plan 04: every tool (`pypdf` 5.9.0, `pandoc` 3.1.3, `python-docx` 1.2.0, `git` 2.43.0) is **pre-installed** in the claude.ai sandbox on Ubuntu 24.04. The `difflib` fallback redesign for Wave 4 `branch-document-review` isn't needed; Wave 4 + Wave 5 of skill ports are tooling-unblocked. `template/reference/SANDBOX_TOOLING.md` shipped as the first content file in `template/reference/` and documents both the primary path and the (now unneeded) workaround table.

Mid-session, Dan pushed a HUMANS.md "Where instructions to Claude live" section establishing four-surface vocabulary (Personal preferences in claude.ai Settings, Project Instructions, upstream `RESEARCHER.md`, `personal_info.md` in `basic_config`) and deleted `template/README.md` per the audit recommendation. With that framing in place, the init-research-repo gap surfaced during the audit had a clean architectural answer: "Research Context" content is **persona-level** — it lives upstream in `RESEARCHER.md`, not duplicated into each repo's `CLAUDE.md`. Per-repo `CLAUDE.md` is for project-specific standing notes the user manages, not workflow conventions. The skill's Step 3 (a 21-line Research Context block appended to `CLAUDE.md`) was removed entirely; a preamble in "## The Process" makes the distinction explicit and notes Claude Code users can use `RESEARCHER.md` as their `~/.claude/CLAUDE.md`.

Dan also requested a §0 Persona section in `RESEARCHER.md` establishing four tier-independent traits: follow instructions, push back on bad ideas, don't make decisions silently, stay organized. Persona precedes calibration; the outline was updated to reflect §0 as first read. Dan handed off to a fresh agent for review at session end.

## Topics Explored

- Plan 04 Task 1: empirical sandbox tooling probes — pypdf, pandoc, python-docx, git availability confirmed in a Project chat (sandbox-level probes generalize to unattached chats)
- Plan 04 Task 2: case-sensitive terminology sweep across 10 files (31 occurrences), with lowercase variant later caught in ATTRIBUTION.md
- Plan 04 Task 3: `Surface: claude.ai | claude-code` field added to convo summary template in `update-docs/SKILL.md`
- Plan 04 Task 4: §2e handshake extended to propose human-readable chat title alongside file slug, with deterministic slug→title mapping rule
- Plan 03 reference-sweep follow-ups (audit during Task 3): stale `CLAUDE.md` refs in `SKILL_INDEX.md` (3), `update-docs/SKILL.md` (1), `template/README.md` (deleted by Dan), `ATTRIBUTION.md` (rewrite — three problems on one line)
- HUMANS.md "Where instructions to Claude live" section (Dan's mid-session push) — surface vocabulary
- §0 Persona drafted iteratively: four-trait list → expanded with research-collaborator framing + Push Back corollary about calibrated pushback
- init-research-repo refactor scoped via persona-vs-per-repo distinction
- One-line `RESEARCHER.md` → `HUMANS.md` cross-reference for future agents asking surface questions

## Provisional Findings

- Wave 4 + Wave 5 of skill ports are tooling-unblocked. The architectural pivot Plan 04 worried about (rebuilding `branch-document-review` around `difflib` if `pandoc` was unavailable) is not needed.
- Plan 04 Task 2's case-sensitive sweep missed lowercase "custom instructions" — caught later in ATTRIBUTION.md audit. Future terminology sweeps should use `grep -ri` for verification.
- The init-research-repo "Research Context" block is a clean example of persona-level content leaking into a per-repo file. Removing it didn't require designing new machinery; the function was already covered by `RESEARCHER.md` (which the agent reads every session).
- `template/README.md` was a stale-data hazard listing files that no longer exist (`CLAUDE.md`, `templates/`); root `README.md` is the canonical entry. Dan deleted (commit `f3a00c3`).
- Three skill files (`SKILL_INDEX.md`, `update-docs/SKILL.md`, `ATTRIBUTION.md`) had forward-looking `CLAUDE.md` refs that Plan 03's principled-split sweep missed; mechanical fixes shipped this session.

## Decisions Made

- Plan 04 shipped as-spec'd; no scope changes during execution.
- Mechanical Plan 03 sweep misses (A) + ATTRIBUTION.md rewrite (B3) + RESEARCHER↔HUMANS cross-ref (D6) shipped in same session as Plan 04 wrap. Item 4 (template/README.md) handled by Dan via outright deletion.
- Item 5 (init-research-repo architectural question) shipped as a refactor in this session rather than parked, given Dan's persona-vs-per-repo framing produced a clean answer.
- §0 Persona established as a new top-level section preceding §1 Calibration. Read order: persona → calibration → process.
- Persona-vs-per-repo nomenclature: "persona-level" describes content in `RESEARCHER.md` (operationally loaded by every session); per-repo `CLAUDE.md` is for project-specific notes the user manages.
- Pushback was added as a calibrated trait (don't manufacture concerns for show); commit messages should not glaze.

## Results

- [`template/reference/SANDBOX_TOOLING.md`](../../template/reference/SANDBOX_TOOLING.md) (commit `2746090`) — first content file in `template/reference/`. Empirical tooling-availability record; quarterly re-verification cadence noted.

## Open Questions

- **init-research-repo refactor untested in practice.** A real retrofit (in Code or claude.ai) would exercise whether the persona-vs-per-repo framing reads cleanly to a fresh agent. Currently the skill body says "the Research Context lives upstream in RESEARCHER.md" — does an agent reading the refactored skill resist the urge to append a CLAUDE.md anyway?
- **REST-adaptation banner adequacy** (existing §8 Parking Lot item). Surfaces now have a name (HUMANS.md "Where instructions to Claude live"), but the empirical question — whether banner translation suffices for cross-surface skills — still awaits a real beta session.
- **`personal_info.md` stale data** (Dan flagged at session start). Some test data from BOOTSTRAP development (incorrect role, incorrect `Git fluency` tier) still lives there. Dan deferred to handling via the `dotfiles` agent; not blocking this project.
- **§0 Persona phrasing borrowed from userPreferences** ("sycophancy is a failure mode, not a virtue" echoes Dan's userPreferences phrasing about helpful/harmless/honest). Now baseline language for every user of `claude_researcher`. Flagged for Dan to swap if he wants those phrasings kept personal.
