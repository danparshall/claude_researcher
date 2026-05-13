# 20260513 — Plan 06 W3.1 + Tier C ship (add-paper synthesis)

**Date:** 2026-05-13
**Branch:** main
**Surface:** Claude Code (CLI)

## Summary

Execution session against Plan 06 (`docs/plans/06_w31_addpaper_synthesis.md`). The plan was written by the prior session (commit `9b4c626`, untracked at session start) as an execution-level companion to Plan 05's W3.1 + Tier C sections — file paths, line ranges, exact strings, a 7-check verification script, and a locked decisions list, designed for a fresh agent with zero session context. This session executed that plan straight through: 9 deliverables on `add-paper/SKILL.md` (single rewrite) + 2 knock-on edits + schema definition + BOOTSTRAP updates. Single ship commit (`454018f`), pushed to origin. Issue #3 closed; issue #4 remains open for the post-real-user-data scaling-discipline work.

Key port-time judgments (all small): kebab-case picked for `{Slug}` in the academic filename default (Plan 06 open question line 462 recommended kebab; matches Plan 06's own examples; superseded BOOTSTRAP Batch 3's prior snake_case `attention_is_all_you_need`); `paper_naming` field references in personal_info.md framed as "Operating preferences" section (where they live in the template); `## Project parameters` section ordering in `init-research-repo`'s minimal-seed slot placed between `## Current Focus` and `## Recent Sessions` (the canonical order matches the new BOOTSTRAP Step 7 seed). No port-time decisions hit; the plan held without re-litigation.

The session's epistemic posture matched yesterday's process-finding heuristic: "execution sessions where the plan doc IS the checklist don't need TaskCreate." Plan 06's deliverable list mapped 1:1 to file edits, and the 7-check verification script provided the end-of-work guarantee. Three harness reminders about task tools were ignored on this basis.

## Topics Explored

