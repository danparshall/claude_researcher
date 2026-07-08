# Verify-affordance edit + STATUS hygiene skills

**Date:** 2026-07-08
**Repo:** `claude_researcher` (meta dev repo, flat `docs/`)
**Main:** advanced `1ade554` → `7696e63` (three commits from this session, plus one from a concurrent agent at the end)

## Summary

Session had two distinct arcs. The first was a follow-up to the 4.8 refusal problem the previous session tried to fix via tone-editing (`dddf518`). Dan pasted a real transcript showing 4.8 still refused, quoting the very tone-edit language back at him as evidence of suspicious framing ("designed to live in this Project Instructions context" = attacker cover story). Initial diagnostic: my edit backfired. Dan corrected: it didn't backfire, it was replaced substrate — 4.8's refusal is anchored at workflow-shape level, and it generates plausible-looking excuses from whatever text is present. Excuses rotate, refusal doesn't. That reframed the problem: tone-editing has a low ceiling because 4.8's disposition doesn't dissolve on better wording. The honest fix is the stop-gate (already in BOOTSTRAP.md at `fcf1c0c`, but not in the runtime `_PROJECT_INSTRUCTIONS.md.template`), or accepting that 4.8 is unsupported. Dan then proposed a different direction: instead of reassuring, give 4.8 an *epistemic tool* — WebFetch RESEARCHER.md as a verification affordance before running it. That reshapes what the workflow *offers* (an affordance to look before acting) rather than how it *talks* (justifying trust). Landed as `af8cbda`.

