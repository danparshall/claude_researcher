# Pre-Merge Gate: Hook Premise Fails, Ceremony Gap Fixed Instead

**Date:** 2026-08-19 (session ran into 2026-08-20 UTC)
**Branch:** pre-merge-hook
**Machine:** Dans-MacBook-Air
**Surface:** CLI

## Summary

Dan opened with: the §2.0b hook-install mechanism (tracked `template/hooks/post-commit` copied into the sandbox clone each session) seems to give us enforceable hooks for web agents — so install a *pre-merge* hook that forces the finishing ceremony (`finishing-a-research-branch` on web; the development/research pair on CLI) to run before any merge.

Investigation killed the premise. Merges in this workflow are not local git operations: the web ceremony merges via `PUT /repos/.../pulls/<N>/merge`, and CLI uses `gh pr merge` — both server-side API calls. No client git hook (`pre-merge-commit`, `pre-push`) ever fires on them, regardless of whether the sandbox honors hooks. Server-side enforcement was examined and rejected for structural reasons: in a solo-owner setup the agent wields the owner's PAT, so any branch protection strong enough to bind the agent must enforce against admins — and admin-enforced required status checks also block the direct-to-main pushes the workflow depends on (`start-research-line` STATUS writes, ceremony Steps 4–5 archive commits, all of `main_only` mode). Non-admin-enforced protection is a no-op against the owner PAT.

The investigation surfaced the actual defect: the web port of `finishing-a-research-branch` had **dropped the CLI ceremony's pre-merge interior**. CLI runs finish-convo → audit-docs → archive → PR → ask → merge; the web port went gate → PR → merge with no checkpoint and no audit, so a line could merge with its final session uncaptured. Fix shipped as **Step 1.5** (1.5a finish-convo, 1.5b audit-docs, both modes, before anything merges or archives), with the merge PUT's precondition stated in-text and a new Common-mistakes entry. Grep confirmed the merge recipe exists nowhere else in the kit, so gating the skill interior gates the workflow's only merge affordance — instruction-architecture enforcement, the honest ceiling on web.

## Topics Explored

- How web agents merge (Pulls REST API) vs. what §2.0b-installed git hooks can see (local commit/push only)
- GitHub server-side options: classic branch protection, rulesets, required status checks, merge queue — all founder on the solo-owner-PAT / direct-main-push conflict
- Enforcement-surface menu presented to Dan: (1) web skill Step 1.5, (2) `pre-push` side-door hook blocking locally-created merge commits to main, (3) CLI PreToolUse merge gate in dotfiles, (4) server-side ruleset. Dan selected (1) only.
- Cross-reference audit before renumbering: `resolve-runtime-issue` pins the ceremony's Steps 2/3 by number → fractional Step 1.5 chosen (house style: §2.0b, Phase 4.5)

## Provisional Findings

- Client-side git hooks cannot gate merges in this workflow — for web *or* CLI — because merges are API-side. This holds independent of the still-unverified question of whether the sandbox fires installed hooks at all.
- Hard server-side merge enforcement is structurally unavailable while the agent holds the owner's PAT and the workflow requires direct main pushes. The realistic threat model is a forgetful agent, not an adversarial one.
- The web `finishing-a-research-branch` port had silently lost finish-convo + audit-docs relative to its CLI parent — a port-fidelity gap worth remembering when auditing other ported skills.

## Decisions Made

- Ship Step 1.5 in the web ceremony (Dan's selection); skip pre-push side-door hook, CLI PreToolUse gate, and server-side ruleset.
- Fractional numbering (Step 1.5) to keep external step references stable.
- Drive-by fix, separate commit: `finish-convo/SKILL.md` referenced the CLI-only path `/Users/dan/.claude/skills/update-docs/SKILL.md`; now kit-relative `template/skills/update-docs/SKILL.md`.
- Consistency edits: SKILL_INDEX trigger line, RESEARCHER.md §6-area close-out summary and skill-dispatch entry now name the checkpoint+audit interior; RESEARCHER.md close-out text also gained "do not merge outside the skill."

## Results

- None (doc/skill edits are the deliverable). Commits on this branch: `4f9f35d` (Step 1.5 change set), `02fbf6c` (finish-convo path leak).

## Open Questions

- **CLI PreToolUse merge gate** (dotfiles `claude-hooks/`): the only option with real enforcement teeth — deny `gh pr merge` / merge-shaped API calls unless a ceremony sentinel exists. Declined for this branch; not yet captured as a dotfiles task (offered, unanswered).
- **`pre-push` side-door hook** (block locally-created merge commits pushed to main): cheap, narrow, unbuilt.
- Sandbox git-hook firing (post-commit auto-push) remains unverified by a fresh web session — irrelevant to merge gating, still relevant to §2.0b generally.
- Branch name `pre-merge-hook` is a mild misnomer for what shipped; fine to keep, but the PR title should say what it actually is.
- Port-fidelity audit of the other Wave 2/3 skills against their CLI parents: is finishing-a-research-branch the only one that lost required steps in translation?

## Addendum (2026-08-20) — close-out handoff

Post-checkpoint follow-up in the same session. Sync verified: `main` == `origin/main` at `9e44c73`, `pre-merge-hook` == origin at `0d9f35c`. A new branch `origin/flare-design` appeared from another session — not touched here.

Readiness assessment: branch is complete-shaped (full scope shipped, convo doc committed, nothing deferred onto it). Merge has deploy value — web runtime agents fetch skills raw from `main`, so the Step 1.5 fix only reaches real sessions once merged.

**Decision:** Dan hands the close ceremony to a fresh agent. Notes for that agent (`finishing-a-development-branch`):

- This repo has **no tests, no linters, no CI** — skill steps 1–5/7 are N/A by design (matches PRs #45–#49); don't go hunting for missed infra.
- Merge method: **real merge commit, not squash/rebase** — house convention for SHA-pin reachability (see STATUS.md notes on PRs #10, #40, #49).
- Repo layout is intentionally flat (`docs/convos/` + `docs/plans/`); there is no `docs/active/<branch>/` to archive — development-branch flow, not research-branch flow.
- At merge, optionally trim the "(on the branch until merge)" parenthetical from the 2026-08-19 STATUS.md Recent-sessions entry and note the merge/PR number there.
- Possible STATUS.md conflict surface vs `flare-design` is append-shaped (Recent sessions / Branch bullet).
