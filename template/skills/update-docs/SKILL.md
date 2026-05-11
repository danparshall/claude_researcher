---
name: Update-Docs
description: Checkpoint research progress mid-session — create/update convo summary, save results with provenance, update RESEARCH_LOG and STATUS.md. Core operation that finish-convo builds on.
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

**If `claude.ai sandbox`:** translate every `git add` / `git commit` / `git push` in this skill into the REST `write_update` / `write_new` recipes from your Project Instructions. Translate local paths like `/Users/<user>/.claude/skills/...` into `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/...` URLs (fetched via WebFetch).

**If `Claude Code`:** follow the skill body as-is.

**If `unknown`:** stop and surface to the user. Don't guess which environment you're in — the cost of a wrong guess (running `git push` in a sandbox with no git, or writing REST calls against a local working tree) is higher than the cost of one round-trip clarification.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Determine the current branch name and convo name.

The convo name is the user-confirmed identifier established during the §2e handshake at session start (see `template/CLAUDE.md`). It links every artifact you write this session — the convo summary, any plans, results files, the RESEARCH_LOG entry, the STATUS line. Format: `YYYYMMDD_<short-slug>` for `main_only` repos, or `<short-slug>` for `branches`-mode repos.

If for some reason no convo name was established (older runtime version that pre-dates the handshake, the §2e step was skipped, or the user initially opted out and now wants to log the session), propose one now and confirm with the user before writing any files. Do not invent a provisional name; the rename later costs more than asking now.

2. Create or update the conversation summary at `docs/active/<branch-name>/convos/<convo-name>.md`:

```markdown
# [Convo Name]

**Date:** YYYY-MM-DD
**Branch:** branch-name

## Summary
2-3 paragraphs of what was discussed and explored this session.

## Topics Explored
- Bullet points of what was investigated

## Provisional Findings
- What we learned or observed (these are provisional, not conclusions)

## Decisions Made
- Any concrete decisions about next steps or approach
- Link to plan docs if any were created

## Results
- Links to any results files saved this session (see step 3)

## Open Questions
- Things we didn't resolve
- Hypotheses that need testing
```

If updating an existing convo file (mid-session checkpoint), append new findings rather than rewriting — preserve the chronological record.

3. Save any results produced this session.

If the session produced tables, figures, analysis outputs, or data summaries:
- Save each to `docs/active/<branch-name>/results/`
- Name with date prefix: `YYYYMMDD_description.md` (for tables), `.png`/`.pdf` (for figures)
- Each results file should include a provenance header:

```markdown
<!-- Generated during: convos/YYYYMMDD_convo_name.md -->
```

- Add links to these results in the convo file's "Results" section
- For markdown tables: save as `.md` files in results/
- For figures/plots: save the image file AND a brief `.md` companion describing what it shows and how it was generated

If no results were produced, skip this step.

4. Append session entry to `docs/active/<branch-name>/RESEARCH_LOG.md`:

```markdown
## Session: YYYY-MM-DD — [convo-name]
### Topics Explored
- Brief bullet points (can reference the full convo file for detail)

### Provisional Findings
- Key takeaways from this session

### Results
- Links to any results files (e.g., `results/20260321_distribution_table.md`)

### Next Steps
- What to try next session
```

Place the new entry at the TOP of the log (below the header), so the most recent session is first.

If updating an existing RESEARCH_LOG entry (mid-session checkpoint), update in place rather than creating a duplicate.

5. Update STATUS.md with a one-line session summary.

- Add a line under a "Recent Sessions" section (or create it if it doesn't exist)
- Format: `- YYYY-MM-DD: [branch] explored X, found Y`
- Do NOT rewrite STATUS.md conclusions — just append the one-liner
</required>

# Common Mistakes

**Writing convo summaries that sound like settled conclusions**
- Problem: Future agents read "we determined X" and treat it as ground truth
- Fix: Use language like "we explored X and the initial evidence suggests Y"

**Forgetting to link results to conversations**
- Problem: A table or figure in results/ has no context — future agents don't know what question it was answering
- Fix: Every results file has a provenance header; every convo lists its results

**Overwriting STATUS.md**
- Problem: A one-session finding replaces months of accumulated context
- Fix: ONLY append a one-liner. Never rewrite existing STATUS.md content during update-docs.

**Creating a duplicate RESEARCH_LOG entry on second update-docs call**
- Problem: Mid-session checkpoint creates a second entry for the same session
- Fix: Check if an entry for this convo-name already exists; update it in place
