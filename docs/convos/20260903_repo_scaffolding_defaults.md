# Repo scaffolding defaults — code, data, deliverables, gitignore

**Date:** 2026-09-03
**Branch:** `repo-scaffolding-defaults`
**Machine:** Dans-MacBook-Pro

## Summary

Dan flagged that the `claude_researcher` toolkit prescribes a folder structure for `docs/` (via `init-research-repo` + `start-research-line`) and for `papers/` (via `add-paper` + the paper-processing skills), but is **silent on everything else** — where code goes, how `data/` should be organized, what `.gitignore` should look like, where outward-facing deliverables live, and how to preserve provenance across the research lines that feed a deliverable. Asked me to survey what naturally emerged in his three real research repos (`policy-levers/`, `verification/`, `econ-impact/`) and propose a reasonable default framework.

Empirical scan surfaced three signals: (1) **`data/`, `docs/`, `papers/` are universal** across all three repos; (2) **code-side dirs (`src/`, `scripts/`, `tests/`, `notebooks/`, `config/`) are common but not universal** — missing in `verification/` because it's reading-heavy, not code-heavy; (3) **the mess is in what didn't have a convention** — `econ-impact/` has `results/` + `output/` + `reports/` + `analysis/` + `notes/` + `drafts/` + `sections/` at root (semantic-overlap dirs that grew one `mkdir` at a time); `policy-levers/` has per-workstream top-level dirs (`bills/`, `essays/`, `us_china_council/`, `leave-behinds/`) that constitute a shadow taxonomy competing with `docs/active/<branch>/`; all three have root-level accumulation of PDFs, handoff notes, one-off scripts, and screenshots.

Dan's key adds during discussion: (a) [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/opinions/) has the right instincts, especially `data/raw/` being gitignored by default; (b) his own machine syncs `data/` through `~/data/` via Syncthing — that's Dan-specific infrastructure, **not** for the downstream default; (c) worktree-data-symlink handling already exists in Dan's `~/.claude/CLAUDE.md` and gets applied via `using-git-worktrees` — also Dan-specific; (d) `deliverables/<target>/` beats `docs/active/<branch>/deliverables/` because deliverables typically draw on **multiple** research lines and outlive any single branch — but this means **a lineage file is mandatory**, or else the "Section 2 says value X — can you confirm?" question becomes unanswerable; (e) `policy-levers/` might genuinely be a different archetype (operational/campaign-driven rather than research-question-driven) and could deserve a distinct scaffolding — but nailing that down should wait until the pain of retrofitting `policy-levers/` to the research-first default is felt for real.

Ship scope agreed: **design doc + `init-research-repo` update for Tier 1** (data/ subdirs, data/README.md, .gitignore). Tier 2 (code scaffold), Tier 4 (deliverables + LINEAGE.md), and the operational-repo archetype are deferred to follow-up sessions.

## Topics Explored

