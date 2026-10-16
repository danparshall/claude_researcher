---
name: paper-processing-academic
description: Protocol A for processing academic-style papers (journal articles, working papers, dissertations, white papers with original empirical or theoretical contribution). Invoked from materials_processing_skill.md's Step 0 triage when the document has two or more of (abstract, research question/hypothesis, original estimates from authors' own data). Covers renaming, text extraction, comprehensive summary writing, index registration, a bibliography entry, and setting Claude status. Use directly when the protocol is already known; otherwise start from materials_processing_skill.md.
triggers: >-
  Academic-style papers (abstract, hypothesis, original estimates); routed from Step 0, or
  directly when the protocol is known
---

# Paper Processing — Protocol A (academic-style)

This skill executes Protocol A: the per-document workflow for academic-style papers, after the Step 0 triage in `materials_processing_skill.md` has routed the document here.

For shared context (prerequisites, folder structure, status framework, lookup protocol, project setup), see `materials_processing_skill.md`. This file carries only the Protocol A pipeline.

## When this skill applies

Triage in `materials_processing_skill.md` Step 0 returned "academic-style." The document has two or more of:
- An abstract (not an executive summary).
- A stated research question or hypothesis.
- Original estimates the authors produced from data they analyzed.

If you arrived here without running the triage, go back and run Step 0 first — the protocol choice changes filename convention, summary emphasis, and BibTeX entry type, and getting it wrong means redoing the work.

---

## Step 1A — Rename using convention

Rename the file to the `who_what_year` stem, all lowercase, underscore-delimited (see `naming_conventions.md`): `<author>_<short_title>_<year>.pdf`

- **author**: last name of the first author, lowercase (compound surnames collapse to a single token, e.g. `garciamarquez`; co-authors split into separate tokens when used).
- **short_title**: two descriptive words, lowercase, underscore-separated.
- **year**: publication year.
- Example: `acemoglu_simple_ai_2024.pdf`.

If the naming is ambiguous (e.g., institutional author, no clear publication year), ask the user before proceeding.

---

## Step 2A — Extract full text

**Language rule (same rule as `document_processing_skill.md` Step 2, stated compactly).** The extract is always in the paper's source language, and the summary is always written from the extract, never from a translation. If the paper's language is not one the user reads (their reading languages are declared in the repo's `CLAUDE.md`; default English), ask the user whether to create an English reading copy (`TEXT_ENGLISH_` + the same stem, in the same subfolder) — never by default, they authorize per document. If created, its header declares it derived, audit-only, never a verification target and never citable, with source verbatim kept in parentheses on load-bearing terms; if declined, record its absence in the paper's index entry. In the summary, load-bearing figures and claims from a language the user does not read carry the source's verbatim words inline with the English rendering beside them.

- Save as `TEXT_author_short_title_year.md` in the `text/` subfolder of the paper's home — the home `materials_processing_skill.md`'s placement rule proposed and the user confirmed, never a hardcoded folder.
- Produce a clean, readable markdown version of the paper's content.
- Preserve section structure, tables (as markdown tables), and key formatting.
- Strip headers/footers, page numbers, and other artifacts.

---

## Step 3A — Write a comprehensive summary

Save as `SUMMARY_author_short_title_year.md` in the `summaries/` subfolder of the paper's home (the same home as the text extraction; see `materials_processing_skill.md`'s placement rule).

Structure:

**(a) What the paper argues** — Main thesis, research question, and contribution to the literature.

**(b) Methodology & key findings** — This section must be precise and detailed. Include:
- Data sources and sample: who, where, when, how many observations.
- Method: RCT, diff-in-diff, calibration, survey, structural model, etc.
- How key variables are constructed: exposure measures, outcome variables, controls.
- Identification strategy (if empirical) or key assumptions (if theoretical).
- Core results: effect sizes, magnitudes, main takeaways.

The description must be specific enough that someone can understand the methodology without reading the paper. Not vague ("uses cross-country data") but detailed ("uses household survey microdata for 23 countries, 2012–2015, linking an occupation-level exposure score to individual-level employment outcomes via OLS with occupation × country fixed effects").

**(c) [Conditional section — only if `CONDITIONAL_SECTION` is defined AND the paper has relevant content]** — Extract all findings matching the project's filter. Only include this section if the paper actually contains matching data.

**(d) Relevance to the project** — How this paper connects to `PROJECT_QUESTION`. Why it matters, what it contributes, what gaps it fills.

**(e) From the visual layer** — anything established by *looking* at a figure, chart, map, photograph, or a table the extraction garbled — stated as such, with what was checked and what it showed. Usually empty, and cheap when it is not: the processor is the only actor in the pipeline who ever has the source open, so this is the one moment such facts can be captured — a finding that lives only in the visual layer is unrecoverable downstream from the text extraction and the summary, at any cost. A **deliberately empty** note is itself informative ("figures reviewed; nothing load-bearing beyond the text"): it tells a later reader the figures were looked at and carried nothing, as against never having been opened. An image-only scan with no text layer is declared here. And where the summary's scope otherwise stops at the text — an honest thing for a summary written from an extraction to do — saying so in the summary is what lets a downstream reader tell "the document does not say" from "this summary did not look."

