---
name: new-repo-setup
description: >
  Birth-time archetype triage + scaffold for a NEW repo (not restructuring an
  existing one). Classifies the repo as research or NONE (the general-purpose
  kind) from intent questions, proposes the classification with reasoning and
  waits for confirmation, then builds the birth skeleton: from the research
  scaffold, or, for a NONE repo, a skeleton tailored to its work.
  Kit-resident birth tool, read at new-repo setup; not copied into content repos.
triggers: >-
  Standing up a NEW repo: the birth-time archetype triage and the scaffold it builds; read at
  new-repo setup, never copied into a repo
---

# New-repo setup — archetype triage + scaffold

*For standing up a **new** repo. Runs as part of project setup: detect new repo →
triage the archetype through the questionnaire → scaffold the structure + indexes.
Proposer model: it proposes the classification with evidence and **waits for the user's
confirmation** before scaffolding.*

## When this runs

A **new / empty repo** is being set up. There is nothing to inventory —
classification comes from **intended work**, asked as questions, not from reading
an existing tree.

## Step 1 — Triage through the questionnaire (intent, not files)

One question decides it. Ask it, unless the project overview already answers it, and capture
the answer:

1. **Is the work *lines of inquiry* — building up literature/evidence toward papers or
   analytical outputs, pursued for their own sake?** → **RESEARCH**.
2. **Anything else** — a repo that tracks or routes work, one task done many times with a
   deliverable per run, a dated project with its deliverables, or a mix of these → **NONE**,
   the general-purpose kind (the universal layer only, with a skeleton tailored to the work).

**Disambiguating question when 1 vs 2 is unclear:**
- Is a **body of literature and evidence built up and reused across outputs** (→ research),
  or is each piece of work done **from the material at hand** (→ NONE)?

If genuinely unclear, present both readings and ask — don't force it.

## Step 2 — Propose, with reasoning, and STOP

Present the proposed classification, the answers that drove it, and the alternative ruled out.
**Wait for the user's confirmation.** (For a single-paper new research repo, note it's the
**N=1** case — it will promote later if a 2nd line appears; born minimal now.)

## Step 3 — Scaffold (Phase-1 skeleton only)

On confirmation, build the **birth skeleton**. **No migration phases** (nothing to migrate —
it's a new repo).

**A research repo:** folders + root indexes (each empty in the form of
`typed_index_template.md`) + `FOLDER_MAP` stubs + a `CLAUDE.md` archetype declaration. The
skeleton is in `research_setup_scaffold.md`. Read it and build it.

**A NONE repo:** it has no scaffold file of its own. Build the universal homes from the
lines of `research_setup_scaffold.md` that `structure_conventions.md` names as the universal
manifest ("Governance rules", "A NONE repo declares its skeleton once"): the root files,
`workspace/` with its six universal subfolders, `workdesk/`, `feedback/`, `writing_notes/`
with its leaf map, `NOTES_INDEX.md` at root as its one index, and `skills/`, each in its
template's form, plus `workspace/agent_outputs/` or `workspace/visuals/` where the owning
skill was curated in. Then propose the
**bespoke skeleton** from the user's answers in Step 1: the root folders the work needs, one
line each with its job, inside the root rules that hold for every repo
(`structure_conventions.md`, "Governance rules"). Wait for the user's confirmation, then
create the folders and write the skeleton in the root `FOLDER_MAP.md` skeleton block, with
`type: NONE` in the `CLAUDE.md` declaration.

A **research** repo carries all three layers: the universal floor
(`structure_conventions.md` + `naming_conventions.md`), the archetype-common layer
(`archetype_conventions.md`), and `research_archetype_spec.md`. A **NONE** repo
keeps **only the floor** (`structure_conventions.md` + `naming_conventions.md`) plus its
bespoke skeleton — no spec, and not `archetype_conventions.md`.

After scaffolding, the repo is born correctly-structured; the user starts working. In a
research repo the archetype's own spec governs from there; in a NONE repo, the floor.


---
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
