---
name: skill-authoring
description: "Use this skill when authoring a new skill file for the kit or for a project, or when revising an existing skill. Covers (1) the general principles and conventions of the user's skills kit — naming, frontmatter discipline, cluster structure, decomposition principle, marker discipline — that any new skill must honor; (2) when to write a skill versus leave a task uncodified; (3) what a skill file contains; (4) the workflow for drafting a skill with Claude; (5) when a project-local skill should be promoted to the kit. Does NOT cover the consolidation workflow that moves skills from project repos into the kit — that lives in the canonical kit's consolidation workflow and only runs in your canonical skills repo."
triggers: >-
  "let's write a skill for this," "I keep correcting Claude the same way," "we should codify
  this," "draft a skill for X"; revising an existing skill substantively
---

# Skill Authoring

A skill is a reusable instruction file that tells Claude how to handle a recurring task. The kit already contains skills for paper processing, document processing, writing, translation review, formatting, session management, and more. But most projects also accumulate their own skills — for tasks specific to how the project works that the generic kit doesn't cover.

This skill is the meta-skill: how to write a new skill that fits the kit's conventions, whether it lives in a project's `skills/` folder for project-local use, or eventually gets promoted to the kit itself.

## When to use this skill

Read this skill when:
- The user says "let's write a skill for this," "I keep correcting Claude the same way — can we make a skill," "this needs a skill," "we should codify this," "how should I structure this skill," "draft a skill for X."
- A task is being done for the third (or fourth, or fifth) time with roughly the same instructions, and codifying the pattern would save the same explanations every future time.
- An existing skill is being revised substantively and the reviser wants to check the conventions.

Do not use this skill for:
- Project-specific configuration that belongs in `CLAUDE.md`, not in a reusable skill (parameters, folder names, deliverable lists, project-specific conventions).
- Editing an existing skill in a minor way (typo, small wording fix) where re-reading the conventions adds nothing.
- The kit-maintenance workflow that pulls candidate skills out of project repos and merges them into a canonical kit — that runs only in the canonical skills repo, if you keep one, and is a different shape of work.

---

## Part 1 — General principles and conventions of the kit

Before writing any new skill, internalize the conventions below. They're not arbitrary — each one is a response to drift the kit has accumulated and corrected over time. New skills that honor them slot in cleanly; new skills that don't create drift the next audit will catch.

**Who these files are for — the principle above every convention.** A skill, like every file the kit shapes in a repo, is written for Claude; the user asks in chat and almost never opens it. So the design measure is what the file costs its reader: reading, not opening, is the cost (everything read stays in working memory all session and stale text is followed as instruction); split by the moment of need (every turn, a known moment behind a pointer and trigger, never at start); fixed headings, because Claude finds by pattern; one home per fact; no maintained views (a hand-curated cross-reference table restates facts that have homes and goes stale silently). Two readers are designed for: the strong model in session and the wave executor following the letter. The principle is stated once, in `structure_conventions.md` ("Who these files are for"); every rule below is one of its consequences, and a new skill is judged by it before anything else — who reads this, at what moment, at what cost.

### Naming conventions

Files in the kit follow a small set of suffix conventions:

- `_skill.md` — instruction files Claude reads and follows. The unit of the kit.
- `_template.md` — templates that get copied into projects and filled in (e.g., `CLAUDE_template.md`, `STATUS_template.md`).
- Plain descriptive `.md` — assets that aren't instruction files but are read for content (e.g., a color-palette reference is an asset, not an instruction).
- `_preamble.tex` / `_preamble.js` — code resources paired with a skill (e.g., `academic_paper_preamble.tex` pairs with `academic_paper_latex_skill.md`).

Format-prefix discipline applies where multiple variants of a format exist: `academic_paper_latex_skill.md` and `academic_slides_skill.md` are the shipped pair, and a house variant of either would be prefixed the same way (`<house>_paper_latex_skill.md`, `<house>_slides_latex_skill.md` / `<house>_slides_pptx_skill.md` for Beamer and PowerPoint variants of one deck). The prefix names the variant; the rest names the kind of thing.

Lowercase throughout, words separated by underscores. The exceptions are the templates named for the `ALL_CAPS` repo file they produce and the kit's own structural files, where the uppercase prefix preserves the convention that the repo file itself is uppercase in every repo.

### Frontmatter discipline

Every skill file starts with YAML frontmatter, three keys:

```yaml
---
name: skill-name-in-kebab-case
description: "One paragraph: what the skill is for, what it does, and what it does NOT cover."
triggers: >-
  One string, about twenty words: the literal phrases the user says and the conditions
  under which the skill is read. The same text the repo's CLAUDE.md skills table shows.
---
```

Three non-obvious rules:

