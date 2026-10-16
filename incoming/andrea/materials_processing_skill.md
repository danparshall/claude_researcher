---
name: materials-processing
description: "Triage for everything that comes into a repo to be filed and summarized — academic papers, working papers, multilateral or government institutional reports, policy documents, AND operational/institutional documents (legislation, government memos, terms of reference, draft policies, consultant deliverables, budget documents). The single entry point: runs Step 0 to route each item to one of three branches — document processing via document_processing_skill.md, academic-paper Protocol A via paper_processing_academic_skill.md, or institutional-paper Protocol B via paper_processing_institutional_skill.md. Use whenever a user uploads a PDF/DOCX and asks to process it, file it, or add it to the repo. Does NOT handle note-taking, reading reviews, or discussion of materials after processing — those are separate workflows."
triggers: >-
  Any paper or institutional document to file or process. The front door: its Step 0 routes to
  one of the three processing skills. Start here unless the branch is already obvious
---

# Materials Processing Skill (triage)

This skill is the **single front door** for filing incoming materials into a
repo's library, plus the **shared infrastructure** for the paper branches. It
runs one Step 0 triage with a three-way outcome, then routes the item to the
branch that handles it. Nothing is processed here directly — the per-item
pipelines live in three sibling skills:

- **`document_processing_skill.md`** — the **document branch**: operational and
  institutional documents (legislation, government reports, terms of reference,
  consultant deliverables, budget and program documents, operational material).
- **`paper_processing_academic_skill.md`** — **Protocol A** for academic-style
  papers.
- **`paper_processing_institutional_skill.md`** — **Protocol B** for
  institutional-style reports.

This skill carries the content shared across the two **paper** branches
(prerequisites, the paper-branch artifacts and their placement rule, the
status framework vocabulary, the lookup protocol, and paper-branch
configuration) plus the rule that every processed item has **one row in one
index** — a paper in the paper-detail index, a document in the materials index.
The document branch is self-contained: `document_processing_skill.md` carries
its own folder model, reliability/confidentiality labels, and indexing.

## When to use this skill

- A user uploads a PDF or DOCX and asks to file it, process it, or add it to the
  repo — whether it's a paper or an operational document.
- A user asks to reprocess or update an existing entry and the branch isn't
  already obvious.

If you already know the branch (e.g., the user said "process this paper" or
"file this piece of legislation"), you may go straight to the relevant branch
skill — but when in any doubt, run Step 0 here first. The triage is cheap and
getting the branch wrong means redoing the filename, summary, and index work.

## Scope: one triage, three branches

Step 0 makes two cuts in sequence:

1. **Document or paper?** Is this an operational/institutional *document* (a
   legal instrument, an operational deliverable, a program or budget document —
   something that is *used* or *acted on*), or a *paper* (a research or
   analytical work destined for the citation library — something that *argues*
   or *synthesizes*)?
2. **If a paper: academic-style or institutional-style?** The three diagnostic
   questions below split Protocol A from Protocol B.

> **Why the boundary lives here now.** Earlier kit versions adjudicated the
> document-vs-paper call in two places at once — `document_processing_skill.md`'s
> "what this is NOT" section and the paper triage's scope section — which let
> the two drift apart. The materials triage replaces that split: the
> document-vs-paper boundary is decided here, in one place, and the branches
> assume the routing decision has already been made.

---

## Prerequisites (paper branches)

These configure the **paper** branches. The document branch defines its own
prerequisites in `document_processing_skill.md`. Before using the paper branches
in a project, the project's CLAUDE.md should define:

1. **`PROJECT_QUESTION`** — A one-sentence description of the project's research
   question or focus (e.g., "How remote work affects productivity in mid-size firms"). Used to write the relevance section of each paper summary.
2. **`CONDITIONAL_SECTION`** *(optional)* — A filter for a conditional section in
   summaries. Define what subset of findings to extract when present (e.g.,
   "region-specific findings"). If not defined, summaries skip section (c).
The paper-detail index and the bibliography are **not** configured by name
here. A paper touches two of the repo's existing homes — its paper-detail index
and its bibliography (when the repo keeps one); never the materials index, which
is the documents' — and the skill finds each by reading the repo's `FOLDER_MAP`s
at filing time, never by a hardcoded filename (see the two sections below). A
repo that tracks citability some other way (e.g. a reliability tag instead of a
bibliography) has no bibliography to find — the skill skips that step rather than
creating one.

