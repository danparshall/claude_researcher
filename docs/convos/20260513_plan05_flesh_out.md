# claude_researcher — Plan 05 flesh-out

**Date:** 2026-05-13
**Repo:** claude_researcher (dev repo)
**Branch:** main
**Surface:** claude-code (CLI)
**Plan:** [`docs/plans/05_aitaxbid_followups.md`](../plans/05_aitaxbid_followups.md) — went from ~175-line stub to ~340 lines this session.

## Summary

Session opened with Dan's starter sentence from yesterday's suggested-next-session: *"Let's flesh out Plan 05 — start with sandbox-tooling recheck against `template/reference/SANDBOX_TOOLING.md` then move to writing-skill."* Surface ended up being Claude Code (CLI) rather than the WebUI assumed in Plan 05's stub header — driven by the discovery that Andrea's AITaxBID source files (`writing_skill.md`, `BranchWorkflow_Skill.md`, `paper_processing.md`) live on Dan's local filesystem only, with no PAT-readable mirror. CLI gives source access; WebUI doesn't. This reframing flipped the source-access open question Dan added in commit `f54ea05` from a blocker into a resolved item: Wave 4 ports execute from CLI.

Substantive output: every task stub in Plan 05 except the two genuinely-mechanical ones (W4.4 SKILL_INDEX entry, W4.5 ship commit) got a full deliverable list. The two architectural decisions the plan was blocked on — W4.2 diff mechanism, Tier C placement — have reasoned recommendations (Compare API and Option C respectively). The W3.1 fold-in revealed itself as bigger than the initial stub suggested: nine deliverables including a new BibTeX step that adds functionality the current `add-paper/SKILL.md` doesn't have, plus a schema split that the Tier C decision retroactively cleaned up. The "Source-access from WebUI" open question Dan added in `f54ea05` resolved cleanly as a side effect.

The session also surfaced and recorded several loose ends that the plan now flags for port-time confirmation rather than locking: filename convention for `add-paper` (three formats in play), branch-naming format for `branch-document-review` (Andrea's `mmm-d` vs claude_researcher's `YYYYMMDD`), and the file-structure mismatch between Andrea's per-file summary layout and Nori's single-file `PAPER_SUMMARIES.md` (resolved as a config knob, with the `per-file` code path deferred).

## Work Done

### W4.0 — Sandbox tooling spot-check (was: pre-check)

Cross-checked W4.0's proposed probe list against SANDBOX_TOOLING.md and Andrea's source. Found that only `pandoc` is a hard Wave 4 dependency, already verified 2026-05-11 at 3.1.3. LaTeX is explicitly conditional in Andrea's BranchWorkflow source (*"no regeneration unless Andrea has set up the LaTeX pipeline"*); `.pptx` regeneration only applies to slide-source projects; `pypandoc` is a fallback already documented. **Collapsed W4.0 to a confirm-only spot-check** with everything else deferred per the tooling-protocol's on-discovery cadence. Surface notes: the spot-check happens in a WebUI session (any chat), and W4.1/W4.3 are no longer blocked on it.

### W4.1 — Andrea's writing skill port spec

Read Andrea's `writing_skill.md` end-to-end (169 lines, SHA `e0a736d` from 2026-05-02). It's a pure-thought skill (planning, drafting, revising) — no git/CLI ops, so **no REST-adaptation banner is needed** (unlike Wave 2/3). Adaptation profile closer to Wave 1 SWE carryovers than Wave 2/3 Researcher skills. Specified four transformations: (1) add `aitaxbid_source` provenance frontmatter; (2) rephrase "your project's CLAUDE.md" → "your project's RESEARCHER.md, STATUS.md, or equivalent coordination file" (post-Plan-03 rename); (3) drop "Last updated" footer; (4) leave Andrea's two-protocol structure intact. Also flagged the naming decision: Andrea's YAML name is `iterative-writing-workflow`, Plan 05's stub example used `writing-skill`. Per "defer to Andrea," Andrea's own name wins — recommendation `iterative-writing-workflow`. Per Dan's request, added an actionable style-profiles note ("if you don't have a style-profiles doc, you can create one — ask the agent to draft a versioned `<project>_Style_Profile.md` from a sample of your prior writing") that doesn't drag Andrea's three project-specific profiles into Plan 05's scope.

