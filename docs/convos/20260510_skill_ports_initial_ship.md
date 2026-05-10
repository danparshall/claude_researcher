# Skill Ports — Initial Ship (Waves 1+2+3, minimal)

**Date:** 2026-05-10
**Branch:** main
**Plan:** [`docs/plans/02_skill_ports.md`](../plans/02_skill_ports.md)

## Summary

Started the session intending to begin Wave 0 (provenance + sync infrastructure) of `02_skill_ports.md` per the suggested-next-session note in STATUS.md. Surfaced five up-front decisions (script language, blob-vs-commit SHA, source-of-truth git repo location, convo name, TDD stance). Before answering any of them, the user reframed the priority: **"the VERY first thing would be to just get skills in there at all, even if not perfect. Right now the onboarding collabs can't use this at all. We'll make improvements later."** That reframe collapsed Wave 0 into "deferred" and pushed Waves 1, 2, and 3 forward into a single fast-ship pass.

Wave 1 went verbatim: 9 SWE carryovers (`brainstorming`, `test-driven-development`, `testing-anti-patterns`, `systematic-debugging`, `root-cause-tracing`, `creating-debug-tests-and-iterating`, `receiving-code-review`, `write-a-plan`, `handle-large-tasks`) copied from `~/.claude/skills/<name>/SKILL.md` into `template/skills/<name>/SKILL.md`. These are pure-thought skills — they don't touch any of the 8 environmental axes — so they work in the claude.ai sandbox unmodified. SKILL_INDEX.md status block updated from "stub" to "partial." Commit `9535e7e`, pushed.

Waves 2+3 (the 6 Researcher skills: `finish-convo`, `update-docs`, `add-paper`, `audit-docs`, `audit-papers`, `init-research-repo`) shipped with one concession to honesty: a single-line banner inserted between frontmatter and body telling a claude.ai agent to translate `git add` / `git commit` / `git push` into the REST `write_update` / `write_new` recipes from its Custom Instructions. The banner is the "B" option from a three-way prompt to the user (A = verbatim, B = banner, C = wait for proper REST adaptation); user picked B. Renamed `auditing-paper-summaries` → `audit-papers` to match the URL convention SKILL_INDEX.md had already locked. SKILL_INDEX.md status block re-updated to "all sections live" with the REST-adaptation caveat made explicit. Commit `0bbd419`, pushed. All 15 skill URLs verified resolving with HTTP 200.

## Topics Explored

- Plan-level reframing: Wave 0 (provenance infra) is not the bottleneck for beta unblock. An empty `template/skills/` directory was the bottleneck. Provenance frontmatter and drift-check are valuable for long-term maintenance but block nothing for v1 beta users.
- Three-way ship gradient for the Researcher skills: (A) verbatim, trust agent's CLAUDE.md context to translate; (B) verbatim + one-line banner flagging the translation work; (C) wait for proper REST adaptation. The cost of B over A is ~5 minutes total. The cost of C over B is days. The cost of A over B is one beta user trying `git push` against a sandbox with no git.
- Naming gap surfaced: local skill dir `auditing-paper-summaries` vs. SKILL_INDEX URL `audit-papers`. The skill's own `name:` frontmatter already said `Audit-Papers`, so the URL was the canonical form; the dir rename was the cleanup.
- Five up-front decisions raised before the reframe (Python vs sh for sync_carryovers; commit-SHA vs blob-SHA for drift detection; where the upstream git repo for `~/.claude/skills/` actually lives; convo name; TDD-or-not for Wave 0 scripts) — all of these still pertain when Wave 0 is eventually picked up. Recording them here so they aren't re-derived next session.

## Decisions Made

- **Wave 0 deferred indefinitely.** No sync_carryovers, no check_drift, no provenance frontmatter on shipped skills. Re-evaluate after first real beta-user session reveals whether drift is actually a problem.
- **Researcher skills ship verbatim with banner, not properly REST-adapted.** Workflow shape is right; command idioms are wrong. Banner makes this legible to the runtime agent. Real REST adaptation is "Wave 2/3 proper" and lands later.
- **`auditing-paper-summaries` → `audit-papers`** as the canonical skill identifier in this repo (matching the SKILL.md `name:` field and the SKILL_INDEX URL).
- **SKILL_INDEX status block tracks reality.** Updated twice this session (after each wave); a partial-state status that lies about what's live is worse than no status. Will keep updating it as ports land.

