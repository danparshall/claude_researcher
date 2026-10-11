---
name: repo-audit
description: "Run a consistency check across a repo — verifying that infrastructure files (CLAUDE.md, FOLDER_MAP.md files, indexes like MATERIALS_INDEX.md, PAPERS_INDEX.md, navigation tables) accurately describe what is actually on disk, and that internal cross-references resolve. Runs in report-only mode (findings only, nothing applied), repair mode (propose fixes per finding, each applied on the user's go), or index-audit mode — the dedicated per-entry currency verification of what the repo's indexes, registers, and FOLDER_MAP descriptions claim, run as its own session on the INDEX_AUDIT_INTERVAL cadence. Never judges deliverable content quality — the boundary is infrastructure claims vs. deliverable quality: the audit may verify that the infrastructure's statements about the work are current; it never reviews whether the work itself is good. If the repo declares an archetype in its CLAUDE.md (type research), Check 12 additionally verifies the repo's structure, index set, placement, and naming against the archetype-common layer (archetype_conventions.md) and the one archetype spec it carries — a conformance check, distinct in kind from the infrastructure-consistency checks. Check 14 runs kit conformance in every repo, NONE included: same-job candidates for every universal home and every New-homes line, every _ex slot as a requires-decision finding, the four readings for unregistered root folders, slot rows and kit blocks in the kit-shaped files, a README structure copy, the .gitignore block, ONBOARDING's six parts; map findings are applied in repair mode. If the repo defines PALETTE_FILE in its CLAUDE.md, also runs the palette-consistency check across files listed in the palette's mirror section."
triggers: >-
  "audit the repo," "run the audit," "run a consistency check," "is CLAUDE.md still accurate?", "find orphaned
  files," "run the index audit"
---

# Repo Audit Skill

This skill defines how to run a consistency check across a content repo — verifying that the repo's infrastructure files (indexes, navigation tables, `CLAUDE.md`, `FOLDER_MAP.md` files) accurately describe what is actually on disk. When the repo declares an archetype, the skill *additionally* checks the repo's structure against that archetype's carried spec (Check 12). That check is different in kind from the others: Checks 1–11 verify *internal consistency* (does the repo's own documentation match the repo's own disk), while Check 12 verifies *conformance to an external standard* (does the repo match the archetype spec it declares). Both are infrastructure checks — neither touches deliverable content.

The point is to catch drift. Over time, files get added, renamed, moved, or deleted, and the surrounding infrastructure that points at them does not always get updated in step. An audit pass finds the gaps so they can be repaired in one focused session, rather than tripping over them piecemeal during normal work.

