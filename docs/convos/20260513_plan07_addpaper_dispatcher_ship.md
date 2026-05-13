# 20260513 — Plan 07 ship (add-paper dispatcher refactor)

**Date:** 2026-05-13
**Branch:** main
**Surface:** Claude Code (CLI)

## Summary

Execution session against Plan 07 (`docs/plans/07_add_paper_dispatcher_refactor.md`), written by the previous session (commit `3027ad7`). Plan 07 specified an architectural pivot from Plan 06's just-shipped unified `add-paper`: split the dual-protocol skill into a thin triage/dispatcher (`add-paper`) plus two per-protocol target skills (`paper-processing-academic` + `paper-processing-institutional`), with a uniform third dispatch branch reserved for the deferred Wave 5 `document-processing`. Plan 07 also picked up Andrea's institutional Step 2 rules (preserve acronym list verbatim, preserve boxes and figure captions with key data, strip decorative front matter) that Plan 06's "keep Step 2 as-is" decision had left out.

Plan 07 worked exactly as designed. All four deliverables (D1 academic skill, D2 institutional skill, D3 dispatcher refactor, D4 SKILL_INDEX update) landed on-spec. Single ship commit [`5ca183b`](https://github.com/danparshall/claude_researcher/commit/5ca183b) (4 files / +424 / -204), pushed to `origin/main`. Pre-flight source SHA verification (`git -C ~/code/AITaxBID diff --stat e0a736d HEAD -- skills/paper_processing.md`) returned empty — no drift since Plan 06's execution earlier the same day. The 10-check verification script ran clean after one mid-flight fix: a single "Protocol A paper" cross-reference in the institutional skill's naming-ambiguity edge case tripped Check 5, rewritten to "academic-style paper" to satisfy the partitioning constraint while preserving the cross-protocol routing hint.

Post-ship, agent surfaced the gap that `document-processing` (the dispatcher's third branch) doesn't exist yet and was only tracked inside Plan 02 Wave 5. Filed as [issue #6](https://github.com/danparshall/claude_researcher/issues/6) on Dan's request, modeled on issue #5's format. Andrea's source `~/code/AITaxBID/skills/document_processing.md` exists at 277 lines, last touched in `80803bf`; the port shape parallels `paper-processing-academic` and is mechanical (Andrea's source already draws the same paper-vs-document boundary that the dispatcher now formalizes).

## Topics Explored

- Plan 07 pre-flight reads (STATUS.md, README.md, Plan 07 itself, Plan 06 ship convo, current `add-paper/SKILL.md`, `SKILL_INDEX.md`, Andrea's `paper_processing.md` lines 180-260 for the Step 2 institutional enrichment + Step 4 Outlet column guidance + Notes-specific-to-Protocol-B routing hints)
- Source SHA verification: `e0a736d` byte-identical to AITaxBID HEAD `abd1c54` (same SHAs as Plan 06's execution — no drift between plans 06 and 07)
- D1 — new `template/skills/paper-processing-academic/SKILL.md` (181 lines; plan target 170-200): Protocol A subset of the unified add-paper lifted into a self-contained skill, renumbered Steps 1-6, Protocol A summary template + `@article`/`@unpublished` BibTeX only, schema back-pointer to dispatcher's Scope section, Common Mistakes scoped to Protocol-A failure modes
- D2 — new `template/skills/paper-processing-institutional/SKILL.md` (207 lines; plan target 190-220): Protocol B subset PLUS the institutional Step 2 enrichment (three rules verbatim per Plan 07 lines 226-232), Step 3 "Outlet" column guidance picked up from Andrea's lines 222-224, Common Mistakes adds "Reading only the executive summary" and "Stripping the acronym list during extraction"
- D3 — rewritten `template/skills/add-paper/SKILL.md` (101 lines, from 278; plan target ~80-100 — 1 over): frontmatter description revised to "Triage skill", TodoWrite shrunk to 2 entries, Scope enumerates the three dispatch targets, Step 0 triage content preserved verbatim from Plan 06 + Andrea's routing notes (Notes-specific-to-Protocol-B lines 244-249) folded into the borderline-case list, new Dispatch block at end of Step 0, Common Mistakes scoped to dispatcher-level only (added "Trying to do the full workflow in `add-paper`" anti-pattern per Plan 07 line 75)
- D4 — `template/skills/SKILL_INDEX.md` updated: `add-paper` description revised to describe the triage role; two new entries (`paper-processing-academic`, `paper-processing-institutional`) inserted after `add-paper` in the knowledge-management section
- 10-check verification: 9 clean on first run; Check 5 caught a single "Protocol A paper" reference in `paper-processing-institutional/SKILL.md:61` (naming-ambiguity sentence noting that an institutional author for what looks like a Protocol A paper should be flagged). Rewritten to "academic-style paper — go back through triage if so" — preserves the cross-routing hint without leaking the Protocol A label into the institutional file
- Post-ship discussion of "what's left for functional" — agent's honest answer prioritized empirical validation (no real beta session yet) over more porting, named `document-processing` (Wave 5) as the one branch in the just-shipped dispatcher that hits a wall, and issue #5 (style-profile meta-skill) as the only other live gap
- Issue #6 filed on Dan's request: "Wave 5: port document-processing skill (third dispatch branch from add-paper)" — medium priority, not blocking beta, source pinned to Andrea's `document_processing.md` at AITaxBID `80803bf` (277 lines)

## Provisional Findings

- Plan 07 worked the same way Plan 06 worked — no port-time decisions hit, no re-litigation, no scope creep. ~30 minutes from "Following Nori workflow..." to ship push, below the plan's 45-60 min estimate. The "decisions confirmed at design time (do NOT re-litigate)" block continues to be load-bearing: the section even had a "TodoWrite renumbering" entry pre-empting an obvious agent-side instinct (try to coordinate per-protocol TodoWrite blocks with the dispatcher's) that would have been wrong.
- Check 5's catch was educational: the partitioning constraint ("no Protocol A references in the institutional file") is stronger than just content-leak protection. The original sentence ("institutional author for a Protocol A paper") was a cross-routing hint, not content leakage, but the verification expects 0 because the per-protocol skills are supposed to be self-contained — agents reading them shouldn't have to know what "Protocol A" means. The rewrite ("academic-style paper") makes the file readable without the protocol-letter vocabulary. Worth keeping the partitioning constraint as written; the catch was real.
- Plan 07's split made the `document-processing` gap visible in a way Plan 06 didn't — Plan 06 mentioned `document-processing` as an aspirational Scope pointer, but Plan 07's Dispatch block makes the third branch a literal dispatch target in the routing code (the agent will read the Dispatch block, look at the branch, and find no skill exists). That visibility is what motivated issue #6 — the gap was always there, but Plan 07 surfaced it from a Plan-02-internal concern to a runtime-visible one.
- Dispatcher length came in 1 line over the 80-100 target (101 vs ceiling 100). Acceptable; the Common Mistakes section's three entries hit minimum useful length and trimming any one of them weakens the dispatcher's role as the canonical schema-location reference. Plan 07's target was a guideline, not a hard cap.
- Two harness reminders about TaskCreate fired during execution. This time I did use TaskCreate (10 tasks), unlike Plan 06's execution session (which deliberately skipped TaskCreate per yesterday's heuristic — "execution sessions where the plan doc IS the checklist don't need it"). Plan 07's deliverables and verification checks mapped 1:1 to discrete sub-steps, and the pre-flight + ship + verification + commit sequence had real ordering. The heuristic still holds — TaskCreate is value-added when the work has parallel branches or non-trivial sequencing, and the plan-doc-is-checklist case still wins when the plan is the linear sequence. Plan 07 just happened to fall on the value-added side.

## Decisions Made

- **Rewrite the "Protocol A paper" cross-reference in `paper-processing-institutional/SKILL.md:61`** to "academic-style paper — go back through triage if so." Preserves the routing hint (an academic paper with an institutional cover is a triage-redo case) without leaking the Protocol A label into the institutional file. Satisfies Check 5; reads more naturally for an agent invoking the institutional skill directly without dispatcher context.
- **Filed [issue #6](https://github.com/danparshall/claude_researcher/issues/6)** for the `document-processing` port. Medium priority, not blocking beta. Modeled on issue #5's format. No assignee (mechanical port, Dan-doable; not Andrea-gated like #5).
- **Did not push back further on Dan's "let's keep porting" framing** after the empirical-first argument was made twice (once in the post-Plan-06 convo, once in this session's "what's left for functional" exchange). Position registered, Dan's call is the dogfood + Plan 07 + issue #6 path, no value in further pressure.

## Results

No results files produced (execution session — no analysis outputs, no figures, no data summaries). The "results" are the shipped commit and the new issue.

## Open Questions

- **First beta session of the now-shipped skill set.** Plan 07 makes `add-paper`'s dispatcher cleaner; that's the most-used skill in the kit. Pending. The empirical question (does the Wave 2/3 REST-adaptation banner approach work at runtime?) remains untested.
- **Issue #6 (document-processing port)** — when to schedule. Not blocking beta but the dispatcher's third branch hits a wall until landed.
- **Issue #5 (style-profile meta-skill)** — Andrea-assigned. The apply-on-explicit-request affordance in `iterative-writing-workflow` references a skill that doesn't exist.
- **Issue #4 (add-paper scaling discipline)** — still post-empirical, gated on ~5 papers of real user data.
- **Issue #2 (convo-name environment indicator)** — small UX, not touched.
- **`raw.githubusercontent.com` allow-list miss at BOOTSTRAP Step 8** — still open; Step 9 falls back to cached WebFetch so non-blocking.
- **W4.0 pandoc spot-check** — still open, "do at next WebUI session" was the action.
- **`per-file` summary code path** — still forward-compat-only; both per-protocol skills carry the warning + fallback paragraph.