Second arc was Dan raising a STATUS.md discipline concern that grew into two skills. He wanted new-branch creation to automatically produce a STATUS.md entry, because "if it's not listed, agents won't always check to see what's there" — `ls docs/active/` is not part of session-start, so any active line missing from STATUS is invisible to future sessions. Shipped `start-research-line` skill (`7d4607b`) bundling four artifacts atomically: STATUS Active table row (on main, pre-branch per Dan's ordering call), branch cut, `docs/active/<branch>/` scaffold, seeded RESEARCH_LOG.md. Then Dan asked for the companion repo-hygiene skill for existing drift: shipped `audit-status` (`7696e63`) with four finding buckets (A: unmerged missing from Active; B: Active row with no branch; C: merged missing from Archived; D: Archived row with no historical dir) plus soft bloat heuristics. Interaction model matches `audit-docs` — one finding at a time, no batching.

Between the two arcs, closed issue #37 (the tone-check ticket) with a summary comment that includes the bonus "PAT threat model" paragraph as FYI for future escalation — which after the 4.8 transcript we agreed would probably make things worse, not better.

## Topics Explored

- **PAT tone-check review** — three findings across `_PROJECT_INSTRUCTIONS.md.template:11` (credentials bullet), `RESEARCHER.md §7` ("under any framing, ever"), `BOOTSTRAP.md §Token handling`. Landed as `dddf518`. Follow-up transcript showed 4.8 still refused.
- **"Excuses rotate" reframe** — Dan corrected my "backfired" diagnostic. The tone edits didn't cause the refusal; they supplied new quotable substrate to a refusal that's anchored elsewhere. Implications: doc-tone edits have a low ceiling for 4.8; either accept the friction or gate.
- **Runtime-path 4.8 stop-gate gap** — BOOTSTRAP.md has the stop-gate (`fcf1c0c`), but `_PROJECT_INSTRUCTIONS.md.template` doesn't. Runtime sessions on 4.8 fall into the argue-cycle instead of hitting a clean gate. Not fixed this session; would be the "honest fix" if 4.8 support becomes a design goal.
- **Verification-affordance reframe** — Dan proposed: give the agent an epistemic tool (WebFetch RESEARCHER.md before running it) instead of asking for trust. Reshapes the workflow's affordance, not its rhetoric. Landed as `af8cbda`.
- **§Ordering rule tightening** — "before any other tool calls" (broad, suspicious-shaped) → "before any actions that touch the user's repos" (narrower, more accurate). `conversation_search` / `recent_chats` reframed from "should not be called" to "generally not useful at session start."
- **STATUS.md as canonical inventory** — Dan's core discipline point: STATUS is the file every session reads; anything not in it is effectively invisible. New research lines need STATUS entries at creation, not as follow-on.
- **Pre-branch STATUS ordering** — for `start-research-line`, update STATUS on main *before* cutting the new branch. Main's STATUS always current; branch-cut failure trivially reversible.
- **Skill vs runtime-rule for coupling** — a runtime rule in RESEARCHER.md §3 would be skippable; a skill is a single ceremony that either runs or doesn't. Chose skill (Y over X) to enforce atomicity.
- **`audit-status` scope + interaction model** — cross-check STATUS against branch state, one finding at a time, no batching. Soft bloat heuristics (~200 lines / ~20 sessions / ~30 lines) as calibration hints, not rules. Requires clone-first mode; stops cleanly in degraded REST fallback.

## Provisional Findings

- Tone-editing docs to reassure 4.8 has a low ceiling — 4.8's refusal is at workflow-shape level, and it will find *something* to quote as suspicious. My earlier "backfired" reading was wrong (Dan corrected: the specific text I added was replaced-substrate, not causation), but the strategic implication holds: iterating tone-edits for 4.8's sake is not converge-able.
- Affordance changes (WebFetch as verification path) may have a higher ceiling than tone changes because they address the *category* of 4.8's objection ("I can't verify the frame") rather than a specific quoted phrase. Untested — Dan will pilot; may still fail if the PAT itself is the trigger.
- STATUS.md drift is a real risk without a coupling mechanism. The pre-existing convention was "branch creation writes RESEARCH_LOG; STATUS updated when convenient" — that's the drift channel. Bundling the STATUS entry into the ceremony (`start-research-line`) closes it prospectively; `audit-status` handles retrospective repair.
- The `init-research-repo` seed was missing an Active Research Lines table entirely (only had Archived). That's an underlying reason the new-line flow had nowhere natural to write. Fixed as part of `start-research-line`'s prep — new repos ship with both tables, and the skill also handles append-if-missing for existing repos.

## Decisions Made

- **Reverting `dddf518`: not doing.** My "backfired" argument was wrong per Dan's correction. The tone edits are mild positives on 4.7 and neither positive nor negative on 4.8.
- **Bonus paragraph ("PAT threat model" for `RESEARCHER.md §2`): definitely not doing.** More reassuring text = more excuse substrate for 4.8. Preserved in issue #37's closing comment as FYI-only.
- **4.8 runtime stop-gate: not fixed this session.** Flagged as the honest fix if runtime 4.8 support becomes a design goal; deferred.
- **Skill vs runtime-rule for start-research-line: skill (Y).** Rationale: runtime rules are skippable under confirmation-gate fatigue; skills are single ceremonies with `<required>` steps.
- **Pre-branch STATUS ordering: yes.** Main's STATUS always current; branch-cut failure trivially reversible.
- **`audit-status` requires clone-first mode: yes.** REST fallback for merge-checking is expensive and error-prone; would produce misleading findings. Stop cleanly instead.

## Results

Landed on `main`:

- `dddf518` — `templates: tone-check PAT framing for 4.8 refusal reflex` (three files: `_PROJECT_INSTRUCTIONS.md.template`, `RESEARCHER.md §7`, `BOOTSTRAP.md §Token handling`)
- `4606512` + `1ade554` — repin pair for `dddf518`
- `af8cbda` — `_PROJECT_INSTRUCTIONS.md.template: WebFetch as verification affordance` (session-start reshape + §Ordering rule tightening)
- `f1cfcad` + `dd5598d` — repin pair for `af8cbda`
- `7d4607b` — `start-research-line skill: bind STATUS.md Active table entry to new-line ceremony` (new skill + `init-research-repo` seed extension + `RESEARCHER.md §3` collapse + `SKILL_INDEX.md` register)
- `7696e63` — `audit-status skill: cross-check STATUS.md against branch state; flag bloat` (new skill + `SKILL_INDEX.md` register)

Related non-code artifacts:

- Issue #36 (2026-07-04): grab-bag of user-facing explainers + tool ideas, fires 2026-07-12.
- Issue #37 (2026-07-04): closed 2026-07-04 with the tone-check summary + FYI on the bonus paragraph.

## Open Questions

- **Does the verification-affordance edit (`af8cbda`) actually reduce 4.8's refusal rate?** Untested. Dan will pilot. Expected outcome: partial — addresses one named concern ("can't verify the frame") but the PAT is still present and may still trigger. If it doesn't help, the honest next step is adding the runtime 4.8 stop-gate to `_PROJECT_INSTRUCTIONS.md.template`.
- **Should `finishing-a-research-branch` (currently absent as a skill, wrap-up lives in `RESEARCHER.md §6`) be reified as a skill too, matching the `start-research-line` pattern?** Not raised this session. The wrap-up flow currently does the archive move (`docs/active/` → `docs/historical/`) inline via `RESEARCHER.md §6`. Would need the same "guarantee STATUS moves too" coupling that `start-research-line` provides — `audit-status`'s Bucket C surfaces the drift retrospectively, but doesn't close the source.
- **STATUS.md's Recent Sessions bloat.** This repo's own STATUS has extremely long per-session detail blocks (see the 2026-06-07→06-09 entry). If Dan applies `audit-status` here, the bloat heuristics will flag `## Recent sessions` — is the flag correct? The section serves a real purpose (dogfooding decisions with full context), but crosses the "dashboard" threshold. Judgment call for Dan when he runs the audit.

## Housekeeping

- `template/scripts/resolve_append_conflict.py` was untracked at session start; got committed by a concurrent agent at `878a49d` right around when finish-convo was invoked. Not touched by this session.
- Feature branches from this session (`webfetch-verification-affordance`, `status-active-lines-skill`, `audit-status-skill`) are all now equal to `main` post ff-merge; safe to delete.