**What this skill is, and what it is not.** The boundary is **infrastructure claims vs. deliverable quality**. This skill verifies that the repo's infrastructure tells the truth — both *structurally* (documentation matches disk: Checks 1–12, run in report-only or repair mode) and *in what it claims* (index rows, register rows, and `FOLDER_MAP` descriptions still state what is currently true: the index audit, run in its own mode on its own cadence). It never judges the work itself — whether a paper is well-argued, a draft well-written, an analysis sound. A stale status label on an entry whose state has since changed is an infrastructure defect, not a content judgment; that is the line. Check 12 widens "infrastructure" to include the repo's *structure* measured against its declared archetype spec, and the index audit widens it to include the *currency of infrastructure claims* — neither crosses into deliverable quality. *(This boundary replaces the prior structure-vs-content line, which deferred claim currency to "the separate index-system revision"; that revision is settled — the archetype layers now define each index's role — and the index-audit mode is the deferred check, built v4.)*

This skill **is** the audit, on demand. The same checklist also runs at skill propagation (Part C Step 10 of `PROJECT_SETUP.md`, the audit pass at propagation) — a subset riding the propagation commit, once, immediately before it. One checklist, two wrappings: on demand (this skill, against a quiet repo, in report-only or repair mode) and at propagation (Step 10's pass, its approved fixes on the same atomic commit as the kit update). Neither applies a fix before the user's go. The light cleaning at every session close is housekeeping, `finish_session_skill.md`; this skill is the deep clean, run when they ask for it. *(The file was `housekeeping_skill.md` from v4.0 to v6.8: the name came from the propagation-time wrapping, and the kit's own text called the run "the audit" throughout; renamed at v6.8 to say what it is.)*

---

## When to use this skill

Read this skill when the user asks to:
- "Audit the repo" / "run the audit" / "check this repo is clean" / "run a consistency check" (the primary phrasing)
- "Are the indexes up to date?"
- "Is `CLAUDE.md` still accurate?"
- "Find orphaned files"
- "Run the index audit" / picking up `project_tracker`'s index-audit count ("last run [date]; work resumed [date], [N] days ago") (index-audit mode)

Do not use this skill for:
- Reviewing deliverable content quality.
- Checking out-of-scope folders not listed in the repo's `CLAUDE.md` audit scope.
- The close of a session ("let's do housekeeping," "let's wrap up"): that is housekeeping, `finish_session_skill.md`.

---

## Three modes

The user chooses the mode at the start of the session. If unclear, ask.

- **Report-only mode** — Report findings, propose no fixes, make no commits. Useful when the user wants to see the picture before deciding how to repair, or when running the audit as part of a broader review.
- **Repair mode** — Report findings, propose fixes per finding, apply on per-finding approval, commit at the end. Useful when the user wants to clean the repo in one pass.
- **Index-audit mode** — the dedicated per-entry currency check ("The index audit" section, after the checklist). Not a run of the Steps 1–5 checklist: it has its own protocol, is inherently interactive (findings adjudicated live, per finding), and ends in a single atomic commit of approved fixes plus the `STATUS.md` date stamp. Invoked by `project_tracker`'s cadence count, by your canonical kit's maintenance campaign if you keep one, or directly ("run the index audit"). Per-entry verification is deliberately kept out of the routine audit pass so that pass stays cheap.

Report-only and repair can shift mid-session: a clean run may end with the user saying "repair these three." Switch modes on the user's word and continue; a fix is never applied before their go. The index audit is its own session type and does not fold into a regular pass.

---

## Repo-specific parameters

The repo's `CLAUDE.md` provides project-specific values for the parameters below, in its **Repo parameters** table (`CLAUDE_template.md`; the single home for every parameter the always-active skills read, backfilled by Part C Step 7.5). If the table does not define a parameter, use the default given here. `none` is a legal declared value; a parameter that is neither declared nor defaulted makes the check that reads it report **skipped: undeclared** in the audit report — never a silent skip. `KIT_FOLDER` is `skills/`, the kit's flat folder; a `skills/general_skills/` still on the tree is the retired split layout, flattened at the pass (`structure_conventions.md`, "Skills layout"). Every derivable row (`KIT_FOLDER`, `INDEX_FILES`, `PALETTE_FILE`, the `AGENT_OUTPUTS_*` rows) is re-derived from the tree at every pass, and a declared value the tree falsifies is reported as **wrong**, never as *skipped: undeclared*.

Declarations live in the repo's table; this table documents what the skill reads and its fallback.

| Parameter | Description | Default |
|---|---|---|
| `INFRASTRUCTURE_FILES` | List of repo infrastructure files to check | `CLAUDE.md`, `README.md`, all `FOLDER_MAP.md` files |
| `INDEX_FILES` | Repo-level index files (e.g., `MATERIALS_INDEX.md`, `PAPERS_INDEX.md`) | None — skip the index-consistency check if not defined |
| `DELIVERABLE_FOLDERS` | Folders containing deliverables that should be referenced from infrastructure. **When the repo declares an archetype, this is derived from the declared spec** (the deliverable/output homes it defines), discovered via the repo's `FOLDER_MAP.md` files — not the hardcoded default. The default below is the fallback for `type: NONE` and pre-archetype repos. | the content homes the root map's skeleton block names |
| `KIT_FOLDER` | Where generic skills live in this repo | `skills/` |
| `PALETTE_FILE` | Canonical color palette file. If defined, the palette-consistency check (Step 2, Check 8) runs against this file and the consumers listed in its "Files that mirror this palette" section. | None — skip the palette-consistency check if not defined |
| `AGENT_OUTPUTS_FOLDER` | Agent-research dives folder. If defined, Check 9 (agent-outputs workflow invariants) runs against it. | None — skip the agent-outputs check if not defined |
| `AGENT_OUTPUTS_INDEX` | Topic-grouped tracker for agent dives, consulted by Check 9. | `<AGENT_OUTPUTS_FOLDER>/INDEX.md` if `AGENT_OUTPUTS_FOLDER` is defined; otherwise None |
| `AGENT_OUTPUTS_LESSONS` | Cross-dive error patterns and prompt-engineering responses, consulted by Check 9. | `<AGENT_OUTPUTS_FOLDER>/LESSONS.md` if `AGENT_OUTPUTS_FOLDER` is defined; otherwise None |
| `EXCLUDED_PATHS` | Paths to skip during the audit (per-repo exceptions) | None |

The audit checks `INFRASTRUCTURE_FILES` for internal consistency, cross-checks `INDEX_FILES` against the contents of `DELIVERABLE_FOLDERS`, verifies references inside `KIT_FOLDER` resolve, and (when `PALETTE_FILE` is defined) verifies palette consumers stay in sync with the canonical palette. When `AGENT_OUTPUTS_FOLDER` is defined, Check 9 additionally verifies workflow invariants in the agent-research dives folder. Paths in `EXCLUDED_PATHS` are skipped entirely.

---

## Workflow

### Step 1 — Triage

Confirm:
1. The repo's `CLAUDE.md` exists and is readable.
2. The audit parameters are defined (or the defaults apply).
3. The user has chosen report-only mode or repair mode.
4. **The index-audit date (cross-reminder; report-only and repair modes).** Read `STATUS.md`'s "Index audit last run" date; a missing slot or `(never)` reads as never run. Anchor on the first commit to `main` after that date (no commit since the audit: nothing fires). If today minus the anchor exceeds `INDEX_AUDIT_INTERVAL` (default 30 days; the parameter lives in `project_tracker_skill.md`, set per-repo in `CLAUDE.md`), surface once, with the count: "the index audit was last run [date]; work resumed [anchor date], [N] days ago; your canonical kit's maintenance campaign runs it, if you keep one — otherwise the index-audit mode in a dedicated session." Prompt-don't-perform; the regular pass does not absorb the index audit.
5. **The archetype declaration.** Read `CLAUDE.md`'s `archetype.type` frontmatter. If it is research, Check 12 runs against the archetype-common layer (`archetype_conventions.md`) **and** the one carried `*_archetype_spec.md`; note the `variant` for that check. If `type: NONE`, Check 12 is skipped (a NONE repo carries neither). If there is no declaration at all (a pre-archetype repo), Check 12 does not run; surface this once as a migration gap (the repo predates the archetype system) rather than checking against a guessed archetype — and `DELIVERABLE_FOLDERS` falls back to its hardcoded default.

If `CLAUDE.md` is missing or the repo structure does not match what's expected (no `skills/` folder, no `FOLDER_MAP.md` files), surface this immediately — the audit cannot proceed against an incoherent baseline. Suggest running `PROJECT_SETUP.md` Part B first.

### Step 2 — Run the checklist

These are ported from `PROJECT_SETUP.md` Part C Step 10, extended to cover cross-folder reference consistency.

1. **Root `CLAUDE.md` — skill table consistency.** Every file in `KIT_FOLDER` either has a row in `CLAUDE.md`'s skill table or has been intentionally excluded. No rows reference files that don't exist. Cross-references in working conventions and trigger maps point to files that exist.

2. **The root `FOLDER_MAP.md` — the kit blocks against disk.** The skeleton block names every root folder on disk or the extras register does; every folder the block names exists; the root-documents block matches the root files; the latent-homes block lists the born-on-demand homes not yet born. (`CLAUDE.md`'s Repository Structure is a pointer to the root map since v6.4; a structure table or tree still there is retired form, a Check 14 finding.)

3. **`FOLDER_MAP.md` files and the standing documents — navigation tables.** Any navigation tables or file lists match the folder's actual contents. Entries point to files that exist; files in the folder are listed (or intentionally omitted), read by the first cell of each row under the kit header (`FOLDER_MAP_template.md`, the catalog); a row kept for a departed entry, a count or a date in a row, and a subfolder re-listed where its typed index registers it are findings too; the same holds for a `leaf` folder's own files: where a typed index registers them, the map's one pointer row is the whole catalog, the files are read against the index, and a file re-listed in the map is a finding. The same reading runs on every catalog document among the standing documents of `workspace/` and `workdesk/` (`standing_documents_template.md`): a row without its file and a file without its row are findings, except a `packages/` row dated sent, whose folder is deleted by design. A standing document missing its markers, carrying a live "Empty = ..." claim, or sitting as a `README.md` beside the skill's `INDEX.md` in one folder is stale form, reported to the conformance pass (Check 14). Findings are repair-mode items (the close-out's catalog refresh in `project_tracker_skill.md` is the write side; this check is the backstop).

4. **`README.md` — the form and its one claim.** The file is in the template's form (`README_template.md`: the name, the paragraph in its slot, the kit sentence and the form comment in the template's current text, the `unplaced` slot), and the paragraph does not contradict `CLAUDE.md`'s Project Overview (twins, not copies; a contradiction is Requires decision). A README carrying a folder tree or table is drift: the root map holds the structure (`structure_conventions.md`, root files); a pointer list, a root-files list, a collaborator line, a conventions or repo-access section, or a date or version line is retired form, each with its home in `PROJECT_SETUP.md` Step 7.5 part 2.

5. **`INDEX_FILES` — entry-to-file correspondence.** Every file in the relevant `DELIVERABLE_FOLDERS` either has an entry in its index file or has been intentionally omitted (e.g., archived, excluded). No entries point to files that don't exist. **Index *content* (the state cells, the `About` cells) is not checked in this pass** — only structural presence of entries; claim currency is the index audit's job (its own mode, its own cadence).

6. **Cross-folder reference consistency.** When a deliverable folder is referenced from elsewhere (e.g., a `Drafts/` file cites a paper in `papers/`, a `FOLDER_MAP.md` in `reference/` points to a file in `inputs/`), the referenced file exists. This is the main extension beyond the propagation-time audit pass.

7. **Skill-to-skill cross-references inside `KIT_FOLDER`.** If a skill file mentions another skill by filename, the referenced file exists in `KIT_FOLDER`. Match whole filenames — a name that is a substring of another is not a hit.

8. **Palette consistency (if `PALETTE_FILE` is defined).** When the repo has a canonical color palette, read `STATUS.md`'s Cluster activations block first and flag a missing consumer only where its cluster is active; a deactivated pair's absent files are the curated state. Then verify:
   - **Completeness:** every color defined in any file listed under "Files that mirror this palette" exists in the canonical palette. No color silently introduced in a consumer without being added to the palette first.
   - **RGB consistency:** the RGB / hex value for each named color is identical across the palette and every consumer. No drift in values.
   - **Name consistency:** no consumer defines a color under a name not present in the palette (catches missed renames, like a stale `AccentLight` after rename to `AccentSoft`).
   - **Sync header presence:** every consumer file listed in the palette's "Files that mirror this palette" section has a header comment naming the palette as canonical source. Missing or out-of-date headers are findings.
   - **Asset references resolve:** asset files referenced in the format skills or preambles (logos, background images, and similar) exist in the `KIT_FOLDER`.
   - **Skill ↔ preamble pairing:** every format skill referenced in `CLAUDE.md` that has a paired preamble file points to an existing preamble; every preamble file that exists is pointed to by some skill (no orphan preambles).

9. **Agent outputs folder consistency (if `AGENT_OUTPUTS_FOLDER` is defined).** When the repo has an agent-research workflow (per `agent_research_verification_skill.md`), verify:
   - **File-set completeness:** every dive folder under `AGENT_OUTPUTS_FOLDER` contains at least a `_prompt.md` and `_raw.md` pair. A dive folder with only one of the two is flagged (partial dive).
   - **Naming convention:** every file in a dive folder matches the `YYYYMMDD_HHMM_{prompt,raw,retrieval,workflow_notes,verification}.md` convention (the five-file set of `agent_research_verification_skill.md`; `_workflow_notes` is lazy, `_verification` the only citable one). Files that don't match (loose drafts, unprefixed notes) are flagged.
   - **INDEX bidirectional consistency:** every dive folder has a corresponding row in `AGENT_OUTPUTS_INDEX`; every row in `AGENT_OUTPUTS_INDEX` points to an existing dive folder. No orphan rows; no unindexed dives.
   - **Verified rows have verification docs:** every row in `AGENT_OUTPUTS_INDEX` marked `verified` has a `_verification.md` file in its dive folder.
   - **Superseded rows reference replacement:** every row marked `superseded` names which row supersedes it in the Notes column.
   - **LESSONS.md exists if any verification doc references error patterns:** verification docs include a "Patterns in the agent's errors" sub-section. If any verification doc lists patterns observed in two or more dives, `AGENT_OUTPUTS_LESSONS` should exist. (This is a workflow-invariant check — see note below.)

   **Note on workflow-invariant checks.** Check 9 was the kit's first audit check that enforces *workflow invariants* (INDEX↔folder consistency, verified-rows-have-verification-docs) rather than passive existence. Check 10 (added v2.1.13) is the second — STATUS.md cluster-activations block must stay in sync with actual `skills/` contents. **The rule-of-three threshold is now at two-of-three.** If a third workflow-invariant check is added, extract Checks 9, 10, and the new one into a separate `workflow_audit_skill.md` that this skill invokes. (Check 11, the cluster-completeness invariant, also does **not** count — it is a kit-only architectural invariant, not an operational workflow-invariant check. And Check 12, added later, is a *conformance* check, not a workflow-invariant one — it does not count toward this threshold either; its own extraction path is noted in Check 12.)

10. **Cluster activations consistency (STATUS.md block vs. `skills/` contents).** STATUS.md carries a `Cluster activations (current)` block recording which clusters of the kit are active in this repo (see `skills_curation_skill.md` and `STATUS_template.md`). Verify:
    - **Block presence:** STATUS.md has a `## Cluster activations (current)` section. If absent in a repo whose `skills/` exists, flag — STATUS.md is out of date with the curation discipline.
    - **Optional-cluster consistency:** for each of the four optional clusters (Source material; Writing and deliverables; Voice and style; Final-production formats), the block's stated activation matches actual file presence in `KIT_FOLDER`. If "Source material: active" but no source-material files are present, that's drift; if "Voice and style: inactive" but a voice profile is present, also drift. A file the block declares declined ("active, less `<file>`", `skills_curation_skill.md` Step 7) is not reported as missing; the declined file present in `KIT_FOLDER` is drift.
    - **Final-production sub-state:** the format-pair sub-entries (Academic paper LaTeX, Academic slides, Deck reconciliation, plus any format-pair the repo has added of its own) match actual file presence per format.
    - **Always-active group:** verify all always-active skills are present. Missing always-active files are findings regardless of what the block says.
    - **`Last curated:` field is present** and parses as a date (or is the initial-template value "not yet curated").

11. **Cluster completeness invariant (kit-side check only).** Run this check only when the repo *is* the canonical kit source — the one repo where the kit is authored and from which it propagates, and where `KIT_FOLDER` therefore points at the canonical package. There, verify the kit honors the cluster completeness invariant: every skill's hard dependencies (workflow steps that invoke another skill as a required action) resolve within the always-active group or within the source skill's own cluster.
    - **Cross-cluster reference scan:** for each skill file in the canonical package, find references to other skill files. Classify each reference by source and target cluster.
    - **Soft references are not violations.** Descriptive prose, "see also" notes, hand-off references, and audit-target references do not break the invariant. Only references that look like workflow invocations ("invoke X," "follow X Step N," "calls X to do Y") are flagged.
    - **Surface ambiguous references for human judgment.** If a reference is borderline, surface it as `Requires decision` rather than auto-classifying.
    - **In every repo that is not the canonical kit source, skip Check 11.** Content repos consume the kit; they don't define the cluster structure. If you keep no canonical kit repo at all, this check never runs.
    - **Kit-only architectural invariant — does not count toward the rule-of-three.** Check 11 enforces a structural property of the kit itself, not an operational workflow invariant (Checks 9, 10), so it does **not** count toward the threshold for a `workflow_audit_skill.md` extraction.

12. **Archetype conformance (if an archetype is declared).** When `CLAUDE.md` declares `archetype.type` as research (per Step 1), check the repo's *structure* against the one archetype spec it carries. Skipped for `type: NONE` and for pre-archetype repos (surfaced as a migration gap in Step 1, not checked).

    **How the check reads the layers.** Read `archetype.type` → load **both** the archetype-common layer (`archetype_conventions.md` — the shared invariants: born-minimal promotion, origin-based typing, the shared-spine test, by-subject keying, the fixed skeleton) **and** the single carried `*_archetype_spec.md` (the type-specific structure, index set, and placement) → compare the repo to them along the fixed dimension frame below. The dimensions are owned by this check; the *content* of each dimension is read from the loaded layers — the shared invariants from `archetype_conventions.md`, the type-specific form from the spec's prose and structure diagram. Do **not** hardcode any one archetype's specifics into this skill, and do **not** name a repo's indexes or folders — discover them from the repo's `FOLDER_MAP.md` files, the same archetype-blind move the kit's other skills follow. This is the one skill that reads the conventions/spec layers at runtime; it reads the shared layer plus the repo's own carried spec.

    - **Structure** — the repo's folders against the archetype's **tagged birth tree** (`<archetype>_setup_scaffold.md`, the one manifest; `structure_conventions.md`, "Conformance"), read by tag: a `[U]` home absent is drift; a `[P]` home absent under a present parent is drift; an `[E]` home is judged by its condition — absent after the condition is a finding, present before it never is; a `[J]` home is never flagged. **Existence alone is never a pass:** for every home the CHANGELOG's New homes lines name, the **same-job check** runs (predecessor names, map descriptions, characteristic contents) and a folder elsewhere doing the home's job is a Requires-decision finding even when the kit's folder exists (the installer failure an audit can miss: a root `admin/` beside an empty `workdesk/admin/`). A folder that fits no line of the tree gets one of the four extras readings (Check 14).
    - **Index set** — does the repo carry the index **set** the spec defines (set membership, discovered via the root map's root-documents block and the `FOLDER_MAP`s — never by hardcoded name), each in the form of `typed_index_template.md` (the form findings are Check 14's). Index *content freshness* is **not** checked here — that is the index audit's job (its own mode, its own cadence).
    - **Placement** — inputs and deliverables sit in the homes the spec defines.
    - **Naming** — folder and file naming against `naming_conventions.md` and the spec.

    **Severity follows the spec's own invariant-vs-latitude line.** The spec deliberately leaves per-repo latitude. Flagging that latitude as drift is a false positive. So: **drift fixes** (mechanical, auto-proposable in repair mode) are naming-convention violations, a missing *required* index from the set, and a missing *required* folder. **Requires-decision** items are structural extras and placement judgment — distinguishing a legitimate per-repo specialization from real drift needs the user's judgment, which the audit doesn't have. Net: most Check 12 findings are Requires-decision, the inverse of the consistency checks.

    **A different kind of check — and a seed.** Check 12 is conformance-to-an-external-standard, not the internal doc-matches-disk consistency of Checks 1–11, and it is **not** a workflow-invariant check — it does **not** count toward the Check 9/10 rule-of-three for a `workflow_audit_skill.md` extraction. It lives here because the audit is the repo's one comprehensive on-demand instrument. If a lightweight sibling materializes (the tracker's freshness check, Pass 2, checks the same declaration, prompt-only), or if further conformance checks accrete, extract Check 12 into its own always-active `archetype_conformance_skill.md` that both this skill and `finish_session` invoke — at that point the shared logic justifies the extra file. The accretion condition was met at v6.4 (Checks 13 and 14 are conformance checks, and Part C Step 7.5 runs the same definition) and **was judged and re-deferred** — v6.4 gave the shared definition one home in the floor ("Conformance: one home per job"), so extracting would add a file to every repo and remove no restatement. **The trigger now:** a **fourth** conformance check accretes, or a conformance check must run outside this skill and Step 7.5. Until then the three checks and the pass stay here.

13. **Module consistency (if the repo carries or declares modules).** Skip (report N/A) when `CLAUDE.md` has no `modules:` block and no `MODULE.md` exists on disk outside a `last_module_update/`. Otherwise — the mirror of `PROJECT_SETUP.md` Part C Step 10 item 8, so a standalone audit sees what propagation checks: the `modules:` declaration rows and the CLAUDE.md Modules roster block name the same set as the `MODULE.md` files on disk, with matching homes and versions, nested modules carrying their own row with the full home, each card in the `MODULE_template.md` form with its `this copy` row naming the pair whose resolved home is the file's own folder (a card still carrying a changelog section or a `corpus` field is pre-v6.5 form, fixed at the next propagation, reported here); every module home has its `last_module_update/` baseline and a labeled-empty `corpus_inbox/`. A module found with no declaration row, or declared with no `MODULE.md`, is **Requires decision** — a module is never removed on Claude's call (Part C Step 2.6). Like Check 12, this is a declaration-conformance check, not a workflow-invariant one — it reads the shared-state `modules:` declaration against disk (`structure_conventions.md`: "shared state read by propagation and the audit, like the archetype declaration") and does **not** count toward the Check 9/10 rule-of-three.

14. **Kit conformance — the homes and the kit-shaped files (every repo, NONE included).** The on-demand form of Part C Step 7.5, the conformance pass (`PROJECT_SETUP.md`), reading the same definition (`structure_conventions.md`, "Conformance: one home per job"). Runs in every repo — a NONE repo against its universal homes and its declared skeleton block — so it is separate from the archetype-only Check 12, whose structure dimension covers the archetype tree. The finding classes, each with its severity:
    - **Same-job candidate** (Requires decision): a folder doing the job of a universal home (the workdesk, `feedback/`, `writing_notes/` — a `general/notes/`, a `workspace/notes/`, a bare `notes/` — `staging/`, `packages/`, `inputs_from_team/`, `quarantine/`) or of a home a New homes line names, whether or not the kit's folder exists. Never moved by the audit. A funding instrument's own `feedback/` (`funding/<instrument>/feedback/`) is not a candidate: it is the floor's one other feedback home.
    - **`_ex` slot** (Requires decision, always): every `<name>_exN` folder at any level is listed with a proposed resolution — a kit home it maps to, a registered extra, or a kit change — and a third slot at one level is also reported as a kit finding for the canonical skills repo.
    - **Unregistered root folder** (Requires decision): each root folder in neither the skeleton block nor the extras register gets one of the four readings proposed (same job as a kit home; unplaced material, to staging; a unit missing its skeleton; a genuine extra, to register); the extras count is reported against the cap of two, never enforced.
    - **Slot row vs. manifest** (Drift fix): a map's slot row disagrees with the kind or stage the manifest and the declaration give the folder, or carries a word outside the closed list of `FOLDER_MAP_template.md`; a content folder without its map where the leaf rule requires one (a map is born with its folder); a `Type:`/`Stage:` header line, a heading beside the slots, or a trailer stack still present; a map below the roots of `workspace/` or `workdesk/`, or an orientation map that restates the floor or the standing documents. Conformance of a map is tested by the presence of the slot row (`Kind:`), never by the absence of a named predecessor header — a repo's own restructure may have written a third form.
    - **Kit block missing or stale** (Drift fix): a `kit` block or `slot` marker absent from a marked file, a kit block whose form is not the template's (`FOLDER_MAP_template.md` for a map: the list form, the fixed empty line), a `STATUS.md` or `CLAUDE.md` header carrying a `Prior:` stack, a `CLAUDE.md` Repository Structure section carrying a table or tree, a `CLAUDE.md` with no trailer line at all (a finding, never read past), content sitting in an `unplaced` slot (reported, Requires decision for the content itself).
    - **A typed index's form** (Drift fix; Requires decision where content moves): an index whose head is not the template's three sentences for the archetype (`typed_index_template.md`), a header row not the template's for that kind, the `index` or `unplaced` marker absent, a `#` column or a row-number cross-reference, a date or count in a row, a `Created ... (skeleton)` or `Last updated` line in place of the trailer, a section heading with no rows; and, Requires decision, content in place of pointers (a summary inside or below a paper's row, an intake narrative in a materials row), a paper registered in both the materials and the papers index, a lowercase catalog at root not in the root-documents block.
    - **README structure copy and retired form** (Drift fix): a folder tree or table in `README.md`; a pointer list, a root-files list, a collaborator line, a conventions or repo-access section, a date or version line, or the kit sentence not in the template's current text (Step 7.5 part 2 names each form's home).
    - **The `.gitignore` block** (Drift fix): absent or not the kit's current text.
    - **ONBOARDING's six parts** (Drift fix for a missing part or a missing Review line; Requires decision for a Review line still reading "draft" or a "read `ONBOARDING.md`" row still standing in a collaborator's *Waiting on* table after their first `LOG.md` entry): where a collaborator's `ONBOARDING.md` exists. The assignment part's date is written once at join and is never stale.
    - **Map findings are applied in repair mode**: Check 3's catalog findings (maps and standing documents) and this check's slot-row and kit-block findings are drift fixes the audit writes on approval; the session close-out keeps maps current between audits (`project_tracker_skill.md`, the touched-catalog refresh).
    Like Checks 12 and 13, this is a conformance check, not a workflow-invariant one, and does not count toward the Check 9/10 rule-of-three.

