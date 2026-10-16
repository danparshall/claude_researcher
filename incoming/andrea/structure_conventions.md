---
name: structure-conventions
description: >
  The kit's universal structure layer (the floor), kept in every repo regardless
  of archetype (including NONE). Opens with the two standing principles: who
  these files are for (every repo file is written for Claude; reading cost is
  the design measure) and conformance by job (one home per job at the kit's
  path; the tagged birth tree as the one manifest; slot markers; latent homes;
  the New homes line). Then the root files (CLAUDE.md, STATUS.md, the root
  FOLDER_MAP.md, README.md, .gitignore), workspace/ and workdesk/ (the waits-on
  split: Claude machinery vs. what waits on the user, incl. the pending-actions
  queue), the collaborator convention with the merge-time folder sweep,
  feedback/, quarantine/, the three input words (inputs/, sources/,
  inputs_from_team/), the FOLDER_MAP form and leaf rule, the session-close
  refresh, the extras rule with its four readings, the _ex slots, the four
  birth kinds, the root register, the intake funnel and root-as-accidental-
  staging, reading-order, versions vs. archive, skills layout, and the module
  tier. The archetype-common rules live in archetype_conventions.md, and the
  per-archetype folder structure and index set in the repo's archetype spec,
  not here. Read when creating or placing any folder.
triggers: >-
  Creating or placing any folder or file; something starts waiting on the user; the form of
  every kit-shaped file. The universal floor, kept in every repo
---

# Repo structure conventions — the universal layer

Describes the universal layer every repo gets regardless of type. The layers
*above* it are **not** here: the archetype-common rules live in
`archetype_conventions.md`, and the per-type purpose-folders and index sets live
in the repo's archetype spec (the one spec the repo keeps for its declared type).
A NONE repo carries only this universal layer (plus a bespoke skeleton); an
archetype repo reads all three, in order.

## The three-layer model

A repo's structure has three layers:

1. **Universal layer (this document).** Archetype-independent — identical in
   every repo, and what makes the skills operate at all. Every repo keeps it,
   including a NONE repo.
2. **Archetype-common layer (`archetype_conventions.md`).** The rules shared by
   every archetype repo but meaningless without one — born-minimal promotion,
   origin-based typing, the shared-spine test, by-subject keying, the
   archetype-fixed root skeleton. Carried by every research repo; **a NONE
   repo does not carry it.**
3. **Type-specific layer (the archetype spec).** The part that *varies* across
   repo types: which purpose-folders a repo has and which indexes it carries. It
   lives in the one `<type>_archetype_spec.md` for the repo's declared type. A
   NONE repo has no archetype spec — it is not a deficient archetype but a
   *kind* of its own: the **general-purpose kind**, any repo that is not a
   research repo. It carries the universal layer only
   (`structure_conventions.md` + `naming_conventions.md`) plus a skeleton
   tailored to its own work, its bespoke skeleton, declared once in the root
   map's skeleton block.

**Where a rule lands — one test, applied twice.** (1) Does it survive without an
archetype? Yes (it holds for a NONE repo too) → it is universal, here. No → not
universal. (2) Does it have a type-specific form? That part peels to the spec
(L3); the general principle behind it stays in `archetype_conventions.md` (L2).
The axis is **general-vs-specific, not count** — with one archetype in the
package the principle still sits in `archetype_conventions.md` and its
realization in the spec.
`archetype_conventions.md` states the full model and owns the layer between this
floor and the spec.

## Who these files are for

Every file the kit shapes in a repo (`CLAUDE.md`, `STATUS.md`, the maps, the
indexes, the standing documents, ONBOARDING, `MODULE.md`) is written for Claude.
The user organizes their mind through the repo's structure and knows what to ask
from it, but they almost never open these files; when they need something they
ask in chat, and the chat is the human-facing surface. Two exceptions:
`README.md`, rendered by GitHub for whoever has access (below), and a
collaborator's `ONBOARDING.md`, written for the person who joins and read by
them once (their Claude takes the repo from the
kit-shaped files like any session, and from ONBOARDING only the reading list,
the order in which to put the repo in front of the person; "Collaborators"
below). So the design
measure for every kit-shaped file is **what it costs its reader, Claude**, and
the cost model is:

- **Reading is the cost, not opening.** Everything read at session start stays
  in working memory all session, and stale text is followed as instruction. A
  long file is expensive every turn; a wrong line is worse than a missing one.
- **Split by the moment of need.** Read every turn: `CLAUDE.md`. Read at a known
  moment: a second file, with a pointer and its trigger in `CLAUDE.md` (STATUS on
  "yes", a skill on its phrase, a map when placing). Never read at start:
  archives and records.
- **Fixed headings, fixed forms.** Claude finds by pattern, so the kit fixes the
  headings, the slot row, the marker forms; a renamed heading is a lookup that
  fails silently.
- **One home per fact.** A fact that lives in two files drifts in one of them;
  every other surface points.
- **No maintained views.** A hand-curated cross-reference or connector table — a
  theme-to-documents map, a repo-wide master catalog — is not a kit surface: it
  restates facts that live in homes of their own, costs too much to maintain
  well, goes stale silently, and is cheaper replaced by a lookup at the moment of
  need over the `About` cells and the maps. The test: delete it — if it can be
  rebuilt from what remains, it was a view. A record whose facts live nowhere
  else is not a view and this rule does not reach it.

Two readers are designed for: the strong model in session (pointers, judgment)
and the executor subagent in a propagation wave, which follows the letter (fixed
headings, slot markers, manifest tags; nothing left to inference). The
principle governs every kit change in
your canonical skills repo, if you keep one (each judged by who reads it, at
what moment, at what cost;
`skill_authoring_skill.md` Part 1 points here).

## Conformance: one home per job

A repo **conforms** to the kit when every job the kit assigns a home has
**exactly one home, at the kit's path**. Conformance is defined by job, not by
path: every kit-shaped home carries a one-line job statement (in the birth
tree and the spec), and a folder elsewhere in the repo doing that job is a
**same-job candidate**, whether or not the kit's folder also exists. Existence
alone is never a pass: the empty kit folder beside a full predecessor is the
failure this definition exists to name (the installer premise, retired at v6.4;
a repo's root `admin/` beside the empty `workdesk/admin/` is an
example). A repo conforms at **every propagation**; the pass is Part
C's conformance pass in `PROJECT_SETUP.md`, the audit is `repo_audit_skill.md`
Check 12, and the one-time backlog of migrations is a dedicated campaign.

**Kit-owned form, project-owned content.** For every kit-shaped file the
template owns the *shape* (headings, order, the kit blocks, the fixed lines, the
trailer form) and the repo owns the *content* poured into the shape's project
slots. The pass rebuilds the file from the template in template order and pours
the project's content into its slots; content that fits no slot is an **ask at
the pass**, never a silent landing and never dropped. Nothing about a file's
form is the repo's to keep: form is regenerated at every stop so template
improvements reach every repo.

**Slots and markers, one notation.** Where the template fixes the headings
(`CLAUDE.md`, `STATUS.md`, `ONBOARDING.md`), the **sections are the slots**: no
marker, the heading is the name. Where project text sits inside kit form with
no heading of its own (a standing document, a `FOLDER_MAP.md`, `README.md`),
HTML comment pairs mark it, invisible when rendered and grep-able by an
executor:

- `<!-- slot: <name> -->` … `<!-- /slot -->` around project text the pass keeps.
  A table inside a slot (a catalog, a queue, an index) has its **header row
  regenerated as kit form** and its rows kept: a marker between header and rows
  would end the table wherever it is rendered, so the slot wraps the whole table
  and the pass rewrites the first two lines.
- `<!-- kit: <name> -->` … `<!-- /kit -->` around a kit block the pass
  regenerates wholesale (the root map's skeleton, a line map's latent homes).
- `<!-- slot: unplaced -->` … `<!-- /slot -->`, the one catch-all, present in
  every marked file, empty in the normal state; anything in it is reported at
  every stop until placed.

A marker deleted by a session is a finding (kit block missing or stale), and the
pass re-inserts it. Slot and block names are fixed per template; the template
is the list.

**The manifest: the tagged birth tree.** The `research_setup_scaffold.md` tree,
reconciled with the spec, is the **one structural
manifest** with three readers: Part A builds from it, the pass creates from it,
the audit compares against it. Every tree line carries one tag at the head of
its comment column:

| Tag | Kind | What the pass does | What the audit does |
|---|---|---|---|
| `[U]` | Unconditional: created up front | creates it if absent, with its stub; same-job check | absent = drift; existence alone never a pass |
| `[P]` | With parent: created with the folder it belongs to, unconditional one level down (`deliverables/` with every line; a line's `FOLDER_MAP.md`) | creates it with the parent | absent under a present parent = drift |
| `[E: <condition>]` | Event-born: the condition is written on the line | tests a mechanical condition and proposes creation plus the same-job check; a content-judgment condition goes to the approval list | presence before the condition is never drift; absence after it is a finding |
| `[J: <skill>]` | Judgment-born: a Claude-prompted, user-ruled event; the prompting skill is named | never creates it | never flags its absence |

Skill artifacts (a `_LEDGER`, a `_PLAN`, the carryover) are not structure and
not in the tree; their shape belongs to the owning skill. The legend lives
here once; the scaffold points at it in one line.

**Latent homes.** A born-on-demand home (`[E]`, `[J]`) is declared before it
exists: its parent's `FOLDER_MAP.md` carries a **latent homes** block (a `kit`
block, one line per latent child: path, condition, and, when a New homes line
named candidate material in this repo, the candidate awaiting ruling). The
block is what makes "the structure exists" true without an empty folder for
every possibility: the structure is
always created, because not knowing the structure exists is the other failure
mode.

**Propagation is a migration: the New homes line.** Every kit CHANGELOG entry
that adds or moves a home closes with a **New homes:** line (path, job,
predecessor names, seeded from where the source repo kept the material before
the lift), the sister of the Retired premises line. The pass reads the lines for
every version the repo crosses and runs the **same-job check** on those homes:
predecessor names, map descriptions, characteristic contents. Every candidate
goes on the approval list; nothing is moved or deleted on Claude's call, and a
candidate never blocks the creation of the empty home. After that one-time
backlog the pass looks only at what is new since the repo's last stop. The
pass is recorded per repo in the wave ledger (created, migrated, ruled
different-job, extras reported).

## The universal layer

### Root files (every repo)

