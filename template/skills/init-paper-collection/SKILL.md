---
name: init-paper-collection
description: Use when a research repo will hold papers and has no PAPER_SUMMARIES.md yet — creates papers/ and papers/text/, seeds PAPER_INDEX.md and PAPER_SUMMARIES.md with the generated-block markers, adds paper_index.toml, and installs the paper-index pre-commit hook. Called from init-research-repo.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Check what already exists
2. Create papers/ and papers/text/
3. Seed PAPER_INDEX.md, PAPER_SUMMARIES.md, paper_index.toml from the templates
4. Install the pre-commit hook and set core.hooksPath
5. Run index, then check; commit
</required>

Announce at start: "I'm using the init-paper-collection skill to set up the paper collection."

Sets up an empty paper collection in the format the `paper-index` skill generates and checks. Idempotent: never overwrites an existing file.

## Step 1: Check what exists

```bash
ls -la PAPER_INDEX.md PAPER_SUMMARIES.md PAPER_RELATED.md paper_index.toml .githooks/pre-commit 2>/dev/null
ls -d papers/ papers/text/ 2>/dev/null
```

If PAPER_SUMMARIES.md already exists in another format, stop and tell the user — converting a legacy collection is a migration, not a seed.

## Step 2: Directories

```bash
mkdir -p papers/text
touch papers/.gitkeep papers/text/.gitkeep
```

## Step 3: Seed files

Copy each template only where the target is absent (`T={{skills_dir}}/init-paper-collection/templates`):

| Template | Target |
|---|---|
| `$T/PAPER_INDEX.md.tmpl` | `PAPER_INDEX.md` — the three generated-block marker pairs and the Quick Reference preamble |
| `$T/PAPER_SUMMARIES.md.tmpl` | `PAPER_SUMMARIES.md` — the `summaries-header` marker pair |
| `$T/paper_index.toml.tmpl` | `paper_index.toml` — every key commented out |

If PAPER_INDEX.md exists without markers, add the three pairs (`counts`, `quick-reference`, `section-list`) by hand; the tool never invents them.

## Step 4: Pre-commit hook

```bash
mkdir -p .githooks
python3 {{skills_dir}}/paper-index/paper_index.py --print-hook > .githooks/pre-commit
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

The hook is tracked; `core.hooksPath` is per-clone, so each fresh clone runs the `git config` line once.

## Step 5: Generate, check, commit

```bash
python3 {{skills_dir}}/paper-index/paper_index.py index .
python3 {{skills_dir}}/paper-index/paper_index.py check .
git add papers/.gitkeep papers/text/.gitkeep PAPER_INDEX.md PAPER_SUMMARIES.md PAPER_RELATED.md paper_index.toml .githooks/pre-commit
git commit -m "Scaffold paper collection"
```

`check` must exit 0 before the commit; the hook runs it again. Then tell the user the collection is ready and that papers go in through the `add-paper` skill.
