---
name: paper-processing-institutional
description: Protocol B workflow for institutional-style reports — rename → extract (institutional rules: preserve acronyms / boxes / figure captions) → index → dual-protocol summary (Protocol B shape) → BibTeX → stage. Triage by `add-paper` Step 0 routes here.
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
2. Extract text — apply institutional front-matter rules (Step 2)
3. Add entry to the master index (Step 3)
4. Read the report and write a Protocol B summary entry (Step 4)
5. Update BibTeX if `BIB_FILE` is defined (Step 5)
6. Stage all new files (Step 6)
</required>

# Adding an Institutional Report

Announce at start: "I'm using the institutional report skill (Protocol B — institutional report)."

This skill handles the Protocol B workflow for institutional-style reports. Triage to Protocol B was already done by `add-paper` Step 0 — if you're reading this skill directly without going through `add-paper`, confirm the document is institutional-style before proceeding (no abstract / executive summary instead; no own hypothesis; synthesis or position document from a multilateral, government, or working-group publisher).

**Configuration keys.** `PROJECT_QUESTION`, `CONDITIONAL_SECTION`, `BIB_FILE`, `PAPERS_INDEX`, `paper_summaries.structure` live in the research repo's `STATUS.md` under `## Project parameters`. The filename format key `paper_naming.institutional_format` lives in the user's `personal_info.md` under "Operating preferences". See `add-paper/SKILL.md` Scope section for the full schema split.

## Step 1: Obtain the PDF

- If the user provides a URL: download to `papers/` using `curl -L -o papers/<filename>.pdf <url>`
- If the user provides a local file path: copy to `papers/`
- If the user just names a report: search for it and confirm the URL before downloading

**Filename convention.** Read `paper_naming.institutional_format` from `personal_info.md`, default `{Institution}_{ShortTitle}_{Year}.pdf`. Institution = short acronym, lowercase (`imf`, `oecd`, `un`, `idb`, `caf`, `pct`, `g20`, `g7`); for governments, country + agency in camelCase (`brazilRfb`, `mexicoSat`, `chileSii`, `peruSunat`). ShortTitle = two descriptive words in camelCase. Examples: `imf_g20RevenueAdmin_2025.pdf`, `oecd_taxAdmin30_2023.pdf`, `worldBank_taxCapacity_2024.pdf`.