- **`CLAUDE.md`** — the front door: routing + the skills table. Its Repository
  Structure section is a **pointer** to the root map (below), never a second
  copy of the tree. One trailer line at the top (kit version, date); the
  propagation record is the repo's `<KIT_FOLDER>/CHANGELOG.md` entry.
- **`STATUS.md`** — Claude's resume file, read on the user's "yes": what is
  open and nothing finished — one entry per workstream (where it stands as
  of a date, Next, Waits on, Resume), rewritten in place at every close; the
  open questions; the live known issues; the kit's cluster block. Header:
  date and flag only, rewritten in place, no stack (the propagation's record
  is the repo CHANGELOG entry and the block's Last curated line).
  `project_tracker_skill.md` owns it.
- **`RECORD.md`** — where the project stands at the big-picture level: everything
  currently true of it, by part of the project, one row per big thing, tagged by
  status, rewritten in place at session close; read by the user as well as Claude.
  Born at the first row, not up front; registered in the root-file enumerations
  when born. `project_tracker_skill.md` owns it ("The record").
- **`STATUS_ARCHIVE.md`** — closed records rotated out of `STATUS.md` at
  session close. Born at the first rotation, not up front; registered in the
  root-file enumerations when born. `project_tracker_skill.md` owns the split
  (rotation rule, cite-by-name pointers, tripwire). Header and trailer stacks
  rotate here too, verbatim.
- **The root `FOLDER_MAP.md`** (every repo, NONE included) — the home of the
  kit-owned structural blocks and the **root-document register**: the
  **skeleton** block (one line per root folder with its job: the archetype's
  fixed skeleton, or a NONE repo's bespoke one), the **root documents** block
  (the typed index set, `references.bib`, the born-on-use files
  when born), the **latent homes** block, and the **extras** register (the
  governance rules, below). Every root folder is in the skeleton block, is a
  registered extra, or gets a reading at the pass; every root file is in the
  root-documents block, each index with what it registers, or gets the function
  check. Form per the `FOLDER_MAP` convention below and `FOLDER_MAP_template.md`
  (`Kind: root`; the blocks are `kit` blocks regenerated at every stop; no
  catalog slot, the blocks being the catalog).
- **`README.md`** (every repo) — the one file whose reader is not Claude: GitHub
  renders it for whoever has access (on a private repo, the owner and the rostered
  collaborators), read on opening the repo to understand what it is for.
  Cut from `README_template.md` in
  the human register to that one job: the repo's name, the what-this-repo-is-for
  paragraph (the project slot; the twin of `CLAUDE.md`'s Project Overview in a
  person's words, not a copy of it), and one kit sentence saying the repo is
  worked with Claude and pointing at `CLAUDE.md`, plus the `unplaced` slot and
  the form comment every marked file carries. Nothing else: no pointers to
  `STATUS.md` or the maps (Claude's files; a person asks), no roster (`CLAUDE.md`
  Collaborators; the person's `ONBOARDING.md`), no date or version line. **No
  structure copy**: the root map holds the tree; a README carrying a folder tree
  or table is drift, and the other retired forms are named with their homes in
  `PROJECT_SETUP.md` Step 7.5 part 2.
- **`.gitignore`** (every repo) — project-owned, with one kit-owned block
  (package binaries and zips under `workspace/packages/`, `__pycache__/`, OS
  files), seeded from the kit's `gitignore_seed.md` and regenerated at every stop;
  the repo's own rules stay outside the block.
- **Archetype declaration** (in `CLAUDE.md`): the repo's `type` (research /
  NONE), `variant` (single-paper / agenda for research) — so
  checks and routing read the declared type rather than
  re-diagnosing it. A NONE repo declares `type = NONE` (it keeps no archetype spec).
- **Loose files at root** are accidental staging (below): a task artifact at
  root (a restructure record, a plan file) is deleted at the task's close, and
  the pass proposes the deletion; a legacy file from before the structure is
  migrated into it, asked per file.

### `workspace/` (every repo)

The machinery layer — Claude's working surfaces: saved conversations, session
handoffs, the **`multisession_active_tasks/`** carryover home (see below), the
**`staging/`** intake funnel (see below), the **`packages/`** outbound
assembly home (see below), and the exploration-branch
**`branch_logs/`** trail. What lives here waits on Claude machinery or session
mechanics; anything waiting on the user's action or judgment belongs on the
**`workdesk/`** (below). A concrete universal folder present in every repo.
"Workspace" is the name of this *folder* — not a name for the whole universal
layer.

**Subfolders are created up front as labeled-empty homes.** Every `workspace/`
subfolder is scaffolded at repo birth, not created lazily on first use. Each
carries a **standing document** — an `INDEX.md` where an always-active or curated
skill owns the folder, otherwise a `README.md` — created up front with its body
from `standing_documents_template.md`. Since git and the GitHub API track files, not bare directories, this
document is also what persists the home: it stays put across task completion, so
finishing a task empties the *contents*, never the folder. An empty
subfolder reads as *state* — "no saved conversations yet," "no active
multi-session task," "nothing staged" — never as breakage or a missing folder;
its contents are born on use, but the folder is always there to receive them, so
nothing is ever created ad hoc mid-session. This is the universal-layer
application of the *created-up-front vs born-on-creation* rule below.

The **universal** subfolders are present in **every repo, NONE included**:
`claude_conversations/`, `brainstorms/`, `multisession_active_tasks/`,
`staging/`, `packages/`, `branch_logs/` — each owned by a universal convention
or an always-active skill. Subfolders owned by a **curated** skill —
`agent_outputs/` (`agent_research_verification_skill.md`) and `visuals/`
(`visuals_workflow_skill.md`) — exist **wherever the owning skill is active**,
whatever the archetype — if the repo has the skill it has the folder: the
archetype birth tree scaffolds them because the
archetype activates the clusters by default, and a NONE repo gets them the day
the skill is curated in (Part B's bootstrap and Part C's Step 8.5 key on the curated
set; `skills_curation_skill.md` Step 5 names the case). *(Documented predecessor, to v6.5:
"archetype repos only.")*

**The standing document per subfolder.** The function statement: a standing document
exists so Claude can find what
the repo already holds, at the moment the user asks ("do we have a visual we can use," "I
remember a brainstorm about"), without redoing the work or searching blind. So the
kit owns the head (the title in path form, one purpose line naming the owner, the
resting state as a permanent fact) and every table header, and the repo owns the
rows and its notes. Two kinds: a **catalog document**, one row per file or stem
where contents persist and are retrieved by topic, refreshed at the close like a
map's catalog; a **label** where contents are transient or named elsewhere. Where a
skill owns the folder's index, the skill's header is the body and carries the same
markers. The bodies are `standing_documents_template.md`, used by the birth scaffold
in Part A and Part C's Step 8.5 alike and regenerated in form by Step 7.5:

| Folder | Document | Kind | Owner |
|---|---|---|---|
| `claude_conversations/` | `INDEX.md` | the skill's index | `repo_conversations_skill.md` |
| `brainstorms/` | `README.md` | catalog document | `brainstorming_skill.md` |
| `multisession_active_tasks/` | `README.md` | label (a carryover, the unseen-close transcript or a campaign's `CONFORMANCE_ITEMS.md` is named in its STATUS entry) | `multisession_task_skill.md` |
| `staging/` | `README.md` | label (transient by design) | the intake funnel, below |
| `packages/` | `README.md` | catalog document; the catalog is a ledger, rows outlive the folder | the outbound packages home, below |
| `branch_logs/` | `README.md` | catalog document; the catalog is the **branch register**, every content-carrying branch registered at creation | `exploration_branch_skill.md`, `writing_branch_skill.md` |
| `agent_outputs/` | `INDEX.md` + `LESSONS.md` + `WORKFLOW_SKIPS.md` | the skill's triple, all three read at the session start of a dive *(where the skill is active)* | `agent_research_verification_skill.md` |
| `visuals/` | `README.md` | catalog document, the reuse shelf *(where the skill is active)* | `visuals_workflow_skill.md` |

The document is permanent: a task's contents come and go, the standing document
(and so the folder) stays. *(Documented predecessor, v4.1 to v6.4: a titled
one-line label with a live "Empty = ..." claim that the close-out rewrote; the
claim is retired for the resting-state line, and the catalog is the live surface.)*

### `workdesk/` (every repo)

The human-action layer — a top-level folder, sibling of `workspace/`, present
in every repo including NONE. The split criterion is **what an artifact waits
on**: waiting on Claude machinery or session mechanics (carryovers, staging,
branch trails) → `workspace/`; waiting on a human action or judgment — the user
needs to *read, think about, decide on, or do* something — → `workdesk/`. A
deferred action that *Claude* will take is neither: it is work state, and lives
in `STATUS.md` Current state or the task's carryover/plan file.

**The scaffold — always created, birth (Part A) and propagation (Part C) alike:**
- `workdesk/INDEX.md` — the standing document *and* the pending-actions queue
  (below; the body in `standing_documents_template.md`).
- `workdesk/admin/` — administrative and personal deliverables whose nature is
  user-facing (a reference letter, a nomination, travel paperwork): produced
  *for the user to use*, not repo content. `README.md`, a catalog document
  (`standing_documents_template.md`).
- `workdesk/postits/` — the user's **post-it notes**, written for themselves.
  `README.md`, a catalog document. **Boundary — the two kinds of note:**
  a note that is repo *content* — a set the writing-notes skill produces,
  indexed, feeding deliverables — is the other kind and lives in
  `writing_notes/` under `NOTES_INDEX` (below); only the post-it notes live
  here. *(Documented predecessor, to v6.5: `workdesk/notes/`; renamed so the
  two kinds cannot share a name.)*
- `workdesk/collaborators/` — one folder per person with access other than
  the owner, behind a `README.md` label; created up front, the per-person
  folders on join. The convention is its own section below.

Other subfolders on demand via the folder-creation placement check; never
pre-scaffolded.

**The queue — `workdesk/INDEX.md`.** The repo's single list of what is waiting
on the user: a table with the columns Item · Action · Artifact — where · Since ·
Added by · Status, inside the file's `catalog` slot, the header row kit form (the
body is `standing_documents_template.md`; nothing above the table but the title
and one line, the rules staying here and in the tracker):

- **Action** is a closed vocabulary: **read · think · decide · do**. Action
  types are a *column*, never subfolders — types are fluid, and a typed-folder
  scheme would scatter empty folders across every repo.
- **Pointer, not artifact.** Artifacts stay where their owning skills put them;
  a row *points* (Artifact — where). `admin/` and `postits/` hold real files
  because their contents are user-facing by nature — but nothing is ever
  *moved* to the workdesk in order to be queued.
- **Add side:** any session adds a row the moment something starts waiting on
  the user — an output ready for review, a decision surfaced but not taken, a
  document to read. The user adds rows themselves too; *Added by* records which.
- **Close side:** the session close-out reconciles the queue
  (`project_tracker_skill.md`): completed rows are cleared — the durable record
  of what was done lives in the `STATUS.md` close-out, not here — and stale
  rows are surfaced. A *working tracker, not a catalog*. An empty queue means
  "nothing is waiting on the user," not breakage.
- `STATUS.md` and every other lookup surface **point at the queue, never
  duplicate it**.
- The workdesk takes no index row and no required `FOLDER_MAP` — it sits
  outside the content-retrieval architecture; the queue is its orientation
  surface.

**Kit-note boundary.** A reference note whose audience is future *Claude
sessions* (e.g. a format-workaround note shipped with the kit) is skills-side
material and never lands on the workdesk — the workdesk is for what waits on a
human.

**Feedback received from people is not a workdesk artifact.** The *record* of
feedback lives content-side in `feedback/` (next section); the *wait* — the user
deciding what to do with it — is a queue row here pointing there (Action:
decide), cleared on absorption.

**Documented predecessor.** The workdesk replaces v4's universal
`workspace/to_do/` tracker. What `to_do/` mixed, the
waits-on criterion splits: items waiting on the user became queue rows; deferred
Claude intentions live in `STATUS.md`/carryovers. The inline `(owner: …)`
ownership tags retire with the split — everything in the queue waits on the user
by construction. The tracker's distinctions carry over unchanged: `STATUS.md`
Open questions are *decisions to resolve*; a queue row is an *action for the user
to take*; notes are reading/thinking.

### Collaborators — `workdesk/collaborators/` (every repo)

The workdesk above is written for one person: everything in its queue waits on
the owner, and the rules in every skill assume the owner is the human at the
keyboard. A second person with access to the repo — a **collaborator**, working
with their own Claude — needs a place of their own, and the skills need one
reading rule so they still hold. Both live here.

**The scaffold — always created, birth (Part A) and propagation (Part C) alike:**
`workdesk/collaborators/` with a `README.md` standing doc (a label pointing here
and at the `CLAUDE.md` roster; the body in `standing_documents_template.md`). Created up front in every repo like the other universal homes,
so the invariant holds and no repo improvises on the day a collaborator joins;
empty until then.

**On join — the per-person folder.** When a person other than the owner gets
access, the owner's session creates `workdesk/collaborators/<id>/` (`id` = lowercase
first name), mirroring the owner's own workdesk plus two files:

- `INDEX.md` — the collaborator's queue: a *Working on* block on top, then two
  tables, *Waiting on <name>* and *For the owner*, with the workdesk queue's
  columns (Item / Action / Artifact — where / Since / Added by / Status).
- `ONBOARDING.md` — the document written for the person, cut from
  `ONBOARDING_template.md` (six parts: the header with its Review line, the
  task in one paragraph, how the repo works, the ordered reading list, the
  assignment at join, working with Claude; the third and sixth open with a kit
  block, the same in every repo — the universal protocols a person with write
  access meets, and the list of what their Claude does or asks without being
  told, so nothing it asks comes as a surprise — and close with the repo's own
  slot). Written by the owner's session, once;
  the assignment part is dated at join and never refreshed, since where the
  work stands is the workstream's `STATUS.md` entry. Their Claude presents it
  to the person while the "read `ONBOARDING.md`" row stands in their *Waiting
  on* table (the first session, or until it has been read) and takes from it
  the reading list, the order in which to put the repo in front of them.
- `LOG.md` — the session log and decision ledger (below).
- `admin/` and `postits/` with their `README.md` labels, same boundary as
  the owner's: personal working material, never repo content (a note set their
  Protocol 1 produces is content and lives in `writing_notes/`).

In the same session: the first *Waiting on* row in the new `INDEX.md` — read
`ONBOARDING.md`, action read, *Added by* the owner — which their Claude clears at
the close of the session that presented it; a roster row in `CLAUDE.md`
Collaborators (person, id,
GitHub handle, scope, folder, branch prefix, Merge), the `USER_IDS` parameter
reading off the roster's id column, and the "Whose session is this" working
convention from `CLAUDE_template.md` if the repo's `CLAUDE.md` predates it.
Part C Step 2.7 reconciles GitHub's access list against the roster and the
folders at every propagation, so a person who got access without this recipe
is caught at the next stop.

**Four rules.** Conventions, not permissions — GitHub grants every
collaborator write access, and the rules hold because they are followed.

1. **The folder is the only place a collaborator writes directly on `main`.**
   Everything else — content, code, `STATUS.md` entries, folder maps — goes on
   a `<id>_br_<topic>-<date>` branch (`writing_branch_skill.md`) and reaches
   `main` through a pull request. Only the owner commits to `main` directly.
2. **Read-for-state at session start.** The collaborator's Claude reads
   `CLAUDE.md`, then the folder — `INDEX.md` for what is waiting, and the
   workstream's own entry in `STATUS.md` for where the work stands — and takes
   its state from there; `ONBOARDING.md` it presents to the person while its
   *Waiting on* row stands, and reads for the reading list, not for state. It
   never reads
   the owner's `workdesk/INDEX.md` or `postits/` for state; reading the rest of the
   repo for the task is unrestricted.
3. **Two-way traffic runs through `INDEX.md`.** *Waiting on <name>* holds what
   the collaborator needs to read, think about, decide, answer, or do —
   the owner's sessions add rows ("this is something the collaborator needs
   to see"). *For the owner* holds what the collaborator hands back — questions,
   outputs ready for review, decisions the rules route to the owner. The owner's
   sessions glance at every *For the owner* table at session start and either take the
   rows or queue them in `workdesk/INDEX.md` with *Added by* naming the
   collaborator. Each side reconciles its own half at close
   (`project_tracker_skill.md`). The action vocabulary is the queue's four plus
   **answer**, for a question addressed to a person. Rows are pointers, as
   everywhere.
4. **Every session that ends with a pull request leaves its decisions on
   record.** The `LOG.md` entry (below) is written at every close, and its
   Decisions block is produced by a walk of the conversation for five named
   events, not by the session's judgment of what was worth recording; a close
   that finds none says so in one line. The owner reads the block beside the pull
   request ("Reviewing a collaborator's decisions", below). A decision that is
   not on record cannot be reviewed or taught from, so a missing block means
   the rule was broken, never that the session was quiet.

**The *Working on* block — territory, declared.** Above the two tables, one
line per active piece of work (what, where, branch, since), written by the
collaborator's Claude when the work starts and cleared when its pull request
merges. It answers "what is <name> on right now," and it is the collision guard:
before a bulk move or an edit inside a collaborator's territory, the owner's
session reads the blocks and either stays out or leaves a *Waiting on* row
saying what it will touch and why. A claim, not a lock.

**`LOG.md` — the session log and decision ledger.** At every session close the
collaborator's Claude appends an entry, newest first, directly on `main`. The
Decisions block is found by walking the conversation for **five events**, each
a decision by definition, so the session never judges whether a record is
owed: (1) **the person chose** between options the session laid out, or said
"go with X"; (2) **the session asked, and the answer changed what it did**;
(3) **the session proceeded on a stated assumption** — unsure, said so, and
went on without asking; (4) **something was dropped, deferred or narrowed**,
or routed to the owner through a *For the owner* row; (5) **the instruction admitted
more than one reading and the session took one.** Every hit is one decision.
A rewording, a formatting fix, a file made exactly as asked are not. When the
walk finds nothing, the block is the one line *No decisions: no choice,
question, assumption, deferral or reading this session.*

```markdown
## YYYY-MM-DD — <short title> — branch `<id>_br_<topic>-<date>` — PR #<n> (or: no PR)

**Done.** <What the session did, in plain prose, with the files touched.>

**Decisions.**
- **<Decision, one line.>** Unsure: <what the session did not know or could
  not settle before deciding; "—" for a plain choice>. Asked: "<the instruction,
  verbatim, when the decision was a reading of it; omitted otherwise>". Why:
  <the reason>. Rejected: <what else was considered>. Applied in: `<file>`.
  Review: pending | informed | accepted YYYY-MM-DD | overturned YYYY-MM-DD
  (<what replaces it>).

**Open.** <Questions and next steps; each question is also a *For the owner* row.>
```

The two fields before the reason are what a review reads first. **Unsure**
marks the decisions taken without knowing, the teaching moments. **Asked**
puts the person's own sentence beside what their Claude did with it, so a
result the person did not expect reads back to the instruction that produced
it rather than to a fabrication. The session also says a reading out loud at
the moment it takes it, before continuing (the rule against proceeding on a
silent assumption holds in every session); the block catches what slipped
past that.

The **Review** field makes the log a ledger rather than a diary. How a decision
opens is set by the roster's **Merge** column: `owner` — the owner merges every
pull request after reading it, and decisions open *pending* their *accepted* or
*overturned*; `self` — the collaborator merges their own pull request inside
their territory once the LOG entry is written, and decisions open *informed*
(same four fields, read by the owner, nothing waiting on them); anything that
reaches outside the territory (another line's files, the spine, shared trackers
beyond `STATUS.md`) waits for the owner. Either way the owner can flip a single
decision to *pending*, and the collaborator can mark one *for the owner* (which
also drops a *For the owner* row). A self-merge is still a pull request with a
log entry behind it, never a direct push. Merge is a procedural label — no
collaborator wears a trust word.

**Reviewing a collaborator's decisions — the owner's session.** The record exists
so that the owner can check the work, learn from the misreads themselves, and teach
the person; it serves most where a collaborator's instructions to their Claude
are not yet precise, where they may not notice that a result is not what they
asked for, or call it a hallucination when it was a reading. "Review <name>'s commits" (or "what did <name> decide") runs in
the owner's session, per person: read the `LOG.md` entries since the last one
whose decisions all carry a dated Review, and for each put the pull request's
diff beside the Decisions block. Present the decisions one at a time, the
**Unsure** and **Asked** fields first, then the decision and its reason;
the owner reasons with it and rules. The ruling lands in two places: the
decision's Review field on `main` (*accepted* or *overturned*, dated, with
what replaces it), and one *Waiting on <name>* row in the person's `INDEX.md`,
action read, pointing at the reviewed entry with the note the person should
take from it — their Claude presents the row at their next session start. A
misread that recurs across people or sessions is a kit lesson rather than a
person's mistake and is logged as a `[SKILL-FEEDBACK]` entry in the channel
(below). The conversation the person saved at their close, when there is one,
is the transcript behind the block; the review opens it only when the block
does not answer.

**`STATUS.md` is updated by everyone.** A collaborator's close rewrites one
place — their own workstream's Current-state entry, short and pointing at
the LOG entry — on the branch, so the update reaches `main` with the pull
request; the header line and the review flag stay the owner's. The LOG entry is
the collaborator's session record.

**The reading rule — what "the user" means in a collaborator session.** The
skills say "the user" throughout. In a collaborator's session, a skill's
"the user" reads as **the human present** wherever the rule is about the person
at the keyboard — the session-start ask, the review-and-approve loops, the
close-out rituals, which bind whoever is the human. Where a rule routes a
*decision* to the owner — a merge to `main`, a placement ruling, a change
to a skill, anything a skill marks as the owner's call — the collaborator's Claude
opens a *For the owner* row instead of deciding. The skills that needed a
collaborator branch of their own have one (`project_tracker_skill.md` step 0
and the queue reconciliation; `finish_session_skill.md` Steps 2–5;
`writing_branch_skill.md` naming; `github_api_workflow_skill.md` parallel
people; `repo_conversations_skill.md` user ids); every other skill is covered
by this rule and is not rewritten.

**Boundary.** The folder takes no index row and no `FOLDER_MAP` — it is
workdesk territory. A collaborator's *content* — notes that feed a deliverable,
data, drafts — lives content-side and indexed like anyone's, on the branch.
What the folder holds is the collaborator's queue, orientation, and log,
nothing else. A collaborator never gets an intake drop folder: someone with
repo access places material where it belongs on their branch, indexes it, and
it reaches `main` by pull request. Material from a
team member *without* access is `inputs_from_team/` (below).

**Folders a collaborator creates: the merge-time sweep.** When a collaborator's
pull request creates a folder outside their workdesk territory, the folder is
swept into `workspace/staging/` at the merge and placed by the intake check
— the owner accepts the merge, the new folder moves into staging, and the owner
integrates it. Two halves, by the
roster's Merge column: an `owner`-mode merge sweeps at the merge, in the owner's
session (`project_tracker_skill.md` owns the step); a `self`-mode merge is
caught at the owner's next session start, where the freshness check reads "folders
created by merged collaborator pull requests since my last session" and stages
them (`project_tracker_skill.md`, the freshness check, Pass 1). The sweep
is the capture mechanism for collaborator-created structure; nothing else
detects it.

### `feedback/` (every repo)

The content-side home for **feedback received from people on the repo's
products** — a top-level folder, sibling of `workspace/` and `workdesk/`,
present in every repo including NONE. One subfolder per person; dated entries
inside (loose notes `YYYY-MM-DD_<topic>.md`, or dated series subfolders where a
series has its own convention, e.g. a recurring check-in). **Every entry is a
pair**: the **raw record**, `YYYY-MM-DD_<topic>_RAW.md`,
the feedback as it arrived — the email, the notes taken in the meeting, or the user's
recollection as they told it — filed on arrival and never edited; and the **worked
entry**, `YYYY-MM-DD_<topic>.md`, written in the session where the user gives their
reading of it and rules, carrying what it means for the product and the
disposition. Until that session the entry is raw only, and the catalog says so. A
series subfolder holds the same pair per meeting. The root `feedback/FOLDER_MAP.md`
lists entries chronologically across people, the raw and the worked half in two
columns, so a missing half is visible.

**Created up front, not born on first need — a deliberate ruling,
with the reasoning on record:** an optional convention is not remembered at the
moment feedback arrives, which is exactly how a repo grows two competing
feedback locations; the empty folder with its seeded `FOLDER_MAP.md` is the
reminder surface, and the seeded map also solves git's inability to track an
empty folder.

**The what-goes-where split, stated at the point of use in
`feedback/FOLDER_MAP.md`** (the seed's kit block in `standing_documents_template.md`,
regenerated whole at every stop; the map's form is the FOLDER_MAP convention's)**:**
the **record** lives here, durable; the **wait** is
a `workdesk/INDEX.md` queue row pointing here (Action: decide), cleared on
absorption; the **link**, where a product ledger exists, is the ledger's
`feedback` event pointing here, open until dispositioned
(`product_ledger_skill.md`); the **version**, on the first feedback received on
a document, is the byte-exact copy of what went out, cut into `versions/`
beside the document ("Versions vs. archive", below). Consumers already wired: `product_ledger_skill.md`
(the `feedback` event) and `finish_session_skill.md` Step 4c (the close-out
capture net for feedback mentioned in session but never filed).

**The one other home: feedback on a funding or contracting instrument.** A review of a
funding instrument's abstract or document, or of a ToR, is feedback on the instrument, not on the repo's
products: it lives in the instrument's own folder, `funding/<instrument>/feedback/<person>/`, in
the same pair form and with the same catalog columns, born on the first review
(`[E: the first feedback on the instrument]`), its map born with it; the root
`feedback/FOLDER_MAP.md`'s description points at it, so a session at the root finds it. Two
subjects, two homes: the
funding document's feedback is about the process of getting funded, language compromises are
made along the way, and it may serve the project not at all; its dispositions are edits to the
instrument's documents, and the record moves with the instrument's folder when that folder is
renamed. A module that drafts the instrument files it there. The audit never reads an instrument folder's `feedback/` as a same-job candidate of the
root home.

### `writing_notes/` (every repo)

The content-side home for **indexed notes** — the note sets the writing-notes
skill produces (Protocol 1, `writing_notes_skill.md`) and drafts cite — a
top-level folder, sibling of `workspace/`, `workdesk/` and `feedback/`, present
in every repo including NONE and **created up front**. **The function statement of
record:** every run of the writing-notes skill lands its note here and nowhere
else, and every "check my notes" or topic ask starts at `NOTES_INDEX`; the two
kinds of note are told apart by home and by name — a **post-it note** is the
user's own and lives in `workdesk/postits/`, an **indexed note** is content and
lives here.

- **A set is a file**, `writing_notes/<set>.md`, named for the line of thinking
  it holds (the skill's purpose rule); a **subject subfolder** only when one set
  spans files (a literature set with per-paper notes), born when the set grows,
  its `FOLDER_MAP.md` (kind `leaf`) born with it. The folder itself always
  exists; only a subfolder inside it is born on need.
- **`NOTES_INDEX.md` is the catalog**: one row per set (`Note · About · Where`,
  `typed_index_template.md`), written when the set is started, named in the root
  map's root-documents block. It is the **one universal index**: the research
  archetype carries it in its set, and a NONE repo carries it alone, its only
  typed index (`archetype_conventions.md` stays L2 for every other index).
- **The folder's own `FOLDER_MAP.md`** is born with it like every root folder's
  (kind `leaf`): the description and one pointer row at `NOTES_INDEX`, never a
  re-list (`FOLDER_MAP_template.md`, the catalog's second row rule). It is also
  what keeps the empty folder in git.
- **Whose sets:** the owner's and a collaborator's alike — a note set is content,
  so it lands here whoever wrote it, the writer named in `About`; a
  collaborator's personal notes stay in their own `postits/`.
- **Retrieval:** the lightning check routes a note to `NOTES_INDEX` (the intake
  funnel, below); "check my notes" reads the set and follows it out to the
  sources (`writing_notes_skill.md`); the freshness check tracks the folder
  (`project_tracker_skill.md`).

*(Documented predecessors, to v6.5: research's `general/notes/<subject>/`, the
only declared home; a legacy `workspace/notes/`; a bare root `notes/`.
NONE declared nothing, and the notes skill named no home, so sets landed
wherever a session put them. The migration is Part C Step 8.5: files moved
whole, citations rewritten, a post-it found among them proposed for
`workdesk/postits/` and asked per file.)*

### `quarantine/` (every repo; event-born)

The content-side hold for material the repo keeps but must not use: a source
withdrawn or contested, a file whose provenance or permission is unresolved, a
draft ruled off-limits until a question settles. Top-level, sibling of
`feedback/`; **born on the first held item** (`[E: the first item is held]`),
with its latent-home line in the root map until then. Four rules: no index rows
and never cited; **skipped by the lightning check** and every retrieval surface,
so a held file cannot be found by accident; a `FOLDER_MAP.md` with **one line per
item saying why it is held** and what would release it; **exit through staging**,
so a released item is placed by the full check like anything new.

### Inputs by origin: `inputs/`, `sources/`, `inputs_from_team/`

Three words, three jobs by origin, universal across archetypes and levels (a
line, or the repo root when the repo is the unit):

- **`inputs/`** — what *I* made for this unit: the material the user (or a
  session) produced as input to the work, not the work itself.
- **`sources/`** — what came from outside the repo and the team, mostly outside
  your organization: the external material the unit reads.
- **`inputs_from_team/`** — what a team member working on the project but
  **without repo access** sent, used as an input and never reworked ("someone
  else made this outside the repo and we use it as an input but do not rework
  it"). Takes the `feedback/` shape: one subfolder per person, dated files
  inside; event-born on the first such file (`[E: a colleague without access
  sends a file]`). A collaborator *with* access does not use it (the
  Collaborators section).

Where a repo uses one word for another word's job (an `inputs/` holding
external proposal background, which is `sources/`), the audit lists it as a
finding for the gate; the pass never renames on its own. The words are the
job names the spec uses in its tree; a spec may say which of the three a
unit carries.

### Per-product tracking — the product ledger (born on use)

A **product** — one thing said several ways (outline, markdown, .docx, .pptx,
.tex, translations) — may carry a **`<stem>_LEDGER.md` living with it**, owned
by `product_ledger_skill.md`. The ledger is **born on the first event git
cannot see** (a representation created or changed outside the repo; a
representation sent or presented, with the feedback that comes back; a
product-level decision no file records) — never scaffolded up front.

**The ownership boundary** (in force wherever a ledger exists): the **ledger
owns product facts** — which representation is current, where they diverge,
what has been presented, what was decided; **structure owns existence** — the
folder maps say what files exist and where; **aggregating surfaces**
(the line map's current-shape paragraph, `STATUS.md`) carry **pointer plus one-line
position only**, never a copy — on any disagreement the ledger wins. There is
no folder- or line-level ledger; the ledger is per product.

### The `multisession_active_tasks/` folder (every repo)

`workspace/multisession_active_tasks/` is the home for the **multi-session carryover** — the working doc that carries one task across the several sessions it
takes to finish, when resource limits (context, execution risk, fatigue) force
the split. Like the other `workspace/` homes, it is **created up front and reads as state: an empty
folder means "no active multi-session task."** The carryover doc itself is **born on
use**, when a task crosses the multi-session threshold, and is named
`MULTISESSION_CARRYOVER_<task_stem>.md`. It is **distinct from the workdesk
queue** (`workdesk/INDEX.md`): the queue holds actions waiting on *the user*; the
carryover holds the live Claude-side state of the *task in hand*. It
**takes no index row** (it lives in `workspace/`, outside the retrieval
architecture). The
workflow that decides when a carryover is warranted, maintains it across sessions, and
folds it into `STATUS.md` at completion lives in `multisession_task_skill.md`;
this layer only defines the home. *(The term "plan" is reserved kit-wide for in-the-work approach-planning — the approach that lives inside the work, with `STATUS.md` carrying position; the **carryover** is the distinct artifact that resource limits force into being.)* Two other files
share the home, both event-born and named in a `STATUS.md` entry's Resume field, neither a
carryover: the **unseen-close transcript** until its retake (`project_tracker_skill.md`, the
unseen path), and a campaign's **`CONFORMANCE_ITEMS.md`**, the repo's ruled conformance items,
seeded from the campaign charter before the campaign and deleted in the repo's campaign commit,
named in the `repo` entry (the form is in your canonical kit's maintenance-campaign
workflow, if you keep one; the file's own head says what it is). Universal — every repo carries the folder, NONE
included.

### The intake funnel — `workspace/staging/` (every repo)

Everything new to the repo enters through **`workspace/staging/`** — a file
the user drops in, material imported from another repo, branch content from an
overturning merge. The drop rule is **zero-decision**: nothing about where the
thing will live is decided at drop time. That is what makes the rule survive
being rushed — a rule with an embedded placement decision is the rule not
followed. `workspace/staging/` is the repo's **single transient hold-and-place
area**; every caller follows the same lifecycle — **hold → place into permanent
homes → empty** — so an empty `staging/` is the normal resting state, and a
non-empty one at session close is a legible signal (`project_tracker_skill.md`
prompts on it at close). (If two callers are ever mid-flight at once, sub-batch
by a named subfolder; not worth pre-building until it happens.)

**The full check, at placement time — a lookup, not a decision.** Placement out of staging runs: identify each item by a skim (ask what a thing is only when the skim can't tell) → the **adjacency/duplicate check** — read the item against the current `FOLDER_MAP`s and the repo's typed indexes and ask *do we already have this, or something adjacent to it?* → the **home lookup**: where the repo's structure already declares a home for that kind of item (the archetype spec, a typed index, or a folder map's description), Claude places it there, registers it in the right index/`FOLDER_MAP`, empties staging, and tells the user what landed where in the same message. A question goes to the user only where the lookup does not settle it: a probable duplicate or supersession, or a kind with no declared home, which is the placement proposal (or a workdesk queue row when it can wait). The adjacency step is what intake adds over the folder-creation placement check: that check decides *where a new thing goes*; this one first asks *whether the repo already has it*. A bulk drop batches — one index pass, one report or proposal message, not one exchange per file. *(Documented predecessor, to v6.10: every placement out of staging a proposal for the user's approval.)*

**The rushed path ("stage it and use it now").** Nothing about staging blocks
reading a file, so a staged item can be used immediately — the **lightning
check** (below) still runs first. Placement is deferred, recorded as a **Pending
placement fixes** entry in `STATUS.md` (the `project_tracker_skill.md` slot,
re-surfaced at session start and close until resolved). The rushed use pre-pays
identification: the entry carries what the user said the thing was, plus any
probable-duplicate flag from the lightning check. The non-empty-staging prompt
at close is the backstop if an entry is missed — the files themselves can't go
invisible.

**The lightning check — the always-run tier.** Ten seconds, not ten minutes, and
it runs even rushed: an **identity skim** (title page, headers — not a read)
plus a **typed-index grep** by topic/title against whatever indexes the repo
carries. **Hit** → say so and work from the *processed* form (the summary, the
extraction) — never re-process; the staged copy is flagged probable-duplicate in
its Pending entry and resolved at placement. **Near-hit** (an earlier *version*
is filed) → a supersession, not a duplicate: use the new informed by the
existing summary; placement follows the repo's superseded-but-retained handling.
**Miss** → proceed. No placement, no `FOLDER_MAP` write, no interrogation at
this tier; its findings pre-pay the full check. The check's *triggers* are a
working convention in the repo's `CLAUDE.md` — the file in context at arbitrary
work moments: before using a staged file, before producing anything (a summary,
an extraction, a visual, a section), before asking the user for an input the repo
might already hold, and, subsumed in the full check, at placement. The
**type-routing** is this layer's: *source-material work* → the papers and
materials indexes (`PAPERS_INDEX` for a paper, `MATERIALS_INDEX` for the rest,
`DEEPDIVES_INDEX` where carried; one row in one index, the `About` cells the
scan), point, don't rebuild; *visuals and assets* → `ASSETS_INDEX`,
and a hit or near-hit is always told to the user, since adapt-vs-rebuild is their
call; *written deliverables* → `OUTPUTS_INDEX`, read index → outline → draft;
*a note* → `NOTES_INDEX`, a hit meaning the line of thinking already has a set
in `writing_notes/`, continued there rather than opened again.
Whatever maps and typed indexes the repo carries; prompt, don't perform. *(The
routing moved here from the template's Working Conventions bullet at v6.5;
the bullet keeps the four moments and points.)*

**Two callers own their step-by-steps elsewhere.** The cross-repo import
workflow — the source-clone read into staging, the
keep/drop/what-must-come-too selection — lives in `cross_repo_import_skill.md`;
an import lands **typed and placed, not dumped at root**, through this same
funnel. The exploration-branch overturn route (`exploration_branch_skill.md`)
stages here too. Neither redefines the staging home or the lifecycle.

### The outbound packages home — `workspace/packages/` (every repo)

`workspace/staging/` covers the inbound direction; **`workspace/packages/`**
covers the outbound one: existing repo material assembled into delivery
formats and sent to someone outside the repo. Before this home existed, that
work had no floor rule and landed wherever the session put it. One subfolder
per recipient, named `<recipient>_package/`, holding the delivery-format
files and the zips that ship; the standing `README.md` is a catalog document
whose catalog is a **ledger** (`standing_documents_template.md`). Three rules
make the folder work:

1. **Derivatives only, and disposable; the row stays.** Every file is a
   derivative of material that lives in a line folder or the shared spine; the
   canonical version never moves. A recipient's package folder is deleted once
   the package is sent, and its catalog row stays, dated as sent: the record of
   what went out and when survives the zip. The
   close-out's catalog refresh never removes a sent row.
2. **The build script is the tracked artifact, not the binaries.** A package
   duplicates source files and duplicates them again inside a zip, and git
   history cannot be trimmed afterward without a force-push, which the kit's
   rules forbid. The copied binaries and zips are **gitignored**; the tracked
   set is a committed build script that regenerates the whole package, the
   standing doc, and the package's generated documents.
3. **It pairs with the ledger, and the send is asked.** Sending a package is a
   `sent` event on every product in it, which `product_ledger_skill.md` owns. The
   folder holds the artifact; the ledger records that it went out and what came
   back. Because the send happens outside the repo, the session that assembles a
   package asks whether it goes out that day, and a catalog row still without a
   send date is put to the user at the next session start (`project_tracker_skill.md`,
   step 0), the date written to the row and the ledger on their word.

Packages have **one home**. A package that draws on a single line still lives
here, never in the line's `deliverables/` — two legitimate homes for the same
kind of object would make every placement a judgment call. Like every
`workspace/` subfolder, `packages/` is created up front as a labeled-empty
home; empty reads as "no outbound package assembled," the normal resting
state.

### The `FOLDER_MAP` convention — the distributed, anti-sponge index

**Everything in a repo is locatable through its maps and indexes, without
scanning the tree** — the no-scan guarantee this convention implements. (Which
*key* you look up by is a layer-2 question; see `archetype_conventions.md`.)

A folder carries a **`FOLDER_MAP.md`** doing two jobs in one file:
- **Description** (rides on top) — what the folder is for, and briefly what's in it.
- **Map / index** (the architectural role) — the catalog of the folder's own contents, read to *locate* without scanning. Weight scales with the folder's role: a leaf folder's map is a short list; a category folder's rosters the whole category (e.g. the sub-units it holds) — same artifact, more catalog when the folder holds more.

**Which folders (the leaf rule).** Every content folder carries a map but one: **a
leaf born on content.** The test is the folder's state, never its name: **does it hold
tracked files that a typed index or the parent map already enumerates fully?** Yes: no
map (a `summaries/` subfolder created by its first file and listed by its parent). No,
because it is empty: **a map, whatever its name or depth** (`[U]`, `[P]`, an `[E]` the
stage offers at birth: `draft/`, `deliverables/`, `background/`), the `leaf` kind of `FOLDER_MAP_template.md`, one
pointer row at the index that rosters it or at the parent map, as `writing_notes/`
has carried since v6.5: the map is the label, and it is what persists the home,
since git tracks files and not bare directories. One folder name can fall on either side
(a papers folder holding the files its index lists carries none; the same folder empty
carries one), so the kit keeps no list of exempt names. Every unit in the manifest (a line,
a root folder) always carries one. **A map is born with its folder**:
whoever creates a folder that carries a map — the
scaffold, the pass, a promotion, the placement check mid-session, the merge
sweep — writes the map at creation, in the form and empty, so it is there to
fill when the folder fills; a content folder without its map is drift
(`repo_audit_skill.md` Check 14), the leaf rule the only exemption.

**The form (fixed by Claude's reading cost;
the drawn form per kind is `FOLDER_MAP_template.md`, the fill rules
`PROJECT_SETUP.md` Step 7.5 part 2).**

1. Title line: `# FOLDER_MAP — <path from root>` (`root` for the root map).
2. The **slot row**, one bare line, kit-owned: `Kind: <word>`, the folder's
   kind from the template's closed list (root · line · category · leaf ·
   module home · orientation), and for a research line the
   stage — `Kind: line · Stage: <word>`, the one home of the stage. Nothing
   else rides on it: the variant has its home in
   `CLAUDE.md`'s frontmatter. It replaces the `**Type:** · **Stage:**` header
   line of earlier kit versions (a documented predecessor the floor never
   defined).
3. The **kit blocks** the folder's kind carries, each a `kit` block regenerated
   whole at every stop, a list with a fixed empty line: the root map's
   skeleton, root documents, latent homes and extras register; a line map's
   latent homes. Content inside the blocks
   is the repo's (which extras); the form is the kit's.
4. The project's **description** (`slot: description`: what is here, what goes
   here; never a restatement of the spec) and **catalog** (`slot: catalog`),
   one table under one kit header for every kind, `| Path | What is here |`,
   rows the repo's: present contents only (a moved entry's row moves with it),
   one pointer row for a subfolder a typed index registers, no counts and no
   dates in a row. The root map carries no catalog slot: its blocks are its
   catalog.
5. One dated trailer line, `*Last updated: YYYY-MM-DD — <what changed>*`,
   rewritten in place by the close-out. **No stack**: an existing stack is
   deleted at the pass, its history being git's.

`FOLDER_MAP.md` is the **authoritative, distributed index for its folder** — the
description orients; the map is why the file exists in the retrieval
architecture. Because every folder self-describes and self-maps, there is no
leftover that needs a central catch-all — which is the mechanism that prevents a
single root index from becoming a sponge that absorbs everything structureless
and never stabilizes. The root indexes register by kind, one row in one index
(`typed_index_template.md`); a folder's map points at the index for what it
registers and never re-lists it, and no root lookup is a second copy of a
folder's map.

**A folder-level domain registry is domain machinery.** A catalog a folder keeps of its own domain, in a shape the kit does not define, has no kit form: its shape is the repo's, preserved verbatim through any restructure or pass, and the one requirement is that the folder's map registers it with a catalog row. The kit promotes a form only on a second instance.

> **Name note.** `FOLDER_MAP` was chosen over `FOLDER_INDEX` so the name carries
> both roles — orient *and* locate — in one word. The cost: it sits just outside
> the repo-level `*_INDEX` family (`MATERIALS_INDEX`, `PAPERS_INDEX`). The typed
> archetype indexes a category folder may also carry are defined in the repo's
> archetype spec.

**Machinery and desk folders are outside this architecture.** `skills/`,
`workspace/`, and `workdesk/` take no index rows and carry no `FOLDER_MAP`
below their roots — their standing documents (`standing_documents_template.md`)
are their own lookup surfaces, a catalog document refreshed at the close like a
map's catalog, and nothing in the retrieval tree points into them; a map found
inside them (a package folder's, a subfolder's) is deleted at the pass, its one
repo fact moved to the standing document's row. An **orientation-only
`FOLDER_MAP.md`** — `Kind: orientation`, the description slot alone, no catalog
and no close-out refresh obligation (the template's last form) — is allowed at
those three roots where its description says something of this repo's that the
floor and the standing documents do not; one that restates them is deleted at
the pass and reported. *(Documented predecessor: the bare "map-exempt"
parentheticals through v4.2, which read as a ban and left a repo that grew an
orienting map in `workspace/` with no in-convention way to keep it; and the
v6.4 "orientation only — not an index" heading, replaced by the kind word.)*

### End-of-session status refresh

The main-category `FOLDER_MAP.md`s get their **status refreshed at session
close** — and so do the catalog documents among the standing documents of
`workspace/` and `workdesk/` (`standing_documents_template.md`), whenever a
session's commits put a file into a folder or remove one. This is a requirement
the universal layer generates; `project_tracker_skill.md`'s close-out implements
it (the catalog refresh, every repo), reached by `finish_session_skill.md` Step 3,
which invokes that close-out in full. The close-out **refreshes the catalog of
every folder the session touched** (rows added and removed; a `packages/` row
dated sent, never removed) and rewrites that document's one trailer line; the
audit fixes maps and standing documents (Check 3 findings are drift fixes applied
in repair mode) and the close keeps them current between audits. *(Documented
predecessor, v6.3 to v6.5: the navigation-label refresh, which rewrote a live
"Empty = ..." claim in the standing `README.md` and the parent map row; the claim
is retired for the resting-state line, and a map row's label is refreshed as any
catalog row is.)*

### Governance rules (in force in every repo)

- **Root = the skeleton plus at most two registered extras.** An extra is a
  root folder for a genuinely repo-particular need, beyond the repo's standing
  set of root purpose-folders, **registered by job** in the root map's extras
  block. The count is mechanical; the cap reports and never blocks.
- **Every unregistered root folder gets one of four readings** at the pass and
  the audit, the reading a judgment for the gate, nothing moved on Claude's
  call: (1) **same job as a kit home** (a same-job candidate: migrate); (2)
  **unplaced material** (to staging, placed by the intake check); (3) **a unit
  missing its skeleton** (a folder that became a line:
  promotion scaffolds the unit, `archetype_conventions.md`); (4) **a genuine
  extra**, registered.
- **Flexibility inside folders, never at the root.** Folder *contents* can be
  arranged with some freedom; the set of root folders stays standard. (Applies to
  every repo, NONE included.)
- **A NONE repo declares its skeleton once.** The universal homes exist as in
  every repo; the bespoke skeleton is written in the root map's skeleton block
  (one line per root folder with its job), proposed at birth from the user's
  answers and confirmed (`new_repo_setup.md`, Step 3), or, in a repo that
  predates the declaration, drafted from the root folders and their maps on
  the first pass for approval; the audit reads the root against
  it and runs no archetype check and no typed-index check beyond
  `NOTES_INDEX`, the one universal index (`writing_notes/`, above). Contents
  are the repo's business. **Its manifest is the universal manifest:** the
  lines of `research_setup_scaffold.md` for the universal homes
  — the root documents, `workspace/` with its six universal subfolders,
  `workdesk/`, `feedback/`, `writing_notes/` with `NOTES_INDEX.md`, `skills/`,
  the `[E]` lines (`RECORD.md`, `quarantine/`, `inputs_from_team/`) — read with their tags by the pass and the audit, so no
  `[U]`, `[P]` or `[E]` call is inferred from prose; the two curated
  `workspace/` homes (`agent_outputs/`, `visuals/`) are latent in a NONE repo
  with the condition *the owning skill is curated in*, and the root map's
  `latent_homes` block lists the `[E]` lines the same way an archetype map does
  (`FOLDER_MAP_template.md`).

*(The rule that an archetype **fixes** the standing root skeleton lives in
`archetype_conventions.md` — it is the one governance rule a NONE repo lacks, so
it is archetype-common, not universal. The clauses above bound root folders
for **every** repo: for an archetype repo, beyond the fixed skeleton; for a NONE
repo, beyond its declared bespoke one.)*

### The `_ex` exception slots

A **bounded gap-slot** for something the standing folder set has no home for: **at
most two per level**, named for what they are with an `_ex` suffix (`<name>_ex1`,
lowercase). A lingering `_ex` is a standing question; **reaching for a third
(`_ex3`) means a folder is missing** — a signal the structure has a gap (you can
override to keep moving, but the flag persists). What counts as the *standing set*
a gap is measured against is the repo's own: for an archetype repo, its type's
skeleton (the spec); for a NONE repo, its bespoke one. **Every slot is reported
at every propagation** with a proposed resolution (a kit home it maps to, a
registered extra, or a kit change) until the user resolves it, and the audit lists
every `_ex` folder as a requires-decision finding, always. A
third slot at one level is a **kit finding**: a New homes line in the next
version. The slot stays because it is the honest label for "this does not fit
and I flagged it".

## Recursion: the sub-unit case

A repo that holds sub-units (mini-projects, or any category of repeated units)
holds them under **one root purpose-folder** — so the root stays
purpose-organized and the two-extra cap holds no matter how many sub-units there
are (the multiplicity lives *inside* the folder, where flexibility belongs).

This makes the universal conventions **recurse one level.** Each sub-unit inside
that folder is its own structural unit: its own description + map in its own
`FOLDER_MAP.md`, refreshed at session end, exactly like the repo root. The
category folder's own `FOLDER_MAP.md` is a **thin roster** pointing at the
sub-units, never a copy — the anti-sponge rule holding one level down.

So the universal-layer rules are written as applying **at each structural
level**, not only at repo root. How a category of repeated sub-units is shaped
for a given repo type (a shared spine plus N units) is defined in that type's
archetype spec.

## Created up front vs born on creation

Two layers, to settle what gets scaffolded:
- **Known structure is created up front and self-documents.** Indexes, the
  standard folders a repo type always has, and every `FOLDER_MAP` exist from the
  start — *even when empty* — and each documents what belongs in it. An
  empty-but-documented folder is a labeled home, not clutter; it is what lets a
  new file route itself to the right place.
- **Unknowable-yet structure is born on creation/expansion.** Anything that
  depends on information you don't have yet (how a repo expands, which
  deliverable types appear) is *not* pre-scaffolded; it's created when that
  information arrives. Don't pre-create empty folders for things that may never
  exist. The structure still *exists* before the folder does: the parent map's
  latent-homes block names it.

The second layer has **four kinds**, the manifest tags (the conformance section
above): **with parent** (`[P]`; `deliverables/` with every line, a unit's
`FOLDER_MAP.md`) is unconditional one level down;
**event-born** (`[E]`) has its condition written on the tree line (`context/`
when line-specific setting material appears; `funding/` when a funding or
contracting instrument exists, a grant, a commissioned study or a ToR; `correspondence/` when a line is
submitted to a journal, the research `under_review` stage; `versions/` at the first
feedback; a collaborator folder on join; `inputs_from_team/` when a colleague
without access sends a file; `quarantine/` on the first held item);
**judgment-born** (`[J]`; `archive/`, prompted by the writing
skill when a document's message, results or structure have changed enough to
be a new draft) is created only on the user's ruling; **skill artifacts** are not
structure. Two rules hold for every kind: **presence before the condition is
never drift** (a folder created early is state, not a finding), and a
content-judgment condition is an ask at the pass, never a test Claude runs
alone.

## The root inbox — accidental staging

Loose content at the repo root is **accidental staging**: it means "needs
placing" (a signal, like `_ex3`), exactly as if it had been dropped in
`workspace/staging/`, and it is swept into the same intake check — not handled
by a separate protocol. **Root should normally be empty of loose content** —
accumulation there is itself a flag. When unsure where something goes, drop it
in `workspace/staging/` (or at root — the funnel treats the two the same) and
the placement check files it from the documented indexes and `FOLDER_MAP`s.

**Root documents are registered, not loose.** The root map's root-documents
block is the register of what legitimately sits at root as a file: the
typed index set (an archetype repo the full set its spec defines; every repo
`NOTES_INDEX`, a NONE repo's only one; each in the form of
`typed_index_template.md`),
`references.bib`, the born-on-use files once born
(`STATUS_ARCHIVE.md`, `RECORD.md`). Any other root document predates the
index system or is a task artifact: the pass runs a **function check** on each
(is everything this file does already done inside the system? if yes, dissolve
it, asked; if not, ask what to do with it in this repo), proposes deletion of a
closed task's artifacts, and migrates legacy files into the structure, asked per
file. A domain catalog stays only when it passes the function check.

## Reference by index entry or stable key, not hard path

Inside documents, reference other things **by index entry or stable key, not by
hard file path**, so moving or renaming a file doesn't stale the reference.
Hard-coded paths in prose are a form of path dependency; they break silently on
the next reorganization. **A processed file's own header lines name a path by design**
(`**Source:**`, `**Source file:**` in a `TEXT_`, `SUMMARY_` or `NOTES_` file): whoever
moves the files repoints those lines in the same commit.

## Reading order — shallow to deep

Where a thing is kept in **layered forms** (a short pointer, a fuller middle
form, the heavy original), an index entry lists them **shallow-to-deep**, and a
reader **stops at the shallowest layer that answers**, opening the heavy form only
when needed. This is a universal reading-cost discipline; the *specific* layered
encodings a repo type uses (a paper's `summary · text · pdf`) are defined in
the repo's archetype spec.

## Nothing is destroyed on a state change

When a repo's recorded state changes — a claim is overturned, an option is
dropped, a stage is relabeled, a structure is superseded — the prior state is
**retained as rationale or history, never deleted.** A state change *re-files*
the past (marks it superseded, points at what replaced it and why); deleting it
would erase the reasoning the next decision needs. The rule is universal; each
layer realizes it in its own form: research keeps both forms and its stage
history (research spec §12), and the exploration-branch overturn route below
stages and supersedes rather than overwriting `main`.

## Versions vs. archive

Two instruments, often conflated. **A version** is a byte-exact copy of a
document as it went to a reviewer, kept beside the live document in a
`versions/` folder (`<document folder>/versions/`; universal — every archetype
and NONE). The folder and its first version are cut **at the first feedback
received on the document**, any document, any archetype, at the moment the
feedback is filed in `feedback/` and, where a ledger
exists, its `feedback` event is logged, so the comments can always be read
against the exact text they answer; later sends add a version each. *(The v6.3
gate, "only when the feedback is ruled substantial", is retired: it asked for a
judgment at the one moment nobody makes one.)* Filename
`<name>_YYYY_MM_DD_<reviewer>.<ext>`, the date the document went out. One row
per version in `versions/FOLDER_MAP.md`: date sent, reviewer, the `feedback/`
entry, the ledger event. A version is never edited, and the live document stays
where it was. **Archive** is for work that became too different to be a version
of the live document: a superseded prospectus, an abandoned lineage, a draft
replaced rather than revised.
Archive keeps its shape per archetype under the rule above (research: the
line-level `archive/`). The cut is prompted at the
feedback intake, not remembered by the writer — the same reasoning that made
`feedback/` a scaffolded folder. Archive itself is **judgment-born**: when a
new version's changes are substantial (the message changes, the results
switch, the structure has changed by more than half), the writing skill
proposes a new draft; on the user's ruling what was there goes to archive and
the document restarts under the new definition. The pass never creates
`archive/` and the audit never flags its absence.

## Skills layout

**`skills/` is the kit's folder, and it is flat:** the kit's files loose in it, the
`last_skill_update/` snapshot the one folder inside. A single-task skill lives
**folder-local, next to the work it serves** (the root `{task}_skill/`, the form
for a repo whose whole work is that one task), rostered in `CLAUDE.md` — not hoisted into `skills/`.
(`skills/` itself stays machinery outside the retrieval architecture — no required
map, per the `FOLDER_MAP` section; `CLAUDE.md`'s table is the roster.) *(Predecessor,
to v6.8: a split layout, the kit in `skills/general_skills/` beside a repo-specific
subfolder; retired at v6.9 because v6.8 moved every repo-only skill out of `skills/`,
which left the split nothing to separate. A repo still split flattens at its next
propagation: `general_skills/` into `skills/`, `KIT_FOLDER` and every skills path in
`CLAUDE.md` with it.)* The one
repo file that sits in it is a **kit candidate in waiting**: a skill the repo wrote there
that the consolidation ruled "kit, eventually", left
in place with its condition registered kit-side and rostered under Project skills until it
joins the kit. A skill ruled repo-only is moved next to the work it serves at that ruling and
never sits in `skills/` again; a whole-repo skill with no one work folder lives in the folder
whose subject it defines. *(Predecessor: the template's "under `skills/` (a single file)",
retired at v6.8 — repo files were re-ruled at every sweep because the folder
could not tell a candidate from a repo-only skill.)* The archetype spec may refine
folder-skill placement for its type. A folder-skill that more than one repo
needs is a **module** (next section): still folder-local, never in `skills/`,
but with a canonical copy in the kit.

**A folder-skill is born in the module's content layout**: the skill file(s) at the folder's root, `references/`
beside them, and its `corpus/` **inside the skill folder** — never a root `corpus/`. A
single-file skill whose corpus takes its first file becomes a folder-skill that day, and
until then there is no corpus folder (v6.9; the predecessor, a root `corpus/` beside a
single-file skill in a single-task repo) — so a promotion to the module tier is a lift of one
folder into `modules/` in your canonical skills repo, organized the way every module already is. The module's
machinery (`MODULE.md`, `parameters.md`, `corpus_inbox/`, the baseline) arrives at
promotion, never before (Check 8 would flag an undeclared card).

**A skill's home holds the skill, never what the skill produced.** A root folder is for something the project makes; a thing a skill creates lives
in the project's own folder beside the skill's home — a module's shape, the skill
in `funding/<module>/` and the product in `funding/<instrument>/` — never inside the skill
folder. For the module tier: a new module's instances are repo-owned folders beside its
home, named in the card, not an `instances/` inside it.

## Modules (the shared-module tier)

A **module** is a self-contained folder package that a repo carries because it
has the matching workstream, not because it was curated. It is the third tier on
the propagation axis:

| Tier | What travels | Where it lives in a repo | Who decides |
|---|---|---|---|
| Kit skill | one file | `skills/` | per-cluster curation at propagation |
| Module | a folder: skill, references, exempt file, header | folder-local, at the home its trigger fixes | the trigger: structural, no question asked |
| Project-specific skill | nothing (never moves) | folder-local | the author |

Two properties define a module, and both must hold:

1. **A structural trigger.** A folder's presence (`funding/`) or
   an archetype type. The trigger fixes the module's home path; the repo never
   chooses where the module lands. A module declares a *list* of trigger-home
   pairs when it can land in more than one place.
2. **Distilled from sources.** A module is a tacit-knowledge skill
   (`skill_authoring_skill.md` Part 2): its corpus is the inputs that made it.
   Kit skills are procedural and carry no such corpus.

A module is the folder-skill above promoted to a canonical copy in the kit: the
archetype layer's lift-on-second-use principle, applied across repos. Canonical
copies live in the kit's `modules/<name>/` folder in your canonical skills repo,
if you keep one; the registry is `modules/MODULES.md` there. This section is floor (L1): a NONE repo can carry a
`funding/` folder, so the rule survives without an archetype.

**Anatomy of a module in a repo.** `<home>/` holds:

- `MODULE.md`: the identity card, in the form of `MODULE_template.md` in your
  canonical skills repo's `modules/` (v6.5): one kit block — name, version with its date, the trigger-home pairs,
  the `this copy` row (the pair in force here, written by propagation from
  detection), nested modules, the exempt files, the entry-point skill, one
  sentence of what the module drafts — regenerated whole at every propagation
  from the canonical copy; and one project slot, the feedback channel, where
  `[SKILL-FEEDBACK]` and `[CORPUS CANDIDATE]` entries land, not in
  `<KIT_FOLDER>/CHANGELOG.md`, swept and cleared once consolidated. Read at the
  trigger phrase (the `CLAUDE.md` module-check bullet), then the skill.
- The skill file(s) and `references/`: everything the skill reads **while
  operating**: section guides, blank templates, the exemplar set.
- The exempt per-repo file(s), typically `parameters.md`.
- `corpus_inbox/`: labeled-empty, created up front. Where a new source example
  lands (below).
- `last_module_update/`: the baseline. Byte-identical copies of every text file
  the module carries, the maps and the exempt file apart; what the sweep
  compares against.
- The maps — the home's `FOLDER_MAP.md` and its subfolders' — are **the repo's,
  never the module's**: born with their folders at
  the land, empty, in `FOLDER_MAP_template.md`'s form, and filled by the pass
  from disk like any folder's map; never in the compared set, never landed at an
  update, never in the baseline. The canonical copy's maps are the canonical
  skills repo's own. *(Before this rule the maps traveled as module files, so every kit update
  re-landed the canonical form and the pass rewrote it to the home.)*

**Not in a repo copy: `corpus/` and `CHANGELOG.md`.** The sources a module was
distilled from live once, kit-side, at `modules/<name>/corpus/` in your canonical
skills repo; the corpus
is kit-resident, always. A repo copy carries only what the skill reads at run
time. The split is decided per file at the module build with one question:
*does the skill read this when operating, or did it read this when it was
written?* A file that is both stays in the corpus and is represented in
`references/` by a trimmed exemplar. The module's history — one entry per
version, the record a consolidation or a redesign session writes — is
`modules/<name>/CHANGELOG.md` there, kit-side beside the corpus; a copy's card
carries the current version only. *(Until v6.5 the history traveled inside
`MODULE.md`'s changelog section, read by no one in a repo; and the floor
offered a `corpus: travels` declaration that nothing implemented.)*

**Declaration.** The repo's `CLAUDE.md` frontmatter carries a `modules:` list
beside the archetype block: name, version, home, per module. It is shared state
read by propagation and the audit, like the archetype declaration, and is
backfilled from detection at first propagation. The declaration *records*
membership; the trigger *decides* it.

**Nesting.** A module may declare another module as nested; the nested module's
home is then relative to the parent's. Versions stay independent: bumping the
parent never bumps the child, and the reverse.

**Exempt files.** Never overwritten by propagation. When an exempt file's schema
grows (a new parameter key), propagation appends the new rows as placeholders
and flags them. The sweep ignores exempt files entirely.

**Placement rules.** Modules never live in `skills/`, so the one-folder
invariant above stands. `CLAUDE.md`'s Skills roster carries a **Modules** block,
one row per module with its home and version; the module set's one home is the
`CLAUDE.md` frontmatter declaration *(until v6.5 `STATUS.md`'s activations block
listed the active modules too)*.

**Lifecycle: made in the kit, used in the repo.** Distilling a module (writing
it from sources, adding a source, re-tuning against the corpus) happens in
your canonical skills repo, if you keep one, where the corpus is. That is the one lifecycle difference from
kit skills, which are born in content repos and swept in. A content repo *uses*
the module and may patch it in place when live work forces it: edit the copy,
bump the patched file's own marker (never the card's version row), log
`[SKILL-FEEDBACK]` in `MODULE.md`'s feedback slot. The next kit update carries the
diff; the revision proper is made in your canonical skills repo, if you keep one,
against the corpus.