If `PROJECT_QUESTION` is not yet defined when the user asks to process a paper,
ask the user to provide it before proceeding.

---

## Paper-branch artifacts and their placement

Each processed paper produces three artifacts:
- the renamed PDF (`author_short_title_year.pdf` / `institution_short_title_year.pdf` — see Cut 2),
- a text extraction `TEXT_<filename>.md`, in a `text/` subfolder of the paper's home,
- a summary `SUMMARY_<filename>.md`, in a `summaries/` subfolder of the paper's home.

The `text/` and `summaries/` subfolders and the `TEXT_`/`SUMMARY_` naming are the
paper pipeline's own within-folder convention — they sit inside whatever folder
holds papers in this repo.

**Placement is suggested and confirmed, not assumed.** This skill does not own
where papers live and never hardcodes a folder. At filing time, read the repo's
`FOLDER_MAP.md` files — the per-folder purpose index every repo carries
regardless of archetype — propose the home they indicate, and **confirm with the
user before filing.** Repo types place intake differently (a research repo keeps
literature in its shared layer; other types use their own intake folders);
reading the `FOLDER_MAP`s keeps this skill blind to the archetype while still
landing the paper in the right place. Do **not** scan the raw folder tree to
guess (archetype knowledge through the back door), do **not** read the archetype layer (`archetype_conventions.md` or an archetype spec) at runtime (that would make this skill archetype-aware), and do **not** file
without the user's confirmation. If the maps are thin or empty in a new repo, the
suggestion degrades to "root, or wherever papers have been going" — still ask,
never silently hardcode.

The homes a paper touches — the repo's paper-detail index and its bibliography
(when it keeps one); the materials index (next section) is the documents' —
already exist in the repo, created at repo setup in the shape that
repo uses. This skill finds each by reading the repo's `FOLDER_MAP`s, adds to
them in the shape they already have, and never names a file or reads the archetype layer (`archetype_conventions.md` or an archetype spec) at runtime. A repo that has no bibliography (citability tracked another way)
simply skips that step.

The document branch uses its own folder model and indexing; see
`document_processing_skill.md`.

---

## The two indexes — one row in one index

Every processed item gets **one row in one index**: a document's row in the
repo's materials index, a paper's row in the repo's paper-detail index. The two
are the repo-level lookups Claude reads when the user asks where something is or
what the repo has on a subject, so a lookup never requires scanning the repo,
and a thing registered twice is the same thing found twice (before v6.5 a
paper had a row in both, the materials row pointing at the paper row).

This skill does **not** define an index's structure or its name. Both indexes
already exist in the repo, created at repo setup in the form of
`typed_index_template.md` (the head naming what is registered and the writer,
the header row, the markers), and the materials index's head says that papers,
notes and dives are in their own indexes. A NONE repo carries neither at birth:
it names the index it uses for each, registered in the root map's root-documents
block. **Locate the index via the
`FOLDER_MAP`s (the root map's root-documents block names each with what it
registers), follow the header row it has, and add the item's row in that
shape** — never name a file or read the archetype layer at runtime. Every row
carries an `About` cell, the subject in Claude's words written at filing (the
topic or instrument, the question or outcome, the setting, the kind of
evidence, about fifteen words): read the index first, and a subject already
named in a row keeps its words; a new word is written only for a subject not
yet there.

The one constant across repo types: an index is a **pointer-level lookup, not a
second copy of the detail.** The summary lives in the summary file, the bib
entry in the bibliography, the reliability and confidentiality detail of a
document in its summary (and, in a research repo, its `MATERIALS_INDEX` row); the row
points.

Each branch writes its row as part of its indexing step (paper branches: the
paper-detail index; document branch: the materials index, alongside its own
folder-index update).

---

## Step 0 — Triage

When a user provides a material and asks to file or process it, **always start
with Step 0** unless the branch is already unambiguous.

### Cut 1 — document or paper?

Ask: is this something that is *used or acted on* (an operational/institutional
document), or something that *argues or synthesizes* (a paper for the citation
library)?

- **Document** → route to `document_processing_skill.md`. Typical: legislation,
  regulations, government memos, terms of reference, draft policies, consultant
  deliverables tied to one project, budget documents, program documents,
  operational material. Rule of thumb: if it would *not* get a BibTeX entry and
  has no analytical thesis of its own, it's a document.
