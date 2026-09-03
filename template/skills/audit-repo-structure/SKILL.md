---
name: audit-repo-structure
description: Check the repo's folder layout against the research-first framework's Tier 5 guardrails — semantic-overlap sprawl at root (results/, output/, reports/), duplicate doc directories, per-workstream shadow taxonomies, root-level accumulation of loose files (PDFs, one-off scripts, handoffs), data/ layout non-conformance, partial code scaffolding, and deliverable lineage gaps. Reports one bucket at a time; prompts the user for judgment rather than auto-fixing (some findings that look like violations in a research repo are appropriate in an operational repo).
---

## Runtime detection

Before following the rest of this skill, determine your environment:

```bash
if [ "$IS_SANDBOX" = "yes" ] || [ -d "/mnt/skills/public" ]; then
  echo "claude.ai sandbox"
elif [ "$CLAUDECODE" = "1" ]; then
  echo "Claude Code"
else
  echo "unknown — surface to user before proceeding"
fi
```

**If `claude.ai sandbox`:** the user's project repo is already cloned at `/home/claude/<REPO>/` per `RESEARCHER.md` §2.0b — run the `ls` / `find` / `git` commands in this skill directly from that working tree. Only if the §2.0b clone failed (degraded REST fallback, surfaced to the user) do you fall back to the GitHub Contents API to enumerate the tree — but note that this skill is much more useful with a real working tree since it inspects file sizes, mtimes, and contents. If you have to run it under degraded REST, warn the user that findings will be more limited.

**If `Claude Code`:** follow the skill body as-is.

**If `unknown`:** stop and surface to the user.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Inventory the repo top-level (files and directories) and classify each entry against the known-good set.
2. Walk the nine finding buckets in order (A through I); collect all findings before reporting.
3. Report findings one bucket at a time; do NOT auto-fix.
4. For each finding, ask the user whether it's a real violation or an intentional exception; act only on approved fixes.
5. Summarize what was surfaced, what was resolved, and what was accepted as exception.
</required>

# The Audit

Announce at start: "I'm using the audit-repo-structure skill to check the folder layout against the research-first framework's guardrails."

**Do NOT auto-fix findings.** The user may be running multiple parallel sessions; a "misplaced" file might belong to another agent's in-flight work. Also, some findings that look like violations in a research repo are the *right* shape in an operational / campaign-driven repo (`policy-levers/`-style). This skill reports; the user decides.

## Step 1: Inventory the repo top-level

```bash
ls -A .            # all top-level entries, including dotfiles
find . -maxdepth 1 -type d -not -path . | sort
find . -maxdepth 1 -type f | sort
```

Classify each top-level entry into one of three sets:

- **Known-good** — files/dirs that belong at the repo root (see the Standing Exceptions list in Bucket I below). Skip these; they're not findings.
- **Framework-required** — `docs/`, `papers/`, `data/`, plus (if code-scaffolded) `src/`, `scripts/`, `tests/`, `notebooks/`, plus (if deliverables exist) `deliverables/`. These are expected; check their internal structure in Buckets E–G.
- **Everything else** — potential findings; walk Buckets A–D below.

## Step 2: Walk the nine finding buckets

Collect findings from each bucket. Don't report as you go — walk them all first, then report grouped by bucket. Some findings are cross-bucket (e.g., a root-level `results/` is Bucket A; if it also contains loose PDFs, that's separately Bucket D). Record both.

### Bucket A — Semantic-overlap sprawl at root

Root-level directories that duplicate what should live under `docs/active/<branch>/results/` (writeups) or `data/processed/` (derived data). These grow one `mkdir` at a time when no lifecycle vocabulary exists.

Check for any of:

```bash
ls -d results/ output/ outputs/ reports/ analysis/ notes/ drafts/ sections/ tmp/ scratch/ 2>/dev/null
```

For each hit, record the directory and a sample of its contents (up to 5 files).

