# Project Setup & Skill Integration Guide

This file is the entry point for any session that involves the skills kit's
lifecycle — new projects, existing repos, kit updates, or portability
evaluations.

**Rule:** Read this file before doing anything that involves the kit. Do not
rely on memory of its contents from prior conversations.

## When to use this file — trigger map

| The user says… | Go to… |
|---|---|
| "set up a new project/repo," "start a new repo," "create CLAUDE.md for X" | **Part A: New Project Setup** |
| "integrate the skills into this repo," "bring this repo in line with the kit," repo has no `skills/` folder yet | **Part B: Skill Integration for Existing Repos** |
| "update the skills on this repo," "propagate the kit," "apply v2.X to this repo" | **Part C: Propagating Kit Updates to Repos** |

---

## Step 0 — Triage

Before proceeding, confirm which Part applies. The triage questions:

1. **Does the repo have a `CLAUDE.md`?**
   - No → **Part A**
   - Yes → continue

2. **Does the repo have a `skills/` folder?**
   - No → **Part B**
   - Yes → continue

3. **Is the user asking about…**
   - Updating the kit (new version) → **Part C**
   - (Note: there is no session-end "evaluate portability" path. Improvements made during normal work simply remain in the repo's `skills/` folder; if you keep a canonical skills repo, the next pass over it picks them up. Portability — "is this generic or project-specific?" — is decided when you next update that canonical copy, not in-session, because that is the moment you can see all your repos at once.)

If unclear, ask the user which path to follow.

---
---

# Part A: New Project Setup

Use this when starting a repo from scratch. The answers to the questionnaire below populate `CLAUDE_template.md` and determine which skills to activate, which folders to create, and what the CLAUDE.md should contain.

**Rule:** Ask the questions in the order below. Group related questions naturally (2–3 at a time), don't fire all of them at once. Use the answers to fill in the template. If the user has already provided some answers in their initial message, skip those questions — don't ask what you already know.

---

## Phase 1: Project Identity

**Q1. Project name**
What should we call this project? (Used for the CLAUDE.md header and folder references.)

**Q2. Project overview**
What is this project about? What problem does it address, what are the deliverables, and who is the audience? (2–3 sentences is enough — we can expand later.)

**Q3. Project question**
Can you state the core research/policy question in one sentence? (This is used by the paper processing skill to write relevance sections in summaries. If the project doesn't involve papers, we can skip this.)

**Q4. Working language**
What language do we work in? Will final products need translation?

---

## Phase 2: Collaborators

**Q5. Who works on this project?**
For each person: name, role, and whether they have direct repo access or contribute through someone else. Also: will anyone other than the owner interact with Claude directly on this repo? Anyone with direct access other than the owner is a **collaborator** under `structure_conventions.md`, "Collaborators": record their roster row for `CLAUDE.md` (id, GitHub handle, scope, Merge mode — `owner` or `self`) and plan their `workdesk/collaborators/<id>/` folder with its `ONBOARDING.md` (from `ONBOARDING_template.md`), created at setup action 2 beside the universal scaffold.

---

## Phase 3: Archetype triage

Before curating skills or building structure, classify the repo as one of two
kinds — **research**, the archetype, or **NONE**, the general-purpose kind (any
repo that is not a research repo) — and confirm it with the user. The kind
decides the repo's structure and index set (the scaffold builds them in the
Setup actions below) and whether the repo keeps the archetype spec (curation
reads the confirmed type at Q6). Run the triage per `new_repo_setup.md`
Steps 1–2; this phase is the triage and confirmation only — the scaffold (its
Step 3) runs after curation.

**The triage is a proposer step, not a fixed questionnaire.** Its intent
question asks about the *nature of the intended work*, which Q2 (overview) and Q3
(question) already speak to. Don't re-ask what those answered — read the
signal from them, ask the disambiguating question only if it remains open
(a body of literature and evidence built up and reused across outputs →
research, vs. each piece of work done from the material at hand → NONE), then
**propose the kind with the evidence that drove it and STOP.** Wait for
the user's confirmation before anything is built.

Capture, as part of the confirmation, what the scaffold and the spec need for a
research repo: the **variant/stage** (single-paper N=1 / agenda N>1) and the
**named work-unit(s)** — the line(s) or the paper. For a single-paper new
repo, note the **N=1** case: born minimal now, promotes additively later if a
second line appears — no migration. A **NONE** repo keeps no archetype spec: it
carries the universal layer only, plus a skeleton tailored to its own work.

The confirmed `type` / `variant` is what the Setup actions write
into the CLAUDE.md archetype declaration, and what Q6 reads to keep the archetype
spec (research) or none (NONE). **Index definitions are not set here** — they
live in the archetype spec (`research_archetype_spec.md`), described there first.

---

## Phase 4: Skills Activation

The skills kit is activated through **per-propagation curation** — see
`skills/skills_curation_skill.md` for the workflow. At project setup (Part A),
existing-repo integration (Part B), and kit propagation (Part C), Claude proposes
which clusters of the kit should be active for the project, anchored to project
signals, with the user confirming, overriding, or refining — by cluster, or down to
individual skills.

The cluster structure — what's in each cluster and what each skill does —
lives in `CLAUDE_template.md`'s Skills section. The four optional clusters get
the proposal; the always-active group (repo and session infrastructure,
brainstorming, kit metadata, the universal naming/structure conventions) ships to
every project without a question. The single archetype spec is fixed by the
confirmed type (Phase 3) — also no question.

The four optional clusters:
- **Source material: reading and processing**
- **Writing and deliverables**
- **Voice and style**
- **Final-production formats** (with per-format-pair sub-asks — the natural grain
  for that cluster)

**Granularity — cluster is the default unit, individual skills can be picked.**
Claude proposes at the cluster level because clusters are the fastest unit to
reason about, but the decision is the user's: take a cluster whole, skip it, or pick
individual skills inside it. There is no all-or-nothing rule and no special-case
cluster — see `skills_curation_skill.md` ("Granularity") for how partial picks are
handled and the one risk they introduce (orphaned intra-cluster dependencies,
which Claude warns about but does not block). *(This relaxed rule — a cluster-level
proposal with a free per-skill decision — replaces the pre-v3.2 all-or-nothing
rule, under which partial activation was refused and Final-production formats were
the lone exception.)*

**Q6. Open the curation conversation.**

Curation reads the **confirmed archetype** from Phase 3: the always-active group
ships unconditionally, and the single archetype spec is fixed by the confirmed
`type` (`research_archetype_spec.md` for research; NONE keeps none) — a constrained
pick, not proposed against signals. For the four **optional** clusters, Claude
proposes activate/skip for all of them together, each naming the signal it's
based on (Q1–Q5 and the archetype); the user confirms, overrides, or refines down
to individual skills. The activated clusters determine which follow-up parameter
questions (Q7/Q8) fire — when a cluster is activated, all parameter questions for
the skills inside it fire.

The curation conversation itself is saved to the repo's
`workspace/claude_conversations/` via `repo_conversations_skill.md` (tags
include `curation` and `propagation-vX.Y`). STATUS.md records the
resulting cluster-activation state. Together, STATUS.md tells future-you
what's active now and the saved conversation tells why.

### Follow-up parameter questions, fired by cluster activation

**If Source material cluster is activated:**

**Q7a. Conditional section?**
When processing papers, is there a specific subset of findings to extract when present? (E.g., "region-specific findings," "findings on a named subgroup.") If not, summaries will use the standard (a)(b)(d) structure without a conditional section.

**Q7b. BibTeX file name?**
Default is `references.bib` at the repo root. Different name?

**Q7c. How should input documents be organized?**
By source institution? By theme? By document type? (Default: by source institution inside the material home: the spec names it in a research repo, the skeleton block in a NONE repo.)

**Q7d. Reliability labels?**
The defaults are: Citable, Validated, Under construction, Working draft, Flagged. Do these fit this project, or do you want to customize?

**Q7e. Confidentiality labels?**
The defaults are: PUBLIC, INTERNAL, CONFIDENTIAL. Do these fit, or do you want to customize?

**Q7g. Agent outputs folder location?**
Default is `workspace/agent_outputs/`. Different location?

**Q7h. Papers protocol entry point?**
The agent_research skill hands off to the papers protocol at Step 6. Default is `materials_processing_skill.md`. If this project uses a different entry point, name it.

**If Writing and deliverables cluster is activated:**

**Q8a. Will this project involve structured note-taking?**
Which note sets will the reading produce? Each is a file in `writing_notes/` with a `NOTES_INDEX` row, named for its line of thinking. A progress tracker or verify-in-repo list, if wanted, names its path here; actions waiting on you go to the workdesk queue, never to a project document.

**Q8b. What status labels will you use for papers/sources?**
Default set: Must-read, Read, No need to read, Middle importance, Flagged. Want to customize?

---

## Phase 5: Working Conventions

**Q11. Main working format?**
Default is markdown. Should we work in something else from the start (e.g., LaTeX)? (This is a working-conventions choice, not a structure one — the folders come from the archetype scaffold, not from the format.)

**Q12. Any project-specific conventions?**
Things like: naming rules for files, how team members submit inputs, special commit procedures, tone/scope guidelines for the deliverable.

**Default conventions (included in every new project):**
- Iterative workflow — Claude waits for the user's go-ahead before producing output
- CLAUDE.md is a living document
- Repetition rule — if a task is done 3+ times, check whether it should be codified
- "Uploaded" / "pushed" = GitHub repo
- Skills stay in `skills/` — don't duplicate skill content into CLAUDE.md

---

## After the questionnaire: Setup actions

Once the user has confirmed the archetype (Phase 3), completed the curation conversation (Q6), and answered the remaining questions, Claude does the following:

1. **Write the CLAUDE.md** by the conformance pass's part 2 (Step 7.5, the `CLAUDE.md` bullet: the per-block rules, the archetype's frontmatter lines, the placeholder rule, the length target), with the interview's answers as the content poured into the slots and the confirmed triage as the declaration. There is no one-time fill: the same rules regenerate the file's form at every propagation. The `modules:` declaration and the Modules roster are written in step 2, when the scaffold lands a module. Present for review before committing.

2. **Scaffold the confirmed archetype.** Read the archetype's scaffold, `research_setup_scaffold.md` — the tagged birth tree, the one structural manifest (`structure_conventions.md`, "Conformance") — and build what its tags say: every `[U]` line and every `[P]` line under a created parent; an `[E]` line only where the interview established its condition (a funding instrument exists); never a `[J]` line. That gives the archetype's folders, its **index set** (each index created up front, empty in the form of `typed_index_template.md`, `ALL_CAPS`; the fill rules in Step 7.5 part 2), and a `FOLDER_MAP.md` in each content folder, written empty in the form its kind takes in `FOLDER_MAP_template.md` (the fill rules in Step 7.5 part 2). The **root `FOLDER_MAP.md`** is built here too, with its skeleton, root-documents, latent-homes and extras blocks; `README.md` from `README_template.md` (the what-this-repo-is-for paragraph from the interview, in plain prose for a person; the fill rules in Step 7.5 part 2) and `.gitignore` from the kit's `gitignore_seed.md` land with it. The scaffold also builds the universal layer every repo gets — `workspace/` (with the universal subfolders `claude_conversations/`, `brainstorms/`, `multisession_active_tasks/`, `staging/`, `packages/`, `branch_logs/`, all **created up front as labeled-empty homes**, contents born on use, each with its standing document from `standing_documents_template.md`), `workdesk/` (the human-action layer: `INDEX.md` — the pending-actions queue — plus `admin/`, `postits/` and `collaborators/`, their bodies from the same template, per `structure_conventions.md`), `feedback/` with its seeded map, `writing_notes/` (the indexed-notes home, with its leaf map and `NOTES_INDEX.md` at root — the one index every repo carries), and `skills/`; an **archetype** scaffold additionally creates the **curated-skill homes** `workspace/agent_outputs/` (`agent_research_verification`) and `workspace/visuals/` (`visuals_workflow`). A **NONE** repo gets only the universal layer (no archetype folders, no archetype-common layer, no archetype spec; `NOTES_INDEX.md` its only index), plus a curated-skill home where Q6 activated its owning skill. Its bespoke skeleton is proposed from the triage answers and confirmed by the user before any skeleton folder is created (`new_repo_setup.md` Step 3), then written in the root `FOLDER_MAP.md` skeleton block. Folder model, index definitions, and naming are **not redefined here** — they live in the archetype spec and the convention files (`structure_conventions.md`, `naming_conventions.md`, and — for an archetype repo — the archetype-common `archetype_conventions.md`); Part A runs the scaffold and points at them.

   **A module lands when the scaffold creates its trigger.** Before building, read the registry `modules/MODULES.md` in your canonical skills repo, if you keep one (local clone at Cowork; via the API on web, per `github_api_workflow_skill.md`), for the trigger-home pairs. When a folder the scaffold creates is a declared trigger — a research `funding/` born because there is a funding instrument — copy the module's traveling folder from `modules/<name>/` in your canonical skills repo to the home the trigger fixes: everything except `corpus/`, `CHANGELOG.md` and the maps (the home's and its subfolders' `FOLDER_MAP.md` are the repo's, never the module's — written empty in `FOLDER_MAP_template.md`'s form at the land, as any folder's, and filled from disk; `structure_conventions.md`, "Modules"), and write the card's `this copy` row from the trigger that fired (`MODULE.md`, the one per-copy row). A nested module rides with its parent at its relative home. Fill the exempt parameters file from its blank template (the canonical copy carries it blank) with what the interview answered and leave the rest as placeholders; write `last_module_update/` as byte-identical copies of the text files landed, the maps and the exempt file apart. No curation question is asked: the trigger decides (`structure_conventions.md`, "Modules"). Then record it: one row per `MODULE.md` landed, nested ones included, in the CLAUDE.md `modules:` declaration and in the Skills section's Modules roster block.

### Skills layout

`skills/` is the kit's folder and it is flat (`structure_conventions.md`, "Skills layout"): the kit's files loose in it, `last_skill_update/` inside it, `KIT_FOLDER` = `skills/`. A repo still carrying the retired split layout (`skills/general_skills/`) is flattened at its next propagation (Part C, Step 5).

