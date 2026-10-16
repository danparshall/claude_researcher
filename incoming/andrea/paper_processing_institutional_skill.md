---
name: paper-processing-institutional
description: Protocol B for processing institutional-style reports (background notes of international groups, flagship reports of multilateral organizations, multilateral working-group papers, policy reports of international organizations, government-agency research syntheses, institutional monographs). Invoked from materials_processing_skill.md's Step 0 triage when the document does NOT have most of (abstract, research question/hypothesis, original estimates from authors' own data). Covers institutional-author renaming, text extraction with acronym/box preservation, synthesized-findings summary, index registration, a `@techreport` bibliography entry, and setting Claude status. Use directly when the protocol is already known; otherwise start from materials_processing_skill.md.
triggers: >-
  Institutional reports (synthesis or policy reports from multilateral or international organizations);
  routed from Step 0, or directly when known
---

# Paper Processing — Protocol B (institutional-style)

This skill executes Protocol B: the per-document workflow for institutional-style reports, after the Step 0 triage in `materials_processing_skill.md` has routed the document here.

For shared context (prerequisites, folder structure, status framework, lookup protocol, project setup), see `materials_processing_skill.md`. This file carries only the Protocol B pipeline.

## When this skill applies

Triage in `materials_processing_skill.md` Step 0 returned "institutional-style." The document is a substantive analytical report that synthesizes evidence, positions a framework, or advises on policy, but does NOT present the authors' own original empirical or theoretical research with a stated hypothesis.

Common examples: background notes of international groups; flagship reports of multilateral organizations; multilateral working-group papers; policy reports of international organizations; government-agency research syntheses; institutional monographs that compile chapter contributions into a unified policy argument.

If you arrived here without running the triage, go back and run Step 0 first — the protocol choice changes filename convention, summary emphasis, and BibTeX entry type, and getting it wrong means redoing the work.

---

## Step 1B — Rename using institutional convention

Pattern: `institution_short_title_year.pdf`

- **institution** (lowercase):
  - For multilaterals: the organization's short acronym.
  - For governments: country code or name + agency acronym, collapsed to a single lowercase token.
  - For working groups: the group's acronym.
- **short_title**: two descriptive words, lowercase, underscore-separated.
- **year**: publication year.
- Examples: `ihn_vaccine_coverage_2025.pdf` (an international agency, by its acronym), `<country><agency>_pilot_program_2024.pdf` (a government agency, country and agency acronym as one token).

If multiple institutions co-published, lead with the principal author institution (the one whose staff produced the document — usually named on the cover). If the document is co-branded by a working group whose members include several institutions, use the working group's acronym (e.g., `<group>_capacity_dev_2025` rather than naming every member).

When unsure, ask the user.

---

## Step 2B — Extract full text

**Language rule (same rule as `document_processing_skill.md` Step 2, stated compactly).** The extract is always in the report's source language, and the summary is always written from the extract, never from a translation. If the report's language is not one the user reads (their reading languages are declared in the repo's `CLAUDE.md`; default English), ask the user whether to create an English reading copy (`TEXT_ENGLISH_` + the same stem, in the same subfolder) — never by default, they authorize per document. If created, its header declares it derived, audit-only, never a verification target and never citable, with source verbatim kept in parentheses on load-bearing terms; if declined, record its absence in the report's index entry. In the summary, load-bearing figures and claims from a language the user does not read carry the source's verbatim words inline with the English rendering beside them.

Save as `TEXT_institution_short_title_year.md` in the `text/` subfolder of the report's home — the home `materials_processing_skill.md`'s placement rule proposed and the user confirmed, never a hardcoded folder. Same general approach as Protocol A: clean, readable markdown; preserve section structure, tables, and key formatting; strip headers/footers, page numbers, and decorative artifacts.

Institutional reports often have heavy front matter (foreword, acknowledgments, list of acronyms, list of figures and boxes). Three specific rules:
- **Preserve the acronym list verbatim** — these are reference material for downstream work.
- **Preserve boxes and figure captions with their key data**, since these often carry the report's quotable findings.
- Strip decorative front matter (forewords, dedications) unless they contain substantive framing.

---

## Step 3B — Write a comprehensive summary

Save as `SUMMARY_institution_short_title_year.md` in the `summaries/` subfolder of the report's home (the same home as the text extraction; see `materials_processing_skill.md`'s placement rule). Structure parallels Protocol A but with institutional-appropriate emphasis.

