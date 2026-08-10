---
name: update-docs
description: Checkpoint research progress mid-session — create/update convo summary, save results with provenance, update RESEARCH_LOG (and, in main_only mode only, a capped STATUS one-liner). Core operation that finish-convo builds on.
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

1. Determine the current branch name and convo name.

The convo name is the user-confirmed identifier established during the §2e handshake at session start (see `template/RESEARCHER.md`). It links every artifact you write this session — the convo summary, any plans, results files, the RESEARCH_LOG entry, the STATUS line — and its `SESSION_TS` fragment (basic-format ISO 8601, `YYYYMMDDTHHMM`) matches the timestamp inside the git-commit author name RESEARCHER.md §2.0b set for this session. Format: `${SESSION_TS}_<short-slug>` for `main_only` repos, or `<short-slug>_${SESSION_TS}` for `branches`-mode repos.

If for some reason no convo name was established (older runtime version that pre-dates the handshake, the §2e step was skipped, or the user initially opted out and now wants to log the session), propose one now and confirm with the user before writing any files. Do not invent a provisional name; the rename later costs more than asking now.

2. Create or update the conversation summary at `docs/active/<branch-name>/convos/<convo-name>.md`:

```markdown
# [Convo Name]

**Date:** YYYY-MM-DD
**Branch:** branch-name
**Surface:** claude.ai | claude-code

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
- Name with date prefix: `YYYYMMDD_description.md` (for tables), `.png`/`.pdf` (for figures). Date-only is fine here — results files aren't joined against git commits, so the compact ISO date suffices.
- Each results file should include a provenance header pointing at this session's convo file:

```markdown
<!-- Generated during: convos/<convo-name>.md -->
```

- Add links to these results in the convo file's "Results" section
- For markdown tables: save as `.md` files in results/
- For figures/plots: save the image file AND a brief `.md` companion describing what it shows and how it was generated

If no results were produced, skip this step.

4. Append session entry to `docs/active/<branch-name>/RESEARCH_LOG.md`:

```markdown
## Session: YYYYMMDDTHHMM — [convo-name]
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

5. Session summary — mode-dependent. Check `workflow_mode` in STATUS.md's header (absent = `branches`).

- **`branches` mode: do NOT touch STATUS.md.** The session summary is the RESEARCH_LOG entry you wrote in step 4 — that IS the session record. STATUS.md is written only by the `start-research-line` and merge ceremonies (see RESEARCHER.md §2c boundary). Do not add STATUS.md to this skill's commit.
- **`main_only` mode:** append a one-liner under `## Recent Sessions`. Format: `- YYYY-MM-DD: explored X, found Y — <link to convo or log>`. Hard cap: ≤2 lines per entry; detail belongs in the convo doc / RESEARCH_LOG. If the section exceeds ~20 entries, offer to roll the oldest into a per-year archive file. Do NOT rewrite STATUS.md conclusions — just append.
</required>

# Common Mistakes

**Writing convo summaries that sound like settled conclusions**
- Problem: Future agents read "we determined X" and treat it as ground truth
- Fix: Use language like "we explored X and the initial evidence suggests Y"

**Forgetting to link results to conversations**
- Problem: A table or figure in results/ has no context — future agents don't know what question it was answering
- Fix: Every results file has a provenance header; every convo lists its results

**Writing STATUS.md in branches mode**
- Problem: The skill historically appended a Recent Sessions one-liner every session; entries drifted to diary length, branch copies of STATUS forked from main's, and merges conflicted (this exact failure motivated the orchestrator model — claude_researcher#38).
- Fix: In `branches` mode, update-docs never writes STATUS.md. In `main_only` mode, ONLY append the capped one-liner; never rewrite existing content.

**Creating a duplicate RESEARCH_LOG entry on second update-docs call**
- Problem: Mid-session checkpoint creates a second entry for the same session
- Fix: Check if an entry for this convo-name already exists; update it in place