1. **`triggers:` is the one home of a skill's trigger phrases**. Claude pattern-matches on it to decide whether to read the skill, and the repo's `CLAUDE.md` Skills table copies it verbatim into the When to use cell at every propagation (`PROJECT_SETUP.md` Step 7.5; the modules registry copies a module skill's key into its Trigger phrases column the same way). So the phrases are written once, in the key, and nowhere else in the frontmatter: the description says what the skill is and what it does not cover and never lists the phrases. *(Predecessor: until v6.5 the description carried a "Triggers:" sentence and the template's cell was hand-written, and nothing kept the two in step.)* A module card's `triggers` row is a different thing under a near name: the structural trigger-home pairs (`MODULE_template.md` in your canonical skills repo's `modules/`).

2. **The `triggers:` value is sourced from observed phrasings, not designer assumptions.** If it doesn't contain the phrases the user actually uses, the skill won't trigger at the right moment. Before drafting frontmatter, list the phrasings the user would actually say when invoking this skill and use them literally. A condition works where a phrase does not ("only when explicitly asked to apply the academic voice").

3. **Name what the skill does NOT cover, alongside what it does.** The description should distinguish the skill from adjacent skills. If two skills overlap on triggers but cover different work, both descriptions should name the boundary explicitly. (See `project_tracker_skill.md` and `finish_session_skill.md` for an example — both fire at session close, but `project_tracker_skill.md` does not save full conversations, and `finish_session_skill.md` does not re-implement the per-step procedures.)

Assets (non-skill files) can get skill-shaped frontmatter if they need discoverability — a color-palette asset carries frontmatter so Claude finds it when producing visuals.

### Environment discipline: the Cowork-only line

The user works in two environments — Cowork (local clones under `repos/`, working git) and claude.ai web (one repo per session, git push blocked). Most skills work in both and say nothing about it; commit and branch mechanics are centralized in `github_api_workflow_skill.md` (the repo-access authority), which every transport-touching skill points at instead of carrying its own.

The test: **does any workflow step read or write outside the home repo?** If yes, the skill is **Cowork-only** — a web session physically cannot run it — and must say so with the standard Environment line, placed immediately after the H1 title:

> **Environment: Cowork only.** \<one sentence naming the multi-repo reach.\> If this is a claude.ai web session, stop and tell the user this needs to run at Cowork — do not improvise a web-side alternative (the API-bridged version of this workflow is retired). At Cowork, open by stating which repo (and, for cross-repo workflows, which direction) this session is working in, and wait for the user's confirmation before proceeding.

The lead token `**Environment: Cowork only.**` is fixed and greppable — audits verify presence mechanically. The middle sentence is file-specific; the two closing instructions are fixed. The no-improvisation clause guards Claude (the failure mode is a web session "helpfully" reconstructing the retired multi-repo transport, not ignoring the line). The confirm-the-working-repo opening guards the user's own discipline as much as Claude's: they run several workstreams in parallel, and at Cowork every clone is equally visible — nothing physical marks the active repo, so the workflow states it and they confirm it. **Marked case only:** works-anywhere skills carry no counterpart line — absence means works anywhere. And skills whose *mechanics* differ by environment but run in both don't get the line either; they point at the authority's environment branch instead of forking.

A skill is a split candidate when **all three** of these hold:

1. It has a clear triage or branch step that routes to substantively different protocols.
2. The protocols evolve asymmetrically over time (the patterns of one change without affecting the other).
3. Typical invocations load only part of the content (when handling paper A, the Protocol B section is dead weight).

When all three hold, splitting produces a triage skill plus protocol-specific skills (see `materials_processing_skill.md` + `paper_processing_academic_skill.md` + `paper_processing_institutional_skill.md`; see `writing_skill.md` + `writing_notes_skill.md` + `writing_drafting_skill.md`).

Do **not** split for these reasons:

- **Size alone.** A long skill is not a split candidate if it's a linear workflow. `repo_audit_skill.md` is long but its steps flow into each other; splitting would fragment it.
- **Reference skills.** Style guides and format references (a personal voice profile, a document-formatting skill) are consulted by lookup, not followed end-to-end. Splitting them doesn't change how they're used.
- **Mode parameters.** `repo_audit_skill.md` has report-only and repair modes. Modes are parameters, not branches; they don't justify splitting.

### Cluster structure

**Scope of this section.** Cluster structure is a kit-side organizational convention. It applies to skills that live **in the kit** — the canonical copy, wherever you keep it, and the curated subset of `skills/` that each content repo receives at propagation. Skills authored inside a content repo are project-local at creation; they live outside the cluster structure. Cluster placement is decided only if and when a project-local skill is consolidated into the kit (the consolidation conversation on the canonical side makes the placement call at that point — not the author at creation time). The rules below describe how that placement works when it happens.

