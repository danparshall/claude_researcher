---
name: skills-curation
description: >
  Run per-propagation per-cluster skills curation in a content repo — propose
  which clusters of the kit should be active for this project, anchored to
  project signals (questionnaire answers, STATUS.md, CLAUDE.md, recent commits,
  recent conversations), and apply the curated state by hard-adding or
  hard-removing skill files from the repo's `skills/` folder. Use when running
  Part A new-project setup, Part B existing-repo integration, or Part C kit
  propagation, at the cluster-activation step. NOT for editing the canonical kit
  itself — that lives in your canonical skills repo, if you keep one.
triggers: >-
  "let's run the curation," "curate the skills for this repo," "propagate the kit update";
  every propagation point (Parts A, B and C of `<KIT_FOLDER>/PROJECT_SETUP.md`)
---

# Skills Curation Skill

This skill defines the **per-propagation per-cluster curation conversation** —
the workflow Claude follows at the cluster-activation step of any kit
application (Part A / Part B / Part C of `PROJECT_SETUP.md`).

It replaces the prior "full-kit-by-default" convention. The kit ships in
clusters, not as a flat list, and at each application point Claude proposes
per-cluster activation based on project signals, with the user confirming or
overriding cluster by cluster.

## Authority rule

`PROJECT_SETUP.md` invokes this skill at the right step in each Part. If there
is a conflict between this skill and `PROJECT_SETUP.md` on the curation
workflow's substance, **this skill wins**. `PROJECT_SETUP.md` describes when
to invoke; this skill describes what the invocation does.

## Core principles

1. **Anchor on project signals, not on current folder contents.** Project
   signals are: questionnaire answers (Part A), repo content from CLAUDE.md
   and STATUS.md and recent commits (Parts B and C), recent conversations
   (Part C). The current `skills/` folder is consulted only to detect drift
   (orphaned files), never to anchor proposals. Anchoring on the folder
   anchors on stale artifacts — a previous decision that became a default.
2. **Cluster is the default unit; individual skills can be picked. Hard-add and hard-remove.** Claude proposes activation at the cluster
   level, but the user can take a whole cluster, skip it, or pick individual
   skills inside it. Whatever is activated ships; whatever is not has its
   files deleted from `skills/` — no soft-archive, no no-op-but-present.
   The point is keeping `skills/` lean; reversibility is the next
   propagation. See "Granularity" below for how partial picks are handled
   and the one risk they introduce.
3. **Recovery via next propagation only.** If a cluster is deactivated and
   later turns out to be needed, reactivation happens at the next propagation
   cycle. No mid-propagation undo plumbing.
4. **Suggest all clusters at once; the user decides across them.** Claude
   presents a proposed activate/skip for every optional cluster together,
   each with its skill list and the signal behind the call, and the user
   decides — whole cluster, skip, or individual skills. (Replaced the prior
   one-cluster-at-a-time ask, which paired with an all-or-nothing rule that
   no longer holds.)

## Granularity

Claude proposes at the **cluster** level — clusters are the fastest resolution
to reason about, so the proposal is framed cluster by cluster. But the decision
is the user's: they can take a cluster whole, skip it, or pick individual skills
inside it. Claude suggests; the user decides. There is no all-or-nothing rule and
no special-case cluster.

(History: through v3.2 this was a hard all-or-nothing rule — whole clusters
only, partial activation refused, with Final-production formats as the lone
exception. The cluster design held in most repos but chafed in a couple, so the
rule was relaxed to a cluster-level proposal with a free per-skill decision.)

**The one risk partial picks introduce: orphaned dependencies.** A few clusters
contain a skill that hard-depends on a sibling — a triage skill that routes to
its protocols (Source material's `materials_processing_skill.md` routes to its
academic and institutional protocols; Writing's `writing_skill.md` routes to
`writing_notes_skill.md` and `writing_drafting_skill.md`). Picking a triage
without its protocols, or a protocol without its triage, leaves an orphan that
breaks mid-workflow. When a pick would orphan an intra-cluster hard dependency,
Claude **warns and names the missing piece** — it does not block. The user still
decides. (Cross-*cluster* hard dependencies don't arise; the cluster
completeness invariant below keeps them out by design.)

