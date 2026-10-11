# Standing documents — the template (workspace/, workdesk/, feedback/)

The standing document of every `workspace/` and `workdesk/` subfolder, the workdesk queue, and
the `feedback/` seed. Every one is written for Claude and read at four moments: the user's
retrieval phrase ("do we have a visual we can use," "I remember a brainstorm about," "what is
pending on my workdesk"), the owning skill's step (a save, a dive, a carryover), the close-out
(the catalog refresh, the queue reconcile) and the audit (Check 3). Their job is location: what
the repo already holds, so nothing is redone and nothing is searched blind
(`structure_conventions.md`, "Who these files are for"). The document also persists its folder
in git; that is a side effect of the job, not the job.

**One discipline, two kinds.** The kit owns the head (the title in path form, one purpose line
naming the owner and the file form, the resting state as a permanent fact) and every table
header; the repo owns the rows and its notes. A **catalog document** carries one row per file
or stem, refreshed by the close-out's touched-catalog rule like a map's catalog
(`project_tracker_skill.md`, "Catalog refresh"); a **label** carries no catalog,
because its contents are transient or named elsewhere. Where a skill owns the folder's index
(the conversations index, the agent-outputs pair) the header is the skill's and this file
points. The fill rules — create where missing, regenerate the head and the header, keep the
rows, pour an existing document's prose into `notes` — are `PROJECT_SETUP.md` Step 7.5 part 2,
never here.

**Markers** (`structure_conventions.md`, "Slots and markers, one notation"): `slot: catalog`
around the table, whose header row is kit form regenerated at every stop and whose rows are the
repo's; `slot: notes` for what the repo wants to say about the folder; `slot: unplaced` in every
document, empty in the normal state. The trailer line on a catalog document is rewritten in
place by the close-out; a label has none. Where a body below reads `<!-- ... -->` outside the
markers it is a placeholder and is not copied.

---

## `workspace/brainstorms/README.md` — catalog document

```markdown
# workspace/brainstorms/ — saved brainstorms

Saved brainstorms, one file per brainstorm (`YYYY-MM-DD_<topic>.md`): the idea, the
alternatives weighed, the direction chosen or deferred (`brainstorming_skill.md`). Resting
state: empty until a brainstorm is saved.

<!-- slot: catalog -->
| Date | Topic | Where it landed | File |
|---|---|---|---|
<!-- /slot -->

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

## `workspace/branch_logs/README.md` — catalog document (the catalog is the branch register)

```markdown
# workspace/branch_logs/ — the branch register and the exploration trails

Every branch that carries repo content, exploration or writing, a collaborator's included:
registered when it is opened, annotated when it merges or is abandoned, so a session finds work
that lives on a branch without scanning git (`structure_conventions.md`, "Exploration-branch
artifacts"; the row is written by `exploration_branch_skill.md` or `writing_branch_skill.md` at
creation). The raw `BRANCH_RESEARCH.md` trail of a merged exploration is filed here as
`<branch-ref>.md`; the distilled review lives in the merged folder's `FOLDER_MAP.md`. Resting
state: no branch open and no trail filed. Status reads `open`, `merged YYYY-MM-DD into <path>`
or `abandoned YYYY-MM-DD`; Extends is the folder or workstream the branch hangs off.

<!-- slot: catalog -->
| Branch | Opened | What it holds | Extends | Status | Trail |
|---|---|---|---|---|---|
<!-- /slot -->

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

## `workspace/visuals/README.md` — catalog document (where `visuals_workflow_skill.md` is active)

```markdown
# workspace/visuals/ — visuals in progress

Figures, diagrams and charts for markdown deliverables, one stem per visual (`<stem>_SKETCH.md`,
then the rendered files), worked here until embedded in the final format and kept afterwards
as the starting point for the next visual, so none starts from zero
(`visuals_workflow_skill.md`). The repo's register of
images is the archetype's `ASSETS_INDEX` where it has one; this catalog is the reuse shelf.
Resting state: empty until a visual is started.

<!-- slot: catalog -->
| Date | Stem | What it shows | For | Stage |
|---|---|---|---|---|
<!-- /slot -->

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

## `workspace/packages/README.md` — catalog document (the catalog is a ledger)

```markdown
# workspace/packages/ — outbound packages

Repo material assembled into delivery formats for someone outside the repo, one
`<recipient>_package/` per recipient: the build script tracked, the copied files and zips
gitignored, the folder deleted once the package is sent (`structure_conventions.md`, "The
outbound packages home"; the `sent` event on each product is `product_ledger_skill.md`'s).
Resting state: empty until a package is assembled. The catalog is the record of what went out
and when: a row is added when a package is assembled, dated when it is sent, and stays after
the folder is deleted. The assembling session asks whether the package goes out today; a row
still without a send date is put to the user at the next session start
(`project_tracker_skill.md`, step 0).

<!-- slot: catalog -->
| Assembled | Recipient | What it held | Sent | Build script |
|---|---|---|---|---|
<!-- /slot -->

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

## `workspace/step_reports/README.md` — label (where `workstream_plan_skill.md` runs a scoped plan or a standalone blind step)

```markdown
# workspace/step_reports/ — the blind-session inbox

Reports written by blind sessions, `REPORT_<plan_stem>_S<N>_<YYYYMMDD>.md` for a plan's step and
`REPORT_<stem>_<YYYYMMDD>.md` for a standalone prompt, each read by the coordinating session's
report sweep and retired under its last-call review, never edited (`workstream_plan_skill.md`,
Parts D and E). Resting state: a report not yet swept is work waiting for the plan's session;
nothing here is a record once swept.

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->
```

## `workspace/step_prompts/README.md` — catalog document (the catalog is the register of standalone blind steps)

```markdown
# workspace/step_prompts/ — standalone prompts and their reports

The prompts handed to a blind session outside any plan's step table, `PROMPT_<stem>_<YYYYMMDD>.md`,
one row each, paired with the report that answered it in `step_reports/`
(`workstream_plan_skill.md`, "Standalone blind steps"); with no plan file to log the step, this
register is the trace. Resting state: empty until a standalone prompt is filed. A row with no
report is a session not yet run; a row whose report was retired keeps the report's date.

<!-- slot: catalog -->
| Date | Prompt | Question | Report | Status |
|---|---|---|---|---|
<!-- /slot -->

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

## A `workspace/<name>/README.md` the kit does not name — label (the generic body)

A `workspace/` subfolder of the repo's own — a ledger, an extraction pile, a design pile, a
vocabulary pass — carries this label, written by the session that creates the folder from the
folder's job and regenerated in form at the pass; the pass never derives a label by hand, and a
`workspace/` subfolder never carries a map (`structure_conventions.md`, "workspace/"). Where the
folder's files are worth finding one by one, the repo gives the label a `slot: catalog` with the
columns it needs, stated in the head; the head and the markers stay kit form.

```markdown
# workspace/<name>/ — <the folder's job, one phrase>

<What goes here and what it is for, one or two sentences; the owner — a repo convention named in
`CLAUDE.md`, a project skill, or the session that made it — and the skill or workflow that reads
it.> Resting state: <the permanent fact: empty until X; accumulates; cleared when Y>.

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->
```

## `workspace/staging/README.md` — label

```markdown
# workspace/staging/ — the intake funnel

Everything new to the repo lands here first, under the zero-decision drop rule, and leaves
through the placement check (`structure_conventions.md`, "The intake funnel"; the lightning
check and the placement triggers in `CLAUDE.md`). Resting state: empty; anything here at a
session's close is waiting to be placed.

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->
```

## `workspace/multisession_active_tasks/README.md` — label

```markdown
# workspace/multisession_active_tasks/ — carryovers

The live state of a task that spans sessions: one `MULTISESSION_CARRYOVER_<task_stem>.md` per
task, named in its workstream's `STATUS.md` entry (the Resume field), and the unseen-close
transcript until its retake (`multisession_task_skill.md`; `project_tracker_skill.md`, the
unseen close); a campaign's `CONFORMANCE_ITEMS.md`, this repo's ruled conformance items,
seeded before the campaign and deleted in the repo's campaign commit, named in the `repo`
entry. Resting state: empty; a file here is a task in flight.

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->
```

## `workspace/claude_conversations/INDEX.md` — the skill's index

The body is the Index format in `repo_conversations_skill.md` ("Index file"), which carries the
markers: the title and the lookup line, then the table inside `slot: catalog` (the `Who` column
present where `USER_IDS` is defined; a `Who` column standing where `USER_IDS` is `none` is
dropped at the pass, its one value kept in the row's text if it says something), then
`slot: notes` (the tag vocabulary and the threshold
choice, when made), then `slot: unplaced`. Rows are added at every save; the
header row is regenerated at every stop, so a column the skill adds reaches every repo.

## `workspace/agent_outputs/INDEX.md`, `LESSONS.md` and `WORKFLOW_SKIPS.md` — the skill's triple (where `agent_research_verification_skill.md` is active)

The bodies are the three headers in `agent_research_verification_skill.md` (the INDEX header
with its citability rule and status values; the LESSONS header; the skips register's header
and table header under "Cross-dive pattern detection"), which carry the markers: the header,
then the per-topic sections, the entries or the rows inside `slot: catalog`, then
`slot: unplaced`. All three are read together at the session start of a dive, so all three
are created up front where the skill is active, the register with its header row and no rows.
*(Documented predecessor, to v6.5: the register was born on use, at the first skip's
commit; a session-start read that finds
no file cannot tell an unlogged skip from none.)*

## `workdesk/INDEX.md` — the queue

```markdown
# workdesk/INDEX.md — what is waiting on the user

The repo's one queue of what waits on the user: read · think · decide · do (the closed list,
`structure_conventions.md`, "workdesk/"). A row points at the
artifact where it lives; nothing is moved here to be queued. Any session adds a row the moment
something starts waiting; the close-out reconciles the queue (`project_tracker_skill.md`); the
criterion is `structure_conventions.md`, "workdesk/". Empty means nothing is waiting.

<!-- slot: catalog -->
| Item | Action | Artifact — where | Since | Added by | Status |
|---|---|---|---|---|---|
<!-- /slot -->

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->
```

## `workdesk/admin/README.md` — catalog document

```markdown
# workdesk/admin/ — user-facing deliverables

Administrative and personal deliverables produced for the user to use, not repo content: a
reference letter, a nomination, travel paperwork (`structure_conventions.md`, "workdesk/").
Resting state: empty until one is produced.

<!-- slot: catalog -->
| Date | Document | For | File |
|---|---|---|---|
<!-- /slot -->

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

## `workdesk/postits/README.md` — catalog document

```markdown
# workdesk/postits/ — the user's post-it notes

The user's post-it notes: what they write for themselves, never indexed. A note that is repo
content — a set the writing-notes skill produces, feeding deliverables — is the other kind and
lives in `writing_notes/` under `NOTES_INDEX` (`structure_conventions.md`, "workdesk/" and
"`writing_notes/`"). Resting state: empty until they write one.

<!-- slot: catalog -->
| Date | Note | About | File |
|---|---|---|---|
<!-- /slot -->

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

## `workdesk/collaborators/README.md` — label

```markdown
# workdesk/collaborators/ — one folder per collaborator

One folder per person with access other than the owner, `<id>/`, created on join with the
collaborator's queue, `ONBOARDING.md` and `LOG.md`. The roster is `CLAUDE.md`, Collaborators;
the convention is `structure_conventions.md`, "Collaborators". The files inside `<id>/` — the
queue `INDEX.md`, `LOG.md`, `admin/README.md`, `postits/README.md` — are the collaborator's own:
the kit fixes no body for them, only the `LOG.md` Decisions block form (the convention above),
and the pass regenerates nothing inside the folder. Resting state: empty until a collaborator
joins.

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->
```

## `feedback/FOLDER_MAP.md` — the seed (a map: its form is the floor's FOLDER_MAP form)

The file takes the `FOLDER_MAP.md` form (`FOLDER_MAP_template.md`: title, slot row, kit
blocks, description and catalog slots, one trailer); `feedback/` is a category (per-person
subfolders). What this template fixes is the kit block, regenerated whole at every stop, and the
catalog's columns, which here replace the map's `Path | What is here` header.

```markdown
# FOLDER_MAP — feedback

Kind: category

<!-- kit: feedback_split -->
Feedback received from people on the repo's products: one subfolder per person, dated entries
inside (or a dated series folder where a series has its own convention). Every entry is a
pair: the **raw record**, `YYYY-MM-DD_<topic>_RAW.md`, the feedback as it arrived — the email,
the meeting notes, the user's recollection as they told it — filed on arrival and never edited;
and the **worked entry**, `YYYY-MM-DD_<topic>.md`, written in the session where the user gives
their reading and rules. Until then the entry is raw only. Four things happen when feedback
arrives, in four places. The **record** is the pair here, durable. The **wait** — the user deciding what to do with it — is a `workdesk/INDEX.md`
row pointing here (Action: decide), cleared on absorption. The **link**, where a product ledger
exists, is the ledger's `feedback` event pointing here, open until dispositioned
(`product_ledger_skill.md`). The **version**, on the first feedback on a document, is the
byte-exact copy of what went out, cut into `versions/` beside the document
(`structure_conventions.md`, "Versions vs. archive"). Resting state: empty until feedback is
received. Feedback on a funding instrument is not filed here: it lives in the instrument's own
folder (`funding/<instrument>/feedback/`), named in this map's description.
<!-- /kit -->

<!-- slot: description -->
<!-- /slot -->

<!-- slot: catalog -->
| Date | From | On what | Raw | Worked entry |
|---|---|---|---|---|
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->

*Last updated: YYYY-MM-DD — <what changed>*
```

---
<!-- Kit file marker below: the template's own version line, not part of any repo file. -->
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
