---
name: paper-processing-academic
description: Protocol A workflow for academic-style papers — rename → extract → index → dual-protocol summary (Protocol A shape) → BibTeX → stage. Triage by `add-paper` Step 0 routes here.
nori_researcher_source: nori-skillsets add-paper v1.0.0 (ported to claude_researcher in 0bbd419, 2026-05-10)
aitaxbid_source: ~/code/AITaxBID/skills/paper_processing.md@e0a736d (2026-05-02)
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

**If `claude.ai sandbox`:** the user's project repo is already cloned at `/home/claude/<REPO>/` per `RESEARCHER.md` §2.0b — run the `git add` / `git commit` / `git push` commands and any other file write in this skill directly from that working tree. Translate local skill paths like `/Users/<user>/.claude/skills/...` to the template clone at `/home/claude/.claude_researcher_template/template/skills/...`. Only if the §2.0b clone failed (degraded REST fallback, surfaced to the user) do you translate `git add` / `git commit` / `git push` and any other file write into the Contents API recipes from your Project Instructions.

**If `Claude Code`:** follow the skill body as-is.

**If `unknown`:** stop and surface to the user. Don't guess which environment you're in — the cost of a wrong guess (operating against the wrong working tree, or using the wrong write path for the environment) is higher than the cost of one round-trip clarification.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Obtain the PDF (Step 1)
2. Extract text (Step 2)
3. Add entry to the master index (Step 3)
4. Read the paper and write a Protocol A summary entry (Step 4)
5. Update BibTeX if `BIB_FILE` is defined (Step 5)
6. Stage all new files (Step 6)
</required>

# Adding an Academic Paper

Announce at start: "I'm using the paper-processing-academic skill (Protocol A — academic paper)."

This skill handles the Protocol A workflow for academic-style papers. Triage to Protocol A was already done by `add-paper` Step 0 — if you're reading this skill directly without going through `add-paper`, confirm the document is academic-style before proceeding (abstract present, research question/hypothesis, original empirical or theoretical contribution from data the authors analyzed).

**Configuration keys.** `PROJECT_QUESTION`, `CONDITIONAL_SECTION`, `BIB_FILE`, `PAPERS_INDEX`, `paper_summaries.structure` live in the research repo's `STATUS.md` under `## Project parameters`. The filename format key `paper_naming.academic_format` lives in the user's `personal_info.md` under "Operating preferences". See `add-paper/SKILL.md` Scope section for the full schema split.

## Step 1: Obtain the PDF

- If the user provides a URL: download to `papers/` using `curl -L -o papers/<filename>.pdf <url>`
- If the user provides a local file path: copy to `papers/`
- If the user just names a paper: search for it and confirm the URL before downloading

**Filename convention.** Read `paper_naming.academic_format` from `personal_info.md`, default `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf`. Common-surname disambiguation: render `{Surname}F` (surname + first-name initial, no separator) when collisions are likely — Anglo surnames (Smith, Jones, Patel, Singh) and East Asian (Wang, Li, Chen, Zhang, Liu, Kim, Park, Choi, Tanaka, Suzuki, Sato; use judgment). For solo authors, single surname only (drop the duplicate). `{Slug}` is two-or-three descriptive words in kebab-case. Examples: `Acemoglu_Restrepo__2026--ai-jobs.pdf`, `SmithJ_2024--stress-sleep.pdf`, `Vaswani_Polosukhin__2017--attention-is-all-you-need.pdf`.

