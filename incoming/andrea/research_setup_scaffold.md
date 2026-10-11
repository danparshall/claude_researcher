---
name: research-setup-scaffold
description: >
  Birth skeleton for a NEW research repo. Born minimal (a single line, N=1, a
  paper); promotes to an agenda (N>1) if more lines appear, no migration. Built
  from new_repo_setup.md Step 3; full design in research_archetype_spec.md.
  Kit-resident; not copied into content repos.
triggers: >-
  Setting up a NEW research repo: the birth skeleton, built from new_repo_setup.md Step 3.
  Kit-resident; not copied into content repos
---

# Research archetype — new-repo scaffold (Phase-1 birth skeleton)

*Build this for a NEW research repo. Born minimal: a single line (N=1, a paper); it promotes
to an agenda (N>1) if more lines appear. No migration — just create the skeleton. Full design:
`research_archetype_spec.md`.*

## Create

*The tagged birth tree: the one structural manifest for Part A, Part C's conformance pass and
the audit (`structure_conventions.md`, "Conformance: one home per job", where the legend lives).
Every line carries one tag at the head of its comment: `[U]` unconditional, created up front ·
`[P]` with parent · `[E: condition]` event-born, the condition on the line · `[J: skill]`
judgment-born, never created by a pass.
Skill artifacts (a `_LEDGER`, a `_PLAN`, the carryover) are not structure and not here. Every
content folder this tree creates empty carries its `FOLDER_MAP.md` at birth, the `leaf` kind
where a typed index or the parent map rosters its files; the map is what persists the folder
across a clone (`structure_conventions.md`, the leaf rule).*

