---
name: init-research-repo
description: Use when setting up a new repo (or an existing repo) for the research-first workflow — creates docs/active/ and docs/historical/ directories, seeds STATUS.md with the Archived Research Lines table, scaffolds data/ subdirs (raw/interim/processed/reference) with a README, and seeds a sensible .gitignore
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

Both environments set positive markers; the probe checks for either side affirmatively rather than inferring from absence. If neither fires, something is misconfigured (env vars stripped, custom shell, etc.) and silently picking a branch is worse than surfacing the question.

**If `claude.ai sandbox`:** the user's project repo is already cloned at `/home/claude/<REPO>/` per `RESEARCHER.md` §2.0b — run the `git add` / `git commit` / `git push` commands in this skill directly from that working tree. Translate local skill paths like `/Users/<user>/.claude/skills/...` to the template clone at `/home/claude/.claude_researcher_template/template/skills/...`. Only if the §2.0b clone failed (degraded REST fallback, surfaced to the user) do you translate `git add` / `git commit` / `git push` into the Contents API recipes from your Project Instructions.

**If `Claude Code`:** follow the skill body as-is.

**If `unknown`:** stop and surface to the user. Don't guess which environment you're in — the cost of a wrong guess (operating against the wrong working tree, or using the wrong write path for the environment) is higher than the cost of one round-trip clarification.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Check what already exists (STATUS.md, docs/, data/, .gitignore)
2. Create directory structure (docs/ + data/)
3. Seed data/README.md with the Cookiecutter-DS convention + provenance stub
4. Seed .gitignore if missing (Python + data/ pattern)
5. Seed STATUS.md with research sections
6. Create initial RESEARCH_LOG.md if on a branch
7. Report what was created
</required>

# Init Research Repo

Sets up the directory structure and documentation scaffolding needed for the research-first workflow.

Announce at start: "I'm using the Init Research Repo skill to set up the research workflow."

## The Process

The research-first workflow's epistemic norms and doc-structure conventions (the "Research Context") are **persona-level** — they live in upstream `RESEARCHER.md`, read by the agent every session, rather than duplicated into each repo's `CLAUDE.md`. Claude Code users can use `RESEARCHER.md` as their `~/.claude/CLAUDE.md`, optionally concatenated with their user-level instructions. A per-repo `CLAUDE.md` is for **project-specific** standing notes — this skill doesn't create or modify it; that's the user's prerogative.

### Step 1: Check What Exists

Before creating anything, check what's already in place:

```bash
ls -la STATUS.md README.md .gitignore 2>/dev/null
ls -d docs/ docs/active/ docs/historical/ data/ data/raw/ data/reference/ 2>/dev/null
ls data/README.md 2>/dev/null
```

- If `docs/active/` already exists, this repo may already be set up — ask the user before overwriting
- If `data/` already exists with subdirs unlike the convention below (e.g., only a flat `data/` with files in it, or `data/output/` + `data/results/` sprawl), **surface to the user before restructuring** — moving data files is a change with lineage implications. This skill only creates missing scaffolding; it doesn't reorganize existing data

### Step 2: Create Directory Structure

Docs skeleton:

```bash
mkdir -p docs/active docs/historical
```

If we're on a named branch (not main), also scaffold the branch's doc dir:

```bash
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
  mkdir -p "docs/active/$BRANCH/convos" "docs/active/$BRANCH/plans" "docs/active/$BRANCH/results"
fi
```

Data skeleton (only if `data/` doesn't already exist with a different layout — see Step 1's surface-to-user rule):

```bash
mkdir -p data/raw data/interim data/processed data/reference
touch data/raw/.gitkeep data/interim/.gitkeep data/processed/.gitkeep data/reference/.gitkeep
```

The four subdirs match the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/opinions/) convention: raw is immutable inputs, interim is scratch space between raw and processed, processed is canonical downstream-consumable output, reference is small lookup tables. The `.gitkeep` files ensure each subdir survives an empty state (the default `.gitignore` in Step 4 ignores everything under raw/interim/processed except the `.gitkeep` markers).