- **Paper** → continue to Cut 2. Typical: journal articles, working papers,
  dissertations, and institutional analytical/synthesis reports — anything with
  authors (individual or institutional), a thesis or synthesized position, and a
  place in a citation library.

**The genuinely fuzzy zone is institutional report vs. operational institutional
document** — both can come from the same publisher. The discriminator is what
the item *does*, not who published it:

- A multilateral organization's **flagship or analytical report** that synthesizes
  evidence or positions a policy framework → **paper**, Protocol B.
- A multilateral organization's **project or program document**, an operational annex, a scope-of-work document → **document**, the document branch.

For borderline calls, exercise judgment and flag the call to the user in the
conversation.

### Cut 2 — academic-style or institutional-style? (papers only)

Open the document and answer three quick questions:

1. Does it have an **abstract** (vs. an *executive summary*)?
2. Does it pose a **research question or hypothesis**?
3. Does it report **new estimates the authors produced from data they analyzed**
   (rather than synthesizing others' findings)?

- **Two or more "yes"** → **Protocol A** (academic-style). Read and follow
  `paper_processing_academic_skill.md`.
- **Two or more "no"** → **Protocol B** (institutional-style). Read and follow
  `paper_processing_institutional_skill.md`.

Common borderline cases:
- Multilateral working papers with abstracts and methods sections but heavy
  policy framing — usually Protocol A.
- Institutional monographs with chapter-level empirical work — usually Protocol
  B at the document level (the value is the synthesis).
- Country case studies with descriptive but not causal analysis — usually
  Protocol B.
- Discussion papers, technical notes, and working papers of international
  organizations — most have
  research-paper structure and are Protocol A; monographs and synthesis pieces
  are Protocol B. Triage on structure, not on the publisher.

The paper pipeline is identical across protocols. What differs:

| Step | Protocol A | Protocol B |
|---|---|---|
| Filename | `author_short_title_year.pdf` (individual author) | `institution_short_title_year.pdf` (institutional author) |
| Summary section (a) | Thesis, research question, contribution | Purpose, commissioning context, position |
| Summary section (b) | Data, sample, identification, effect sizes | Document type, frameworks/databases, headline findings, policy framework |
| Summary section (d) | Standard "relevance" framing | Same plus "what position does this represent" + cross-references |
| BibTeX entry type | `@article` / `@unpublished` | `@techreport` / `@book` / `@inbook` |

---

## Status framework — Tracking (canonical, applies to both paper protocols)

This is the canonical Status framework for the paper branches. Both protocol
skills set the Claude status as their final step and refer back to this table
for the label vocabulary. (The document branch uses its own reliability and
confidentiality labels, defined in `document_processing_skill.md`.)

The paper-detail index serves as the single tracking file for papers. Each paper
entry includes two status columns:

| Column | Set by | When | Purpose |
|---|---|---|---|
| **Claude status** | Claude | At processing time (Step 6 of either protocol) | Claude's reading recommendation |
| **User status** | The user | When they review/confirm | The user's own assessment |

**Claude status values:**

| Claude Status | Meaning |
|---|---|
| **Recommend full read** | Core to the project — the user should read this in full |
| **Recommend skim** | Useful but not central — reading the summary is probably enough, a skim of key sections would add value |
| **Summary sufficient** | Peripheral or tangential — the summary captures what the project needs |
| **Flagged — [reason]** | Something noteworthy that doesn't fit the above (e.g., "Flagged — methodological template for our estimation," "Flagged — contradicts Paper X") |

When setting "Recommend full read" or "Flagged," also tell the user *in the
conversation* why — don't just set the label silently.

**User status labels** — These are defaults; each project can customize:

| User Status | Meaning |
|---|---|
| **Must-read** | Core paper, user has read or will read in full |
| **Read** | User has read it, notes taken |
| **No need to read** | Reviewed summary, not worth a full read |
| **Middle importance** | Worth reading but not urgent |
| **Flagged** | Needs deeper review later |

The user may use other labels as they see fit. Claude never sets the user status
— only the user does. If the user provides a status label during conversation,
update the index accordingly.

**The row** is the paper-detail index's header row in `typed_index_template.md`
— `Stem · Title · About · Claude status · User status · Forms` — one line per
paper, the stem the pointer into the paper home and the bibliography, `Forms`
the forms held in reading order (`summary · text · pdf`):

```markdown
| Stem | Title | About | Claude status | User status | Forms |
|---|---|---|---|---|---|
| acemoglu_simple_ai_2024 | The Simple Macroeconomics of AI | AI and aggregate productivity; task-based model; modest ten-year TFP gains; theory, calibration to one country | Recommend full read | Must-read | summary · text · pdf |
| ihn_vaccine_coverage_2025 | Background Note on Vaccine Coverage | routine immunization coverage; supply and outreach; low-income countries; institutional synthesis | Recommend full read | | summary · text · pdf |
```

The summary lives in the paper's summary file and the row points at it; a
summary written below or inside the row is retired form (the pre-v6.5 example
had it "follow below its row," which makes an index grow without bound), and
a row number is never a pointer, since it shifts on every insert while the stem
never does.

---

## Lookup Protocol

When discussing a material in conversation, check Claude's indexes before
scanning the repo:

1. **Check the index for the kind first** — the paper-detail index for a paper,
   the materials index for a document (both named in the root map's
   root-documents block); a subject ask scans the `About` cells of both. The row
   tells you what the item is, where it lives, and which forms are held.
2. **Check the detailed entry** — the paper-detail index row and the individual
   summary in the paper's `summaries/` subfolder for papers; the document's
   folder index and
   summary for documents.
3. **Go to the full text** only if deeper detail is needed.

Do not read full text by default — only when the user asks or when a specific
question requires it. **The one exception:** a row whose `Claude status` says imported and
`not integrated` (`cross_repo_import_skill.md` Step 5) is read through its `TEXT_` extract before
any claim from its summary is used; the summary was written for another repo's question.

---

## Configuring the paper branches in a repo

Repo structure — the intake folders and the materials/detail indexes — is
created at repo setup by the archetype scaffold, **not here.** This skill does
not create intake folders, index files, or any folders. What it needs in place before
the paper branches run is the paper-branch configuration in the project's
CLAUDE.md:

1. Ensure `PROJECT_QUESTION` is defined (and `CONDITIONAL_SECTION`, if the repo
   uses one). The paper-detail index, the bibliography, and the materials index
   are **not** named here — the skill finds each by reading the repo's
   `FOLDER_MAP`s at filing time. If `PROJECT_QUESTION` is missing when a paper is
   to be processed, ask the user.
2. Ensure the project's CLAUDE.md references this triage skill plus whichever
   branch skills the project uses.

With those in place, process and file items via Step 0 and the branches, placing
each into the repo's existing structure per the placement rule above (read the
`FOLDER_MAP`s, suggest, confirm).

