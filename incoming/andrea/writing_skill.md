---
name: iterative-writing-workflow
description: "Triage skill for the two-protocol writing workflow: Protocol 1 (reading, thinking, note-taking — fully interactive, lives on main) via writing_notes_skill.md, and Protocol 2 (drafting written content — outline interactively, draft in one pass on a branch, finalize with compiled outline + divergence table) via writing_drafting_skill.md. Use whenever a project involves reading source material and producing written deliverables (policy notes, papers, reports, chapters). Also use when the user asks to set up a writing workflow or organize how to collaborate on a document. This triage skill routes to the right protocol and carries the shared content: how the two protocols interact, and project-setup parameters."
triggers: >-
  Any reading or writing work; read first to triage between the notes protocol and the
  drafting protocol
---

# Iterative Writing Workflow (triage)

This skill is the **triage and shared infrastructure** for the two-protocol writing workflow. It decides whether work-at-hand is thinking work (reading and note-taking — Protocol 1) or writing work (drafting deliverables — Protocol 2), and routes to the appropriate protocol skill.

The protocol-specific workflows live in two sibling skills:

- **`writing_notes_skill.md`** — Protocol 1 for reading, thinking, and note-taking.
- **`writing_drafting_skill.md`** — Protocol 2 for drafting written content.

This skill carries: scope and when-to-use guidance, how the two protocols interact, and the project-setup parameters used by both.

## When to use this skill

Use this skill (and its two protocol skills) whenever a project involves:

- Reading and processing source material (papers, reports, data).
- Taking notes and developing ideas interactively.
- Producing written deliverables (reports, chapters, policy notes, papers, talking points, op-eds).

The two protocols exist because thinking work and writing work have fundamentally different dynamics. Thinking work benefits from tight interactivity. Writing work benefits from larger drafting passes. Each protocol is tuned to its own dynamic.

## Choosing a protocol

| The user is… | Protocol | Skill |
|---|---|---|
| Reading sources, reacting, asking questions, taking notes, developing ideas | **Protocol 1** | `writing_notes_skill.md` |
| Producing a written deliverable (section, chapter, policy note, report) | **Protocol 2** | `writing_drafting_skill.md` |

**The protocols are not sequential phases.** A typical project interleaves them: read sources (Protocol 1) → build an outline (Protocol 2 step 1) → process more sources (Protocol 1) → draft (Protocol 2) → revisit a claim against sources (Protocol 1) → continue drafting (Protocol 2). The user signals which mode they're in. When in doubt, ask.

**Neither protocol — the outside-edit route.** When the user reports a representation of a product created, changed, sent, or presented **outside the repo** ("I edited this outside the repo," "I made this in the design tool," "this came back from Overleaf / from a co-author," "I presented the deck," "she sent me her comments"), or asks **which version of a product is current**, that is not thinking work and not drafting work: route to `product_ledger_skill.md`, which records the events git cannot see. When the artifact is a slide deck authored in a design tool, `design_deck_reconciliation_skill.md` owns the intake and comparison and routes its rulings to the ledger; when it is a paper whose LaTeX source lives in Overleaf or another external editor, `latex_round_trip_skill.md` owns the review copy, the apply register and the refresh, and routes the events to the ledger. If a revision follows, drafting resumes under Protocol 2 as usual.

## How the two protocols interact

In a typical project, the user alternates between protocols:

1. **Protocol 1** — Process source material, take notes, develop ideas.
2. **Protocol 2, step 1** — Use the accumulated understanding to build an overall outline.
3. **Protocol 1** — Continue processing material (may reveal new angles).
4. **Protocol 2, steps 2–7** — Draft drafting units, revising the outline as needed.
5. **Protocol 1** — Go back to sources to check a claim, fill a gap, or process new material.
6. **Protocol 2** — Continue drafting.

**Where work lives.** Branches enter at Protocol 2 step 1 (outline → scale check → branch) and stay open until the document is done, per `writing_branch_skill.md`. **Protocol 1 work lives on `main`** — notes, summaries, indexes are never moved to a branch. Branches are scoped to the active drafting workstream, not to all work happening in parallel. A typical session may write to notes on `main` (Protocol 1) and to a draft on a branch (Protocol 2) in the same session.

