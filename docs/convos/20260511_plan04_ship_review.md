# Plan 04 ship review

**Date:** 2026-05-11
**Branch:** main
**Surface:** claude.ai

## Summary

Fresh-agent review of the prior 2026-05-11 session's ship (Plan 04, Plan 03 audit follow-ups, §0 Persona, init-research-repo refactor). Three pushback items landed as edits: (a) §0 Push Back paragraph reworded to drop two universal-baseline phrases sourced from Dan's userPreferences ("Sycophancy is a failure mode, not a virtue"; "Disagreement isn't disrespect — it's the colleague the user is asking you to be") while preserving the structural "what might not work / why / fixable" template; (b) HUMANS.md "Where this comes from" reframed Claude Code as a later-available parallel option rather than a graduation path the user outgrows to (web is immediately-available, Code opens up later, conventions carry across both); (c) the reference-sweep failure mode — find-and-replace by inspection rather than exhaustive search, hit twice across Plan 03 and Plan 04 Task 2 — was scoped repo-specific rather than promoted to a RESEARCHER.md §5 universal.

Mid-session, the deferred sandbox-tooling-matrix follow-up surfaced. Methodology and snapshot got split into separate files: `tools/sandbox-tooling-protocol.md` documents inclusion criteria, probe procedure, cadence, and post-probe update steps; `template/reference/SANDBOX_TOOLING.md` retains the current snapshot. The init-research-repo retrofit was deferred until a real research project exists as a retrofit target — no synthetic exercise.

End-of-session, `personal_info.md` was confirmed still stale (Research faculty at GWU; Git fluency `occasional`) and updated inline. Bio elicitation produced a full History block: UTK PhD 2010 on spin-phonon coupling in pnictide superconductors via neutron scattering, CU Boulder postdoc (~3 years), NIST Center for Neutron Research Instrument Scientist on BT-7 (~2.5 years), data science 2016–2025 (MITRE/aviation safety, edtech, IT), AI policy pivot in 2026 with Canary Institute as the public-facing home, plus `claude-exit` + welfare-agnostic posture noted. Git fluency bumped to `fluent`. PAT scope on `basic_config` turned out to permit write despite Project Instructions docstring suggesting read-only.

## Topics Explored

- §0 Persona phrasing audit — which lines were Dan's voice as universal default
- HUMANS.md Code-as-graduation-path vs Code-as-later-parallel-option framing
- Reference-sweep failure mode: technique vs rule placement (repo-specific note vs §5 universal)
- Sandbox-tooling protocol-vs-snapshot artifact split
- init-research-repo retrofit timing (deferred to real-project trigger)
- `personal_info.md` refresh — academic + work history elicited iteratively over several turns
- PAT scope discrepancy: docstring vs actual `basic_config` write capability
- Meta-question: how much does richer biographical context actually help future agents

## Provisional Findings

- The §0 Push Back trait's operational substance (structural "what might not work / why / fixable" template) survived the edit; what got cut was rhetorical capstone material that read as Dan's personal voice
- The Code-as-option reframe needed only a single-paragraph rewrite in HUMANS.md "Where this comes from"; line 35 (about Nori non-replacement) is unaffected and remains accurate
- The reference-sweep failure has hit twice (Plan 03's CLAUDE.md → RESEARCHER.md sweep, Plan 04 Task 2's case-sensitive "Custom Instructions" sweep). A repo-specific note in `tools/` is the appropriate weight — actual research repos rarely have repo-wide renames, so a §5 universal would be over-generalized
- Mechanically, the personal_info.md refresh's only behavior-changing field is `Git fluency: fluent` — that's what RESEARCHER.md §1 keys verbosity off of
- The rest of the bio refresh affects engagement quality, not workflow: avoids over-explaining DS concepts, lets physics analogies deploy without translation, anchors `claude-exit` context for any future cross-Claude welfare-adjacent conversation
- One risk introduced: physics-overreach temptation. The bio makes physics analogies more legible to agents reading it, which can be a default-lens trap when policy-native framings would serve better
- userPreferences and personal_info.md now overlap substantially on biographical content (userPreferences had a one-sentence arc; personal_info.md now has the full version)

## Decisions Made

- §0 Push Back paragraph edit shipped (commit `633c1dd`); "Curiosity isn't a luxury" line in framing paragraph retained per Dan's preference
- HUMANS.md Code-as-option reframe shipped (commit `c13dd39`)
- `tools/` folder established for repo-maintenance content (markdown notes, not just scripts). Two initial residents: `sandbox-tooling-protocol.md` (commit `6290260`) and `reference-sweep-note.md` (commit `37986a7`). No `tools/README.md` for two files; revisit if folder grows
- init-research-repo retrofit deferred until next real research-repo project — no synthetic retrofit target
- `personal_info.md` refresh shipped to `basic_config` (commit `0672b28`); Git fluency `occasional` → `fluent`; welfare/claude-exit context placed in History.Work as cross-Claude calibration anchor
- Starter sentence for next session committed to STATUS Suggested-next-session bullet

## Results

- None saved to `docs/results/` — this is the meta dev repo with flat-docs layout and no results/ directory by convention.

## Open Questions

- **PAT scope vs documentation**: Project Instructions docstring describes the PAT as "scoped to read `<USERNAME>/basic_config` and read/write `<USERNAME>/<REPO>`," but a write to `basic_config/personal_info.md` succeeded this session. Either the docstring is stale or the PAT was issued with wider scope than intended. Worth a future audit, or a docstring correction.
- **userPreferences ↔ personal_info.md precedence on biographical content**: both now describe Dan's background at different granularities. RESEARCHER.md §1 has a precedence rule for `Interaction style` overrides but not for biographical fields. If they drift in future, which wins?
- **§0 phrasing edit's empirical test**: whether the milder phrasing still elicits adequately direct pushback from agents in real sessions is unverified. Answer comes from the next several sessions' behavior.
- **Wave 4 scope** (for next session): Dan's "overhaul" language for Andrea's AITaxBID skills suggests deeper rework than the verbatim-with-REST-banner pattern Waves 2/3 used. Worth scoping at session start before executing.
