# claude_researcher — Plan 12: Orchestrator STATUS.md (implements #38)

**Written:** 2026-07-14, claude.ai web session (claude_researcher Project).
**Executes:** fresh session per Nori flow (plan-then-fresh-session); CLI recommended (audit-status validation runs are cheap there).
**Branch:** `orchestrator-status` (this plan lands on it; execution continues it; PR at the end).
**Tracks:** [issue #38](https://github.com/danparshall/claude_researcher/issues/38) (supersedes F5 from the 2026-07-06 audit shakedown). Closes #38 on merge.

## Why now

The design was locked 2026-07-07 and deliberately gated on dogfooding: the econ-impact migration shipped 2026-07-11 (`danparshall/econ-impact@6c238716`, 937 → 112 lines) and the model survived first contact — three `start-research-line` ceremonies, one full merge ceremony (PR #66, fresh 2-sentence Summary), one mid-flight merge-recipe execution (reconcile-authors, both in-body edits ported and grep-verified), partial-read order holding, Buckets B/C = 0. Dan's execution report on #38 (2026-07-11) also surfaced three audit-status defects that only a real migrated repo could expose. This plan universalizes the model and fixes those three.

## Design being implemented (locked — see #38 for rationale)

- STATUS.md records **research-line lifecycle only**: row added at line start (Purpose = 1 sentence, amendable at milestones); row moved to Archived at merge (Summary written **fresh** at close, 1 sentence, ≤2 if needed — never a stale copy of Purpose). Day-to-day records live in `RESEARCH_LOG.md`.
- **Sessions never write STATUS** in `branches` mode — only the two ceremonies do. `## Recent Sessions` is retired in `branches` mode; it survives in `main_only` mode (no line lifecycle to hang events on) with a hard cap.
- **Partial-read convention:** STATUS section order is metadata + how-to-read header → `## Current focus` → `## Active Research Lines` → everything else; session-start reads only through the end of the Active table unless the task requires more.
- Recency is **derived, not stored**: `git for-each-ref --sort=-committerdate refs/remotes/origin`.

## Bite-sized tasks

### Phase A — RESEARCHER.md

1. **§2c partial-read.** Replace the whole-file `view /home/claude/<REPO>/STATUS.md` step with: read from top through the end of `## Active Research Lines`; read further only when the task requires it (archived-line lookup, `## Project parameters` consumers, audits). Note explicitly that skills needing Project parameters read that section on demand — it moves below the fold.
2. **§2c boundary text** (the original F5 gap): one paragraph stating what belongs in STATUS (lifecycle rows, Current focus, parameters, open questions) vs RESEARCH_LOG (everything session-shaped), and that in `branches` mode sessions never write STATUS. Update §2c's description of expected STATUS contents (currently says "recent sessions") to describe both modes.
3. **§6 merge ceremony** (line ~452): change "append a row" to **move** the line's row from Active to Archived; Summary written fresh at close (1 sentence, ≤2 if needed), Material must be a resolvable reference (dir, file, results path, or PR link — per the signed Q5 convention). Add the grep-verify habit for any content the branch ported.
4. **Recent-Sessions sweep** of RESEARCHER.md: remove/mode-split every remaining assumption that the section exists (session-start expectations, §5 references if any).

### Phase B — skills

5. **update-docs step 5 mode-split** (SKILL.md:107–111): `branches` mode → the session summary goes into the RESEARCH_LOG entry; do NOT edit or stage STATUS.md. `main_only` mode → keep the one-liner, hard-capped at ≤2 lines with a link out; detail lives in the log/convo doc. Update the commit-staging list to match.
6. **finish-convo:** staging list + delegation note consistent with 5 (it invokes update-docs; make the override structural, not a per-repo exception).
7. **start-research-line:** Purpose already specced as one sentence — add "amendable at milestones"; confirm newest-first row placement; if the target STATUS lacks the how-to-read header, offer to add it (migration on-ramp for older repos).
8. **audit-status** — the three defects from Dan's #38 execution report, plus the original F5 items:
   a. **Bucket D:** verify the Archived row's *Material reference resolves* (dir, file, results path, or PR), not that `docs/historical/<topic>/` exists. Fixes 27 false positives on econ-impact.
   b. **Bucket A carve-out:** suppress the finding for branches annotated as classified-for-deletion in Known issues or a referenced worksheet; report them once under a "pending deletion" list instead of re-flagging every audit.
   c. **Bloat heuristics:** in `branches` mode, the *presence* of `## Recent Sessions` is itself a finding (suggest migration); the ">20 entries" heuristic applies only in `main_only` mode. Recalibrate line-count hints for the orchestrator era (see Q1).
   d. **New checks:** section order matches the partial-read convention; oversize Purpose (>1 sentence) / Summary (>2 sentences) as soft flags.
   e. **CLI-mode preflight** note (from original F5): the skill assumes a local clone; say so up front and fail gracefully on web-degraded mode.
9. **SKILL_INDEX.md:** update the one-line descriptions where behavior changed (update-docs, finish-convo, audit-status).

### Phase C — seeds and onboarding

10. **BOOTSTRAP.md / STATUS skeleton:** wherever new-repo STATUS is seeded, emit the orchestrator skeleton (how-to-read header, Current focus, Active table, Archived table, mode-appropriate extras). If no seed exists as a file, add `template/templates/STATUS.md.template` (both modes) and point BOOTSTRAP at it.
11. **README / onboarding touch:** one paragraph on the model where the workflow is described, if such a description exists (implementer greps).

### Phase D — validation

12. **Live-repo validation:** run the revised audit-status against econ-impact (already migrated, already conformant). Expect: Bucket D false positives 27 → 0; the 7 deletion-pending branches suppressed; zero Recent-Sessions findings; section-order check passes; no new false positives.
13. **main_only fixture:** minimal STATUS with a capped Recent Sessions; verify update-docs' main_only path and audit-status' entry-count heuristic still fire, and no branches-mode findings leak in.
14. PR from `orchestrator-status`; body links #38 and this plan; #38 closes on merge.

## Testing plan

After Phase B: dry-read each edited SKILL.md as a fresh agent would — no step should instruct a STATUS write outside the two ceremonies in branches mode. After Phase D: the econ-impact run is the acceptance test; its expected deltas are enumerated in step 12 and any deviation is a finding about *this plan*, not about econ-impact.

## Questions for Dan

**Sign-off 2026-07-14 (Dan, in-session): LGTM, proceed — all four defaults below approved as written.** Q1: flag >200 / firm >300. Q2: ≤20 entries, ≤2 lines each. Q3: audit-status yes, session-start no. Q4: this repo keeps Recent Sessions under the main_only cap, no migration. Executing in the same claude.ai session (Dan's call, overriding the fresh-session default).

1. **Bloat numbers for the orchestrator era:** old hints were 200 lines / 20 sessions. Proposal: flag > 200 lines, firm finding > 300 (econ-impact sits at ~112–114 with 16 active lines). Original F5 said firm at ~500 — that was calibrated to diary-era files. Confirm or adjust.
2. **main_only Recent Sessions cap:** proposal ≤ 20 entries retained, each ≤ 2 lines + link; older entries roll to a per-year archive file. Confirm.
3. **Derived recency:** should audit-status (or session-start) print a last-activity-per-line table from `git for-each-ref` as standard output? Cheap, useful, but adds noise. Default: audit-status yes, session-start no.
4. **This repo's own STATUS** is diary-style with Recent Sessions and is explicitly flat/`main_only`-shaped ("not a research project itself"). Default: it keeps Recent Sessions under the main_only cap and gets trimmed opportunistically, no migration. Confirm.

## Execution record (2026-07-14, same session as sign-off)

Phases A–D complete on this branch. Acceptance test (step 12) against econ-impact: **Buckets A/B/C/D all 0** after two validation-driven skill fixes that the plan didn't anticipate: (1) preflight must `git fetch --prune` — unpruned refs from econ-impact's Jul-11 deletion sweep produced 8 phantom Bucket-A flags; (2) valid Material types extended to globs and commit refs (2 false Bucket-D flags otherwise; both resolved in reality). Also added: bundle rows cover branches named in Summary/Material (Bucket C). Schema checks: no Recent Sessions, section order correct, 114 lines, no oversize flags, derived recency table produced. main_only fixture (step 13): presence-finding correctly silent, entry-count heuristic correct, oversize-entry flag fires on a 3-line entry. The 4 Known-issues deletion-pending locals are desktop-side only (origin already clean) — suppression logic verified against them pre-prune.

## What could change

- **Upstream Nori sync:** these files diverge further from the upstream Skillset; if Dan later pulls upstream changes to update-docs/finish-convo, this plan's mode-split is the likely conflict site. The PR description should name the diverged files for future syncs.
- **Other research repos:** any repo besides econ-impact using the old schema (e.g. `reproduction-task-exposure`, if it has a STATUS) will start flagging under the new audit-status Recent-Sessions presence check — that's intended (it's the migration on-ramp), but worth a heads-up line in the PR.