The kit is organized into **eight functional clusters**. The canonical roster — cluster names, membership, and order — lives in `CLAUDE_template.md`'s Skills section (point, don't restate: an enumerated copy carried here drifted as the kit grew). Every kit skill lives in exactly one cluster.

Two cross-cutting rules govern cluster work:

**Cluster placement is decided by current purpose, not anticipated future generality.** `writing_branch_skill.md` lives in Repo and session infrastructure (always-active), not in Writing and deliverables where its topic would suggest, because `finish_session_skill.md` (always-active) invokes it as a required action — the hard dependency that exists *now* places it, not the cluster its name points at.

**Cluster completeness invariant.** Every skill's hard dependencies (workflow steps that invoke another skill as a required action) must resolve within the always-active group or within the source skill's own cluster. If a new skill needs to invoke a skill in another cluster, either the dependency moves to the always-active group, or one of the two skills moves clusters. Soft references (descriptive prose, hand-off notes, "see also") are not constrained by the invariant.

### Physical placement vs. cluster placement

Two different "where does it go" questions, easily conflated:

- **Physical placement** — where the skill *file* actually sits in the repo. This is the author's call **at creation**, governed by the **folder-skill placement rule** in `structure_conventions.md` ("Skills layout") and refined per type in the repo's archetype spec (the research spec's skills-and-machinery note). The shape: `skills/` is the kit's flat folder, where only a generic candidate's loose file sits beside the kit; a project-specific skill, and any skill that **needs its own folder** (multiple files, or a `corpus/`), does *not* live in `skills/` — it goes **folder-local, next to the work it serves**. `CLAUDE.md`'s skills table rosters every skill wherever it physically lives — `skills/` itself is machinery outside the retrieval architecture (no required map; `structure_conventions.md`), not the roster.
- **Cluster placement** — which of the eight functional clusters a skill belongs to. This is **not** a creation-time call; it is decided at consolidation on the canonical side, only for skills being absorbed into the kit (see the scope note above and Part 5).

So the creation-time structural decisions are the **propagation axis** (project-specific vs. generic-candidate) and **physical placement** — both worked through in Part 4, Step 2. Cluster comes later, and only for generic candidates that graduate. Don't reach for the substance of the folder-skill rule here; read it in `structure_conventions.md` + the archetype spec. This section only fixes which question is being asked when.

### Per-propagation per-cluster curation

The kit ships to each project as a curated subset, not the full kit. At project setup and at every kit propagation, the user and Claude decide per cluster whether the cluster activates for this project. Activated clusters' skills are copied into `skills/`; deactivated clusters' skills are not copied (or are removed if they were present from a prior propagation).

This is relevant to skill authoring only at the consolidation stage — when a project-local generic-candidate skill is being absorbed into the kit, the cluster placement decision also shapes how widely the skill will be available across projects (a skill placed in a cluster that's often deactivated will not be present where it's needed). At creation time in a content repo, the author doesn't make this call; the file is project-local and isn't curated.

Curation runs at the cluster grain but is not all-or-nothing: the cluster is the **proposal unit**, and individual skills within an activated cluster can be skipped or added per repo (the relaxed rule that replaced v2.x's all-or-nothing-per-cluster contract; `skills_curation_skill.md` owns the activation rules — point, don't restate). When consolidating a new skill into the kit, do not design it to *require* whole-cluster activation: it should degrade gracefully if a sibling skill is not present.

### Modules: the third tier on the propagation axis

Between kit skills (single files, curated per cluster) and project-specific skills (never move) sits the **module**: a folder package that repos carry when they have a structural trigger (a folder such as `funding/`, or an archetype type), distilled from a corpus of sources. The tier is defined in `structure_conventions.md` ("Modules"); this skill only fixes what it means for authoring. Two things differ from kit skills. A module is **made in your canonical skills repo**, where its corpus lives, and only *used* (and patched in place when live work forces it) in content repos. And its corpus is split at the build into what the skill **reads while operating** (travels, in `references/`) and what it **was distilled from** (kit-resident `corpus/`). Cluster placement does not apply: a module has no cluster, its trigger decides where it goes.

### Version and last-updated marker discipline

The kit uses two independent version trackers. They never track each other.

**Skill version — MAJOR.MINOR.PATCH.** Each skill carries its own semantic version, classified by what a change does to *that skill*:

- **MAJOR** (x → x+1): the skill behaves differently when invoked — a step added, removed, or reordered, or a workflow restructured or replaced. ("Step" means something the skill *does* during an interaction, not an explanatory passage.)
- **MINOR** (x.y → x.y+1): same behavior, refined — a caveat, a clarification, an added explanation, or a new rule that only sharpens how an existing step is described.
- **PATCH** (x.y.z → x.y.z+1): trivial — a typo, an accent, a formatting fix. This is the floor; three components, never more.

Tie-breaker for the ambiguous middle (e.g. a newly added hard rule): does it change what the skill *does* when invoked (major), or only how an existing step is described (minor)?

**Kit version — MAJOR.MINOR.** The canonical package as a whole carries a separate version that marks a *dissemination* — a consolidate-and-re-propagate event. It has no patch level, because a dissemination is costly and is never run for a trivial fix.

- **MAJOR** (x → x+1): the kit's functional structure changes — workflow, clusters, curation/propagation, or naming/decomposition conventions — or a deliberate re-baseline. Volume alone does not force a major; many purely additive skills are still a minor, though a milestone-worthy additive release may be stamped major as a deliberate call.
- **MINOR** (x.y → x.y+1): skills added or updated, including a complementary skill that does not change any workflow.

**Two clauses that keep the trackers from colliding:**

1. A skill's version is its own and is **never set equal to the kit's**. A skill at v1.1 lives fine inside a kit at v2 or v3.
2. The kit version is stamped **only at dissemination**, and a planning cycle is named for the kit version it targets. Intermediate commits within a multi-session cycle do not bump the kit version.

**Marker format.** Every skill ends with a single italic line:

```
*Last updated: Month D, YYYY — vX.Y.Z (what changed in this version; MAJOR, MINOR or PATCH). Prior versions: the kit CHANGELOG.*
```

One trailing marker per file, carrying the current version only. When a skill is revised, the line is rewritten in place: the new version, the new note, the same pointer sentence. Prior versions are not kept in the file — the kit CHANGELOG holds every version's note, entry by entry, and git holds the file. *(Predecessor: the prior note was folded into each new marker's parenthetical, so the chain grew without bound and duplicated the CHANGELOG. Stacked markers, the older drift, stay out too.)* Non-skill kit files (specs, scaffolds, conventions, templates) follow the same rule in their own opening form (`*Kit file — **vX.Y, the session (date):** …*`); a module skill's pointer names the module's kit-side CHANGELOG. **A project skill never stamps the kit version** in its body or marker ("kit v6.5"): it goes stale at every wave, and the kit version the repo is on has one home, `CLAUDE.md`'s trailer.

