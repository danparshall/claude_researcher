# Starter Package

A curated, scrubbed skills kit for collaborators who are new to working with
Claude in a repo-based setup. Everything here is generic: no personal voice
profiles, no institutional branding, no assets tied to one organization.

## What's the idea

Claude does not remember between sessions. Every conversation starts fresh.

The way around this is to put the context in a GitHub repo and tell Claude to
read it at the start of every session. Two things do the work:

- **`CLAUDE.md`** — the project's instruction file. Tells Claude what the
  project is, who you are, who the collaborators are, and what protocols to
  follow. Lives at the root of the repo.
- **`skills/`** — a folder of reusable workflow files. Each file is a "skill":
  instructions for handling a specific recurring task. `CLAUDE.md` references
  skills by filename and says when to read each one.

Claude reads `CLAUDE.md` at the start of every session, sees which skills apply
to the task at hand, and reads the relevant skill before doing the work.

## What's in this folder

### Bootstrap files

The files you use to stand a repo up, plus the templates a repo is built from.

- `PROJECT_SETUP.md` — the setup workflow Claude follows. Part A (new project),
  Part B (retrofit an existing repo), Part C (update an existing repo from a
  newer kit).
- `CLAUDE_template.md` — the blank `CLAUDE.md` template, including the full
  skills inventory.
- `STATUS_template.md` — the blank `STATUS.md` project-tracker template.
- `ONBOARDING_template.md` — the template for a collaborator's first document,
  written when someone with their own Claude joins the repo.
- `README_template.md` — the blank repo `README.md`: the name, one paragraph on
  what the repo is for, and a pointer at `CLAUDE.md`.
- `FOLDER_MAP_template.md` — the form of every folder's `FOLDER_MAP.md`: the
  slot row (kind and stage), the kit blocks, one catalog header per kind.
- `typed_index_template.md` — the form of every typed index (papers, materials,
  outputs, notes, and the rest): the three-sentence head and one table per
  section, with the row shape by kind.
- `standing_documents_template.md` — the standing documents of `workspace/`,
  `workdesk/` and `feedback/` (queues, registers, ledgers), with their labels.
- `gitignore_seed.md` — the `.gitignore` every repo starts from.
- `new_repo_setup.md` and `research_setup_scaffold.md` — birth-time archetype
  triage and scaffolding (see below). These are read at setup and are not
  copied into the repo.
- `CHANGELOG.md` — which version of this package you are on.

### The structure layer

A repo is one of two kinds, declared at setup:

- **Research** — lines of inquiry that build up literature and evidence toward
  papers or analytical outputs. It is the one archetype the package ships: a
  fixed root skeleton, typed indexes, and a full spec.
- **General purpose** (declared `NONE`) — any other repo: a tracker, one task
  done many times, a dated project with its deliverables. It keeps the
  universal floor and a skeleton tailored to its own work.

Three layers govern how a repo is organized, read in order:

1. **`structure_conventions.md`** — the universal floor. Root files, `workspace/`,
   `workdesk/` (including `workdesk/collaborators/` for people who work in the
   repo with their own Claude), `feedback/`, `writing_notes/` (the indexed
   notes home, `NOTES_INDEX` its one universal index), the `FOLDER_MAP`
   convention, the product ledger, versions vs. archive, and the module tier.
   Every repo keeps it. `naming_conventions.md` sits beside it.
2. **`archetype_conventions.md`** — what every archetype repo shares.
3. **`research_archetype_spec.md`** — the full structure-and-index spec for a
   research repo.

A general-purpose repo keeps only the first layer. `new_repo_setup.md` runs the
triage and proposes a kind; you confirm before anything is scaffolded.

### The skills

Skills are grouped into **clusters**. Some always ship; the rest are proposed
cluster by cluster at setup, and you decide.

**Always active**

- **Repo and session infrastructure** — `skill_authoring_skill.md`,
  `skills_curation_skill.md`, `project_tracker_skill.md`,
  `finish_session_skill.md`, `writing_branch_skill.md`,
  `exploration_branch_skill.md`, `multisession_task_skill.md`,
  `workstream_plan_skill.md`, `BLIND_SESSION.md`, `repo_conversations_skill.md`,
  `repo_audit_skill.md`, `github_api_workflow_skill.md`,
  `cross_repo_import_skill.md`, `product_ledger_skill.md`
- **Thinking aids** — `brainstorming_skill.md`
- **Shared assets** — bring-your-own; the package ships none

**Proposed at setup**

- **Source material: reading and processing** — `materials_processing_skill.md`
  (the front door), `paper_processing_academic_skill.md`,
  `paper_processing_institutional_skill.md`, `document_processing_skill.md`,
  `agent_research_verification_skill.md`, `own_document_verification_skill.md`
- **Writing and deliverables** — `writing_skill.md` (triage),
  `writing_notes_skill.md`, `writing_drafting_skill.md`,
  `visuals_workflow_skill.md`
- **Voice and style** — bring-your-own. Voice profiles are personal, so the
  package ships none; you author your own with `skill_authoring_skill.md`.
  `translation_review_skill.md` and its companion
  `translation_corrections_log.md` ship with this cluster.
- **Final-production formats** — `academic_paper_latex_skill.md` +
  `academic_paper_preamble.tex` (with `latex_round_trip_skill.md`, the review
  round trip for a paper edited outside the repo), `academic_slides_skill.md` +
  `academic_slides_preamble.tex`, and `design_deck_reconciliation_skill.md` +
  `extract_design_deck_mirror.py` (reconciling a deck built in a design tool
  against the repo's markdown). Formats particular to your institution are
  authored as further pairs (a skill plus its preamble).

Curation is cluster-level by design: clusters are the resolution that fits in
one head. You can still take or skip individual skills inside a cluster —
`skills_curation_skill.md` owns the workflow.

## How to use it

To set up a new project repo:

1. Create a new GitHub repo.
2. Open a Claude session pointed at it.
3. Tell Claude to read `PROJECT_SETUP.md` from this folder and walk through
   Part A with you.
4. Claude runs the questionnaire, triages the archetype, runs the curation
   conversation, and produces a project-specific `CLAUDE.md` plus the curated
   `skills/` folder.
5. Commit.

For an existing repo that needs the kit retrofitted, run **Part B**. For a repo
that needs updating from a newer version of this package, run **Part C**.

## Writing your own skills

This package is a starting point, not a finished set. The skills you will get
the most from are the ones you write yourself, for the tasks you actually
repeat. `skill_authoring_skill.md` is the guide: when a skill is worth writing,
what goes in one, how to name it, and how to draft it with Claude.

The two bring-your-own clusters — Voice and style, and Shared assets — exist
precisely because those files are personal. A voice profile that captures how
*you* write, or a color palette that matches *your* house style, cannot ship in
a generic package.

## What's not here

This package is a curated subset. Left out by design:

- Personal voice and style profiles, and personal shared assets such as a color
  palette
- Institution-specific format skills and their preambles (branded Word
  documents, branded decks), and the logo and background image assets they use
- Institution-bound conventions: the canonical home for one organization's
  strategy documents, and the parameter that points at it- Kit-maintenance workflows — the discovery sweep and consolidation machinery
  that maintains a canonical kit across many repos. This package is standalone;
  it does not assume you keep a kit factory. Where a skill mentions "your
  canonical skills repo, if you keep one," that is what it means.

---

*Starter package v2.5 — October 2026*
