---
name: research-archetype
description: >
  The structure-and-index preset for a research repo — work organized around
  research lines (a paper, or several papers sharing literature/background as an
  agenda). Kept only by repos whose declared type is research. Read after
  structure_conventions.md and archetype_conventions.md (the common layers),
  alongside naming_conventions.md. Defines the line-container
  shape, the general/ shared spine, placement rules, the six root indexes, notes
  and deep dives, and retention — the invariants the archetype audit checks a
  research repo against.
triggers: >-
  Structuring, placing, indexing or auditing files against this repo's declared archetype.
  Kept where the `type` in `CLAUDE.md`'s frontmatter is `research`; none in NONE
---

# Research archetype — spec

*The archetype-common
machinery — born-minimal promote-on-evidence, origin-based typing, the
shared-spine / "one repo or two" test, by-subject keying, the archetype-fixed
root skeleton — lives in `archetype_conventions.md`; the universal floor (naming,
`FOLDER_MAP`, structure conventions, the `_ex` rule, reading-order) in
`naming_conventions.md` / `structure_conventions.md`. This doc describes only
what is **specific to a research repo** — research's forms of those common rules,
and its own index set.*

---

## 1. What this is, and when it applies

A research repo holds work organized around **research lines** — a paper, or
several papers that share literature/background/empirics (an "agenda"). **Paper
and agenda are one archetype:** an agenda is the same layout with more than one
line. A single paper is the archetype at **N = 1 line**.

North-star: the archetype-common by-subject acceptance test
(`archetype_conventions.md`), in research's form — **any paper, note, or asset
findable by its subject (the `who_what_year` stem, the line-sectioned indexes)
without remembering where it lives, and never scanning the repo (or its
branches) to locate it.** Every rule below serves that.

## 2. What exists up front vs. what is born later

The universal **created-up-front vs born-on-creation** rule
(`structure_conventions.md`) governs; this is its research realization:

- **Created up front** (the layout *determined* by "this is a research paper"):
  the indexes, `general/` and its standard subfolders, the line container with
  its map and `deliverables/`, the folders the line's stage offers, and every
  `FOLDER_MAP` the leaf rule requires — present from the start even when empty,
  each documenting what belongs in it.
- **Born later**, each with its condition on the manifest line
  (`research_setup_scaffold.md`, the tagged tree; the four birth kinds in
  `structure_conventions.md`): the line's `context/` when line-specific setting
  material appears, at any N (§6); the `deliverables/` categories when the first
  of each is produced (§5); `draft/versions/` at the first feedback received on
  the draft; `correspondence/` when the line is submitted (§3); `explorations/`
  on the first merged exploration; `archive/` on the user's ruling only (§12); a
  second line when it exists. Presence before the condition is never drift.

## 3. Core shape — the prefixed line-container

Each research line is a **container folder, named for the line, carrying the
standard skeleton inside it**:

```
<line>/
├── FOLDER_MAP.md          ← the line's map; its slot row carries `Stage: <word>` — the one
│                            home of the stage; records cross-line pointers
├── draft/                 ← the paper draft (the academic paper) — only this
│   ├── versions/          ← born at the first feedback: byte-exact copies as sent (§12)
│   └── archive/           ← born on the user's ruling: a draft become too different (§12)
├── empirics/              ← the empirical work — data, code, results (active stage)
├── research_proposal/     ← the proposal (active stage; advisory when the work is one)
├── deliverables/          ← umbrella, with every line; categories born on demand (§5)
├── context/               ← born when line-specific setting material appears (§6)
├── correspondence/        ← born at submission: referee reports, editor letters (§3)
├── explorations/          ← born on the first merged exploration (structure_conventions.md)
└── inputs_from_team/      ← born when a colleague without access sends a file for this line
```

`empirics/` is one folder for the empirical work, whatever its method. *(Documented
predecessor: through v6.3 the active stage offered `quantitative/` and `qualitative/`,
a split that predicted a method before the work existed. The pair merges into `empirics/` at a kit update,
`git mv` with the map and index rows fixed.)*

Two non-negotiables:

- **The line is named/prefixed from day one** — even a lone paper gets
  `<paper>/`, never a bare `draft/` at the root. This makes growth
  *append-only*: a second line is added beside the first, never nested
  reactively. Bare root names are the path-dependency trap.
- **The skeleton lives inside the container.** Root holds *lines* (plus
  `general/` and machinery), not line×subfolder. Inner folders are bare
  (`draft/`, not `<line>_draft/`) — the container namespaces them.

`draft/` holds **only the paper draft**. All other deliverables (a government
policy brief, a report to your boss, a presentation, …) live under
`deliverables/` in categories created on demand (§5).