## Results

- 15 skills live at `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/<name>/SKILL.md` (verified resolving):
  - **Working-style (9):** brainstorming, test-driven-development, testing-anti-patterns, systematic-debugging, root-cause-tracing, creating-debug-tests-and-iterating, receiving-code-review, write-a-plan, handle-large-tasks
  - **Session lifecycle (2):** finish-convo, update-docs
  - **Knowledge management (4):** add-paper, audit-docs, audit-papers, init-research-repo
- 2 commits on main: `9535e7e` (Wave 1), `0bbd419` (Waves 2+3).
- SKILL_INDEX.md status block now accurately describes the partial-but-usable state and points the agent to translate Claude-Code git idioms when fetching the Researcher skills.

## Open Questions

Carried forward from this session, mostly Wave 0 design issues that didn't get answered before the reframe:

- **Where does the upstream git repo for `~/.claude/skills/` live?** The directory itself is an install location (managed by Nori `sks`), not a git checkout. To compare a stamped SHA against "current upstream" later (for the deferred drift check), need to identify the actual upstream repo per skill — likely `tilework-tech/nori-skillsets` for SWE carryovers, and Dan's own author repo for Researcher-authored skills. Resolve when picking Wave 0 back up.
- **Blob SHA vs commit SHA for provenance stamping.** Blob SHA (via `git rev-parse HEAD:<path>`) is content-addressed and only changes when the file content changes — better for drift detection than commit SHA, which rotates on merges/rebases without content change. Likely the right call when Wave 0 lands; flagging now so the choice is intentional.
- **Banner vs proper REST adaptation — does it actually work in practice?** The banner is a hypothesis ("a smart agent reading the skill body + the CLAUDE.md REST recipes will translate correctly"). Empirically untested. The first beta user trying to end a session via `finish-convo` is the test. If the agent translates cleanly, banner is sufficient and proper REST adaptation can stay deferred. If the agent fumbles, prioritize Wave 2/3 proper REST work.
- **Path references inside Researcher skill bodies still hardcoded to `/Users/dan/.claude/skills/...`** (e.g., `finish-convo.md` line 13: "Read and follow `/Users/dan/.claude/skills/update-docs/SKILL.md`"). Banner doesn't address this. Same empirical question — does the agent translate the path to a `raw.githubusercontent.com` URL automatically, or does it try to read the local path? Watch for this in the first beta session.
- **15-skill claim vs the 14-skill SKILL_INDEX baseline.** SKILL_INDEX listed 14 entries before this session (per STATUS.md's "currently lists 14 skills" note); we shipped 15 SKILL.md files. The audit-papers rename netted +0; everything else was new. Worth a sanity-check at the start of next session to confirm the SKILL_INDEX entry count and per-section breakdown match what's actually on disk.

## Deferred — when to pick back up

- **Wave 0 (provenance + sync infrastructure):** when drift between upstream and shipped skills becomes a real concern. Likely after first beta session, or after the first time Dan touches `~/.claude/skills/<x>` and wants to know whether the change is also in `template/skills/<x>`.
- **Wave 4 (AITaxBID Tier A: writing-skill, branch-document-review):** untouched. Wave 4 covers Andrea's most portable AITaxBID skills; not on the critical path for the SWE-carryover-style beta unblock but valuable for actual research use.
- **Phase 4.6 (CLAUDE.md retrofit from AITaxBID audit):** untouched. ~30-60 min of focused edits. Recommended before more skills layer on so the universal rules land in CLAUDE.md cohesively.
- **Wave 5 (deferred): document-processing + init-research-repo proper.** `init-research-repo` was actually shipped (with banner) since it lives in `~/.claude/skills/`; only `document-processing` (AITaxBID, 277 lines, not yet read) is still in the Wave-5 bucket.
- **Phase 9 (collaborator walkthrough):** independent of skill-port work; runs in parallel as candidate availability lines up. The first such walkthrough is also the empirical test for the banner-vs-proper-REST question above.