### W4.2 — Diff mechanism for branch-document-review

Re-evaluated the Compare API vs read-both-and-difflib decision now that sandbox `git` 2.43.0 is confirmed, which surfaced a third option: clone the user's research repo and run Andrea's exact `git diff` invocation. Built a reasoning matrix (round-trips, architectural fit, faithfulness to Andrea). **Recommended Option A — GitHub Compare API.** Reasoning: one round-trip, matches the REST-first commitment, faithfulness gap to Andrea is small (Compare API returns unified diff, same as her local `git diff`), and Option C's clone-state management problem isn't worth solving for a marginal faithfulness gain. Surfaced the Compare API's 300-file response cap as a future-extension cliff.

### W4.3 — Andrea's branch-document-review port spec

Read Andrea's `BranchWorkflow_Skill.md` end-to-end (178 lines, SHA `e0a736d` from 2026-05-02). Specified 10 keep-intact items (bracketed comments convention, Mode 1/Mode 2 distinction, comment-classification rules, light-vs-heavy proofreading, three-section report structure, "never push to main while branch open," "branches accumulate per project," pandoc regeneration step, LaTeX-conditional path, pptx-conditional path) and 5 adapt items (Step 4 diff mechanism per W4.2, branch-naming convention, provenance frontmatter, drop footer, strip Andrea/Marta/RA name references with role-generic substitutions). Noted that Andrea's Steps 1 and 6 already ship REST recipes verbatim, so no REST-adaptation banner needed. Flagged the `mmm-d` vs `YYYYMMDD` branch-naming question for port-time confirmation.

### W3.1 — add-paper retrofit spec

Read Andrea's `paper_processing.md` (320 lines) and the current `template/skills/add-paper/SKILL.md` (151 lines). The fold-in is **bigger than the original stub suggested** — it's a strict superset replacement, not an additive edit. Specified 9 deliverables: Step 0 triage, filename convention parameterization, replace Step 4 summary template with Andrea's dual-protocol (a)/(b)/(c)/(d) shape, add Summary Evolution Principle, add BibTeX step (new functionality, gated on `BIB_FILE`), `document_processing.md` pointer (aspirational — Wave 5 deferred), schema split between user-level and project-level (after Tier C decision), BOOTSTRAP.md interview update, dual provenance stamp. Three architectural issues surfaced and flagged: (a) three filename conventions floating around (Nori `AuthorLast_Year__short_description.pdf`, BOOTSTRAP smoke-test `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf`, Andrea `Author_shortTitle_year.pdf`); (b) file-structure mismatch (Andrea per-file vs Nori single-file) — resolved as a config knob with `single-file` as default; (c) Claude-status / User-status framework deferred as separate future work.

### Tier C decision — Option C (extend STATUS.md role)

Walked all four options with full reasoning. Picked Option C with these justifications: project params are config (not state), change rarely, full Andrea-pattern set is ~6 fields (fits comfortably); Option B's separation-of-concerns upside is mostly aesthetic at this scale; Option A breaks the upstream-shared SKILL.md model for a localization benefit most skills don't need; Option D leaves users re-explaining context to fresh agents indefinitely (the §1.5 tracker-not-past-chats failure mode). Sycophancy-checked the call: Option B is closer than the recommendation suggests, and if params proliferate to ~15+ fields the call should flip — re-evaluation trigger documented. Built the user-level vs project-level split table that retroactively cleaned up W3.1's schema deliverable (PROJECT_QUESTION / CONDITIONAL_SECTION / BIB_FILE / PAPERS_INDEX / paper_summaries.structure go in STATUS.md project params; paper_naming.* formats stay in personal_info.md). Enumerated five knock-on edits that bundle with W3.1 execution.

