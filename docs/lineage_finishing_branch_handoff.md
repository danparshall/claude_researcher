# Handoff — LINEAGE.md maintenance in `finishing-a-research-branch`

**Written:** 2026-09-03
**Origin:** `docs/convos/20260903_repo_scaffolding_defaults.md` (deferred item; the framework session decided not to touch `finishing-a-research-branch` without a dedicated design pass)
**Merged basis:** [PR #55](https://github.com/danparshall/claude_researcher/pull/55) (real merge commit `19e4534`) — the five-tier scaffolding framework that shipped `add-deliverable` (Tier 4) with `LINEAGE.md` provenance conventions
**For:** the next agent (Claude Code, or Fable in a claude.ai web session) that picks up this follow-up

## What you're picking up

The scaffolding framework introduced `deliverables/<target>/LINEAGE.md` files that track which research branches fed each deliverable and where citable numbers came from. LINEAGE rows pin **merge-commit SHAs** (permanent) for merged branches and **HEAD SHAs + `active` marker** for branches that are still open at deliverable-creation time.

Two related follow-ups need to land inside the `finishing-a-research-branch` skill (`template/skills/finishing-a-research-branch/SKILL.md`) to close the maintenance loop:

1. **LINEAGE re-pin grep at merge time.** When a branch merges, any LINEAGE row across all deliverables that references that branch as `active` (with a HEAD SHA) needs to be re-pinned to the merge-commit SHA. Without this, LINEAGE files silently accumulate stale HEAD pins that will point at deleted refs once the branch is cleaned up.

2. **Optional `data/processed/<branch>/` promotion at archive time.** The framework's Tier 3 convention (documented in `template/skills/init-code-scaffold/SKILL.md` under "Data outputs from code") says derived data that only makes sense in a branch's context lives under `data/processed/<branch>/`. When a branch's outputs are meant for downstream consumption (other branches, deliverables), they should be promoted to `data/processed/` (dropping the branch subdir). The framework session deliberately kept this **manual and opt-in** — automation was rejected because "not everything a branch produces is meant to leave the branch." But the current manual affordance is "user remembers to `git mv` by hand," which isn't discoverable and won't happen reliably.

The two are separable — ship them independently if that keeps the design cleaner. Both belong in `finishing-a-research-branch` because that's the ceremony that runs at merge time.

## Why this needs its own design pass, not a same-session patch

`finishing-a-research-branch` contains the **workflow's only merge affordance** — the PUT to `pulls/<N>/merge`. Modifying anything around that step has outsized blast radius:

- **A LINEAGE re-pin bug could rewrite provenance rows across every deliverable in the repo** and land the corruption in the archived state. Provenance corruption is the exact failure mode LINEAGE is designed to prevent; introducing it via a maintenance bug would be a serious regression.
- **A data-promotion bug could `git mv` derived data to the wrong path**, breaking downstream code that imports from `data/processed/`, or clobber existing `data/processed/foo.csv` with a branch's version.
- **Interaction with the existing Step 1.5** (finish-convo + audit-docs — the checkpoint-and-audit interior added in [PR #51](https://github.com/danparshall/claude_researcher/pull/51)) needs thinking about — where in the sequence do LINEAGE re-pin and data promotion belong? Before merge, so their commits ride along on the branch? After merge, so they land on main? The answer isn't obviously the same for both.
- **`resolve-runtime-issue`'s push-race recovery** (`resolve_append_conflict.py`) currently understands STATUS.md's lifecycle tables. If the new steps write LINEAGE.md files across the repo, that's a new concurrent-write surface that may need equivalent handling.

None of these is a blocker; each is a real design consideration.

## What's decided (from the framework convo)

Do not re-litigate these unless you find concrete evidence they're wrong:

- **Merge-SHA pinning, not branch HEAD.** LINEAGE rows for merged branches always pin the permanent merge-commit SHA. This is the load-bearing correctness property.
- **Data promotion is opt-in per file, not automatic.** The user decides whether each `data/processed/<branch>/foo.csv` should be promoted; the skill offers the option, doesn't take it silently.
- **Tiered rigor for LINEAGE claims stays.** Light format (claim + where-appears + source-with-SHA) is the default; fuller format (adds runnable Method column) is the upgrade for citable/defensible numbers. Re-pinning affects both formats identically — only the SHA in the Source column changes, the Method column (if present) refers to the same regeneration command using the new SHA.

## Unknowns / design questions you need to resolve

**LINEAGE re-pin scope:**
- Grep across the whole repo (`find deliverables -name LINEAGE.md`), or only against deliverables that STATUS.md or some manifest declares as `active`/`draft`?
- Auto-apply the re-pin, or surface each match to the user for confirmation? (Auto is probably fine — SHA substitution is unambiguous and lossless.)
- What if a LINEAGE row references the branch but with an already-set SHA that's *not* the current HEAD? That means someone hand-pinned it earlier; probably leave alone and log the anomaly.
- What if the grep matches inside a Change log entry rather than an Input research lines row? Should not rewrite. Requires scoping the substitution to the right section.

**Data promotion scope:**
- Ask about promotion **before** the merge PUT (Step 3), or **after** the archive move (Step 4)? Before means promotion commits ride the branch; after means they land directly on main. Before is probably safer (the merge is the sync point), but ask about UX.
- What's the file list surface look like? `ls data/processed/<branch>/` and let the user pick? Show sizes? Show git-log for each file?
- Collision behavior: if `data/processed/<branch>/foo.csv` and `data/processed/foo.csv` both exist, promotion would clobber. Detect and stop.
- Should the skill also offer to *delete* `data/processed/<branch>/` files that the user says "don't promote"? Or leave them in the archived branch dir (which then lives forever on the merged-into-main history)? Design call.

**Interaction with `main_only` mode:**
- In `main_only` mode there's no branch merge — everything happens on main directly. LINEAGE re-pin doesn't apply (no branch to re-pin from). Data promotion may still apply (files that were written to `data/processed/<some-conceptual-branch>/` and now want to graduate). Or it may not — `main_only` mode probably doesn't have branch-scoped data dirs. Verify.

**Interaction with the `finishing-a-development-branch` skill (Dan's local):**
- That skill (`~/.claude/skills/finishing-a-development-branch/SKILL.md`) is what runs for code-shipping branches in the meta dev repo — including the branch that shipped LINEAGE itself. Does that skill need equivalent affordances, or is LINEAGE maintenance only relevant to the research-first ceremony? Probably the latter, but worth checking.

**Sandbox affordance:**
- Whatever REST recipes the design uses need to work in the claude.ai sandbox without `gh`. Same constraint as [issue #56](https://github.com/danparshall/claude_researcher/issues/56) (`add-deliverable` sandbox affordance) — worth handling both in the same design pass since they share the pattern.

## What to deliver

Model on the pattern used for the MCP-migration handoff (`docs/mcp_migration_briefing.md` on the `github-mcp-migration` branch): verification → design doc → code, on a dedicated branch.

**Branch:** cut something like `lineage-finishing-branch-maintenance` off `main`.

**Verification report** (short — a page or two): confirm the current state of `finishing-a-research-branch`, `resolve-runtime-issue`'s conflict handling, and any `data/processed/` conventions actually in use in the three research repos (`policy-levers/`, `verification/`, `econ-impact/`). Especially: are there any deliverables/*/LINEAGE.md files anywhere yet? If not, this ships against a zero-usage baseline and the design has more latitude.

**Design doc** (in `docs/convos/YYYYMMDD_lineage_finishing_branch_maintenance.md`): resolve the unknowns above. Explicitly close the LINEAGE-re-pin and data-promotion pieces as either "shipping together" or "shipping separately," with rationale. Include the interaction with `main_only` mode and the sandbox REST recipe shape.

**Code:** edits to `template/skills/finishing-a-research-branch/SKILL.md`. Slot the new steps into the existing numbered sequence (Steps 1, 1.5, 2, 3, 4, 5, 6). Likely places:
- LINEAGE re-pin: new Step 4.5, after the `git mv` archive move (Step 4) but before the STATUS row move (Step 5). Runs on `main`; commits the LINEAGE rewrites as a separate atomic commit.
- Data promotion: new Step 3.5, between merge (Step 3) and archive move (Step 4). Runs on `main` right after `git pull --ff-only origin main` gets the merged branch content locally; user picks the files; commits promotion as a separate commit before the archive move.

But: verify this ordering against the actual skill body — the numbering here is from memory and the current file may not match. Read `template/skills/finishing-a-research-branch/SKILL.md` before slotting.

**Companion updates**:
- `template/skills/SKILL_INDEX.md` `finishing-a-research-branch` entry description gets updated to mention the new steps.
- `template/skills/add-deliverable/SKILL.md` gets a Notes-section update: "when the branch you cited as `active` merges, `finishing-a-research-branch` will now re-pin your LINEAGE rows automatically" (replacing the current "worth doing a quick grep of LINEAGE.md files at branch-merge time" hand-waving).
- `resolve-runtime-issue` may need a new entry for LINEAGE-file merge conflicts if they turn out to be a concern.

## Success criteria

- LINEAGE re-pin runs against a real test case (a branch that a deliverable actually references as `active`) and produces exactly-right rewrites — no drift into Change log sections, no over-broad substitutions.
- Data promotion runs against a real test case (a branch that produced `data/processed/<branch>/*.csv`) and the user gets a clear per-file yes/no with a stop on collision.
- Both new steps have entries in `resolve-runtime-issue` for their likely failure modes (partial rewrite, push race, sandbox REST fallback).
- The merge affordance itself (`PUT /pulls/<N>/merge`) is untouched — the load-bearing invariant is that Step 3 remains the workflow's *only* merge, and nothing new happens between confirmation gate (Step 1) and merge (Step 3) beyond what Step 1.5 already does.
- Skill runs end-to-end in Claude Code and in claude.ai sandbox — both paths tested.

## Non-goals

- **Do not build an automatic branch-scoped-data promotion.** The convo explicitly rejected this. Every promotion is a per-file user decision.
- **Do not add persistent LINEAGE-maintenance state** (e.g., a `.lineage-cache/` or manifest file). Re-derive by grepping; keep the maintenance surface stateless.
- **Do not touch the merge-PUT itself.** Any new steps flank it, never modify it.
- **Do not conflate this with [issue #57](https://github.com/danparshall/claude_researcher/issues/57)** (operations-mode archetype). Operations-mode is a separate axis and shouldn't gate this work.

## Related material

- `docs/convos/20260903_repo_scaffolding_defaults.md` — the framework design record (main body + two addenda; deferred items list at the bottom of Addendum 2)
- `template/skills/add-deliverable/SKILL.md` — the skill that creates LINEAGE.md files; its "LINEAGE.md maintenance — the audit affordance" section describes the auditor's-eye view of what a properly-maintained LINEAGE looks like
- `template/skills/init-code-scaffold/SKILL.md` — carries the "Data outputs from code" section that defines the `data/processed/<branch>/` convention this maintenance step operates against
- `template/skills/finishing-a-research-branch/SKILL.md` — the skill you'll be editing
- `template/skills/resolve-runtime-issue/SKILL.md` — where any new failure-mode recovery recipes belong
- [Issue #56](https://github.com/danparshall/claude_researcher/issues/56) — sibling deferred item for `add-deliverable` sandbox affordance; same REST-fallback pattern applies to this work

## What you don't need to figure out from scratch

The framework session already thought through:
- Why LINEAGE lives on top-level `deliverables/<target>/` rather than under `docs/active/<branch>/deliverables/` (deliverables outlive branches; multiple branches feed each deliverable)
- Why the light/fuller tiering exists (match rigor to stakes; avoid maintenance theater for values nobody will defend)
- Why merge-SHA pinning is non-negotiable (branch HEAD SHAs get deleted when branches are cleaned up)
- Why data promotion is opt-in per file (branch-scoped outputs are often meaningful only in the branch's original context)

Those are settled. This handoff is about the mechanism, not the philosophy.