**First-use prompt.** If `paper_naming.institutional_format` is unset (no `- **Paper naming (institutional):**` line in `personal_info.md`'s "Operating preferences" section), treat this as a first-use case. Show the default plus one example (`imf_g20RevenueAdmin_2025.pdf`) and ask: "Use this format, or give me a different one? (Enter to accept the default.)" Persist the chosen value as `- **Paper naming (institutional):** <value>` appended after the last existing `- **...:**` line in "Operating preferences"; if the line already exists (race with a concurrent edit), leave it as-is. `personal_info.md` lives in the user's config repo (`claude_research_config` by default). The same format is reused for every subsequent institutional report; ask once, never again.

**Multi-institution co-publication.** Lead with the principal author institution (the one whose staff produced the document — usually named on the cover). If the document is co-branded by a working group whose members include several institutions, use the working group's acronym (e.g., `pct_capacityDev_2025` rather than naming all four PCT members). When unsure, ask the user.

**Naming ambiguity.** If the naming is ambiguous (e.g., institutional author for what looks like an academic-style paper — go back through triage if so, no clear publication year, multiple equally-eligible institutions), ask the user before proceeding.

If the report already exists in `papers/`, skip to Step 2.

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

**Institutional reports often have heavy front matter** (foreword, acknowledgments, list of acronyms, list of figures and boxes). Three specific rules apply:

- **Preserve the acronym list verbatim.** Institutional acronyms (TADAT, ISORA, RA-GAP, PIAAC, etc.) are reference material for downstream work. The list usually appears in the report's front matter; keep it intact in the extracted text.
- **Preserve boxes and figure captions with their key data.** These often carry the report's quotable findings — numbers and statements that the executive summary omits. Capture the box/figure caption text and any tables it contains.
- **Strip decorative front matter** (forewords, dedications) unless they contain substantive framing. The line is judgment-based: if the foreword contains a thesis statement or policy position the report is building on, keep it; if it's pure ceremony, drop it.

Verify the extraction is reasonable: check the first ~20 lines to confirm it's not garbled.

## Step 3: Add to the master index

The index filename is `PAPERS_INDEX` from `STATUS.md` `## Project parameters` (default `PAPER_INDEX.md`).

Add a one-line entry in the appropriate section (or create a section if needed):

```markdown
| Institution (Year) | One-sentence description of what the report contributes | `filename.pdf` |
```

If the project's index format has an "Outlet" column (or similar), describe the document type rather than a journal — examples: "IMF G20 background note", "World Bank Policy Research Working Paper", "OECD policy paper", "IDB Technical Note IDB-TN-XXXX", "UN flagship report".

Keep entries sorted by institution within each section. If the index file doesn't exist yet, create it:

```markdown
# Paper Index

| Paper | Description | File |
|-------|-------------|------|
| Institution (Year) | One-sentence description | `filename.pdf` |
```

## Step 4: Add to PAPER_SUMMARIES.md

Read the report (use the extracted text from `papers/text/`). Write a summary entry to the file determined by `paper_summaries.structure` from `STATUS.md` `## Project parameters`:

- **`single-file`** (default) — append to `PAPER_SUMMARIES.md` at the repo root.
- **`per-file`** — the config knob exists but the per-file code path is **not yet implemented** in this version of `add-paper`. **Warn the user inline** with this text: *"Note: `paper_summaries.structure: per-file` is configured but the per-file code path isn't implemented in this version of `add-paper`. Falling back to `single-file` (appending to `PAPER_SUMMARIES.md`) for this report. The config knob is honored once per-file ships."* Then proceed with the single-file branch.

Use the Protocol B summary template:

```markdown
### Report Title

- Institution: Name(s)
- Date: Month Year
- File: `filename.pdf`
- Source: [URL or DOI if available]

**(a) What the report argues** — Purpose of the document, who commissioned it (or the request context — G20 ask, presidency mandate, board request), the principal thesis or position, and how it relates to prior or companion reports from the same institution. The "argues" framing applies even when the report seems neutral — institutional reports always carry a position, even if implicit.

**(b) Document type, methods, and findings** — Cover:
- **Document provenance:** what kind of report this is (background note, flagship, working paper, monograph, technical note); commissioning context; institutional team and lead authors; companion reports if part of a series; partner institutions consulted.
- **Frameworks and databases drawn on:** which institutional tools or datasets are used (e.g., for tax/fiscal: TADAT, ISORA, RA-GAP, IDB MICs survey; for macro: WEO, IFS; for trade: COMTRADE). Name them so the user can locate underlying sources.
- **Headline synthesized findings:** the report's main numerical claims or qualitative conclusions, with their underlying citation when the report attributes them. Be explicit when a number is *the report's own synthesis* versus *a number it borrows from a cited paper* (cite the original where given).
- **Policy framework or recommendations:** the structured guidance the report offers — typology of reforms, decision frameworks, sequencing logic, country-typology distinctions (advanced economies / emerging markets / low-income developing countries / fragile states).
- **Country case studies, if any:** which countries are profiled and what for.

The precision principle still applies: name the tools, name the countries, name the underlying papers. "Synthesizes IMF research" is not enough — say which papers, which datasets, which estimates.

**(c) [Conditional section — only if `CONDITIONAL_SECTION` is defined in `STATUS.md` project parameters AND the report has matching content]** — Same conditional logic as the academic-paper protocol. Frequently empty for institutional reports with global framing.

**(d) Relevance to the project** — Address two questions specific to institutional reports:
- **Why this matters for `PROJECT_QUESTION`** (from `STATUS.md` project parameters) — standard relevance framing.
- **What position does this report represent?** ("This is the IMF's authoritative public statement on X as of 2025"; "This is the OECD Inclusive Framework's framing of pillar 2 implementation"). Readers want to know what position they are implicitly endorsing or arguing against if they cite it.
- **Cross-references in the existing library.** Institutional reports almost always cite papers already in the project's `papers/` collection. List the matches with relative paths to the existing summaries — this knits the library together and saves future readers a step.
```

**Summary evolution principle.** The (a)–(d) structure above is a **floor, not a ceiling**. As the user works with a report over time (asking questions, requesting explanations, cross-referencing with other reports), the summary should grow. Expanded summaries with worked examples, accessible explanations of technical concepts, cross-references, and the user's own notes are expected and desirable. Do not trim or reorganize expanded summaries back to the minimal format.

**Important:**

- Read the actual results tables, boxes, and figure captions, not just the executive summary. Institutional reports often bury their key numbers in boxes and figures.
- Always include numerical results with context (e.g., "67% of LICs report capacity gaps in X, compared to 22% of advanced economies" not just "67%").
- If the report is long, focus on the sections most relevant to `PROJECT_QUESTION`.

## Step 5: Update BibTeX (if `BIB_FILE` is defined in STATUS.md project parameters)

If `BIB_FILE` is unset, skip this step silently.

Add a new entry to the project's `.bib` file. The cite key follows the filename convention (matches the filename without the `.pdf` extension — e.g., `imf_g20RevenueAdmin_2025`, `worldBank_taxCapacity_2024`).

Use `@techreport` for institutional reports. Required fields:

- `author = {{Institution Name}}` — **double braces** preserve casing and prevent BibTeX from treating "Fund" or "Bank" as a surname.
- `title`, `institution`, `year`.
- `type` — describe the document type (e.g., "G20 Background Note", "Policy Research Working Paper", "Technical Note").
- `month` — when relevant.
- `note` — for institutional team, lead authors, partner institutions.
- `abstract` — copy from the report's executive summary if no separate abstract exists.

For **monographs published as books**, use `@book` with `publisher`, `address`, and `isbn` if available. For **chapters within institutional monographs**, use `@inbook` referring back to the parent `@book` entry.

## Step 6: Stage files

```bash
git add papers/<filename>.pdf papers/text/<filename>.txt PAPER_INDEX.md PAPER_SUMMARIES.md
# If BIB_FILE was updated in Step 5, also add it:
git add <BIB_FILE>
```

Do NOT commit — the user may be adding multiple reports or may want to review first.

# Adding Multiple Institutional Reports

If the user asks to add several institutional reports at once:

- Process each report through all 6 steps (after `add-paper` Step 0 triage routes each one here) before moving to the next.
- This ensures each report is fully integrated before context moves on.
- For bulk additions (5+), consider using subagents in parallel for text extraction and summary writing.

# Common Mistakes

**Reading only the executive summary**
- Problem: Institutional reports often bury key numbers in boxes and figure captions, which the executive summary omits.
- Fix: Scan the boxes and figures captured by Step 2's preserve-boxes rule; read the body sections relevant to the project question.

**Stripping the acronym list during extraction**
- Problem: Institutional acronyms (TADAT, ISORA, RA-GAP, etc.) are reference material that downstream summaries and cross-references rely on; losing them in front-matter cleanup costs more than the lines saved.
- Fix: Apply Step 2's "preserve the acronym list verbatim" rule before any front-matter trimming.

**Adding numbers without context**
- Problem: "67% of countries" means nothing without knowing which countries, what they were measured on, and what the comparison group is.
- Fix: Always include the cohort, the measurement, and the comparison point.

**Forgetting to update PAPER_INDEX when updating PAPER_SUMMARIES**
- Problem: Index and summaries get out of sync.
- Fix: Always update both in the same operation.
