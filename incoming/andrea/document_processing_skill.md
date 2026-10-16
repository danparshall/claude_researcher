---
name: document-processing
description: "The document branch of materials processing. Use when a user provides a non-academic, operational/institutional document — legislation, institutional reports, government memos, terms of reference, draft policies, consultant deliverables, budget or program documents — and wants it filed and summarized. Reached from materials_processing_skill.md's Step 0 (Cut 1) when the material is a document rather than a paper; also use directly when the document/paper call is already obvious. Handles text extraction, summarization, folder-level indexing, repo-level materials indexing, and cross-referencing — working in the folder where the document already lives by default. Does NOT triage document-vs-paper (that is materials_processing_skill.md's job), handle academic or institutional papers (the paper protocols do), note-taking, or discussion of documents after processing."
triggers: >-
  Operational and institutional documents (legislation, government reports, operational
  material); routed from Step 0, or directly when the call is obvious
---

# Document Processing Skill

A reusable workflow for building and maintaining a structured library of operational and institutional documents across projects. Handles the full pipeline from uploaded document to indexed, summarized, classified, and cross-referenced entry.

## When to Use

- A user provides a document (PDF, DOCX, or other) and asks to add it to the project's document library
- A user asks to reprocess or update an existing document entry, or to re-verify its summary against the extract (Step 7)

## The document branch of materials processing

This skill is the **document branch** of the materials triage. The
document-vs-paper decision is made upstream in `materials_processing_skill.md`
(Step 0, Cut 1); by the time you are here, that call has been made and the
material is an operational/institutional document — legislation, government
reports, institutional strategies, draft memos, consultant deliverables, terms
of reference, budget documents, policy proposals, program
documents, and similar.

The other branches build a **citation library** (author-centric, BibTeX,
methodology summaries) via the paper protocols. This branch builds an
**operational knowledge base** (source-centric, reliability-classified,
cross-referenced, feeding into drafting). Each registers its output in its own
root index, one row in one index: a paper in the paper-detail index, a document
in the materials index (`typed_index_template.md`).

You don't re-litigate the routing here. If you reached this skill directly and
the material turns out to argue or synthesize like a paper (authors, a thesis, a
methodology section, would earn a BibTeX entry), go back to
`materials_processing_skill.md` Step 0 — the boundary criteria live there now.

> **Predecessor.** Earlier kit versions adjudicated the document-vs-paper
> boundary in two places — a "what this is NOT" section here and the paper
> triage's scope section. The v3.2 materials-triage merge moved that decision
> into `materials_processing_skill.md`; this section no longer carries the
> discriminator, only the routing assumption.

---

## Prerequisites

Before using this skill in a project, the project's CLAUDE.md should define:

1. **Where the document lives** — Documents are heterogeneous and arrive in different places, so location is a per-document decision, not a fixed setup detail. The common case is that the user has *already put the document somewhere* and is telling you to process it ("I put it in `[folder]`, process it"). When that's the case, **work in place**: the document stays where it is, its `extracts/` and `summaries/` subfolders are created alongside it if absent, and its path is recorded in the indexes. When a document arrives with no obvious home, **read the repo's `FOLDER_MAP`s, suggest a home, and confirm with the user before filing** — never infer or hardcode a location, and never read the archetype layer (`archetype_conventions.md` or an archetype spec) at runtime. See Step 0 below.

2. **File naming convention** — How source files are renamed. Default convention:
   ```
   shortdescription_institution_monthyear.ext
   ```
   Rules:
   - All lowercase, underscores instead of spaces
   - Short description: 2–4 words, no articles or prepositions
   - Institution: abbreviated to its usual short form, lowercase (e.g., `moh` for a ministry of health)
   - Month-year: three-letter month + four-digit year (e.g., `feb2026`). If only the year is known, use just the year
   - Extension: source files keep their original extension; extractions use `.md`

3. **Derived file prefixes:**
   - `TEXT_` — raw text extractions, stored in `extracts/`
   - `SUMMARY_` — document summaries, stored in `summaries/`

4. **Reliability labels** *(project-specific — see below)*
5. **Confidentiality labels** *(project-specific — see below)*

If these are not yet defined when the user asks to process a document, ask the user to provide them — or note them as pending and proceed with the extraction and summary steps. Labels can be assigned retroactively.

---

## Reliability Labels

Every document in the library is assigned a reliability label. The label determines how the document can be used during drafting and analysis.

**These labels are project-specific.** Each project defines labels that fit its context. During project setup, ask the user what labels make sense — or defer until the first document arrives and define them then.