### Per-line stages — a closed vocabulary, one home, forward only

Every line carries a **stage**, one of **seven closed words**: four that form the
**forward-only sequence of a paper**, each entered by an event — `active` (the paper
is being made: the pre-working-paper stage), `working_paper` (the draft was complete
enough to go out, and went out: submitted to a working-paper series, or circulated
as a working paper — the going-out is the event), `under_review` (submitted to a
journal, which opens the referee channel; a revise-and-resubmit stays here),
`published` — and three **non-paper kinds** —
`chapter` (a book chapter, not an academic paper), `advisory` (no paper;
deliverables-led) and `reference` (a line that exists to serve other lines —
comparison material, a country's source documents — and produces no paper of its
own; it never advances).

**One home.** The stage lives in the line's `FOLDER_MAP.md` slot row, in one fixed
form: `Stage: <word>` (the kit-owned row, `structure_conventions.md`, the `FOLDER_MAP`
form). Nowhere else: the pre-v6.4 "agenda, mixed" stamp in `CLAUDE.md` and the light
heading-toward note are retired. A line with no stage is a finding; the pass proposes
one read off the folders. Every research repo declares `variant = single-paper /
agenda`; a mixed agenda is simply lines at different words.

**Closed and intentional.** The seven words are mandatory and the vocabulary is closed:
an off-vocabulary label (`editing`, `first draft`, `submitted`, `revise-and-resubmit`)
is mapped to its word at the pass (`editing`, where it names a paper at the
journal, → `under_review`, or `published` when the paper is out; `submitted` and
`revise-and-resubmit` → `under_review`; `first draft` → `active`). An **eighth word is a kit change**: its CHANGELOG entry says which word
failed and why, and the pass maps old labels from that entry.

**Forward only, nothing removed.** A paper moves `active` → `working_paper` →
`under_review` → `published`; a line never goes back, and no folder is removed at a
transition — `published` keeps everything. The label is moved forward by the user's
session, and the freshness check's stage-drift pass (`project_tracker_skill.md`, Pass
3) prompts the label forward when the folders outrun it (a `working_paper` line with
referee reports in `correspondence/` is `under_review`). `advisory` → `active` when
the work starts a paper; `chapter` stays `chapter`.

What each stage **offers** (created with the stage; a folder beyond the offer is
still born on its own condition, never forbidden):
- **active** — `draft/`, `empirics/`, `research_proposal/`, `deliverables/`.
- **working_paper** — nothing new; `draft/versions/` at the first feedback.
- **under_review** — `correspondence/` (the submission channel, below).
- **published** — nothing new; kept, never deleted.
- **chapter** — `draft/`, `deliverables/`.
- **advisory** — `deliverables/`; `context/` on setting material;
  `research_proposal/` when the work is itself a proposal.
- **reference** — the source documents and their derived files (`TEXT_`, `SUMMARY_`, the
  summaries the served line cites); no `draft/`, no `deliverables/`; the line never advances.

**`draft/` is the universal "primary written output" folder** across stages — the
chapter for a `chapter` line, the paper draft for an `active` line. The stage word
disambiguates; the folder is never renamed on transition.

### The submission channel — `correspondence/`

A line's **`correspondence/`** is the **formal submission channel only**: referee
reports, editor letters, and the responses to referees — born when the line is
submitted to a journal, the `under_review` stage; a working-paper series opens no
referee channel, so the `working_paper` stage has no `correspondence/`. Nothing else
lives there. Material made outside the repo and used
as-is — a coauthor's or contractor's deliverable, a data buy, a colleague's comments
file — is `inputs_from_team/` when the person has no repo access, and is placed on a
branch by the person when they do (`structure_conventions.md`, "Inputs by origin" and
"Collaborators"). The request that commissions a consultant's work is a hiring ToR and
lives in `funding/<module>/instances/` (below), never in the line. *(Documented
predecessor: through v6.3 `correspondence/` was the home for anything exchanged with
people outside the line's work, requests and returns filed together; the widening
made it a second inputs folder, and the boundary is drawn at the channel.)*
Placement follows the usual rule: tied to one line → that line's `correspondence/`;
spanning lines → an **agenda-level `correspondence/`** sibling to `general/`.

### `funding/` (agenda-level, first-class)

