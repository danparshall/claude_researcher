---
name: init-research-repo
description: Use when setting up a new repo (or an existing repo) for the research-first workflow — creates docs/active/ and docs/historical/ directories, seeds STATUS.md with the Archived Research Lines table
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

1. Check what already exists (STATUS.md, docs/)
2. Create directory structure
3. Seed STATUS.md with research sections
4. Create initial RESEARCH_LOG.md if on a branch
5. Report what was created
</required>

# Init Research Repo

Sets up the directory structure and documentation scaffolding needed for the research-first workflow.

Announce at start: "I'm using the Init Research Repo skill to set up the research workflow."

## The Process

The research-first workflow's epistemic norms and doc-structure conventions (the "Research Context") are **persona-level** — they live in upstream `RESEARCHER.md`, read by the agent every session, rather than duplicated into each repo's `CLAUDE.md`. Claude Code users can use `RESEARCHER.md` as their `~/.claude/CLAUDE.md`, optionally concatenated with their user-level instructions. A per-repo `CLAUDE.md` is for **project-specific** standing notes — this skill doesn't create or modify it; that's the user's prerogative.

### Step 1: Check What Exists

Before creating anything, check what's already in place:

```bash
ls -la STATUS.md README.md 2>/dev/null
ls -d docs/ docs/active/ docs/historical/ 2>/dev/null
```

- If `docs/active/` already exists, this repo may already be set up — ask the user before overwriting

### Step 2: Create Directory Structure

```bash
mkdir -p docs/active docs/historical
```

If we're on a named branch (not main):

```bash
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
  mkdir -p "docs/active/$BRANCH/convos" "docs/active/$BRANCH/plans" "docs/active/$BRANCH/results"
fi
```

### Step 3: Seed STATUS.md

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

Then check whether STATUS.md already has an "Archived Research Lines" section. If not, append:

```markdown
## Archived Research Lines

Lines moved to docs/historical/ — not currently active, but available for reference.

| Topic | Summary | Archived | Material |
|-------|---------|----------|----------|
| (none yet) | | | |

## Recent Sessions

(One-line session summaries, newest first)
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

## Recent Sessions

(One-line session summaries, newest first)

## Archived Research Lines

Lines moved to docs/historical/ — not currently active, but available for reference.

| Topic | Summary | Archived | Material |
|-------|---------|----------|----------|
| (none yet) | | | |
```

### Step 4: Create Initial RESEARCH_LOG.md (if on a branch)

If we're on a named branch (not main/master), create `docs/active/<branch>/RESEARCH_LOG.md`:

```markdown
# Research Log: [branch-name]
Created: YYYY-MM-DD
Purpose: [ask the user for a one-sentence description]

---

(Sessions will be logged here, newest first)
```

### Step 5: Report

Tell the user what was created:

```
Research workflow initialized:
  - docs/active/           (active research lines)
  - docs/historical/       (archived research lines)
  - STATUS.md              (Project parameters section + Archived Research Lines table + Recent Sessions section added)
  [- docs/active/<branch>/ (with RESEARCH_LOG.md, convos/, plans/, results/)]

Next steps:
  - Fill in `PROJECT_QUESTION` in STATUS.md `## Project parameters` (and any optional keys: `CONDITIONAL_SECTION`, `BIB_FILE`)
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

- This skill is idempotent — it checks before creating and won't overwrite existing content
- It's safe to run on an existing repo that's partially set up
- The skill creates structure only. Content comes from the research workflow (finish-convo, write-a-plan, etc.)
- **Push after setup** — `git push -u origin <branch>` to back up the scaffolding immediately