### Atomic-commit discipline for kit changes

Changes that touch multiple kit files (renaming a skill, splitting a skill, adding a new skill with wiring updates in `CLAUDE_template.md` and `PROJECT_SETUP.md`) must ship as one atomic commit (plain git at Cowork; the Trees API on the web — `github_api_workflow_skill.md`); project-local skill additions in a single content repo don't need this discipline because they touch fewer files.

---

## Part 2 — When to write a skill

A dedicated skill is warranted by **either** of two signals — you don't need both:

- **Frequency.** The same kind of task, with roughly the same instructions, **three or more times.** The third time the same correction or context appears is the cue. Here the recipe is encoded once, and the skill's own runs accumulate material over time (the *skill→corpus* direction).
- **Tacit-knowledge capture.** A task done *rarely* but carrying a lot of unwritten knowledge — there's a body of good and bad examples you reason from, and a skill would make the implicit explicit. Here the skill is distilled *from* that example body (the *corpus→skill* direction). A low-frequency task can still warrant a skill on this signal alone.

If the task warrants its own **`corpus/`** — task-tuning material with provenance to the skill — the skill is a **folder-skill**, not a loose single file, and that has a placement consequence (Part 4, Step 2: a corpus-backed skill is folder-needing and lands folder-local, with its `corpus/` alongside). *(The corpus rules live in `structure_conventions.md`, "Skills layout"; this is the authoring-side view of them.)*

Other good triggers:

- The same correction appears across multiple sessions ("you forgot to include X," "the structure should be Y, not Z").
- A task has a fixed structure that can be articulated (steps, sections, conventions) and retyping it every time is friction.
- The task is something a colleague or future-you might also do, and writing it down would save the same explanations.

**When NOT to write a skill:**

- For a one-off task. If it won't recur, don't formalize it.
- For a task that can't yet be articulated. If "what good looks like" is still unclear, do the task a few more times first. Codify when the pattern is stable, not when it's still forming.
- For something already covered. Check existing skills first — sometimes what's needed is a small addition to an existing skill, not a new one.
- For project-specific configuration. Parameters, folder names, deliverable lists, collaborator names — these belong in `CLAUDE.md`, not in a reusable skill.

---

## Part 3 — What a skill file contains

The components, in order:

### 1. YAML frontmatter

Three fields: `name:` (kebab-case, matches the filename minus `_skill.md`), `description:` (one paragraph: what it is, what it does not cover) and `triggers:` (one string: the phrases and conditions that fire the read; the `CLAUDE.md` cell). See Part 1 for the discipline.