An agenda may carry a first-class **`funding/`** folder, born when **any funding or
contracting instrument** exists — a grant, a commissioned study, a terms of
reference — for that instrument's material: proposals, budgets, project
documents, ToRs; an
instrument's folder carries its own `feedback/` on the first review of the instrument
(`structure_conventions.md`, "`feedback/`", the one other home). It
is a *recognized* archetype folder, sibling to `general/` — **not** an `_ex` slot, so
it doesn't spend the repo-specific-root budget. Its presence is a module trigger
(`structure_conventions.md`, "Modules"): a module that drafts
the instrument or a hiring request lands at `funding/<module>/`; a ToR
for work that has a repo is made in that repo, and a consultant's commissioning ToR
for a research line lives in `funding/<module>/instances/`, not in the line's
`research_proposal/`.

## 4. The shared spine — `general/`

`general/` is the repo's **central shared layer** (vs. line-specific): the
shared **literature** you draw *from* (papers and background). **A repo whose lines are
self-contained has no `general/`** — every line a paper predating the repo, no shared
reading — and its typed indexes carry no `## general` section. *(Documented
predecessor, to v6.5: it also held the central `notes/` tracker; indexed notes
now live in the universal `writing_notes/`, §8.)* **Background is shared by nature and lives in `general/background/`; a line's
`context/` is born when line-specific setting material appears** — what belongs in
the paper's background section for that line — at any N (§6).

Reference/background material lives in `general/` **regardless of how many lines
use it** — it's *referential*, not *transformed*, and pre-placing it here avoids
a later lift. (This is the key refinement of the placement rules: see §5 rule 3.)

**Actions waiting on the user live in the workdesk queue (`workdesk/INDEX.md`),
not in `general/`** — the universal pending-actions queue, defined in
`structure_conventions.md` (working-tracker-not-catalog, pointer-not-artifact,
no index row, pointed at from `STATUS.md`). Forward-looking
actions are a universal construct, so `general/` carries only the shared
literature. *(Documented predecessors, and a live migration source: the research-specific
`general/to_do/`, then v4's universal `workspace/to_do/`, which the workdesk
queue replaced in turn. A research repo arriving at
Part C with a live `general/to_do/` is expected, and it is a named migration
source in `PROJECT_SETUP.md` Part C Step 8.5.)* (A pending action is still not a
note — notes are reading/thinking, indexed by line-of-thinking in `NOTES_INDEX`;
queue rows are actions, not retrieved by subject. The user's post-it notes
live in `workdesk/postits/`, not `writing_notes/` — see the boundary in
`structure_conventions.md`.)

## 5. Placement — the rules

Decide any item's home by how it's used:

1. **Co-owned reference → `general/`.** Shared **literature** (shared by nature),
   regardless of consumer count. But **source/institutional/setting material is
   line-specific** — in a multi-setting agenda it lives in each line's `context/`,
   not a shared `general/background/`. `general/background/` exists only for
   background genuinely co-owned across lines (e.g. a single paper, where it merges
   with context until expansion, §6).