### Step 3: Seed data/README.md

If `data/README.md` doesn't already exist:

```markdown
# data/

Data lifecycle follows the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/opinions/) convention. **Raw data is immutable — never edit files in `raw/` by hand.** Analysis is a DAG: if `interim/` or `processed/` is deleted, it should regenerate from `raw/` plus code in `src/` / `scripts/` / `notebooks/`.

## Layout

- `raw/` — original, immutable inputs (downloaded datasets, vendor exports, scraped snapshots). Gitignored.
- `interim/` — in-progress transforms; scratch space between raw and processed. Gitignored.
- `processed/` — canonical, downstream-consumable datasets. Gitignored by default; commit small stable ones if they're expensive to regenerate.
- `reference/` — small lookup tables and code lists (country codes, taxonomies, unit conversions). **Committed** — treat as documentation.

## Provenance

For every dataset in `raw/`, add a section here so a fresh collaborator (or a future agent) knows where it came from:

### <dataset-name>

- Source: <URL or vendor>
- Retrieved: <YYYY-MM-DD>
- License / terms: <if applicable>
- Retrieval command / script: <e.g., `scripts/fetch_<name>.py`>
- Hash: <sha256 of the file or archive, if reproducibility matters>

## External sync (optional)

If you sync `raw/` (or the whole `data/`) externally — e.g., Syncthing to a shared home-directory location, an S3 bucket, or a shared drive — document the arrangement here. The default assumption is that `raw/` files come from re-running the retrieval commands above.
```

### Step 4: Seed .gitignore

If `.gitignore` doesn't exist, create one with sensible Python + data defaults (aligned with the Step 2 layout):

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
.python-version

# Jupyter
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db

# Environment / secrets
.env
.env.local
*.key
*.pem

