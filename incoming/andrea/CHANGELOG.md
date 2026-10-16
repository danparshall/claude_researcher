# Starter Package Changelog

This file records the version of the starter package — a curated, scrubbed
subset of a canonical skills kit, for sharing with collaborators who are new to
working with Claude in a repo-based setup.

The starter's version scheme (v0.1, v1.0, v2.0, …) is separate from the
canonical kit's. The starter's version reflects how the starter itself is
curated and organized; the kit version it was mirrored from is named in each
entry below.

---

## v2.5 — October 10, 2026 — Two kinds of repo: research and general purpose

**Mirrored from kit v6.11**, as v2.4 was: the canonical kit did not move. This version changes what the package offers, not what it mirrors. The package now describes two kinds of repo. **Research** is the one archetype it ships, with its spec and its birth tree. **`NONE` is the general-purpose kind**: any repo that is not a research repo. It carries the universal layer and a skeleton tailored to its own work.

### What left

- **Four files**: `coordination_archetype_spec.md`, `coordination_setup_scaffold.md`, `operation_archetype_spec.md`, `operation_setup_scaffold.md`. The package goes from 55 files to 51.
- **Every passage that named the two archetypes**, in twenty files, and the machinery only they used: the `task` and `reform` map kinds and the instance-layout block; the `tasks:` and `layout:` declaration keys; the layout tag of the birth trees (the legend has four tags now); the instances index, the sub-product spine, the reference index and the positions register in `typed_index_template.md`; the session-close feedback prompts of the coordination archetype; the module trigger that was a task unit.

### What changed in the files that stay

- **`NONE` is defined wide.** Earlier versions described it as a tracker or a lookup, a repo too particular for any reusable skeleton. It now takes every repo that is not research, a repo that produces deliverables included (`archetype_conventions.md`, `structure_conventions.md`, `README.md`). The declared value is still `NONE`.
- **One question at birth** (`new_repo_setup.md`, `PROJECT_SETUP.md` Phase 3): is the work lines of inquiry that build up literature and evidence toward papers or analytical outputs? Yes is research; anything else is `NONE`. For a `NONE` repo the skeleton is proposed from the answers, confirmed, and written in the root map's skeleton block.
- **The three-layer model stays**, with one archetype in it: the universal floor, the archetype-common layer (`archetype_conventions.md`), the spec (`research_archetype_spec.md`). The middle layer is kept as its own file because its rules are the ones any archetype shares; an archetype you add later leans on it and writes only its own spec.
- **The folder-skill rule stays whole** (`structure_conventions.md`, "Skills layout"; `skill_authoring_skill.md`): a skill that serves one piece of work lives next to that work, and a skill with its own corpus is a folder with the corpus inside it. This is the path for a general-purpose repo whose work is one task done many times.
- **Rules that were cited to a spec that left keep the rule and move the citation**: the reliability and confidentiality labels are defined in `document_processing_skill.md`, and in a research repo they enter the materials index once the document branch is active; supersede-but-retain is the floor's rule ("Nothing is destroyed on a state change").
- **`typed_index_template.md`** keeps two worked examples, both research: the materials index empty at birth, and an outputs index with two lines and rows.

### A second read for what identifies

Every file was read line by line, first line to last, by five readers, for anything that identifies an author or an organization. The earlier passes had searched the older text of the long files; this one read it. About 110 small fixes followed: real dates and counts in provenance notes, quoted remarks given as the reason for a rule, labels of the canonical kit's own internal work, and a few examples replaced by invented ones.

### After the release: the colors of the two LaTeX preambles

The color block of `academic_slides_preamble.tex` and `academic_paper_preamble.tex` no longer carries fifteen fixed RGB values. It asks for a palette: four base colors (three hues and a gray), shipped with generic placeholder values, and the shades derived from them with `\colorlet`. Six colors that no theme setting and no skill used are gone (`DarkYellow`, `MintGreen`, `BrightBlue`, `BrightYellow`, `BrightGreen`, `DeepGreen`); `LightGray` is new; the eight names the slide theme and the skills use are unchanged. `academic_slides_skill.md` and `academic_paper_latex_skill.md` describe the palette and say to ask for the four base colors before the first real deck or figure. The block was checked by reading and was not compiled; it uses the standard mixing syntax of `xcolor`.

