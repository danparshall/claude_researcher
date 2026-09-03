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

- Skill: `template/skills/init-research-repo/SKILL.md` — updated this session (Tier 1)
- Skill: `template/skills/init-code-scaffold/SKILL.md` — created this session (Tier 2; also carries the Tier 3 doc note)
- Skill: `template/skills/add-deliverable/SKILL.md` — created this session (Tier 4)
- Skill: `template/skills/start-research-line/SKILL.md` — sibling; scaffolds per-branch `docs/active/<branch>/`
- Skill: `template/skills/finishing-a-research-branch/SKILL.md` — the natural home for a future opt-in `data/processed/<branch>/` → `data/processed/` promotion step (deliberately not touched this session; needs its own design)
- Manifest: `template/skills/SKILL_INDEX.md` — updated to register the two new skills
- Reference: [Cookiecutter Data Science opinions](https://cookiecutter-data-science.drivendata.org/opinions/) — the data-lifecycle model this session adopts
- Existing gitignore reference: `~/code/policy-levers/.gitignore` — the mature CDS-aligned pattern the new default is modeled on
- Dan-specific infra (out of downstream scope): `~/.claude/CLAUDE.md` "Worktree data discipline" block; `using-git-worktrees` skill; `~/data/` Syncthing sync

---

## Addendum — 2026-09-03 (T2 + T3 + T4 continuation, same session)

Dan approved shipping T2/T3/T4 immediately after the T1 commit landed. Framework decisions and shipped artifacts:

**Tier 2 — `init-code-scaffold` skill (shipped).** Lazily-invoked repo-setup skill for research repos that start needing code. Creates `src/<pkg>/`, `scripts/`, `tests/`, `notebooks/`, `pyproject.toml`, `.python-version`, optional `.venv/`. Uses `uv` per the researcher-profile Python policy. Deliberately opt-in — the skill's "When to run this skill" section calls out that reading-heavy repos (`verification/` at the time of writing) should skip it entirely. Package name is asked-for rather than guessed (renaming is a real refactor once imports exist). `pyproject.toml` template pins Python 3.12+, configures ruff and pytest, uses `src/<pkg>/` layout so tests exercise the installed package rather than a shadow-imported working copy.

**Tier 3 — folded into `init-code-scaffold`'s "Data outputs from code" section (no standalone skill).** Documented decision: the `data/processed/<branch>/` convention is a *rule* about where derived data lives, not a ceremony worth reifying. The rule appears in the T2 skill because that's the surface where researchers are about to write code that produces the data in question — putting the guidance somewhere else would just mean it isn't read at the right moment. Promotion at merge time (`data/processed/<branch>/foo.csv` → `data/processed/foo.csv`) is explicitly manual and opt-in — not every branch's outputs are meant to leave the branch, and automatic promotion would risk polluting `main`'s `data/processed/` with branch-scoped artifacts that only made sense in their originating context. `finishing-a-research-branch` is the natural home for an eventual opt-in promotion step, but touching that ceremony (which contains the workflow's only merge affordance) needs its own design conversation triggered by real friction. Not this session.

**Tier 4 — `add-deliverable` skill (shipped).** Creates `deliverables/<target>/` with a seeded `LINEAGE.md`. Key design choices:
- **Merge-commit SHA pinning, not branch HEAD.** Branch names can be deleted or reused; merge commits are permanent. Rows for still-active branches carry `active` marker and are meant to be re-pinned at merge time.
- **Tiered rigor is explicit in the LINEAGE template itself** — Light format (claim + where-it-appears + source-with-branch-SHA) is the default; Fuller format (adds a runnable Method column) is the upgrade path for citable / defensible numbers. Both formats appear in the seeded LINEAGE.md as tables the researcher can populate incrementally.
- **The skill only scaffolds provenance, not the deliverable content itself.** Authoring the paper / memo / bill response is a separate flow (`iterative-writing-workflow` or `branch-document-review`, or plain writing). `add-deliverable` is the "cut the target and cast the lineage plumbing" ceremony that precedes writing.
- Target names follow a suggested prefix convention (`paper-`, `memo-`, `bill-`, `essay-`, `deck-`, `testimony-`) to keep `deliverables/` scannable.
- Chose to seed the Claims table with visible-but-commented example rows (`<!-- example: ... -->`) rather than filling it with placeholder data — pattern is discoverable without polluting the initial file.
- Which branch the deliverable dir lives on (`main` vs. a dedicated deliverable branch vs. a research branch) is explicitly a per-deliverable decision, defaulted to `main` since most deliverables outlive any single branch.