3. **Copy the curated skill subset** into `${KIT_FOLDER}` — the always-active group + every skill in every activated cluster (with Final-production format-pair sub-decisions applied) + the single archetype spec matching the declared type (NONE copies no spec). The kit metadata files (`PROJECT_SETUP.md`, the seven templates — `CLAUDE_template.md`, `STATUS_template.md`, `ONBOARDING_template.md`, `README_template.md`, `standing_documents_template.md`, `FOLDER_MAP_template.md`, `typed_index_template.md` — `gitignore_seed.md`, `CHANGELOG.md`) ship as part of the always-active group. Birth tools (`new_repo_setup.md`, `research_setup_scaffold.md`) are **kit-resident** — read at setup, never copied into the repo. Mirror the copied files into the `last_skill_update/` snapshot (byte-identical; the baseline the next kit update compares against). Source from the canonical kit copy in the local clone of your canonical skills repo at Cowork (filtered to the curated subset), or from an unzipped copy of the kit; a claude.ai web session fetches it via the GitHub API from that repo (per `github_api_workflow_skill.md`'s web branch). Modules are not part of this copy: they land in step 2 by trigger, never in `${KIT_FOLDER}`.

4. **Create the cluster-conditional starter files** — the artifacts keyed to *which optional clusters* were activated at Q6, which the archetype scaffold does not own:
   - `references.bib` (or the custom name from Q7b) — if Source material is active and paper processing is among the parameters.
   - The note sets named at Q8a — each a file in `writing_notes/` with its `NOTES_INDEX` row (`writing_notes_skill.md`); a progress tracker or verify-in-repo list, if wanted, at the path Q8a gave.
   - *(The archetype `*_INDEX` set, every `FOLDER_MAP.md`, and the curated-skill homes with their standing documents — `workspace/agent_outputs/` with its INDEX, LESSONS and WORKFLOW_SKIPS triple included — are built by the scaffold in step 2, not here.)*

5. **Populate STATUS.md** at repo root, generated from `STATUS_template.md` by the conformance pass's part 2 (Step 7.5, the `STATUS.md` bullet: the workstream entries, one per unit the scaffold created, with the interview's first moves; the open questions the interview surfaced). The cluster-activations block records the curated state per `skills_curation_skill.md` Step 7, replacing the initial-template "unknown" values; the archetype and the module set are in `CLAUDE.md`'s frontmatter (step 1), not here. The `WORKFLOW_MODE` answer goes to `CLAUDE.md`'s Repo parameters table. Header flag: `reviewed` (the user just confirmed every entry).

6. **Save the curation conversation** to `workspace/claude_conversations/` per `repo_conversations_skill.md` (tags include `curation` and `propagation-vX.Y`, where vX.Y is the kit version integrated). This is the audit trail for why the activations and the archetype are what they are.

7. **Commit everything** in one initial commit naming the archetype, the activated clusters, and any module landed, then **summarize** what was set up, which clusters were activated, and what went to `STATUS.md`'s Open questions for later decisions.

---
---

# Part B: Skill Integration for Existing Repos

Use this when a repo already has a `CLAUDE.md` and needs to be brought in line with the current generic skills kit. The goal is to integrate the generic skills without overwriting project-specific content — and to surface cases where the repo's version of something is better than the generic.

**Core principle:** The repo's project-specific content (project overview, collaborators, deliverables, project question, parameters, tracking documents, conventions) is sacred. The generic skills are tools that serve the project — they get added alongside or underneath what already exists, never on top of it.

---

## Phase 1: Audit the Existing Repo

### Step 1 — Read the existing CLAUDE.md

Read the full CLAUDE.md. Understand:
- What the project is about
- Who the collaborators are
- What deliverables exist
- What protocols are already in place (writing, reading, paper processing, etc.)
- What folder structure exists
- What conventions are defined
- Whether there's a `skills/` folder already, and if so, what's in it
- Whether there's a `skills/CHANGELOG.md` (used to determine which kit version the repo is on — if present)

### Step 2 — Inventory for the user

Present a short summary to the user:

> "Here's what I found in this repo's CLAUDE.md:
> - **Project:** [name and brief description]
> - **Protocols in place:** [list — e.g., writing protocol, paper processing, note-taking]
> - **Skills folder:** [exists / doesn't exist] [if exists: contains X, Y, Z]
> - **Kit version the repo is on:** [read from skills/CHANGELOG.md, or 'unknown' if no CHANGELOG]
> - **Conventions:** [key conventions already defined]
> - **Folder structure:** [what's there]"

Wait for the user to confirm the inventory is accurate before proceeding.

---

## Phase 2: Gap Analysis

Phase 2 has two stages: **cluster curation** (proposing which clusters of
the kit should be active for this repo) and then **per-skill gap analysis**
inside the activated clusters.

### Stage 1: Cluster curation

Run the per-cluster curation conversation per `skills/skills_curation_skill.md`.
Signal sources for Part B are: the repo's existing `CLAUDE.md`, `FOLDER_MAP.md`
files (or whatever the repo uses to describe its folders), any existing
`skills/`-like content, `STATUS.md` if present, recent commits. The current `skills/` folder contents (if any) are consulted only
to detect drift (orphaned files); they are NOT what proposals anchor on.

The four optional clusters get the sequential ask. The always-active group
(repo and session infrastructure, repo structure conventions,
brainstorming, kit metadata)
ships without a per-cluster question.

After the curation conversation, the curated set is what gets gap-analyzed
in Stage 2.

### Stage 2: Per-skill gap analysis (inside activated clusters)

For each skill **inside an activated cluster**, classify it:

| Category | Meaning | Action |
|---|---|---|
| **Missing** | The repo doesn't address this at all | Propose adding it |
| **Covered but weaker** | The repo has something, but the generic skill is more developed | Propose replacing with the generic, preserving project-specific parameters |
| **Equivalent** | The repo's version and the generic are functionally the same | No action needed |
| **Stronger in repo** | The repo has a better version than the generic | Note in the integration report. If you keep a canonical skills repo, fold the difference back into it the next time you update the kit. No in-session action required. |

Skills in deactivated clusters are not gap-analyzed — they are not part of
this repo's kit. If a deactivated cluster's skill has a project-specific
analog in the repo (e.g., a project-specific paper-processing protocol in
a repo where Source material cluster is deactivated), that analog stays
where it is and is not classified against the generic skill.

### How to assess each skill (only for skills inside activated clusters)

**Writing workflow (`writing_skill.md` + Protocol skills) — Writing cluster:**
- Does the repo have a writing/drafting protocol? How detailed is it?
- Does it have a reading/note-taking protocol?
- Does it separate the two (thinking vs. writing)?
- Are the key rules present (interactive outlines, one-pass drafting, review-before-commit)?
- The skill ships as three files since v2.1.8: `writing_skill.md` (triage with shared content), `writing_notes_skill.md` (Protocol 1), `writing_drafting_skill.md` (Protocol 2). All three propagate together; the triage routes to the appropriate protocol skill.

**Paper processing (`materials_processing_skill.md` + `paper_processing_academic_skill.md` + `paper_processing_institutional_skill.md`) — Source material cluster:**
- Does the repo process papers? If so, how?
- Are the steps defined (Step 0 triage; then per-protocol rename, extract, summarize, index, BibTeX)?
- Are project-specific parameters set (PROJECT_QUESTION, CONDITIONAL_SECTION)?
- Is there a tracking/status system?
- All three skills propagate together. If the repo carries an older single-file paper-processing protocol, the Part C refactor re-points the reference and adds the two protocol skills.

**Document processing (`document_processing_skill.md`) — Source material cluster:**
- Does the repo process non-academic documents (legislation, government reports, institutional material)? If so, how?
- Are the steps defined (rename, extract, summarize, classify, index, cross-reference)?
- Are reliability and confidentiality labels defined?
- Is there a materials index and are the folders mapped?

**Agent research verification (`agent_research_verification_skill.md`) — Source material cluster:**
- Does the project run deep-research agents (Claude Research, ChatGPT Deep Research, similar)? If yes:
  - Is there a folder for agent outputs? Where?
  - Is there a discipline distinguishing raw agent output from verified findings? (Most older projects won't — this is the discipline the skill codifies.)
  - Is there an INDEX.md tracking past dives?
  - Is there a LESSONS.md of prompt-engineering responses to past failure modes?
- If the project runs agent dives but lacks these structures, propose adopting the skill plus bootstrapping `workspace/agent_outputs/INDEX.md`, `workspace/agent_outputs/LESSONS.md` and `workspace/agent_outputs/WORKFLOW_SKIPS.md` — the skill's triple.

**Own-document verification (`own_document_verification_skill.md`) — Source material cluster:**
- Does the project produce documents whose claims need checking against the repo's processed sources (deliverables approaching submission, collaborator drafts arriving from outside)?
- If yes, does the repo have the prerequisites — processed sources (extracts registered in indexes) and a drafting-artifacts home to insulate against?
- The skill inherits its claim-verification core from `agent_research_verification_skill.md`; ship the pair together where possible (the skill carries a fallback paragraph for repos without the sibling, but the pair is the intended configuration).

**Voice profiles (bring-your-own) — Voice and style cluster:**
- The kit ships **no** personal voice profiles — you author your own with `skill_authoring_skill.md`, and this cluster is where they live. The gap analysis for them is therefore about the repo, not about a generic file to compare against.
- Does the repo reference a writing-style or voice profile at all? Is it inline in CLAUDE.md or in a separate file?
- Are the key elements present (draft-first-style-second, do-not-infer, a pre-styling checklist)?
- Which voices does this project actually need — your own academic voice, an institutional house voice, a principal's voice you write on behalf of, an endorsement/vouching voice for recommendation letters? Each becomes one authored profile in this cluster.

**Translation review (`translation_review_skill.md` + `translation_corrections_log.md`) — Voice and style cluster:**
- Does the repo produce Spanish deliverables?
- Is there existing translation-corrections material (notes, marked-up translations, ad-hoc pair lists) worth folding into `translation_corrections_log.md` at adoption?

**Academic paper LaTeX (`academic_paper_latex_skill.md` + `academic_paper_preamble.tex`) — Final-production formats:**
- Does the project produce an academic paper in LaTeX? If yes, is there already a preamble, and does it differ from the kit's?

**Academic slides (`academic_slides_skill.md` + `academic_slides_preamble.tex`) — Final-production formats:**
- Does the project produce academic presentations (conference talks, seminars)?

**Branded or institutional formats (bring-your-own) — Final-production formats:**
- Does the project produce branded deliverables — a house Word template, an institutional LaTeX note, a team slide deck? The kit ships only the generic academic pair; any branded format skill (plus its preamble and logo/background assets) is one you author yourself with `skill_authoring_skill.md` and keep in this cluster.
- If such a spec already exists in the repo — inline, in a separate file, or only in someone's head — note it here so it can be written up as a proper format skill.

**Always-active group — no per-skill gap analysis, but two confirmations:**

These skills ship to every repo without per-cluster ask. Two parameter
confirmations still apply:

- **The repo audit (`repo_audit_skill.md`):** confirm whether the repo's default audit scope (the content homes the root map's skeleton block names) matches this project, or whether the parameters need tuning (e.g., exclude or add folders).
- **Project tracker (`project_tracker_skill.md`) and STATUS.md:** does the repo have a `STATUS.md` at root, or any equivalent project-level tracking file? If not, one will be bootstrapped during Phase 3 (Integration) — Claude reads the existing `CLAUDE.md`, the repo's folder-description files (`FOLDER_MAP.md` or whatever the repo uses), recent `CHANGELOG.md` entries (if present), and recent commits, drafts a `STATUS.md` from those signals (including the cluster-activations block populated from Stage 1's curation), walks the user through section-by-section for review, then commits.
- Does the existing `CLAUDE.md` have a "Parking Lot" section? If yes, it will be migrated to STATUS.md's "Open questions" section at bootstrap time, and the CLAUDE.md Parking Lot section removed in the same commit.
- Does the repo's default workflow mode (`branches` vs `main_only`) need to be confirmed? Most content repos use `branches`; only quick personal/scratch repos use `main_only`.
- Folder bootstrap: every universal `workspace/` subfolder defined in `structure_conventions.md` that does not exist in the repo, the `workdesk/` scaffold, the `feedback/` home with its seeded `FOLDER_MAP.md`, and the `writing_notes/` home with its leaf map and `NOTES_INDEX.md`, is created in the integration commit — unconditionally, per the created-up-front convention (an empty subfolder is a labeled home reading as state, never clutter). No per-folder ask. Where the repo has an existing arrangement doing the same job (a root `TODO.md`, a conversations folder under another name), Claude proposes reconciling it into the universal home — prompt-don't-perform; the home is created either way. Curated-skill homes (`workspace/agent_outputs/`, `workspace/visuals/`) follow their owning skill's curation, not this bootstrap. *(Replaces the v2.2 per-folder ask / Deferred-folders mechanism.)*

### Present the gap analysis

Show the user a table covering skills inside activated clusters only:

| Skill | Cluster | Status | Notes |
|---|---|---|---|
| Writing workflow | Writing (activated) | Covered but weaker — has a writing protocol but missing the reading/note-taking protocol and session resumption rules | Propose adding generic, preserving the project's outline-unit and drafting-unit conventions |
| Paper processing | Source material (activated) | Equivalent — full pipeline already defined with project-specific parameters | No action; copy to `skills/` as-is |
| Visuals workflow | Writing (activated) | Missing | Propose adding |
| Academic slides | Final-production formats (activated, Academic slides selected) | Missing | Propose adding |
| ... | ... | ... | ... |

**Wait for the user's input.** They decide what to integrate. Do not proceed without their go-ahead on each item.

---

## Phase 3: Integration

For each skill the user approves:

### Step 1 — Create the `skills/` folder (if it doesn't exist)

Create `skills/` at the repo root.

### Step 2 — Copy in the curated skill subset

Copy each skill file from your copy of the kit into the repo's `skills/` per the curation outcome from Phase 2 Stage 1. Use the standard filenames — do not rename them. The curated subset = the always-active group plus every skill in every activated cluster (with format-pair sub-decisions applied for Final-production formats).

Files grouped by cluster — copy each cluster's files only if that cluster was activated in Phase 2 Stage 1:

**Source material: reading and processing** *(copy these if Source material cluster was activated)*
- `skills/materials_processing_skill.md`
- `skills/paper_processing_academic_skill.md`
- `skills/paper_processing_institutional_skill.md`
- `skills/document_processing_skill.md`
- `skills/agent_research_verification_skill.md`
- `skills/own_document_verification_skill.md`

**Writing and deliverables** *(copy these if Writing cluster was activated)*
- `skills/writing_skill.md` (triage)
- `skills/writing_notes_skill.md` (Protocol 1 — ships alongside triage)
- `skills/writing_drafting_skill.md` (Protocol 2 — ships alongside triage)
- `skills/visuals_workflow_skill.md` (visuals embedded in markdown deliverables; invoked from drafting)

**Voice and style** *(copy these if Voice cluster was activated)*
- `skills/translation_review_skill.md` + `skills/translation_corrections_log.md` *(companion pair — the Spanish naturalness review; ships whenever the Voice cluster is active. On propagation to a repo that already carries the log, the log reconciles per Step 3's per-file local-modification handling — local pairs are never silently dropped)*
- Plus any **voice profiles you have authored yourself** with `skill_authoring_skill.md`. The kit ships none — a voice profile is personal by definition — but this cluster is their home, and they propagate with it like any other file once they exist.

**Final-production formats** *(copy only the format-pairs selected in the cluster's sub-asks)*
- `skills/academic_paper_latex_skill.md` + `skills/academic_paper_preamble.tex` *(if Academic paper LaTeX selected)*
- `skills/latex_round_trip_skill.md` *(ships whenever the LaTeX paper pair is selected — the review round trip for a paper whose live source is edited in Overleaf or another external editor: the review copy, the apply register, the refresh; routes events to `product_ledger_skill.md`)*
- `skills/academic_slides_skill.md` + `skills/academic_slides_preamble.tex` *(if Academic slides selected)*
- `skills/design_deck_reconciliation_skill.md` + `skills/extract_design_deck_mirror.py` *(companion pair — placing and reconciling a deck authored in a design tool (Claude Design and the like) against the repo's own version of the same content; routes rulings to `product_ledger_skill.md`. Ships whenever any slides format-pair is selected, and on demand the first time a design-tool deck lands in a repo without it; added v5.1)*

**Always-active group** *(copy all — these ship to every repo)*
- `skills/skill_authoring_skill.md` *(meta-skill for authoring new skills; needed in every repo so the conventions are available wherever new skills are written)*
- `skills/project_tracker_skill.md`
- `skills/finish_session_skill.md`
- `skills/writing_branch_skill.md` *(in always-active group; required dependency of `finish_session_skill.md`)*
- `skills/exploration_branch_skill.md` *(in always-active group; the long-lived exploration-branch workflow — placed with `writing_branch_skill.md`, added v4)*
- `skills/multisession_task_skill.md` *(in always-active group; the multi-session carryover — universal because its home `workspace/multisession_active_tasks/` is defined in `structure_conventions.md` for every repo, added v4)*
- `skills/workstream_plan_skill.md` + `skills/BLIND_SESSION.md` *(in always-active group; the workstream plan-file workflow — plain default, scoped upgrade — and its blind-session companion asset; universal because workstreams arise in any repo and the plan file lives with the work; the pair ships together. Added v4.2 as `scoped_plan_skill.md`; since merged and renamed — a repo carrying the old file replaces it at propagation)*
- `skills/product_ledger_skill.md` *(in always-active group; the per-product `<stem>_LEDGER.md` tracker — which representation is current, where they diverge, what has been sent, presented, or decided; born on the first event git cannot see. Universal because any repo's product can be edited, sent, or presented outside the repo; the `feedback/` folder and `finish_session_skill.md` Step 4c consume it. Added v5.1)*
- `skills/repo_conversations_skill.md`
- `skills/repo_audit_skill.md`
- `skills/github_api_workflow_skill.md`
- `skills/cross_repo_import_skill.md` *(in always-active group; universal — any repo can import from another, NONE included; Cowork-only, reading the source repo's local clone; fires only on an import trigger, added v4)*
- `skills/skills_curation_skill.md` *(needed in every repo so future propagations can run the curation conversation)*
- `skills/brainstorming_skill.md`
- `skills/STATUS_template.md` *(informational reference — the actual `STATUS.md` lives at repo root, generated from this template at bootstrap time)*
- `skills/ONBOARDING_template.md` *(template for a collaborator's first document — `workdesk/collaborators/<id>/ONBOARDING.md`, written by the owner's session on join; ships everywhere because `workdesk/collaborators/` is universal. Added v6.2)*
- `skills/CLAUDE_template.md` *(template ships for reference)*
- `skills/README_template.md` *(the repo's `README.md` is generated from it at setup and regenerated in form at every propagation — the one repo file whose reader is a person. Added v6.4)*
- `skills/standing_documents_template.md` *(the body of every standing document of `workspace/`, `workdesk/` and `feedback/`, created at setup and regenerated in form at every propagation. Added v6.5)*
- `skills/FOLDER_MAP_template.md` *(the form of every `FOLDER_MAP.md` by kind of folder and of the root map's blocks, written empty at the folder's creation and regenerated in form at every propagation. Added v6.5)*
- `skills/typed_index_template.md` *(the form of every typed root index and a repo's own catalog — the head, the header row per kind, the markers, the trailer — created empty by the scaffold and regenerated in form at every propagation. Added v6.5)*
- `skills/gitignore_seed.md` *(the kit-owned block inside the repo's project-owned `.gitignore`, written at setup and regenerated at every propagation. Added v6.4)*
- `skills/PROJECT_SETUP.md` *(setup-guide reference ships for completeness)*
- `skills/CHANGELOG.md` *(records which kit version the repo is on; future Part C runs read this)*

**Repo structure and archetype** *(always-active group; floor conventions to every repo, the archetype-common layer to archetype repos only, the spec to research repos only)*
- `skills/naming_conventions.md` *(universal — copied to every repo)*
- `skills/structure_conventions.md` *(universal — copied to every repo, including NONE)*
- `skills/archetype_conventions.md` *(archetype-common — copied to every archetype repo; a NONE repo does not get it)*
- `skills/research_archetype_spec.md` — the archetype spec, copied where the repo's declared type is `research`; a NONE repo copies none
- *Not copied per-repo:* `skills/new_repo_setup.md` and `skills/research_setup_scaffold.md` are kit-resident birth tools, read from the kit at new-repo setup only — never copied into a content repo.

### Step 2a — Land the module set

Modules are the shared-module tier (`structure_conventions.md`, "Modules") and land on a structural trigger, never through curation — they are independent of Phase 2's cluster conversation and never enter `skills/`. Run **Part C Step 2.6** against this repo: detect each registry module's triggers from the repo's structure, walk for `MODULE.md` files, reconcile the found set against the declared set, and present the one approval table. Land each approved module per Step 2.6's rules (the traveling copy at the home its trigger fixes; the exempt parameters file from its blank template — extended, never overwritten, where a copy exists; nested modules from their own canonical copies; a fresh `last_module_update/` baseline). The wiring rides the steps that follow: the `modules:` declaration rows and the Modules roster block at Step 3's refactor, everything in the Step 5 commit.

### Step 2b — Bootstrap STATUS.md and tracked folders

This step runs after the skills are copied but before CLAUDE.md is refactored. It establishes the project-level tracker and ensures the folders the new skills depend on exist.

**Folder bootstrap (create unconditionally).** For each universal `workspace/` subfolder, each piece of the `workdesk/` scaffold (`INDEX.md` + `admin/` + `postits/` + `collaborators/`), the `feedback/` home with its seeded `FOLDER_MAP.md` (the record/wait/link/version split stated at the point of use; every standing document's body from `standing_documents_template.md`), the `writing_notes/` home with its leaf map and `NOTES_INDEX.md` at root (`structure_conventions.md`, "`writing_notes/`"; the migration of a predecessor notes home is Part C Step 8.5's, run here too when one exists), the root `FOLDER_MAP.md` with its kit blocks (the skeleton block drafted from the root folders and their maps, for approval), `README.md` from `README_template.md` (the fill rules in Step 7.5 part 2: an existing README read for the paragraph worth keeping, the retired forms dropped and reported, a structure tree or table asked) and the `.gitignore` kit block, all defined in `structure_conventions.md`, check whether it exists in the repo:
- If yes → skip.
- If no → create it in this Part B integration commit. No ask — the universal subfolders are load-bearing homes for always-active skills, created up front as labeled-empty homes per the convention; an empty subfolder reads as state, never clutter, so declining one saves nothing and breaks the floor every skill reads.

If the repo has an **existing arrangement doing the same job** as a universal home (a root `TODO.md` or a `general/to_do/` doing the workdesk queue's job, a conversations folder under another name), Claude proposes reconciling it into the universal home — for a to-do arrangement, item-by-item into the `workdesk/INDEX.md` queue — migration is the user's call (prompt-don't-perform), but the universal home is created either way. Curated-skill homes (`workspace/agent_outputs/`, `workspace/visuals/`) follow their owning skill's curation, not this bootstrap. *(This replaces the v2.2 per-folder ask and its **Deferred folders** CLAUDE.md subsection; a repo still carrying that subsection has it resolved at the next Part C run — see `project_tracker_skill.md`, Folder bootstrap protocol.)*

**STATUS.md bootstrap.** Follow the procedure in `project_tracker_skill.md` Bootstrap → Part B section:
1. Read the existing `CLAUDE.md`, the repo's folder-description files (`FOLDER_MAP.md` or whatever the repo uses), recent `CHANGELOG.md` entries (if present), and recent commits (last 10–20 on `main`).
2. Draft a STATUS.md in the template's form (`STATUS_template.md`; the pour rules in Step 7.5 part 2): one workstream entry per unit — where it stands, Next, Waits on — from what those artifacts reveal, plus the open questions.
3. Walk the user through the draft section by section for review.
4. Once approved, STATUS.md is committed alongside the other Part B changes.

**Parking Lot migration.** If the existing `CLAUDE.md` has a "Parking Lot" section, its contents migrate to STATUS.md's "Open questions" section during bootstrap. The CLAUDE.md Parking Lot section is removed in the same commit (handled in Step 3 — Refactor CLAUDE.md).

Header flag on the new STATUS.md: `reviewed` (the user just reviewed every section).

### Step 3 — Refactor CLAUDE.md

This is the most delicate step. The goal: make CLAUDE.md reference the `skills/` files instead of having protocols inline, while preserving all project-specific content.

**What to preserve (never delete or overwrite):**
- Project Overview section (name, description, question, audience, deliverables)
- Collaborators section
- Project-specific parameters (PROJECT_QUESTION, CONDITIONAL_SECTION, etc.)
- Project-specific conventions
- Folder structure — the root `FOLDER_MAP.md`'s skeleton block, built at Step 2b; the `CLAUDE.md` section is the pointer
- Any project-specific skills or protocols that aren't covered by the generic kit

**What migrates out of CLAUDE.md (handled in Step 2b — Bootstrap STATUS.md):**
- The Parking Lot section, if present. Its contents move to STATUS.md's "Open questions." Remove the CLAUDE.md Parking Lot section in this Step 3 refactor commit.

**What to refactor:**
- Inline protocols that now have a generic skill equivalent → replace with a reference to the skill file plus the project-specific parameters, written in the template's three-part form for a workflow section (`CLAUDE_template.md`).
- Add the Skills table (from `CLAUDE_template.md`) listing all activated skills, each When to use cell copied verbatim from the skill's `triggers:` frontmatter key
- Add the kit Working Conventions bullets not already present, in the template's current text (iterative workflow, the project slots are living, codify after the third repetition, uploaded = repo, skills stay in `skills/`, and the rest)

**What to add:**
- Skills table
- References to newly added skills
- Any sections from `CLAUDE_template.md` that the repo is missing and that apply (the How to start and Project skills slots; a workflow section for each activated cluster, in the template's three-part form; Repo parameters)

### Step 4 — Present the updated CLAUDE.md

Show the user the full updated CLAUDE.md. Highlight what changed:
- "Added: Skills table, reference to visuals_workflow_skill.md, reference to writing_skill.md"
- "Refactored: Writing protocol now references `skills/writing_skill.md` — project-specific parameters preserved"
- "Unchanged: Project Overview, Collaborators, Paper Processing parameters, folder structure"

**Wait for approval before committing.**

### Step 5 — Commit

Commit the `skills/` folder, any landed module homes, and the updated CLAUDE.md with a message like:
```
Integrate generic skills kit (vX.Y): add skills/, refactor CLAUDE.md to reference skill files
```

### Step 6 — Flag "Stronger in repo" cases

If any skills were classified as "Stronger in repo" in the gap analysis, note them in the integration report. If you keep a canonical skills repo, fold them back into it the next time you update the kit. No in-session action — portability calls happen when the canonical copy is updated, not during integration.

---
---

# Part C: Propagating Kit Updates to Repos

**Environment: Cowork only.** This workflow reads a newer copy of the kit from local files sitting alongside this repo — a clone of your canonical skills repo, if you keep one, or an unzipped kit folder. If this is a claude.ai web session, stop and tell the user this needs to run at Cowork — do not improvise a web-side alternative. At Cowork, open by stating the direction — "propagating from the newer kit copy into `<this repo>`" — and wait for the user's confirmation before proceeding.

Use this when you hold a newer version of the kit (new version number, renames, new skills, existing skills modified) and the user wants to push those updates into an existing repo that already has `skills/` integrated.

**When to trigger:** the user says "update the skills on this repo," "push the new skills," "propagate the kit," "apply v1.X to this repo."

**Two modes.** The step-by-step below is the interactive, single-repo default. When a campaign targets several repos at once — a propagation wave or any Part-C-shaped multi-repo change — run the **Multi-repo waves — the parallel-agent protocol** section (after Step 11) instead of repeating the interactive mode per repo.

**Core principles:**
- The newer kit copy is the source of truth for this run. At Cowork it is directly readable as local files, so Claude stages from it (Step 1); if it is a clone, sync it with its remote before staging.
- Never overwrite without checking. Repos may have local modifications that should be preserved or reconciled. Local modifications are detected per-file (Step 3 classification); they don't filter which files propagate, only how content merges.
- **Per-propagation per-cluster curation** (v2.1.13 change, replacing the v2.0.1 full-kit-by-default convention). At each propagation, Claude runs the curation conversation per `skills_curation_skill.md`, proposing per-cluster activation based on project signals (STATUS.md, CLAUDE.md, recent commits, recent conversations — NOT the current `skills/` folder contents). The user confirms or overrides cluster by cluster. The curated subset is what gets applied to `skills/`; clusters that were active but are now inactive have their files hard-removed.
- The always-active group (repo and session infrastructure, repo structure conventions, brainstorming, kit metadata) ships with every propagation without per-cluster ask. See `skills_curation_skill.md` for the rationale and the cluster completeness invariant that lets curation work without runtime dependency resolution.
- After updates land, the repo's `skills/last_skill_update/` snapshot is refreshed wholesale to match the active `skills/` (Step 9). This is what the next kit update (the discovery sweep, if you keep a canonical skills repo) compares against.
- **The module tier rides Part C** (`structure_conventions.md`, "Modules"): a module lands or updates because its structural trigger is present in the repo, never through curation; it lives at the home the trigger fixes, outside `skills/`; its exempt per-repo file is never overwritten. Step 2.6 fixes the module set; Steps 3, 5, 7, and 9 carry the module branch.
- **Propagation is a migration, not an installer** (`structure_conventions.md`, "Conformance"): a repo conforms to the kit at every propagation, one home per job at the kit's path. Step 7.5 is the conformance pass — it creates every home the manifest requires, runs the same-job check from the CHANGELOG's New homes lines, rebuilds every kit-shaped file in template order and pours the repo's content into the template's slots, and puts every judgment on one approval list. Nothing is moved or deleted on Claude's call; the empty home is created regardless. *(Retired at v6.4: the installer premise, under which a home was created and never reconciled with the folder already doing its job.)*

---

## Step 1 — Stage the new version

Claude creates `skills/pending_vX.Y/` (where `vX.Y` is the target kit version — e.g., `pending_v5.0/`; the folder name carries whatever version is being propagated) and populates it with the **full kit**, copied from the canonical kit copy in the local clone of your canonical skills repo. Confirm the kit version with the user before copying, and sync that clone first. The staging folder is a working-tree device only — it is never committed, and Step 11 deletes it. The registered modules stage beside the kit: every module's traveling folder from `modules/<name>/` in your canonical skills repo (everything except `corpus/` and `CHANGELOG.md`, the two kit-side files that never travel) is copied to `skills/pending_vX.Y/modules/<name>/`, same device, same cleanup; the registry is `modules/MODULES.md` there.

Staging is always the full kit. Curation happens *in session*, not at staging — the staging folder is the candidate set; the curation conversation decides which of those candidates actually land in `skills/`. Pre-curating at staging would anchor decisions on setup-time guesses rather than on a deliberate per-propagation conversation.

*(If the session cannot read the newer kit copy directly, the user can fill the staging folder themselves by extracting the kit zip into it. The folder's job is the same either way: it pins the candidate set and anchors the curation conversation.)*

---

## Step 2 — Claude reads both folders and the CHANGELOG

Read:
1. `skills/pending_vX.Y/CHANGELOG.md` — what changed between the repo's current version and the target
2. `skills/CHANGELOG.md` — what version the repo is currently on (if no CHANGELOG, assume v1.0 or earlier)
3. Every file in `skills/` and `skills/pending_vX.Y/`
4. Every staged `MODULE.md` (`skills/pending_vX.Y/modules/<name>/MODULE.md`) for the module's version, and the module's kit-side `modules/<name>/CHANGELOG.md` in your canonical skills repo for what changed in the module since the repo's copy (the card carries no history)

Extract from the staging CHANGELOG: renames applied, new files added, existing files modified, version numbers (from → to).

---

## Step 2.5 — Confirm the archetype declaration (declaration-backfill)

Before any file classification or diff, read the repo's root `CLAUDE.md` for the `archetype:` YAML declaration block (the declaration format: `archetype:` / `type:` / `variant:`).

**If present:** continue to Step 3. The spec travels with the kit, so a repo is always at the spec it carries; the spec's marker line is its version, and the pass drops a `spec_version` key from the declaration.

**If absent** (repos restructured into archetype shapes before the declaration format existed will not carry it):
1. Determine the kind (research or NONE) from the repo's actual structure, tested against the staged `archetype_conventions.md` and `research_archetype_spec.md` — not from memory or from the repo's self-description alone. If the user has named the archetype (e.g., from the propagation manifest), treat it as the hypothesis to confirm, not the answer.
2. For a research repo, determine `variant` from the repo and the staged spec.
3. Present the proposed declaration block to the user for approval, flagging any mismatch between the named archetype and the observed structure.
4. On approval, add the block to the repo's `CLAUDE.md` (it lands in the same atomic commit as the rest of the propagation, Step 9).

The declaration gates the rest of Part C: a research repo keeps `research_archetype_spec.md` (a NONE repo keeps none, and skips archetype-dependent steps). Archetype *conformance* verification (audit Check 12) is not run here — it runs post-propagation, per Step 10.

---

## Step 2.6 — Confirm the module set (trigger detection + declaration backfill)

After the archetype declaration, before file classification. Modules are the shared-module tier (`structure_conventions.md`, "Modules"): folder packages a repo carries because a structural trigger is present, never through curation. Their registry is `modules/MODULES.md` in your canonical skills repo; the staged copies sit under `skills/pending_vX.Y/modules/<name>/`.

1. **Detect triggers, tree-first.** For every module in the registry, test each of its trigger-home pairs against the repo's tree: a folder trigger is present when the folder exists anywhere the pair names it; an archetype trigger is present when the Step 2.5 declaration names that type; a nested module's trigger is its parent landing or being present. Read the trigger from the repo's structure, never from its self-description and never from a roster: a module list in a wave order or a manifest is a hint, and the walk runs in every repo regardless. A module whose registry status is *planned* is reported as a planned trigger present, never landed.
2. **Find what is there.** Walk the repo for `MODULE.md` files (outside any `last_module_update/`): the found set. Read the `CLAUDE.md` `modules:` block: the declared set. If the campaign manifest names a predecessor folder for a module (a copy made before the tier existed), move it to the module's home now (`git mv`, so history follows); it joins the found set without a `MODULE.md`, and Step 3 classifies its files as locally modified against the staged module.
3. **Reconcile** into one table, one row per module and per trigger-home pair: trigger present + module found → **update** (Step 3 classifies its files); trigger present + nothing found → **land** (new module; the exempt parameters file from its blank template); found but undeclared → update and **backfill the declaration**; declared but not found → anomaly, surface; found with no trigger → surface, never removed on Claude's call. Note each found module's `MODULE.md` version against the staged version for the update plan.
4. **Present** the table and the proposed `modules:` rows to the user, one row per `MODULE.md` that will exist after the run, nested modules included with their full home. On approval, the rows land in `CLAUDE.md` in the same atomic commit (Step 11).

Exemption protects a file from being overwritten, not from being corrected — a retired parameter or a path to a folder that left is corrected at the refresh and reported.

No module is landed, moved, or removed before the user approves this table. Modules never enter `skills/` and are not part of the Step 3.5 curation conversation.

---

## Step 2.7 — Confirm the collaborator set (access reconcile + roster backfill)

After the module set, before file classification. Collaborators are the people with access other than the owner (`structure_conventions.md`, "Collaborators"); every one of them is onboarded onto the convention, so access and the repo's own record never drift apart unnoticed.

1. **Read the three sets.** GitHub's direct collaborators — the **access set** (`gh api repos/<owner>/<repo>/collaborators?affiliation=direct` at Cowork, plus `/invitations` for pending ones; the Collaborators API on web); the `CLAUDE.md` Collaborators roster — the **declared set**; the `workdesk/collaborators/<id>/` folders — the **scaffolded set**. Read access from GitHub, never from the repo's self-description.
2. **Reconcile** into one table, one row per person: in all three → nothing; on GitHub, not in the roster → **surface** — the owner rules onboard (a roster row, the folder, `ONBOARDING.md` from the template) or revoke (their own account action, never Claude's); in the roster, not on GitHub → **surface** — stale row or re-invite; roster row without a folder → **scaffold** the folder in the commit; folder without a roster row → **backfill** the row. A pending invitation is listed, not acted on.
3. **Present** the table with the proposed roster rows (id, GitHub handle, scope, Merge mode) to the owner. On approval, the rows and folders land in the same atomic commit (Step 11); an `ONBOARDING.md` the run drafts carries its Review line as "draft, pending the owner's review" and gets a `workdesk/INDEX.md` queue row (Action: read) for their review — the assignment part especially; their review writes the date into the line. The new folder's `INDEX.md` gets its first *Waiting on* row in the same commit — read `ONBOARDING.md`, Action: read, Added by the owner — which the collaborator's Claude clears at the close of the session that presented the document.

No access is granted or revoked by this step, and no roster row is written before the owner approves the table. A repo whose access set is the owner alone reports "none" and moves on.

---

## Step 3 — Classify each file

For each file in the staging folder, classify it:

| Category | Definition | Action |
|---|---|---|
| **Up to date** | Repo has a file with the same name and byte-identical content | No action (subject to Step 3.5 curation — file may still be removed if its cluster is deactivated) |
| **Rename target** | Staging has a new name; repo has a corresponding file under the old name (per the kit CHANGELOG) | Rename the repo's file to the new name, then compare content (still subject to Step 3.5 curation) |
| **Outdated — unmodified** | Repo has the file with older content; content matches the older kit version exactly | Replace with new kit version if its cluster stays active (Step 3.5); otherwise remove |
| **Outdated — locally modified** | Repo has the file with older content AND the content differs from that older kit version (repo customized it) | Flag for the user — show the diff, let them decide merge / replace / keep. If the cluster is deactivated in Step 3.5, the local-modification question is moot (file removed); flag explicitly so the user doesn't lose customization without realizing it. |
| **New in staging, not in repo** | Staging has a file the repo doesn't have | Add if its cluster is activated in Step 3.5; do not add if its cluster is deactivated |
| **Repo-only** | Repo has a file not in staging (project-specific or older kit file the user chose to exclude) | Leave untouched |

Step 3 classification determines **how** each file's content changes; Step 3.5 curation determines **whether** the file is present in the repo at all. They are independent dimensions of the propagation.

**Modules are classified at folder level.** For each module Step 2.6 marked *update*, the unit in the plan is the module, and the files inside are compared against the repo's `<home>/last_module_update/` the same four ways (up to date / outdated unmodified / outdated locally modified / new in staging), rolled up to one row. Four exceptions to the file rules: the **exempt file** (typically `parameters.md`) is never compared or overwritten — when its schema grew, append the new keys as placeholder rows and flag them; **`corpus_inbox/`** is never diffed, and is emptied only of the candidates the module's record in your canonical skills repo, if you keep one, says were consolidated; **the maps** — the home's and its subfolders' `FOLDER_MAP.md` — are the repo's, never the module's, so they are never compared or replaced here; the pass owns them like every other map (Step 7.5 part 2; `structure_conventions.md`, "Modules"); **`last_module_update/`** is the baseline, refreshed at Step 9, never classified. A module marked *land* is one new-in-staging row. **`MODULE.md`** is compared like any kit file, and its update is a regeneration: the card's kit block is taken whole from the staged copy with the `this copy` row written from Step 2.6's detected pair, and the feedback slot's entries are surfaced before the block is replaced — an entry the module's record in your canonical skills repo, if you keep one, says was extracted is dropped, any other is kept in the slot (the fill rules, Step 7.5 part 2); a difference inside the block itself is a hand edit of kit text, shown as locally modified.

Also scan for references: after identifying renames, search the whole repo (not just `skills/`) for mentions of the old filename. Typical places:
- Root `CLAUDE.md`
- `FOLDER_MAP.md` files in any folder (or whatever the repo uses to describe its folders)
- Task-specific skills that may reference generic skills
- Redirect stubs or documentation files

List every reference to any renamed file.

---

## Step 3.5 — Run the curation conversation

Per-propagation per-cluster curation per `skills/skills_curation_skill.md`. Signal sources for Part C are STATUS.md, recent commits, recent conversations (`workspace/claude_conversations/`), and CLAUDE.md — NOT the current `skills/` folder contents. Anchoring on the folder anchors on what was decided at last propagation, which is exactly what curation is designed to make a fresh decision against.

Walk the user through the four optional clusters sequentially. Confirm or override each. Then compute the curation delta — ADD (cluster activated, file not currently present), REMOVE (cluster deactivated, file currently present), UNCHANGED (cluster still active, file present, version-update behavior from Step 3 applies).

Present the delta to the user for final confirmation before continuing to Step 4. The curation conversation itself gets saved per `skills_curation_skill.md` Step 8 (the save via `repo_conversations_skill.md`).

---

## Step 4 — Present the update plan

Show the user a table that combines per-file classification (Step 3) with the curation delta (Step 3.5):

```
| File | Cluster | Repo state | Staging state | Status | Proposed action |
|------|---------|-----------|---------------|--------|-----------------|
| writing_skill.md | Writing (active) | v1.0 | v3.0 | Outdated — unmodified; also see split into Protocol skills | Replace with triage + 2 protocols |
| materials_processing_skill.md | Source material (active) | v2.0.0 | v2.0.0 | Up to date | No action |
| visuals_workflow_skill.md | Writing (active) | v1.0 (modified) | v1.1 | Outdated — locally modified | Review diff |
| MyVoiceProfile_Skill.md → my_voice_profile_skill.md | Voice and style (active) | old name | new name | Rename target | Rename + compare |
| academic_slides_skill.md | Final-production / Academic slides (active) | — | v1.2 | New in staging | Add (per curation) |
| academic_paper_latex_skill.md | Final-production / Academic paper LaTeX (inactive) | v1.0 | v1.2 | Cluster deactivated in curation | Remove from skills/ |
| project_specific_tracker.md | (project-specific, not kit) | — | — | Repo-only | Leave |
| funding/<module>/ (module) | (module, trigger `funding/`) | v4.2, 2 files modified | v5.0 | Outdated — locally modified (folder level) | Review 2 diffs; parameters.md kept; declaration row v4.2 → v5.0 |
```

The Cluster column shows whether the file's cluster was activated in Step 3.5 (curation) and, for Final-production formats, which format-pair was selected.

For renames, also list the references found in Step 3:
```
References to `MyVoiceProfile_Skill` found outside skills/:
- CLAUDE.md L42: Skills table row
- CLAUDE.md L87: Writing style profiles section
- FOLDER_MAP.md L12: ...
(N references total)
```

**Wait for the user's approval per line.**

---

## Step 5 — Apply updates

For each approved operation:

**Rename target:** Rename the repo's file. Then treat the content comparison as one of the other categories below.

**Outdated — unmodified:** Replace the file's content with the staging version.

**Outdated — locally modified:** Show the three-way diff (old kit, repo's version, new kit). The user decides:
- **Accept kit version** — replace (local modifications are lost)
- **Merge** — Claude integrates the kit changes into the repo's modified version, preserving local customizations. Present the merged file for review before saving.
- **Keep repo version** — skip this file

**New in staging, not in repo:** Add if the file's cluster was activated in Step 3.5 (curation). Do not add otherwise. The decision was made in curation; Step 5 just executes.

**Cluster deactivated (file present in repo, cluster deactivated in Step 3.5):** Hard-remove the file from `skills/`. No soft-archive, no commented-out reference. Update CLAUDE.md's Skills table to remove the row (Step 7).

**A split `skills/` (the layout retired at v6.9):** before any other operation, move `skills/general_skills/`'s files and its `last_skill_update/` up into `skills/` and delete the empty folder; rewrite `KIT_FOLDER` to `skills/` and every `skills/general_skills/` path in `CLAUDE.md` and the repo's maps. A repo-only skill still in `skills/` is moved next to the work it serves once the user has ruled where it goes (`structure_conventions.md`, "Skills layout"); one with no ruling is asked, never moved by guess.

**Modules:** apply per the folder-level classification — a *land* copies the staged folder to the home (the traveling folder only — `corpus/` and `CHANGELOG.md` stay kit-side, and the maps are not copied: the home's and its subfolders' `FOLDER_MAP.md` are written empty in the form at the land and filled at Step 7.5 part 2, as any folder's; exempt file from its blank template, `corpus_inbox/` created labeled-empty; the card's `this copy` row written at Step 7.5 part 2); an *update* applies the per-file outcomes above inside the home, exempt file and maps untouched. Before replacing a repo's `MODULE.md` with the staged one, check its feedback slot (`slot: feedback`) for tagged entries (`[SKILL-FEEDBACK]`, `[CORPUS CANDIDATE]`) the kit copy does not carry and surface them — the same hazard as Step 8's CHANGELOG replacement; an entry that postdates the last sweep is lost otherwise (the rulebook is Step 7.5 part 2's `MODULE.md` bullet).

---

## Step 6 — Update references for renames

For each rename the user approved, update every reference identified in Step 3. Scan the whole repo, not just `skills/`. This includes the root `CLAUDE.md`, `FOLDER_MAP.md` files in any folder (or whatever the repo uses to describe its folders), task-specific skills, and redirect stubs.

Present the list of updated references to the user before committing.

---

## Step 7 — Update CLAUDE.md

After applying file changes:
- Update the Skills table in CLAUDE.md if any filenames changed
- Add rows for any new files that were added in this propagation (per the Step 3.5 curation — files added when their cluster was activated). **The curated-table branch:** a repo's skills table may be a full kit-files table or one curated on the kit-metadata axis — the `CHANGELOG.md`, the seven templates (`CLAUDE_template.md`, `STATUS_template.md`, `ONBOARDING_template.md`, `README_template.md`, `standing_documents_template.md`, `FOLDER_MAP_template.md`, `typed_index_template.md`), `gitignore_seed.md` and `PROJECT_SETUP.md` deliberately unlisted as a group. A full table gets the new row; a curated table is left alone, with the split stated in one line above the table ("kit metadata files are not rostered here"); where the repo rosters the templates in `ASSETS_INDEX.md`, the row goes there. Never add one kit-metadata row to a table that omits the group.
- Remove rows for files that were removed (per Step 3.5 — files removed when their cluster was deactivated, plus deletions from renames)
- Update the Cluster activations (current) block in STATUS.md to reflect the post-propagation state
- Update the `modules:` declaration rows (versions; the Step 2.6 backfill rows) and the Skills section's Modules roster block *(the frontmatter is the module set's one home; the STATUS.md Active modules line was retired at v6.5)*
- Write the Collaborators roster rows approved at Step 2.7 (onboarding and backfill rows) and update `USER_IDS` if the roster's id column changed
- Registration of the homes Steps 7.5 and 8.5 create is the root `FOLDER_MAP.md`'s skeleton block, regenerated by Step 7.5 from the manifest — no CLAUDE.md structure table exists to update any more (the section is a pointer to the root map; a table still present is retired form, handled at Step 7.5). Step 10 checks the block against disk. *(The per-home registration bullet an earlier kit version carried is subsumed: the block is rebuilt whole at every stop.)*
- If the repo's working conventions section has the legacy "generic-skill improvements trigger an improvement artifact" rule (added in v1.3, retired in v2.0.2), **remove it.** The session-end artifact path no longer exists; portable changes are picked up by the next discovery sweep run from your canonical skills repo.
- Update any other cross-references affected by renames or changes

---

## Step 7.5 — The conformance pass

A repo conforms to the kit at every propagation: every job the kit assigns a home has one home at the kit's path, and every kit-shaped file carries the template's form with the repo's content in its slots (`structure_conventions.md`, "Conformance: one home per job", the definition this step implements). The pass has four parts, run in order; the structure is mechanical, every judgment goes on one approval list, and nothing is moved, renamed or deleted on Claude's call. *(Replaces the v6.3 "Reconcile STATUS.md and CLAUDE.md against the templates" step, which backfilled missing sections and left form alone; a kit update found form drifting in every surface the kit shapes because nothing regenerated it, and homes created beside the folders already doing their job because nothing compared them.)*

**0. Read the manifest and the migration lines.** The tagged birth tree for the declared archetype (`research_setup_scaffold.md`; a NONE repo reads the universal lines only) with the carried spec; the **New homes** and **Retired premises** lines of every kit CHANGELOG entry between the repo's version and the staged one; the repo's root `FOLDER_MAP.md` (or, before one exists, its root folders and their maps). After the first full conformance pass, the New homes lines to read are only those newer than the repo's last stop. Where the repo carries `workspace/multisession_active_tasks/CONFORMANCE_ITEMS.md` (a campaign's ruled items for this repo, seeded from its charter's Part C seed), read it here: every `ruled` row is an instruction parts 1 and 2 carry out, never an item on the list; a `done early` row is verified against the tree and skipped; a row whose premise the tree falsifies is reported as changed and not run as written; the file is deleted in the propagation commit (Step 11) and its rows' outcomes go into the record (part 4).

**1. Structure.** From the manifest: create every `[U]` home absent, with its stub, and every `[P]` home under a present parent; test each `[E]` line's condition where it is mechanical (a funding folder holds an instrument) and propose the creation, sending a content-judgment condition to the list; never a `[J]` home. Presence before a condition is never drift. Then the checks that make existence insufficient: (a) the **same-job check** for every home a New homes line names — predecessor names, map descriptions, characteristic contents — every candidate to the list, the empty home created regardless, the new home's latent-homes or map line naming the candidate awaiting ruling; (b) every **unregistered root folder** gets one of the four readings (same job as a kit home; unplaced material, to staging; a unit missing its skeleton; a genuine extra, registered), proposed, the count of extras reported against the cap of two; (c) every **`_ex` slot** reported with a proposed resolution; (d) the **root-documents function check** on every root file outside the register (dissolve, migrate or delete, asked per file; a closed task's artifacts proposed for deletion); (e) the module homes confirmed tree-first (Step 2.6 already reconciled the set); (f) in a research repo, a line without a `Stage:` word gets one proposed from its folders, and a stage label off the closed vocabulary is mapped by the CHANGELOG entry that retired it (the research spec). A NONE repo runs (a) on the universal homes and (b) against its skeleton block, and skips archetype and typed-index checks.

**2. The kit-shaped files, rebuilt in template order.** For each file below, the template owns the form and the repo owns the content: regenerate the form, pour the content into the slots (sections where the template fixes headings; `slot` markers elsewhere; `kit` blocks regenerated whole), and put any content that fits no slot on the list — never dropped, never silently landed in the `unplaced` slot without being reported.
- **`CLAUDE.md`** (`CLAUDE_template.md`, v6.5 form; the template's fill rules live here, not in the template). **The frontmatter:** the declaration with the archetype's lines — research keeps `type`, `variant`; NONE keeps `type` alone; the `modules:` block only where a module is carried. **The top:** the one-line trailer (kit version, date) with any trailer stack rotated verbatim into `STATUS_ARCHIVE.md`, and the template's form comment kept — the one-line trailer is asserted, not only rewritten: a `CLAUDE.md` with no trailer at all gets one and the absence is reported; the template's own kit marker at its bottom (below the comment that names it) is never poured. **The sections, in template order:** a renamed template section poured into its slot, retired form dropped with its content checked against the kit's current home and asked where none exists. Slot by slot: *Project Overview* takes the project's facts every session needs (background, deliverables, people, vocabulary, tools, the repo's GitHub name); *How to start* takes the project's routing rows (a "routing," "how to navigate," "session opener," "never mix" section maps here); *Collaborators* is the roster in form from the Step 2.7 reconcile; the *Skills* tables regenerated from the curated set in the two-column form (file, When to use — the cell copied verbatim from the skill's `triggers:` frontmatter key, its one home (a path inside a `triggers:` string is written `<KIT_FOLDER>/<file>` in the kit, as in a skill body, so the verbatim copy resolves in either layout); the curated-table branch of Step 7 stands), the *Modules* roster only where a module is carried, *Project skills* always present with the repo's own workflow files rostered, and an inline project workflow with steps proposed for extraction into a file (an ask, never done on Claude's call); each *workflow section* present where its cluster is active — Paper Processing, Document Processing and Agent Research with Source material; Writing Protocol for Drafts and Note-Taking with Writing and deliverables; Document Format & Export with Final-production formats; Naming Conventions in every repo; where the STATUS Cluster activations block declares the section's skill declined ("active, less `<file>`"), the section keeps its heading and writes "not carried (STATUS cluster block)" in the pointer's place — in the three-part form (pointer, parameters, `### Project conventions`), the parameters' values kept and the label tables at the kit defaults unless the repo set its own, everything that restated the skill dropped; a section with nothing of the project's is written in its **short empty form** — the heading, the one-line pointer to the skill, the parameters at their defaults, an empty `### Project conventions` — never omitted (the structure is always there, so placement is never a guess; the every-turn cost is a few lines per section); the **Repo parameters** table (create if absent: `KIT_FOLDER` as `skills/`, `INDEX_FILES` off the typed indexes present, `PALETTE_FILE` off the palette file where the repo authored one, the `AGENT_OUTPUTS_*` rows off the folder; any parameter declared elsewhere moved in with a pointer left, the backfill dissolving the predecessor section (`## Skill Parameters` and its kin) in the same edit — never a second home beside the first; every derivable row (`KIT_FOLDER`, `INDEX_FILES`, `PALETTE_FILE`, the `AGENT_OUTPUTS_*` rows) is re-derived from the tree at every pass, and a declared value the tree falsifies is reported as *wrong*, never as *skipped: undeclared*; a parameter a skill reads that the table has no row for gets a row below the kit rows and is reported as a kit finding); the kit *Working Conventions* bullets brought to the template's current text, project bullets under `### Project conventions`, missing kit bullets added by name, and a project bullet that contradicts a kit bullet never overwritten — it is an ask, and the ruling behind it a kit finding; *Repository Structure* as the pointer to the root map (a structure table or tree there is retired form). **Placeholders:** a bracketed placeholder left unfilled is deleted (a placeholder row, a placeholder bullet), except a Repo parameters row, which takes `none` and stays, a workflow section's parameter bullet, which keeps the template's text (the short empty form above), and an empty `### Project conventions` slot, which stays as its heading. **Retired form the pass names** (each an ask with its content's home): a Parking Lot section (its items to `STATUS.md` Open questions, Part B's rule); a GitHub Access or Repo Access section (web-era residue; the access authority is `github_api_workflow_skill.md`); a Writing Style Profiles section (the two routing lines under the Voice table); a structure tree, a master index, or an index-system section (the root map, the archetype spec); a Skills table with a Purpose column. Then the **Retired premises** sweep — grep `CLAUDE.md` and `STATUS.md` for each retired premise and propose the rewrite of every live hit (historical records stay). **The length target** (`CLAUDE_template.md` v6.5), stated in **words** — lines stop tracking the reader's cost once a file is hard-wrapped — with lines reported beside: count the regenerated file twice, before and after the slots are poured; the first count is the kit floor for this repo's activation, computed at run time and never stated as a number: the word count of the current `CLAUDE_template.md` body, the kit marker excluded and the rows of clusters the repo does not carry removed, the pass reporting the repo's count beside it; the difference is the project content, and a project content over **1,500 words** (about 100 lines) is a finding for the user, never a cut.
- **`STATUS.md`** (`STATUS_template.md`, v6.5 form; the template's fill rules live here, not in the template). **The sections, in template order** — Current state with its three subsections, Open questions, Known issues, Cluster activations — each missing one added empty, `(none)` or `(never)`. **The header** rewritten in place to date and flag, its `Prior:` stack rotated verbatim into `STATUS_ARCHIVE.md`'s Headers section — the header protocol asserts the shape (one H1, one date-and-flag line, no banner) and rewrites whatever stands there to it, rather than repairing one line; the fixed archive line under it; the comment guidance regenerated whole; the Cluster activations block rewritten by Step 7 (five cluster lines and Last curated, in place — the Repo archetype, Active modules and Always-active lines are retired form, dropped, the frontmatter being the home). **Current state, the workstream form:** one entry per workstream named by its folder (the tracker names the unit per archetype: lines, a NONE skeleton's folders, plus `general` where the archetype has a spine, plus `repo`), in the root map's order, with the fixed fields (where it stands as of a date, Next, Waits on, Resume). A STATUS already in the form keeps every entry in place. **A STATUS in the log form** (dated entries per session under Current state, the pre-v6.5 shape) is poured once: the log rotates verbatim to the archive under its heading, and the entries are drafted from the folders, the plan files and the old narrative — one per workstream, dated today, with what the narrative says is next — and put to the user on the approval list as **an ask, never a silent pour** (the one place the pass writes new text; the campaign's charter pre-authorizes the rotation, not the entries). **Open questions** kept one per entry, named and dated; an entry that is an action becomes a proposed queue row, an entry already answered is proposed for rotation with its answer. **Known issues** kept; a fixed one proposed for rotation; a known issue or open question naming a kit skill or template with no `[SKILL-FEEDBACK]` entry behind it gets the entry written in the propagation commit, the STATUS entry pointing at it (the floor's same-commit rule, "One channel, many writers"); a pointer at a channel entry an earlier propagation cleared is rewritten to the kit record in your canonical skills repo, if you keep one, never left dangling. **Retired sections, each with its content's home:** *What this repo is* — its paragraph checked against `CLAUDE.md` Project Overview, anything Overview lacks proposed for it, then dropped; *Workflow mode* — its value moved to the `WORKFLOW_MODE` row of the Repo parameters table, then dropped; *Recent sessions* — rotated verbatim to the archive, whole; *Archived workstreams* — its rows rotated verbatim to the archive, once. **Extra sections** asked and mapped (an Archetype section to the frontmatter and the root map; Resolved and Follow-ups to rotation or the workdesk queue; Open branches to the entries' Resume fields; a misplaced Index audit heading folded into its subsection; a dated subsection under Current state to the entry it belongs to). **Placeholders:** a bracketed placeholder left unfilled is deleted, except the three fixed lines, which take `(none)` or `(never)`. Closed records rotated mechanically per the tracker's rule, verbatim, and a STATUS over the tripwire rotated without a ruling; distillation of live text never. **The length target** (`STATUS_template.md` v6.5), in words with lines beside: count the regenerated file twice, empty and poured; the kit floor is computed at run time and never stated as a number: the word count of the current `STATUS_template.md` body, the kit marker excluded and the lines of clusters the repo does not carry removed (the comment guidance included), the pass reporting the repo's count beside it; the project content over **1,200 words** (about 100 lines) is a finding for the user, never a cut — under the workstream form it means entries have outgrown their slots, and the tracker's outgrowth catch is the answer.
- **The standing documents** of `workspace/`, `workdesk/`, `feedback/` (`standing_documents_template.md`, v6.5 form; the template's fill rules live here, not in the template). Every one is written for Claude and its job is location — what the repo already holds, at the moment the user asks (the floor's function statement, "workspace/"); the pass creates each where missing from its body in the template and regenerates the form of each that exists. **The head** — the title in path form, the purpose line, the resting-state line — is rewritten to the template's text; a title in another form (`# Brainstorms`, `# Workdesk — pending-actions queue`) is retired form. **The catalog:** the table inside `slot: catalog` keeps its rows and takes the template's header row; an existing document with no catalog and files in its folder gets the header and one row per file or stem, **populated from the repo as best Claude reasonably can** (the file's title and date, the conversation or plan it pairs with, the deliverable it served) and written at the pass, reported in the ledger, never held as an ask: the user corrects a row when they notice it wrong in use, and what matters is that from the pass on the close-out keeps the catalogs current; a `packages/` folder's rows are drafted from its build scripts and, where a ledger exists, from the ledger's `sent` events, a send date the repo does not record left blank; the branch register's rows from the repo's branches (`git branch -a`), open ones included, and from a `BRANCHES_LOG.md` where one exists, which is then deleted in the same commit. **The notes slot:** prose an existing document carried beyond the head — a restated skill, a house "Governing skill" line, a "populated on demand" paragraph — is dropped where it restates the owning skill or the floor (reported by file, never silently) and kept in `slot: notes` where it says something of the repo's. **The skill's index** (the conversations index; the agent-outputs triple — `INDEX.md`, `LESSONS.md`, `WORKFLOW_SKIPS.md`, and a pass creates the three or none, never one of three): the header regenerated to the owning skill's current form inside the markers — a conversations index without the `Who` column where `USER_IDS` is defined gets it, and a `Who` column standing where `USER_IDS` is `none` is dropped at the pass, its one value kept in the row's text if it says something — and the rows and sections kept; a folder carrying both a `README.md` and the skill's `INDEX.md` keeps the index, folds the README's repo prose into the index's `notes`, and deletes the README in the same commit (an ask); a `LESSONS.md` entry flagged `Cross-project candidate: Y` with no matching `[SKILL-FEEDBACK]` entry in the repo's `skills/CHANGELOG.md` gets one, quoting the lesson's prompt response, so the next sweep carries it (`agent_research_verification_skill.md`, "Cross-project hoisting"). **The queue:** the title and one line, the table in its slot with the rows kept; everything above the table that restated the rules is dropped and reported. **The feedback seed:** the map's kit block regenerated whole from the template and the entry rows kept; its `Type:`/`Stage:` line and description are the `FOLDER_MAP.md` bullet's. **Placeholders:** the trailer line takes today's date and "regenerated at propagation"; an empty slot stays as its markers; a live "Empty = ..." claim anywhere in a standing document is retired form. **Length:** no target; a head is about sixty words, and a document far past that outside its catalog is reported.
- **Every `FOLDER_MAP.md`** (`FOLDER_MAP_template.md`, v6.5 form; the template's fill rules live here, not in the template). **Created** empty in the form where the leaf rule requires one and none exists (a map is born with its folder); a module home's maps among them — the repo's, never landed from the canonical copy (Step 3), so a map found with the module's relative title (`<module> (module home)`) or the kit's path as title is regenerated here like any other; a map found below the roots of `workspace/` or `workdesk/` is deleted, its one repo fact moved to the standing document's row (a package folder's note to the packages ledger row); a folder the scaffold created empty and that has no map (`general/papers/text/`, `summaries/`, `draft/`, `deliverables/`) gets its `leaf` map here, one pointer row at the index or the parent map, since the map is what persists the folder across a clone (the leaf rule exempts only a leaf born on content). **Form regenerated:** the title in path form (`root` for the root map); the slot row from the folder's place in the manifest and the declaration — `Kind: <word>` from the template's closed list, and for a research line `Stage:` from the existing header or, absent, proposed from the folders (the research spec's mapping of off-vocabulary labels) — replacing any `Type:`/`Stage:` or `Line:`/`Stage:`/`Spec:` header line — conformance of a map is tested by the presence of the slot row (`Kind:`), never by the absence of a named predecessor header, since a repo's own restructure may have written a third form; the kit blocks the kind carries regenerated whole from the manifest and disk — the skeleton from the present root folders with the manifest's job text (a NONE repo's bespoke lines drafted for approval at the first pass), the root documents from the root files with each index's job and the repo's own domain catalog once it passed the function check, the latent homes from the manifest's unborn `[E]` and `[J]` lines under the folder with the candidate from the New homes lines, the extras from the register; the catalog's header row regenerated as `| Path | What is here |` with the rows poured from the existing lists and tables and **populated from the folder's present contents as best Claude reasonably can, written and reported, never an ask** — a departed or retired entry's row dropped, a count or a date in a row dropped, a subfolder a typed index registers reduced to its pointer row, a `## Contents`, `## Work folders` or `## Cross-line pointers` heading dropped with its list poured; the description poured from the existing prose where it says what is here and what goes here (a line's current-shape opener and its working rules included; a bolded lead-in opening a paragraph, `**Purpose.**` or `**Line:** ...`, is part of the paragraph and pours with it, never read as a heading), prose that restates the owning skill, the spec or the floor dropped and reported (a legacy document migrated below a map is the case: its walkthrough and its rules go, checked against the skill first, its facts of the repo's go to the description or to index rows), anything else to `unplaced`, reported; one trailer line, a stack deleted. An orientation map at `workspace/`, `workdesk/` or `skills/` root is kept as `Kind: orientation` only where its description says something of the repo's; one restating the floor or the standing documents is deleted and reported. A description over about 150 words is reported, never cut; the count of maps created, regenerated and deleted is the pass's record.
- **The typed root indexes** and a repo's own registered catalog (`typed_index_template.md`, v6.5 form; the template's fill rules live here, not in the template). **Created** empty in the form where the spec's set names an index the root has no file for (the spec's list is the set; in a NONE repo `NOTES_INDEX` alone, the universal index, with the template's NONE sectioning line). **Form regenerated:** the title as the bare file name; the head rewritten to the template's three sentences for the archetype (the writer, the sectioning line for the declared archetype, the reading order), replacing any purpose line, placeholder sentence, "Holds:" line, maintenance rule or "Last updated" line; every table's header row regenerated as the template's row for that index under the `index` marker, every section heading of the archetype's form kept, or created, whether or not it has rows (a research line; the empty case is the heading and the header row); the rows poured from the existing tables and lists with the old columns **mapped by meaning** — Scope or Purpose to `About`, Location or Path or Links to `Where` or `Forms`, a status column to the state cell the kind carries, a `#` column dropped and any cross-reference by row number rewritten to the stem — and **populated from the folders as best Claude reasonably can, written and reported, never an ask**: a paper in the paper home with no row gets one with its `About` from the summary and both statuses blank where unknown, a product with an outline and no row gets one with its stage read off the files, a visual in `workspace/visuals/` with no row gets one, a note set in `writing_notes/` with no row gets one with its `About` from the file's head (a migrated set's row rewritten to its new path); a row for a departed file dropped and reported. **The two content cases are asks on the approval list**, since they move content: an index carrying content in place of pointers (a summary written below or inside a paper's row, an intake narrative in a materials row) is proposed for the pour into the paper's summary file or the line's map description, the row reduced to the template's; a paper registered in the materials index as well as the papers index loses the materials row. A repo's own catalog keeps its columns with `About` added and its head rewritten to the kit's three sentences with the repo's purpose sentence kept as the first; a lowercase catalog is renamed ALL_CAPS and its root-map line written. Head prose that says something of the repo's and fits no sentence goes to `unplaced`, reported; one trailer line, a `Created ... (skeleton)` or `Last updated` line replaced. The count of indexes created and regenerated, rows added from the folders, and content asks is the pass's record.
- **`README.md`** (`README_template.md`, v6.5 form; the template's fill rules live here, not in the template). The one repo file whose reader is a person, read on opening the repo to understand what it is for; the form is the name, one paragraph, one kit sentence. **Created** where missing; **the form regenerated:** the title written from the repo's name (the GitHub name in `CLAUDE.md`'s Project Overview, else the folder), the kit sentence pointing at `CLAUDE.md` and the form comment in the template's current text, the `unplaced` slot present and empty. **The paragraph** (`slot: what_this_repo_is_for`): an existing paragraph kept in the person's register — the existing README read for the one worth keeping, a subtitle or institution line folded into it; where none exists, **drafted from `CLAUDE.md`'s Project Overview in plain prose for a person, written and reported, never an ask** (the user corrects it in use); the paragraph and the Overview are twins, not copies — the Overview holds the facts every session needs, the paragraph the objective in a person's words — and a contradiction between them goes on the approval list. **Retired form, each dropped and reported with its content's home:** a structure tree or table (the root map; dropped, asked, as before); a root-files list or an index list (the root map's root-documents block); a pointer list to `STATUS.md`, the maps or the skills (the kit sentence; `CLAUDE.md` routes); a collaborator line or roster (`CLAUDE.md` Collaborators; the person's `ONBOARDING.md`); a conventions section (`CLAUDE.md` Working Conventions, checked against the kit's current text first; a project convention with no home there goes on the list); a repo-access section (`github_api_workflow_skill.md`); a date or version line (the kit version's home is `CLAUDE.md`'s trailer, the propagation's record the repo CHANGELOG entry). **Placeholders:** the bracketed paragraph placeholder never survives, the paragraph is always written. **Length:** the paragraph about 150 words, reported, never cut; the kit form is about ten rendered lines.
- **`.gitignore`**: the kit block seeded or regenerated; the repo's rules outside it untouched.
- **`ONBOARDING.md`** where a collaborator has one (`ONBOARDING_template.md`, v6.5 form; the template's fill rules live here, not in the template). The file is written for the person and read once, so the pass regenerates the form and never rewrites content. **The six parts, headings fixed, in template order:** the header (the Written line, in the join variant or the had-access-before variant; the **Review** line, added as "reviewed by the owner: <date>" where a review is recorded in the header or the queue, otherwise "draft, pending the owner's review" with a `workdesk/INDEX.md` row); What the task is; How this repo works (**the kit block regenerated whole** — the universal protocols in the template's current text, the `<id>`, `<Name>` and Merge-column slots filled from the roster; a pre-v6.5 document's four kit bullets replaced by it, its "where work stands, session by session" STATUS wording being retired form; then the repo's own bullets kept in the slot, except one that restates a kit bullet — staging, feedback, the queues — which is dropped and reported); The reading list (rows kept; a row without a what-to-take clause reported, never written); **Your assignment** (a "Where the work stands" heading renamed, its content kept with its date, the fixed closing line added; a document whose assignment content has since moved on is not refreshed — the workstream's `STATUS.md` entry is where the work stands, and a fresh assignment is a *Waiting on* row); Working with your Claude (**the kit block regenerated whole** — the list of what a collaborator's Claude does or asks, then the kit habits; a pre-v6.5 document's habits replaced by it, the "open every session" and "ask where it belongs" habits being in the block now; the repo's own habit kept in the slot). **The row:** a collaborator whose `LOG.md` is still empty gets the "read `ONBOARDING.md`" *Waiting on* row if their `INDEX.md` lacks it. **Placeholders:** a bracketed placeholder left unfilled is deleted. **Length:** no target; a person reads it once whole. The kit blocks are about 1,050 words; a filled document comes to about 1,750 to 1,950 words in the form, and a document far outside that range is reported, never cut.
- **`MODULE.md`** in every module home (`MODULE_template.md` in your canonical skills repo's `modules/`, v6.5 form; the template's fill rules live here, not in the template). The card is kit text with one per-copy row and one project slot, so the pass never pours it: **the kit block** (`kit: card`) is regenerated whole from the staged canonical copy, the `this copy` row written from the pair Step 2.6 detected for this home — the pair copied from `triggers` with its flavor, and the home resolved, a nested copy naming the parent's home (`nested:<parent module> -> funding/<parent module>/<nested module>/`); **the feedback slot** (`slot: feedback`) keeps its entries, surfaced first, an entry the module's record in your canonical skills repo, if you keep one, says was extracted dropped, the rest kept; **a pre-v6.5 card** (the table carrying a `corpus` field, a "What this module does" paragraph, a "Changelog and feedback channel" section carrying the versioned history) is replaced whole — the history is the kit's (`modules/<name>/CHANGELOG.md` in your canonical skills repo, never in a copy), the paragraph the skill's, and only its tagged entries move into the slot; a card found with prose outside the block and the slot has that prose reported, never kept. **Placeholders:** none survive — `this copy` is always written. **Length:** about twenty lines with an empty slot; a copy far over that with an empty slot is a hand edit of the block, reported.

**3. The approval list.** One batched presentation: the same-job candidates, the root readings, the `_ex` resolutions, the function-check results, the no-slot content, the extra STATUS sections, the stage proposals, the content-judgment `[E]` conditions, the length findings. The user rules; the step proposes. In a wave the list is the repo's part of the Stage 2 gate; unruled items fall back to the charter's pre-authorizations or are skipped and surfaced, never guessed.

**4. The record.** The pass is recorded per repo in the wave ledger (created; migrated; ruled different-job; extras reported; asks pending; the `CONFORMANCE_ITEMS.md` rows by outcome where one stood) and, for a single-repo run, in the propagation commit message. Everything lands in the propagation's atomic commit (Step 11). The tracker's bootstrap section (`project_tracker_skill.md`, "Bootstrap during Part C") names this step as the STATUS half.

---

## Step 8 — Update the repo's skills/CHANGELOG.md

Replace the repo's `skills/CHANGELOG.md` with the one from staging. This records which kit version the repo is now on — future Part C runs read this. The tagged entries this clears were collected at the kit update; their record is your canonical skills repo's, if you keep one, and a live surface that pointed at one is repointed by Step 7.5.

---

## Step 8.5 — Scaffold `workdesk/`, `feedback/`, `writing_notes/` and the workspace folders

The universal homes are labeled-empty homes created up front (`structure_conventions.md`): the `workdesk/` scaffold, the `feedback/` home, the `writing_notes/` home, the six universal `workspace/` subfolders, and the curated homes the archetype adds. A repo propagated from an older kit will be missing some — bring it up to the full set, migrate its legacy to-do homes into the workdesk queue and its legacy notes homes into `writing_notes/`.

**1. Scaffold `workdesk/`** per `structure_conventions.md`: `INDEX.md` (the queue, no rows), `admin/` and `postits/` each with its `README.md`, and `collaborators/` with its `README.md` — every body from `standing_documents_template.md` (`structure_conventions.md`, "Collaborators" — the per-person folders inside are created on join, never here; a repo that already carries the folder keeps it as is). A repo carrying the predecessor `workdesk/notes/` (every repo before v6.5) has it **renamed to `postits/`** (`git mv`, contents untouched, the README regenerated by Step 7.5), a collaborator's `notes/` likewise; the reference sweep in step 2.5 covers the old path.

**2. Scaffold `feedback/`** per `structure_conventions.md` ("`feedback/` (every repo)"): the top-level home, sibling of `workspace/` and `workdesk/`, present in every repo including NONE, with its seeded `FOLDER_MAP.md` from `standing_documents_template.md` (the kit block stating the record/wait/link/version split at the point of use; the catalog of entries across people). Per-person subfolders are born on the first feedback, never here; a repo that already carries the folder keeps it as is.

**2.5. Scaffold `writing_notes/` and migrate the notes homes** per `structure_conventions.md` ("`writing_notes/` (every repo)"): the top-level indexed-notes home, sibling of `workspace/`, `workdesk/` and `feedback/`, present in every repo including NONE, with its `FOLDER_MAP.md` written empty in the form of `FOLDER_MAP_template.md` (kind `leaf`, the one pointer row at `NOTES_INDEX`) and `NOTES_INDEX.md` at root where the root has none (a NONE repo's only index; the form in Step 7.5 part 2). Then the **migration**, the same-job check made concrete for this home: every existing note set moves, nothing is left in a legacy home. Check for each of: research's `general/notes/` (every research repo before v6.5), a `workspace/notes/`, a bare root `notes/`, and any folder the root map or a `CLAUDE.md` names as the notes home. For every file found, propose a per-file disposition on the approval list — *a note set* (a line of thinking, indexed or citable) → moved whole into `writing_notes/`, a subject subfolder kept as one when the set spans files, its `NOTES_INDEX` row written or rewritten to the new path (Step 7.5 part 2); *a post-it note* (written for the user themselves, not feeding a deliverable) → `workdesk/postits/`. On the user's approval, move the files (`git mv`) and **delete every emptied legacy home in the same propagation commit**, its `FOLDER_MAP.md` with it; an empty legacy folder is deleted without a proposal round. **Then sweep the repo for references to the retired homes** — root `CLAUDE.md`, `STATUS.md`, every `FOLDER_MAP.md`, every typed index, repo-local skills, and the drafts and outlines that cite a note by path — for `general/notes`, `workspace/notes`, `workdesk/notes` and the path of any other reconciled home; repair live references to the new path and leave historical records untouched, the repair/leave triage being `finish_session_skill.md` Step 1b's. A repo with no legacy home gets the empty folder and index and nothing else.

**3. Bring `workspace/` up to the full set its archetype requires:**
- **Every repo (NONE included):** `claude_conversations/`, `brainstorms/`, `multisession_active_tasks/`, `staging/`, `packages/`, `branch_logs/`. (`to_do/` is no longer among them — see step 4.)
- **Wherever the owning skill is active** (the curated set in `STATUS.md`'s Cluster activations; archetype repos by default, per the `research_setup_scaffold.md` birth tree, a NONE repo the day the skill is curated in): `agent_outputs/` (`agent_research_verification`), `visuals/` (`visuals_workflow`).

For each folder in either set that does not already exist, create it with its **standing document**, the body copied from `standing_documents_template.md` (the floor's table names the document and its kind per folder; the skill's index bodies are in `repo_conversations_skill.md` and `agent_research_verification_skill.md`, which the template points at) — the document is the folder's lookup surface *and* what persists it in git (git and the Contents/Trees API track files, not bare directories — see the Appendix), so it survives task completion and the folder never collapses to empty. Catalogs and index tables start with their header row and no rows. **Never lose content:** an existing standing document is not overwritten here — its *form* is regenerated by Step 7.5 with the repo's rows and notes kept in their slots — and folder *contents* are never created or touched. Also make sure the root map's latent-homes block carries the `quarantine/` line (`structure_conventions.md`: event-born on the first held item, never scaffolded).

**4. Migrate the legacy to-do homes.** Check for each of: `workspace/to_do/` (v4-era), `general/to_do/` (pre-v4 research repos), and any equivalent arrangement the repo grew (a root `TODO.md`; Part B's audit may have flagged one). For every item found, propose a per-item disposition — *waiting on the user* → a `workdesk/INDEX.md` queue row (Action and Artifact-where filled from the item); *deferred Claude action* → a `STATUS.md` Current-state entry; *done/stale* → retire. On the user's approval, write the rows and **delete every legacy home in the same propagation commit** — exactly one place for pending actions survives the run. Empty legacy folders are deleted without a proposal round.

**Then sweep the repo for references to the retired homes.** Grep the repo-side files — root `CLAUDE.md`, `STATUS.md`, every `FOLDER_MAP.md`, repo-local skills — for `workspace/to_do`, `general/to_do`, and the path of any reconciled `TODO.md`. Repair live references to point at the queue; leave historical records (saved conversations, CHANGELOG entries, archived docs) untouched — the repair/leave triage is `finish_session_skill.md` Step 1b's. A deleted home with surviving pointers is the same defect this migration exists to prevent; the sweep rides the same propagation commit.

These additions land in the propagation's atomic commit (Step 11).

---

## Step 9 — Refresh the `skills/last_skill_update/` snapshot

After all file updates in `skills/` have landed (Steps 5–8), refresh the snapshot subfolder so it byte-matches the active `skills/`. The snapshot tracks the curated state of `skills/`, not the full kit — it's what the next kit-update run compares against.

Operation:
1. If `skills/last_skill_update/` does not exist, create it.
2. Replace the entire contents of `skills/last_skill_update/` with a copy of the active `skills/` files (excluding `last_skill_update/` itself — don't recurse).
3. Both folders should now be byte-identical at the file level.

Why this step exists: future kit-update runs compare each repo's active `skills/` against this snapshot. If the snapshot is stale, the diff produces noise. Refresh-from-active means the snapshot represents *what this repo last received and decided to keep* — not *what the kit happened to hold at the time*. So if the user declined a specific file in Step 5, the snapshot reflects their choice, and the next update run won't keep flagging the absent file as "missing from current."

Note: the snapshot is read-only between propagations. The user and Claude only edit files in active `skills/` during normal work; `last_skill_update/` is touched only by Part C runs.

**Module baselines.** For each module in the repo after Steps 5–8, refresh `<home>/last_module_update/` the same way from the module's active home: text files only, excluding the exempt file, every `FOLDER_MAP.md` (the repo's, never the module's), `corpus_inbox/`, and the baseline itself; a nested module's baseline sits inside the nested home, not the parent's. This is what the next sweep compares each module against.

---

## Step 10 — The audit pass at propagation (added v2.0.4 as the housekeeping pass; renamed at v6.8)

Before the atomic commit, run the audit pass at propagation — the subset of `repo_audit_skill.md`'s checklist listed below — to make sure the rest of the repo is internally consistent with the updated `skills/`. Skill propagation can leave stale references, missing index entries, and navigation tables that no longer reflect reality. Catching this here means the propagation commit ships a *coherent* repo, not just an updated `skills/` folder surrounded by stale infrastructure.

**Scope: infrastructure only.** The pass checks repo infrastructure files (root `CLAUDE.md`, `FOLDER_MAP.md`, `README.md`, `PAPERS_INDEX.md`, navigation tables in folder-level `FOLDER_MAP.md` files, repo-specific task skills under non-`skills/` paths). It does **not** modify deliverables (the paper homes, the drafts, the extracts and summaries). Deliverables are work product; the pass only checks that infrastructure references *to* deliverables are accurate.

**Checklist.** Run all of these against the post-propagation repo state:

1. **Root `CLAUDE.md` — skill table consistency.** Every skill in `skills/` either has a row or has been intentionally excluded by the user. No rows for files that don't exist in `skills/`. Cross-references in working conventions and trigger maps point to files that exist.

2. **The root `FOLDER_MAP.md` — the skeleton block.** Every root folder on disk is in the skeleton block or the extras register, and every folder the block names exists. A root folder in neither is a Step 7.5 reading that was missed.

3. **`README.md` — the form.** The name, the paragraph in its slot, the kit sentence and the form comment in the template's current text, the `unplaced` slot; a folder tree or table in it is drift (the root map holds the structure), and any of the retired forms Step 7.5 part 2 names (a root-files or pointer list, a collaborator line, a conventions or repo-access section, a date or version line) is a residue of the pass.

4. **Repo-specific task skills (under non-`skills/` paths).** Their own `FOLDER_MAP.md` and any internal references stay consistent with their content. References *from* repo-specific skills *to* generic skills point to files that exist.

5. **Indexes — `PAPERS_INDEX.md`, or whatever the repo uses.** Files mentioned exist. Files that exist in their respective folders are mentioned (or intentionally omitted — e.g., archived or excluded items). Note: index *content* (whether a paper has been read, status labels, etc.) is not the pass's concern; only the structural presence of entries.

6. **Folder-level `FOLDER_MAP.md` files.** Any navigation tables or file lists in these files match folder reality.

7. **Skill-to-skill cross-references inside `skills/`.** If a skill mentions another skill by filename, the referenced file exists in `skills/` (or in `last_skill_update/`). This is a sanity check on the propagation itself, not on the repo — but cleanest to run here.

8. **Module consistency.** The `modules:` declaration rows and the Modules roster block name the same set as the `MODULE.md` files on disk *(a STATUS.md Active modules line is retired form since v6.5, dropped at Step 7.5)*, with matching homes and versions, and each card's `this copy` row names the pair whose resolved home is the file's own folder; every module home has its `last_module_update/` and a labeled-empty `corpus_inbox/`.

9. **Conformance-pass residue.** Every `[U]` home of the manifest exists; every marked file carries its markers and its `unplaced` slot is empty or reported; no `STATUS.md` or `CLAUDE.md` header carries a `Prior:` stack; no map carries a `Type:`/`Stage:` header line or a trailer stack; README carries no structure copy. Anything found here is a Step 7.5 miss, fixed in the same commit (`repo_audit_skill.md` Check 14 is the on-demand form).

**Proposed fix vs. requires decision.** Two categories; neither is applied before the user's go:

- **Trivially-fixable** (proposed as one list and applied on the user's go, in the same atomic commit as the propagation; on a wave, one list per repo, their go per repo or for the batch): a stale name reference to a renamed file (apply the rename); a clearly-deleted skill mentioned in CLAUDE.md's table (remove the row); a missing skill row in CLAUDE.md's table for a file that exists in `skills/` (add the row).

- **Requires-decision** (surface for the user, do not commit until they decide): an index entry that *might* be stale or *might* be intentionally minimal; a deliverable mentioned that doesn't exist (could be deleted, could be a typo, could be planned-but-not-created); any structural change to navigation that's larger than a renaming.

**Reporting format.** Produce a brief report of the pass:

```
Audit pass at propagation — N findings:
  Proposed, trivially fixable (M):
    - <file>: <what was fixed>
    - ...
  Requires decision (K):
    - <file>: <what was found, options for how to resolve>
    - ...
```

If there are zero findings: report "Audit pass at propagation — clean." Proceed to Step 11.

If there are trivially-fixable items: apply them on the user's go and include them in the atomic commit. Proceed to Step 11.

If there are requires-decision items: pause and let the user decide each one. Apply their decisions, then proceed to Step 11. **Do not commit until requires-decision items are resolved or explicitly deferred.**

---

## Step 11 — Commit and clean up

One atomic commit — plain git, pushed (per `github_api_workflow_skill.md`'s Cowork branch) — covering:
1. All file updates in `skills/`
2. Renamed files (old path deleted, new path added)
3. Updated references in the repo's own documentation (from Step 6 rename pass)
4. User-approved trivially-fixable items from Step 10
5. User-approved requires-decision items from Step 10
6. Updated `CLAUDE.md`
7. Updated `skills/CHANGELOG.md`
8. Refreshed `skills/last_skill_update/` snapshot (full contents)
9. Module homes landed or updated (Step 5), their refreshed `last_module_update/` baselines (Step 9), and the `modules:` declaration rows (Step 2.6); collaborator folders scaffolded and roster rows written (Step 2.7)
10. The conformance pass's output (Step 7.5): homes created with their stubs, migrations the user approved, every kit-shaped file in its regenerated form (`STATUS.md` in the workstream form, the root map, README, `.gitignore`, the maps), rotations into `STATUS_ARCHIVE.md`; the propagation's own record is the repo's `skills/CHANGELOG.md` entry (Step 8) and this commit message
11. **Delete the `skills/pending_vX.Y/` staging folder**, `modules/` included — its job is done

Commit message:
```
Update skills kit from v[A.B] to v[X.Y]

- [file]: [action — replace / merge / rename / ...]
- [file]: [action]
- Updated N references to renamed files across repo
- Audit pass at propagation: M approved fixes, K user-approved adjustments
- Refreshed skills/last_skill_update/ snapshot to v[X.Y]
```

Present the commit summary to the user showing what was applied, what was skipped, and any new files they chose to decline.

---

## Multi-repo waves — the parallel-agent protocol

When a propagation — or any Part-C-shaped multi-repo change (kit-wide renames, wording sweeps, cascaded convention changes) — targets several repos in one campaign, run it under the five-stage protocol below instead of the interactive one-repo mode. The interactive mode stays the default for single-repo runs. **Environment: Cowork only** — the protocol reads and writes many local clones; a claude.ai web session cannot run it (Part C's Environment line governs).

**Stage 1 — Pre-flight (read-only, parallel).** One agent per repo, cheap model. Each reports: sync state (clean tree, ahead/behind after fetch), declaration present, legacy homes, cluster activations, module triggers present / modules found (`MODULE.md`) / modules declared — detected **tree-first** in every repo, the wave order's roster being a hint only (Step 2.6) — collaborators on GitHub / in the roster / with folders (Step 2.7), the conformance pass's list for the repo (Step 7.5 part 3: same-job candidates, root readings, `_ex` slots, no-slot content), the repo's `CONFORMANCE_ITEMS.md` where one stands, each row reported against the tree as still present, fixed or changed (Step 7.5 part 0), anomalies. No agent writes anything. A dirty or diverged repo is pulled from the wave for manual handling — never auto-resolved.

**Stage 2 — One batched gate (the user).** A single presentation: per-repo table, curation proposals, the collaborator reconcile table (Step 2.7), the conformance pass's list per repo (Step 7.5), everything requiring a ruling. The user rules once for the whole wave. **Fallback for unruled items:** they fall back to whatever the campaign's charter explicitly pre-authorizes; absent a pre-authorization, they are skipped and surfaced in the close report — never guessed. (The substance of any pre-authorization is campaign content: it lives in the campaign's charter, not here.)

**Wave sizing.** No numeric cap on parallel executors — the binding constraint is the gate, not the execution. Size and group waves (e.g., by archetype) so the Stage 2 presentation stays reviewable in one sitting. (The verification stage, not wave size, is the safety mechanism.)

**Stage 3 — Execution (parallel).** One repo = one agent = one atomic commit + push, approved package/work-list only. Stop rules, binding: never force-push; never resolve conflicts; anything unexpected → skip that repo and report, continue the others. Agents write only inside their assigned repo; the clone of your canonical skills repo is read-only for all wave agents.

**Stage 4 — Independent verification (parallel, different agents).** Never the executor. Checks: commit matches the approved work (renames R100 where content must not change), cascade completeness (grep old tokens — hits only in historical surfaces), push confirmed (HEAD == origin), held items untouched; for propagation waves, Step 10's audit pass at propagation is the per-repo backstop. Failures surface; they are never silently fixed — repairs are small follow-up commits, each named in the ledger.

**Stage 5 — Ledger close (one commit, your canonical skills repo).** Manifest/worklist status per repo, the conformance pass's record per repo (created; migrated; ruled different-job; extras reported; asks pending; the conformance items' outcomes — Step 7.5 part 4), the campaign record, and the next session's handoff.

**Model mix.** Judgment (orchestration, gate compilation, curation proposals, adjudication, canonical-wording drafts) on the strongest available model; mechanical stages (1, 3, 4) delegable to a cheaper model. Verification agents are always distinct from executors.

**Run lessons (binding, not advisory):**
- The Step 9 snapshot refresh must cover **repo-local files inside the kit folder** (for example, a repo's own `skills/FOLDER_MAP.md`).
- **STATUS freshness headers are part of the close** — advancing them is the executor's job, checked at verification.
- Case-only renames on a case-insensitive filesystem need the **two-step `git mv`** (via a temp name); binaries must land byte-identical (R100).
- Historical surfaces (CHANGELOG entries, STATUS session logs, saved conversations, archive snapshots, demoted catalogs, a dated handoff or carryover record living with the work) are **never edited** in a wave; old names there are the record.
- **One session per clone, explicit paths only.** Two sessions in one clone share the index, HEAD and the working tree; a landing commit stages explicit paths and never `git add -A`, close-outs run one at a time, and a second task in an active clone gets its own session or waits (`github_api_workflow_skill.md`, "What actually collides").
- A **roster is a hint, the tree is the fact**: module triggers, universal homes and same-job candidates are read off every repo's tree, never off the wave order's list of which repos "have" them.

---

## Common pitfalls (added v2.0.2)

These are mistakes encountered during real propagations. Read these before starting; they're cheap to avoid if you know about them and annoying to recover from if you don't.

- **Empty-file commits when adding new files.** A copy that takes only the files that differ skips additions; load every staged file before Step 5.

---
---

# Appendix: Full Skills Kit Inventory

For reference, these are all the files in the generic skills kit. When setting up a new project (Part A), integrating into an existing repo (Part B), or propagating updates (Part C), this is the complete list of files that may be copied to `skills/`.

Grouped by functional cluster, matching the structure used in `CLAUDE_template.md`'s Skills section and the Phase 4 (Skills Activation) menu above. The canonical roster is `CLAUDE_template.md`'s **eight** Skills-section clusters; **"Meta and templates" directly below is an Appendix-only inventory grouping** — the kit's meta files, which ship with the always-active group — not a ninth cluster, and it never appears in curation. Modules (the shared-module tier) are not inventoried here: they are folder packages, not kit files, and their registry is `modules/MODULES.md` in your canonical skills repo.

### Meta and templates

| File | Type | Purpose |
|---|---|---|
| `PROJECT_SETUP.md` | Meta | This file — project setup and skill integration. Ships in the always-active group to every repo (informational reference, not active workflow). |
| `CLAUDE_template.md` | Template | Blank CLAUDE.md template. Ships in the always-active group to every repo (each repo's actual root `CLAUDE.md` is generated from this template at setup). |
| `CHANGELOG.md` | Meta | Version history for the skills kit (copied to repos' `skills/` so each repo knows which version it's on) |
| `STATUS_template.md` | Template | Template for the per-repo `STATUS.md` file generated at bootstrap |
| `ONBOARDING_template.md` | Template | Template for a collaborator's first document, `workdesk/collaborators/<id>/ONBOARDING.md` — written for the person, six parts, by the owner's session when a person joins; presented by their Claude on the "read `ONBOARDING.md`" queue row (`structure_conventions.md`, "Collaborators"). Ships in the always-active group to every repo |
| `README_template.md` | Template | Template for the repo's `README.md` — the one repo file whose reader is a person, read on opening the repo to understand what it is for: the name, the what-this-repo-is-for paragraph (the project slot), one kit sentence pointing at `CLAUDE.md`, the `unplaced` slot; no structure copy, no pointer list, no roster; created at setup, regenerated in form at every propagation (Part C Step 7.5 part 2, the fill rules). Ships in the always-active group to every repo. Added v6.4; cut to the one job at v6.5 |
| `standing_documents_template.md` | Template | The body of every standing document of `workspace/`, `workdesk/` and `feedback/` — the head, the catalog or the label, the skill's index by pointer, the queue, the feedback seed's kit block — copied at birth and regenerated in form at every propagation. Ships in the always-active group. |
| `FOLDER_MAP_template.md` | Template | The form of every `FOLDER_MAP.md` by kind of folder — the slot row, the four kit blocks, the one catalog header, the orientation form — written empty at the folder's creation and regenerated in form at every propagation. Ships in the always-active group. |
| `typed_index_template.md` | Template | The form of every typed root index and of a repo's own registered catalog — the three-sentence head with the writer named, the header row per kind with `About` in every row, the `index` and `unplaced` markers, one trailer — created empty by the scaffold and regenerated in form at every propagation. Ships in the always-active group. |
| `gitignore_seed.md` | Meta | The kit-owned block of the repo's `.gitignore` (package binaries and zips, Python and Node residue, OS files), written at setup and regenerated at every propagation between its marker lines. Ships in the always-active group to every repo. Added v6.4 |

### Source material: reading and processing

| File | Type | Purpose |
|---|---|---|
| `materials_processing_skill.md` | Skill | Paper processing — Step 0 triage and shared infrastructure (prerequisites, folder structure, status framework vocabulary, lookup, project setup). Routes documents to Protocol A or B |
| `paper_processing_academic_skill.md` | Skill | Paper processing — Protocol A (academic-style papers). Per-document workflow: rename, extract, summarize with thesis/methodology/findings/relevance, BibTeX `@article`/`@unpublished`, Claude status |
| `paper_processing_institutional_skill.md` | Skill | Paper processing — Protocol B (institutional-style reports). Per-document workflow: institutional rename, extract with acronym/box preservation, synthesized-findings summary, BibTeX `@techreport`/`@book`/`@inbook`, Claude status |
| `document_processing_skill.md` | Skill | Document processing pipeline for operational and institutional documents (rename, extract, summarize, classify, index, cross-reference) |
| `agent_research_verification_skill.md` | Skill | Deep-research-agent workflow: prompt drafting, raw-output filing, link extraction, hand-off to papers protocol, verification of claims against retrieved originals, INDEX.md tracker, LESSONS.md for prompt-engineering compounding. **Core principle: agent outputs are NEVER directly citable — only the verification document is.** |
| `own_document_verification_skill.md` | Skill | Verification of a document written by the user or a collaborator against the repo's processed sources — intake fork (co-produced vs. external), fresh-session claims extraction, do-not-read insulation, inherited claim-verification core, coverage report with the user's triage rulings, tiered change list read-only on the draft |

### Writing and deliverables

| File | Type | Purpose |
|---|---|---|
| `writing_skill.md` | Skill | Writing workflow triage (routes to Protocol 1 or Protocol 2) + shared content: how the two protocols interact, project-setup parameters |
| `writing_notes_skill.md` | Skill | Writing workflow — Protocol 1 (reading and note-taking as coupled operation; fully interactive; always on `main`) |
| `writing_drafting_skill.md` | Skill | Writing workflow — Protocol 2 (drafting on a branch; planning loops, one-pass drafting, compiled outline + divergence table; 10k-word scale check, hierarchical naming, assembly cycles) |
| `visuals_workflow_skill.md` | Skill | Visuals embedded in markdown deliverables — sketch in markdown, review, SVG generated post-merge; invoked from drafting; consumes the project's color palette; home `workspace/visuals/` |

### Voice and style

The kit ships **no** personal voice profiles — a voice profile is personal by
definition, so this is a bring-your-own cluster: you author your own profiles
with `skill_authoring_skill.md` and they live here alongside the translation
pair below, curating and propagating like any other file.

| File | Type | Purpose |
|---|---|---|
| `translation_review_skill.md` | Skill | Spanish translation review — naturalness pass + correction capture (companion: `translation_corrections_log.md`) |
| `translation_corrections_log.md` | Record | Append-only Spanish corrections log (unnatural → natural → why); local pairs are merged back into your canonical copy, never silently dropped at propagation |

### Final-production formats

The kit ships only the generic academic pair. Branded or institutional formats
(a house Word template, an institutional LaTeX note, a team deck) — together
with their preambles and any logo or background assets — are bring-your-own:
author them with `skill_authoring_skill.md` and treat each as one more
format-pair in this cluster.

| File | Type | Purpose |
|---|---|---|
| `academic_paper_latex_skill.md` | Skill | Academic paper LaTeX workflow (working papers, journal submissions) |
| `academic_paper_preamble.tex` | Code | Academic LaTeX paper preamble (copy-paste template; a color palette is defined for figures/TikZ only — document chrome is academic); paired with `academic_paper_latex_skill.md` |
| `latex_round_trip_skill.md` | Skill | The review round trip for a paper whose live LaTeX source is edited outside the repo (Overleaf, co-authors): the review copy regenerated each round, the apply register (line number, original text, proposed text) the user applies by hand, the refresh read by diff; routes events to `product_ledger_skill.md`; ships with the LaTeX paper pair |
| `academic_slides_skill.md` | Skill | Academic presentation slides (Beamer/Boadilla, conference talks, seminars) |
| `academic_slides_preamble.tex` | Code | Academic Beamer slides preamble (copy-paste template; colors defined inline); paired with `academic_slides_skill.md` |
| `design_deck_reconciliation_skill.md` | Skill | Placing and reconciling a slide deck authored in a design tool outside the repo against the repo's own version of the same content — intake from staging, `_DESIGN` naming, layout-aware mirror extraction, the slide-level map (splits, design-only slides, reordered blocks, drift), divergence-versus-defect, rulings to `product_ledger_skill.md` (copied with any slides format-pair, or on demand; added v5.1) |
| `extract_design_deck_mirror.py` | Code | Layout-aware .pptx-to-markdown mirror extractor; parameterized to run against any deck; paired with `design_deck_reconciliation_skill.md` |

### Shared assets

Bring-your-own. The package ships no palette or logo assets; a project that authors a palette file lists it here and in `CLAUDE.md`'s Shared assets section.

### Repo and session infrastructure

| File | Type | Purpose |
|---|---|---|
| `skill_authoring_skill.md` | Skill | The meta-skill: how to author a new skill that fits the kit's conventions. Covers (1) general principles and conventions of the kit (naming, frontmatter, decomposition, cluster structure, last-updated marker discipline), (2) when to write a skill, (3) what a skill file contains, (4) workflow for drafting with Claude, (5) the downstream lifecycle (a skill written in one repo, folded back into your canonical kit copy, then propagated onward). Every new skill is born project-local; cluster placement is decided when it is folded into the canonical copy, not at creation time in the content repo |
| `skills_curation_skill.md` | Skill | The per-propagation per-cluster curation workflow. Codifies the cognitive contract (cluster-level proposal, free per-skill decision — no all-or-nothing rule; Final-production format-pairs are the natural sub-grain) and the cluster completeness invariant (an activated cluster's dependencies must be on the always-active group or in the same cluster). Used at all three propagation points (Part A new-repo setup, Part B existing-repo integration, Part C update propagation), with signal sources varying by point (questionnaire / existing-repo content / STATUS.md + commits + conversations — explicitly NOT current `skills/` folder contents) |
| `project_tracker_skill.md` | Skill | Defines `STATUS.md` as the repo's project-level tracker (session-start check, session-close mandatory update, freshness check, bootstrap, Pending re-integrations subsection) |
| `finish_session_skill.md` | Skill | Housekeeping, the session close — five-step sequence wiring together STATUS.md update, conversation save (conditional), branch disposition (conditional), and uncommitted-work check; does not duplicate the procedures in the canonical skills, only sequences them |
| `writing_branch_skill.md` | Skill | Ephemeral, single-document review branch (bracketed comments + direct edits); invoked by `finish_session_skill.md` for branch disposition at session close and by `writing_drafting_skill.md` for review cycles during drafting. In the always-active group because `finish_session_skill.md` is always-active and invokes it as a required action (cluster completeness invariant). |
| `exploration_branch_skill.md` | Skill | Long-lived, isolated exploration branch for work whose purpose is to test whether a `main` claim holds; reached from `brainstorming_skill.md`'s purpose-triage or a folder→branch promotion; finalized via the review→reconcile→route→record+delete protocol. In the always-active group (added v4, placed with `writing_branch_skill.md`). |
| `multisession_task_skill.md` | Skill | The multi-session carryover — a per-task carryover doc (`workspace/multisession_active_tasks/MULTISESSION_CARRYOVER_<task_stem>.md`) carrying one task across the sessions it takes to finish when resource limits force the split; a two-question gate decides carryover-vs-prompt; worklist-mimic format; folded into `STATUS.md` and deleted at completion. In the always-active group because its home is defined in `structure_conventions.md` for every repo (added v4). |
| `workstream_plan_skill.md` | Skill | The workstream plan file — `<stem>_PLAN.md` living with the work: required sketch, "we are here" re-entry, lookup surfaces carrying pointer + one-line position. Plain mode (ordinary full-context sessions) is the default; scoped mode (separate sessions with controlled reading scopes, blind-session prompts cut from the plan) is the gated upgrade. In the always-active group; ships with its companion asset. |
| `BLIND_SESSION.md` | Note | Companion asset to `workstream_plan_skill.md`'s scoped mode (not a skill): the survival kit a blind session reads instead of `CLAUDE.md` — reading rule, minimal conventions, contamination declaration, step-report format. Ships wherever `workstream_plan_skill.md` ships (added v4.2). |
| `product_ledger_skill.md` | Skill | The product ledger — `<stem>_LEDGER.md` living with the product: which representation is current, where they diverge, what has been sent, presented, or decided; intake restricted to the events git cannot see; representations as a tree with named parents; both-sides divergence stamps; orthogonal to `workstream_plan_skill.md` (plan tracks work, ledger tracks artifacts). In the always-active group — born on use, universal (added v5.1). |
| `repo_conversations_skill.md` | Skill | Save, index, and retrieve substantive Claude↔user conversations in a repo (transcript format, INDEX.md, tag vocabulary) |
| `repo_audit_skill.md` | Skill | The repo audit: three-mode infrastructure consistency check across a content repo (report-only / repair / index-audit) |
| `github_api_workflow_skill.md` | Skill | The repo-access authority: environment branch first (Cowork/local clone → plain git and gh; claude.ai web → the REST API recipes — Contents API single-file, Trees API atomic multi-file, branch recipes, safety rules); owns the parallel-session / mixed-environment hygiene convention |
| `cross_repo_import_skill.md` | Skill | Cowork-only import of already-processed material from another repo: reads the source repo's local clone (read-only, synced first) into `workspace/staging/`, selects keep/drop/what-must-come-too in staging before placement, hands off to the repo's normal placement rules, empties staging. Staging home/lifecycle in `structure_conventions.md`. In the always-active group — universal, any repo (NONE included), fires only on an import trigger (added v4; Cowork-only). |

### Repo structure and archetype

Always-active group. The two convention files are copied to every repo; the archetype spec (`research_archetype_spec.md`) is copied to a research repo only (NONE copies none). The triage and the research scaffold are kit-resident birth tools — read from the kit at new-repo setup, never copied into a content repo.

| File | Type | Purpose |
|---|---|---|
| `naming_conventions.md` | Convention | Universal naming rule — content `lowercase_underscore`, structural `ALL_CAPS`, content-file markers `ALL_CAPS` on a lowercase stem (the closed list); carry-safety, paper-stem/cite-key identity. Copied to every repo. |
| `structure_conventions.md` | Convention | Universal structure layer — root files + archetype declaration, `workspace/` (machinery) + the intake funnel (`staging/`), `workdesk/` + the pending-actions queue (the waits-on split), the `FOLDER_MAP` convention (the form in `FOLDER_MAP_template.md`; a map born with its folder; orientation maps at the machinery roots only), governance rules, created-up-front vs born, root-as-accidental-staging, reference-by-subject, reading-order, the `_ex` rule, skills layout. Copied to every repo (incl. NONE). |
| `archetype_conventions.md` | Convention | Archetype-common layer — born-minimal promote-on-evidence, origin-based typing, the shared-spine / "one repo or two" test, by-subject keying, the archetype-fixed root skeleton, and the three-layer placement model. Copied to every archetype repo; a NONE repo gets none. |
| `research_archetype_spec.md` | Spec | Full structure-and-index spec for research repos (research lines: paper N=1 / agenda N>1). Copied to a research repo only. |
| `new_repo_setup.md` | Birth tool | Archetype triage + scaffold for a new repo. Kit-resident; read at setup, not copied per-repo. |
| `research_setup_scaffold.md` | Birth tool | Research birth skeleton. Kit-resident; read at setup, not copied per-repo. |

### Thinking aids

| File | Type | Purpose |
|---|---|---|
| `brainstorming_skill.md` | Skill | Two-phase structured-questioning discipline for refining rough ideas before drafting, planning, or deciding |

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