**First-use prompt.** If `paper_naming.academic_format` is unset (no `- **Paper naming (academic):**` line in `personal_info.md`'s "Operating preferences" section), treat this as a first-use case. Show the default plus one example (`Acemoglu_Restrepo__2026--ai-jobs.pdf`) and ask: "Use this format, or give me a different one? (Enter to accept the default.)" Persist the chosen value as `- **Paper naming (academic):** <value>` appended after the last existing `- **...:**` line in "Operating preferences"; if the line already exists (race with a concurrent edit), leave it as-is. `personal_info.md` lives in the user's config repo (`claude_research_config` by default). The same format is reused for every subsequent academic paper; ask once, never again.

**Naming ambiguity.** If the naming is ambiguous (e.g., no clear publication year, multiple equally-eligible first-author orderings), ask the user before proceeding.

If the paper already exists in `papers/`, skip to Step 2.

## Step 2: Extract text

Extract the PDF text to `papers/text/` with the same base filename and `.txt` extension:

```bash
# Using pdftotext if available
pdftotext papers/<filename>.pdf papers/text/<filename>.txt

# If pdftotext is not available, use Python
python3 -c "
import subprocess
result = subprocess.run(['python3', '-m', 'pymupdf', 'convert', '-output', 'papers/text/<filename>.txt', 'papers/<filename>.pdf'])
"
```

If neither tool works, read the PDF directly using the Read tool and write the extracted content to `papers/text/<filename>.txt`. This is the fallback — it works but may lose some formatting.

Verify the extraction is reasonable: check the first ~20 lines to confirm it's not garbled.

## Step 3: Add to the master index

The index filename is `PAPERS_INDEX` from `STATUS.md` `## Project parameters` (default `PAPER_INDEX.md`).

Add a one-line entry in the appropriate section (or create a section if needed):

```markdown
| Author (Year) | One-sentence description of what the paper contributes | `filename.pdf` |
```

Keep entries sorted by author within each section. If the index file doesn't exist yet, create it:

```markdown
# Paper Index

| Paper | Description | File |
|-------|-------------|------|
| Author (Year) | One-sentence description | `filename.pdf` |
```

## Step 4: Add to PAPER_SUMMARIES.md

Read the paper (use the extracted text from `papers/text/`). Write a summary entry to the file determined by `paper_summaries.structure` from `STATUS.md` `## Project parameters`:

- **`single-file`** (default) — append to `PAPER_SUMMARIES.md` at the repo root.
- **`per-file`** — the config knob exists but the per-file code path is **not yet implemented** in this version of `add-paper`. **Warn the user inline** with this text: *"Note: `paper_summaries.structure: per-file` is configured but the per-file code path isn't implemented in this version of `add-paper`. Falling back to `single-file` (appending to `PAPER_SUMMARIES.md`) for this paper. The config knob is honored once per-file ships."* Then proceed with the single-file branch.

Use the Protocol A summary template:

```markdown
### Paper Title

- Authors: Names (Affiliations)
- Date: Month Year
- File: `filename.pdf`
- Source: [URL or DOI if available]

**(a) What the paper argues** — Main thesis, research question, and contribution to the literature.

**(b) Methodology & key findings** — Precise and detailed. Include:
- Data sources and sample: who, where, when, how many observations.
- Method: RCT, diff-in-diff, calibration, survey, structural model, etc.
- How key variables are constructed: exposure measures, outcome variables, controls.
- Identification strategy (if empirical) or key assumptions (if theoretical).
- Core results: effect sizes, magnitudes, main takeaways.

The description must be specific enough that someone can understand the methodology without reading the paper. Not vague ("uses cross-country data") but detailed ("uses PIAAC microdata for 23 OECD countries, 2012–2015, linking Felten AIOE scores crosswalked to ISCO-08 to individual-level employment outcomes via OLS with occupation × country fixed effects").

**(c) [Conditional section — only if `CONDITIONAL_SECTION` is defined in `STATUS.md` project parameters AND the paper has matching content]** — Extract all findings matching the project's filter. Only include this section if the paper actually contains matching data.

**(d) Relevance to the project** — How this paper connects to `PROJECT_QUESTION` (from `STATUS.md` project parameters). Why it matters, what it contributes, what gaps it fills.
```

**Summary evolution principle.** The (a)–(d) structure above is a **floor, not a ceiling**. As the user works with a paper over time (asking questions, requesting explanations, cross-referencing with other papers), the summary should grow. Expanded summaries with worked examples, accessible explanations of technical concepts, cross-references, and the user's own notes are expected and desirable. Do not trim or reorganize expanded summaries back to the minimal format.

**Important:**

- Read the actual results tables and figures, not just the abstract. Key findings are often buried in the results.
- Always include numerical results with context (e.g., "67% accuracy on X, compared to 52% baseline" not just "67%").
- If the paper is long, focus on the sections most relevant to `PROJECT_QUESTION`.

## Step 5: Update BibTeX (if `BIB_FILE` is defined in STATUS.md project parameters)

If `BIB_FILE` is unset, skip this step silently.

Add a new entry to the project's `.bib` file. The cite key follows the filename convention (matches the filename without the `.pdf` extension — e.g., `Acemoglu_Restrepo__2026--ai-jobs`).

Use `@article` for published work or `@unpublished` for working papers. Required fields: `title`, `author`, `year`, plus `journal` / `note` / `institution` as appropriate. Always include an `abstract = {}` field — copy the paper's abstract verbatim, do not paraphrase.

## Step 6: Stage files

```bash
git add papers/<filename>.pdf papers/text/<filename>.txt PAPER_INDEX.md PAPER_SUMMARIES.md
# If BIB_FILE was updated in Step 5, also add it:
git add <BIB_FILE>
```

Do NOT commit — the user may be adding multiple papers or may want to review first.

# Adding Multiple Academic Papers

If the user asks to add several academic papers at once:

- Process each paper through all 6 steps (after `add-paper` Step 0 triage routes each one here) before moving to the next.
- This ensures each paper is fully integrated before context moves on.
- For bulk additions (5+), consider using subagents in parallel for text extraction and summary writing.

# Common Mistakes

**Writing summaries from the abstract only**
- Problem: Abstracts omit key numerical findings, edge cases, and limitations.
- Fix: Read the results/discussion sections; check tables and figures.

**Adding numbers without context**
- Problem: "The model achieved 0.73" means nothing without knowing what was measured, on what data, and what the baseline was.
- Fix: Always include metric name, dataset, and comparison point.

**Forgetting to update PAPER_INDEX when updating PAPER_SUMMARIES**
- Problem: Index and summaries get out of sync.
- Fix: Always update both in the same operation.