**Manifest update.** `SKILL_INDEX.md` gained entries for both new skills. `init-code-scaffold` slots into the Session-lifecycle group alongside `init-research-repo` (both are repo-setup, both are lazily-or-once invoked); `add-deliverable` slots into the Knowledge-management group next to `add-paper` (parallel shape: create-a-typed-thing-with-mandatory-metadata).

**What still isn't done, and is intentional:**
- **Fold into `finishing-a-research-branch`** — the LINEAGE.md re-pinning grep-check + optional `data/processed/<branch>/` promotion. Both worth adding; both need their own design pass. Recording as a follow-up.
- **`add-deliverable` sandbox affordance** — the runtime-detection block treats claude.ai sandbox and Claude Code symmetrically, but SHA-resolution via `gh pr view` might not be available in the sandbox. If a user hits this, resolve via the Pulls REST API instead. Not fixed pre-emptively; wait for the actual friction.
- **Operations-mode / campaign-mode archetype** for `policy-levers/`-style repos — still deferred until real retrofit pain surfaces a design brief.

---

## Addendum 2 — 2026-09-03 (T5 ship, same session)

Dan approved shipping T5 immediately after T2/T3/T4 landed. Skill created: `template/skills/audit-repo-structure/SKILL.md`.

**What T5 covers.** Guardrail enforcement — a filesystem-shape audit that walks nine finding buckets against the research-first framework's conventions and reports bucket-at-a-time. Modeled on the interaction pattern of `audit-docs` / `audit-papers` / `audit-status`: inventory, categorize, report, no auto-fix, one bucket at a time so the user's decision surface stays small.

**Nine buckets:**
- **A. Root sprawl** — `results/`, `output/`, `outputs/`, `reports/`, `analysis/`, `notes/`, `drafts/`, `sections/`, `tmp/`, `scratch/` at root. Fix depends on contents (writeups → `docs/active/<branch>/results/`, data → `data/processed/<branch>/`, deliverable outputs → `deliverables/<target>/`, scratch → gitignore + move).
- **B. Duplicate doc dirs** — `project_docs/`, `documentation/`, `_docs/`, `docs2/`, `wiki/`, `handbook/`. Fix: merge into `docs/`.
- **C. Workstream shadow taxonomy** — top-level dirs that look like workstreams/deliverables rather than kinds. Per-finding ask: research line (→ `docs/active/<name>/`)? Deliverable (→ `deliverables/<name>/` with LINEAGE.md)? Self-contained sub-project (accept)? **Operational-repo caveat explicit in the skill body** — a repeat pattern of "this is operational" exceptions here is the trigger to consider the deferred operations-mode archetype, and the skill's Step 5 surfaces that as a repo-shape observation rather than a per-finding fix.
- **D. Loose files at root** — PDFs, `.py` scripts, `.sh` scripts, `.md` handoffs, `.zip` archives, `.csv`/`.parquet`/`.json` data, images. Fix depends on file type; skill lists the mapping.
- **E. `data/` non-conformance** — missing subdirs, files directly in `data/` root, missing `data/README.md`, missing `.gitignore` block. Fix: point at `init-research-repo` (idempotent) + manual recategorization.
- **F. Partial code scaffold** — `pyproject.toml` without `src/`, `src/` without `pyproject.toml`, missing `__init__.py`, missing `.python-version`. Fix: point at `init-code-scaffold` or complete manually.
- **G. LINEAGE gaps** — `deliverables/<target>/` without `LINEAGE.md`, `Purpose: TBD` unresolved, empty Claims table despite shipped outputs, stale `active` branch pins. Fix: manual updates to LINEAGE (never wholesale rewrite of existing LINEAGE files).
- **H. Notebook rot** — informational heuristic (large notebooks, production-sounding names). Non-actionable by design; some notebooks are legitimately meant to stay in notebook form.
- **I. Standing exceptions** — enumerated list of files/dirs that should never be flagged (`README.md`, `STATUS.md`, `.venv/`, `.git/`, framework kinds, etc.). Deliberate design decision: **no persistent exception file** — re-audit each time so stale exceptions get re-considered.

