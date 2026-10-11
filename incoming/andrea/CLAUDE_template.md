---
# Archetype and module declarations: written at setup, rewritten by propagation, read by
# propagation and the audit. Semantics: skills/structure_conventions.md. Pour rules: PROJECT_SETUP.md Step 7.5.
archetype:
  type:         "[research | NONE]"
  variant:      "[research: single-paper|agenda]"
modules:
  - name:    "[module name]"
    version: "[module version, e.g. v4.2]"
    home:    "[home path fixed by the trigger, e.g. funding/<module name>/]"
---

# CLAUDE.md — [PROJECT_NAME]

*Kit v[X.Y] — propagated YYYY-MM-DD*

<!--
  The one trailer line, at the top, rewritten in place at every propagation: kit version and
  date, nothing else. The propagation's record is the repo's skills/CHANGELOG.md entry and the
  Last curated line in STATUS.md; a stack of prior lines is retired form and rotates verbatim
  into STATUS_ARCHIVE.md. Where the project stands at the big-picture level is RECORD.md,
  born at its first row (skills/project_tracker_skill.md, "The record").
  Sections are the slots: the kit owns this file's form (headings, order, the kit blocks) and
  Part C's conformance pass rebuilds it in template order at every propagation, pouring the
  project's content into its slots; content that fits no slot is asked about, never dropped.
  Skills, workflows and conventions live in skills/; this file routes to them.
  A blind session (skills/BLIND_SESSION.md) stops here: it reads that file and its prompt,
  nothing else.
-->

## Project Overview