### Summary evolution principle

The (a)–(e) structure above is a **floor, not a ceiling**. As the user works with a paper over time (asking questions, requesting explanations, cross-referencing with other papers), the summary should grow. Expanded summaries with worked examples, accessible explanations of technical concepts, cross-references, and the user's own notes are expected and desirable. Do not trim or reorganize expanded summaries back to the minimal format.

---

## Step 4A — Register in the repo's paper-detail index

Add one row to the repo's **paper-detail index** (located by reading the
`FOLDER_MAP`s, never named here; its header row is `typed_index_template.md`'s),
in the section the index's head says it takes (a research line, `general` for
shared literature), with:

- **Stem** — the `who_what_year` stem, the pointer into the paper home and the bibliography.
- **Title** — the paper's title.
- **About** — the subject in Claude's words, about fifteen words: the topic or instrument, the question or outcome, the setting, the kind of evidence. Read the index first; a subject already named in a row keeps its words (`materials_processing_skill.md`, "The two indexes").
- **Claude status** — Claude's reading recommendation, set at processing time in Step 6A (see Status framework in `materials_processing_skill.md`).
- **User status** — Left blank until the user confirms their own label.
- **Forms** — the forms held, in reading order: `summary · text · pdf`.

The bibliographic detail lives in the bibliography (Step 5A) and the summary in the summary file; neither is copied into the row. The paper gets **no row in the materials index** (one row in one index, the materials skill's rule). Write the row in the shape the repo's index already has; never name a file or read an archetype spec at runtime.

---

## Step 5A — Update BibTeX

If the repo maintains a bibliography, add a new entry to it — the bibliography file is located by reading the `FOLDER_MAP`s, never a hardcoded filename. A repo that tracks citability another way (e.g. a reliability tag rather than a bibliography) has none; skip this step there. The cite key follows the same naming convention — it is the paper's `who_what_year` stem (e.g., `acemoglu_simple_ai_2024`). Always include an `abstract = {}` field with the paper's abstract (copied from the paper itself, not paraphrased).

Use `@article` for journal articles, `@unpublished` for working papers without a formal journal venue. Other BibTeX entry types may apply for specific cases (proceedings, dissertations) — use the standard BibTeX entry type for the publication kind.

---

## Step 6A — Set Claude status and flag if relevant

Based on the paper's content and its connection to `PROJECT_QUESTION`, set the **Claude status** in the index. This is Claude's recommendation — the user will confirm or override with their own label later.

The four Claude status values are: **Recommend full read**, **Recommend skim**, **Summary sufficient**, **Flagged — [reason]**. Full vocabulary and rationale in `materials_processing_skill.md`'s Status framework section.

When setting "Recommend full read" or "Flagged," also tell the user *in the conversation* why — don't just set the label silently.

---

## Step 7A — Re-verify an existing summary (optional, on the user's ask)

Same step as `document_processing_skill.md` Step 7, stated compactly, and run only when the user asks. A subagent on a lower tier reads only the summary and its `TEXT_` extract and returns a verdict per claim (`supported`, `imprecise`, `unsupported`, `contradicted`); the session re-checks each flag against the extract, corrects `imprecise` and `contradicted` claims to the extract's words, removes `unsupported` ones, and leaves the structure and any growth past the (a)–(e) floor alone. The record is one **Verified against the extract:** line at the top of the summary (date, checking model, counts); the index row does not change.

---

## Edge cases specific to Protocol A

- **Multiple first authors**: Use the first listed author for the filename.
- **Working papers without journal**: Use the institution or series as the source in bibliographic info; BibTeX entry type is `@unpublished`. (If the document is a synthesis or position paper rather than a research paper, it should have routed to Protocol B at Step 0 — go back and re-triage.)
- **Very short academic papers** (research notes, short comments): Still follow the full workflow; the summary may be shorter than the original — that's fine, the value is in the structured format and indexing.

For triage-level edge cases (borderline cases between academic and institutional, non-English papers, papers with no clear year), see `materials_processing_skill.md`'s Edge Cases section.

---

## Composition with other skills

- **`materials_processing_skill.md`** — Parent triage skill. Routes here when Step 0 returns academic-style. Carries the canonical Status framework, Prerequisites, Folder Structure, and Lookup Protocol.
- **`paper_processing_institutional_skill.md`** — Sibling skill for Protocol B (institutional-style reports). Not invoked from this skill; the choice is made at the triage upstream.
- **`project_tracker_skill.md`** — the repo's paper-detail index is in the freshness-audit's `TRACKED_LOCATIONS`. New entries added by this skill are picked up by the freshness check.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
