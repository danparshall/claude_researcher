---
name: add-paper
description: Add a paper to the research collection — Step 0 triage routes to academic or institutional protocol; pipeline runs rename → extract → summary (dual-protocol) → index → BibTeX. Ensures every paper is fully integrated.
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

**If `claude.ai sandbox`:** translate every `git add` / `git commit` / `git push` in this skill into the REST `write_update` / `write_new` recipes from your Project Instructions. Translate local paths like `/Users/<user>/.claude/skills/...` into `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/...` URLs (fetched via WebFetch).

**If `Claude Code`:** follow the skill body as-is.

**If `unknown`:** stop and surface to the user. Don't guess which environment you're in — the cost of a wrong guess (running `git push` in a sandbox with no git, or writing REST calls against a local working tree) is higher than the cost of one round-trip clarification.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

0. Triage — Protocol A or Protocol B (Step 0)
1. Obtain the PDF (Step 1)
2. Extract text (Step 2)
3. Add entry to the master index (Step 3)
4. Read the paper and write a dual-protocol summary entry (Step 4)
5. Update BibTeX if `BIB_FILE` is defined (Step 5)
6. Stage all new files (Step 6)
</required>

## Scope

This skill processes two kinds of documents:

- **Academic-style papers** — research-oriented documents with original empirical or theoretical contribution (journal articles, working papers, dissertations, white papers structured as research). Routed to **Protocol A** by Step 0 triage.
- **Institutional-style reports** — substantive analytical documents that synthesize evidence, position a framework, or advise on policy, but do not present the authors' own original research with a stated hypothesis (G20 background notes, IMF/World Bank/OECD/UN flagship reports, multilateral working-group papers, regional development bank policy reports). Routed to **Protocol B** by Step 0 triage.

For **legislation, government regulatory documents, terms of reference, and consultant deliverables tied to a single project**, use `document-processing` instead — not this skill. (Note: `document-processing` is deferred per Plan 02 Wave 5; the pointer is currently aspirational.)

**Where config keys live.** The four `PROJECT_QUESTION` / `CONDITIONAL_SECTION` / `BIB_FILE` / `PAPERS_INDEX` keys live in the research repo's `STATUS.md` under `## Project parameters`. The two `paper_naming` keys (`paper_naming.academic_format`, `paper_naming.institutional_format`) live in the user's `personal_info.md` under "Operating preferences". The `paper_summaries.structure` knob also lives in `STATUS.md` project parameters.

# Adding a Paper

Announce at start: "I'm using the Add Paper skill to integrate this paper into the collection."

## Step 0: Triage — academic-style or institutional-style?

Open the document and answer three quick questions:

1. Does it have an **abstract** (vs. an *executive summary*)?
2. Does it pose a **research question or hypothesis**?
3. Does it report **new estimates the authors produced from data they analyzed** (rather than synthesizing others' findings)?

- **Two or more "yes"** → **Protocol A** (academic-style). Apply the Protocol A branch at each step that differs.
- **Two or more "no"** → **Protocol B** (institutional-style). Apply the Protocol B branch at each step that differs.

For borderline cases, exercise judgment and flag the call to the user in the conversation. Common borderline cases:

- Multilateral working papers that have abstracts and methods sections but lean heavily on policy framing — usually Protocol A.
- Institutional monographs with chapter-level empirical work — usually Protocol B at the document level (the value is the synthesis).
- Country case studies with descriptive but not causal analysis — usually Protocol B.
- IDB Discussion Papers, Technical Notes, and Working Papers — most have research-paper structure and are Protocol A; monographs and synthesis pieces are Protocol B. Triage on structure, not on the publisher.

The pipeline is identical across protocols. What differs:

| Step | Protocol A | Protocol B |
|---|---|---|
| Filename | `paper_naming.academic_format` | `paper_naming.institutional_format` |
| Summary section (a) | Thesis, research question, contribution | Purpose, commissioning context, position |
| Summary section (b) | Data, sample, identification, effect sizes | Document type, frameworks/databases, headline findings, policy framework |
| Summary section (d) | Standard "relevance" framing | Same plus "what position does this represent" + cross-references |
| BibTeX entry type | `@article` / `@unpublished` | `@techreport` / `@book` / `@inbook` |

For **legislation, government regulatory documents, terms of reference, and consultant deliverables**, route to `document-processing` (see Scope above) — not this skill.

## Step 1: Obtain the PDF

- If the user provides a URL: download to `papers/` using `curl -L -o papers/<filename>.pdf <url>`
- If the user provides a local file path: copy to `papers/`
- If the user just names a paper: search for it and confirm the URL before downloading

**Filename convention:** Read from the user's `personal_info.md` `paper_naming` field, selecting by Step 0 outcome:

- **Protocol A (academic):** `paper_naming.academic_format`, default `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf`. Common-surname disambiguation: render `{Surname}F` (surname + first-name initial, no separator) when collisions are likely — Anglo surnames (Smith, Jones, Patel, Singh) and East Asian (Wang, Li, Chen, Zhang, Liu, Kim, Park, Choi, Tanaka, Suzuki, Sato; use judgment). For solo authors, single surname only (drop the duplicate). `{Slug}` is two-or-three descriptive words in kebab-case. Examples: `Acemoglu_Restrepo__2026--ai-jobs.pdf`, `SmithJ_2024--stress-sleep.pdf`, `Vaswani_Polosukhin__2017--attention-is-all-you-need.pdf`.
- **Protocol B (institutional):** `paper_naming.institutional_format`, default `{Institution}_{ShortTitle}_{Year}.pdf`. Institution = short acronym, lowercase (`imf`, `oecd`, `un`, `idb`, `caf`, `pct`, `g20`, `g7`); for governments, country + agency in camelCase (`brazilRfb`, `mexicoSat`, `chileSii`, `peruSunat`). ShortTitle = two descriptive words in camelCase. Examples: `imf_g20RevenueAdmin_2025.pdf`, `oecd_taxAdmin30_2023.pdf`, `worldBank_taxCapacity_2024.pdf`.

If `paper_naming` is unset in `personal_info.md`, fall back to the defaults above.

**Multi-institution co-publication (Protocol B).** Lead with the principal author institution (the one whose staff produced the document — usually named on the cover). If the document is co-branded by a working group whose members include several institutions, use the working group's acronym (e.g., `pct_capacityDev_2025` rather than naming all four PCT members). When unsure, ask the user.

**Naming ambiguity.** If the naming is ambiguous (e.g., institutional author for a Protocol A paper, no clear publication year, multiple equally-eligible institutions), ask the user before proceeding.

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

The summary structure branches on Step 0 outcome.

### Protocol A — academic-style papers

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

### Protocol B — institutional-style reports

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

**(c) [Conditional section — only if `CONDITIONAL_SECTION` is defined in `STATUS.md` project parameters AND the report has matching content]** — Same conditional logic as Protocol A. Frequently empty for institutional reports with global framing.

**(d) Relevance to the project** — Address two questions specific to institutional reports:
- **Why this matters for `PROJECT_QUESTION`** (from `STATUS.md` project parameters) — standard relevance framing.
- **What position does this report represent?** ("This is the IMF's authoritative public statement on X as of 2025"; "This is the OECD Inclusive Framework's framing of pillar 2 implementation"). Readers want to know what position they are implicitly endorsing or arguing against if they cite it.
- **Cross-references in the existing library.** Institutional reports almost always cite papers already in the project's `papers/` collection. List the matches with relative paths to the existing summaries — this knits the library together and saves future readers a step.
```

**Summary evolution principle.** The (a)–(d) structure above is a **floor, not a ceiling**. As the user works with a paper over time (asking questions, requesting explanations, cross-referencing with other papers), the summary should grow. Expanded summaries with worked examples, accessible explanations of technical concepts, cross-references, and the user's own notes are expected and desirable. Do not trim or reorganize expanded summaries back to the minimal format.

**Important:**

- Read the actual results tables and figures, not just the abstract. Key findings are often buried in the results.
- Always include numerical results with context (e.g., "67% accuracy on X, compared to 52% baseline" not just "67%").
- If the paper is long, focus on the sections most relevant to `PROJECT_QUESTION`.

## Step 5: Update BibTeX (if `BIB_FILE` is defined in STATUS.md project parameters)

If `BIB_FILE` is unset, skip this step silently.

Add a new entry to the project's `.bib` file. The cite key follows the filename convention (matches the filename without the `.pdf` extension — e.g., `Acemoglu_Restrepo__2026--ai-jobs`, `imf_g20RevenueAdmin_2025`).

**Protocol A entries** use `@article` for published work or `@unpublished` for working papers. Required fields: `title`, `author`, `year`, plus `journal` / `note` / `institution` as appropriate. Always include an `abstract = {}` field — copy the paper's abstract verbatim, do not paraphrase.

**Protocol B entries** use `@techreport` for institutional reports, `@book` for monographs published as books, or `@inbook` for chapters within institutional monographs. Required fields for `@techreport`:

- `author = {{Institution Name}}` — **double braces** preserve casing and prevent BibTeX from treating "Fund" or "Bank" as a surname.
- `title`, `institution`, `year`.
- `type` — describe the document type (e.g., "G20 Background Note", "Policy Research Working Paper", "Technical Note").
- `month` — when relevant.
- `note` — for institutional team, lead authors, partner institutions.
- `abstract` — copy from the report's executive summary if no separate abstract exists.

For `@book` / `@inbook`, include `publisher`, `address`, and `isbn` if available.

## Step 6: Stage files

```bash
git add papers/<filename>.pdf papers/text/<filename>.txt PAPER_INDEX.md PAPER_SUMMARIES.md
# If BIB_FILE was updated in Step 5, also add it:
git add <BIB_FILE>
```

Do NOT commit — the user may be adding multiple papers or may want to review first.

# Adding Multiple Papers

If the user asks to add several papers at once:

- Process each paper through all 6 steps (including Step 0 triage) before moving to the next.
- This ensures each paper is fully integrated before context moves on.
- For bulk additions (5+), consider using subagents in parallel for text extraction and summary writing.

# Common Mistakes

**Forgetting Step 0 triage**
- Problem: Skipping triage routes the paper through the wrong protocol — wrong filename convention, wrong section emphasis in the summary, wrong BibTeX entry type.
- Fix: Always start with Step 0. If borderline, flag the call to the user before proceeding rather than silently picking a branch.

**Skipping text extraction**
- Problem: Future sessions can't search or discuss the paper's details without re-parsing the PDF.
- Fix: Always extract, even if the current task doesn't need the text.

**Writing summaries from the abstract only**
- Problem: Abstracts omit key numerical findings, edge cases, and limitations.
- Fix: Read the results/discussion sections; check tables and figures.

**Adding numbers without context**
- Problem: "The model achieved 0.73" means nothing without knowing what was measured, on what data, and what the baseline was.
- Fix: Always include metric name, dataset, and comparison point.

**Forgetting to update PAPER_INDEX when updating PAPER_SUMMARIES**
- Problem: Index and summaries get out of sync.
- Fix: Always update both in the same operation.

**Reading `paper_naming` or `BIB_FILE` from the wrong file**
- Problem: Schema is split per Tier C: user-level `paper_naming.*` lives in `personal_info.md`; per-project `PROJECT_QUESTION` / `CONDITIONAL_SECTION` / `BIB_FILE` / `PAPERS_INDEX` / `paper_summaries.structure` live in `STATUS.md` `## Project parameters`.
- Fix: Read user-level keys from `personal_info.md`; read per-project keys from the research repo's `STATUS.md`.