For each check, record findings as either:
- **Drift fix** — A reference no longer matches reality and the fix is mechanical (rename a stale reference; remove a row for a deleted file; add a row for an existing file missing from the table). In repair mode, these are proposed as one-line fixes.
- **Requires decision** — A finding where the right fix is not obvious (an orphaned file might be intentionally orphaned or genuinely stale; an index entry might be intentionally minimal). These get surfaced for the user regardless of mode.

### Step 3 — Report findings

Produce a structured report.

```
Audit pass — N findings across M checks:

Check 1 — CLAUDE.md skill table:
  Drift fixes (auto-proposable in repair mode):
    - [file]: [what was found, proposed fix]
  Requires decision:
    - [file]: [what was found, options]

Check 2 — ...

...

Summary: N drift fixes proposed, K requires-decision items surfaced.
```

If there are zero findings: report "Audit pass — clean." Done.

In **report-only mode**: present the report. Done. Do not propose or apply fixes.

In **repair mode**: proceed to Step 4.

### Step 4 — Repair (repair mode only)

For each drift fix:
1. Show the user the proposed fix.
2. Wait for the user's go; nothing is applied before it. They may say "yes," "no, surface this," or "yes but change to X."
3. Apply approved fixes to local staging.

For each requires-decision item:
1. Present the options. Common options include:
   - **Update the reference** to point to where the file actually is.
   - **Delete the reference** if the referenced file is gone for good.
   - **Add the reference** if a file exists but is unindexed and should be.
   - **Surface as orphan** if the file exists but its disposition is unclear (the user may want to invoke `materials_processing_skill.md` or `document_processing_skill.md` on it, move it, or delete it — but **the audit does not auto-invoke other skills**; surfacing is the audit's job, deciding is the user's).
   - **Mark as intentional** — add a one-line note in the relevant `FOLDER_MAP.md` or index file documenting that the file is intentionally excluded.
