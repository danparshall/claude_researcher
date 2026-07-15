# audit-status first-exercise + resolve_append_conflict.py landing

**Date:** 2026-07-06 (main work), follow-up 2026-07-09 (`resolve_append_conflict.py` commit), logged 2026-07-14
**Repo:** `claude_researcher` (meta dev repo, flat `docs/`)
**Main:** advanced `7696e63` → `878a49d` (one direct commit here; four commits landed on `econ-impact` cross-repo via `finish-convo`)

## Summary

First real-repo exercise of `audit-status` (shipped one day prior in `7696e63`). Cross-repo CLI session — rooted in `~/code/claude_researcher` (skill authoring context), but the audit target was `econ-impact`, Dan's first research repo and the one whose pain points shaped the workflow that `audit-status` enforces.

The shakedown produced two useful outputs. First, a full audit of econ-impact — 923-line STATUS.md, no `## Active`/`## Archived Research Lines` tables, all 35 merged branches unarchived, 14 of 23 unmerged branches lacking on-branch docs — followed by a schema-migration plan drafted via `write-a-plan` and landed at `econ-impact:docs/active/main/plans/20260706_status_migration_from_diary_to_dashboard.md`. Second, upstream findings for `claude_researcher` itself (F5, five sub-findings) captured here for future action.

The most important structural observation: the ~50 mechanical Bucket-A/C findings on econ-impact share one root cause — the researcher workflow was formalized after econ-impact was already established, and STATUS.md never got retrofitted to the newer schema `audit-status` enforces. The right response was a schema migration, not per-row fixes, which meant the skill's one-finding-at-a-time interaction model was structurally wrong for this case. `audit-status` should probably fast-fail with a "schema migration first" message when the STATUS schema doesn't match, instead of firing ~50 findings that share one cause.

Follow-up on 2026-07-09: committed `resolve_append_conflict.py` (`878a49d`) — a small helper for STATUS.md's Recent Sessions merge-conflict case (both sides append on top → keep both). Docstring gates safe usage. Not yet wired into any skill.

## Topics Explored

- **Cross-repo session mechanics** — running `audit-status` against a different repo than the CLI session was rooted in; using `git -C <path>` throughout instead of the SKILL.md's `/home/claude/${REPO}` assumption.
- **Repo shape-check as pre-audit** — six candidate research repos under `~/code`; only `lobby_analysis` had both Active + Archived Research Lines tables. Three others (including econ-impact) had partial structure. Dan chose econ-impact ("Right and Just" — the repo that begat the workflow should be the paradigm case for the audit).
- **Structural mismatch on econ-impact** — 923-line rolling diary, no schema, every merged branch un-archived (only `docs/historical/v4_prompt_design_march2026/` predates), two `docs/active/` orphans (`draft-cdr-v9-restructure`, `package-restructure`), no move-on-merge convention ever operationalized.
- **Artifact vs repo-plan misfire** — I initially drafted the migration plan as a claude.ai Artifact (URL `dda05f81-...`). Dan pushed back: plans belong in the repo per the workflow this audit is diagnosing. Rerouted via `write-a-plan` → `econ-impact:docs/active/main/plans/`. Same drift pattern the plan itself diagnoses.
- **`resolve_append_conflict.py` script** — small union-merge helper for STATUS.md-shape append-on-top conflicts (both sides added Recent Sessions entries; want both kept). Committed with docstring that gates safe usage; not wired into any skill yet.

## Provisional Findings — F5 sub-findings