- Plan 06 pre-flight reads (STATUS.md, README.md, Plan 06 itself, Plan 05 W3.1 + Tier C sections, Andrea's source `paper_processing.md` byte-identical to `e0a736d`, current `add-paper/SKILL.md`, `personal_info.md.template`, `init-research-repo/SKILL.md`, RESEARCHER.md §2c, BOOTSTRAP.md Batch 3 + Step 5b + Step 7 STATUS.md seed)
- Source SHA verification: `git -C ~/code/AITaxBID diff --stat e0a736d HEAD -- skills/paper_processing.md` returned empty — no drift since plan was written. AITaxBID HEAD at execution: `abd1c54`.
- Full rewrite of `add-paper/SKILL.md` (151 → 281 lines, 194 insertions / 64 deletions): Step 0 triage, Scope section with `document-processing` pointer + "where config keys live" note, filename parameterization in Step 1, config-aware index file (PAPERS_INDEX) in Step 3, dual-protocol Step 4 with Summary Evolution Principle, gated BibTeX Step 5, renumbered Stage step to Step 6, "Forgetting Step 0 triage" added to Common Mistakes, "Reading keys from the wrong file" added to Common Mistakes (reinforces Tier C split), dual provenance frontmatter (`nori_researcher_source` + `aitaxbid_source`).
- Schema split per Tier C Option C: `personal_info.md.template` line 35 (single `<PAPER_NAMING>`) replaced with two fields (`<PAPER_NAMING_ACADEMIC>` + `<PAPER_NAMING_INSTITUTIONAL>`). Canonical `## Project parameters` block defined in three seed locations (BOOTSTRAP Step 7, init-research-repo Step 3 append + minimal-seed branches, add-paper's "where config keys live" note).
- BOOTSTRAP.md updates: Batch 3 question rewritten to ask both formats with defaults + "press Enter to accept both" affordance; canonical text below the question split into two stanzas (academic + institutional); recording vars renamed to `<PAPER_NAMING_ACADEMIC>` + `<PAPER_NAMING_INSTITUTIONAL>`. Step 5b extended to capture `<PROJECT_QUESTION>` after `<TOPIC>` is recorded, with the "same sentence is fine" affordance from Plan 06's suggested phrasing. Step 5c (knowledge_base path) given a default `<PROJECT_QUESTION>` placeholder. Step 7 STATUS.md seed extended with a `## Project parameters` section between `## What this repo is` and `## Current state`, substituting `<PROJECT_QUESTION>` and leaving other keys at defaults.
- RESEARCHER.md §2c knock-on: one sentence appended at the end of the STATUS.md description, before the "README.md tells you what the repo is about" sentence, listing the five `## Project parameters` keys and noting no extra fetch is needed.
- Verification: 7-check script ran clean (no drift, dual provenance present, no stale CLAUDE.md refs, Project parameters in both seed files, both new placeholders in personal_info.md.template, RESEARCHER.md §2c line 199 mentions Project parameters, audit skills don't touch project parameters). Plus Knock-on 3 cross-reference verification: `personal_info.md` references in add-paper SKILL.md only pair with `paper_naming.*` keys; `STATUS.md` references only pair with `PROJECT_QUESTION` / `CONDITIONAL_SECTION` / `BIB_FILE` / `PAPERS_INDEX` / `paper_summaries.structure`.

## Provisional Findings

- Plan 06 worked exactly as designed — no port-time decisions hit, no re-litigation, no scope creep. ~40 minutes from "Following Nori workflow..." to push. Plan 06 line 471 estimated 45-60 min; under budget.
- The "decisions confirmed at design time (do NOT re-litigate)" block at lines 22-115 of Plan 06 prevented multiple temptations to expand scope (e.g. enriching Step 2 with Andrea's institutional preserve-acronyms / preserve-boxes rules; collapsing dual `paper_naming` fields into a single format with a smart `{Author}` placeholder; trying to read paper_naming from STATUS.md instead of personal_info.md). The Tier C explicit-split table in Plan 05 lines 280-285 was load-bearing — without it, the easy mistake is putting everything in one file.
- The 7-check verification script (Plan 06 lines 355-385) was sufficient — caught nothing because the work was on-spec, but the cross-reference Knock-on 3 grep (verifying which keys pair with which file in the new SKILL.md) gave the highest signal that the schema split actually landed cleanly. Worth preserving the pattern in future skill ports that involve multi-file schema splits.
- Setting Plan 06 line 462's open question (kebab-case vs snake_case for `{Slug}`) earned its keep — that was the only port-time judgment that mattered (and the plan had already pre-resolved it with a recommendation). Snake_case → kebab-case was the one breaking change for users who used the BOOTSTRAP default earlier this week.
- The repo's flat `docs/` layout caused a small skill-adaptation moment: finish-convo's SKILL.md prescribes `docs/active/<branch-name>/convos/` and `RESEARCH_LOG.md` updates, but this meta repo uses flat `docs/convos/` and has no per-branch RESEARCH_LOG. The "Critical note for fresh agents" at STATUS.md lines 7-12 anticipates this and waives the scaffolding check, but the finish-convo skill body itself doesn't have a flat-repo branch — the agent has to adapt. Worth noting for any future plan that wants to formalize the flat-repo case in the skill (low priority; one-of pattern).

## Decisions Made

- **Kebab-case `{Slug}`** for the academic-default filename convention. Plan 06 line 462 recommended; plan's own examples use it; the SKILL.md and BOOTSTRAP Batch 3 rewrite both use it. Supersedes BOOTSTRAP Batch 3's prior snake_case example (`attention_is_all_you_need` → `attention-is-all-you-need`).
- **Order of `## Project parameters` in the init-research-repo minimal-seed STATUS.md**: between `## Current Focus` and `## Recent Sessions`. Matches the BOOTSTRAP Step 7 seed order (where it sits between `## What this repo is` and `## Current state`). Not specified by the plan; chosen for cross-file consistency.
- **Append-branch logic for init-research-repo Step 3**: separate `## Project parameters` check from the existing `## Archived Research Lines` check. Each block is independently idempotent. The plan said "after the equivalent position" without naming an anchor in the append branch; chose pragmatic append-if-missing logic instead.
- **No backfill of `## Project parameters` to existing repos** (claude_researcher itself or any beta-user repos). Plan 06 line 465 already recommended no; this session confirms — claude_researcher is a meta dev repo, not a research repo, so the section isn't needed here. Beta users will pick up the section the next time they bootstrap.

## Results

- Ship commit: [`454018f`](https://github.com/danparshall/claude_researcher/commit/454018f) — `plan 06 W3.1 ship: add-paper synthesis + Tier C schema split`. 5 files / 220 insertions / 47 deletions.
- Issue #3 closed: [#3 — W3.1 fold-in](https://github.com/danparshall/claude_researcher/issues/3) with reference to ship commit + summary of what landed.
- Issue #4 remains open: [#4 — add-paper scaling discipline](https://github.com/danparshall/claude_researcher/issues/4), sequenced after ~5 papers of real user data accumulate so threshold calibration (length guidelines, two-stage file structure trigger, lookup discipline) has data to calibrate against.

## Open Questions

- **`per-file` summary code path** — still deferred per Plan 05 W3.1 out-of-scope. The config knob `paper_summaries.structure: per-file` now exists in three seed locations but the code path that writes to `papers/summaries/SUMMARY_*.md` isn't implemented. Skill warns the user inline and falls back to `single-file`. Re-evaluate when a user actually wants per-file. Tracked indirectly via issue #4's scope (two-stage file structure trigger could absorb this).
- **Default filename convention for `add-paper`** (Plan 05 line 334) — resolved by Plan 06 D2 (parameterized via `paper_naming.academic_format` + `paper_naming.institutional_format` defaults). Marked resolved in Plan 05 retroactively.
- **First beta session of the W4 skills** — still pending. The just-shipped `iterative-writing-workflow` and `branch-document-review` (commit `9ca89b8` earlier today) haven't been used in a real claude.ai session yet. That's the natural next path per STATUS.md "Suggested next session" lines 27-29.
- **`raw.githubusercontent.com` allow-list miss at BOOTSTRAP Step 8** (still open; STATUS.md line 81). Step 9 validation passes despite this (agent falls back to cached WebFetch); small follow-on, not blocking.
- **W4.0 pandoc spot-check** (Plan 05 line 62) — still open, "do at next WebUI session" was the action. Not a blocker for anything; W4.3 ships without LaTeX/pptx hard dependencies.