2. Apply the user's decision to local staging.

Once all findings are resolved, proceed to Step 5.

### Step 5 — Commit (repair mode only)

Single atomic commit covering all approved fixes.

Commit message:

```
Audit-driven repair: M drift fixes, K decisions

- [file]: [what was fixed]
- [file]: [what was fixed]
- ...

Findings surfaced but deferred: J items (see audit report in conversation).
```

If items were surfaced and explicitly deferred by the user (not resolved this session), note them in the commit message so the audit trail is preserved.

---

## The index audit (index-audit mode)

The dedicated currency check on what the repo's infrastructure **claims**. Where Checks 1–14 verify structure cheaply in one pass, the index audit verifies **per entry** that live claims still hold — which is heavy, so it runs as its own session, against a quiet repo, on the cadence `project_tracker_skill.md`'s close-side read enforces (`INDEX_AUDIT_INTERVAL`, default 30 days).

**Scope — live claims, never records.** Staleness applies only to **live claims** — fields that say "this is true now": status labels, reliability tags, summary lines, `FOLDER_MAP` description slots, live register rows. **Records** — fields that say "this was true then": log lines (e.g. a branch register row's merge annotation), frozen `Standing:` slots, superseded-but-retained register rows — cannot go stale: their append/freeze semantics are exactly what the universal nothing-destroyed-on-a-state-change rule (`structure_conventions.md`) retains, and this audit never touches them. Also out of scope: `STATUS.md` (the freshness check owns it) and — always — deliverable quality.

**Discovery is archetype-blind.** Find the surfaces from the repo's `FOLDER_MAP.md` tree and the typed root indexes the declared spec defines — never by hardcoded name. What each index's fields *claim* is read from the head and the header row the index carries (`typed_index_template.md`: the state cell per kind — `Claude status` and `User status`, `Stage`, `Verified`, `Used in`, `Reliability` — is the live claim; `About` is a claim about the subject, falsified when the thing is about something else; `Where` and `Forms` are existence claims Checks 3 and 5 already cover) and from the conventions/spec layers behind it (`archetype_conventions.md` typed-index behavior; the carried spec). The staleness frame above is owned by this mode, the same way Check 12 owns its dimension frame.

**A seed (extraction path).** This mode is the audit's first **content-aware** instrument — it reads what entries *claim*, not only whether files exist. The collaborator-push capture backstop this paragraph once anticipated (the audit detecting and indexing collaborator pushes on the owner's behalf) is served since v6.2 by the collaborator `LOG.md` ledger and the pull-request route (`structure_conventions.md`, "Collaborators") — pushes arrive announced, not detected. If a content-aware capture is ever still needed, it and the index audit are the family that extracts together into its own skill; until then the mode stays here.

