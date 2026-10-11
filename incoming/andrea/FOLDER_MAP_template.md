# FOLDER_MAP.md — the template (every content folder, and the repo root)

The map of every content folder that carries one, and the root map of every repo. A map is
written for Claude and never read at session start. It is read at four moments: **placing** (a
file is about to be created or moved, and the target folder's map says what goes there),
**locating** (the user asks for something by name or topic, and Claude walks the maps to find it
without scanning the tree), the **structural readings** (the pass and the audit read the root
map's blocks against disk, a line map's stage word at the drift peek) and the
**close** (the close-out rewrites the catalog and the trailer
of every touched folder). Its job is that Claude can place and find without scanning, and that
the pass and the audit can read a folder's structural claims without inference
(`structure_conventions.md`, "Who these files are for"). Locating runs index first: a thing of
a registered kind (a paper, a material, an output, an asset) is found through its
typed index, and the maps are the lookup
for everything else and for a NONE repo entirely; the root map is where Claude learns which is
which, its root-documents block naming each index with what it registers.

**The form, fixed.** Title line, the slot row, the kit blocks the folder's kind carries, the
`description` slot, the `catalog` slot, the `unplaced` slot, one trailer line. No headings: the
markers are the names. Nothing with a home elsewhere is restated in a map — the variant
lives in `CLAUDE.md`'s frontmatter, the birth tags in the manifest, a registered item's
status in its index — and the map points where it must. The fill rules — create where the leaf
rule requires one, regenerate the form, keep the rows, drop the retired headings — are
`PROJECT_SETUP.md` Step 7.5 part 2, never here.

**Markers** (`structure_conventions.md`, "Slots and markers, one notation"): `kit: <name>`
around every block, regenerated whole at every stop; `slot: description` and `slot: catalog`
around the repo's text, the catalog's header row being kit form regenerated at every stop and
its rows the repo's; `slot: unplaced` in every map, empty in the normal state. A map is created
in this form, empty, by whoever creates the folder — the scaffold, the pass, a promotion, the
placement check mid-session, the merge sweep — so that when the folder fills the map is there
to fill. Where a form below reads `<...>` it is a placeholder and is not copied.

---

## The slot row

The third line of the file, bare, no bold, no marker: the fixed prefix is the grep.

```
Kind: <word>
Kind: line · Stage: <word>
```

The row carries the folder's **kind** and, for a research line, the **stage** — its one home
(`research_archetype_spec.md` §3, the seven closed words). Nothing else rides on it. The kind
selects the blocks the map carries and the grain of its catalog:

| Kind | Which map | Blocks | Catalog rows |
|---|---|---|---|
| `root` | the repo root map only | skeleton, root_documents, latent_homes, extras | none: the blocks are the catalog |
| `line` | a research line | latent_homes; `Stage:` on the row | the line's present subfolders and loose files |
| `category` | a folder holding units or subfolders | none | one row per unit, its subject |
| `leaf` | a folder of files no index enumerates; or a folder whose files a typed index or the parent map registers, created empty by the scaffold or the pass (`writing_notes/`, `draft/`) — the map persists it across a clone | none | one row per file; where an index registers the files, one pointer row naming the index and never a re-list |
| `module home` | a module's home, beside its `MODULE.md` | none | the repo-side entries; the kit files point at `MODULE.md` |
| `orientation` | an orientation-only map at `workspace/`, `workdesk/` or `skills/` root | none | no catalog |

The list is closed. A kind the list lacks is a kit finding, never a word improvised in a repo.
*(Documented predecessor: the `**Type:** · **Stage:**` header line earlier kit versions
wrote in every map, and its per-kind variants — `**Line:** · **Stage:** · **Spec:**` —, replaced
by this row at a kit update; the spec version travels with the kit and is declared nowhere since v6.6.)*

## The kit blocks

A block is a list, one line per entry, path in backticks, an em-dash, then the entry's job or
condition. Every block has a fixed empty line, so an empty block is a claim the audit reads,
never an omission. Blocks come before the slots, in the order below.

**`skeleton`** (root map). One line per root folder present on disk, the universal layer
included, the job from the manifest's comment column (`<archetype>_setup_scaffold.md`) or, in a
NONE repo, from the bespoke skeleton the user approved, at birth or, in a repo that predates
the declaration, at the first pass. No tags: the tag's home is the
manifest, the block states what is on disk.

```markdown
<!-- kit: skeleton -->
- `general/` — the central shared literature layer
- `<line>/` — <the line's subject>
- `workspace/` — Claude's working layer
- `workdesk/` — what waits on the user
- `feedback/` — feedback received on the repo's products
- `writing_notes/` — the indexed note sets, under `NOTES_INDEX`
- `skills/` — the kit and the repo-local skills
<!-- /kit -->
```

**`root_documents`** (root map). Every file at root: the kit-shaped files on one fixed line,
then one line per typed index, `references.bib` and born-on-use file once born, each
with what it registers — the line that routes a locating session to the right index. A repo's
own domain catalog that passed the function check is registered here beside the spec's set,
ALL_CAPS like them. A root file not in the block is a finding for the function check
(`structure_conventions.md`, "The root inbox").

```markdown
<!-- kit: root_documents -->
- `CLAUDE.md`, `STATUS.md`, `README.md`, `FOLDER_MAP.md`, `.gitignore` — the kit-shaped root files
- `PAPERS_INDEX.md` — registers every paper in the literature layer, by stem
- `MATERIALS_INDEX.md` — registers every processed material, by stem
- `NOTES_INDEX.md` — registers every note set in `writing_notes/`, by set (every repo, NONE included)
- `references.bib` — the bibliography
- `STATUS_ARCHIVE.md` — closed records rotated out of `STATUS.md`
- `RECORD.md` — where the project stands at the big-picture level, by part; born at the first row
<!-- /kit -->
```

**`latent_homes`** (root map; line map). One line per declared home not yet born — the `[E]`
and `[J]` lines of the manifest under this folder; in a NONE repo, the `[E]` lines of the
universal manifest (`structure_conventions.md`, "A NONE repo declares its skeleton once") — with
its condition and, where a New homes line named candidate material in this repo, the candidate
awaiting ruling.

```markdown
<!-- kit: latent_homes -->
- `funding/` — born on: any funding or contracting instrument — candidate: none
- `correspondence/` — born on: the line is submitted to a journal — candidate: none
<!-- /kit -->
```

Empty line: `- none: every declared home is born`.

**`extras`** (root map). The register of root folders beyond the skeleton, one line each with
its job and the date it was registered; the two-extra cap is read from the count
(`structure_conventions.md`, "Governance rules").

```markdown
<!-- kit: extras -->
- `<folder>/` — <job> — registered YYYY-MM-DD
<!-- /kit -->
```

Empty line: `- none registered`.

## The description

What is here and what goes here, in the repo's words, never a restatement of the spec or the
floor. A line's description may open with the dated, pointer-only **current-shape** paragraph
(`research_archetype_spec.md` §9: which artifact is canonical, what is retired and where, which
representation has been presented; a cache over the ledger). A folder's own working rule —
"sections first, then the summary" — lives here too, being a placement-time rule
(`CLAUDE_template.md`, the structure pointer). A folder's own live external facts — a funder's
deadlines, an award's binding commitments, a position in an external cycle — are the
description's first paragraph; the form has no slot for them and needs none. A description is about a paragraph; one over
about 150 words is reported to the user at the pass, never cut.

## The catalog

One table, one header for every kind, empty state the header alone:

```markdown
<!-- slot: catalog -->
| Path | What is here |
|---|---|
<!-- /slot -->
```

Three row rules. **Present contents only:** a moved or retired entry leaves this catalog and
appears in the map of the folder it went to; the trailer names the change once, git keeps the
rest; a row that stays to say "this used to be here" is a finding. **Point at the index, never
re-list:** a subfolder whose contents a typed index registers gets one row that names the index
(`papers/` — the literature layer; every paper registered in `PAPERS_INDEX`), the leaf rule read
from the parent. **No counts, no dates in a row:** a count goes stale on the next file and the
date is the trailer's; a row says what a thing is. What varies by kind is the rows (the kind
table above), never the columns. A status column is a live claim with a home elsewhere — the
typed index for a registered item, the ledger for a package.