- What emerged empirically in `policy-levers/`, `verification/`, `econ-impact/` — universal dirs, near-universal dirs, semantic-overlap dirs, per-workstream top-level dirs, root-level accumulation.
- The core design tension: **"kind of thing" axis** (`src/`, `data/`, `docs/`, `papers/`) vs. **"workstream / deliverable" axis** (`bills/`, `latam/`, `us_china_council/`). `docs/active/<branch>/{convos,plans,results}` picked kind-primary, workstream-secondary, and that works — but when a researcher makes their first top-level `bills/` folder, they invent a workstream-primary shadow taxonomy that then competes with `docs/active/bills/` and the split-brain never gets resolved.
- Where the framework belongs: `init-research-repo` currently only scaffolds `docs/`. Extending it to also scaffold `data/`, `.gitignore`, and (eventually) `deliverables/` + a code hint is the right home — this is the entry point every new research repo already hits.
- Cookiecutter Data Science adoption: raw/interim/processed/reference lifecycle; `raw/` immutable; analysis as a DAG (blow away `interim/` + `processed/` and regenerate from `raw/` + code); notebooks are for exploration, stable code migrates to `src/<pkg>/`.
- Dan-specific vs. downstream-default distinction. Dan's `~/data/<repo>/` Syncthing sync and his worktree-data-symlink rule are infrastructure choices baked into `~/.claude/CLAUDE.md` and the `using-git-worktrees` skill. The downstream toolkit should stay silent on external-sync mechanisms and just leave a "document your sync arrangement here" pointer in `data/README.md` — so anyone can plug in Syncthing, S3, a shared drive, or nothing.
- Deliverables lineage design. `deliverables/<target>/` at repo root; each carries a required `LINEAGE.md`. Chose the **tiered** rigor model: default light (claim + where-it-appears + source-path + branch-SHA), upgrade the Method column (runnable command that regenerates the number) for values that will be cited externally or defended in Q&A. Matches rigor to stakes — the paper's headline number gets Method, the throwaway sanity check doesn't.
- Whether `policy-levers/` needs a distinct "operational" archetype. Provisional yes — it's a continuous stream of campaigns and deliverables, not a set of research questions with branches per hypothesis, and the `deliverables/<target>/` pattern fits most of what's at its root today. Deferred until the retrofit surfaces a concrete design brief.
- Naming caveat: `template_lite/LITE.md` already exists for the minimal web-only claude.ai bootstrap. Do not overload "LITE" for the operational archetype — better names would be `operations-mode`, `campaign-mode`, or `deliverables-first`.

## Provisional Findings

- **`init-research-repo` is the right home** for the scaffolding rules that every research repo needs. It already runs at repo init, is already idempotent, and already has the pattern of check-then-create. Adding `data/` + `.gitignore` fits its shape rather than requiring a new skill.
- **Kind-primary is the winning axis for the universal defaults.** `docs/`, `papers/`, `data/`, `src/`, `deliverables/` are all "kinds." Workstream (branch) appears as a sub-axis inside each kind where needed (`docs/active/<branch>/`, `data/processed/<branch>/` if the branch produces canonical data). Per-workstream top-level dirs are an escape hatch, not a default.
- **LINEAGE.md is the mechanism that makes `deliverables/<target>/` safe to promote across research-line boundaries.** Without it, a deliverable dir is just a bag of files, and the "which branch did this number come from?" question decays fast — branches get merged, deleted, renamed. Merge-SHA pinning in LINEAGE.md is what lets a future agent actually go look. The Claim table should scope to citable numbers, not everything, to avoid maintenance theater.
- **Cookiecutter Data Science's `raw`/`interim`/`processed`/`reference` split solves the semantic-overlap problem.** `econ-impact/`'s `results/` + `output/` + `reports/` + `analysis/` proliferation happened because there was no lifecycle vocabulary — every one of those dirs was a well-intentioned guess at where derived data + writeups go. With a named lifecycle, the guesses stop: derived data goes in `data/processed/`, derived writeups go in `docs/active/<branch>/results/`, and there's no `results/` at root.
- **`policy-levers/`-style operational repos may benefit from a different default**, but the empirical case isn't strong enough yet to design one blindly. Retrofitting `policy-levers/` to the research-first default first — and noticing which parts fight the operational shape — is the better path to a real archetype.
- **`.gitignore` should be seeded, not left to the researcher.** All three example repos have hand-rolled gitignores that evolved after data-scale pain; giving downstream users a working baseline avoids that same evolution. `policy-levers/.gitignore` is the mature reference — it already follows the CDS pattern.

## Decisions Made

- **`init-research-repo` updated** to scaffold Tier 1 in this session (commit landing in this branch):
  - `data/{raw,interim,processed,reference}/` with `.gitkeep` markers.
  - `data/README.md` seeded with the CDS convention, provenance stub, and optional "external sync" pointer.
  - `.gitignore` seeded (if missing) with Python + CDS-aligned data rules.
  - Step 1 check extended to look at `data/`, `data/README.md`, `.gitignore`.
  - Steps renumbered: old 3/4/5 → 5/6/7. Report text updated. Notes section extended to (a) allow `data/` to be skipped for pure-code or paper-only repos and (b) name deliverables + code scaffolding as explicitly out-of-scope-for-this-skill for now.
