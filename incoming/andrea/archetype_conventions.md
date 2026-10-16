---
name: archetype-conventions
description: >
  The archetype-common layer — conventions shared by every archetype repo
  (this package ships one archetype, research) but NOT carried by a NONE repo. Sits
  between the universal floor (structure_conventions.md, every repo) and the
  per-type spec (research_archetype_spec.md). Holds the rules
  that presuppose an archetype: born-minimal promote-on-evidence, origin-based
  typing, the shared-spine / "one repo or two" test, by-subject keying,
  typed-index behavior, and the archetype-fixed root skeleton. Read after
  structure_conventions.md and before
  the repo's archetype spec. A NONE repo does not carry this file.
triggers: >-
  Structuring, placing or typing files in an archetype repo. Kept in every archetype repo; none
  in NONE
---

# Archetype conventions — the archetype-common layer

This is the **middle of three layers**. It holds what every *archetype* repo
shares but a **NONE repo does not** — the rules that only make sense once a repo
has an archetype at all.

- **Floor (L1) — `structure_conventions.md`.** Archetype-independent; every repo
  keeps it, NONE included.
- **Archetype-common (L2) — this file.** Carried by every archetype repo;
  **a NONE repo does not carry it.**
- **Type-specific (L3) — the archetype spec.** The one
  `<type>_archetype_spec.md` a repo keeps for its declared type. This package
  ships one archetype, research, so the spec is `research_archetype_spec.md`.

Read in that order: `structure_conventions.md` → **this file** →
`research_archetype_spec.md`. The floor names it as a sibling to
`naming_conventions.md`; the spec describes only what is *different* about its
type, leaning on this file for the common rules rather than restating them.
The two stay separate files with one archetype in the package because the rules
here are the ones any archetype shares: an archetype you add later leans on this
file and writes only its own spec.

## How a rule lands in a layer — one test, applied twice

A repo's structure is three layers, and any rule is placed by **one test asked
twice**:

1. **Does it survive without an archetype?** If yes — it holds for a NONE repo
   too — it is **floor (L1)**, in `structure_conventions.md`. If no — it
   presupposes an archetype — it is **not** floor.
2. **Does it have a type-specific form?** The part that does peels to **L3**, in
   the spec. The general principle behind it stays **L2**, here.

The axis is **general-vs-specific, not count.** With one archetype in the
package the count is one, and the placement does not change: research's form is
**a specific realization of a general principle**, and the principle belongs
here while the realization stays in the spec. (This is why a shape such as
born-minimal promotion is stated once here and *realized* in the spec.)

What makes the rules in this file L2 rather than L1 is the same fact each time: a
NONE repo has no archetype-fixed skeleton, no typed buckets or archetype root indexes
(it carries `NOTES_INDEX` alone, the one universal index — `structure_conventions.md`,
"`writing_notes/`"), no archetype-typed units, and no subject key fixed by rule — so
the rules below have **nothing to attach to** in a NONE repo. They begin to apply
the moment a repo has an archetype.

## Born-minimal, promote-on-evidence

Nothing is classified by prediction. Everything **enters at its lowest-commitment
honest reading** and **promotes only on observed evidence** — additively, no
migration, no rebuild. *Not knowing yet* is a first-class, supported state; the
structure never forces a repo to guess what it will become. The drift check (the
periodic revision pass / session-close prompts) **surfaces** promotion
candidates, so a promotion is *noticed*, not predicted.

The principle has **three faces** — the same move at three scales. The *names* of
the units peel to the spec (L3); the move itself is common:

- **Unit count — N = 1 → N > 1.** A repo is born holding one unit and grows to
  many by **adding a unit beside the first**, never by restructuring the first.
  The unit is a research **line** (L3); the N=1 special case (a single paper)
  and its promotion to the N>1 case (an agenda) is the same born-additive shape.