### Cleanup

- Plan 05 title and confidence updated from "(stub)" to fleshed-out state
- "Status: Fleshing out" → "Status: Fleshed out"
- Open questions section pruned (3 items resolved this session, 2 new ones added for port-time confirmation)
- W4.2 and Tier C statuses honestly framed as "Recommendation made" rather than "locked" — Dan can override before execution
- Parent-plans block updated: Plan 04 reference reflects that pandoc/python-docx/git were verified there
- Forward-reference to this convo file added under Originating convos

## Decisions Made

| Decision | Outcome | Override path |
|---|---|---|
| W4.0 probe scope | Confirm-only on pandoc; LaTeX/pptx/pypandoc deferred to on-discovery cadence | Run full probe if a port surfaces an unexpected dependency |
| W4.1 surface | Claude Code (CLI) — source files filesystem-only | N/A — source-access constraint is binding |
| W4.1 skill name (recommendation) | `iterative-writing-workflow` (Andrea's YAML name) | Dan can pick `writing-skill` shorthand at port time |
| W4.2 diff mechanism (recommendation) | Compare API (Option A) | Dan can pick B (difflib) or C (git clone) before W4.3 |
| W4.3 branch-naming (recommendation) | Keep Andrea's `mmm-d` per defer-to-Andrea | Dan can pick `YYYYMMDD` for cross-convention consistency |
| Tier C placement (recommendation) | Option C — extend STATUS.md role | Re-evaluation trigger documented (if params >15 fields, switch to B) |
| `add-paper` filename default | Deferred to port time — three formats in play | Decide based on which conventions users in the wild already have |
| `paper_summaries.structure` default | `single-file` (preserves current behavior); per-file code path deferred until requested | Add per-file branch when first user wants it |

## Open Questions Remaining

- Andrea's AITaxBID kit may have evolved since 2026-05-09 (current SHA `e0a736d` from 2026-05-02). Re-check at port time.
- Default filename convention for `add-paper` — three formats in play, port-time decision.
- Branch-naming format for `branch-document-review` — `mmm-d` vs `YYYYMMDD`, port-time decision.
- After Plan 05 ships, should the `aitaxbid-skills-audit` branch be archived?
- The W4.2 Compare API recommendation and Tier C Option C recommendation both await Dan's explicit confirm-or-override before W4.3 / W3.1 actually execute.

## Process Notes

- **Convo-name handshake done early** — proposed `20260513_plan05_flesh_out.md` at session start and got tacit approval (no override). Different from yesterday where the handshake slipped to finish-convo time.
- **Main-sync check ran at session start** — `git fetch origin && git rev-parse main origin/main` confirmed `d4558dc` on both sides before any other work. The lesson from yesterday's push-rejected-because-14-commits-behind held.
- **Multi-terminal note** — `?? template/README.md` shows in git status at session start (same untracked file noted in yesterday's convo, still untouched per multi-terminal protocol).
- **Dan's pushback caught a soft option-text framing** — I offered "W3.1 might benefit from clear scope before the bigger Wave 4 ports," Dan asked "Why do you think W3.1 is needed before W4?" Honest answer was that I had no technical reason; it was procedural softening. Useful catch; the sycophancy-check discipline from RESEARCHER.md §0 worked as intended.
- **Sycophancy-self-check on Tier C** ran before locking the recommendation. Steelmanned Option B; identified the proliferation threshold that would flip the call; documented it as a re-evaluation trigger.
- **Did NOT use TaskCreate** — Plan 05 itself served as the de-facto checklist; adding harness tasks for a doc-editing session would have been redundant. Three system reminders about it ignored consciously.

## Suggested Next Session

Two natural paths:

1. **Execute W4.1 + W4.3 (the Tier A ports).** Both have full specs and are ready to run from Claude Code with filesystem access to Andrea's sources. ~45–90 min combined. Sequence W4.1 first (simpler), W4.3 second (Step 4 diff parsing + name stripping). W4.4 (SKILL_INDEX entry) and W4.5 (ship commit) flesh out at execution time.

2. **Execute W3.1 (add-paper retrofit) + Tier C knock-on edits.** Bundles the BibTeX addition, schema split, BOOTSTRAP.md interview update, and STATUS.md "Project parameters" section seed. ~45–60 min. Independent of Wave 4 — can run before or after.

Either path is fine; Dan picks. If Dan has appetite for both, run W4.1+W4.3 first (smaller surface area of new behavior; easier to verify).

---

## Continuation (later in same session) — `add-paper` scaling discipline + issue #4

After the update-docs checkpoint, Dan raised six adjacent items about `add-paper` that didn't fit W3.1's methodology-fold-in scope:

1. Multi-repo destination when the user has multiple research repos registered (e.g., a project repo + a general `knowledge_base`).
2. A "Beyond this summary" affordance — each PAPER_SUMMARIES entry calls out what's in the full paper but cut from the summary, so a reader can decide whether reading further pays off.
3. Tier thresholds for migration between single-file `PAPER_SUMMARIES.md` and per-file `papers/summaries/SUMMARY_*.md` structure.
4. Summary length guidelines — Dan proposed ~10% of paper length.
5. Lookup discipline — whether an agent has to read all of PAPER_SUMMARIES to find one entry, or can target-read.
6. Chunk delimiter convention.

Engaged substantively with each, with pushback in three places:

- **Multi-repo (1):** I initially proposed "ask when ambiguous." Dan's first response ("don't understand the question") prompted me to overcorrect to "default to session repo; honor explicit override; no auto-ask at all." Dan came back to clarify he actually concurred with "only ask when ambiguous" — my overcorrection had dropped a useful affordance. Final rule: default to session repo; honor explicit overrides; ask only when the destination is genuinely ambiguous (multiple research repos registered AND session isn't clearly scoped). Useful reminder that "I don't understand" doesn't necessarily mean "disagree" — pushback in the other direction would have been correct.
- **Length (4):** pure 10% breaks down on long monographs (a 150-page flagship at 10% would produce a 7.5K-word "summary"). Proposed a hard ceiling of ~2000 words; the Beyond-this-summary section (item 2) becomes load-bearing on long papers where the cap binds.
- **Tier thresholds (3):** Dan agreed Stage 1 (PAPER_INDEX only, no summaries) doesn't earn its complexity. Simplified to two stages — start at Stage 2, migrate to Stage 3 on first-of: 20+ papers, concurrent edit conflicts, single summary >3000 words.

For lookup discipline (5) + delimiters (6), Dan asked whether `## ` headings are grep-friendly enough to support targeted reading via `Read(offset, limit)`. Confirmed yes — `grep -n "^## " PAPER_SUMMARIES.md` returns all heading line numbers; the agent picks the target heading, reads to the next heading line. No explicit `-----` delimiter needed; the heading convention also yields stable markdown anchor links.

**Filed [issue #4](https://github.com/danparshall/claude_researcher/issues/4) — add-paper: scaling discipline.** Six items, acceptance criteria, sequenced after W3.1 (same SKILL.md, but scaling layer benefits from real user data before threshold calibration). Plan 05's W3.1 entry now links to issue #4 as a companion follow-on, and the Tracking-issues block at the top lists both #3 and #4.

**Process note:** the sycophancy-check on item 4 (pushing back on pure 10% with the long-monograph counterexample) and item 1 (Dan's correction to my over-cautious framing) worked the way RESEARCHER.md §0 intends — neither side just nodded. The "Beyond this summary" affordance is a genuinely new design contribution from Dan's framing.