### 2. Title

A single `#` heading with the human-facing skill name. Title case is fine; the filename is the convention point.

### 3. One-paragraph summary

What the skill does, who uses it, when. This is what a human reads to confirm they're at the right file.

### 4. "When to use this skill" section

A short list of triggering scenarios for human confirmation, plus an explicit "Do not use this skill for" subsection that names what's out of scope. The frontmatter's `description:` is for Claude's pattern-matching; this section is the human-readable counterpart.

### 5. Prerequisites (optional)

If the skill assumes certain parameters or files exist in the project's `CLAUDE.md`, list them here.

### 6. The workflow

The core of the skill. A numbered series of steps Claude follows. Each step should be:

- **Specific.** Not "extract the text" but "use PyMuPDF to extract text. If fewer than 100 words come out, classify as scanned PDF and flag for manual review."
- **Imperative.** Tell Claude what to do, not what the task is about.
- **Decision-aware.** If a step branches ("if X, do this; if Y, do that"), spell out the branches.

### 7. Key rules

A short bulleted list of non-negotiable rules. These often capture the mistakes already seen — "do not skip the outline step," "do not summarize quotes verbatim," "always show before committing."

### 8. Edge cases

Things that don't fit the main workflow but recur. Worked examples here are valuable.

### 9. Setting up for a new project (optional)

If the skill needs configuration in the project's `CLAUDE.md`, describe what to add there. This is how the generic skill becomes specific to a project.

### 10. Last-updated marker

A single trailing italic line, the current version only. See Part 1 for the discipline.

---

## Part 4 — Workflow: drafting a skill with Claude

### Step 1 — Describe the task

Describe the task to Claude in concrete terms: what the input looks like, what the output looks like, who the audience is, what makes a good output versus a bad one. Examples help — "the last time I did this, the result was X, and what I wanted was Y."

### Step 2 — Decide placement: the propagation axis and the physical home

Every new skill is born project-local — it lives in the repo where it was authored. Two placement decisions are made now, at creation, and both are the author's call. (A third — *cluster* placement — is **not** made here; see the end of this step.)

**Decision 1 — propagation axis: project-specific or generic candidate?** Will this skill ever be useful in another project?

- **Project-specific** — it references a deliverable, collaborator, parameter, or workflow unique to this project, and will never propagate. It stays **out of `skills/`** so the discovery sweep correctly ignores it (the sweep only looks inside `skills/`). Where it physically lands is Decision 2.
- **Generic candidate** — it describes a pattern that could apply across projects, even if authored in one repo for now. Place it **inside `skills/`**, a loose file (the folder is flat), so the next discovery sweep picks it up; consolidation later decides cluster placement, generalizes phrasings, and merges it into the kit; a future propagation ships it to other repos.
- **Module candidate** — it is a folder-needing, tacit-knowledge skill (a corpus behind it) that a **second repo** needs, and both repos share a structural trigger (the same workstream folder, or the same archetype). It stays folder-local where it is; it is announced, not moved (Step 7). The tier is defined in `structure_conventions.md` ("Modules").

If the decision isn't clear, default to project-specific — a skill is promoted later by moving it into `skills/` and logging it; a skill that propagates prematurely is harder to claw back.

**Decision 2 — physical home: apply the folder-skill placement rule.** This is where the file actually sits. The binding rules live in `structure_conventions.md` ("Skills layout") and the repo's archetype spec (the research spec's skills-and-machinery note) — read those; the shape is:

- A **single-file** skill is a **loose file** (`skills/` is flat, `last_skill_update/` the one folder inside). A generic candidate's loose file goes in `skills/` per Decision 1; a project-specific single-file skill goes **folder-local, next to the work it serves** (the root `{task}_skill/`, the form for a repo whose whole work is that one task).
- A skill that **needs its own folder** (multiple files — agents, render scripts, templates, or a `corpus/`) does **not** live in `skills/`. It goes folder-local, next to the work it serves (the repo root `{task}_skill/` in a repo whose whole work is that one task). **Inside its folder the skill is laid out the way a module is** — the skill file(s) at the folder's root, `references/` beside them, `corpus/` inside — so a promotion to the module tier lifts the folder whole; the module's machinery (`MODULE.md`, `parameters.md`, `corpus_inbox/`, the baseline) arrives at promotion, never before. **And the folder holds the skill, never what the skill produced:** a thing the skill makes lives in the project's own folder beside the skill's home, never inside it (`structure_conventions.md`, "Skills layout").
- Wherever it lands, **`CLAUDE.md`'s skills table is the roster** — register the skill there regardless of physical location; `skills/` itself is machinery outside the retrieval architecture (no required map), not the roster.

