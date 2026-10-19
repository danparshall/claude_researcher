# 20261014_andrea_incoming_pr_review

**Date:** 2026-10-14 (session ran into 2026-10-16)
**Branch:** main
**Surface:** claude-code
**Machine:** Dans-MacBook-Air
**Session:** Dan (air, claude_researcher, 20261014T1942, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-claude-researcher/be2f3ae4-0336-40e3-b354-03a1afb7489f.jsonl · —

## Summary

We reviewed Andrea's PR #76. It adds `incoming/andrea/`: 51 files, ~14.6k lines, a byte copy of her starter package v2.5 from the private `SkillPropagation` repo, with nothing in `template/` reading it. My first take was to merge it after Andrea explicitly confirmed she was fine with public release and Apache-2.0 (the repo is public, her source is private), with a pointer in `_MAINTENANCE.md` and none in SKILL_INDEX. Dan chose instead to compare the kits skill by skill. Five parallel agents compared her files against our `template/skills/`. The merged report is in results (below).

The comparison showed that her kit has become a prescriptive system: FOLDER_MAPs, typed indexes, workspace/workdesk folders, archetypes, propagation. Its git model is also main-first. So most of what transfers is rules and ideas, not files. Dan then proposed that the useful material belongs in separate repos with their own focus, starting with a `claude_writing` repo. He then proposed a third repo: a lighter version of `pat-helper`, focused on read paper → extract claim → compare to source → confirm.

Reading `~/code/pat-helper` (multi-model paper review, with claim checking as one strand) and `~/code/verification` (its archived `power-side-citation-check` line: a 69-agent workflow, 462 claims, `claims_ledger.csv`, a sources manifest with sha256s) showed that the claim-check pipeline already exists in three independent versions. Each has different strengths and different verdict words. That made the case for the third repo much stronger: distill the three versions rather than invent a fourth. Dan said the plan is "broadly good".

## Topics Explored
- PR #76 merge considerations: public exposure of private-repo content and the license grant; clone weight (~1.3 MB, about doubling the template); duplicate skill names in the clone; where to point to it
- Per-skill comparison of our template skills with her v2.5 kit (see results file)
- Splitting the useful material into focused repos (writing; claim checking)
- pat-helper's design (8 lenses × 3 models, mechanical quote check, `unverifiable` verdict, source-check stage 3.5, recall harness)
- verification's Oct 9 power-side claim check as a hand-built run of the same pipeline

## Provisional Findings
- Her two verification skills (`agent_research_verification`, `own_document_verification`) look like the highest-value material. They are about evidence, not prose, and they matter most where deep-research output gets cited to policymakers.
- Structure-independent ports for claude_researcher: paper summary section (e) "From the visual layer" and the re-verify loop; the dangling-reference scan in finish-convo; the brainstorming turn rules; the audit "drift fix / requires decision" labels; `document_processing` (#6) once a materials index has a home.
- Her FOLDER_MAP / typed-index structure doesn't transfer. Adopting it would be a rewrite, and our generated, hook-checked paper index looks more reliable.
- Three independent versions converged on the same rules. pat-helper's `unverifiable` and Andrea's "unretrieved → unverifiable" were reached separately, as were model rotation and her separate chats, and the power-side workflow's freeze-then-correct and her "verifier never edits the draft". This suggests the rules are sound.
- The three verdict vocabularies don't line up (upheld/refuted/unverifiable; confirmed/partly/contradicted/not found/not checkable; confirmed/partially/contradicted/unverifiable/fabricated/misattributed).
- The power-side `claims_ledger.csv` (462 rows) could serve as a test set for a lighter tool, but its verdicts came from agents and haven't been reviewed one by one. Treat them as unconfirmed labels until a sample is hand-checked.

## Decisions Made
- PR #76 is not to be merged as a vendored folder (Dan: "let's not do it that way"). Proposed: close it with a note to Andrea explaining the split. Not yet done.
- Proposed three-repo split, which Dan called "broadly good":
  - **claude_researcher:** getting sources in and organized. Her paper-processing additions and the verification-adjacent session rules port here.
  - **claude_writing (new):** her writing cluster (writing notes and drafting, product ledger, visuals, LaTeX paper and slides, latex round trip, design deck, translation review), plus our `iterative-writing-workflow` and `branch-document-review` moved out. `add-deliverable` stays in researcher.
  - **Claim-check repo (new, name TBD):** distills pat-helper, the power-side workflow, and her two verification skills. "Lighter" means skills plus one standard-library script for quote grounding and citation matching, shared with pat-helper rather than written twice.
- Repos are to be created one at a time, as each gets a first real user.

## Results
- [`docs/results/20261014_andrea_kit_v2.5_comparison.md`](../results/20261014_andrea_kit_v2.5_comparison.md): per-skill comparison, merged from five agents, not line-checked

## Open Questions
- Is Andrea a co-owner of claude_writing? Is it an add-on to researcher (cloned alongside it) or standalone with its own bootstrap? I leaned toward add-on.
- The claim-check repo's minimal input format for a "held source", so it works with either kit or with none.
- One verdict vocabulary across the three versions.
- Contamination: the light tool must not see pat-helper's or the ledger's verdicts on the same draft.
- Prior art on splitting text into claims: FActScore (Min et al. 2023), SAFE (Wei et al. 2024). These are from memory and not yet looked up.
- Next steps offered: draft the PR #76 note to Andrea, or brainstorm the claim-check repo starting from the verdict vocabulary.
- Fired reminders surfaced at session start and not yet handled: claude_researcher #74, #42, #36; dotfiles #109, #91, #70, #68, #42, #35. (By 2026-10-19, #74 and #42 had been handled elsewhere.)

## Addendum (2026-10-19)

The two new-repo design tickets were filed here, each with an outline sketch in its body, to be transferred once the repos exist. The rest of the proposed ticket list was offered for Dan's later review and not filed: close PR #76 with a note to Andrea; port the paper-summary additions; add the dangling-reference scan to finish-convo; add the brainstorming turn rules; add the audit labels and modes; comment on #6; hand-check a sample of the power-side ledger; pull pat-helper's mechanical checks into a shared script.

PR #76 was closed on Dan's instruction on 2026-10-19, with a comment to Andrea explaining the split and asking whether she wants to co-own claude_writing. The branch `andrea-incoming-starter-v2.5` was left in place.

## Captured Tasks

- [#98: Design and create claude_writing repo (drafting + deliverables kit)](https://github.com/danparshall/claude_researcher/issues/98) — captured 2026-10-19
- [#99: Design and create claim-check repo (lighter sibling of pat-helper)](https://github.com/danparshall/claude_researcher/issues/99) — captured 2026-10-19