- **LINEAGE.md rigor is tiered.** Default: claim + where-it-appears + source-path + branch-SHA. Upgrade: runnable Method column for citable numbers. Written into the design doc; not yet in a skill (Tier 4 deferred).
- **Deliverables live at `deliverables/<target>/`** (top-level, kind-primary). Documented in the design doc; not yet scaffolded by any skill.
- **Guardrails documented but not yet enforced:** no root-level `results/`, `output/`, `reports/`, `analysis/`, `notes/`, `drafts/`; no `project_docs/` alongside `docs/`; per-workstream top-level dirs are an escape hatch. To be added to `init-research-repo`'s Step 1 warnings in a follow-up.

## Results

- **Skill update:** `template/skills/init-research-repo/SKILL.md` — Tier 1 additions (data/ scaffolding, data/README.md seed, .gitignore seed, renumbered steps, updated report + notes).
- **Design doc:** this file. Captures the full framework, empirical evidence, deferred items.
- **No new tests or scripts.** The skill is documentation-only; verification happens the next time a researcher runs it against a fresh repo.

## Open Questions

- **Tier 2 (code scaffold) — separate skill or extension to `init-research-repo`?** Arguments for a separate `init-code-scaffold`: not every research repo is code-heavy (`verification/` is a counter-example), keeps `init-research-repo` from feeling opinionated about Python. Arguments for extending `init-research-repo` with a "want code scaffolding?" y/n gate: one skill run at repo start, no discoverability problem. Punt until Tier 2 is designed.
- **Tier 4 (deliverables + LINEAGE.md) — new skill `add-deliverable`?** Would create `deliverables/<target>/` + seed `LINEAGE.md` from a template. Parallels `add-paper` and `start-research-line` in shape. Worth designing; not this session.
- **How does `LINEAGE.md` interact with a merged branch that gets renamed or force-pushed?** Merge-SHA pinning survives rename; force-push to a branch that a LINEAGE.md references would break the pointer, but force-push to a merged branch is unusual. Might warrant a mention in the LINEAGE.md template ("pin the merge-commit SHA, not the branch HEAD").
- **Operational archetype for `policy-levers/` — retrofit-first or design-first?** Leaning retrofit-first (feel the pain, then design). Real question: does Dan want to actually retrofit `policy-levers/` at some point, or is it fine as-is and this is only a hypothetical concern?
- **Should `add-paper` cross-reference `data/reference/`?** Paper appendix tables and code lists occasionally show up as reference data (ONET taxonomy in `econ-impact/`, e.g.). No current linkage between the two. Probably a "note it in `data/README.md`'s provenance section" answer, not a skill change.
- **Do the existing repos (`policy-levers/`, `verification/`, `econ-impact/`) want cleanup passes against the new framework?** Not in scope for this session. Would each be its own session (and `econ-impact/` in particular would be a real retrofit lift given the current data/results sprawl).

## Related

- Skill: `template/skills/init-research-repo/SKILL.md` — updated this session
- Skill: `template/skills/start-research-line/SKILL.md` — sibling; scaffolds per-branch `docs/active/<branch>/`
- Reference: [Cookiecutter Data Science opinions](https://cookiecutter-data-science.drivendata.org/opinions/) — the data-lifecycle model this session adopts
- Existing gitignore reference: `~/code/policy-levers/.gitignore` — the mature CDS-aligned pattern the new default is modeled on
- Dan-specific infra (out of downstream scope): `~/.claude/CLAUDE.md` "Worktree data discipline" block; `using-git-worktrees` skill; `~/data/` Syncthing sync