**A new source example, found while working in a repo.** Drop it in
`corpus_inbox/` (with its extract, if one was made) and log a
`[CORPUS CANDIDATE]` entry in `MODULE.md`'s feedback slot: what it is, why it is a good or bad
example, which part of the skill it speaks to. If it should shape today's
drafting, also copy it into `references/` as an exemplar; that is a local
modification, swept as a diff like any other. The sweep bundles the inbox;
consolidation files the source in the kit corpus, makes or keeps its extract,
and reads it against the skill: confirm, sharpen, or contradict. Only the last
two bump the module version. Duplicates are detected by **filename and content
hash together**: same name and same hash is one file; same name with a different
hash is a conflict surfaced at consolidation, never auto-resolved; a different
name with the same hash is one document reconciled to one name. The next wave
empties every inbox whose candidates were consolidated. The inbox is transient,
never a second corpus.

**Becoming a module.** A project-local folder-skill that a second repo needs is
announced with a `[MODULE CANDIDATE]` entry in `<KIT_FOLDER>/CHANGELOG.md` pointing
at the folder (the sweep does not walk folders outside `skills/` until the
folder carries a `MODULE.md` — the walk keys on the physical header, never the
declaration, which only Part C writes). Consolidation **opens** the lift: it registers the module as
planned in the module registry (`modules/MODULES.md` in your canonical skills
repo) and queues a build session, which reads
the folder from the repo, sorts its material into corpus (consumed at
authoring) and references (read while operating), and writes `MODULE.md`;
the next wave carries it to every repo with the trigger. (The build is a
redesign session, not a merge: the folder is not in the sweep's bundle, only
its announcement is.)

