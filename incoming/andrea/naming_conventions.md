---
name: naming-conventions
description: >
  The kit's universal naming rule, kept in every repo regardless of archetype
  (including NONE). Content files and folders use lowercase under_score;
  structural/organization files (the index family, FOLDER_MAP, STATUS) use
  ALL_CAPS; a content-file marker (TEXT_, SUMMARY_, _PLAN, _OUTLINE, the closed
  list here) is an ALL_CAPS token on a lowercase stem. Covers the carry-safety
  rationale, underscore-not-hyphen, the human-readable-display exemption, and
  the paper-stem / BibTeX cite-key identity.
triggers: >-
  Before naming or renaming any file or folder
---

# Naming conventions

## The rule: three categories

Names fall into three categories, each internally consistent, with the
difference between them carrying meaning:

| Category | Form | What it covers |
|---|---|---|
| **Content** | `under_score` (lowercase, underscore-delimited) | Ordinary repo content — folders, working files, anything created and moved in the course of work. The default. |
| **Structural / organization** | `ALL_CAPS` (underscore-delimited) | Repo-organization files: the index family (`MATERIALS_INDEX`, `PAPERS_INDEX`, the archetype indexes), `FOLDER_MAP`, `STATUS`, and similar scaffolding. |
| **Content-file marker** | an `ALL_CAPS` token on a lowercase stem (`TEXT_<stem>.md`, `<stem>_OUTLINE.md`) | A content file that is a representation or companion of another content file, named by its stem plus the marker that says which. The closed list is below. |

The capitals are deliberate and load-bearing: they make the
structural/organization files **pop out from content at a glance**, so a folder
can be scanned and its scaffolding identified instantly, and they do the same
for a marker: among a folder of `who_what_year` stems the summaries, the
outlines and the ledgers are found without reading the names. Case carries the
meaning "this is a structural file" or "this is the <marker> of that stem."
This is one rule with three categories — not an inconsistency.

## Why this rule

- **Carry-safety.** Names move by path through the GitHub API. Mixed-case
  (CamelCase) is lossy to carry: every internal capital is a spot where the
  casing gets guessed wrong, the API treats it as a different path, and the file
  goes missing or duplicates (e.g. `Coverimage.png` vs `CoverImage.png`).
  **Both `under_score` and `ALL_CAPS` are carry-safe** — neither has mixed casing
  to guess wrong. CamelCase is the form that breaks; it is retired.
- **Readability.** Word-breaks are read faster when marked. The underscore *is*
  the space made literal — it puts the break exactly where it's read, without
  requiring the casing to be supplied correctly each time. So `under_score`
  gives the same word-break signal CamelCase gave, minus the part that breaks.
- **Visual distinction.** `ALL_CAPS` for the structural files lets repo-
  organization files be identified at a glance, while staying carry-safe; the
  same capitals on a marker let a stem's derived files be found the same way.

## Content-file markers (the third category)

A marker is a fixed `ALL_CAPS` token attached to a lowercase content stem: a
**prefix** when the file is a representation of a source (`TEXT_<stem>.md` is
the extraction of `<stem>.pdf`), a **suffix** when the file is a companion of a
product (`<stem>_OUTLINE.md` travels with `<stem>.md`). The stem stays the
identity and stays lowercase; the marker never enters a cite key or an index
row's stem. **The purpose is retrieval by eye:**
the markers exist so the user finds a stem's derived files at a glance in a folder
listing, the way the structural files pop out — so every marker is `ALL_CAPS`,
and a lowercase form (`text_<stem>.md`, `summary_<stem>.md`) is drift the
conformance pass migrates. Carry-safety is not at stake: a marker is a fixed
token with no mixed casing to guess wrong.

**The closed list.** A marker is born here, by a kit change that names its
owning skill; a skill does not coin one on its own.

