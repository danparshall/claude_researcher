---
name: init-research-repo
description: Use when setting up a new repo (or an existing repo) for the research-first workflow — creates docs/active/ and docs/historical/ directories, seeds STATUS.md with the Active and Archived Research Lines tables and an empty HISTORY.md, scaffolds data/ subdirs (raw/interim/processed/reference) with a README, and seeds a sensible .gitignore
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Check what already exists (STATUS.md, HISTORY.md, docs/, data/, .gitignore)
2. Create directory structure (docs/ + data/)
3. Seed data/README.md with the Cookiecutter-DS convention + provenance stub
4. Seed .gitignore if missing (Python + data/ pattern)
5. Seed STATUS.md and HISTORY.md
6. Create initial RESEARCH_LOG.md if on a branch
7. If the repo will hold papers, run init-paper-collection
8. Report what was created
</required>

Announce at start: "I'm using the Init Research Repo skill to set up the research workflow."

Sets up the directory structure and documentation scaffolding for the research-first workflow. Idempotent — checks before creating and never overwrites existing content, so it's safe on a partially set-up repo. It creates structure only; content comes from the research workflow (finish-convo, write-a-plan).

The workflow's epistemic norms and doc-structure conventions are **persona-level** — they live in `RESEARCHER.md` (web) or `AGENTS.md` (Claude Code), read every session, not duplicated into each repo's `CLAUDE.md`. A per-repo `CLAUDE.md` is for project-specific standing notes; this skill doesn't create or modify it.

Seed templates live in `{{skills_dir}}/init-research-repo/templates/` (`T` below).

## Step 1: Check What Exists

```bash
ls -la STATUS.md HISTORY.md README.md .gitignore 2>/dev/null
ls -d docs/ docs/active/ docs/historical/ data/ data/raw/ data/reference/ 2>/dev/null
ls data/README.md 2>/dev/null
```

- If `docs/active/` already exists, this repo may already be set up — ask the user before overwriting.
- If `data/` already exists with subdirs unlike the convention below (a flat `data/` with files in it, or `data/output/` + `data/results/` sprawl), **surface to the user before restructuring** — moving data files has lineage implications. This skill only creates missing scaffolding.

## Step 2: Create Directory Structure

```bash
mkdir -p docs/active docs/historical

BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
  mkdir -p "docs/active/$BRANCH/convos" "docs/active/$BRANCH/plans" "docs/active/$BRANCH/results"
fi
```

Data skeleton (only if `data/` doesn't already exist with a different layout — see Step 1):

```bash
mkdir -p data/raw data/interim data/processed data/reference
touch data/raw/.gitkeep data/interim/.gitkeep data/processed/.gitkeep data/reference/.gitkeep
```

The four subdirs match the Cookiecutter Data Science convention (https://cookiecutter-data-science.drivendata.org/opinions/): raw is immutable inputs, interim is scratch between raw and processed, processed is canonical downstream-consumable output, reference is small lookup tables. The `.gitkeep` files keep each subdir in an empty state (Step 4's `.gitignore` ignores everything under raw/interim/processed except the markers).

## Step 3: Seed data/README.md

If `data/README.md` doesn't exist, copy `$T/data_readme.md.tmpl` to it (layout, provenance stub, optional external-sync note).

## Step 4: Seed .gitignore

If `.gitignore` doesn't exist, copy `$T/gitignore.tmpl` to it (Python, Jupyter, OS, secrets, and the `data/raw/**` block aligned with Step 2).

If `.gitignore` already exists, do **not** overwrite. Check whether the `data/raw/**` block is present; if missing, offer to append it (don't silently modify a hand-maintained file). If the user declines, note it in the report.

## Step 5: Seed STATUS.md and HISTORY.md

Seed: `$T/status_seed.md.tmpl` — header, Current Focus, `## Project parameters` (optional keys read only by web-profile skills), `## Active Research Lines`, `## Archived Research Lines`.

- If STATUS.md exists, append each of those three `##` sections it lacks, copied from the seed. Don't add `## Recent Sessions` — sessions log in RESEARCH_LOG.md, and STATUS.md changes only when a line opens or closes.
- If STATUS.md doesn't exist, ask the user whether to create one; if yes, copy the full seed.

If `README.md` doesn't exist, ask the user for a one-paragraph description of the repo and write `# <repo name>` followed by that paragraph.

If `HISTORY.md` doesn't exist, copy `$T/history_seed.md.tmpl` to it. `finishing-a-research-branch` rolls Archived rows beyond the newest 10 into it.

## Step 6: Create Initial RESEARCH_LOG.md (if on a branch)

If on a named branch (not main/master), create `docs/active/<branch>/RESEARCH_LOG.md` from `$T/research_log_seed.md.tmpl`, filling in the branch name and asking the user for the one-sentence Purpose.

## Step 7: Paper collection (optional)

If the repo will hold papers, read and follow `{{skills_dir}}/init-paper-collection/SKILL.md`.

## Step 8: Report

Tell the user what was created (only the lines that actually landed — skip anything already present or declined):

```
Research workflow initialized:
  - docs/active/           (active research lines)
  - docs/historical/       (archived research lines)
  - data/                  (raw/, interim/, processed/, reference/ + README.md)
  - .gitignore             (Python + data/raw|interim|processed gitignored)
  - STATUS.md              (Project parameters + Active/Archived Research Lines tables)
  - HISTORY.md             (archived rows beyond the newest 10)
  [- docs/active/<branch>/ (with RESEARCH_LOG.md, convos/, plans/, results/)]
  [- paper collection     (papers/, PAPER_INDEX.md, PAPER_SUMMARIES.md, pre-commit hook)]

Next steps:
  - Fill in `PROJECT_QUESTION` in STATUS.md `## Project parameters` if you use web-profile skills
  - When you add a dataset to `data/raw/`, add a provenance section for it in `data/README.md`
  - Start a research session; finish-convo writes the convo doc and the RESEARCH_LOG line
  - Archive completed lines with finishing-a-research-branch
```

Then push to back up the scaffolding: `git push -u origin <branch>`.

## DOCS_INDEX.md Approach

If the repo has a DOCS_INDEX.md (or similar index file), convert it to a lightweight meta-index:

```markdown
## Active Research Lines
See docs/active/. Each branch directory has convos/, plans/, results/, and a RESEARCH_LOG.md of its sessions.

## Historical
See docs/historical/. Summaries in STATUS.md "Archived Research Lines" table (older rows in HISTORY.md).

## Legacy Docs (docs/ root)
[existing entries for files not yet migrated]
```

Per-line indexing is RESEARCH_LOG.md's job inside each `docs/active/<branch>/`. Don't maintain a single global index across branches — that creates merge conflicts and busywork.

## Notes

- **`data/` layout is the default, not the only choice.** Some repos (heavy-code with no external data, or all inputs in `papers/`) don't need `data/`. If the user says "no data dir," skip Step 2's data block, Step 3, and the data lines in the `.gitignore`.
- **Deliverables and code scaffolding are out of scope.** Code (`src/<pkg>/`, `scripts/`, `tests/`, `notebooks/`) is created lazily when needed; `deliverables/<target>/` with a `LINEAGE.md` holds outward-facing artifacts. Neither applies to every research repo.