**The unit of a pick is a skill with its companions.** A companion — a preamble,
a corrections log, an extractor script, a logo or background asset — never ships
or drops alone: it goes with the skill it serves, in and out together. The pairs
are the ones `PROJECT_SETUP.md` Part B Step 2 marks with a plus sign (the
format pairs, the translation review with its log, the deck reconciliation skill
with its extractor, the plan skill with the blind-session asset).

## The cluster completeness invariant (architectural constraint, not runtime check)

Curation works without runtime dependency resolution because the kit is
designed to honor a structural invariant:

> **Every skill's hard dependencies must resolve within the always-active
> group or within the skill's own cluster.** Hard dependencies between
> non-always-active clusters are a kit-design bug, not a curation feature
> to support.

A *hard dependency* is a workflow step in skill X that invokes skill Y as a
required action — if Y is absent, X breaks mid-sequence. Soft references
("see also Y," "Y often runs after X," hand-off prose) are not dependencies
and don't trigger the invariant.

When a kit redesign session adds or moves a skill, the cluster completeness
invariant must be checked. `repo_audit_skill.md` Check 11 automates this
wherever the repo is itself the canonical kit source: it scans every kit-side
skill for cross-cluster references and flags any that look like hard
dependencies.

**Why `writing_branch_skill.md` is always-active.** `finish_session_skill.md`
Step 2 invokes it as a required action, so the invariant places it in the
always-active group. Nearly all other cross-cluster references in the kit are soft.