| Marker | Marks | Owning skill |
|---|---|---|
| `TEXT_<stem>.md` | the text extraction of a source | the paper-processing pair, `materials_processing_skill.md`, `document_processing_skill.md` |
| `SUMMARY_<stem>.md` | the summary of a source | the same |
| `TEXT_ENGLISH_<stem>.md` | the English reading copy of an extraction (marker `TEXT_` plus the language token) | the same |
| `MULTISESSION_CARRYOVER_<task_stem>.md` | a task's carryover across sessions | `multisession_task_skill.md` |
| `PROMPT_<stem>_<YYYYMMDD>.md` | a scoped-mode prompt in `workspace/step_prompts/` | `workstream_plan_skill.md` |
| `<stem>_PLAN.md` | a workstream plan file | `workstream_plan_skill.md` |
| `<stem>_OUTLINE.md` | the compiled outline paired with a draft (`A_chapter_<name>_OUTLINE.md` is this marker under the drafting skill's chapter prefix) | `writing_drafting_skill.md`, `writing_branch_skill.md` |
| `<stem>_LEDGER.md` | a product's ledger, living with the product | `product_ledger_skill.md` |
| `<stem>_DESIGN.pptx` | the Claude Design deck of a markdown product | `design_deck_reconciliation_skill.md` |
| `<stem>_SKETCH.md` | a visual's sketch, one per visual stem | `standing_documents_template.md` ("`workspace/visuals/`"; the workflow is `visuals_workflow_skill.md`) |
| `YYYY-MM-DD_<topic>_RAW.md` | the raw record of a feedback entry | `structure_conventions.md`, "`feedback/`" |
| `<stem>_BUILD.js`, `<stem>_BUILD.py` | the generator of a rendered representation, committed beside the file it renders | the project's document-formatting skill, if it has one; a slide-building skill's python builds take the same name |
| `<stem>_PLAIN.md` | the pre-style copy of a document, saved beside it before a voice profile is applied so the unstyled text survives the pass | the project's voice profiles, if it has any, which point here |

## Underscore vs. hyphen (within the content category)

`under_score`, not `hyphen-case`, for content names: underscores survive
double-click selection (the whole token highlights as one word), read cleanly in
code and in Stata / R / Python, and match the kit's existing convention. Hyphens
would be preferable only for URL slugs / web contexts, which the kit doesn't
have. (A date that leads a filename is the one exception inside the content
category: it is written hyphenated ISO, `YYYY-MM-DD_`, the form the feedback
entries, the saved conversations, the brainstorms and the standing documents all
use, so a folder sorts by date at a glance; the conversations skill's
`<short-tag>` slugs keep their hyphens by that
skill's own documented convention. The one exception is the dive prefix
`YYYYMMDD_HHMM_` of `agent_research_verification_skill.md`'s five-file set,
which sorts by minute inside a dive folder and is that skill's. A date inside a
name that does not lead it follows the content rule, `2026_08_04`-style.)

## Branch names (a hyphen exception)

Git branch refs use **hyphens**, lowercase — by git convention, the same kind of
localized exception as the conversation `<short-tag>` slugs above:
`<slug>-<purpose>-<date>`. The purpose token names the branch kind — `edits` /
`restructure` / `redraft` / `review` for a writing branch
(`writing_branch_skill.md`), and **`explore`** for an exploration branch
(`exploration_branch_skill.md`) — e.g. `survey-weights-explore-jun-12`. A branch
ref is a transient git identifier, not repo content carried by path into the
tree, so the content `under_score` rule does not bind it.

## Human-readable display text is exempt

The carry-safety rule binds only names a **machine carries by path** (filenames,
identifiers skills parse). Text a person *reads* and no machine carries by path
— document titles, headings, the human label inside a `FOLDER_MAP` index
entry — can be written however reads best, including capitalized words with
spaces. The pairing is free because the index entry already exists: the index
can show `Regional trade — descriptive paper` while the file on disk is
`paper_regional_trade.md`. The scanned thing is readable; the carried thing is safe.

## Names that double as identifiers — paper-processing stems and cite keys

The paper-processing skills (`paper_processing_academic_skill.md`,
`paper_processing_institutional_skill.md`, `materials_processing_skill.md`) name
renamed PDFs on a `who_what_year` stem, reuse that stem for the extracted-text
and summary files (`TEXT_<stem>.md`, `SUMMARY_<stem>.md`), **and reuse it as the
BibTeX cite key.**

**Keep the `who_what_year` structure; lowercase the whole stem under the content
rule.** The structure front-loads the author/institution handle and folds the
cite key into the filename so disk and `\cite{}` share one identity. Only the
casing changes: the intra-token CamelCase (`simpleAI`, `shortTitle`) is the
carry-unsafe, non-reconstructible form this convention retires. So
`acemoglu_simple_ai_2024`, `institution_short_title_2025`.

**Authorship (collapse vs split) is read from the source at intake, not guessed
from the stem.** Whether a multi-token surname is one person's compound surname
(collapse: `garciamarquez`) or several co-authors (split: `kleven_kreiner_saez`) is
**undecidable from the stem alone** — read it off the document's
citation/authorship when the paper is processed, and fix it once, correctly.
Given that:

**Compound surnames collapse to a single lowercase token** — `DellAcqua` ->
`dellacqua`, `delRioChanona` -> `delriochanona` (drop the internal capital; the
surname does not split into multiple tokens).

**Cite-key scope.** The lowercasing rule binds only keys that *are* filename
stems (the paper-processing `stem = key = filename` identity). A legacy or
external `.bib` whose keys are *not* filenames (e.g. a Zotero library) is
**exempt** — no carry-safety is at stake, so its keys are left as-is.

**Renaming a stem rewrites its cite key.** Because the stem *is* the cite key,
lowercasing or otherwise renaming a stem rewrites that paper's `.bib` entry key
and every `\cite{}` that points to it. Do this as a deliberate per-file
migration — read the source, fix the key once — not a blanket find-replace. The
`TEXT_` / `SUMMARY_` prefixes are markers (the third category) and the
`PAPERS_INDEX` / `MATERIALS_INDEX` files are structural; neither changes when
the stem does.


---
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