- **Classification — one-off → recognized unit.** A piece of work first read as a
  **one-off** (produced with the general skills only, drawing on the shared
  layer) becomes a **recognized unit with its own dedicated machinery** when
  evidence shows it warrants one. The triage and the marker that distinguishes
  the two are type-specific (L3 — research's: a working folder with a map and
  outputs and no stage word, which has become a line); the
  promote-when-evidence-arrives rule is common.

**Promotion is a structural act.** When a promotion is ruled — a one-off becomes
a unit, a folder becomes a line, a single-unit repo becomes N>1 — the ruling and
the unit's scaffold travel in **one commit**: the folder gets its map with the
slot row, its with-parent children, its index rows, its stage line,
per the archetype's tagged birth tree. Never the ruling now and the structure
later: a promoted folder without its skeleton is drift.
The candidate is surfaced by the promotion-drift prompt at session close
(`project_tracker_skill.md`).
- **Resource — lift on second use.** A resource born at a **narrow scope**
  (one unit's) is **promoted toward the shared layer on its second use** — the
  index surfaces the candidate, the move is confirmed, scope and used-by update.
  The shared home it lifts *to* is type-specific (L3 — research's `general/`);
  the lift-on-second-use rule is common. The
  same move across *repos* is the module tier: a folder-skill a second repo
  needs is lifted to a canonical copy in the kit (`structure_conventions.md`,
  "Modules").

## Origin-based typing

The typing axis is **origin relative to *this* repo**, not authorship. Anything
**produced outside the repo and brought in** is typed normally — paper / material
/ asset, with a scope — **regardless of who authored it** (a colleague's document
and a downloaded one collapse: both are just brought-in material). The **one
special category is what *this* repo produces** — its units' outputs, and any
shared-layer resource it makes for its own future work. A **provenance override**
exists: a document authored in another repo can be marked as *yours* on upload;
ask when it is unclear.

A repo may still **organize** a layer by authorship even though it **types** by
origin (e.g. splitting shared reference into own-institution / external when "what
is our own?" is a live query) — organization by authorship and typing by origin
are both true at once, on different axes. The typed **index set** these buckets
fill is type-specific (L3).

This is L2, not floor: a NONE repo has no typed index buckets to sort intake
into (its one index, `NOTES_INDEX`, registers note sets, not intake), so
origin-typing has nothing to act on there.

## The shared spine, and the "one repo or two" test

An archetype repo holding more than one unit keeps a **shared spine** — the
central layer the units draw on in common — distinct from the per-unit work. What
the spine *contains* is type-specific (L3 — research's `general/` literature).

Before composing several units into **one** repo, apply the **"one repo or
two"** test: is the spine **genuinely co-used** across the units, or are they
**co-located strangers** that merely sit together? If they share no real spine,
they are probably **two repos, not one**. The shared resource is what *earns* the
composition; without it, composing only invents a spine that isn't there. (The
spec states this in its own units' terms — research's agenda-vs-multiproject —
and the test is the same.)

## Retrieval is keyed by subject / topic

In an archetype repo, **you find things by what they are about** — the retrieval
key is the **subject / topic**, not the deliverable type, the producer, or the
location. This is distinct from, and sits on top of, the floor's *no-scan
locatability* (everything reachable through the maps and indexes without scanning
the tree, per `structure_conventions.md`): the floor guarantees you never scan;
this layer fixes the **key you look up by**.

The **form** of the key is type-specific (L3): research's `who_what_year` paper
stem. The choice to key by subject at all is the common rule, and it is the
archetype's acceptance test — *the repo's hardest-to-find thing should be
findable by subject, without remembering where it lives.* It is L2 because a NONE
repo has no typed indexes to key: its contents are reached through its maps, by
whatever key its own work uses.

## Typed-index behavior

An archetype repo carries a set of **typed root indexes** (*which* ones is
type-specific — L3). Their **behavior** is common:

- **Created up front, empty-but-headed.** The full set exists from setup,
  each index created empty in the form of `typed_index_template.md` — the
  three-sentence head naming what is registered, the writer, the sectioning and
  the reading order; the `index` slot with its header row; the `unplaced` slot;
  one trailer line — so an empty index reads as *ready*, not broken (anti-drift —
  the structure never waits for content). The head is the index's whole
  self-documentation; the writer pointer is what "names its feeding process."
- **Found by kind and by subject.** An index is read when the user asks Claude to
  find something ("where is X that is about Y"; "what do we know about Y"): the
  root map's root-documents block routes a kind ask to one index, and a topic
  ask is one scan across every root index, which is why every row carries an
  `About` cell in Claude's words, the state the kind reports, and the pointer
  (the template; the index's function statement).
- **Pointer-only.** A typed index locates content; it never stores it. Rows are
  pointers into the tree.
- **Self-registering at creation.** Placement is known at the moment a file is
  made — the index row is written then, never reconstructed later.
- **Kept current at close; verified on a cadence.** Rows' live-claim fields
  (the state cell of the kind — a reading status, a stage, a reliability
  tag — and the `About` cell) are refreshed at session close for
  the files the session touched — `project_tracker_skill.md` implements; an
  update the user had no time to review carries a trailing `[unreviewed]` marker
  until the next index audit sweeps it — and verified periodically by
  `repo_audit_skill.md`'s index-audit mode. The writer named in the head puts
  a row in; the close and the audit keep it true; together they are the process
  every typed index has behind it, and an index with no process behind it is a
  liability.
- **No central catch-all.** There is no `MASTER_INDEX`: the floor's
  `FOLDER_MAP` tree plus the typed indexes leave nothing for one to absorb
  (the anti-sponge mechanism itself is floor — `structure_conventions.md`).

This is L2, not floor, because a NONE repo carries no archetype root indexes —
its `FOLDER_MAP`s, any lookup of its own and the one universal
`NOTES_INDEX` are its whole index layer.

## The root skeleton is fixed by the archetype

The set of **root purpose-folders is determined by the repo's type**, not
improvised per repo — the archetype lays down a standard skeleton, and every repo
of that type is born with it. This is precisely **the rule a NONE repo lacks**: a
NONE repo has no preset archetype skeleton (it gets a *tailored, bespoke*
skeleton instead — see below), which is why this clause is L2 and not floor.

The floor still governs **how many folders sit at root and where flexibility
lives** (the two-registered-extras cap with its four readings,
flexibility-inside-folders-never-at-root, multiplicity-nests-under-one-root-folder)
— those apply to every repo including NONE, and stay in
`structure_conventions.md`. What an archetype adds on top is the **fixed skeleton
itself**. The specific skeleton per type is L3 (research's prefixed
line-containers + `general/`), and its **manifest is the archetype's tagged birth
tree** (`research_setup_scaffold.md`; the four tags in `structure_conventions.md`,
"Conformance") — the one document Part A builds from, the conformance pass
creates from, and the audit compares against. The skeleton is also written into
the repo's root `FOLDER_MAP.md` skeleton block, one line per root folder with its
job, regenerated at every propagation; a NONE repo writes its bespoke skeleton in
the same block, which is what lets the audit read a NONE root without a spec.

## NONE is a kind, not a deficient archetype

A **NONE** repo is the **general-purpose kind**: any repo that is not a research
repo — a tracker or a lookup, one task done many times, a dated project with its
deliverables, a mix of these. It is **not** an archetype repo missing its spec; it
is a repo whose structure follows its own work, so it gets a **tailored bespoke
skeleton** built for it directly.

A NONE repo therefore carries **the floor only** (`structure_conventions.md` +
`naming_conventions.md`) **plus its bespoke skeleton**, declared once in the root
map's skeleton block — **no spec, and not this file.** The decision rule is
encoded at birth (`new_repo_setup.md`, Step 1): *lines of inquiry that build up
literature and evidence toward papers or analytical outputs* → research; anything
else → NONE. A NONE repo that files papers or materials, or keeps a list of what it
has produced, registers them in a catalog of its own, in the form
`typed_index_template.md` gives ("A repo's own catalog"), named in its root map.


---
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