**The protocol — three passes, then one commit:**

1. **`[unreviewed]` sweep.** Collect every index row carrying the trailing `[unreviewed]` marker (written by `project_tracker`'s close-side entry refresh when the user had no time to review). Present them grouped for review; on approval the marker comes off, with any corrections applied.
2. **Evidence pass.** For live-claim fields whose **targets** show commit activity since the "Index audit last run" date in `STATUS.md` (commits to `main` — the same authoritative source the freshness check uses; work that never landed in a commit is invisible by design: *if it matters, leave a trace in the repo*), compare the claim against the target's current state and **propose a rewrite per finding**, evidence cited. **First run on a repo: no baseline date — the evidence pass is full**, every live claim against every target; it doubles as the population/baseline pass for a repo adopting the discipline.
3. **Interview pass — always full.** Claims only the user can falsify (a line at `under_review` whose journal decision has arrived) leave no repo trace, so this pass never scopes down: sweep them and ask, batched by kind ("these two lines are under review — any decisions?").

**Severity.** The standard two categories, with the distribution inverted even harder than Check 12: **drift fix** only when a claim is falsified by unambiguous repo evidence with an obvious rewrite; **requires decision** for everything else — the entire interview pass by construction. Prompt-don't-perform throughout: nothing is rewritten without per-finding approval.

**Close and write-back.** One atomic commit: the approved fixes **plus** today's date stamped into `STATUS.md`'s "Index audit last run" slot. The stamp travels with the fixes — a stamp without them would claim an audit that didn't finish. The stamp is what silences `project_tracker`'s close-side reminder; no confirm-stamp step remains.

---

## Composition with other skills

This skill **surfaces findings**; it does not **act on them** by calling other skills. When an orphan file is detected and the user decides "this paper needs to be processed," the user invokes `materials_processing_skill.md` separately. The audit's job ends at surfacing.

Reasoning: the right action for any given orphan depends on context the audit doesn't have (is this paper still relevant? was it dropped intentionally? does it duplicate something else?). Auto-invoking a pipeline would prejudge the answer. The audit reports what it sees and lets the user decide.

---

## Notes on scope

- **Generic skill, propagates to all content repos.** Each content repo's `CLAUDE.md` configures the parameters (or accepts defaults).
- **Quiet-repo audit.** Most findings will be structural drift, not propagation artifacts. The check distribution will look different from `PROJECT_SETUP.md` Step 10's audit pass at propagation — fewer rename-stale references, more "this folder grew and the FOLDER_MAP.md didn't keep up."
- **Repair commits are separate from propagation commits.** Audit-driven fixes go in their own commit, not folded into a propagation commit. This keeps the audit trail clean and avoids mixing kit updates with repo repairs.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
