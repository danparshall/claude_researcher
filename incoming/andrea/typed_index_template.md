# Typed root indexes — the template (the archetype's index set, a repo's own catalog)

The typed root indexes of an archetype repo (research's six)
and a repo's own catalog registered with them.
Every one is written for Claude and read at three moments: **the user's ask** ("where is X that is
about Y"; "what do we know about topic Y"), the **writer's step** (a skill or a session files a
thing and writes its row), and the **close and the audit** (the close-out refreshes the rows a
session touched and rewrites the trailer; the index audit verifies what rows claim). Its job is
that Claude finds a thing by its kind and by its subject without scanning the tree, and answers
"what do we know about Y" with the state of each thing (`structure_conventions.md`, "Who these
files are for"). Locating runs index first: the root
map's root-documents block names each index with what it registers, so a kind ask reads one
index whole, and a topic ask is one scan across every root index. A NONE repo carries
`NOTES_INDEX` alone, the one universal index (`structure_conventions.md`, "`writing_notes/`").

**The form, fixed.** The title line is the file name without its extension (`# PAPERS_INDEX`).
The head is three sentences: what is registered and the unit of a row, with the writer named
(that pointer is the whole of "the header names its feeding process"); how the rows are
sectioned; how a row's pointer is read, shallow to deep. Then the `index` slot, holding one
table per section, the sections born with their first row, never with the unit; the
`unplaced` slot; one trailer line. Every row carries `About` (the subject in Claude's words),
the state the kind reports where the kind has one (a reading status, a stage, a verification
date, where a visual is used), and the pointer. A column is the same word wherever it means
the same thing (`About`, `Where`, `Forms`), and the first column names the unit. Nothing with
a home elsewhere is restated: the behavior rules are
`archetype_conventions.md`'s ("Typed-index behavior"), the state vocabularies are the writer
skills', what each index registers is the root map's, the rules of a kind are the spec's. The
fill rules — create the set where missing, rewrite the head, regenerate every header row and
keep the rows, map old columns by meaning — are `PROJECT_SETUP.md` Step 7.5 part 2, never here.

**`About`, the subject cell.** Written by Claude at filing, from the thing itself (a paper's
abstract, title and summary; a product's outline; a dive's question), in the repo's working
vocabulary: the topic or instrument, the question or outcome, the setting, the kind of
evidence, about fifteen words. The index is its own vocabulary: a subject already named in a
row keeps its words, and a new word is written only for a subject not yet there (Claude reads
the index to find the row's place, so it sees the words in use). No tag list, no author
keywords as a field; a subject that becomes live later gets its word added to the rows it
concerns by the close-out's refresh or the index audit. No date and no count in a row; the
trailer carries the date.

**Markers** (`structure_conventions.md`, "Slots and markers, one notation"): `slot: index`
around every section heading and table, each table's header row kit form regenerated at every
stop, the section headings and the rows the repo's; `slot: unplaced` in every index, empty in
the normal state. The trailer is rewritten at the close that touched the index and is the only
date in the file. An index is created in this form, empty, by the scaffold or the pass. Kit
form is about eight lines; a row is one line. Where a form below reads `<...>` or
`YYYY-MM-DD` it is a placeholder and is not copied; a line marked `[research]` is written
for a research repo only, a line marked `[NONE]` for a NONE repo's `NOTES_INDEX` only, the other dropped. A head
may list the values of its state cell (the five stage words) so the writer reads them where
it writes; the vocabulary's home stays the skill named.

---

## The index set by archetype

| Archetype | Indexes (the spec's set) | Sectioning |
|---|---|---|
| research (`research_archetype_spec.md` §7) | `MATERIALS_INDEX` · `PAPERS_INDEX` · `OUTPUTS_INDEX` · `ASSETS_INDEX` · `NOTES_INDEX` · `DEEPDIVES_INDEX` | `## general` first where the repo has a shared spine, then `## funding` where the funding layer exists, then by line, every line's section present from birth — the heading and the header row, rows or none |
| NONE — no archetype; the universal index only (`structure_conventions.md`, "`writing_notes/`") | `NOTES_INDEX` alone | unsectioned |

A repo's own catalog that passed the function check
is registered in the root map beside the set, ALL_CAPS, in the form at the end of this file.

## The cells, and which kinds carry them

- **`About`** — the subject, as above; in every row.
- **`Where`** — the path, relative to root; `ledger` appended when the thing has a product
  ledger (`product_ledger_skill.md`), which then holds its representation states, sends and
  feedback. Every kind but two: a paper's pointer is its stem into the archetype's paper home,
  a dive's its `Verification` path.
- **`Forms`** — the forms held, in reading order, shallow to deep; stop at the shallowest
  that answers, open the heavy form only when needed (`structure_conventions.md`,
  "Reading order"). Only where a thing has several forms: materials, papers, outputs. The
  other kinds state their reading order once in the head.
- **The state cell** — where the kind has one, named for what it holds, its vocabulary the
  writer skill's: `Claude status` and `User status` (papers, `materials_processing_skill.md`,
  the status framework), `Stage` (outputs, `writing_drafting_skill.md`), `Verified` (dives,
  the date), `Used in` (assets). Materials and notes carry none.
- **`Reliability` · `Confidentiality`** `[research where the document branch is active]` — the
  two load-bearing tags of `document_processing_skill.md`
  ("Reliability Labels", "Confidentiality Labels"); none on an output, an
  asset, a note or a dive (the dive's reliability is its verification). In a research repo the
  two columns enter `MATERIALS_INDEX` alone, the day `document_processing_skill.md` files its
  first document: the document branch's per-document register lives in the row, never folded
  into a map's `About` or a row's text; `PAPERS_INDEX` never carries
  them, a paper's reliability being its publication.

---

## `MATERIALS_INDEX.md`

```markdown
# MATERIALS_INDEX

Every material brought into the repo that is not a paper — a law that was passed, a decree, a
manual, a dataset, a strategy document, a colleague's document — one row per item, written at
filing by `document_processing_skill.md` (a dataset or an unprocessed item by the session that
places it); papers are in `PAPERS_INDEX`, notes in `NOTES_INDEX`, verified dives in
`DEEPDIVES_INDEX`.
Sectioned: `general` first, `funding` where it exists, then by line.                [research]
A row reads shallow to deep: summary · extract · original.

<!-- slot: index -->
| Item | About | Where | Forms |
|---|---|---|---|
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

A research `MATERIALS_INDEX` takes the header row
`| Item | About | Reliability | Confidentiality | Where | Forms |` once the document branch is
active (the cells rule above), the pass regenerating it at the next stop.
`[research]` the first table sits under `## general` where the repo has one; a repo whose lines are self-contained has no `general/` and its indexes carry no `## general` section.

## `PAPERS_INDEX.md`

```markdown
# PAPERS_INDEX

Every paper, report or book in the literature layer, one row per stem, written at filing by
the paper protocols (`materials_processing_skill.md`; its status framework owns the two status
vocabularies, Claude's set at processing, the user's set only by the user); the bib entry is
in `references.bib`, the summary in the paper's summary file, never here; a chapter processed
and cited on its own is a stem and a row of its own.
Sectioned: `general` first, `funding` where it exists, then by line.                [research]
A row reads shallow to deep: summary · text · pdf.

<!-- slot: index -->
| Stem | Title | About | Claude status | User status | Forms |
|---|---|---|---|---|---|
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

A repo may add one column of its own beside the kit's (a provenance class such as `Source`),
stated in the head; the kit's columns are never reordered. The paper home is not a column: it
is the archetype's (research `general/papers/`), named in the root map. The stem is the pointer
into the home and the bib; a row number is never one.

## `OUTPUTS_INDEX.md`

```markdown
# OUTPUTS_INDEX

Every product the repo has produced, one row per product from its first document on, written
at the outline by `writing_drafting_skill.md`, which owns the stage words (outline · drafting ·
in review · final · published); a product is one thing said several ways, its representations
listed in Forms and its history in the ledger where one exists; a superseded product keeps its
row at `final`, the successor named in About.
Sectioned: `general` first, `funding` where it exists, then by line.                [research]
A row reads shallow to deep: outline · document · deck · translation, then the ledger.

<!-- slot: index -->
| Product | About | Kind | Stage | Forms | Where |
|---|---|---|---|---|---|
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

`Kind` is the product's genre in the repo's words (paper, policy note, brief, deck, proposal,
ToR, op-ed). A deck built from a document is that product's form, not a row; a standalone
presentation is a row. The row points at the folder; a product with a ledger reads `ledger` in
Where, and the ledger, not the row, says which representation is current and what was sent.

## `ASSETS_INDEX.md`

```markdown
# ASSETS_INDEX

Every visual made in the repo — a chart, a figure, a map, a generated image — one row per
asset, written when the visual is made (`visuals_workflow_skill.md`). The kit's own machinery
(its preambles, generator scripts, the palette as code) is not an asset and is rostered in
`CLAUDE.md`'s Skills tables, never here — where `CLAUDE.md` curates the kit-metadata group out of
those tables (`skills_curation_skill.md`), the group is unlisted in `CLAUDE.md` and gets
no row here either. A repo-specific
skill of files that require each other and want no folder of their own is a shared work-product
asset, one row each.
Sectioned: `general` first, `funding` where it exists, then by line.                [research]
A row reads shallow to deep: this row · svg · rendered.

<!-- slot: index -->
| Asset | About | Where | Used in |
|---|---|---|---|
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

`Used in` is the deliverable the asset is embedded in, empty while it is a building block
only; it is the reuse signal (a new visual starts from an old one) and the cell the close-out
refreshes when a deliverable embeds it.

## `NOTES_INDEX.md`

```markdown
# NOTES_INDEX

Every indexed note set in `writing_notes/`, one row per set, written when the set is started
(`writing_notes_skill.md`); About says what the set holds and what you were doing when you
made it, so a set is returned to by purpose. Post-it notes in `workdesk/postits/` are not
indexed here.
Sectioned: `general` first, `funding` where it exists, then by line.                [research]
Unsectioned.                                                                            [NONE]
A row reads: the set's file, or its folder when the set spans files.

<!-- slot: index -->
| Note | About | Where |
|---|---|---|
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

## `DEEPDIVES_INDEX.md`

```markdown
# DEEPDIVES_INDEX

Every verified deep-research dive, one row per dive, written at verification by
`agent_research_verification_skill.md`; a raw dive earns no row, and a claim cites the
verification document, never the raw dive. The skill's own tracker in
`workspace/agent_outputs/` follows every dive at every status; this index holds the verified
ones by subject.
Sectioned: `general` first, `funding` where it exists, then by line.                [research]
A row reads shallow to deep: verification · raw.

<!-- slot: index -->
| Dive | About | Verified | Verification |
|---|---|---|---|
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

`Dive` is the dive's id (the timestamped stem); `Verified` the date; `Verification` the path
of the verification document.

## A repo's own catalog

A domain catalog the repo keeps beside the set, once it passed the function check at the pass
(`structure_conventions.md`, "The root inbox") and is registered in the root map. The kit owns
the head, the markers and the `About` column; the other columns are the repo's, kept.

```markdown
# <NAME>_INDEX

<What is registered, the unit of a row, and who writes it — the repo's sentence, kept.>
<Sectioning, if any.>
A row reads: <the repo's reading order>.

<!-- slot: index -->
| <Item> | About | <the repo's columns> |
|---|---|---|
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

## Two composed heads, the letter for an executor

Research, `MATERIALS_INDEX.md`, empty at birth:

```markdown
# MATERIALS_INDEX

Every material brought into the repo that is not a paper — a law that was passed, a decree, a
manual, a dataset, a strategy document, a colleague's document — one row per item, written at
filing by `document_processing_skill.md` (a dataset or an unprocessed item by the session that
places it); papers are in `PAPERS_INDEX`, notes in `NOTES_INDEX`, verified dives in
`DEEPDIVES_INDEX`.
Sectioned: `general` first, `funding` where it exists, then by line.
A row reads shallow to deep: summary · extract · original.

<!-- slot: index -->
## general
| Item | About | Where | Forms |
|---|---|---|---|
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — created empty at the scaffold*
```

Research, `OUTPUTS_INDEX.md`, an agenda with two lines:

```markdown
# OUTPUTS_INDEX

Every product the repo has produced, one row per product from its first document on, written
at the outline by `writing_drafting_skill.md`, which owns the stage words (outline · drafting ·
in review · final · published); a product is one thing said several ways, its representations
listed in Forms and its history in the ledger where one exists; a superseded product keeps its
row at `final`, the successor named in About.
Sectioned: `general` first, `funding` where it exists, then by line.
A row reads shallow to deep: outline · document · deck · translation, then the ledger.

<!-- slot: index -->
## general
| Product | About | Kind | Stage | Forms | Where |
|---|---|---|---|---|---|

## survey_methods
| Product | About | Kind | Stage | Forms | Where |
|---|---|---|---|---|---|
| mode_effects | survey mode and reported time use: phone against in-person interviews, a randomized comparison | paper | drafting | outline · document · deck | `survey_methods/draft/` |
| questionnaire_length | questionnaire length and item nonresponse: what the pilot rounds show, written for survey teams | brief | final | document | `survey_methods/deliverables/brief/` |

## school_attendance
| Product | About | Kind | Stage | Forms | Where |
|---|---|---|---|---|---|
| attendance_reminders | text-message reminders to parents and school attendance: a field experiment in primary schools | paper | in review | outline · document · translation | `school_attendance/draft/` |
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — attendance_reminders moved to in review*
```

---

<!-- Kit file marker below: the template's own version line, not part of any repo file. -->
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