### Default labels (adapt to project)

| Label | Meaning | Usage rules |
|-------|---------|-------------|
| **Citable** | Published, final, authoritative. Numbers and statements can be cited directly. | Use as-is. Cite institution + date. |
| **Validated** | Internal or partner document, final version, reviewed. Content is reliable but may not be public. | Use for substance and numbers, but check confidentiality before citing externally. |
| **Under construction** | Draft being actively worked on. Content is directionally correct but may change. | Use for ideas and structure. Verify specific numbers before citing. Note which version/date you used. |
| **Working draft** | Early-stage internal draft. May contain gaps, placeholders, or unverified content. | Use cautiously for orientation only. Do not cite numbers or specific claims without independent verification from a higher-category source. |
| **Flagged — verify with [user]** | Document has known errors or outdated sections, but may contain useful content. | Never use without explicit confirmation from the user. Show the specific content you want to use and ask. |

### Using reliability labels in practice

1. **Check the label first.** Before using any document, look up its reliability label.
2. **Citable and Validated:** Use freely. For Validated documents, check confidentiality before citing in external-facing materials.
3. **Under construction:** Use for ideas and structure. Flag specific numbers as needing verification. Always record the version or date you read.
4. **Working draft:** Orientation only. Do not cite specific numbers or claims without confirming against a higher-category source.
5. **Flagged:** Always ask the user before using anything from a flagged document.
6. **Conflicts between sources:** Prefer the higher-category source. If both are the same category, flag the discrepancy and ask the user.
7. **Logging inputs:** When recording inputs in notes or drafts, always include the document name, folder path, and reliability label.

---

## Confidentiality Labels

Every document summary includes a confidentiality tag. These determine what can be shared in external-facing materials.

### Default labels (adapt to project)

| Tag | Meaning |
|-----|---------|
| `PUBLIC` | Publicly available document (e.g., published reports, legislation, press releases) |
| `INTERNAL` | Internal working document, not for external circulation |
| `CONFIDENTIAL` | Marked "For Official Use Only" or equivalent; restricted distribution |

Apply the most restrictive classification that matches the document's markings or context. When in doubt, classify as `INTERNAL`.

---

## Folder Structure

A document lives wherever the repo's `FOLDER_MAP`s place it — there is no fixed `inputs/` tree this skill imposes. Whatever the containing folder, the document's derived files sit beside it:

```
[containing folder]/          ◄── located per the repo's FOLDER_MAPs (Step 0)
├── FOLDER_MAP.md             the folder's map where the leaf rule gives one: one pointer row at the materials index (Step 4)
├── [source files]
├── extracts/
│   └── TEXT_filename.md
└── summaries/
    └── SUMMARY_filename.md
```

The document's one entry is its row in the repo-level materials index — the lookup that makes documents findable across folders, one row in one index — which is the repo's own (discovered, not named here; see Step 5). The containing folder's `FOLDER_MAP.md`, where the floor's leaf rule gives the folder one, does not re-list the documents: it carries one pointer row naming that index (`FOLDER_MAP_template.md`, the `leaf` kind; Step 4).

---

## Processing Workflow

When a user provides a document and asks to process it:

### Step 0 — Locate the document's home