```
REPO ROOT
├── CLAUDE.md            [U] declares: type=research, variant=single-paper (N=1) | agenda (N>1);
│                            the structure section points at the root FOLDER_MAP.md
├── STATUS.md            [U]
├── FOLDER_MAP.md        [U] the root map (FOLDER_MAP_template.md): skeleton, root documents, latent homes, extras blocks
├── README.md            [U] from README_template.md; human register; no structure copy
├── .gitignore           [U] the kit block inside a project-owned file
├── STATUS_ARCHIVE.md    [E: first rotation out of STATUS.md]
├── RECORD.md            [E: the first big-picture row — where the project stands, by part; project_tracker_skill.md]
├── references.bib       [E: the first paper processed — one per paper home; a home mirroring an external bibliography (Zotero) keeps its own keys]
├── <line>/              [U] PREFIXED line-container, named for the line — even a lone paper
│   │                        gets <paper>/, never a bare draft/ at root (named from day one so
│   │                        growth is append-only)
│   ├── FOLDER_MAP.md    [P] carries the slot row with `Stage: <word>` — the one home of the stage
│   ├── draft/           [E: the stage offers it — active does] the line's primary written output
│   │   ├── versions/    [E: first feedback received on the document] byte-exact copies as sent
│   │   └── archive/     [J: writing_drafting_skill.md] a draft become too different to be a version
│   ├── empirics/        [E: the stage offers it — active does] the empirical work, one folder
│   ├── research_proposal/  [E: the stage offers it — active does; advisory when the work is one]
│   ├── deliverables/    [P] the umbrella, with every line
│   │   └── <category>/  [E: the first deliverable of that kind — slides, a note, a brief]
│   ├── context/         [E: line-specific setting material appears — what belongs in the
│   │                        paper's background section; at any N]
│   ├── correspondence/  [E: the line is submitted to a journal — the under_review stage]
│   │                        referee reports and editor letters only
│   ├── explorations/    [E: the line's first merged exploration]
│   └── inputs_from_team/  [E: a colleague without repo access sends a file for this line]
├── general/             [U] central shared LITERATURE layer — not born where every line is a
│   │                        self-contained paper with no shared reading, and its `## general`
│   │                        index sections go with it
│   ├── FOLDER_MAP.md    [P]
│   ├── papers/          [P] each paper = text + summary
│   │   ├── text/        [P]
│   │   └── summaries/   [P]
│   └── background/      [P]
├── skills/              [U] the kit, flat, + last_skill_update/ (folder-skill rule)
├── workspace/           [U] subfolders created up front, contents born on use; each carries its
│   │                        standing document from standing_documents_template.md (a catalog
│   │                        document, a label, or the owning skill's index)
│   ├── claude_conversations/  [U]
│   ├── brainstorms/     [U]
│   ├── multisession_active_tasks/  [U]
│   ├── staging/         [U]
│   ├── packages/        [U]
│   ├── branch_logs/     [U]
│   ├── agent_outputs/   [U] (curated: agent_research_verification; where the skill is active)
│   └── visuals/         [U] (curated: visuals_workflow; where the skill is active)
├── workdesk/            [U] the human-action layer — what waits on the user (waits-on criterion;
│   │                        structure_conventions.md); INDEX.md is the queue, its body in
│   │                        standing_documents_template.md
│   ├── INDEX.md         [P]
│   ├── admin/           [U]
│   ├── postits/         [U] the user's post-it notes (predecessor: notes/)
│   └── collaborators/   [U] the label; per-person folders below
│       └── <id>/        [E: a person other than the owner gets access — on join]
├── feedback/            [U] feedback received from people on the repo's products — one subfolder
│   │                        per person, dated entries; created up front with its seeded map (the
│   │                        kit block in standing_documents_template.md)
│   └── FOLDER_MAP.md    [P]
├── writing_notes/       [U] the indexed-notes home — every set writing_notes_skill.md produces, a
│   │                        set a file, a subject subfolder when a set spans files; NOTES_INDEX its
│   │                        catalog (structure_conventions.md; predecessor: general/notes/)
│   └── FOLDER_MAP.md    [P] kind leaf: one pointer row at NOTES_INDEX
├── quarantine/          [E: the first item held — kept but not to be used; structure_conventions.md]
├── inputs_from_team/    [E: a colleague without repo access sends a file that serves no one line]
└── funding/             [E: a funding or contracting instrument exists — a grant, a commissioned study or a ToR]
                             agenda-level, first-class; a module lands here by trigger
```

The work folders inside the line-container reflect the line's **stage**, one of the seven closed
words of `research_archetype_spec.md` §3 — `active`, `working_paper`, `under_review`,
`published` (the forward-only paper sequence), `chapter`, `advisory`, `reference` — which `new_repo_setup.md`
proposes and the user confirms, written as `Stage: <word>` in the line map's slot row, its one
home. The set above is the **active** offer (a new paper's default); other stages offer fewer
folders. Stages offer, never limit — any folder is still born on its own condition if the line
grows into it.

## Six root indexes (create all up front, empty in the form of `typed_index_template.md`, ALL_CAPS)
`MATERIALS_INDEX` · `OUTPUTS_INDEX` · `ASSETS_INDEX` · `PAPERS_INDEX` · `NOTES_INDEX` · `DEEPDIVES_INDEX`
— each with the template's head (what it registers, the writer, the sectioning by line, the
reading order), its header row under the `index` marker, the `unplaced` slot and one trailer.

## Rules at birth
- The line is a **prefixed container from day one**; a second line is added beside it (append-only).
- Naming: content `lowercase_underscore`, structural `ALL_CAPS`, a content-file marker (`TEXT_`,
  `SUMMARY_`, `_OUTLINE`) `ALL_CAPS` on a lowercase stem; paper stem = `who_what_year`,
  lowercase, and doubles as the BibTeX cite key (see `naming_conventions.md`).
- `FOLDER_MAP.md` in every content folder except a leaf born on content, holding tracked files a typed index or the parent map enumerates fully (a folder created empty carries its map, whatever its name) (the leaf rule), born with the folder, empty in the form its kind takes in `FOLDER_MAP_template.md` — title, slot row, kit blocks, description and catalog slots, one trailer line; machinery and desk (`skills/`, `workspace/`, `workdesk/`) carry none below their roots (an orientation map at a root by its kind word; `structure_conventions.md`).
- Indexes are pointer-only, line-sectioned, self-registered at creation.
- Universal floor (naming, structure, import protocol) per `naming_conventions.md` /
  `structure_conventions.md`, **plus the archetype-common layer** (`archetype_conventions.md`)
  — every archetype repo carries it; a NONE repo does not.


---
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
