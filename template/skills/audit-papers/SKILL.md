---
name: audit-papers
description: Use when auditing the papers/ collection — runs the paper-index check for structure, then verifies a sample of PAPER_SUMMARIES.md entries against their source text. Prompts the user for discrepancies.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
CRITICAL: Add the following steps to your Todo list using TodoWrite:

1. Run the paper-index check; report structural problems and fix only what the user approves
2. Agree the scope of the accuracy pass with the user
3. For each entry in scope, verify the summary against the source text
4. Fix errors in the entries, then regenerate and re-check
5. Report results
</required>

# Auditing Papers

Announce at start: "I'm using the Audit Papers skill to check the papers structure and verify summary accuracy."

Structure is the tool's job; accuracy is yours. The entry format is the metadata contract in the `add-paper` skill — this skill does not restate it.

## Step 0: Structure

```bash
python3 {{skills_dir}}/paper-index/paper_index.py check .
```

`check` covers what this skill used to list by hand: every top-level `papers/*.pdf` has a `papers/text/` extraction, every `File`/`Text extraction` ref resolves, no PDF is unreferenced, every entry has Focus and One-liner, no `Related` slug dangles, and the generated files are current. If the repo has no generated-block markers it is not on the format yet — say so and stop; converting it is a migration, not an audit.

Report the problems first and ask before fixing:

```
check reports 3 problems:
- papers/Smith_2025_deployment.pdf has no text extraction
- papers/Jones_2024_scaling.pdf is not referenced by any entry
- `chen-25-agents`: One-liner missing

Want me to fix these? (I can extract text, write an entry for Jones via add-paper, and condense Chen; missing PDFs need downloading.)
```

Missing Focus/One-liner fields are the `condense-summary` skill's job. A PDF with no entry goes through `add-paper`.

## Step 1: Scope

Ask the user which scope to use:

- Recent additions: entries changed since the last audit (`git log -p -- PAPER_SUMMARIES.md`)
- A section, or named papers
- Priority: entries whose Key findings carry no number — most likely to be incomplete
- Full audit: every entry (expensive at 100+ papers; use parallel subagents, 5–10 entries each, writing findings to scratch files — never to PAPER_SUMMARIES.md)

One entry takes 2–5 minutes to verify properly. Reference-only entries (no local source) are flagged, not verified, unless the user asks.

## Step 2: Verify each entry against the source

Read `papers/text/<file>.txt` (or the PDF if there is no extraction) and check:

Factual accuracy:
- Do cited numbers match the paper? (percentages, counts, ratios)
- Are benchmark names and results correct?
- Are authors, affiliations, date, and identifiers (arXiv ID, DOI) correct?
- Are method names and architectural claims correct?
- Does the One-liner claim only what the entry body supports?

Completeness:
- Are the main quantitative results in Key findings, with metric, dataset, and baseline?
- Are ranges given where the paper gives them?
- Is the central contribution described accurately?
- Is there a Relevance paragraph?

<system-reminder>Verify against the source text, not the abstract — and against the original table or figure for any number. Key findings are often in results tables the abstract omits.</system-reminder>

## Step 3: Fix

- Factual errors: correct the claim in the entry, noting the source section.
- Missing numbers: add them with context (what was measured, the baseline, the result).
- A One-liner the corrected body no longer supports: rewrite it per `condense-summary`.

Edit entries only — never a generated block. Then:

```bash
python3 {{skills_dir}}/paper-index/paper_index.py index .
python3 {{skills_dir}}/paper-index/paper_index.py check .
```

Stage `PAPER_SUMMARIES.md PAPER_INDEX.md PAPER_RELATED.md` by name.

## Step 4: Report

Per entry: what was verified, what was corrected, what was added. Flag any entry that substantially misrepresents its paper.

# Common Mistakes

- **Correcting a number from memory or the abstract.** Check the paper's table or figure.
- **A number with no context** ("67%" with no metric or baseline). Always say what was measured.
- **Hand-editing PAPER_INDEX.md to fix a row.** Rows are generated; fix the entry and run `index`.