**Reading and note-taking are coupled.** For this user, reading is rarely separated from note-taking — even small marginal notes count. Protocol 1 treats reading-with-note-taking as one operation, not two. The protocol's workflow reflects this: present material → user reacts and notes → update notes file → wait. There is no "reading-only" mode separate from "note-taking" mode.

**Reading-with-Claude is conversational.** When working through sources with Claude, the conversation itself does the work that deferred-marker mechanisms (bracketed comments) handle for drafts. Brackets-in-notes is a feature the user considered and rejected: the conversation already handles it. Bracketed comments are a Protocol 2 mechanism (used on branches via `writing_branch_skill.md`), not a Protocol 1 mechanism.

## Setting up for a new project

When adopting this workflow for a new project, document the following in your project's CLAUDE.md (or equivalent coordination file). Both protocols use these parameters.

- **Source material format** — What are the inputs? (PDFs, reports, data, transcripts.)
- **Note sets** — Which sets exist, by name and purpose. Where they live is not a parameter: every set is a file in the kit's `writing_notes/` home, in every repo (`writing_notes_skill.md`, "Where Protocol 1 work lives"). *(Protocol 1.)*
- **Action items** — Never in a notes file: waiting on the user, a `workdesk/INDEX.md` row; Claude's own, the workstream entry's Next field (`structure_conventions.md`). Not a parameter. *(Protocol 1.)*
- **Progress tracker** — For session resumption: where is the file that records what's been covered and what's next? *(Protocol 1.)*
- **Deliverable format** — What's the output? (Word doc, LaTeX, markdown, slides.) *(Protocol 2.)*
- **Deliverable placement** — Outputs are not assumed into a fixed folder. At production, Protocol 2 asks where the deliverable lands and suggests by reading the repo's `FOLDER_MAP`s — never a hardcoded home. *(Protocol 2.)*
- **Style profiles** — Do you have writing style guides? When should they be applied? *(Protocol 2.)*
- **Version control** — How are outlines and drafts saved? (Git, file system, cloud storage.) *(Protocol 2.)*
- **Drafting-unit sizing** — Typical drafting-unit length for the project (e.g., "1,500 words per subsection," "policy-note paragraphs of ~300 words each"). This calibrates step 3 of Protocol 2 *and* the scale check at step 1. *(Protocol 2.)*
- **Lookup order** — When answering questions about source material, what files should Claude check first? (e.g., index → summaries → full text → source files.) *(Both protocols.)*

The protocol skills reference these parameters; this triage skill is the canonical source for the list.

## Composition with other skills

- **`writing_notes_skill.md`** — Protocol 1. Invoked when the user is reading sources, taking notes, or developing ideas.
- **`writing_drafting_skill.md`** — Protocol 2. Invoked when the user is producing a written deliverable.
- **`writing_branch_skill.md`** — Used by Protocol 2 from step 1 onward. Not used by Protocol 1.
- **`materials_processing_skill.md`** + Protocol skills — Protocol 1 often follows paper processing: process a paper through `materials_processing_skill.md`, then take notes on its summary via `writing_notes_skill.md`.
- **`document_processing_skill.md`** — Same relationship as paper processing for operational/institutional documents.
- **`project_tracker_skill.md`** — `writing_notes/` is a named `TRACKED_LOCATIONS` entry of the freshness check; deliverable folders are covered by its recursive `FOLDER_MAP.md` scan, wherever the archetype places them. Updates from both protocols are picked up by the freshness check.
- **`product_ledger_skill.md`** — The outside-edit route above. Owns the per-product `<stem>_LEDGER.md`; consulted whenever a product's representations may be out of step for reasons git cannot see.
- **`design_deck_reconciliation_skill.md`** — The design-tool deck case of the outside-edit route: intake, mirror extraction, slide-level mapping; routes rulings to the ledger.
- **`latex_round_trip_skill.md`** — The externally edited LaTeX paper case of the outside-edit route: the review copy, the apply register the user works from by hand, the refresh read by diff; routes events to the ledger.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