### Verification

By script over the 51 files: no file of the two archetypes named, no citation to their specs, none of their indexes, keys or tags, outside this changelog's own history; the v2.4 identity checks unchanged and clean; every file LF. By two independent reviewers who read the result against v2.4: leftovers, dangling references, counts, over-cuts, and the general-purpose kind followed end to end from the birth question to the audit.

### If you set a repo up from an earlier version

A repo declared `coordination` or `operation` under an earlier version is not covered by this one. Do not run Part C from v2.5 on it: the curation step would treat its spec as a stray. Keep it on the version it was built from.

---

## v2.4 — October 10, 2026 — Re-mirror from kit v6.11, and a stricter scrub

**Mirrored from kit v6.11.** The package sat at a mirror of kit v6.5 since September 7, 2026; the canonical kit moved through six versions after it, and this pass brings every shipped file to the v6.11 state, scrubbed. Same audience and framing as v2.0 to v2.3. The bump is MINOR: one file added, one renamed, none deleted. Method: the v2.2 three-way merge per file (base the kit at the v2.3 mirror commit, ours the package, theirs the kit now; all three sides read from git objects, LF output), 156 conflicts resolved toward the kit side with the scrub re-applied to the incoming text, every trailing marker set by rule.

### What's new

- **`latex_round_trip_skill.md`** (Final-production formats) — the review round trip for a paper whose live LaTeX source is edited outside the repo with co-authors: the review copy regenerated each round, the register of edits the user applies by hand, the refreshed copy read by diff. Ships with the LaTeX paper pair.
- **`repo_audit_skill.md`** replaces `housekeeping_skill.md` (the kit's rename): the deep consistency check of a repo, run on demand. "Housekeeping" now names the light cleaning at every session close, `finish_session_skill.md`.

### What changed in the shipped files

- **Placement is a lookup** (`structure_conventions.md`, the import and processing skills): a kind the repo already has a home for is placed and registered without asking, and only a kind with no declared home, or a probable duplicate, is proposed.
- **The hand-over mode** of `cross_repo_import_skill.md`: material with a single home repo is imported by the home, and only then does the sending repo retire its copy, under four rules.
- **The project record** (`project_tracker_skill.md`): `RECORD.md`, the project as one thing, by category, beside the per-workstream `STATUS.md`.
- **The collaborator convention widened** (`structure_conventions.md`, `ONBOARDING_template.md`): the five events of a collaborator's work and the owner's review of a collaborator's decisions.
- **`skills/` is flat**: the kit's files loose in it, `last_skill_update/` inside it; the split layout is retired and Part C migrates it.
- **The standing documents, the maps and the typed indexes** in their current forms (`standing_documents_template.md`, `FOLDER_MAP_template.md`, `typed_index_template.md`), with the fill rules in `PROJECT_SETUP.md` Step 7.5.
- **The verification skills**: the retriever step and the held-work definition in `agent_research_verification_skill.md`; the companion-document mode in `own_document_verification_skill.md`.
- **The translation review** covers a deliverable written in Spanish from the start, the in-chat round and the design-tool round.

### What was excluded, and why

The v2.0 to v2.3 exclusions stand: personal voice profiles, the personal palette, the email skill, the institution-specific format pairs with their assets, the kit's own changelog, the strategy-documents home (cut at section grain, including its new per-archetype form and the import skill's strategy case), and the modules' canonical copies. Two tables that the kit fills ship empty, as before: the Known agent failure modes table and the translation corrections log.

### The scrub

The v2.3 rules, applied to the incoming text by five executors against a written rules file, then read in full by three independent reviewers with the kit's text beside them, whose findings were ruled on and applied. This pass is stricter than the earlier ones in four ways, and each was applied to the whole file, not only to the incoming text:

- **No institution is named anywhere**, a list of example publishers included. A named publisher, database or tool is described by its kind; a filename example uses an invented acronym.
- **No anecdote of real work.** A provenance note that carried a date, a count, a file name or a quotation is cut; the rule it explained stays. A *Documented predecessor* note stays where it states only what the earlier rule was.
- **Examples are neutral.** A worked example, a slug, a sample row or a correction pair that came from one person's field is replaced by an invented one of the same shape.
- **Module names are placeholders** (`<module>`), and an organization's own names for its funding instruments are generic ("a grant, a commissioned study, a terms of reference").

A public scholar's surname in a paper-stem or citation example stays; a colleague's does not.

### Verification

By script over the 53 mirrored files: no author name, colleague, institution, country, private repo name, kit-factory path or strategy-home term; no author pronoun outside a quoted example utterance; every file LF; every marker the v2.4 sentence; no conflict marker left; `extract_design_deck_mirror.py` compiles and differs from the kit's copy in one docstring line and one message string. By the reviewers: every skills-table and Appendix row names a shipped file and every shipped skill has its rows.

### Ruled for v2.5

The next version narrows the package to two kinds of repo: the **research** archetype, and **NONE**, the general-purpose kind that carries the floor only. The operation and coordination archetypes leave: `operation_archetype_spec.md`, `operation_setup_scaffold.md`, `coordination_archetype_spec.md`, `coordination_setup_scaffold.md`, and every passage in the other files that names the two. They are still in this version.

### Markers

Every shipped `.md` file ends in the one-sentence starter marker, now naming kit v6.11 and October 10, 2026.

---

## v2.3 — September 7, 2026 — Re-mirror from kit v6.5 (the conformance design, the template rework, the kit sweep)

**Mirrored from kit v6.5.** The package sat at a mirror of kit v6.3 (with its rider) since
September 5, 2026; the canonical kit moved through v6.4 (the conformance design) and v6.5
(the template rework, the `writing_notes/` home, the kit sweep) in the two days after, and this
pass brings every shipped file to the v6.5 state, scrubbed. Same audience and framing as v2.0
to v2.2; the bump is MINOR because the refresh is additive: five files added, no renames, no
deletions. Method: the v2.2 three-way merge per file (base the kit at the v2.2 mirror commit,
ours the package, theirs the kit now; index content on all three sides, LF output), 38 marker
conflicts resolved by rule, 105 others taken from the kit side with the scrub re-applied to the
incoming text, one kept from the package (the added-format slot in the curation skill's
activation block).

### What's new

- **`FOLDER_MAP_template.md`, `README_template.md`, `standing_documents_template.md`,
  `typed_index_template.md`, `gitignore_seed.md`** (bootstrap) — the forms of every folder map,
  the repo README, the standing documents of `workspace/`, `workdesk/` and `feedback/`, every
  typed index, and the `.gitignore` block; each created at setup and regenerated in form at
  every propagation.
- **The `triggers:` frontmatter key** in every shipped skill and convention file (49 files): one
  string, the phrases and conditions that fire the read. `CLAUDE_template.md`'s When to use
  cells are verbatim copies of it, and the propagation copies the cell from the key.

### What changed in the shipped files

- **The conformance definition** (`structure_conventions.md`: "Who these files are for",
  "Conformance: one home per job", the tagged birth trees as the one manifest, slot and kit
  markers, latent homes, the New homes line); Part C Step 7.5 as the conformance pass, with
  the fill rules of every kit-shaped file; `housekeeping_skill.md` Check 14.
- **The templates rebuilt under the cost model:** `CLAUDE_template.md` (the How to start and
  Project skills slots, the three-part workflow sections, the two-column skills tables, the
  length target in words); `STATUS_template.md` (one entry per workstream, rewritten in place;
  Recent sessions and three other sections retired to their homes); `ONBOARDING_template.md`
  (six parts, written for the person); the maps and typed indexes in their drawn forms.
- **`writing_notes/`** at root in every repo, `NOTES_INDEX` the one universal index,
  `workdesk/notes/` renamed `postits/`; the archetype rulings (the six research stage words,
  `empirics/`, the submission channel, the coordination `layout` key, promotion as a structural
  act, a module's maps as the repo's).
- **The marker chain capped:** every file ends in the one-sentence starter marker, and the
  kit-file history paragraphs the v2.2 package kept (the floor, the specs, the scaffolds, the
  naming floor) go with it.