**(a) What the report argues** — Purpose of the document, who commissioned it (or the request context: who asked for it and under what mandate), the principal thesis or position, and how it relates to prior or companion reports from the same institution. The "argues" framing applies even when the report seems neutral — institutional reports always carry a position, even if implicit.

**(b) Document type, methods, and findings** — This section replaces Protocol A's "Methodology & key findings." It must cover:
- **Document provenance:** what kind of report this is (background note, flagship, working paper, monograph, technical note); commissioning context; institutional team and lead authors; companion reports if part of a series; partner institutions consulted.
- **Frameworks and databases drawn on:** which institutional tools or datasets are used (e.g., a diagnostic assessment tool, a cross-country survey of agencies, a macroeconomic database, a trade statistics database). Name them so the user can locate underlying sources.
- **Headline synthesized findings:** the report's main numerical claims or qualitative conclusions, with their underlying citation when the report attributes them. Be explicit when a number is *the report's own synthesis* versus *a number it borrows from a cited paper* (cite the original where given).
- **Policy framework or recommendations:** the structured guidance the report offers — typology of reforms, decision frameworks, sequencing logic, any grouping of cases the report uses.
- **Country case studies, if any:** which countries are profiled, what for, and whether a given region is represented.

The precision principle still applies: name the tools, name the countries, name the underlying papers. "Synthesizes a multilateral's research" is not enough — say which papers, which datasets, which estimates.

**(c) [Conditional section — only if `CONDITIONAL_SECTION` is defined AND the report has relevant content]** — Same as Protocol A. If the report has region-specific content (country cases, regional cuts, region-specific tables), extract here. Frequently empty for institutional reports with global framing.

**(d) Relevance to the project** — In addition to the standard "why this matters" framing, address two questions specific to institutional reports:
- **What position does this report represent?** ("This is a multilateral organization's authoritative public statement on X as of 2025"; "This is an international group's framing of how to implement a reform"). Readers want to know what position they are implicitly endorsing or arguing against if they cite it.
- **Cross-references in the existing library.** Institutional reports almost always cite papers already in the repo's existing paper collection. List the matches with relative paths to the existing summaries — this knits the library together and saves future readers a step.

**(e) From the visual layer** — anything established by *looking* at a figure, chart, map, photograph, or a table the extraction garbled — stated as such, with what was checked and what it showed. Usually empty, and cheap when it is not: the processor is the only actor in the pipeline who ever has the source open, so this is the one moment such facts can be captured — a finding that lives only in the visual layer is unrecoverable downstream from the text extraction and the summary, at any cost. A **deliberately empty** note is itself informative ("figures reviewed; nothing load-bearing beyond the text"): it tells a later reader the figures were looked at and carried nothing, as against never having been opened. An image-only scan with no text layer is declared here. And where the summary's scope otherwise stops at the text — an honest thing for a summary written from an extraction to do — saying so in the summary is what lets a downstream reader tell "the document does not say" from "this summary did not look." (Same item as Protocol A.)

### Summary evolution principle

The (a)–(e) structure above is a **floor, not a ceiling**. As the user works with a report over time, the summary should grow with cross-references, accessible explanations, and the user's own notes. Do not trim or reorganize expanded summaries back to the minimal format. (Same principle as Protocol A.)

---

## Step 4B — Register in the repo's paper-detail index

Same row as Protocol A (`Stem · Title · About · Claude status · User status · Forms`, the header row of `typed_index_template.md`). The paper-detail index is the repo's existing one, located by reading the `FOLDER_MAP`s (never named here). The report's kind of document — "multilateral background note," "working paper," "policy paper," "technical note," "flagship report" — goes in the `About` cell as its kind of evidence, and in the bibliography entry, not in a column of its own.