# Data — raw/interim/processed are large or regenerable; reference is committed
data/raw/**
data/interim/**
data/processed/**
!data/raw/.gitkeep
!data/interim/.gitkeep
!data/processed/.gitkeep

# Local project instructions (per-user copy — the Project Instructions block lives in claude.ai, not the repo)
_PROJECT_INSTRUCTIONS.md
```

If `.gitignore` already exists, do **not** overwrite. Check whether the `data/raw/**` block is present; if missing, offer to append it (don't silently modify a hand-maintained file). If the user declines, note it in the report so they can wire it in later.

### Step 5: Seed STATUS.md

If STATUS.md exists, check whether it already has a `## Project parameters` section. If not, append:

```markdown
## Project parameters

Per-project configuration the skills read at runtime. Update only when the project's scope or conventions change.

- `PROJECT_QUESTION`: [to be filled in — one-sentence research question]
- `CONDITIONAL_SECTION`: unset
- `BIB_FILE`: unset
- `PAPERS_INDEX`: PAPER_INDEX.md
- `paper_summaries.structure`: single-file
```

Then check whether STATUS.md already has an "Active Research Lines" section. If not, append:

```markdown
## Active Research Lines

Lines currently in flight; see `docs/active/<topic>/` for material. Updated by the `start-research-line` skill.

| Topic | Started | Purpose |
|-------|---------|---------|
| (none yet) | | |
```

Then check whether STATUS.md has a "Recent Sessions" section. If not, append:

```markdown
## Recent Sessions

(One-line session summaries, newest first)
```

Then check whether STATUS.md has an "Archived Research Lines" section. If not, append:

```markdown
## Archived Research Lines

Lines moved to docs/historical/ — not currently active, but available for reference.

| Topic | Summary | Archived | Material |
|-------|---------|----------|----------|
| (none yet) | | | |
```

If STATUS.md doesn't exist, ask the user whether to create one. A minimal seed:

```markdown
# STATUS — [Project Name]

Last updated: YYYY-MM-DD

## Current Focus

[To be filled in]

## Project parameters

Per-project configuration the skills read at runtime. Update only when the project's scope or conventions change.

- `PROJECT_QUESTION`: [to be filled in — one-sentence research question]
- `CONDITIONAL_SECTION`: unset
- `BIB_FILE`: unset
- `PAPERS_INDEX`: PAPER_INDEX.md
- `paper_summaries.structure`: single-file

## Active Research Lines

Lines currently in flight; see `docs/active/<topic>/` for material. Updated by the `start-research-line` skill.

| Topic | Started | Purpose |
|-------|---------|---------|
| (none yet) | | |

## Recent Sessions

(One-line session summaries, newest first)

## Archived Research Lines

Lines moved to docs/historical/ — not currently active, but available for reference.

| Topic | Summary | Archived | Material |
|-------|---------|----------|----------|
| (none yet) | | | |
```

### Step 6: Create Initial RESEARCH_LOG.md (if on a branch)

If we're on a named branch (not main/master), create `docs/active/<branch>/RESEARCH_LOG.md`:

```markdown
# Research Log: [branch-name]
Created: YYYY-MM-DD
Purpose: [ask the user for a one-sentence description]

---

(Sessions will be logged here, newest first)
```

### Step 7: Report

Tell the user what was created (show only the lines that actually landed — skip any that were already present or that the user declined):

```
Research workflow initialized:
  - docs/active/           (active research lines)
  - docs/historical/       (archived research lines)
  - data/                  (raw/, interim/, processed/, reference/ + README.md)
  - .gitignore             (Python + data/raw|interim|processed gitignored)
  - STATUS.md              (Project parameters + Active/Archived Research Lines tables + Recent Sessions section added)
  [- docs/active/<branch>/ (with RESEARCH_LOG.md, convos/, plans/, results/)]

Next steps:
  - Fill in `PROJECT_QUESTION` in STATUS.md `## Project parameters` (and any optional keys: `CONDITIONAL_SECTION`, `BIB_FILE`)
  - When you add a dataset to `data/raw/`, add a provenance section for it in `data/README.md`
  - Start a research session and the finish-convo skill will populate the rest
  - Use `git mv docs/active/<topic> docs/historical/<topic>` to archive completed research lines
```

## DOCS_INDEX.md Approach

If the repo has a DOCS_INDEX.md (or similar index file), convert it to a lightweight meta-index:

```markdown
## Active Research Lines
See docs/active/. Each branch directory has convos/, plans/, results/.
STATUS.md "Recent Sessions" tracks activity across branches.

## Historical
See docs/historical/. Summaries in STATUS.md "Archived Research Lines" table.

## Legacy Docs (docs/ root)
[existing entries for files not yet migrated]
```

The detailed per-branch indexing is handled by RESEARCH_LOG.md within each `docs/active/<branch>/` directory. Don't try to maintain a single global index across all branches — that creates merge conflicts and busywork.

## Notes

- This skill is idempotent — it checks before creating and won't overwrite existing content.
- It's safe to run on an existing repo that's partially set up.
- The skill creates structure only. Content comes from the research workflow (finish-convo, write-a-plan, etc.).
- **`data/` layout is the default, not the only choice.** Some repos (heavy-code with no external data, or repos where all inputs live in `papers/`) may not need `data/` at all. If the user says "no data dir," skip Steps 2's data block, Step 3, and the data lines in Step 4's `.gitignore`.
- **Deliverables and code scaffolding are out of scope for this skill.** The research-first framework separately assumes: `src/<pkg>/`, `scripts/`, `tests/`, `notebooks/` for code (lazily created when needed); `deliverables/<target>/` with a `LINEAGE.md` for outward-facing artifacts (which may draw on multiple research lines). Those aren't scaffolded here because they don't apply to every research repo.
- **Push after setup** — `git push -u origin <branch>` to back up the scaffolding immediately.
