---
name: update-docs
description: Use when checkpointing research progress mid-session — creates or updates the convo summary, saves results with provenance, and writes the session's one-line RESEARCH_LOG entry. Never writes STATUS.md (a LITE repo's `## Sessions` entry is the one exception). Core operation that finish-convo builds on.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Work out where the session's record goes, its convo name, and its identity.

- **Line or not.** If the session worked in a research line (a `docs/active/<line>/` directory exists for it), everything below goes under that directory. If it had no line — a repo that has lines, but this session was a one-off fix or maintenance — convo docs go in `docs/convos/`, results in `docs/results/`, and the log entry in a repo-root `RESEARCH_LOG.md`.
- **Convo name.** The name the user confirmed at session start (both surfaces propose one in the first reply). Format: `YYYYMMDD_<short-slug>`. If none was established, propose one now and confirm before writing any files — do not invent a provisional name; a later rename costs more than asking.
- **Session identity.** The session codename (the `user.name` on this session's commits) and, on Claude Code, the transcript path — both announced at session start; with the session-identity hook installed, `~/.claude/session-identity/<session_id>.env` holds them. On claude.ai, the session URL if you have it. Write `—` for anything you don't have.
- **Machine.** `hostname -s` on Claude Code; `sandbox` on claude.ai.

2. Create or update the conversation summary at `<line dir>/convos/<convo-name>.md`:

```markdown
# [Convo Name]

**Date:** YYYY-MM-DD
**Branch:** branch-name
**Surface:** claude.ai | claude-code
**Machine:** <hostname -s, or sandbox>
**Session:** <codename> · <transcript path or —> · <claude.ai session URL or —>

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
- Save each to `<line dir>/results/`, named with a date prefix: `YYYYMMDD_description.md` (tables), `.png`/`.pdf` (figures)
- Each results file starts with a provenance header pointing at this session's convo file:

```markdown
<!-- Generated during: convos/<convo-name>.md -->
```

- Link each one from the convo file's "Results" section
- For figures/plots: save the image file AND a brief `.md` companion describing what it shows and how it was generated

If no results were produced, skip this step.

4. Write the session's log entry — **one line**, at the TOP of the log (below the header), newest first:

```markdown
- YYYY-MM-DD: [<codename>] <one sentence: what the session did and found> — convos/<convo-name>.md
```

- In a line: `docs/active/<line>/RESEARCH_LOG.md`.
- No line: the repo-root `RESEARCH_LOG.md`, linking `docs/convos/<convo-name>.md`. If the file is absent, create it with the header `# RESEARCH_LOG` and the line "Sessions with no research line, newest first. Line sessions log in `docs/active/<line>/RESEARCH_LOG.md`."

Topics, findings, results, and next steps belong in the convo doc, not the log. Log → convo doc → transcript is the chain that reconstructs any session. Mid-session checkpoint: if this convo already has a log line, update it in place.

5. If `paper_index.toml` exists at the repo root, run `python3 {{skills_dir}}/paper-index/paper_index.py check .`. If it is red, fix it (usually `paper_index.py index .`) before anything is committed.

6. STATUS.md:

- **LITE repo (`LITE.md` at the root):** write the ≤5-line STATUS `## Sessions` entry per `LITE.md` and stop here.
- **Otherwise: do not write STATUS.md.** The log line is the session record. STATUS.md is written only when a line opens or closes.
</required>

# Common Mistakes

**Writing convo summaries that sound like settled conclusions**
- Problem: Future agents read "we determined X" and treat it as ground truth
- Fix: Use language like "we explored X and the initial evidence suggests Y"

**Forgetting to link results to conversations**
- Problem: A table or figure in results/ has no context — future agents don't know what question it was answering
- Fix: Every results file has a provenance header; every convo lists its results

**Writing STATUS.md from a session**
- Problem: When every session appends to STATUS.md, it grows into a diary nobody can read at session start — one repo's reached 208 KB and had to be grepped — and branch copies conflict at merge.
- Fix: Sessions write the convo doc and one log line. STATUS.md changes only when a line opens or closes (LITE repos excepted, per `LITE.md`).

**Writing a multi-paragraph log entry**
- Problem: The log is read at every session start; long entries push the recent ones out of reach.
- Fix: One line linking the convo doc; the detail goes there.

**Creating a duplicate log entry on a second update-docs call**
- Problem: A mid-session checkpoint adds a second line for the same session
- Fix: Check whether this convo already has a line; update it in place