- **The tracker family:** the branch register (replacing `BRANCHES_LOG.md`), the packages
  ledger with the asked send, the feedback raw/worked pair, the same-commit rule for kit
  feedback, the Known agent failure modes table (empty in the package).

### What was excluded, and why

The v2.0 and v2.2 exclusions stand. The kit's rebuilt Skills tables re-listed the excluded
voice, email, format and palette files; cut again, the Voice and Shared assets clusters keeping
their bring-your-own paragraphs in the new two-column form. The strategy-documents home's line in
the three birth trees and its two parameter clauses in Step 7.5 are cut at the same grain as
v2.2. The modules' canonical copies do not ship; module names stay as examples of the tier.

### The scrub

The v2.2 rules re-applied to the incoming text by three executors against a written rules
file, the package's diff read whole by the session. Decisions kept: "the user" by default and
"the owner" inside the collaborator convention; provenance parentheticals and campaign
bookkeeping deleted; kit-factory paths hedged as "your canonical skills repo, if you keep one."
New this pass: role, unit and place names in examples and in `triggers:` keys were made
generic. One exception stands by rule: a third party's pronoun inside a quoted example utterance.

### Verification

By script over the 49 shipped `.md` files: no author name, institution, private repo name or
kit-factory path; no author pronoun outside a quoted example; every file LF; every marker the
v2.3 sentence; no conflict marker left; every skills-table row and Appendix row names a shipped
file and every shipped file has its rows; every reference to the five new templates resolves.

### Markers

Every shipped `.md` file's trailing marker is the one-sentence starter-package-edition note,
now naming kit v6.5; no file carries a history paragraph any more.

---

## v2.2 — September 5, 2026 — Re-mirror from kit v6.3 (with its same-day rider)

**Mirrored from kit v6.3.** The package had sat at a mirror of kit v5.0 since August 4, 2026;
the canonical kit moved through v5.1, v6.0, v6.1, v6.2 and v6.3 in the meantime, and this pass
brings every shipped file to the v6.3 state, scrubbed. Same audience and framing as v2.0 and
v2.1; the bump is MINOR because the refresh is additive: four new files, no renames, no
deletions.

### What's new

- **`product_ledger_skill.md`** (always-active) — the per-product `<stem>_LEDGER.md`: which
  representation of a product is current, where they diverge, what has been sent, presented,
  or decided. `writing_skill.md`'s triage now routes outside-the-repo edits to it.
- **`design_deck_reconciliation_skill.md` + `extract_design_deck_mirror.py`** (Final-production
  formats) — placing and reconciling a deck built in a design tool against the repo's own
  markdown, with the paired extractor. The "design tool keeps the markdown text" rule rides in
  this skill and in `academic_slides_skill.md`.
- **`ONBOARDING_template.md`** (bootstrap) — the template for a collaborator's first document,
  part of the collaborator convention below.

### What changed in the shipped files

- **The collaborator convention** (`structure_conventions.md`, `CLAUDE_template.md`,
  `PROJECT_SETUP.md`, `STATUS_template.md`, `project_tracker_skill.md`,
  `finish_session_skill.md`, `writing_branch_skill.md`, `github_api_workflow_skill.md`,
  `repo_conversations_skill.md`, the three scaffolds): `workdesk/collaborators/` in every repo,
  the per-person folder, the roster in `CLAUDE.md`, the three rules (own folder is the only
  direct write on `main`; everything else a `<id>_br_<topic>-<date>` branch and a pull request),
  whose-session-is-this at session start, the collaborator close, and Part C Step 2.7 (the
  access reconcile).