- **F5.a — RESEARCHER.md §2c under-norms the STATUS ↔ RESEARCH_LOG boundary.** Current text: *"STATUS.md tells you what's currently active, recent sessions, the archived-research-lines table, and may contain a top-of-file `workflow_mode` field."* Never says *"diary detail belongs in RESEARCH_LOG, not STATUS."* Under-normed guidance is why econ-impact's STATUS grew to 923 lines over months without anyone flagging it. Proposed addition: explicit ~200-line target, explicit link-out convention, *"if STATUS is past ~300 lines, migration is overdue."*
- **F5.b — `audit-status` SKILL.md preflight assumes claude.ai sandbox.** Step 1 hard-codes `/home/claude/${REPO}/`. CLI mode wasn't handled — git ops work regardless, but the runtime-detection block classifies the environment then never actually branches on it. Portable fix: two-line branch in the preflight step.
- **F5.c — `audit-status` bloat threshold should sharpen.** Current: soft question at ~200 lines (*"is that fine, or should we look at what's driving the length?"*). Proposal: escalate to a firm finding above ~500 lines (2.5× target) — at that point drift is structural, not incidental, and the soft question stops being informative.
- **F5.d — `audit-status` doesn't gracefully degrade for non-schema STATUS.md.** When the schema is entirely different (no Active/Archived Research Lines sections), running the mechanical audit produces ~50 findings that share one root cause. Skill should detect this early (Step 3's parser) and stop with a *"schema migration first"* message + link to a companion migration skill, instead of firing 50 findings the user can't productively review one at a time.
- **F5.e — `resolve_append_conflict.py` sits unwired.** Docstring points at STATUS.md merges as the canonical case; no skill (`finish-convo`, a merge-time helper, etc.) actually calls it. Loose end — either wire it or delete it.

## Decisions Made

- **econ-impact migration plan** lives in econ-impact (`docs/active/main/plans/20260706_status_migration_from_diary_to_dashboard.md`), not in claude_researcher. The workflow-doc findings (F5) are what belongs upstream.
- **F5 disposition:** captured here + in econ-impact's plan's Phase 4. No GH issue filed yet — Dan can decide whether F5 warrants a plan, an issue, or gets rolled into the next skill-editing session.
- **`resolve_append_conflict.py` landed unwired** — deliberate. Wiring it into `finish-convo` or a merge-time helper is separate work that shouldn't gate the script existing in the tree. Loose end acknowledged, not resolved.

## Results

Landed on `main` (claude_researcher):
- `878a49d` — `resolve_append_conflict.py: union-merge helper for STATUS.md-shape append-on-top conflicts` (154 lines, one file, this repo).

Landed on `main` (econ-impact, cross-repo):
- `33641cde9` — `convo: 20260706_status_audit_and_migration_plan — audit-status shakedown, migration plan drafted` (four files: `STATUS.md` +2-line update, `RESEARCH_LOG.md` session entry, new convo, new plan).

Superseded artifact:
- `https://claude.ai/code/artifact/dda05f81-390a-4847-9e16-3c3dc8aace98` — first-cut migration plan as a claude.ai Artifact. Corrected by re-landing in econ-impact's `plans/` dir via `write-a-plan`. Recorded because the misfire itself was a live example of the drift the plan diagnoses.

## Open Questions

- **F5 disposition** — plan, issue, or absorb into next skill-edit session? RESEARCHER.md edit is small (~1 paragraph); `audit-status` edits touch preflight + bloat threshold + graceful-degrade — ~3 places, moderate scope. Issue is probably right; leaving Dan to file. **See post-pull note below — some of F5 may already be in flight.**
- **`resolve_append_conflict.py` wiring** — which skill invokes it, and does that require a new `finish-convo` sub-step or a separate merge-helper skill? Not decided.
- **Should `audit-status` grow a "schema-not-detected" fast-fail path?** F5.d says yes. Alternative view: this affects only pre-workflow-adoption repos (econ-impact is the paradigm case), so manual handling is fine and the mechanical audit's noise is acceptable. Depends on whether other users have pre-workflow STATUS.md shapes — probably at least one collaborator repo does (unclear which). **See post-pull note.**
- **Should a companion `migrate-status-to-schema` skill exist?** F5.d's "schema migration first" fast-fail would ideally link to a skill that automates the diary → dashboard migration. Would help future adopters. Scoped in the econ-impact plan's Implementation Details as a possible follow-up.

## Post-pull note (2026-07-14 — logged eight days after the shakedown)