If a repo predates the v4 archetype scaffolding and lacks the intake structure or
the materials index, that is a setup/migration gap — flag it to the user rather
than hand-creating a structure that may not match the repo's archetype.

---

## Edge Cases (triage-level)

These are edge cases for the triage decision itself. Edge cases specific to
running a branch live in that branch's skill file.

- **Operational document that also reports original analysis** (e.g., a program
  evaluation): if the analytical contribution is the point and it would earn a
  BibTeX entry, treat as a paper (usually Protocol B); if it's an operational
  deliverable that happens to contain analysis, treat as a document. Flag the
  call.
- **Working papers without journal**: Triage as Protocol A if the paper has
  academic structure (abstract, hypothesis, methods, results); as Protocol B if
  it's a synthesis or position paper.
- **Papers or documents with no clear year**: Ask the user.
- **Non-English materials**: The triage applies on structure. Text extraction
  and summarization happen in the project's working language (ask if unclear).
- **Borderline triage**: When a cut is genuinely ambiguous, flag it to the user
  and proceed with your best judgment.

---

## Composition with other skills

- **`document_processing_skill.md`** — the document branch. Invoked from Step 0
  Cut 1 when the material is an operational/institutional document.
- **`paper_processing_academic_skill.md`** — Protocol A. Invoked from Step 0
  Cut 2 when triage returns academic-style.
- **`paper_processing_institutional_skill.md`** — Protocol B. Invoked from Step 0
  Cut 2 when triage returns institutional-style.
- **`project_tracker_skill.md`** — the repo's materials index, paper-detail
  index, and the document branch's folder index are in the freshness-audit's
  `TRACKED_LOCATIONS`.
  Updates from this skill and the branch skills are picked up by the
  freshness check.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