[Two or three paragraphs: what the project is, what problem it addresses, what the
deliverables are, with enough institutional context that a first reading understands the
setting. Then the facts every session needs: the people involved and how they are referred
to, the people the project touches who have no repo access (the wider cast — a roster row is
for people with access), the project's own vocabulary, the tools or languages in use.]

**Repo:** [GitHub owner/name]

**Background documents:**
- [Key background documents in the repo, one line each. Inputs to the project, not
  deliverables.]

**Project question:** [One sentence; the paper-processing workflow writes relevance sections
from it. Delete if the project involves no papers.]

**Tone and scope guidelines:**
- [Constraints on the deliverables' voice, scope or framing. Delete if not needed.]

**Deliverables:**
- [Each deliverable with its audience]

**Language:** [Working language; whether final products are translated.]

**Reading languages:** [The languages the user reads themselves; default English. Read
by the materials-processing skills and the own-document verification skill.]

## How to start

The project's routing rows: what a session reads and does first on a given ask. The kit's
own routing stays where it lives (the STATUS ask and the other Working Conventions below,
the Skills tables' When to use column, the Modules roster where one is carried); this section is project rows only.

| When the user says | Read | Then |
|---|---|---|
| [phrase] | [file or section] | [what to do] |

## Collaborators

The owner is the repo's main user; the rules in this file and the skills in `skills/` are
written for them. Every other person with access is a **collaborator** under
`skills/structure_conventions.md`, "Collaborators": their folder `workdesk/collaborators/<id>/`
is the only place they write directly on `main`; everything else goes on a
`<id>_br_<topic>-<date>` branch and reaches `main` by pull request; their `INDEX.md` is the
two-way channel (*Waiting on <name>* from the owner's sessions, *For the owner* back), with the
*Working on* block as their declared territory and `LOG.md` as their session log. **Merge**
says who merges their pull requests: `owner` (the owner merges every one; logged decisions open
*pending*) or `self` (the collaborator merges inside their territory; decisions open
*informed*). Every session that ends with a pull request leaves its decisions in the `LOG.md`
entry, found by the five-event walk, with what the session was unsure of and the instruction
it read; the owner reviews them beside the pull request, rules in the entry, and hands the
lesson back through the person's *Waiting on* table. People without access contribute
through the owner; their feedback is recorded in `feedback/`.

| Person | id | GitHub | Scope | Folder | Branches | Merge |
|---|---|---|---|---|---|---|
| **[Owner name]** | `[id]` | `[handle]` (admin) | owner | `workdesk/` | their own naming (`<topic>-<date>`) | — |
| **[Name]** | `[id]` | `[handle]` | [what they work on, and where; access date] | `workdesk/collaborators/[id]/` | `[id]_br_<topic>-<date>` | `owner` or `self` |

## Skills

Reusable skills live in `skills/`. **Read the relevant skill file before starting any task it
covers; never rely on memory of it from a prior conversation.** The tables roster every skill
by cluster; the When to use column is what fires the read. **A curated table** (the kit-metadata
group out, `skills/skills_curation_skill.md`) rosters every skill but the ten files of
that group (`CHANGELOG.md`, the seven templates, `gitignore_seed.md`, `PROJECT_SETUP.md`), and one
line here in `CLAUDE.md` says so; the group is in or out of `CLAUDE.md` together.

### Source material: reading and processing

| Skill file | When to use |
|---|---|
| `skills/materials_processing_skill.md` | Any paper or institutional document to file or process. The front door: its Step 0 routes to one of the three processing skills. Start here unless the branch is already obvious |
| `skills/paper_processing_academic_skill.md` | Academic-style papers (abstract, hypothesis, original estimates); routed from Step 0, or directly when the protocol is known |
| `skills/paper_processing_institutional_skill.md` | Institutional reports (multilateral and international organization synthesis or policy reports); routed from Step 0, or directly when known |
| `skills/document_processing_skill.md` | Operational and institutional documents (legislation, government reports, operational material); routed from Step 0, or directly when the call is obvious |
| `skills/agent_research_verification_skill.md` | "I'm going to run a deep dive," "let's draft a research prompt," "I have an agent output to file," "verify this dive"; any Claude Research or Deep Research output. Agent outputs are never citable; only the verification document is |
| `skills/own_document_verification_skill.md` | "verify this document against the repo," "check what I wrote against the sources," "verify my draft." Not for agent outputs (`skills/agent_research_verification_skill.md`) or review rounds (`skills/writing_branch_skill.md`) |

### Writing and deliverables

| Skill file | When to use |
|---|---|
| `skills/writing_skill.md` | Any reading or writing work; read first to triage between the notes protocol and the drafting protocol |
| `skills/writing_notes_skill.md` | Thinking work: processing source material, taking notes, developing ideas; routed from the triage. Always on `main` |
| `skills/writing_drafting_skill.md` | Drafting a section, chapter, policy note, report or any substantial deliverable; routed from the triage. Outlining means branching |
| `skills/visuals_workflow_skill.md` | "let's add visuals," "make a sketch for this," "we need a diagram here," "let's see the SVG"; a markdown deliverable that needs visuals beyond tables |

### Voice and style

This is a **bring-your-own cluster**: voice profiles are personal, so the package ships none.
Write your own with `skills/skill_authoring_skill.md`, one profile per distinct voice, and roster
each one here with its When to use cell. The one cluster member that ships is the translation
review, which the profiles hand off to.

| Skill file | When to use |
|---|---|
| `skills/translation_review_skill.md` (+ companion `skills/translation_corrections_log.md`) | Translating any deliverable to Spanish, and at the review round of a translated branch; the user's corrections go to the companion log |

Styles are never applied by default: apply one only when the user asks, following the
profile's own checklist.

### Final-production formats

| Skill file | When to use |
|---|---|
| `skills/academic_paper_latex_skill.md` | Setting up or editing an academic LaTeX paper (working paper, journal submission) |
| `skills/academic_paper_preamble.tex` | Used by the academic LaTeX skill; copied at generation |
| `skills/latex_round_trip_skill.md` | A review round on a paper whose LaTeX source lives in Overleaf or another external editor; "this came back from Overleaf," "my co-author sent the new .tex," "make me the list of changes to apply in Overleaf" |
| `skills/academic_slides_skill.md` | Creating or editing academic Beamer slides (conference, seminar) |
| `skills/academic_slides_preamble.tex` | Used by the academic slides skill; copied at generation |
| `skills/design_deck_reconciliation_skill.md` | A deck made in a design tool lands in staging or covers content the repo already holds; "map this design deck to the markdown." Not for building a deck from repo content |
| `skills/extract_design_deck_mirror.py` | Used by the reconciliation skill to rebuild a design deck's markdown mirror |

### Shared assets

The package ships no color palette; that is a **bring-your-own asset**. If your project needs a
consistent look across deliverables, author a palette file in `skills/`, point `PALETTE_FILE` at
it in the Repo parameters table, and roster it here.

### Repo and session infrastructure

| Skill file | When to use |
|---|---|
| `skills/skill_authoring_skill.md` | "let's write a skill for this," "I keep correcting Claude the same way," "we should codify this," "draft a skill for X"; revising an existing skill substantively |
| `skills/skills_curation_skill.md` | "let's run the curation," "curate the skills for this repo," "propagate the kit update"; every propagation point (Parts A, B and C of `skills/PROJECT_SETUP.md`) |
| `skills/project_tracker_skill.md` | Every session: the STATUS.md ask at the start, the mandatory update at close, the freshness check, bootstrap |
| `skills/finish_session_skill.md` | Every session close: "thanks," "good night," "we're done," "let's wrap up," "let's do housekeeping"; the close-out sequence, the repo's housekeeping |
| `skills/writing_branch_skill.md` | Any co-produced document reviewed on a branch; merge at session close or on request |
| `skills/exploration_branch_skill.md` | An offshoot that tests a `main` claim (robustness check, alternative spec) and must stay off `main` until resolved |
| `skills/multisession_task_skill.md` | "make a carryover"; a task that will not finish in one session and a resume prompt cannot carry |
| `skills/workstream_plan_skill.md` | "make a plan for this workstream," "this needs blind sessions," "cut the prompts"; "we are here" / "where are we on plan X" on re-entry; a STATUS entry outgrowing its slot |
| `skills/product_ledger_skill.md` | The user edited, made, sent or presented a product outside the repo; feedback came back on it; "which version is current," "make a ledger for this product" |
| `skills/BLIND_SESSION.md` | Read only by a blind session under a scoped prompt; never part of a normal session's reading |
| `skills/repo_conversations_skill.md` | "save this conversation"; a multi-session topic worth finding later; proactively after a substantive exchange |
| `skills/repo_audit_skill.md` | "audit the repo," "run the audit," "run a consistency check," "is CLAUDE.md still accurate?", "find orphaned files," "run the index audit" |
| `skills/github_api_workflow_skill.md` | At the start of any session that will commit, and whenever commit, branch or merge mechanics are needed; the repo-access authority for both environments |
| `skills/cross_repo_import_skill.md` | "import X from repo Y," "bring in the material from [repo]," "hand X over to [repo]," a workdesk row saying a hand-over is owed; Cowork only. Not a skills sweep, not export |

### Repo structure and archetype

| Skill file | When to use |
|---|---|
| `skills/naming_conventions.md` | Before naming or renaming any file or folder |
| `skills/structure_conventions.md` | Creating or placing any folder or file; something starts waiting on the user; the form of every kit-shaped file. The universal floor, kept in every repo |
| `skills/archetype_conventions.md` | Structuring, placing or typing files in an archetype repo. Kept in every archetype repo; none in NONE |
| `skills/research_archetype_spec.md` | Structuring, placing, indexing or auditing files against this repo's declared archetype. Kept where the `type` in `CLAUDE.md`'s frontmatter is `research`; none in NONE |

### Modules

Shared folder packages this repo carries because it has their structural trigger
(`skills/structure_conventions.md`, "Modules"). Not in `skills/`; each lives at the home its
trigger fixes. Read the module's `MODULE.md` first, then its skill. The `modules:` declaration
at the top of this file lists the same set.

| Module | Home | Version | When to use |
|---|---|---|---|
| `[module name]` | `[home path]/` | `[vX.Y]` | [Trigger phrases, copied from the registry's trigger-phrases column (`modules/MODULES.md` in your canonical skills repo, if you keep one); the module-check bullet in Working Conventions fires on them] |

### Thinking aids

| Skill file | When to use |
|---|---|
| `skills/brainstorming_skill.md` | "let's brainstorm," "I want to think through X," "help me refine this idea"; a vague task where the right deliverable is not obvious yet |

### Project skills

This repo's own workflows, each in a file, next to the work it serves (a single file in the
work's folder, or a skill with its own folder there); `skills/` is the kit's folder, and the
one repo file that sits in it is a **kit candidate in waiting**, rostered here until it is
folded into your canonical skills repo, if you keep one (`structure_conventions.md`,
"Skills layout"). A project rule that fits one bullet is a convention and goes under Project
conventions; anything with steps is a workflow and lives here.

| Skill file | When to use |
|---|---|
| `[path/to/skill]` | [Trigger] |

## Paper Processing Workflow

> **Generic skill:** `skills/materials_processing_skill.md` is the front door; its Step 0
> routes papers to `skills/paper_processing_academic_skill.md` or
> `skills/paper_processing_institutional_skill.md`. Read the skill before the task; this
> section holds the project's parameters and conventions only.

- **PROJECT_QUESTION:** "[One sentence describing the project's research focus]"
- **CONDITIONAL_SECTION:** "[The subset of findings to extract when present, e.g. 'region-specific
  findings'; 'None' if no conditional section is needed]"

### Project conventions

- [Conventions beyond the skill, or none]

## Document Processing Workflow

> **Generic skill:** `skills/document_processing_skill.md`, the document branch of the
> materials triage (`skills/materials_processing_skill.md` Step 0 routes here). Read the
> skill before the task; it discovers the materials index and the filing home from the
> `FOLDER_MAP.md` files at run time.

Reliability labels (kit defaults; edit to fit the project):

| Label | Meaning |
|---|---|
| **Citable** | Published, final, authoritative |
| **Validated** | Internal or partner document, final, reviewed |
| **Under construction** | Active draft, directionally correct |
| **Working draft** | Early-stage, may have gaps |
| **Flagged — verify with the user** | Known issues, use only with confirmation |

Confidentiality labels (kit defaults):

| Tag | Meaning |
|---|---|
| `PUBLIC` | Publicly available |
| `INTERNAL` | Internal working document |
| `CONFIDENTIAL` | Restricted distribution |

### Project conventions

- Bindings (`skills/document_processing_skill.md`, "Setting Up for a New Project"; Step 0 reads
  this line at every document): reliability labels — [bound: kit default | deferred until the
  first document]; confidentiality labels — [bound: kit default | deferred]; naming convention —
  [bound: the default | deferred]; materials-index home — [bound: `MATERIALS_INDEX.md` | deferred]
- [Conventions beyond the skill, or none]

## Agent Research Workflow

> **Generic skill:** `skills/agent_research_verification_skill.md`. Read it before any
> deep-research work. **Agent outputs are never directly citable; only the verification
> document is.** The skill hands off to this project's papers protocol at its Step 6.

The `AGENT_OUTPUTS_*` paths are declared once, in Repo parameters below, and so are
`PAPERS_PROTOCOL_SKILL` and `DOCUMENT_PROTOCOL_SKILL`.

### Project conventions

- [Conventions beyond the skill, or none]

## Writing Protocol for Drafts

> **Generic skill:** `skills/writing_drafting_skill.md` (Protocol 2; `skills/writing_skill.md`
> is the parent triage). Read the full protocol before any drafting task; the workflow,
> the branch rule, the scale check and the finalization steps live there.

- **Drafting-unit sizing:** [e.g. "1,500 words per subsection" or "policy-note paragraphs of
  about 300 words"; the input to the scale check. If unset, Claude asks at outline approval]

### Project conventions

- [Conventions beyond the skill, or none]

## Protocol: Note-Taking from Reading

> **Generic skill:** `skills/writing_notes_skill.md` (Protocol 1; `skills/writing_skill.md`
> is the parent triage and its "Setting up for a new project" section defines the parameters
> below). Read the protocol before a reading session.

- **Note sets:** [Each set by name and purpose; every set is a file in `writing_notes/`, the
  kit's home in every repo, with its `NOTES_INDEX` row — never a path here. A progress
  tracker or verification list, if kept, with its path. Actions waiting on the user go to
  `workdesk/INDEX.md`, not to a project doc]
- **Status labels:** [Kit defaults: Must-read, Read, No need to read, Middle importance,
  Flagged; add the project's own]

### Project conventions

- [Conventions beyond the skill, or none; e.g. "papers are reviewed in index order"]

## Document Format & Export Workflows

> **Generic skills:** the Final-production formats table above pairs each format's skill with
> its preamble; read the format skill before producing the file. Colors default to
> the project's palette file where one is declared (`PALETTE_FILE`).

- **Main working format:** [Markdown by default, since the final product goes to a designer
  and human editor; or LaTeX from the start, or another]

### Project conventions

- [Conventions beyond the skills, or none]

## Naming Conventions

> The universal casing rule lives in `skills/naming_conventions.md` (content
> `lowercase_underscore`; structural files `ALL_CAPS`; a content-file marker an `ALL_CAPS`
> token on a lowercase stem, from its closed list), the folder model, versions, archive
> and inputs from team members in `skills/structure_conventions.md`, and the hierarchical
> naming of multi-part drafts in `skills/writing_drafting_skill.md`. Papers and institutional
> documents are named by their own pipelines. This section holds only the project's own rules.

### Project conventions

- [Naming rules specific to this project, or none]

## Repo parameters

The single home for every parameter the always-active skills read. Each skill documents what
its parameters mean (`skills/repo_audit_skill.md`, `skills/project_tracker_skill.md`,
`skills/repo_conversations_skill.md`);
this table holds the repo's values. `none` is a legal value: it means the parameter is
deliberately undeclared, and the audit reports the check that reads it as **skipped:
undeclared** instead of skipping silently. A row left bracketed is unfilled, which the audit
also reports. `KIT_FOLDER` is `skills/`, the kit's flat folder (`structure_conventions.md`, "Skills layout").

| Parameter | This repo | Kit default |
|---|---|---|
| `KIT_FOLDER` | [`skills/`] | `skills/` |
| `INFRASTRUCTURE_FILES` | [the files the audit checks] | `CLAUDE.md`, `README.md`, all `FOLDER_MAP.md` |
| `INDEX_FILES` | [the typed root indexes this repo carries, listed] | none |
| `DELIVERABLE_FOLDERS` | [the folders holding this repo's deliverables] | the content homes the root map's skeleton block names |
| `PALETTE_FILE` | [`<KIT_FOLDER>/<your_palette>.md`, or none] | none |
| `AGENT_OUTPUTS_FOLDER` | [`workspace/agent_outputs/`, or none] | none |
| `AGENT_OUTPUTS_INDEX` | [`<AGENT_OUTPUTS_FOLDER>/INDEX.md`] | derived from the folder |
| `AGENT_OUTPUTS_LESSONS` | [`<AGENT_OUTPUTS_FOLDER>/LESSONS.md`] | derived from the folder |
| `AGENT_OUTPUTS_SKIPS` | [`<AGENT_OUTPUTS_FOLDER>/WORKFLOW_SKIPS.md`] | derived from the folder |
| `EXCLUDED_PATHS` | [paths the audit skips, or none] | none |
| `TRACKED_LOCATIONS` | [the tracker's default set, or a repo-specific list] | the tracker's default set |
| `EXTRA_TRACKED_LOCATIONS` | [additional paths for the freshness check, or none] | none |
| `INDEX_AUDIT_INTERVAL` | [days] | 30 days |
| `WORKFLOW_MODE` | [`branches` or `main_only`; read by the branch skills] | `branches` |
| `USER_IDS` | [the Collaborators roster's ids, or none] | none |
| `TAG_THRESHOLD` | [saved conversations before a tag vocabulary is proposed] | 10 |
| `STATUS_LOCATION` | [where `STATUS.md` lives, if not at root] | `STATUS.md` at root |
| `DOCUMENT_PROTOCOL_SKILL` | [the document-processing protocol this repo runs, or none] | none |
| `PAPERS_PROTOCOL_SKILL` | [the paper-processing protocol this repo runs, or none] | none |

## Working Conventions

- **Trackers are the source of truth, not past chats.** `CLAUDE.md`, `STATUS.md` and the
  `FOLDER_MAP.md` files are the record of where work stands. Do not search past chats at
  session start, and verify "last time we decided X" against the trackers. Saved
  conversations are retrievable artifacts, not the resumption mechanism.
- **STATUS.md: ask at the start, update at the close.** Before anything else, ask literally
  "Do you want me to check STATUS.md?" and do not open it before the answer. At close
  ("thanks," "good night," "we're done") the update is mandatory: draft, show, commit.
  A session that changed no workstream's state — a capture push, a dictation, a mechanical
  sweep — owes no entry; its commit is the record.
  Protocol: `skills/project_tracker_skill.md`; the close sequence: `skills/finish_session_skill.md`.
- **Whose session is this.** When the prompt does not say who is there, establish it before
  reading any tracker (the git config name at Cowork; ask on the web). The owner's session runs
  as this file describes; a collaborator's runs in guest mode per the Collaborators section.
  Mechanics: `skills/structure_conventions.md`, "Collaborators"; `skills/project_tracker_skill.md`.
- **Check placement before creating a folder.** Describe its purpose, read that against the
  maps and indexes, decide whether it is a new unit (a new line, in a research repo) or new
  structure, then propose the home and write its
  `FOLDER_MAP.md` at creation, empty in the form of
  `skills/FOLDER_MAP_template.md`; a folder the user created gets the same check on first
  reference. A mis-placed folder is flagged, never moved (`skills/structure_conventions.md`).
- **Stage new material, and run the lightning check.** Anything new enters
  `workspace/staging/` and is placed by the intake check. Before using a staged file,
  producing anything, or asking the user for an input the repo might hold, grep the indexes by
  topic, ten seconds, always: a hit means work from the processed form, never re-process.
  Index layer only; the routing by kind is in `skills/structure_conventions.md`, the lightning check.
- **The workdesk queue.** The moment something starts waiting on the user, add a row to
  `workdesk/INDEX.md` (an action from read · think · decide · do — the closed list,
  `skills/structure_conventions.md`, "workdesk/"; a pointer to the artifact,
  never a copy). Deferred Claude actions go to STATUS, not the queue. The queue is read as well as
  written: when a named task or a workstream step opens, grep `workdesk/INDEX.md` for its subject
  first, since a row aimed at a later cycle can become the task's most useful item once the
  timing changes.
- **A module's trigger phrase is a check before the work starts.** On a module's trigger
  phrase (the Modules roster's, where one is carried), check the
  `modules:` declaration where one is carried, and the `MODULE.md` on disk. Carried: read the module's skill first. Absent with its trigger folder
  present or coming: offer to land it now (`skills/PROJECT_SETUP.md` Steps 2.6 and 5). Never
  draft a module's document with the general skills while the module exists unlanded.
- **Iterative workflow.** The user gives information in stages; do not jump ahead or produce
  output without a go-ahead.
- **Don't infer, ask.** Missing what you need to act correctly (which file, which audience,
  what counts as done, which language), ask; one round trip beats an undo. A small gap can be
  stated inline as an assumption the user can correct cheaply. Inferring silently is the failure
  mode.
- **Show before committing.** Before any write to the repo or a deliverable, say in a
  sentence what will be written and why; the scripted gates in specific skills (merges,
  deletions) are the emphatic cases. On a feature branch the branch is the show, and the gate
  moves to the merge — during drafting only; from the handover of a round of the user's comments
  on, every push is shown first (`skills/writing_branch_skill.md` Convention 3 owns the
  prohibition).
- **Plain register for outlines and anchor documents.** Full sentences, one idea per beat,
  examples named; never compressed note style. If Claude has to talk the user through a document
  it wrote, the document failed.
- **"Plan" is a routing word.** On "plan," pause and triage: one bounded task split across
  sessions is a carryover (`skills/multisession_task_skill.md`); a workstream with its own
  sequence and open decisions is a plan file (`skills/workstream_plan_skill.md`). State the
  routing in one sentence and confirm before building.
- **A correction that restates a loaded skill is a misfire.** When the user's correction repeats
  something a skill already in play says, offer to log a `[SKILL-FEEDBACK]` entry in
  `skills/CHANGELOG.md`, model version included (`skills/structure_conventions.md`, the
  channel). The close-out asks once more.
- **Codify after the third repetition.** The same kind of ask three times, in one session or
  visibly across sessions, is a candidate rule: a Project conventions bullet here, a project
  skill, or a status doc. Three is deliberate: earlier is premature, later is the user repeating
  themselves.
- **The project slots are living; the form is the kit's.** Update the project content here as
  the project evolves. The headings, order and kit blocks are regenerated from
  `skills/CLAUDE_template.md` at every propagation, and content that fits no slot is asked
  about then.
- **"Uploaded" / "pushed" = this GitHub repo.** Check the repo, not the chat.
- **Skills stay in `skills/`.** Never duplicate skill content into this file; reference the
  skill and read it when the task fires. The workflow sections above carry parameters,
  pointers and project conventions only; a project workflow with steps lives in a file and is
  rostered under Project skills.
- **Repo file listing.** For what files exist, query the repo live; never rely on memory or a
  cached listing. The structure itself: Repository Structure below.

### Project conventions

- [Conventions specific to this project, one bullet each, or none]

## Repository Structure

This repo's folder model and index set are, in an archetype repo, its archetype spec
(`skills/research_archetype_spec.md`, in a research repo) over
`skills/archetype_conventions.md` and the universal floor,
`skills/structure_conventions.md`; in a NONE repo, the floor plus the bespoke skeleton declared
in the root map, with no spec and no conventions file. Read the live structure, never a copy kept
here: the root skeleton, root documents, latent homes and registered extras are in the root
`FOLDER_MAP.md`, the one home of the kit-owned structural blocks (a tree or table in this
section is retired form); what is inside a folder is in that folder's `FOLDER_MAP.md`; the
root indexes register by kind; what files are physically present, query live.

---
<!-- Kit file marker below: the template's own version line, not part of the repo file. -->
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