## The skills CHANGELOG and the `[SKILL-FEEDBACK]` channel

`<KIT_FOLDER>/CHANGELOG.md` is the **kit's version history**, copied into every repo so
it knows which kit version it carries. It is overwritten wholesale on each kit
update — it is **not** the repo's own work log (that is `STATUS.md`; different
layers).

It carries three entry kinds:
- **Versioned kit-change entries** — a `## vX.Y — …` heading, authored centrally
  on the canonical kit side when the kit changes.
- **`[SKILL-FEEDBACK]` entries** — a `## [SKILL-FEEDBACK] — <skill> — <date> — <model>`
  heading, **no version stamp**, logged in a content repo when a kit skill
  misfired or could be better. The tag sits in the leading slot where a version
  would go. The `<model>` slot names the model the session was running (e.g.
  `Fable 5`, `Opus 5`) — model-fit evidence is unreadable without it; entries
  predating the slot stay valid (absence = pre-convention). The channel covers
  **both cases**: *logged-not-fixed* (no file change
  behind the entry — the problem is recorded and left for the kit) and
  *fixed-locally-pending-review* (the repo's live copy of the skill was edited
  and its own version marker bumped, while `skills/last_skill_update/` is
  deliberately left untouched so the next kit update (the discovery sweep, if
  you keep a canonical skills repo) sees the diff). The
  entry says which case it is; without this, a locally fixed skill has no
  in-convention way to explain itself and comes back to the sweep as unexplained
  drift. Whether a local fix propagates is decided at consolidation.
  **Voice-divergence documents ride this channel too:** when the user delivers
  their final version of a deliverable a voice profile was applied to, the
  session builds a divergence document (Claude's styled draft vs. their final,
  the deltas) and logs it as a `[SKILL-FEEDBACK]` entry on the profile — the
  entry carries the distilled deltas and *points* at the divergence doc, which
  stays with the work. (The close-side queue row that sets this up lives in
  `finish_session_skill.md`; a dedicated tag waits on volume.)
