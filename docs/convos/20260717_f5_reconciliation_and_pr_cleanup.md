# F5 reconciliation post-plan-12 + PR #40 merge + PR #23 supersede-close

**Date:** 2026-07-17
**Repo:** `claude_researcher` (meta dev repo, flat `docs/`)
**Main:** advanced `574ef6f` → `c3d3d4e` (PR #40 merge)

## Summary

Three days after logging the 07-06 audit-status shakedown convo with a hedged "read plan 12 next session" Post-pull note, Dan asked for the reassessment. Read plan 12 (still on `orchestrator-status` branch since PR #40 hadn't merged); mapped the F5 sub-findings against what plan 12 shipped; verified the econ-impact migration executed successfully on 07-11 as `6c238716a` (STATUS 937 → 112 lines, still ~115 lines today with the new orchestrator schema); merged PR #40 with a real merge commit and closed PR #23 as superseded.

**Key correction to the shakedown convo's Post-pull note.** That note said plan 12 "likely obsoletes the econ-impact migration plan" — that was the wrong framing. The 07-06 plan wasn't obsoleted; it was the *seed* of plan 12. Trail: 07-06 plan drafted → 07-07 orchestrator-STATUS model locked → 07-08 Phase 1 sign-off complete (Dan, desktop) → 07-11 STATUS migration executed (`6c238716a`) + supporting work (TODO→issues #61–65, orphan resolution, verbatim sessions archive, merge-ceremony pilot via PR #66) → 07-14 plan 12 written and executed same-day, incorporating three defects that only real migrated-repo validation could surface → 07-17 PR #40 merged. The migration and the upstream generalization were sequential, not competing.

F5 sub-findings: four of five closed by plan 12. Only F5.e (`resolve_append_conflict.py` unwired) is still a live loose end.

## Topics Explored

- **Locating plan 12** — not on main yet (PR #40 open); on `origin/orchestrator-status` branch as `docs/plans/12_orchestrator_status.md`. 72 lines.
- **Plan 12's structure** — Phase A (RESEARCHER.md §2c/§6), Phase B (skills — `update-docs`, `finish-convo`, `start-research-line`, `audit-status`, `SKILL_INDEX`), Phase C (seeds/onboarding), Phase D (validation against econ-impact + `main_only` fixture).
- **Mapping F5.a–e against plan 12 delivery** — 4 of 5 closed:
  - **F5.a** (RESEARCHER.md §2c under-norms STATUS↔RESEARCH_LOG boundary) → Phase A steps 1–2 (partial-read + boundary text).
  - **F5.b** (`audit-status` CLI-mode preflight) → Phase B step 8e.
  - **F5.c** (bloat threshold sharpening) → Phase B step 8c + Q1 sign-off (flag >200, firm >300 — narrower than F5's original 500 proposal, calibrated for the orchestrator era where 100–150 is normal).
  - **F5.d** (schema-not-detected fast-fail) → *closed via reframe*, not the fast-fail I proposed. Plan 12 made the whole schema lifecycle-only + mode-aware, so *any* legitimate STATUS shape now audits cleanly and the fast-fail path became unnecessary. Cleaner solution.
  - **F5.e** (`resolve_append_conflict.py` unwired) → **still open.** Plan 12 doesn't touch it.
- **Econ-impact migration verification** — commit trail from `33641cde9` (my 07-06 shakedown convo commit) through `6c238716a` (07-11 migration exec) confirms all Phase 1–4 landed. STATUS.md on origin/main is 115 lines, 7 sections, matches the orchestrator schema. Three new active lines created 07-11 → 07-17 via `start-research-line` (`ceo-bot-legal`, `ceo-bot-reliance`, `latam-tax-base`) — model working.
- **PR #23 forensic** — 40-day-stale PR proposing template reorder. Structural comparison of PR #23's commit `18aa9db` vs current `origin/main`: identical section headers at identical line numbers. Body text on main is a richer version of what PR #23 proposed. Intent already fully landed via `dddf518` (tone-check) + `af8cbda` (WebFetch verify-affordance) + their repin pairs.
- **PR #40's validation-forced defects** — three fixes surfaced during Phase D that plan-writing didn't anticipate: `fetch --prune` preflight (unpruned refs from econ-impact's 07-11 deletion sweep were producing 8 phantom Bucket-A flags), glob/commit-ref Material types (2 false Bucket-D flags), bundle-row Bucket-C coverage. All rolled into skill fixes before the plan-12 execution record was written.

## Provisional Findings

- **F5 is 4/5 closed, cleanly, via the orchestrator reframe.** Not by patching audit-status' bucket logic; by rethinking what STATUS *is*. F5.d in particular is a stronger solution than what F5 originally proposed — the fast-fail path I described would still assume the researcher schema was the correct target and non-conformant repos needed migration. Plan 12 lets the schema *be* mode-aware, so pre-existing shapes (like `main_only` with capped Recent Sessions) audit cleanly without being "wrong."
- **PR #23's intent landed via smaller commits later.** Sometimes a 40-day PR is legit-just-slow, sometimes it's stale-because-the-territory-moved-underneath. PR #23 is the latter: same section headers, same intent, richer text — no net benefit to rebasing.
- **PR #40 merged with real merge commit** to preserve SHA-pin reachability (per the architecture-convention documented in PR #23's original merge note — the note outlived the PR it was in and still applies to any PR that touches template files). Issue #38 auto-closed.
- **F5.e wiring is genuinely non-trivial.** `resolve_append_conflict.py`'s canonical use case was STATUS.md's Recent Sessions section merge conflicts. Under the new orchestrator model, `branches` mode retires Recent Sessions from STATUS entirely — so the append-on-top surface at merge time has *shifted*, not disappeared. Likely candidates for the new surface: `## Archived Research Lines` table (two branches merged concurrently, both wanting to add rows), or `## Active Research Lines` table (two `start-research-line` invocations concurrently). Which skill invokes the helper depends on which surface is the real conflict site — needs a read of the new lifecycle-only §6 to see where merge-time conflict handling actually lives now.

## Decisions Made

- **PR #40 merged** (`c3d3d4e`, real merge commit). Closed issue #38 automatically.
- **PR #23 closed as superseded** with explanatory comment naming the specific commits that supersede it. Not rebased.
- **F5.e wiring deferred** to a separate session. Placement decision needs the new §6 read.

## Results

Landed on `main`:
- `c3d3d4e` — Merge PR #40 (plan 12 orchestrator STATUS + 4 skill updates + SKILL_INDEX + BOOTSTRAP seed).

Closed:
- **Issue #38** — superseded by plan 12 execution (auto-closed by PR merge).
- **PR #23** — superseded by intervening template edits (explanatory close comment posted).

Repo state at session close: zero open PRs on `claude_researcher`; local `main` at `c3d3d4e`, in sync with origin.

## Open Questions

- **F5.e placement.** The one still-live F5 finding. `resolve_append_conflict.py` sits committed but unwired. Under the new orchestrator model, append-on-top conflicts on STATUS.md have shifted from `## Recent Sessions` (retired in `branches` mode) to the lifecycle tables (`## Active`/`## Archived Research Lines`). Which skill should invoke the helper — `finishing-a-research-branch`'s merge-ceremony? A new merge-time helper skill? — depends on where the conflict surface actually is under lifecycle-only §6.
- **PR #23's merge-commit-preservation note as canonical convention.** PR #23's body carried an inline "**Merge with a real merge commit** so pinned commits stay reachable" instruction. That's a repo-wide convention rooted in the SHA-pin architecture, not a PR #23-specific fact. Worth promoting from PR-body convention to somewhere durable (RESEARCHER.md contributor notes? a `.github/PULL_REQUEST_TEMPLATE.md`?). Deferred; not this session.
- **Econ-impact plan follow-up.** The 07-06 plan doc at `econ-impact:docs/active/main/plans/20260706_status_migration_from_diary_to_dashboard.md` was iterated by desktop/other agents 07-07 → 07-08 → 07-11. It's presumably marked done in-repo (the migration executed), but a follow-up check on its Phase 4 items (GH issues #61–65 for TODOs — filed; upstream feedback via #38 — closed) would confirm the plan is fully retired.