**Fix guidance to surface to the user:**
- If the dir holds *writeups, figures, tables* for a specific research line → move to `docs/active/<branch>/results/`.
- If the dir holds *derived data* → move to `data/processed/<branch>/` (or `data/processed/` if it's meant for downstream consumption).
- If the dir holds *scratch work* that shouldn't be committed → add to `.gitignore` (e.g., `sandbox/`, `scratch/`) and move contents there.
- If the dir belongs to a specific *deliverable* → move to `deliverables/<target>/`.

### Bucket B — Duplicate or adjacent doc directories

Root-level directories that shadow `docs/`.

Check for any of:

```bash
ls -d project_docs/ documentation/ _docs/ docs2/ wiki/ handbook/ 2>/dev/null
```

For each hit, record. **Fix guidance:** merge into `docs/` (specifically `docs/active/<branch>/` or `docs/historical/<branch>/` as appropriate; long-lived reference docs may want `docs/reference/` if the repo has one).

### Bucket C — Per-workstream top-level shadow taxonomy

Root-level directories that look like *workstreams* or *deliverables* rather than *kinds*. This is the kind-primary vs. workstream-primary axis conflict — each such directory is a shadow taxonomy competing with `docs/active/<branch>/` and `deliverables/<target>/`.

Heuristic: any top-level dir that isn't:
- In the known-good set (Bucket I),
- A framework-required kind (`docs/`, `papers/`, `data/`, `src/`, `scripts/`, `tests/`, `notebooks/`, `deliverables/`),
- Or already flagged in Bucket A / B.

For each such dir, sample its contents:

```bash
ls -A <dir>/ | head -20
```

Record with the sample.

**Fix guidance to ask the user, per finding:**

> *"`<dir>/` is a top-level directory that isn't in the framework's known kinds. What is it?*
> *(a) A research line — should be `docs/active/<dir>/` (or `docs/historical/<dir>/` if the line is complete)?*
> *(b) A deliverable — should be `deliverables/<dir>/` with a `LINEAGE.md`?*
> *(c) A genuinely self-contained sub-project that's kind-independent (has its own docs/, data/, code) — flag for review but leave in place?*
> *(d) Something else — describe and I'll help find the right home."*

**Operational-repo caveat:** in a `policy-levers/`-style repo where the primary organizing axis is campaigns/deliverables rather than research questions, a chunk of Bucket C findings will be *intentional* — the repo is deliverables-first by design. If the user says "this repo is operational, `bills/` and `us_china_council/` are meant to be top-level," accept the exception and move on. Note the pattern in the final report so the user can consider whether an `operations-mode` archetype would be a better fit than repeated exceptions.

### Bucket D — Root-level accumulation of loose files

Individual files at the repo root that aren't in the standing exceptions set. These typically indicate one-off work that never got homed properly.

Check for:

```bash
# PDFs at root (should be in papers/, deliverables/<target>/, or docs/active/<branch>/results/)
find . -maxdepth 1 -type f -name '*.pdf' 2>/dev/null

# Loose Python scripts (should be in scripts/ or src/)
find . -maxdepth 1 -type f \( -name '*.py' -not -name 'setup.py' -not -name 'conftest.py' \) 2>/dev/null

# Loose shell scripts (should be in scripts/)
find . -maxdepth 1 -type f -name '*.sh' 2>/dev/null

# Handoff / one-off markdowns (should be in docs/active/<branch>/ or deliverables/<target>/)
find . -maxdepth 1 -type f -name '*.md' -not -name 'README.md' -not -name 'STATUS.md' -not -name 'PAPER_INDEX.md' -not -name 'PAPER_SUMMARIES.md' -not -name 'CLAUDE.md' -not -name 'HUMANS.md' -not -name 'LICENSE*.md' -not -name '_PROJECT_INSTRUCTIONS*.md' 2>/dev/null

# Loose archives (should be gitignored or in data/raw/)
find . -maxdepth 1 -type f \( -name '*.zip' -o -name '*.tar.gz' -o -name '*.tgz' \) 2>/dev/null

# Loose data files (should be in data/raw/ or data/reference/)
find . -maxdepth 1 -type f \( -name '*.csv' -o -name '*.parquet' -o -name '*.json' -o -name '*.jsonl' -o -name '*.xlsx' -o -name '*.db' -o -name '*.sqlite' \) -not -name 'uv.lock' -not -name 'package.json' 2>/dev/null

# Loose images (should be in papers/, deliverables/, or docs/)
find . -maxdepth 1 -type f \( -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.gif' \) 2>/dev/null
```

For each hit, record the filename and size. **Fix guidance depends on file type:**
- PDF → `papers/` (if literature), `deliverables/<target>/` (if outward-facing), `docs/active/<branch>/results/` (if a research-line output)
- .py → `scripts/` (if runner) or `src/<pkg>/` (if library) — probably needs a rewrite to import from `src/<pkg>/` rather than living solo at root
- .sh → `scripts/`
- .md → `docs/active/<branch>/` or `deliverables/<target>/` depending on scope
- archives → typically `data/raw/` if inputs, otherwise gitignore + delete
- data files → `data/raw/` (if source) or `data/reference/` (if small committed lookup)
- images → wherever the surrounding artifact lives

### Bucket E — `data/` layout non-conformance

If `data/` exists but doesn't follow the Cookiecutter-DS convention:

```bash
ls -d data/raw/ data/interim/ data/processed/ data/reference/ 2>/dev/null
ls data/README.md 2>/dev/null
find data -maxdepth 1 -type f 2>/dev/null    # files directly in data/ root
```

Findings:
- Missing any of `raw/`, `interim/`, `processed/`, `reference/` subdirs
- Files sitting directly in `data/` root (should be in a subdir)
- Missing `data/README.md`
- `.gitignore` missing the `data/raw/**` / `data/interim/**` / `data/processed/**` block

Check the `.gitignore`:

```bash
grep -E 'data/raw|data/interim|data/processed' .gitignore 2>/dev/null
```

**Fix guidance:** point the user at `init-research-repo` (idempotent — will fill in the missing pieces without touching what's already there). For files directly in `data/` root, ask the user which subdir they belong in.

### Bucket F — Partial code scaffold

Signals of a half-set-up Python code layout — usually the result of ad-hoc `mkdir src/` without following through to `pyproject.toml`, or vice versa.

Check for:

```bash
ls -d src/ scripts/ tests/ notebooks/ 2>/dev/null
ls pyproject.toml .python-version uv.lock 2>/dev/null
find src -maxdepth 2 -name '__init__.py' 2>/dev/null
```

Findings:
- `pyproject.toml` exists but no `src/` directory (unlikely to actually work — the package it declares doesn't exist)
- `src/` exists but no `pyproject.toml` (no way to install; imports will fail unless `PYTHONPATH` is hand-set)
- `src/` exists with a package dir but no `__init__.py` in it
- `pyproject.toml` exists but no `.python-version`

**Fix guidance:** point the user at `init-code-scaffold` for a clean setup, or offer to complete the missing pieces manually if only one small thing is off.

### Bucket G — Deliverable lineage gaps

If `deliverables/` exists, each `deliverables/<target>/` should have a `LINEAGE.md`.

```bash
find deliverables -maxdepth 2 -type d 2>/dev/null
find deliverables -maxdepth 2 -name 'LINEAGE.md' 2>/dev/null
```

For each `deliverables/<target>/`:

- **Missing `LINEAGE.md`** — the deliverable has no provenance record. Point the user at `add-deliverable` (or offer to seed LINEAGE.md manually from the template if the deliverable was created outside the skill).
- **`Purpose: TBD` still in place** — the placeholder never got filled in. Ask the user to update.
- **Claims table is empty AND the deliverable has rendered outputs** (PDF, DOCX in the dir) — the deliverable has shipped but nothing was recorded. High-signal finding; a shipped-with-no-lineage deliverable is the exact failure mode LINEAGE is designed to prevent.
- **Input research lines section references branches that are `active` but were `active` many months ago** — the row was never re-pinned to a merge SHA. Ask the user to grep for the branch's merge commit and re-pin.

### Bucket H — Notebook rot (informational heuristic)

Notebooks that appear to have grown into production code and should probably be extracted to `src/<pkg>/`.

Heuristic signals:

```bash
find notebooks -name '*.ipynb' -size +200k 2>/dev/null   # large notebooks
find notebooks -name 'analysis.ipynb' -o -name 'pipeline.ipynb' -o -name 'final.ipynb' -o -name 'production*.ipynb' -o -name 'main.ipynb' 2>/dev/null    # production-sounding names
```

For each hit, record. **Fix guidance:** this is informational — the user decides whether the notebook still deserves to live in `notebooks/` or whether its logic should be lifted to `src/<pkg>/` and the notebook reduced to a thin caller. Do not push the user to extract; some notebooks are legitimately meant to stay in notebook form (a captured investigation, a walk-through for onboarding).

### Bucket I — Standing exceptions (never flag)

Files and directories that are known-good at the repo root and should never appear as findings. Don't include these in any bucket; skip during Step 1's classification.

**Files:**
- `README.md`, `STATUS.md`, `PAPER_INDEX.md`, `PAPER_SUMMARIES.md`, `CLAUDE.md`, `HUMANS.md`
- `LICENSE`, `LICENSE.md`, `LICENSE-ADDENDUM.txt`, and other `LICENSE*` variants
- `pyproject.toml`, `.python-version`, `uv.lock`, `requirements.txt`, `poetry.lock`, `setup.py`, `setup.cfg`
- `package.json`, `package-lock.json`, `tsconfig.json` (JS/TS projects)
- `.gitignore`, `.gitattributes`, `.editorconfig`
- `.env`, `.env.local`, `.env.*` (any local env files)
- `_PROJECT_INSTRUCTIONS.md`, `_PROJECT_INSTRUCTIONS_*.md` (per-user copies; gitignored)
- `.DS_Store` (macOS cruft; gitignored)
- Workspace files (`*.code-workspace`)

**Directories:**
- Framework kinds: `docs/`, `papers/`, `data/`, `src/`, `scripts/`, `tests/`, `notebooks/`, `deliverables/`
- Git and IDE: `.git/`, `.github/`, `.vscode/`, `.idea/`, `.worktrees/`
- Python cruft: `.venv/`, `venv/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `dist/`, `build/`, `*.egg-info/`
- Claude / tooling: `.claude/`, `.nori/`
- Jupyter: `.ipynb_checkpoints/`

If a repo has additional standing exceptions specific to it (e.g., a project-specific tooling dir), don't hardcode them — surface as a Bucket C finding the first time and let the user tell you to treat it as an exception going forward. This skill doesn't persist exceptions across runs; re-audit fresh each time so the user re-considers the classification.

## Step 3: Report findings

Present findings **grouped by bucket, bucket at a time**. Between buckets, wait for the user to respond before moving to the next.

For each bucket, use this format:

```
=== Bucket A — Semantic-overlap sprawl at root ===

Finding A1: `results/` at repo root
  Contents (5 of N):
    results/figure_1.png
    results/summary_v3.md
    results/2026-05-run.csv
    ...
  Fix guidance:
    - Writeups & figures → docs/active/<branch>/results/
    - Data (the .csv) → data/processed/<branch>/

Finding A2: `output/` at repo root
  Contents (2 of 2):
    output/rendered.pdf
    output/build.log
  Fix guidance: rendered.pdf may belong under deliverables/<target>/;
    build.log should be gitignored.

Two findings in Bucket A. How would you like to handle them? For each,
I can (a) move to the suggested destination, (b) accept as an exception
(operational-repo or intentional), or (c) skip for this session.
```

The user's response drives resolution. Once Bucket A is resolved, move to Bucket B. Don't front-load a giant list — the point of one-bucket-at-a-time is to keep the decision surface small.

**If a bucket has zero findings**, say so briefly ("Bucket B — Duplicate doc directories: no findings.") and move on. Don't skip silently; the user should see that each bucket was checked.

## Step 4: Act on approved fixes

For each finding the user approves:

- **Move a file / directory:** `git mv <src> <dst>` (preserves history). If the file wasn't tracked, plain `mv`.
- **Delete a file:** ask twice. Deletes are usually a mistake in a research repo. Prefer `git mv <file> sandbox/<file>` + adding `sandbox/` to `.gitignore` if the user wants it out of the way but not gone.
- **Add a `.gitignore` entry:** append to `.gitignore`, don't rewrite.
- **Point at another skill:** tell the user which skill covers the fix (e.g., "Bucket E's missing `data/README.md` is fixed by re-running `init-research-repo` — it's idempotent") and stop; don't reach into other skills' territory.
- **Update `LINEAGE.md` in a deliverable:** guide the user through re-pinning the SHA or filling the placeholder; don't rewrite the file wholesale.

**Commit the fixes** in logical groups (one commit per bucket typically, or one atomic commit if it's a small set of related moves). Use `git status` before committing to make sure nothing unexpected is staged.

## Step 5: Summary report

After all buckets are walked, produce a short summary:

```
audit-repo-structure — summary

Findings: <total>
  Bucket A (root sprawl):        N (M fixed, K accepted as exception, J skipped)
  Bucket B (duplicate docs):     N ...
  Bucket C (workstream shadow):  N ...
  Bucket D (loose files):        N ...
  Bucket E (data/ layout):       N ...
  Bucket F (partial code):       N ...
  Bucket G (LINEAGE gaps):       N ...
  Bucket H (notebook rot):       N (informational only)

Commits: <N> commits on <branch-name>

Follow-ups the user asked to defer:
  - <finding> (rationale)
  - <finding> (rationale)

Patterns worth noting:
  - <e.g., "Multiple Bucket C findings suggest this repo may fit the
    operational archetype better than the research-first default.
    Worth considering an operations-mode variant if this friction
    persists."> — only surface if a real pattern showed up
```

The patterns section is high-value — it turns a per-file audit into a repo-shape observation. Don't invent patterns that aren't there, but do surface real ones.

## Notes

- **Multi-session safety:** another agent may be actively working in a `.worktrees/<branch>/` directory. This skill inspects the *current* worktree only; findings from other worktrees are out of scope. If the user asks "check all worktrees," decline and explain — cross-worktree audits are how in-flight work gets clobbered.
- **Idempotency:** re-running this skill on a repo where the user has already accepted certain exceptions will re-flag those exceptions. That's deliberate. Persistent exception lists tend to accumulate stale entries; a fresh audit lets the user re-consider whether last month's exception is still the right call.
- **Operational-repo signal:** if a session repeatedly gets "this is an operational repo, leave it" responses to Bucket C findings, that's a real signal — surface in Step 5's patterns section. The `operations-mode` archetype for `policy-levers/`-style repos is a known deferred design item; every Bucket C exception in that direction adds weight to actually building it.
- **This skill does NOT modify `finishing-a-research-branch` or `start-research-line`** — it just points at them when a fix is upstream of what this skill can do alone.
- **What this skill is *not* for:** finding bugs in code, verifying test coverage, checking documentation quality, or evaluating research decisions. It's a filesystem-shape audit only.

## Common mistakes

**Auto-fixing findings without asking**
- Problem: `results/` at root looks like a violation, but it might be a deliberate choice in an operational repo, or it might be work-in-progress from another session's worktree. Auto-moving it destroys work.
- Fix: Step 3's "report and wait" is not optional. No `git mv` runs until the user has classified the finding.

**Reporting all findings at once instead of bucket-at-a-time**
- Problem: A big flat list is overwhelming — the user context-switches on every finding, and the "why is this a finding" gets lost. Small batches (per bucket) let the user stay in one frame per response.
- Fix: Walk all buckets first (Step 2), then report Bucket A, wait for resolution, then Bucket B, etc.

**Treating Bucket H (notebook rot) as actionable**
- Problem: Pushing the user to extract every large notebook is presumptuous. Some notebooks are legitimately reference/onboarding artifacts.
- Fix: Bucket H is informational. Surface the finding; move on unless the user asks to act.

**Missing the operational-repo caveat on Bucket C**
- Problem: Aggressively pushing all top-level workstream dirs into `docs/active/<branch>/` in a repo where campaigns/deliverables are the primary axis creates busywork and fights the repo's real shape.
- Fix: Ask; accept "this repo is operational" as a valid answer; note the pattern in Step 5.

**Rewriting `LINEAGE.md` files wholesale during Bucket G fixes**
- Problem: The researcher's specific claim rows, source paths, and change log entries are irreplaceable. A "seed a clean LINEAGE" fix that overwrites existing content is a lineage break.
- Fix: For a `deliverables/<target>/` that already has a partial `LINEAGE.md`, only append/update specific rows the user approves. If LINEAGE is entirely missing, use `add-deliverable`'s template — but only when the file doesn't exist yet.

**Committing all buckets in one commit**
- Problem: Reverting a specific fix (say, one wrong file move in Bucket D) means also reverting unrelated changes from Bucket A and Bucket E. History becomes hard to unwind.
- Fix: Commit per bucket, or per logically-related group of fixes within a bucket. Keep the commit messages specific ("Bucket A: move root results/ into docs/active/<branch>/results/").