- **The tracker family**: the date-only STATUS header with the three-state flag
  (`reviewed | unreviewed | unseen`), the `STATUS_ARCHIVE.md` split, the index-audit cadence
  count, the navigation-label refresh, the Repo parameters table in `CLAUDE_template.md`
  (`none` is a legal value; the audit reports skipped checks), the two-axis coordination
  declaration (`tasks` and `variant`), Part C Step 7.5 (reconcile STATUS.md and CLAUDE.md
  against the templates), the curated-table branch in Step 7, and `housekeeping_skill.md`
  v3.x (Check 13 module consistency, Check 3 label reads, Check 9's five-file list).
- **The universal floor**: `feedback/` (created up front, scaffolded and registered by Part B,
  Part C Step 8.5 and the birth trees), `workspace/packages/` (the outbound sibling of
  staging), versions vs. archive, the product-ledger registration, `STATUS_ARCHIVE.md` in the
  root-file set.
- **The module tier** (`structure_conventions.md`, `CLAUDE_template.md`, `STATUS_template.md`,
  `PROJECT_SETUP.md`, `skill_authoring_skill.md`, `skills_curation_skill.md`,
  `housekeeping_skill.md`): a third propagation tier — folder packages a repo carries because a
  structural trigger is present, never through curation. Kept, with its addresses generalized
  (see the scrub).
- **Skills**: `writing_branch_skill.md` conventions 3, 4, 11 and 12 (the branch belongs to the
  reviewer from handover to round close; read-then-exact-replace; round-count checkpoints; a
  version is cut at the feedback intake); `writing_drafting_skill.md` (the presenter question,
  Compressions); `writing_notes_skill.md` (the document on screen is the referent, recording
  the source, explicit approval); `workstream_plan_skill.md` + `BLIND_SESSION.md` (blind steps
  without a plan, the counting rule); `agent_research_verification_skill.md` v4.2.0 (the
  five-entry pass); the materials trio's "From the visual layer" summary item;
  `visuals_workflow_skill.md` (delete scaffolding at hand-off); `cross_repo_import_skill.md`
  v3.x; `naming_conventions.md` (the date-boundary ruling); the operation spec's eight root
  indexes with the feeding-process rule; the research spec's current-shape block and line-level
  archive; `PROJECT_SETUP.md`'s parallel-agent protocol for multi-repo waves and the Phase 4
  label fix.

### Unchanged

Eight files had no kit change since v5.0 and are untouched: `academic_paper_latex_skill.md`,
`brainstorming_skill.md`, `exploration_branch_skill.md`, `multisession_task_skill.md`,
`own_document_verification_skill.md`, `new_repo_setup.md`, `translation_review_skill.md`,
`translation_corrections_log.md` (still ships empty). The two `.tex` preambles keep their
self-contained color blocks: the kit added one accent color to its palette mirrors, and nothing
this package ships uses it.

### What was excluded, and why

The v2.0 exclusions stand (personal voice profiles, the personal palette, the email skill, the
institution-specific format pairs and their assets, the kit's own CHANGELOG). Two additions:

- **The canonical strategy-documents home** (kit v6.3): one organization's strategy documents,
  a single source repo, a per-archetype home, and the parameter that points at it.
  Institution-bound by nature. Left out at section grain: the floor section, the parameter
  row, the import case, and the three spec tree mentions.
- **The by-environment pointer to the docx skill** (the v6.3 rider) lives only in an excluded
  format skill, so it lands nowhere in this package; no shipped file carries the bare path it
  replaced.

### The scrub

Every refreshed file went through the v2.0 scrub again, applied to the incoming kit text only
(a three-way merge carried the v2.0 scrub decisions forward on unchanged passages). Four
decisions were new this pass:

- **The module tier stays, generalized.** The registry and canonical copies live in the kit
  author's kit repo; the package points at "your canonical skills repo, if you keep one," the
  same phrasing the v2.0 pass used for the discovery sweep and consolidation.
- **The owner is a role.** The collaborator convention distinguishes the repo's owner from other
  people with access. Where the kit says the author's name in that sense, the package says
  "the owner" (`*For the owner*`, the Merge value `owner`); everywhere else the name is "the
  user," as before. The reading rule follows: in a collaborator's session "the user" is the
  human present, and a decision a rule routes to the owner becomes a *For the owner* row.
- **The index-audit cadence points at a campaign you may not have.** The kit's cadence count
  points at a maintenance campaign run from the kit repo. The package keeps the count and says:
  point at your canonical kit's maintenance campaign, if you keep one; otherwise run the index
  audit in a dedicated session.
- **Provenance parentheticals go.** Rulings dated to a private repo's gate, campaign
  bookkeeping, and example paths into private repos were deleted or neutralized rather than
  renamed.

### Consistency audit (same day, after the commit)

Seven read-only checks over the refreshed package: every file reference against the shipped
set; the Files-to-copy list, the Appendix inventory, and the `CLAUDE_template.md` skills table
against the 49 files; the universal folder set at every site (the floor, Part A, Part B, Part C
Step 8.5, the three birth trees); the STATUS cluster-activations block across its three sites;
the Repo parameters table against the parameters the skills read; section-name and step-number
cross-references against existing headings; the reading rule and the owner vocabulary across the
collaborator files. Two findings, both fixed in the follow-up commit: `STATUS_template.md`'s
Final-production sub-entries still listed a Word format-pair the package does not ship (a v2.0
leftover), now the two academic pairs plus the added-format slot, matching the Step 7 block in
`skills_curation_skill.md`; and that skill's always-active roster sentence omitted the repo
structure conventions the block names. Everything else agreed.

### Markers

Every shipped `.md` file's trailing marker is the one-sentence starter-package-edition note,
now naming kit v6.3. The files with a kit-file history paragraph (the floor, the specs, the
scaffolds, the naming floor) keep it, scrubbed, with the clauses about excluded content removed.

---

## v2.1 — August 4, 2026 — Marker standardization pass

The v2.0 review found the version-marker treatment inconsistent: three files
had their kit-maintenance histories compressed to a short note, while the
other shipped files carried their full histories, scrubbed but intact — dense
with worklist numbers, internal commit hashes, and consolidation-cycle
bookkeeping meaningless outside the kit's home repository.

This pass standardizes: every shipped `.md` file's trailing marker is now the
same one-sentence starter-package-edition note, naming the kit version the
file was mirrored from (v5.0) and inviting the collaborator to record their
own changes in the marker from there on. The full histories remain available
in the canonical kit. The two `.tex` preambles keep their own short markers —
those document this package's deliberate divergences from the kit versions
(self-contained color block, no logo overlay), which a collaborator may
actually need. `README.md` and this file keep their own package-native
history.

---

## v2.0 — August 3, 2026 — Re-mirror from kit v5.0, with the scrub pass restored

**Breaking change in framing — the audience returns to collaborators.** v1.0 was
a wholesale, unscrubbed mirror of the canonical kit, aimed at the kit author's
own use when seeding new repos. v2.0 returns to the v0.1 framing: a curated,
**scrubbed** subset for external collaborators. Personal references and
institution-specific assets are excluded again, and the surviving files are
scrubbed of personal and institutional content.

The own-use case that v1.0 was built for is now served differently — by taking a
plain snapshot of the canonical kit directly, with no curation. That removed the
reason v1.0 existed, and freed this package to be a genuine collaborator package
again.

**Mirrored from kit v5.0.** The package had been sitting at a mirror of kit v3.0
and had drifted badly: no archetype layer, five files still under names the kit
had since renamed or split, and roughly a dozen v4/v5 skills missing entirely.

### What's new

- **The archetype layer** — `archetype_conventions.md`, the three archetype
  specs (`research_`, `coordination_`, `operation_archetype_spec.md`), and the
  birth tools (`new_repo_setup.md` plus the three `*_setup_scaffold.md` files).
  A repo now declares a type at setup and is structured against it.
- **Structure conventions** — `structure_conventions.md` and
  `naming_conventions.md` as the universal floor beneath the archetype layer.
- **New skills** — `own_document_verification_skill.md`,
  `multisession_task_skill.md`, `workstream_plan_skill.md`, `BLIND_SESSION.md`,
  `cross_repo_import_skill.md`, `visuals_workflow_skill.md`,
  `translation_review_skill.md` + `translation_corrections_log.md`,
  `housekeeping_skill.md`, `exploration_branch_skill.md`.

### Renames and splits carried over

Files whose kit sources were renamed or split are present under their new names
only; the old names are gone:

| Old (v1.0) | New (v2.0) |
|---|---|
| `audit_repo_skill.md` | `housekeeping_skill.md` |
| `branch_workflow_skill.md` | split into `writing_branch_skill.md` + `exploration_branch_skill.md` |
| `paper_processing_skill.md` | `materials_processing_skill.md` |
| `AboutFolder.md` (repo-side) | `FOLDER_MAP.md` |

The kit also moved to lowercase folder names, which the shipped files now
prescribe.

### What was excluded, and why

Twenty kit files did not cross into this package:

- **Personal voice and style profiles** (four) — a voice profile captures how
  one specific person writes. The Voice and style cluster survives as a
  bring-your-own cluster.
- **The personal color palette** — likewise personal. The Shared assets cluster
  survives as bring-your-own, and the two LaTeX preambles were made
  self-contained: each preamble's own color block is now the source of truth,
  with no external palette file to mirror.
- **The email drafting skill** — on inspection this is a voice profile in
  substance, naming real recipients and their registers, not a generic workflow.
- **Institution-specific format skills and preambles** (eight) — branded Word,
  branded LaTeX paper, and two branded coordination-deck variants. The generic
  academic pairs (LaTeX paper, Beamer slides) ship and were scrubbed of their
  branded counterparts' cross-references.
- **Institutional assets** (five) — two logos and three slide background images.
  The academic slides preamble's logo overlay was removed with them; the
  template now compiles with no external image dependencies.
- **The canonical kit's own CHANGELOG** — kit-maintenance history, and its
  filename collides with this file.

### The scrub

Every shipped file was scrubbed of personal and institutional content:

- Personal names replaced with "the user" / "a colleague"; pronouns
  generalized to "they".
- Institution names, real colleague names, private repo names, and
  institution-specific worked examples replaced with neutral equivalents.
- Kit-factory machinery (the cross-repo discovery sweep, consolidation) — which
  presumes a canonical kit repo the collaborator does not have — generalized to
  "your canonical skills repo, if you keep one," or trimmed. The Part A / B / C
  setup structure survives intact.
- Every reference to an excluded file removed, with the surrounding prose,
  cluster listings, and copy manifests repaired so nothing points at a file the
  package does not ship.
- `translation_corrections_log.md` ships **empty** — it is an append-only
  corpus, and the accumulated corpus was the kit author's own. The header,
  lifecycle note, and entry format ship; the entries do not.

### Why v2.0, not v1.1

The framing shift is breaking, in the same way v1.0's was. Anyone opening v1.0
expecting a full unscrubbed mirror finds a curated subset instead. The major
bump honors that.

---

## v1.0 — May 14, 2026 — Full mirror of the canonical kit at v3.0 (superseded by v2.0)

**Breaking change in framing.** v0.1 was a curated three-skill subset of the kit,
scrubbed of personal references and institution-specific assets, intended for
collaborators new to working with Claude in a repo-based setup. v1.0 was a
wholesale mirror of the canonical kit, intended as the kit author's own
project-setup kit when starting new project repos.

**The audience shift.** During the v3.0 cycle, the starter's audience was
reframed from external collaborators to the kit author's own use. With that
reframe, the "scrub for outside audience" filter no longer applied. Voice
profiles, institution-specific format skills, logos, and institution-specific
assets were all in the mirror.

**Boundary discipline preserved.** The mirror covered the canonical kit only.
Kit-maintenance workflows (discovery, consolidation, structural redesign, and the
planning docs) did not cross into the starter — they are kit-maintenance tools,
not propagation targets.

**Superseded by v2.0** (August 3, 2026), which restored the collaborator
audience and the scrub.

---

## v0.1 — May 2026 — Starter package release (superseded by v1.0)

Initial release of the starter skills kit. Contained:

- `writing_skill.md` — two-protocol writing workflow (reading/note-taking +
  drafting)
- `paper_processing.md` — paper processing pipeline for academic papers, working
  papers, and white papers
- `document_processing.md` — document processing pipeline for operational and
  institutional documents

Plus bootstrap files: `CLAUDE_TEMPLATE.md`, `PROJECT_SETUP.md`,
`how_to_write_a_skill.md`.

The v0.1 framing — a curated, scrubbed subset for collaborators new to
repo-based work — was deprecated in v1.0 and **restored in v2.0**.