First read the project's bindings line (`CLAUDE.md`, Document Processing Workflow,
`### Project conventions`; "Setting Up for a New Project" below): a binding still
`deferred`, or no line at all, is asked for now, before the first document is filed.
Then resolve *where the document lives* before doing anything else, because for
documents this is the genuinely variable decision (a paper's home is the one
the archetype fixes for the literature layer; a document's is not).

- **If the user already placed it** ("I dropped it in `[folder]`," "process the
  file in `[folder]`," or it's plainly sitting in a task or source folder) →
  **work in place there.** Create that folder's `extracts/` and `summaries/`
  subfolders if they don't exist. Do not relocate the document to match any
  convention.
- **If there's no obvious home** → read the repo's `FOLDER_MAP`s, **suggest** a
  home that fits the existing structure, and **confirm with the user before
  filing.** Never infer or hardcode a location; never read the archetype layer (`archetype_conventions.md` or an archetype spec) at runtime.

Whichever applies, the document's actual path is what gets recorded in
the repo-level materials index (Step 5) — so the item is findable wherever it
sits.

### Step 1 — Rename using the project's convention

Rename the file following the project's naming convention. If the naming is ambiguous (e.g., no clear date, uncertain institution), ask the user before proceeding.

### Step 2 — Text extraction

- **For PDFs:** Attempt text extraction with PyMuPDF (`fitz`). If fewer than 100 words are extracted, classify the file as **SCANNED PDF** and note it in the summary's header (`Extraction status`) and the document's row in the repo-level materials index. Do not attempt OCR — flag it to the user for manual review.
- **For DOCX files:** Extract text including table cells (not just paragraph text — many institutional documents use tables). Use `python-docx` with table iteration.
- **For large files (>1MB on GitHub):** read them per `github_api_workflow_skill.md` (on the web branch, the authority's `gh_read`), which handles files the contents API truncates over 1MB.
- Save the extraction as `TEXT_filename.md` in the folder's `extracts/` subfolder. The filename must match the source file's name (under the naming convention), with the `TEXT_` prefix and `.md` extension.

#### Language rule — extraction language, and the English reading copy

- **The extract is always in the document's source language.** It is the ground truth for everything derived from it; translation at extraction is where scope drift enters, and a translated extract cannot be checked against the original without re-doing the extraction.
- **The summary is always written from the source-language extract, never from a translation.** A summary written from a translation is a derivative of a derivative: if the translation drops a scope qualifier, the summary inherits the drop and the original moves two layers away instead of one.
- **If the document's language is not one the user reads** (their reading languages are declared in the repo's `CLAUDE.md`; default English), **ask the user whether to create an English reading copy — do not create one by default.** They authorize per document; the cost is real (a full translation of a long extract is a session's work) and the need only bites when the document becomes load-bearing for a deliverable.
  - **If authorized:** create `TEXT_ENGLISH_filename.md` in the same `extracts/` subfolder, a full English translation of the extract. Its header must declare its status: *derived from `TEXT_filename.md`; the user's reading copy for audit; never a verification target and never citable — verification of any claim runs against the source-language extract or the original.* Load-bearing figures, legal instruments, and technical terms keep the source's verbatim words in parentheses beside the translation — e.g., "the permit remains suspended (*bleibt ausgesetzt*)" — so the exact words a verdict rests on are visible without opening the source file.
  - **If declined or not yet requested:** the index row's `Forms` cell lists the forms held, so the absence of an English reading copy stays visible there.
- **Tables and figures are the exception where translation-first is fine:** numbers carry no scope-drift risk, and a translated table is directly checkable cell against cell.

### Step 3 — Document summary

Write a summary and save it as `SUMMARY_filename.md` in the folder's `summaries/` subfolder. Follow this structure:

**Header block:**
- **Source file:** Reference to the source filename
- **Confidentiality:** The appropriate tag
- **Reliability:** The appropriate label
- **File metadata:** File type, extraction status, word count, author (if known), date
- **Document description:** One sentence on what the document is

**Body — mirror the original document's structure:**
- The summary must follow the same section and subsection structure as the original document. Use the original headings (translated to the project's working language if needed). Do not reorganize, merge, or skip sections.
- Every section in the original gets a corresponding section in the summary — even if the content seems minor. The reader should see that everything was covered.
- Each section's summary should be comprehensive enough that the reader gets a solid grasp of what the section says without opening the source. Include: key arguments, specific data points (numbers, percentages, dates, names), policy positions, recommendations, and any caveats or qualifications the authors make.
- **For documents in a language the user does not read (outside the reading languages declared in the repo's `CLAUDE.md`; default English): every load-bearing figure or claim in the summary carries the source's verbatim words inline, with the English rendering beside them** — so scope qualifiers are visible in the summary itself without opening the extract. This is the audit surface when no English reading copy exists.
- Do not filter for project relevance or infer what the reader might want. Summarize what the document actually says, completely and neutrally. Project relevance notes can be added at the end of each section as a separate clearly-marked paragraph, but they must not replace or shorten the substantive summary.

**Footer:**
- **From the visual layer:** anything established by *looking* at a figure, chart, map, photograph, or a table the extraction garbled — stated as such, with what was checked and what it showed. Usually empty, and cheap when it is not: the processor is the only actor in the pipeline who ever has the source open, so this is the one moment such facts can be captured — a finding that lives only in the visual layer is unrecoverable downstream from the text extraction and the summary, at any cost. A **deliberately empty** note is itself informative ("figures reviewed; nothing load-bearing beyond the text"). An image-only scan with no text layer is declared here; where the summary's scope otherwise stops at the text, saying so is what lets a downstream reader tell "the document does not say" from "this summary did not look."
- **Template value** (if applicable): For reference documents from other contexts (e.g., a program document from another country, a reform law from a peer), note what structural or design lesson the document offers for the current project. Example: "This program's monitoring design — a short list of indicators with a fixed review calendar — is a useful template for structuring the monitoring section of our project."
- **Cross-references:** Links to related documents in other folders.
- **Glossary of acronyms** (if the document introduces terms not already defined in other summaries).

#### Worked example — summary structure

```markdown
# Summary — [filename].pdf

**Source file:** `[folder]/[filename].pdf`
**Confidentiality:** `[PUBLIC / INTERNAL / CONFIDENTIAL]`
**Reliability:** `[label]`
**Type:** [file type — e.g., PDF — Program Document]
**Extraction status:** [Full text extractable / Scanned — flagged for manual review]
**Word count:** ~[N]
**Author:** [institution or person]
**Date:** [month year]

---

## Document Description

[One paragraph: what the document is, its scope, key structural features.]

---

## [Section heading from original document] (¶1–N)

**[Subsection topic] (¶1):** [Summary with specific data points — percentages,
dollar amounts, dates, institutional names. Not vague.]

**[Subsection topic] (¶2):** [Continue mirroring the document's structure.]

---

## From the Visual Layer

[What was established by looking at figures, charts, maps, or garbled tables — stated as such, with what was checked and what it showed. Or: "Figures reviewed; nothing load-bearing beyond the text."]

---

## Cross-References

- **[Related doc]:** `[folder]/[filename]` — [why this connection matters]

---

## Glossary of Acronyms

| Acronym | Full name | What it is |
|---------|-----------|------------|
| **[ABC]** | [Full Name] | [Brief plain-language explanation] |
```

**Key features to replicate:**
- Header block with all metadata fields populated.
- Document description: one paragraph with the document's full name, scope, and key structural features.
- Body sections mirror the original's structure. Paragraph references (¶1, ¶2...) help locate content in the source.
- Each section includes specific data points (percentages, dollar amounts, dates, institutional names) — not vague summaries.
- Cross-references link to other documents in the repo with a note on why the connection matters.
- Glossary includes a "What it is" column — especially useful for institutional terms that are unfamiliar even when spelled out.

### Step 4 — Check the folder's `FOLDER_MAP.md` pointer row

The document's one entry is its row in the materials index (Step 5); the containing folder's map points at that index and never re-lists the documents, since a second list of the same files would drift from the first (`FOLDER_MAP_template.md`, the `leaf` kind: one pointer row naming the index, never a re-list). So the map is not touched per document:

- **The folder's map already carries its pointer row at the materials index** → nothing to do.
- **The folder was born by this run** → the floor's leaf rule decides whether it carries a map (`structure_conventions.md`: a leaf born on content that a typed index enumerates fully carries none); where it does, the map is written at birth in the template's `leaf` form, with that one pointer row.
- **A folder whose files no typed index registers** keeps a row per file (the template's own rule for that case).

The metadata — confidentiality, reliability, file type and extraction status, word count, date and author — lives in the summary's header block (Step 3), the cross-references in its footer; a map row carries no status, count or date (a status is a live claim with its home elsewhere: the summary, and in a research repo the `MATERIALS_INDEX` row).

### Step 5 — Update the indexes

Register the document in the repo's **existing repo-level materials index** — the lookup that makes documents findable across folders, one row in one index (a paper's row is in the paper-detail index, not here). Find that index by reading the repo's `FOLDER_MAP`s (the root map's root-documents block names it); **do not assume a particular index name.** Add the document's row in the header row that index carries (`typed_index_template.md`: `Item · About · Where · Forms`, a research repo's `MATERIALS_INDEX` row adding `Reliability` and `Confidentiality`), in the section its head says it takes: the item's name, `About` in Claude's words (what the document is — a law, a decree, a manual, a strategy document — its subject, its setting, about fifteen words; read the index first, and a subject already named keeps its words), its path from Step 0, and the forms held in reading order (`summary · extract · original`). Keep the row a pointer — outside a research repo's `MATERIALS_INDEX` the reliability/confidentiality detail stays in the summary, and the section-level content always does. If the new document creates important cross-references, record those in the summary's Cross-References footer (Step 3).

### Step 6 — Check for duplicates

Before finalizing, check if an identical or near-identical file already exists in the repo. If it does, flag it to the user — do not keep both without explicit instruction.

### Step 7 — Re-verify an existing summary (optional, on the user's ask)

An optional step, run only when the user asks for it ("re-verify this summary," "check the
summaries against their extracts"): the summary is checked claim by claim against its `TEXT_`
extract and fixed.

- **The check.** A subagent on a lower tier reads only the summary and its extract, nothing
  else in the repo, and returns a verdict per claim: `supported`, `imprecise` (the extract says
  it, with a qualifier or number the summary drops or bends), `unsupported` (nothing in the
  extract says it), `contradicted`. These are the one-source form of the verification core's
  six (`agent_research_verification_skill.md`, Step 7): with one held extract nothing is
  unverifiable and there is no citation to misattribute.
- **The fix.** The session re-checks every flagged claim against the extract before touching
  the summary; a flag that does not hold is dropped. Then it edits: an `imprecise` or
  `contradicted` claim is corrected to the extract's words, an `unsupported` claim comes out.
  Where a summary marks its own inferences (`[INF]`), an inference is checked for a traceable
  basis in the extract, not for a matching sentence. The structure is not rewritten; a summary
  that has grown past the floor keeps its growth.
- **The record.** One line in the summary's header, **Verified against the extract:** the
  date, the checking model, and the counts (claims, flagged, corrected, removed). A later check
  replaces the line. The index row and the folder's map do not change; the summary is the one home
  of its own status.

---

## Versioning

When a document is updated (new draft of the same document):
- Rename by appending `_v01`, `_v02`, etc.: `concept_note_institution_mar2026_v01.docx`, `concept_note_institution_mar2026_v02.docx`
- Update the document's repo-level materials index row to reflect the new version (the folder's map points at the index and does not change; Step 4)
- If the previous version's summary and extraction are still in the repo, note which version they correspond to

---

## Infrastructure Files

These files are part of the repo structure and are **never renamed:**
- `FOLDER_MAP.md` — one per containing folder (its one pointer row names the materials index, which registers the documents; Step 4)
- The repo's repo-level materials index — the lookup for every non-paper material, at the repo root (papers are in the paper-detail index); its name is the repo's own, discovered from the root map's root-documents block, not fixed by this skill
- `CLAUDE.md`, `README.md` — repo-level infrastructure

---

## Setting Up for a New Project

This skill does **not** build a repo's folder or index structure — that is born at repo setup, owned by the archetype scaffold (`new_repo_setup.md` and `research_setup_scaffold.md`). When a user asks to "set up document processing" for a new project, configure the skill's project-specific parameters; do not hand-create folders or indexes.

The skill needs four **bindings** from the project, and nothing in the repo notices when one is missing unless they are written down as a checklist. At setup, write the checklist into the project's `CLAUDE.md` Document Processing section, under `### Project conventions`, one line per binding with its state — `bound: <the value or "kit default">` or `deferred until the first document`:

1. **Reliability labels** — the project's set, or the kit defaults above. Present the defaults and ask the user to customize; deferring until the first document arrives is fine.
2. **Confidentiality labels** — same approach. The PUBLIC / INTERNAL / CONFIDENTIAL defaults work for most institutional projects.
3. **Naming convention** — present the default (`shortdescription_institution_monthyear.ext`) and ask if it needs modification.
4. **The materials-index home** — bound means the archetype's `MATERIALS_INDEX` exists with its header row and the root map's root-documents block names it (Step 0 discovers it from there at run time); a NONE repo names the index it uses.

**Step 0 of the workflow reads the checklist at every document** and, before filing the first one, asks for every binding still `deferred`; nothing reads the absence between documents, because a deferred binding is legitimate until a document arrives. A checklist absent from `CLAUDE.md` in a repo where the skill is active is read as all four deferred.

**Pre-v4 repos (no archetype structure yet).** If the repo predates the archetype scaffold and lacks a repo-level materials index or per-folder `FOLDER_MAP`s, **flag the missing structure as a migration gap** and surface it to the user — do not hand-build a folder or index tree, which risks materializing a layout the repo's archetype would not have. Proceed with extraction and summary in place; record the migration gap so the structure can be regularized when the repo is brought onto the current kit.

---

## Edge Cases

- **Scanned PDFs:** Do not attempt OCR. Note the file as scanned in the summary's header and the document's repo-level materials index row, and flag it to the user for manual review.
- **Non-text-primary documents:** Spreadsheets, slide decks, and databases may need adapted extraction. Flag to the user and discuss approach.
- **Documents in other languages:** Extract text as-is. Summaries are written in the project's working language (translate if needed).
- **Very short documents** (cover letters, 1-page memos): Still follow the workflow, but the summary may be shorter than the original. The value is in the classification, indexing, and cross-referencing.
- **Documents without clear dates or authors:** Ask the user. If unknown, note it in the metadata as "Date unknown" or "Author unknown."
- **Bundled documents** (e.g., a PDF containing multiple separate reports): Ask the user whether to treat as one document or split into separate entries.

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