2. **Produced by one line, reused by others → owned by the producing line,
   others point.** A result one line makes lives in that line; consumers
   reference it via a `FOLDER_MAP` pointer — never copied, never hoisted to
   `general/` (it's owned, not co-owned).
3. **Transformed/data input consumed by one line → nested inside that line.**
   This rule is for **inputs a line transforms** (e.g. a dataset feeding a
   model), *not* reference/background material (which goes to `general/` per
   rule 1 even at single use). It graduates to its own home (a pointer target)
   only if a second consumer appears.

**Visuals are their own layer.** Every visualization you make — charts, figures,
maps, one-offs included — goes in **`ASSETS_INDEX`**, because a visual is revised
across the paper's life (a living object, not a frozen output). The kit's own
machinery (preambles, generator scripts, palettes-as-code) is *not* an asset — it lives in
`skills/` and is rostered in `CLAUDE.md` (§9); a repo-specific skill of two or more files
that require each other and want no folder of their own is a shared work-product asset,
one `ASSETS_INDEX` row each.

**Deliverables are created on demand.** `deliverables/` is the line-level
umbrella; its categories are born when the first of each is produced and are
**named for what they are** — e.g. `policy_brief_gov/`, `report_<recipient>/`,
`presentations/`. No category is pre-created empty.

## 6. Expansion — when a line grows or a second line appears

Expansion is a **deliberate decision point**, not an automatic "add a folder."
When (if) the repo grows, ask **"in which direction?"** — another paper in the
same setting / a new country / a new system / a new method — and *that answer*
decides the split:

- The **background-vs-context split is decided here** for an agenda: what was
  genuinely shared stays in `general/background/`; what turns out to be specific
  to one line moves to that line's `context/`. The split is made *with
  information*, at the moment you have it. (`context/` itself is content-defined,
  not expansion-born: a single paper with setting material of its own already
  carries one. Expansion is where the split rule bites, not where the folder is
  born.)
- A **second line-container** is added beside the first (append-only).
- Shared material is **lifted to `general/`** as it becomes co-owned.

**At an agenda restructure** (multiple lines already present), this split is not
deferred — it's decided when the lines are decomposed: the lines and
the shared-vs-line-specific assignment (`general/background/` vs each line's
`context/`) are determined up front, because the information already exists.

Expansion is also where the archetype-common **"one repo or two" test**
(`archetype_conventions.md`) bites, in research's terms: lines that share no
literature/background/empirics are probably **two repos, not an agenda** — the
shared spine (`general/`) is what earns the composition.

## 7. Indexes

**Six index files at the repo root.** All follow the archetype-common
typed-index behavior (`archetype_conventions.md`: created up front and
self-documenting, pointer-only, self-registered at creation), each in the drawn
form of `typed_index_template.md` (the head, the header row, the markers, the
trailer); research's form is **line-sectioned** — `## general` first, a line's
section born with its first row:

- `MATERIALS_INDEX.md` — every material brought in that is not a paper (a law, a
  decree, a manual, a dataset, a strategy document), one row per item; its head
  says that papers, notes and dives are in their own indexes.
- `PAPERS_INDEX.md` — every paper in the literature layer, one row per stem, with
  the two reading statuses of the materials skill's status framework; the bib
  entry is in `references.bib`, the summary in the summary file, never in the
  row.
- `OUTPUTS_INDEX.md` — every product the repo has produced, one row per product
  from its outline on, with its stage; a product is one thing said several ways,
  the deck built from a document a form of that product, not a row.
- `ASSETS_INDEX.md` — **all visualizations you made** (§5), with where each is
  embedded.
- `NOTES_INDEX.md` (§8), `DEEPDIVES_INDEX.md` (§8).

**Entry encoding — layered pointers in reading order.** Where a thing has
several forms (a paper, a material, a product), the row's `Forms` cell lists
them shallow-to-deep, and a reader stops at the shallowest layer that answers,
opening the heavy form only if needed (a paper's `summary · text · pdf`, never
the PDF unprompted; a product's `outline · document · deck`, then the ledger).
An asset's, a note's or a dive's row has no `Forms` cell: its head states the
reading order once (the row, then the svg, then the render; the note file; the
verification, then the raw dive).

**By-subject retrieval** is one scan of the six indexes' `About` cells, the
subject in Claude's words written at filing, a subject already named keeping its
words (the template). No subject tags: the index is its own vocabulary.

## 8. Notes and deep dives

- **Notes cluster centrally** in the universal `writing_notes/` home
  (`structure_conventions.md`): a set is a file, `writing_notes/<set>.md`, a
  subject subfolder when a set spans files (e.g. `literature/`); never inside a
  line. Indexed in **`NOTES_INDEX.md`**, **sectioned by line, `general` first**
  (research's realization of the universal index), which records per set **what
  it holds** *and* **what you were doing when you made it** (the line of thinking
  at creation) so you return by purpose, not by guessing. *(Documented
  predecessor, to v6.5: `general/notes/<subject>/`, migrated whole at a kit
  update, citations rewritten.)*
- **Deep dives** (verified deep-research runs) → **`DEEPDIVES_INDEX.md`**, a
  detail index `MATERIALS_INDEX` points at. **Only verified dives are
  indexable;** a raw dive earns no row. Use a dive's findings, but **cite the
  verified output**, not the raw dive. Craft/log files (`LESSONS`,
  `WORKFLOW_SKIPS`) stay *outside* the catalog.

## 9. `FOLDER_MAP.md`, the root inbox, and placement

**`FOLDER_MAP.md`** is the universal distributed-index convention
(`structure_conventions.md`): every content folder carries one (description +
map) except a leaf born on content, holding tracked files a typed index or the
parent map enumerates fully; the test is the folder's state, never its name (the
leaf rule); machinery and desk (`skills/`,
`workspace/`, `workdesk/`) carry none below their roots (an orientation map at a
root by its kind word, kept only where it says something of the repo's).
The form is `FOLDER_MAP_template.md`: title, the slot row `Kind: line · Stage:
<word>` (the one home of the stage), the line's latent homes as a `kit` block,
the description and catalog slots, one trailer line. Research specifics: it
does **not** re-list the detail the typed indexes hold (no double-writing; a
`papers/` row points at `PAPERS_INDEX`); plain name everywhere, the path
disambiguates. *(Documented predecessor: the `## Work folders` and `## Cross-line
pointers` sections of earlier kit versions; the catalog holds the first, the
description states cross-line consumption where it exists.)*

**The current-shape paragraph.** A line's description slot may open with a **dated,
pointer-only paragraph** stating the line's current shape: which artifact is
canonical, what is retired and where, which representation has been presented,
and where the product ledger is. It answers "what is the real version of this
line right now" without making the reader walk the folders. **Discipline:
pointers and one-line positions only, always dated.** The block is a cache over
the ledger and the folder maps — on any disagreement they win
(`product_ledger_skill.md`'s ownership boundary) — and the moment it carries
facts of its own it has become a second ledger, which is the drift this
convention exists to prevent.

**Skills, assets, machinery.** A repo-specific skill need not sit in `skills/`;
it may live where it's produced **as long as it's registered in `CLAUDE.md`**
(the skills table is the roster — no separate skill roster). The division with
assets: **loaded/run by name → `skills/` + `CLAUDE.md` roster, not in
`ASSETS_INDEX`**; **a made visual retrieved by subject → `ASSETS_INDEX`**.

**The root inbox** is the universal intake rule (`structure_conventions.md`):
loose content at root is *accidental staging* — it means "needs placing" and is
swept into the same intake check as `workspace/staging/`. Root should normally
be empty of loose content.

## 10. Naming

Naming follows `naming_conventions.md` (content `lowercase_underscore`,
structural `ALL_CAPS`, the content-file markers `ALL_CAPS` on a lowercase stem).
Research-specific points, all governed by that file:

- Paper stems keep `who_what_year`, lowercase (`acemoglu_simple_ai_2024`). **The
  stem is the BibTeX cite key**, so renaming a stem rewrites the `.bib` keys and
  every `\cite{}` — see `naming_conventions.md` for the stem/cite-key rule.
- Compound surnames collapse to one lowercase token (`DellAcqua` -> `dellacqua`).
- Human-readable display text (titles, headings, index labels) is exempt.

## 11. The `_ex` exception discipline

The `_ex` gap-slot rule is universal (`structure_conventions.md`): at most two
per level, `_ex` suffix, a third (`_ex3`) flags a missing folder. In a research
repo the **levels are repo root and inside each line**, and a missing folder
means a gap against the research skeleton (§3) — the archetype is missing a
folder the work needs.

## 12. Retention and reading-order (keep both forms)

Both forms of a thing are kept by design — **no canonical-vs-derived flag**.
Retention by type: papers/materials keep PDF + extraction + summary; visuals keep
source (svg) + rendered; written work keeps **all `.md`s** (full thinking
history) but **only the last rendered doc**. The index encodes reading order
(§7); it does not mark a "canonical" form. This is a reading-cost optimization —
shallow first, heavy form only when needed.

**0-byte source placeholders:** if a source file is empty (0 bytes) but its
derivatives (extraction/summary) are full, delete the empty source, keep the
derivatives, and write a `workdesk/INDEX.md` row (Action: do) naming the
wanted original.

**The line-level `archive/` — whole-folder retirements within a line.** When a
whole folder of a line is retired — a superseded prospectus, a legacy layer, an
abandoned lineage — it moves to the line's own
`<line>/archive/YYYY-MM-DD_<brief-description>/`: dated, append-only, sibling
of the line's `draft/archive/` where one exists. **Retire, don't delete** (the
line-scope realization of the universal nothing-destroyed rule in
`structure_conventions.md`): the folder map records what moved and why, and
nothing is destroyed on a state change. Both `archive/` folders are
**judgment-born** (`[J: writing_drafting_skill.md]` in the manifest): the drafting
skill proposes a new draft when the message, the results or more than about half
the structure change, and on the user's ruling what was there goes to archive; the
pass never creates the folder and the audit never flags its absence. Versions are not archive: `<line>/draft/versions/` holds the
byte-exact copies of the draft as it went to reviewers
(`structure_conventions.md`, "Versions vs. archive"), a sibling of `archive/`,
never the same thing.

## 13. Root files and machinery

Root files (`CLAUDE.md` + the archetype declaration, `STATUS.md`), `workspace/`
and its created-up-front subfolders, `workdesk/` (the pending-actions queue +
`admin/` + `postits/`), `feedback/`, `writing_notes/` (the indexed-notes home,
§8) and `skills/` are the universal layer (`structure_conventions.md`). Research-specific: `CLAUDE.md` declares
`variant = single-paper / agenda` alongside `type`; the
line stages live in the line maps only (§3), never in `CLAUDE.md`. The root
`FOLDER_MAP.md` holds the skeleton, the root documents (the six indexes,
`references.bib`), the latent homes (`funding/`, `quarantine/`,
`inputs_from_team/`) and the registered extras.


---
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