The report gets **no row in the materials index** (one row in one index, the materials skill's rule); the institutional metadata stays in the bibliography and the summary. Write the row in the shape the repo's index already has; never name a file or read an archetype spec at runtime.

---

## Step 5B — Update the bibliography

If the repo maintains a bibliography, add an entry to it — the bibliography file is located by reading the `FOLDER_MAP`s, never a hardcoded filename; a repo that tracks citability another way (e.g. a reliability tag) has none, so skip this step there. Use `@techreport` for institutional reports. Required fields:
- `author = {{Institution Name}}` — **double braces** preserve casing and prevent BibTeX from treating the last word of the institution's name as a surname.
- `title`, `institution`, `year`.
- `type` — describe the document type (e.g., "Background Note," "Working Paper," "Technical Note").
- `month` — when relevant.
- `note` — for institutional team, lead authors, and partner institutions if needed.
- `abstract` — copy from the report's executive summary if no separate abstract exists.

For **monographs published as books**, use `@book` with `publisher`, `address`, and `isbn` if available. For **chapters within institutional monographs**, use `@inbook` referring back to the parent `@book` entry.

Cite key follows the filename convention — the document's stem: `ihn_vaccine_coverage_2025`.

---

## Step 6B — Set Claude status and flag if relevant

Same status framework as Protocol A. The four Claude status values are: **Recommend full read**, **Recommend skim**, **Summary sufficient**, **Flagged — [reason]**. Full vocabulary and rationale in `materials_processing_skill.md`'s Status framework section.

One observation specific to institutional reports: they tend to cluster at "Recommend full read" (when they're flagship statements relevant to active work) or "Summary sufficient" (when they're routine technical updates or peripheral). Set the status based on the report's current relevance to active task folders, not just its general quality.

When setting "Recommend full read" or "Flagged," also tell the user *in the conversation* why — don't just set the label silently.

---

## Step 7B — Re-verify an existing summary (optional, on the user's ask)

Same step as `document_processing_skill.md` Step 7, stated compactly, and run only when the user asks. A subagent on a lower tier reads only the summary and its `TEXT_` extract and returns a verdict per claim (`supported`, `imprecise`, `unsupported`, `contradicted`); the session re-checks each flag against the extract, corrects `imprecise` and `contradicted` claims to the extract's words, removes `unsupported` ones, and leaves the structure and any growth past the (a)–(e) floor alone. The record is one **Verified against the extract:** line at the top of the summary (date, checking model, counts); the index row does not change.

---

## Edge cases specific to Protocol B

- **Working papers from multilateral institutions are usually Protocol A**, not B — they have abstracts, hypotheses, identification strategies, and are written in academic-paper structure even when the institution is the publisher. If you arrived here on a working paper that has clear academic structure, re-triage via `materials_processing_skill.md` Step 0.
- **Monographs with chapter-level empirical work** are still Protocol B at the document level (the value is the synthesis), but if a chapter is heavily reused on its own, consider creating a separate Protocol A summary for that chapter and cross-linking.
- **Reports without named individual authors** (e.g., secretariat reports of international organizations, agency reports) are unambiguously Protocol B.
- **Reports with named authors but commissioned by an institution** (e.g., "Prepared by two named authors for a multilateral group") — the cover usually names the institution as the publisher and the individuals as the production team. Treat as Protocol B; list the production team in section (b) under "institutional team."
- **Co-published institutional reports**: Lead with the principal author institution; use working-group acronym if co-branded by a working group with multiple members.
- **Very short institutional documents** (policy briefs, 2-pagers): Still follow the full workflow; the summary may be shorter than the original — that's fine, the value is in the structured format and indexing.

For triage-level edge cases (borderline cases between academic and institutional, non-English papers, papers with no clear year), see `materials_processing_skill.md`'s Edge Cases section.

---

## Composition with other skills

- **`materials_processing_skill.md`** — Parent triage skill. Routes here when Step 0 returns institutional-style. Carries the canonical Status framework, Prerequisites, Folder Structure, and Lookup Protocol.
- **`paper_processing_academic_skill.md`** — Sibling skill for Protocol A (academic-style papers). Not invoked from this skill; the choice is made at the triage upstream.
- **`project_tracker_skill.md`** — the repo's paper-detail index is in the freshness-audit's `TRACKED_LOCATIONS`. New entries added by this skill are picked up by the freshness check.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