**The two axes line up in practice, so they don't fight.** A folder-needing skill is tied to a task's `corpus/`, so it is project-specific and goes folder-local; a generic candidate is a single-file pattern and goes as a loose file in `skills/`. `skills/` is flat, so a multi-file skill folder never sits in it anyway. Whether the skill warrants a `corpus/` (and is therefore folder-needing rather than a loose single file) is settled by the Part 2 triage; if it has one, the corpus is skill-scoped and travels with the skill's folder.

Filename in all cases: `<purpose>_skill.md`. See Part 1 naming conventions.

There is no **cluster** placement at this step. Cluster placement happens at consolidation on the canonical side, not at creation in the content repo — see Part 1's "Physical placement vs. cluster placement" and Part 5.

### Step 3 — Source observed phrasings for the frontmatter

Before Claude drafts frontmatter, list the literal phrasings used when invoking this skill. They go in `triggers:`, never in the description. If the phrasings aren't clear yet, name the most natural way the task would come up.

### Step 4 — Claude proposes a draft

Ask Claude to draft a skill file using the structure in Part 3. Read it carefully.

### Step 5 — Iterate

The work happens here. Common things to fix:

- The `description:` is too vague — make it more specific; include the actual triggering phrasings.
- The workflow is too high-level — break a step into substeps.
- A rule is missing — add it.
- An assumption is wrong — flag it.
- The skill is doing too much — check Part 1's decomposition principle; if all three conditions hold, split.

Don't expect the first draft to be right. Skills get better as they're used.

### Step 6 — Test it

Use the skill on a real task. Where Claude gets it right and where it doesn't are both signals. The places it gets wrong are usually places where the skill needs more detail.

### Step 7 — Save and wire

Save the file at the physical home chosen in Step 2 (Decision 2), then wire it up per the propagation axis (Decision 1).

**Physical placement (both cases):**
- Save the skill at its folder-skill home — a generic candidate's loose file in `skills/`; a project-specific single-file skill folder-local next to the work; a folder-needing skill in its own folder next to the work (the root `{task}_skill/` in a repo whose whole work is that one task), per `structure_conventions.md` + the archetype spec.
- If the skill warrants a **`corpus/`** (the Part 2 triage), create it skill-scoped alongside the skill and seed it by direction: a **frequency** skill's corpus accumulates from its runs over time (skill→corpus), so it may start empty; a **tacit-knowledge** skill's corpus holds the **inputs that make the skill** — the good and bad examples it was distilled from — placed now, with a provenance pointer back to the skill (corpus→skill).
- Register the skill in **`CLAUDE.md`'s skills table** regardless of where the file sits — that table is the roster.

**If the skill is project-specific:**
- Add its row to the `### Project skills` table of the project's `CLAUDE.md` (always present, `CLAUDE_template.md`: Skill file, When to use), with the actual path.
- No `<KIT_FOLDER>/CHANGELOG.md` entry — that changelog is for kit-side state, not project-specific work.
- Optionally note in STATUS.md if the addition is part of in-flight work worth tracking.

**If the skill is a module candidate:**
- It stays at its folder-local home (Decision 2); nothing is moved into `skills/`.
- **Add an entry to `<KIT_FOLDER>/CHANGELOG.md`** under the heading `## [MODULE CANDIDATE] — <folder> — <date>`, naming the folder, the trigger the two repos share, and the other repo that needs it. This is what the next kit update (the discovery sweep, if you keep a canonical skills repo) reads, since it does not walk folders outside `skills/` until a module is declared.
- Register the folder's skill in the `### Project skills` table; the `[MODULE CANDIDATE]` entry carries that it is a candidate and which repo needs it.
- Consolidation opens the lift: a planned row in the module registry (`modules/MODULES.md` in your canonical skills repo) and a queued build session that sorts the folder's material into corpus and references and writes `MODULE.md`; the next wave then carries it to every repo with the trigger (`structure_conventions.md`, "Becoming a module").