- **`[PROJECT-LOCAL SKILL ADDED]` entries** — a `## [PROJECT-LOCAL SKILL ADDED]
  — <file> — <date>` heading, **no version stamp**, logged when a
  generic-candidate skill is authored locally in the repo (per
  `skill_authoring_skill.md` Part 4 Step 7). It marks the new file as a
  deliberate addition rather than ambient drift for the next kit update.

Tagged entries are **evidence, not kit history.** They are swept back at the
next discovery, analyzed centrally on the canonical kit side, and **never merged into
the canonical CHANGELOG.** (For a fixed-locally entry, the edit itself travels as
the sweep's content diff; the entry is its explanation.) They do not survive the
propagation that overwrites them, and need not: an entry is **transport, not a
record** — the sweep has collected it, and its record is kept on the
canonical kit side. A live repo surface
therefore never treats a channel entry as a permanent home; the same-commit rule
below says how a pointer reads once its entry is gone. *(Documented predecessor:
the claim that entries survive because the overwriting propagation
ships the fix — false whenever a propagation clears entries whose findings are
still open, which leaves every "logged as" pointer at them dangling.)* (The sweep, extraction, and routing mechanics live in the canonical kit's
discovery and consolidation workflows, not here; this layer only defines the entry
types and the tags.)

**One channel, many writers — the same-commit rule.** The sweep reads this channel and
nothing else, so a kit observation written anywhere else never arrives. Wherever
a repo surface records something about a kit file, the `[SKILL-FEEDBACK]` entry
is written **in the same commit** and the repo surface points at it (`logged as
[SKILL-FEEDBACK] <date>`) — a pointer that holds while the entry stands; once a
propagation has cleared the channel, the pass rewrites it to the record (`logged as
[SKILL-FEEDBACK] <date>; kit record: <the kit-side record>`), so
no live surface points at an entry that is gone: a `STATUS.md` known issue or open question that
names a kit skill or template (the issue stays in STATUS where the repo needs
the workaround); a `LESSONS.md` entry flagged `Cross-project candidate? Y`
(`agent_research_verification_skill.md`); **any other standing surface with a
row or an entry of its own** — a typed index's head prose, a `workdesk/postits/`
note, a `workdesk/INDEX.md` queue row, a map's description — which points the
same way; a note
in a working file, which has no surface to point from and so is logged at the
close (`finish_session_skill.md` Step 4b, "anything for the kit?"). The conformance pass writes the entry any of
these is missing (`PROJECT_SETUP.md` Step 7.5). *(Documented predecessor, to
v6.5: the channel had only event-shaped writers — a correction restating a
loaded skill, a local fix, a voice divergence — and an observation made in
passing was parked where it was noticed.)*

## Exploration-branch artifacts

An *exploration* — a branch whose purpose is to test whether a `main` claim
holds (a robustness check, an alternative specification; see
`exploration_branch_skill.md`) — carries a small, fixed set of artifacts. They
are **defined here**; the workflow that creates and routes them lives in
`exploration_branch_skill.md`, which never redefines their format. These are
universal (any repo can run an exploration), so they live in this layer.

- **The branch register** — the catalog of `workspace/branch_logs/README.md`
  (`standing_documents_template.md`), **on `main`**: one row per branch that
  carries repo content, exploration or writing, a collaborator's included,
  written **at creation** by the skill that opens the branch (this section's
  exploration; `writing_branch_skill.md` Step 1), annotated at merge or
  abandonment (Status: `merged <date> into <path>`, or the staging pointer plus
  the `STATUS.md` restructure workstream for an overturn; `abandoned <date>`),
  and pointing at the trail file where one exists. Columns: Branch · Opened ·
  What it holds (for an exploration, `testing:` the `main` claim at risk and
  `origin: created | promoted-from <folder>`) · Extends (the subject or parent it
  hangs off) · Status · Trail. It retires "go scan the branches" for every kind
  of branch: the function statement is that a session looked
  for something the repo held and could not find it because it lived on a
  branch. *(Documented predecessor, v4 to v6.5: `BRANCHES_LOG.md`, a repo-root
  log born on the first exploration's registration and covering explorations
  only, writing branches being "findable via git"; born in no repo.)*

- **The in-branch `FOLDER_MAP.md`** — **not a new type.** An exploration folder
  carries the universal `FOLDER_MAP.md` like any folder; it gains three
  description slots: **`Extends:`** (the subject/parent it hangs off),
  **`Testing:`** (the `main` claim at risk), and **`Standing:`** (the distilled
  current answer, updated as the exploration runs and frozen at merge). Because
  it is the universal map, the exploration system stays archetype-blind.

- **`BRANCH_RESEARCH.md`** — the **in-branch log**, inside the branch. A
  two-part file: a **review** on top (what the exploration was opened for, the
  hypothesis, what was done, how it turned out, how it connects to `main`) and
  the chronological **trail** beneath (newest-first session entries). Its header
  names the branch-ref, so provenance is explicit once anything from it reaches
  `main`. **It splits at merge:** the review distils into the merged product
  folder's `FOLDER_MAP` (`Standing` + the branch-origin roster line), and the
  raw trail moves to `workspace/branch_logs/<branch-ref>.md`.

- **`workspace/branch_logs/<branch-ref>.md`** — the raw `BRANCH_RESEARCH` trail
  after merge: history, quarantined out of the retrieval tree but kept on `main`
  so it survives branch deletion. It earns its keep because the "why this spec,
  what was ruled out" reasoning is not recoverable from the frozen `Standing`
  line. The branch's register row names it in its Trail column.

- **`workspace/staging/`** — the repo's transient intra-repo staging area,
  **created up front as a labeled-empty home** and **shared through the universal intake funnel** (above). An overturning merge brings branch content here (read from the
  branch — `git show <branch>:<path>` at Cowork, `gh_read(path, ref=branch)` on
  the web; `github_api_workflow_skill.md`) rather than git-merging to canonical,
  because a git-merge would land both the old and the new claim and report no conflicts while `main`
  is now self-contradictory. Empty between uses — that is its resting state.

- **The per-subject `explorations/` nest** — a merged exploration lands by its
  `extends:` parent into an `explorations/` folder at the subject's home, **born
  on the subject's first merged exploration** (not a repo-wide explorations root,
  which would fight organize-by-subject and spend a root slot).


---
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