## The trailer

One line, the last in the file, rewritten in place by the close-out and the pass
(`project_tracker_skill.md`, "Catalog refresh"): `*Last updated: YYYY-MM-DD — <what changed>*`.
The trailer line is written when the map is created, not first when it changes.
No stack; a stack found at the pass is deleted, its history being git's.

## Length

Kit form about 20 lines for a map with no blocks (title, row, three marker pairs, the header
row, the trailer) and about 45 for a root map with typical blocks; the catalog has no budget,
it scales with the folder; the description's paragraph as above. Lines beside.

---

## The root map

```markdown
# FOLDER_MAP — root

Kind: root

<!-- kit: skeleton -->
- `<folder>/` — <job>
<!-- /kit -->

<!-- kit: root_documents -->
- `CLAUDE.md`, `STATUS.md`, `README.md`, `FOLDER_MAP.md`, `.gitignore` — the kit-shaped root files
- `<INDEX>.md` — registers <what>
<!-- /kit -->

<!-- kit: latent_homes -->
- none: every declared home is born
<!-- /kit -->

<!-- kit: extras -->
- none registered
<!-- /kit -->

<!-- slot: description -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

The root map carries no `catalog` slot: the skeleton and the root documents are its catalog.

## A line map

```markdown
# FOLDER_MAP — <line>

Kind: line · Stage: <word>

<!-- kit: latent_homes -->
- `<path>/` — born on: <condition> — candidate: none
<!-- /kit -->

<!-- slot: description -->
<!-- /slot -->

<!-- slot: catalog -->
| Path | What is here |
|---|---|
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

## A category, leaf or module-home map

The no-block form: the kind word varies, the rest is the same.

```markdown
# FOLDER_MAP — <path from root>

Kind: <category | leaf | module home>

<!-- slot: description -->
<!-- /slot -->

<!-- slot: catalog -->
| Path | What is here |
|---|---|
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

A module home's catalog rows the repo-side entries (`instances/`, `parameters.md`, a
`corpus_inbox/` drop, the baseline); its kit files take one row pointing at `MODULE.md`, whose
anatomy is the kit's (`structure_conventions.md`, "Modules"), and the two kit-side files that
never travel (`corpus/`, `CHANGELOG.md`) take one pointer row each to their place in the kit.
A module's maps — the home's and its subfolders' — are the repo's, never the module's
(`structure_conventions.md`, "Modules"): born at the land, filled by the pass from disk,
never compared or landed at an update, so a copy's map rows what is on
that disk under the home's path, and the canonical copy's map in `modules/<name>/` in your
canonical skills repo is that repo's own, rowing the kit's folder under the kit's path.

## An orientation-only map

Allowed, never required, at the root of `workspace/`, `workdesk/` or `skills/`; nowhere below
them, where the standing documents are the lookup surface. The description role alone, kept
only where it says something of this repo's that the floor and the standing documents do not;
one that restates them is deleted at the pass and reported. No catalog, no `unplaced`, no
close-out obligation.

```markdown
# FOLDER_MAP — workspace

Kind: orientation

<!-- slot: description -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

---
<!-- Kit file marker below: the template's own version line, not part of any repo file. -->
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