Between the shakedown (2026-07-06/09) and this convo being logged (2026-07-14), `main` advanced by six commits that substantially overlap with the F5 findings above. Recording here so the two threads don't drift out of sync; substantive reconciliation is deferred to a follow-up session.

**What landed:**
- **`#39` merged** — `template_lite/` track shipped. New files: `template_lite/LITE.md` (lite-mode runtime spec, 123 lines), `template_lite/_PROJECT_INSTRUCTIONS_LITE.md.template` (35 lines). Commit messages signal design intent: *"standard skills usable on demand; never-list bans automatic overhead only"*, plus a "check for lite updates" affordance and a one-time setup section including a CLAUDE.md pointer.
- **`b2d5c5b`** (2026-07-14 STATUS entry) — Plan 12 written and EXECUTED same day (Dan sign-off w/ defaults). Touched RESEARCHER.md §2c/§6, four skills, SKILL_INDEX, BOOTSTRAP seed. **Explicitly validated against econ-impact and got Buckets A–D = 0**, which surfaced three defects in `audit-status` itself that got fixed in the same execution: `fetch --prune` preflight, glob/commit Material, bundle rows. Open **PR #40** on `orchestrator-status`: *"Orchestrator STATUS.md: lifecycle-only writes, partial-read convention, mode-aware audit (plan 12, closes #38)"*.

**Bearing on F5, on first read (not yet verified against the actual diffs):**
- **The econ-impact validation is the big one.** Plan 12's econ-impact run produced Buckets A–D = 0 — meaning either econ-impact's shape now passes `audit-status` under the new orchestrator/lifecycle-only/partial-read/mode-aware framing, or the migration plan I drafted at `econ-impact:docs/active/main/plans/20260706_status_migration_from_diary_to_dashboard.md` has been effectively obsoleted by a schema reframe that accepts pre-existing STATUS shapes rather than requiring migration. Either way, the econ-impact migration plan needs re-scoping against what plan 12 actually did before any of its Phases 2–4 execute.
- **F5.d (schema-not-detected fast-fail)** — likely addressed by *"mode-aware audit"*. The mechanism sounds different from F5.d's proposal (mode-detection vs. schema-mismatch-detection) but scratches the same itch.
- **F5.a (RESEARCHER.md §2c under-norms the STATUS ↔ RESEARCH_LOG boundary)** — plan 12 explicitly touches §2c and §6; the "lifecycle-only writes" + "partial-read convention" language sounds like it formalizes exactly the boundary F5.a called out. Worth diff-reading before assuming it's closed.
- **F5.b (CLI-mode preflight) and F5.c (bloat threshold)** — probably still orthogonal; plan 12's three surfaced fixes (`fetch --prune`, glob/commit Material, bundle rows) don't obviously overlap. Likely still uncovered unless the plan-12 mode-aware framing changes what "bloat" even means.
- **F5.e (`resolve_append_conflict.py` unwired)** — orthogonal.

**Next-session task if F5 is picked up:**
1. Read `template_lite/LITE.md`, `_PROJECT_INSTRUCTIONS_LITE.md.template`, and PR #40 diff + plan 12 + issue #38 — understand what "lifecycle-only writes, partial-read convention, mode-aware audit" actually means.
2. **Reassess the econ-impact migration plan.** If plan 12's mode-aware audit legitimately accepts econ-impact's shape, the 27-row migration table drafted 07-06 may be moot — the honest thing is to close the plan as superseded rather than execute against a schema that no longer applies. If parts are still relevant (e.g., the orphan reconciliation for `draft-cdr-v9-restructure` / `package-restructure`, or the TODO-to-issue conversions), rescope narrowly.
3. Reconcile F5.a and F5.d against what plan 12 shipped. File F5.b, F5.c, F5.e as issue(s) if still open.

Not attempted this session — filed as-is with this note so the shakedown findings and the plan-12 / lite-mode / orchestrator-status track don't drift as separate threads. The econ-impact reassessment is the highest-priority follow-up: writing a migration plan and *then* having the workflow's own audit skill say the target is fine as-is is exactly the kind of thing to catch before the plan gets executed.