**If the skill is a generic candidate:**
- It is saved inside `skills/` (Decision 1), so the discovery sweep will see it.
- **Add an entry to `<KIT_FOLDER>/CHANGELOG.md`** under the standard heading `## [PROJECT-LOCAL SKILL ADDED] — <file> — <date>` (defined in `structure_conventions.md`'s CHANGELOG-channel section), with a brief description of what it does and why it's a candidate (one or two sentences). This entry is what the next kit update (the discovery sweep, if you keep a canonical skills repo) reads to recognize the file as a deliberate addition rather than ambient drift. Like `[SKILL-FEEDBACK]`, the entry is spent once the candidate is consolidated and does not survive propagation's overwrite — by then the kit CHANGELOG carries the real entry.
- **Add its row to the `### Project skills` table** of the project's `CLAUDE.md` (Skill file, When to use — the row every project-local skill gets, whatever its axis). The propagation axis and the suggested kit cluster are not cells: they travel in the `[PROJECT-LOCAL SKILL ADDED]` entry, which is what consolidation reads ("generic candidate, suggested cluster: Voice and style"); the suggestion is advisory, consolidation makes the binding decision.
- **Note in STATUS.md** in the `repo` workstream entry's Next or where-it-stands field — a short clause that this generic-candidate skill was added and awaits the sweep. STATUS.md keeps the project's tracker honest; the changelog is for downstream consolidation.
- The next discovery sweep in the canonical skills repo will pick up the file from `skills/`, the consolidation conversation will decide cluster placement and generalize the frontmatter, and a future propagation will ship the canonical version back to relevant repos.

In either case: do not pre-assign a cluster, do not write the skill's frontmatter as if it were already in the kit, and do not anticipate generalizations the consolidation conversation will make. The author's job at this step ends when the file (and its `corpus/`, if any) is in place and the relevant logs are updated.

### Step 8 — Reuse and revise

Each use surfaces small things to improve. Iterate. Skills are living documents.

**Revising an existing *kit* skill inside a content repo** (the case the steps above don't cover — they are new-file-shaped): when a kit skill needs more than feedback can carry and the fix can't wait for the next kit cycle, edit the repo's **live copy** in `skills/` directly. Then:

- **Bump that copy's own version marker** (MAJOR.MINOR.PATCH by what the change does to the skill), so the sweep's version signal is honest.
- **Log a `[SKILL-FEEDBACK]` entry** in `<KIT_FOLDER>/CHANGELOG.md`, stating explicitly that there *is* a file change behind it (the fixed-locally-pending-review case; see `structure_conventions.md`). The entry explains what was wrong and what changed; the edit itself travels as the sweep's diff.
- **Leave `skills/last_skill_update/` untouched.** The snapshot is what makes the diff visible to the next discovery sweep; updating it hides your fix. (Derivable from Part 5, stated here so nobody has to derive it.)
- Whether the fix propagates to the canonical kit is decided at the next consolidation, not by the repo.

---

## Part 5 — The downstream lifecycle: from generic-candidate to kit skill

Promotion isn't a decision the author makes at creation time. It happens later, on the canonical side — **if you keep a canonical skills repo**: one place where the kit lives and from which it propagates out to your project repos. If you don't keep one, this part simply doesn't apply. The skill stays where it was authored, and "promotion" means copying it by hand into the next project that needs it.

**The mechanics, in short.** A canonical kit repo runs two habits, both outside this skill's scope. A periodic **sweep** compares each project repo's `skills/` folder against the snapshot in its `skills/last_skill_update/`, so new and locally edited files surface as diffs; your generic candidate shows up there as a new file, and its `<KIT_FOLDER>/CHANGELOG.md` entry is the context that marks it a deliberate addition rather than ambient drift. A **consolidation** conversation then decides what to absorb.

**What consolidation decides.** Cluster placement (per Part 1), frontmatter generalization (drop project-specific phrasings; source new phrasings from observed usage), a naming check against the kit's naming conventions (rename if it doesn't conform), the wiring updates in `CLAUDE_template.md` (cluster row) and `PROJECT_SETUP.md` (Phase 4 menu, Files-to-copy list, Appendix), and a kit CHANGELOG entry. A later propagation (Part C of `PROJECT_SETUP.md`) then ships the now-canonical skill to content repos as part of the per-cluster curation conversation: repos that activate the cluster receive the skill; repos that don't, don't.

**What this means for the author.** The author's job ends at "saved in `skills/`, logged in changelog and STATUS.md." Cluster placement, generalization, kit-wide phrasing — all of it happens later, by people (or a session) with full visibility of the kit. The author writes the skill that works in this project; the consolidation conversation translates it into a kit skill.

**One thing the author can do to make consolidation easier:** keep project-specific references in the project's `CLAUDE.md` (parameters, paths, collaborator names), not baked into the skill body. A clean generic-candidate references its inputs via parameters defined elsewhere; a messy one hard-codes project specifics into rules. The cleaner one is straightforward to consolidate.

**Modules follow a different loop.** A module is made and revised in your canonical skills repo against its corpus, if you keep one (the kit's `modules/<name>/` folder), so the content-repo side of its lifecycle is feedback, not authorship: a live patch to the repo copy is logged as `[SKILL-FEEDBACK]` in the module's `MODULE.md`, a new source example goes to `corpus_inbox/` with a `[CORPUS CANDIDATE]` entry, and the sweep carries both here. `structure_conventions.md` ("Modules") owns the full lifecycle; point, don't restate.

**Signals that a generic-candidate is consolidation-ready:**
- It has been used unchanged for long enough that the patterns are stable.
- It would work as-is (or with light frontmatter edits) in a different project.
- It doesn't duplicate something already in the kit.

A sweep picks up the candidate regardless of readiness; the consolidation conversation is where readiness is judged. A candidate that isn't ready can be deferred, archived, or rejected — the project repo's copy stays in place either way.

---

## Part 6 — Worked example: a talking-points skill

Suppose the user finds themselves asking Claude to prepare talking points for meetings repeatedly, and keeps giving the same kinds of instructions. Here's how the conversation might go:

**User:** "I'd like to write a skill for preparing talking points. Each time I ask, I usually need: 3–5 main points, each with a one-line message and 2–3 supporting facts; ordered from most to least important; in my voice (direct, evidence-based, no filler). The audience varies — sometimes a client, sometimes a peer, sometimes a journalist. Can you draft a skill?"

**Claude:** "Before drafting, the two creation-time placement calls. **Propagation axis:** talking-points prep is a general pattern, not tied to anything unique to this repo, so I'd call it a generic candidate and save it in `skills/` where the next sweep can find it. **Physical home:** it's a single-file deliverable skill, and there's no example-corpus driving it (the frequency signal, not tacit-knowledge), so it's a loose file — not a folder-skill, no `corpus/`. Filename: `talking_points_skill.md`. No cluster call here — that's consolidation's job if it ever gets promoted (Part 5)."

**User:** "Right. Go ahead."

**Claude:** [drafts `talking_points_skill.md` with frontmatter, when-to-use, workflow, rules]

**User:** "Looks good but: the `description:` should mention 'briefing,' 'preparation for a meeting,' and 'key messages' — those are the phrases I actually use. Also, you have a step that says 'identify the audience' — turn that into a specific question Claude should ask me at the start, because I always forget to say. And add a rule: if I haven't given you the meeting context, ask before drafting."

**Claude:** [revises]

**User:** "Better. Let's test it." [uses the skill on a real meeting]

**User:** "It worked but the points were too long. Add: 'Each main message is one sentence, max 20 words.' That's a hard limit."

**Claude:** [adds the rule, bumps the version]

After a few iterations like that, the skill captures how this task is actually done. The next time the user says "prepare talking points for the meeting with X," Claude reads the skill and produces something close to what the user would have produced themselves, without retyping the instructions.

If, six months later, the same skill is being used unchanged in three projects, that's the promotion signal — a candidate to graduate into the kit per Part 5.

---

## Part 7 — Common mistakes

- **Description too vague to trigger.** "Write professionally" tells Claude nothing about when to read this file. Specific triggering phrasings, included literally, are what make the skill discoverable.
- **Skill content duplicated in CLAUDE.md.** If the same instructions appear in multiple projects' CLAUDE.md files, that's a skill, not project context. Move it.
- **No examples.** Examples are the fastest way to teach Claude what good looks like. Include at least one worked example for any non-trivial skill.
- **Trigger phrasings invented by the designer.** "When the user wants to optimize their workflow" is a designer phrase; nobody says that. Use the user's actual words.
- **Cluster-shopping at creation time.** Project-local skills don't get a *cluster* — that's a consolidation decision on the canonical side, not a creation-time call. At creation the structural calls are the **propagation axis** (project-specific vs. generic-candidate → whether the file goes in `skills/`) and the **physical home** (the folder-skill placement rule → loose-in-`skills/`, folder-local, or a `{task}_skill/` folder, plus where a `corpus/` lands). Cluster is a different, later, canonical-side decision.
- **Hoisting a folder-needing skill into `skills/`.** A skill with multiple files or a `corpus/` does not belong in `skills/` — that folder is flat, the kit's loose files and the `last_skill_update/` snapshot. A corpus-backed skill goes folder-local, next to the work it serves (`structure_conventions.md` + the archetype spec). Putting it in `skills/` breaks the flat folder the next audit checks.
- **Forgetting to log a generic candidate.** A new file in `skills/` without a corresponding `<KIT_FOLDER>/CHANGELOG.md` entry is ambient drift, not a deliberate candidate. The log entry is what tells the next kit update (the discovery sweep, if you keep a canonical skills repo) this was intentional.
- **Pre-generalizing for the kit.** Writing the frontmatter, naming, and wording as if the skill were already in the kit anticipates work that belongs in consolidation. Write what works in the project; let consolidation translate.
- **Growing the marker.** The marker is the current version line only; a revision rewrites it in place. Don't stack markers, and don't fold the prior note into the new one — prior versions are the kit CHANGELOG's.
- **Splitting too early.** A skill with two sections is not necessarily a split candidate. All three conditions of the decomposition principle must hold.
- **Splitting too late.** A skill with a triage step that's been routing to two divergent protocols for months is overdue for a split. The drift compounds.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