**Design choices worth flagging:**
- **Operational-repo caveat is baked into the skill body, not tacked on as a footnote.** Bucket C's per-finding prompt explicitly says "if the user says the repo is operational, accept the exception," and Step 5's summary section surfaces "multiple Bucket C exceptions suggest operations-mode may be a better fit" as an explicit pattern to watch for. This turns the skill into a signal-collector for the deferred archetype decision rather than a pedantic checker.
- **No auto-fix, in line with the other audit-* skills.** Multi-session safety (another agent's worktree may have work in flight) + operational-repo judgment call + destructiveness of `mv` in the wrong direction all point the same way.
- **Bucket H is deliberately informational.** Pushing users to extract every large notebook is presumptuous; the skill flags but doesn't nag.
- **Commit-per-bucket** rather than one giant commit — makes reverting a specific fix cleanly possible.
- **Skill points at other skills** for fixes it can't complete alone (`init-research-repo` for Bucket E, `init-code-scaffold` for Bucket F, `add-deliverable` shape for Bucket G) rather than reaching into their territory.

**Retrofit runway.** The three existing research repos (`policy-levers/`, `verification/`, `econ-impact/`) are the natural first exercise targets. Ordering by likely-difficulty: `verification/` (smallest, cleanest — should be a light pass); `econ-impact/` (largest, most `results/`+`output/`+`reports/`+`analysis/` sprawl — will surface real Bucket A + Bucket D volume and probably some Bucket C findings around `RCT_KnowledgeUnbundling/`, `economist_AI_boom/`, `latam/`); `policy-levers/` (most Bucket C findings; strongest test of the operational-repo caveat — if the skill nags too hard here, the caveat needs to be sharpened). Each retrofit is its own session; the results of the three runs together are the empirical calibration for whether the guardrail buckets are hitting the right targets.

**Manifest.** `SKILL_INDEX.md` gained an entry in the Knowledge-management section, alongside `audit-docs`, `audit-papers`, `audit-status`.

**What's now cleared from the deferred list:**
- ~~Guardrail enforcement (Tier 5)~~ — shipped.
- ~~Operations-mode / campaign-mode archetype~~ — remains deferred, but now with a *signal-collection mechanism* in place (Bucket C exceptions accumulate as a pattern the audit surfaces).

**What's still deferred:**
- **Fold into `finishing-a-research-branch`** — LINEAGE re-pin grep + optional `data/processed/` promotion. Cold handoff briefing written: [`docs/lineage_finishing_branch_handoff.md`](../lineage_finishing_branch_handoff.md).
- **`add-deliverable` sandbox affordance** — REST-API SHA-resolution fallback. Tracked: [issue #56](https://github.com/danparshall/claude_researcher/issues/56) (`task`).
- **Operations-mode archetype** — waiting on retrofit pain + accumulated Bucket C exception patterns from real `audit-repo-structure` runs. Tracked: [issue #57](https://github.com/danparshall/claude_researcher/issues/57) (`parking-lot`).
- **Retrofit the three existing research repos** against the new framework — one session per repo, in the order `verification/` → `econ-impact/` → `policy-levers/`.