**Row order inside a cluster.** In the template's tables, rows are ordered by
dependency flow: the cluster's entry point first, then the skills it invokes,
then utility plumbing (a preamble beside its format skill). The template's
tables carry two columns, the skill file and its When to use cell, the cell
copied verbatim from the skill's `triggers:` frontmatter key (its one home);
a skill's purpose lives in its description, never
restated in the table.
*(Rule moved here from the template's Skills intro at the v6.5 template
rework: it is the roster author's rule, read at curation, not a
session's.)*

## The two groups

The kit's eight clusters from `CLAUDE_template.md` split into:

### Always-active group (skip the ask, ship always)

Treated as one infrastructure-layer group. No project signal
could ever say no; the question would be redundant. These ship to every
project.

The group contains:
- The Shared assets cluster — a **bring-your-own** cluster: the package ships
  no shared assets. If you author one (a canonical color palette, say, per
  `skill_authoring_skill.md`), it belongs here and is always-active, because
  such an asset is invoked anywhere visuals come up.
- `project_tracker_skill.md`, `finish_session_skill.md`,
  `repo_conversations_skill.md`, `repo_audit_skill.md`,
  `github_api_workflow_skill.md`, `writing_branch_skill.md`,
  `exploration_branch_skill.md` (Repo and session infrastructure cluster —
  the session-start/-close spine. `writing_branch_skill.md` is here because
  `finish_session_skill.md` Step 2 (branch disposition) invokes it as a
  required action; the cluster completeness invariant then *requires* it to
  be always-active. `exploration_branch_skill.md` is here by placement
  decision — the two branch skills kept together — *not* by the invariant:
  nothing always-active hard-invokes it (`finish_session`'s light arm and
  `brainstorming`'s triage are both soft hand-offs), so its membership is a
  choice, not a requirement.)
- `brainstorming_skill.md` (Thinking aids cluster — trigger is
  conversational, not project-shaped)
- Kit metadata files: `CLAUDE_template.md`, `PROJECT_SETUP.md`,
  `STATUS_template.md`, `ONBOARDING_template.md`, `README_template.md`,
  `standing_documents_template.md`, `FOLDER_MAP_template.md`, `typed_index_template.md`,
  `gitignore_seed.md`, `CHANGELOG.md` (define how the repo works at all)
- `naming_conventions.md`, `structure_conventions.md` (Repo structure and
  archetype cluster — the universal floor; they ship to every repo, NONE
  included, with no ask), `archetype_conventions.md` (the archetype-common
  layer — ships to every archetype repo, a NONE repo gets none)

These four clusters keep their distinct functional groupings in
`CLAUDE_template.md`'s Skills inventory (the functional reading still
matters when you're asking "what does this skill do?"), but at the curation
layer they collapse into one group.

**The curated skills table is a legal shape.** A
repo's `CLAUDE.md` skills table may roster every kit file, or it may be curated
on the kit-metadata axis — the `CHANGELOG.md`, the seven templates (CLAUDE,
STATUS, ONBOARDING, README, standing documents, FOLDER_MAP, typed index),
`gitignore_seed.md` and `PROJECT_SETUP.md` deliberately unlisted **as a group**,
with the split stated in one line above the table in `CLAUDE.md`; the group never gets rows in
`ASSETS_INDEX.md`. What is not legal is a table that
lists part of the group: the group is in or out together. Part C Step 7 applies
the branch when it adds a kit-file row.

**Three curation behaviours in this one cluster.** (1) The **floor conventions**
(`naming_conventions.md`, `structure_conventions.md`) ship to **every repo
unconditionally**, NONE included, like the rest of the always-active group. (2)
The **archetype-common layer** (`archetype_conventions.md`) ships to **every
archetype repo and only those** — unconditional *within* archetype repos, but
**absent from a NONE repo**; the gate is simply
`type` ≠ NONE, read from the declaration. (3)
The **archetype spec** (`research_archetype_spec.md`) is kept where the repo's
declared `type` in `CLAUDE.md` is `research`, and a NONE repo carries none. The
spec pick is a *constrained* one,
reusing the same per-skill pick machinery as the optional clusters (see
"Granularity"), but *determined by the declaration* rather than proposed against
project signals. So
the cluster as a whole stays always-active — there is no activate/skip question,
it always ships — while the single spec inside it is fixed by `type`. The triage
(`new_repo_setup.md`) and `research_setup_scaffold.md` are kit-resident
birth tools, read from the kit at new-repo setup and never curated into a repo's
`skills/`.

### Optional clusters (sequential ask)

Four clusters where project signals genuinely differentiate.

- **Source material: reading and processing** — the files are the template's
  table rows for this cluster (`CLAUDE_template.md`, the Skills section, the
  one roster). Signal: project involves literature, papers, deep-research
  agents, or institutional source documents.
- **Writing and deliverables** — the files are the template's table rows for
  this cluster (`CLAUDE_template.md`, the Skills section, the one roster).
  Signal: project produces written deliverables using the structured
  note-taking + drafting protocol. Default lean: yes, because most projects
  write something; but admin projects without a
  structured deliverable may not need it. (The branch skills —
  `writing_branch_skill.md` and `exploration_branch_skill.md` — live in the
  always-active group, not here; see the always-active group above for the
  rationale.)
- **Voice and style** — a **bring-your-own** cluster: voice profiles are
  personal, so the package ships none. The files are the template's table rows
  for this cluster (`CLAUDE_template.md`, the Skills section, the one roster):
  the translation review with its corrections log, plus every profile you
  author with `skill_authoring_skill.md` and roster there. Signal: project
  produces content in one or more of the voices you profile.
- **Final-production formats** — the files are the template's table rows for
  this cluster (`CLAUDE_template.md`, the Skills section, the one roster).
  Signal: project produces output in specific final-production formats. Its format-pairs are independent, so picking individual pairs here is the common case rather than the exception. (Formats particular to your institution — a house Word template, a branded deck — are authored as further pairs, a skill plus its preamble, and join this cluster.)

## Step-by-step workflow

### Step 1 — Determine which Part is running

The signal-sources differ by Part:

| Part | Trigger | Signal-sources for proposals |
|---|---|---|
| Part A | New project setup | Questionnaire answers (Q1–Q5 from `PROJECT_SETUP.md`) |
| Part B | Existing-repo integration | Repo CLAUDE.md, STATUS.md (if present), FOLDER_MAP.md files, existing skills/skill-like files, recent commits |
| Part C | Kit propagation to existing repo | STATUS.md, recent commits, recent conversations (from `workspace/claude_conversations/`), CLAUDE.md. **NOT the current `skills/` folder contents.** |

**The archetype spec is the exception to "signals drive the proposal."** Its
pick is not proposed from project signals — it is read from the declaration. The
pick keys off `CLAUDE.md`'s `archetype.type` frontmatter: in Part
A the declared type is the one the new-repo triage just confirmed and the
scaffold wrote; in Part B/C it is read from the repo's existing `CLAUDE.md`. This
skill *reads* the declaration and acts on it — it does not run the triage or
write the declaration (those belong to `new_repo_setup.md` and the scaffold,
wired into Part A by `PROJECT_SETUP.md`).

If Part is unclear, confirm with the user before proceeding.

### Step 2 — Inventory signals

For each optional cluster, gather the relevant project signals. Write a brief
internal note (one sentence per cluster) of what signal points to activation
or deactivation. This is what Claude will name explicitly during the ask.

Examples of signals → proposals:

- Questionnaire Q1 says "policy note on school attendance" → Source material
  cluster proposed active (literature review implied); Writing cluster active
  (note is a deliverable); Voice cluster active (an institutional house voice
  likely); Final-production cluster active (a paper format likely).
- STATUS.md mentions "conference presentation in June" → Academic slides
  format-pair active.
- Recent commits show no document drafts in 60 days, only admin updates →
  Writing cluster proposed inactive for this propagation.

If a signal is ambiguous or weak, propose conservatively and surface the
ambiguity in the ask ("I'm not sure whether you'll need X — defaulting to no,
let me know if I should activate").

### Step 3 — Present all optional clusters and let the user decide

First, resolve the archetype spec from the declaration — this is stated, not
asked. Read `CLAUDE.md`'s `archetype.type` and report the result: the one spec
being kept (or, for NONE, that no spec is kept) and any other specs being
removed as strays. The convention files are not mentioned per-repo — they always
ship.

Most of the time the declaration and the specs on disk agree, and this is a
one-line statement. When they disagree — the declared type's spec is **absent**,
a NONE repo **carries a spec**, more than one spec is present and they don't
reduce to the declared one, or **no archetype is declared at all** (a repo that
predates the archetype system) — **warn and name the mismatch, propose
normalizing to the one spec the declaration implies (or to none), and proceed as
the user decides. Don't block.** This is the same stance the skill takes on
orphaned intra-cluster dependencies (see "Granularity"): surface the problem,
name the fix, leave the decision to the user. The universal convention files ship
regardless of any archetype mismatch.

Then present all four optional clusters together — Source material, Writing and
deliverables, Voice and style, Final-production formats — each with its proposed
activate/skip, its skill list, and the signal behind the call. The user decides
per cluster: take it whole, skip it, or pick individual skills inside it.

**The standing instruction — the quick opener.** Where `CLAUDE.md`'s Working
conventions or `STATUS.md` records a standing curation instruction (for example,
"ship everything, keep the repo's specifics"), Step 3 is one
line: name the instruction and where it stands, state the activated set it
implies (every cluster, every skill), and go to Step 5's delta. The per-cluster
presentation is skipped; the user can still say "no, ask me this time."

```
**Optional clusters — proposal**

1. Source material — <activate / skip>
   Skills: <comma-separated list>
   Signal: <why this call>

2. Writing and deliverables — <activate / skip>
   Skills: <list>
   Signal: <why>

3. Voice and style — <activate / skip>
   Skills: <list>
   Signal: <why>

4. Final-production formats — <activate / skip, by format-pair>
   Pairs: <list each format-pair>
   Signal: <why>

For each: take the whole cluster, skip it, or name the individual skills you want.
```

Wait for the user's decision and absorb it before staging.

If a pick would orphan an intra-cluster hard dependency — a triage without its
protocols, or a protocol without its triage — warn and name the missing piece,
then proceed as the user decides. Don't block. (See "Granularity.")

### Step 4 — Sub-asks for Final-production formats

Final-production formats is where per-pair picking is most common, since the
format-pairs are independent. When the user is choosing among pairs, the
detail reads:

```
**Cluster 4 — Final-production formats**

Each format-pair (skill + preamble) is independent. Based on signals,
I propose:

- Academic paper LaTeX (academic_paper_latex_skill.md + academic_paper_preamble.tex):
  YES / NO — <signal>
- Academic slides (academic_slides_skill.md + academic_slides_preamble.tex):
  YES / NO — <signal>
- Deck reconciliation (design_deck_reconciliation_skill.md + extract_design_deck_mirror.py):
  ships with any slides pair
- LaTeX round trip (latex_round_trip_skill.md): ships with the LaTeX paper pair
- <any format-pair you have added yourself>: YES / NO — <signal>

Ship as proposed? (yes / modify the list / skip the whole cluster)
```

If a format-pair depends on a shared asset (a logo, a background image), that
asset is not a separate question: its dependency is structural — when the pair
is active the asset ships with it, and when the pair is inactive it doesn't.

### Step 5 — Stage the curated state

After all four optional clusters have been confirmed (and the always-active
band added implicitly), assemble the full activated file list. This is what
ships to `skills/` after the propagation.

Compute the delta against current state:
- Files to ADD (in activated state, not currently in `skills/`). A new member
  of a cluster that was already active when the member joined the kit is an ADD
  like any other (v6.5's `visuals_workflow_skill.md` in Writing and
  deliverables), and its curated home
  (`workspace/visuals/`) is created by Part C Step 8.5, which keys on the
  curated set — never by hand, never only at the cluster's flip.
- Files to REMOVE (in `skills/` but cluster now inactive)
- Files to LEAVE UNCHANGED (in `skills/` and still active — Step 3 of Part C's
  classify-each-file logic still applies to these for version updates)

The Repo structure and archetype cluster contributes to the same delta: the two
convention files are always in (UNCHANGED if present, ADD if missing); the spec
matching the declared `type` is ADD if missing and UNCHANGED if present (its
version skew, if any, is handled by Part C Step 3 classification like any other
unchanged-but-present file — no separate machinery); any other spec found is
REMOVE as a stray. A NONE repo adds no spec and removes any spec found.

Present the delta to the user for final confirmation before applying:

```
**Curation delta:**

ADD (N files):
- <file>
- <file>

REMOVE (N files):
- <file>
- <file>

UNCHANGED but still subject to version classification (N files):
- <file>
- <file>

Apply? (yes / revise)
```

### Step 6 — Apply the curated state

Adds and removes go into the same atomic commit as the rest of the propagation
(or the rest of Part A/B setup). Hard-remove means delete: no archive
subfolder, no `_archived/` suffix, no commented-out CLAUDE.md row. Gone.

The version-classification logic for unchanged files runs as defined in
`PROJECT_SETUP.md` Part C Step 3 — curation determines whether the file is
present, classification determines whether its content updates. The kept
archetype spec rides this same path: curation keeps it, and any version update
to it is the ordinary Part C Step 3 classification — no new machinery. Stray
specs are hard-removed exactly like a deactivated cluster's files.

### Step 7 — Update STATUS.md cluster-activations block

Update (or create, for Part A) the STATUS.md `Cluster activations (current)`
block to reflect the curated state. Format:

```
## Cluster activations (current)

- Source material: <active / inactive>
- Writing and deliverables: <active / inactive>
- Voice and style: <active / inactive>
- Final-production formats:
  - Academic paper LaTeX: <active / inactive>
  - Academic slides: <active / inactive>
  - Deck reconciliation: <active / inactive>
  - <any format-pair you have added>: <active / inactive>

Last curated: YYYY-MM-DD (propagation vX.Y)
```

The four optional clusters get explicit active/inactive states; a deactivation
may carry its date and reason in the line ("deactivated YYYY-MM-DD, <reason>").
**A member declined at a sub-ask** while its cluster stays active is
written on the cluster's line as `<cluster>: active, less <file> (<reason>, <date>)`,
one `less` clause per declined file. This block is the one home of that choice:
the audit's Check 10 reads it and does not report the file, and Part C Step 7.5
writes the workflow section the file serves as "not carried (STATUS cluster block)". The Last curated line is **rewritten in place**, never stacked with
`Prior:` lines. *(Retired at v6.5: the Repo
archetype line, the Always-active line and the Active modules line — the
archetype and the module set have their one home in `CLAUDE.md`'s frontmatter,
read by this skill's Step 1 and by Part C Step 2.6, and the always-active group
is the kit's, not the repo's state. The pass drops the three lines where a
repo carries them.)*

### Step 8 — Save the curation conversation

The curation conversation itself is the audit trail of *why*. Save it via
`repo_conversations_skill.md` to the repo's conversations folder. Use tags
that include `curation` and `propagation-vX.Y` so future lookups by tag
find it cleanly. The conversation is automatically findable via
`workspace/claude_conversations/INDEX.md`.

This step is NOT optional. STATUS.md tells future-you what's active now; the
saved conversation tells future-you why. Both are needed.

## When a new skill is added to the always-active group

If the kit adds a skill to the always-active group (currently: shared assets,
the repo and session infrastructure cluster, brainstorming, kit metadata, the floor
conventions and the archetype layer), that addition silently ships to every repo
that pulls the next propagation. This is the trade-off of always-active: no
per-repo checkpoint.

**Mitigation:** when this happens, the propagation conversation in the FIRST
repo to pull the change should reconfirm the always-active classification
explicitly:

> "v2.X.Y adds <skill> to the always-active group. Should it remain
> always-active, or should it move to one of the optional clusters?"

The user's answer for that propagation either confirms always-active (the new
skill ships everywhere going forward) or moves it to an optional cluster
(subsequent propagations include it in the relevant cluster's ask).

The decision propagates by updating this skill, not by per-repo flag.

## Open scope — what this skill does NOT cover

- **What's *inside* each cluster.** The cluster contents are defined by the
  kit's structure (Skills inventory in `CLAUDE_template.md`). When the kit
  reorganizes clusters, this skill consumes the new structure but doesn't
  argue with it.
- **The Gap Analysis classification in Part B** (Missing / Covered but weaker
  / Equivalent / Stronger in repo). That logic still runs, but only on
  skills *inside* activated clusters. Curation is the outer filter; Gap
  Analysis is the inner one.
- **Local modifications.** If a repo has a heavily customized version of a
  skill in an activated cluster, the file is still flagged for diff review per
  Part C Step 3. Curation doesn't override per-file diff handling.
- **The archetype triage and the declaration itself.** This skill consumes the
  declared `type` and acts on it — keep the matching spec **and
  `archetype_conventions.md`** for an archetype repo (remove both, and any stray
  spec, from a NONE repo), record the archetype in STATUS.md. It does NOT run the
  archetype triage, write the `CLAUDE.md` declaration, or define what the spec
  contains. The triage and scaffold live in `new_repo_setup.md` (wired into Part A
  by `PROJECT_SETUP.md`); the spec contents live in
  `research_archetype_spec.md` and the common rules in `archetype_conventions.md`.

## Pointers to related material

- `PROJECT_SETUP.md` — Parts A, B, C invoke this skill at the cluster-
  activation step.
- `repo_conversations_skill.md` — defines how the curation conversation gets
  saved (this skill's Step 8).
- `repo_audit_skill.md` — Check 10 (added v2.1.13) verifies STATUS.md
  cluster-activations block matches actual `skills/` contents.
- `STATUS_template.md` — defines the cluster-activations block as part of
  every project's STATUS.md.
- `new_repo_setup.md` — the kit-resident archetype triage + scaffold that
  confirms the type and writes the `CLAUDE.md` declaration this skill reads.
- `research_archetype_spec.md` — the full archetype spec, kept where the declared
  `type` is `research`.
- The cluster structure itself lives in `CLAUDE_template.md`'s Skills section.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
