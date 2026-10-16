---
name: project-tracker
description: "STATUS.md project-level tracker for content repos — read at session start (on the user's 'yes' to a session-start check) and rewritten at session close. Holds what is open for the repo as a whole: one entry per workstream (where it stands, next move, waits on, resume), the open questions, the live known issues; nothing finished. Also runs at session close to rewrite the tracker (every task finished or given a resume record), and on demand for bootstrapping STATUS.md in a new repo. Includes a lightweight freshness check (TRACKED_LOCATIONS check at session start, per-entry staleness) that flags drift between STATUS.md and reality — distinct from the heavier on-demand infrastructure audit (repo_audit_skill.md). Does NOT save full conversations (use repo_conversations_skill.md) or store brainstorm summaries (use brainstorming_skill.md)."
triggers: >-
  Every session: the STATUS.md ask at the start, the mandatory update at close, the freshness
  check, bootstrap
---

# Project Tracker Skill

This skill defines how `STATUS.md` works as a content repo's project-level tracker — the file Claude reads at session start (on the user's "yes") and rewrites at session close. STATUS.md is the answer to "where are we?" and "what is to be done?" for the repo as a whole: where each workstream stands, what it waits on, what is undecided, what is broken.

STATUS.md holds **what is open, and nothing finished**. It is not a log: what was done lives in commits, in the indexes and folder maps, in the deliverables, and in the rulings written where they apply; a closed record rotates to `STATUS_ARCHIVE.md` at the close that closes it, and what is true of the project at the big-picture level is `RECORD.md` (below). Mechanical activity (file moves, typo fixes, routine processing) never lands in STATUS.md; a change in where a workstream stands does, by rewriting its entry.

**What this skill is, and what it is not.** This skill defines (a) the STATUS.md template and what each section is for, (b) the session-start check protocol, (c) the session-close protocol, (d) the freshness check that detects when STATUS.md has drifted from reality, (e) the bootstrap procedure for setting up STATUS.md in a new or existing repo, (f) the hierarchical-naming integration tracking that supersedes v2.1.1's stop-gap, and (g) the pending-placement-fix tracking that pairs with `CLAUDE.md`'s folder-creation placement check, (h) the lightweight structure- and stage-drift peeks the freshness check runs against the declared archetype, and (i) the session-close index-audit cadence read, and (j) the session-close workdesk-queue reconciliation (every repo, against the pending-actions queue `workdesk/INDEX.md`), (k) the session-close promotion-drift check (archetype repos since v6.4; promotion scaffolds the unit in one commit), (l) the session-close index-entry refresh (every repo; a NONE repo for `NOTES_INDEX` only) that keeps typed-index rows' live claims current — the write side of the index audit, (m) the session-close non-empty-staging prompt (every repo) — the backstop that keeps staged files visible when a Pending placement fixes entry was missed, (n) the session-close workstream position refresh and outgrowth catch (every repo) — the write side of the plan-file lookup surface (the plan-file convention itself lives in `workstream_plan_skill.md`), (o) the STATUS archive — the current/historical split (`STATUS_ARCHIVE.md`), the session-close rotation of closed records, the cite-by-name pointer rule, and the length tripwire, (p) the session-close touched-catalog refresh and the one-line map trailer (every repo), (q) the collaborator merge sweep — the `merge: owner` half at the merge, the `merge: self` half in the freshness check, (r) the **workstream entry** — one per workstream, rewritten in place, with the close line when a workstream closes — and the **close check** that every task the session touched is finished or has a resume record at one of three grades, (s) the **unseen-close transcript** — the verbatim resume record a "close now" leaves for the retake, and (t) **the record**, `RECORD.md` — where the project stands at the big-picture level, by part of the project, rewritten at close beside the entry rewrites; the one tracker file a person reads too.

It is **not** the skill for repo-wide infrastructure consistency checking — that's `repo_audit_skill.md`. The relationship: `repo_audit_skill.md` is the heavy, on-demand check the user runs occasionally to catch drift across the whole repo's infrastructure; the **freshness check** defined here is a lightweight, routine check that runs at session start (on the user's yes) against tracked locations only. Both can flag missing folders; only `repo_audit_skill.md` is comprehensive.

---

## When to use this skill

Read this skill when:
- The user says "let's pick up where we left off," "check status," "what were we doing?", "what's in flight?", "what is to be done on this project?"
- A session is about to close (the user says "thanks," "good night," "we're done," "let's wrap up," or similar).
- A new content repo is being set up and STATUS.md needs to be bootstrapped.

Do not use this skill for:
- Heavy infrastructure audits across the whole repo (use `repo_audit_skill.md`).
- Saving full conversations (use `repo_conversations_skill.md`).
- Brainstorm summaries (use `brainstorming_skill.md`).

---

## Repo-specific parameters

The repo's `CLAUDE.md` provides project-specific values for the parameters below, in its **Repo parameters** table (`CLAUDE_template.md`, the single home for every parameter the always-active skills read). If the table does not define a parameter, use the default given here.

| Parameter | Description | Default |
|---|---|---|
| `STATUS_LOCATION` | Where STATUS.md lives | Repo root (alongside CLAUDE.md) |
| `WORKFLOW_MODE` | `branches` (every workstream gets its own branch, merges via PR) or `main_only` (quick personal/scratch repos; everything happens on `main`). Read by the branch skills; its one home is the Repo parameters table *(until v6.5 it was also a STATUS.md section)* | `branches` |
| `TRACKED_LOCATIONS` | Folders and files the freshness check checks for activity since STATUS.md's last update | `workspace/brainstorms/`, `workspace/claude_conversations/`, `writing_notes/` (the indexed note sets), `workdesk/` (the queue + anything the user dropped in `admin/`/`postits/` between sessions, and — in repos with a collaborator on the roster — every `workdesk/collaborators/<id>/INDEX.md` and `LOG.md`, which collaborators write directly on `main` between the owner's sessions), all `FOLDER_MAP.md` files (recursive) — which covers the repo's content, deliverable, and index folders wherever the archetype places them — and the catalog documents among the standing documents of `workspace/` and `workdesk/` (`standing_documents_template.md`; the catalog refresh reads and writes them) |
| `EXTRA_TRACKED_LOCATIONS` | Additional repo-specific paths to include in the freshness check | None |
| `INDEX_AUDIT_INTERVAL` | How long after work resumes following the last index audit the session-close read starts counting the days out loud | 30 days |

---

## STATUS.md structure

The full template lives in `STATUS_template.md`; the fill rules the conformance pass applies live in `PROJECT_SETUP.md` Step 7.5 part 2. The sections, in order — every one present in every repo, empty where it has nothing (sections are the slots; the pass adds a missing one empty):

1. **Header line: last-updated date and review state.** Format: `*Last updated: YYYY-MM-DD — [reviewed | unreviewed | unseen]*`. Date only, no time: the freshness check anchors on the commit that last touched STATUS.md, not on the header. **Rewritten in place, never stacked:** the header carries no `Prior:` lines and no parenthetical. A propagation's record is the repo's `<KIT_FOLDER>/CHANGELOG.md` entry and the Last curated line of the Cluster activations block *(until v6.5, a Recent-sessions entry; before that, an interim "demote, never overwrite" rule, under which each propagation pushed the previous header down a `Prior:` line)*; a stack that exists rotates verbatim into `STATUS_ARCHIVE.md` at the pass. The flag records how the last close went. `reviewed`: the user read the close draft with care before commit. `unreviewed`: they read it quickly and said "commit"; the next session start surfaces it in one line and a nod clears it. Rotation rides both, since both are closes they read. `unseen`: they said "close now"; no draft was shown or explained, and the next session start shows the close's diff verbatim before anything else; nothing rotates on this path. Both clear to `reviewed` at the next session start. Below the header, one fixed line: closed records rotate to `STATUS_ARCHIVE.md`; cite by section and name.
2. **Current state.** One entry per workstream, rewritten in place (the next section). Holds the **Pending re-integrations** subsection (described below), the **Pending placement fixes** subsection (described below), and the **Index audit** record (the date the repo's index audit last ran, read by the session-close cadence check).
3. **Open questions.** Decisions to resolve, one named and dated entry each. This section absorbs what was previously the CLAUDE.md "Parking Lot" — moves here at integration time. A question closes at the close that answers it and rotates with its answer; an action waiting on the user is a queue row (`workdesk/INDEX.md`), never a question.
4. **Known issues.** What broke and the workaround, while the issue is live; a fixed issue rotates.
5. **Cluster activations (current).** Kit-owned, written by `skills_curation_skill.md` Step 7 at every propagation, never by hand: the five cluster lines and the Last curated line, rewritten in place. The archetype and the module set are in `CLAUDE.md`'s frontmatter, not here. Last in the file because its readers are the curation step and the pass, not the session resuming.

*(Retired at v6.5, each with its home: **What this repo is** — `CLAUDE.md` Project Overview, read every turn, so a second copy drifted; **Workflow mode** — the `WORKFLOW_MODE` row of the Repo parameters table; **Recent sessions** — a log, whose three jobs are re-homed in the close protocol below; **Archived workstreams** — `STATUS_ARCHIVE.md`, where a closed workstream's entry lands with its close line, so no row is written. The pass retires each with its content: the paragraph checked against Project Overview, the mode value moved to the table, the table's rows rotated once, the session log rotated verbatim.)*

---

## Current state — the workstream entry

**The unit is the workstream, not the session.** Until v6.5 the close appended a dated entry per session under Current state, and the section became a log under the wrong name, where a claim answered long before could survive because no close ever re-read it. An entry is now one per workstream, and the close rewrites it.

**What a workstream is, by archetype.** Research: each line, plus `general` (the shared spine), `funding/` and `repo` (infrastructure and kit state beyond the Cluster activations block). NONE: each folder of the bespoke skeleton that carries work, plus `repo`. A workstream with no unit in the list takes the name of the folder its work sits in (a root product takes the product's stem) — the list names the usual units, never all of them. The entry is **named by its folder**, in the root `FOLDER_MAP.md`'s order, so the executor pours by name and the freshness check maps commits to entries. A folder born mid-session (the `CLAUDE.md` placement check fires) births its entry at that session's close.

**The fields, fixed:**
```markdown
- **<folder>** (as of YYYY-MM-DD) — <where it stands>. Next: <the next move, or "none
  until <event>">. Waits on: <the user | a named person | data | nothing>. Resume: <the
  carryover, plan file or unseen-close transcript, only when one exists>.
```
*Where it stands* is a few lines at most, dated: the "as of" date is the date of the last rewrite, which the freshness check reads against commits. *Next* holds the next move, including deferred Claude actions (never the workdesk queue's rows, which wait on the user and are pointed at, not copied). *Waits on* names the blocker or says nothing. *Resume* points at the resume record when the task stopped short (the close check, below); the `repo` entry's Resume field also names the repo's `CONFORMANCE_ITEMS.md` between its seeding and the campaign that runs it (the campaign's ruled items for this repo, in the carryover home; not a resume grade the close writes, and not a plan file, so the position refresh below does not read it; `structure_conventions.md`, the carryover home); a task stopped mid-step says so here — "stopped after step 2, resume from the branch" — so a retake reads as a retake. A workstream that outgrows a few lines has a **workstream plan file** living with the work (`<stem>_PLAN.md`, per `workstream_plan_skill.md`, which owns the convention — plain by default, the scoped upgrade decided by its gate), and its entry trims to a short description, the pointer in Resume, and a **one-line position** (`step 3/6 — drafting`) refreshed at session close. A dormant workstream keeps its entry, one line: dormant since when, what would resume it — it is still an option when the user asks what is to be done.

**Rewritten in place, never appended.** At every close, each entry whose workstream the session touched is rewritten whole, dated today. The session's narrative — what was tried, the reasoning, the rulings taken on the way — is not state and does not go here: rulings go where they apply (a study design's rulings sheet, a skill, a `CLAUDE.md` Project conventions bullet), reasoning worth keeping goes to a saved conversation, and the rest is in the commits.

**The close line.** When a workstream closes, its final rewrite is a close line — "closed YYYY-MM-DD: what came out, where it lives, the one thing learned if there is one" — and the entry rotates in the same close. That line is the workstream's record in the archive; `workstream_plan_skill.md`'s Retire step writes it in place of the former Archived-workstreams row. A workstream that comes back to life is reborn in STATUS from its close line, dated the day it reopens; the archive keeps the old entry.

---

## The Pending re-integrations subsection

Lives inside "Current state." This is the proper mechanism that replaces v2.1.1's stop-gap workaround.

**When it's needed.** When the repo has folders using hierarchical naming (chapter/section drafts: `A_chapter_*.md` assembled from `A1_section_*.md`, `A2_section_*.md`, etc.). The subsection is present in every repo, `(none)` where hierarchical naming is not in use.

**What it tracks.** When a section file (`A1_section_*.md`) in `main` has been edited *after* its chapter (`A_chapter_*.md`) was assembled, the chapter and section drift — the chapter no longer reflects the section's current state. This subsection lists those drift cases so the user can decide whether to re-assemble the chapter or whether the section edit is small enough to defer.

**Format:**
```markdown
### Pending re-integrations

- **[A_chapter_<topic>.md](path)** — section [A1_section_<topic>.md](path) edited YYYY-MM-DD HH:MM, chapter last assembled YYYY-MM-DD HH:MM. Re-assembly pending.
- ...
```

**How drift is detected.** Manual for v1.0 — when the user edits a section in a way they know creates drift, they tell Claude and the entry gets added. If this proves unreliable in practice (the user forgets to flag), v2 may add a commit-based inference (Claude scans commits at session start, flags edits to section files post-dating their chapter assembly). Starting manual to keep the skill simple.

**Read at session start.** When the start-of-session check runs and the user says yes, Claude reads this subsection and surfaces any pending re-integrations proactively before doing other work.

---

## The Pending placement fixes subsection

Lives inside "Current state." Pairs with the folder-creation placement check in the repo's `CLAUDE.md` Working Conventions — that check is where a deferred move gets recorded.

**When it's needed.** When a folder was created in a rush — during a session, or by the user outside one — and a placement check later finds it mis-placed or duplicative, but the user defers the fix rather than moving it then. The placement check flags it, does not move it, and records the pending move here. The subsection is present in every repo, `(none)` until a move has been deferred.

**What it tracks.** Each deferred placement fix: which folder or staged file, what's wrong with where it sits (mis-placed, duplicates an existing home, or used from staging with placement deferred), the proposed correct home, and when it was recorded. The entry persists across sessions until the move is made.

**Format:**
```markdown
### Pending placement fixes

- **`path/to/folder/`** — duplicates `other/path/` / sits outside the archetype skeleton. Proposed home: `proposed/path/`. Recorded 2026-06-06.
- ...
```

**How entries are added.** Two writers: the `CLAUDE.md` folder-creation placement check, on a deferred folder move; and the intake funnel's rushed path (`structure_conventions.md`), when a staged file is used now and placed later — that entry carries what the user said the file was plus any probable-duplicate flag from the lightning check. This subsection records; it does not decide. **Prompt-don't-perform:** recording an entry never moves anything.

**Read at session start and re-surfaced at session close.** At session start (on the user's yes), Claude surfaces any open entries proactively before other work, alongside Pending re-integrations. At session close, Claude re-surfaces any still-open entries so a deferred move isn't lost across the boundary. Either way the move is offered, never forced: remind the user the fix is still pending and ask whether to action it now — following the `CLAUDE.md` placement check to do the move and remove the entry — or leave it recorded for next time.

---

## The STATUS archive (`STATUS_ARCHIVE.md`)

STATUS.md's failure mode is unbounded growth: a long-running repo's tracker
reaches tens of thousands of tokens, a session honestly answering "yes, check
STATUS" spends a large share of its working memory before doing anything, and
sessions start routing around the file — which defeats the tracker. The fix is
a current/historical split, sharpened at v6.5 to
**open in STATUS, closed in the archive**:

- **`STATUS.md` stays open** — the workstream entries, the open questions, the
  live known issues, the kit block.
- **`STATUS_ARCHIVE.md` (repo root) holds the closed records** — rotated
  there at the close that closes them. When something beyond the open state
  is needed, that file is where to look.

**What rotates:** a closed workstream's entry with its close line; a resolved
open question with its answer written in; a fixed known-issues block; at the
conformance pass, every header `Prior:` stack and the retired sections' content
(the session log, the Archived-workstreams rows) verbatim, once. **What never
rotates:** anything still live, however old — closed-ness, not age, is the
criterion. **Conservative rule: unsure means it stays in STATUS.md.**

**Rotation is lossless and verbatim.** Entries move unchanged, under their
original section headings (mirrored in the archive; a **Headers** section
receives the rotated header stacks) and original entry names, each block
marked *Rotated YYYY-MM-DD*. Rotation never rewrites, trims, or dedups an
entry — distillation of live text is content work, gated by the user, never part
of rotation. The one line written on the way to the archive, the close line,
is written by the close that closes the workstream, before rotation.

**Born at first rotation, not up front.** A lean STATUS.md needs no archive;
the fixed line under STATUS.md's header says so from birth ("born at the first
rotation"). On first rotation: create the file with the header naming the
repo and the cite-by-name rule, and **register `STATUS_ARCHIVE.md` wherever
the repo enumerates its root files** (the root `FOLDER_MAP.md`'s
root-documents block) in the same commit.

**The cite-by-name rule.** Any file pointing at a STATUS record cites it by
section + entry name (e.g. "STATUS.md → Open questions, *Who owns the baseline
dataset*"), never by line number — rotation (and ordinary editing) breaks
line numbers, and a rotated entry keeps its name in the archive, so a
name-based pointer stays followable with one hop. When rotation moves a cited
entry, the citing pointer's location part updates to name the archive.

**The archive is cold storage.** It is not in `TRACKED_LOCATIONS`, the
freshness check does not read it, and session-start orientation never opens it
unprompted.

---

## Session-start check protocol

This is the central discipline. The flow:

0. **Whose session is this.** Before anything else, and before any tracker is read, the session establishes whether the human is the owner or a collaborator (`CLAUDE.md` Collaborators roster; in Cowork the git config name is the hint, on claude.ai web the session asks; a prompt that says who is there settles it). **The owner's session** continues below, with one addition: glance at the *Working on* block and the *For the owner* table of every `workdesk/collaborators/<id>/INDEX.md`, say in one line what each collaborator is on, and offer to take any new *For the owner* rows now or queue them in `workdesk/INDEX.md` with *Added by* naming the collaborator; and read the packages catalog (`workspace/packages/README.md`) for a row without a send date — if one stands, ask whether that package went out and when, write the date to the row and, where the product has a ledger, its `sent` event (the session that assembles a package asks whether it goes out that day, and the next session confirms). **A collaborator's session** does not run this protocol against `STATUS.md` at all: it reads `CLAUDE.md`, then its own folder — `INDEX.md` for what is waiting, and its own workstream's entry in `STATUS.md` for where the work stands (the rest of `STATUS.md` only when the task needs it) — and takes its state from there. While the "read `ONBOARDING.md`" row stands in the *Waiting on* table (the first session, or until the person has read it), the session presents `ONBOARDING.md` to the person, in the reading list's order, and clears the row at its close; otherwise `ONBOARDING.md` is not read for state. The convention is `structure_conventions.md`, "Collaborators".
1. **New session opens.** The user sends their first message.
2. **Before doing anything else, Claude asks:** *"Do you want me to check STATUS.md?"*
3. **If the user says no:** proceed with the actual request. STATUS.md is not read.
4. **If the user says yes:**
   1. Read STATUS.md. Note the last-updated date and the `[reviewed | unreviewed | unseen]` flag.
   2. If the flag is `unreviewed`: one line ("the last close was committed unreviewed on [date]") and ask for a nod. A nod flips the flag to `reviewed`; "let me see" shows the last close's changes for correction first. If the flag is `unseen`: before anything else, before the freshness check and before the summary, show the last close verbatim — the diff of the commit that last touched STATUS.md, which is the exact record of what it rewrote — and, where an entry's Resume field names an unseen-close transcript, say so; then ask whether to accept or correct. Either flips the flag to `reviewed`.
   3. Run the **freshness check** (next section).
   4. If freshness check finds no post-timestamp activity and no stale entry: STATUS.md is current. Read the orientation straight off the file: the options are the entries' Next fields, the blocked ones their Waits on fields, the decisions the Open questions; surface Pending re-integrations and Pending placement fixes. Ask the user where they want to pick up.
   5. If freshness check finds post-timestamp activity or stale entries: STATUS.md is behind. Surface what was found, entry by entry. Propose the rewrites derived from the audit findings (see below). Get the user's review/correction. Commit the updated STATUS.md. Then summarize and proceed.
5. **Then engage with the actual request.** A session that retakes a task from a Resume field reads the resume record first — the plan file (the "we are here" ritual), the carryover, or the unseen-close transcript — with the user, before deciding how to continue.

---

## The freshness check

Runs at session start when the user says yes. Lightweight; uses only the repo as source of truth. It runs three cheap passes — an activity check (Pass 1, below), then two conformance peeks (Pass 2 structure, Pass 3 stage). All three are deliberately lightweight: the heavy, interpretive archetype-conformance check lives in `repo_audit_skill.md` (Check 12), and the peeks route to it rather than duplicate it.

**Pass 1 — activity.** Inputs (both authoritative):
- **Files on disk** modified since the commit that last touched STATUS.md (the header date is for reading, not for anchoring), in `TRACKED_LOCATIONS` and `EXTRA_TRACKED_LOCATIONS`.
- **Commits to `main`** since that commit — what was committed, what files were touched, what the messages say.
- **Folders created by merged collaborator pull requests** since that commit (repos with a collaborator on the roster): the self-mode half of the merge-time sweep (`structure_conventions.md`, "Collaborators"). Any such folder outside the collaborator's workdesk territory is proposed for staging — moved into `workspace/staging/` on the owner's yes and placed by the intake check — because a `merge: self` collaborator merges without the owner's session present, and this read is the only place the new folder is caught. The `merge: owner` half runs at the merge itself (the close-out section, "Collaborator merge sweep").

**The per-entry staleness read (v6.5).** Commits are mapped to workstream folders. An entry whose folder has a commit later than its "as of" date is **stale**, named as such — "work in `<workstream folder>/` on 2026-08-10, entry as of 2026-07-27" — and its rewrite proposed. Only commits that changed **content files** under the folder count; a commit that touched only kit-shaped files (the maps, the indexes, the skills, STATUS.md, CLAUDE.md) is a propagation, a sweep or a close, not work, and marks nothing stale. A workstream with no commits stays as it is, however old its date.

**Out of scope:** past-chats search, conversation history lookup. Past chats are not the repo. If a session didn't leave a trace in the repo (no commit, no saved brainstorm, no saved conversation), the freshness check does not see it. The discipline that makes the tracker work is: **if it matters, leave a trace in the repo.** Brainstorming and repo-conversations skills are the mechanisms for leaving traces.

**Output of the check:** a list of findings, each tagged with the source (file modification, commit, or both), the entry it bears on, and a short description of what changed.

**Proposing the update.** Claude reads the findings and drafts the entry rewrites derived from them. Default approach: commits give the structural skeleton (decision X landed, file Y was created); brainstorms and saved conversations give the content; the user fills in the *why* and the *what's still open*. The proposal is shown for the user's review; they correct and approve. Then commit.

**Pass 2 — structure drift.** Read the declared archetype from `CLAUDE.md`'s `archetype.type` frontmatter and the archetype spec (`research_archetype_spec.md`). Cheap scan for the obvious: loose root files outside the spec's root-file set, folders off the skeleton, filled `_ex` placeholder slots, content folders missing a `FOLDER_MAP.md`. This is a peek, not the full audit — on any hit, surface it and route: "this looks off the archetype skeleton; run the audit's Check 12 (`repo_audit_skill.md`) for the complete picture." Prompt-don't-perform. A NONE repo (no archetype) skips this pass.

**Pass 3 — stage drift.** In a research repo, which records a stage label per line, read each line's recorded stage (wherever the spec records it) and check it against cheap progress signals — for example, a line still labeled an early stage that now has drafted outputs. If a line looks to have outgrown its label, surface: "recorded as '[stage]' but looks further along — update the label?" No new storage; the label lives where the spec already keeps it. Prompt-don't-perform. A NONE repo skips this pass.

---

## The record (`RECORD.md`)

STATUS holds what is open and nothing finished, and it answers "where
are we this week". The record answers **"where are we on this project"**, at the level above:
everything currently true of the project at the big-picture level, by part of the project,
one row per big thing, tagged by status. It is the second repo file, after `README.md`, whose
reader is a person as well as Claude: the user and Claude read it to understand where the
project is, so its register is plain, the section names are the project's words, and the What
and Why cells are sentences one would say to a colleague. Under v6.5 what was done and decided
was split five ways — commits, the close line in the archive, a plan's session record deleted
at its retirement, rulings where they apply, saved conversations — and nothing showed the
project as one thing.

```markdown
# RECORD — <Repo Name>

Where this project stands at the big-picture level: everything currently true of it, by part
of the project, one row per big thing, tagged by status. Written at the session close that
made it true; a row's status moves as the thing moves, and a row that stops being true leaves
the file (git keeps it). Open work in detail is in STATUS.md; the reasoning is where the Where
column points. The repo's own machinery (kit, structure, tooling) is not here.

Inside each part, rows are ordered by category, four, fixed: **Scope** (what the part is about
and its boundaries, who asked, what was ruled out) · **Method** (how it is done: the design, the
data, the model, the sources) · **Outputs** (the documents, decks and datasets built or to be
built, and their state) · **Outcomes** (what happened once something went out: presented,
reviewed, funded, and what came back); by date inside a category.

Status words, five: **decided** (settled, in force) · **done** (built or delivered, and
standing) · **to do** (decided to be done, not started) · **proposed** (the user's idea, no
buy-in yet) · **open** (undecided; the row names who owns the decision).

## <The part, in the project's words> (<the STATUS entry's name>)

| Category | Date | Status | What | Why | Where |
|---|---|---|---|---|---|
| Scope | YYYY-MM-DD | decided | the handbook covers the first study only; the follow-up is out (the editor) | the commission is for the first study | the scoping record of YYYY-MM-DD, 2.1 |
| Method | YYYY-MM-DD | open | the robustness workload: which later chapters run both specifications (the lead author owns) | a second specification multiplies work in every later chapter | the same record, 2.4 |
| Outputs | YYYY-MM-DD | done | the handbook outline, with its compiled outline | — | `<line>/draft/handbook_outline.md` |
| Outcomes | YYYY-MM-DD | done | the slide deck presented at the review meeting; a reviewer's feedback filed, not yet absorbed | — | the handbook's ledger; `feedback/<person>/` |
```

**The sections are the parts of the project**, in the project's words, with the STATUS entry's
name in parentheses so the two surfaces line up, in the root map's order: a research agenda's
lines, a single paper's parts (the literature review, the empirics, the draft, the submission),
a NONE repo's folders that carry work. A part with nothing big-picture standing has no section;
`repo` never has one. The funding instrument is a part.

**A row is a big thing**: a decision that shapes the part, a thing built or delivered and still
standing, a thing decided to be done that would be a workstream or a step of one, a proposal
without buy-in, a question only a named person can settle. Small steps, small to-dos and
mechanical activity never enter; the close line, the queue and the commits keep those. **The
category follows what was decided, not the artifact it touches.** Why is one clause, in the
user's words where they gave them, so the decision is not re-litigated; Where names the surface
that carries the detail (a skill, a rulings sheet, a plan, a ledger, a queue row), by name.

**Rewritten in place, like STATUS, never appended as a log.** A row is written at the close
that made it true; its status moves at the close that moves it (`to do` to `done` with that
close's date; `proposed` to `decided` or out; `open` to `decided`); a row that stops being true
— a reversed decision, an abandoned thing — leaves the file, and the new decision gets its own
row. The Date is when the row's current status became true. Git keeps every earlier state;
the file is a record, not a view: the plans and conversations its rows distill are gone at
their retirement, so it cannot be rebuilt from what remains.

**Who writes it.** The close-out (below), from the same touched set that drives the entry
rewrite: the draft carries the record's rows beside the rewrites, and every path writes them,
the unseen one included, since losing the record is worse than an unreviewed row. The plan
skill's Retire step, distilling the plan's big rulings and its outcome into rows (the close
line keeps saying what came out). The carryover's distill (`multisession_task_skill.md`).
**Who reads it.** The user, when they ask where the project is; a session asked about the
project's arc or a past decision, before it answers from memory; a plan's construction, so a
new plan does not re-decide; nobody at session start, and it is not in `TRACKED_LOCATIONS`.

**Born at the first row, not up front**, the archive's precedent: on the first row, create the
file with its head and **register it in the root `FOLDER_MAP.md`'s root-documents block** in
the same commit. The pass creates nothing and pours nothing: a repo's first rows are written by
its next close, and a hand-built record a repo already keeps
stays as the content it is and is pointed at from a Where cell.

## Session-close update protocol

The other central discipline. The flow:

1. **The user signals close.** "Thanks," "good night," "we're done," "let's wrap up," or similar.
2. **Claude derives the touched set** — the session's commits plus modified files, the same set the checks below use — and maps it to workstream folders. Those entries are the ones to rewrite; a task with no entry yet (a folder born this session) gets one.
3. **Claude drafts the rewrite.** For each touched workstream: the entry rewritten whole, dated today — where it stands, Next, Waits on, Resume. Then the **close check** (below) on each task the session worked: finished, or given a resume record. Then: every open question the session answered closed with its answer; every fixed known issue marked; a closed workstream's entry written as its close line. No entry is added for the session itself. **Then the record** (`RECORD.md`, above): walk the session for what became true of the project at the big-picture level — a decision that shapes a part, a thing built, delivered or presented, a thing decided for later, a proposal, a question opened — and draft each as a row with its category and status beside the rewrites; move the status of a row the session moved, and drop a row that stopped being true. Written on every path, the unseen one included. A session that changed no workstream's state — a capture push, a dictation, a mechanical sweep — owes no entry; its commit is the record.
4. **Claude shows the draft to the user.** *(Collaborator session: the draft is one entry — the collaborator's own workstream's entry, short and pointing at the `LOG.md` entry, which is their session log. It is committed to the collaborator's `<id>_br_<topic>-<date>` branch and travels in the pull request; the header line and flag are not touched. If the owner's session rewrote the same entry meanwhile, git surfaces the conflict at the pull request — never resolved silently.)*
5. **If the user has time:** they review, correct, approve. Commit clean. Header flag `reviewed`.
6. **If the user says "just commit it":** they have read the draft quickly. Claude commits it as-is. Header flag `unreviewed`; the next session start surfaces it in one line and a nod clears it.
7. **If the user says "close now":** the **unseen path** (below). Nothing is shown or explained; Claude writes the best rewrite it can, saves the transcript, commits. Header flag `unseen`; the next session start shows the close's diff verbatim before anything else. This is also the interrupted-session path in `finish_session_skill.md` Step 3.
8. **Either way, the session ends with STATUS.md committed.**

**The close check — every task finished or resumable (v6.5).** A session ends with each task it worked in one of two states, and the close records which. **Finished:** the workstream's entry is rewritten to where it now stands; if the task was the workstream's last, the entry becomes its close line and rotates. A finished task is not a finished workstream — processing five papers moves the spine's entry forward and rotates nothing. **Unfinished:** the resume is recorded before the close, at one of three grades, and the entry's Resume field points at it: (1) the entry's own Next line, when a single line can resume the task — "stopped after step 2, resume from the branch"; (2) a **carryover**, when one bounded task spans sessions and a line cannot carry its state — `multisession_task_skill.md`'s two-question gate decides between (1) and (2), and this check is the gate's close-time trigger; (3) a **plan file**, when the work is a workstream with its own sequence and open decisions — `workstream_plan_skill.md`'s gate decides, the outgrowth catch below offers it. A session that opened from a recorded resume closes the same way: the resume's position updated, or the task finished and the carryover deleted (that skill's Completion rule) or the plan retired (that skill's Retire step, which writes the close line). The check runs per task touched, not per session, so a second task started mid-session is caught by its folder in the touched set whether or not anyone remembers it.

**Rotation check (rides the reviewed and unreviewed paths).** As part of drafting the update, identify STATUS.md entries that are now closed — a workstream whose close line was written, questions resolved this session or earlier, fixed known-issues blocks — and include their rotation to `STATUS_ARCHIVE.md` in the draft the user reviews (see **The STATUS archive**: verbatim, lossless, conservative-rule, cite-by-name pointer reconciliation). On an `unseen` close, **skip rotation** — it waits for the next close the user sees, since nothing they have not looked at leaves `STATUS.md`; a record rotated at a reviewed or unreviewed close, or at a pass, carries no review mark in the archive, which stays verbatim. **Length tripwire:** if STATUS.md exceeds the kit's length target at close (stated once in `PROJECT_SETUP.md` Step 7.5 part 2: the floor computed at run time from the current template, never a number, and the project content it allows; words, never lines, since lines stop tracking the reader's cost once a file is hard-wrapped), surface that a rotation pass is due — under the workstream-entry form a STATUS over the tripwire means entries have outgrown their slots, which the outgrowth catch answers. **Rotation of closed records is mechanical** wherever it runs — here on the reviewed and unreviewed paths, and at Part C's conformance pass — verbatim and lossless, and a STATUS over the tripwire is rotated at the pass without a ruling; only **distillation** of live text is content work, gated by the user, never part of rotation. (`finish_session_skill.md` Step 3 invokes this close-out, so the check rides the standard session close — no separate step there.)

**The unseen path — "I have to go, close now" (v6.5).** Claude rewrites the touched entries as best it can, dated today. For an unfinished task it writes the resume at the smallest grade that holds it — the entry's own Next line; if the session was already running under a carryover or a plan, that file's position is updated; a new carryover is written only if a line cannot carry the resume, and the entry says it is unreviewed; a new plan file is never created unseen (the plan skill's sketch round needs the user). Then the **unseen-close transcript**: the conversation is saved verbatim, by default and without asking, in `repo_conversations_skill.md`'s transcript format, into the carryover home (`workspace/multisession_active_tasks/`, beside the carryovers) — **not** the conversations folder, and with no index row — and each touched entry's Resume field names it ("resume from the unseen-close transcript of YYYY-MM-DD"). Transcript and STATUS land in one commit, so the pointer never dangles. The transcript is a resume record, not a conversation: its function is a clean restart. **At the retake**, the session reads it first, with the user; the resume is written at its proper grade or the task is finished; and the transcript is **deleted in that session's commit by default**. Keeping it is the user's call on the spot, and keeping means promoting it to the conversations folder through `repo_conversations_skill.md`, with its index row, as an ordinary saved conversation. Pointer-target consistency at the next close catches a transcript left behind. Nothing rotates on this path. This default is deliberately **not** universal: a reviewed close writes the resume with the user in the loop, and the transcript is worth most where the review was skipped.

**Re-surface open Pending placement fixes.** As part of the close-out, read the Pending placement fixes subsection and re-surface any still-open entry, so a deferred placement (a folder move, or a staged file awaiting its home) persists across the session boundary instead of going stale. Remind the user each is still pending and ask whether to action it now (follow `CLAUDE.md`'s folder-creation placement check to do the move and remove the entry) or leave it recorded. Prompt-don't-perform: never move a folder unprompted. (`finish_session_skill.md` Step 3 invokes this close-out protocol, so the re-surfacing rides the standard session close — no separate step there.)

**Index-audit cadence read.** Also as part of the close-out, read the "Index audit last run" date in `STATUS.md`. The clock runs on use, not on the calendar: the anchor is the first commit to `main` after that date (a missing slot or `(never)` anchors on the repo's first commit, and says "never run"). No commit since the audit means nothing to audit, and nothing fires. If today minus the anchor exceeds `INDEX_AUDIT_INTERVAL` (default 30 days), surface it with the count: "the repo's index audit was last run [date]; work resumed [anchor date], [N] days ago; your canonical kit's maintenance campaign runs it, if you keep one — otherwise run the index audit in a dedicated session (`repo_audit_skill.md`, index-audit mode)." Persistent by design and counting up: it fires at every close, the number growing, until the date is refreshed. The date is stamped by that campaign's audit pass or by `repo_audit_skill.md`'s index-audit mode (its closing commit stamps today's date into the slot, the write-back), so the reminder stops only when an audit genuinely ran; if no campaign is due and the count is bothering the user, the index-audit mode in a dedicated session clears it. Prompt-don't-perform: this reminds, it never runs the audit. (`finish_session_skill.md` Step 3 invokes this close-out, so the reminder rides the standard session close — no separate step there.)

**Workdesk queue reconciliation (every repo).** Every repo carries the pending-actions queue `workdesk/INDEX.md` (`structure_conventions.md`). Reconcile it at close, three moves — four in repos with a collaborator on the roster — all prompt-don't-perform:
1. **Clear the done.** Rows whose action happened this session → surface: "these look done — clear them?" On the user's yes, remove them; the durable record of what was done is the commit and the workstream entry it moved, not the queue, which stays a live working list per the universal "working tracker, not a catalog" rule (`structure_conventions.md`).
2. **Add the missed.** Anything that *started waiting* on the user this session and never got a row — the add-side is a `CLAUDE.md` Working Convention that fires mid-session; this is its close-side catch — → propose the missing rows (Action: read · think · decide · do; Artifact-where pointing at the artifact).
3. **Surface the stale.** Rows with an old *Since* and no movement → name them; don't touch them.
4. **Collaborator queues (repos with a collaborator on the roster).** In the owner's session: rows they had added this session to a collaborator's *Waiting on* table are confirmed written; *For the owner* rows they took this session are cleared from the collaborator's table (on their yes). In a collaborator's session: the same three moves run on the collaborator's own `INDEX.md` only (their *Working on* block cleared for work whose pull request merged; *Waiting on* done rows cleared; *For the owner* rows added for every question and every decision the rules route to the owner), and the session appends its `LOG.md` entry per `structure_conventions.md`, "Collaborators" — done, decisions with their review state per the roster's Merge column, open. The owner's `workdesk/INDEX.md` is never written by a collaborator's session.
Never clear or add a row unprompted. (`finish_session_skill.md` Step 3 invokes this close-out, so the reconciliation rides the standard session close — no separate step there. Documented predecessor: the v4 done-to-do retirement check against `workspace/to_do/`, which the queue replaces.)

**Workstream position refresh + outgrowth catch (every repo).** Also as part of the close-out, walk the Current-state workstream entries — two moves, both prompt-don't-perform:
1. **Refresh the position.** For each entry pointing at a plan file (`<stem>_PLAN.md`), re-derive the one-line position (`step 3/6 — drafting`) from the plan's step table and update the entry's cached line. On any disagreement the plan file wins — the position line is a cache (`workstream_plan_skill.md`).
2. **Catch the outgrown.** An entry that has visibly outgrown its slot — step lists, embedded decisions, cross-artifact dependencies accreting inside `STATUS.md` — is the workstream signal: offer the plan file ("this entry has outgrown its slot — move its plan to a `<stem>_PLAN.md` per `workstream_plan_skill.md`?"). On the user's yes, that skill runs (sketch first); the entry trims to description + pointer + position. Never create the file unprompted.
(`finish_session_skill.md` Step 3 invokes this close-out, so both ride the standard session close — no separate step there.)

**Non-empty-staging prompt (every repo).** Also as part of the close-out, check `workspace/staging/`. Its documented resting state is empty (`structure_conventions.md`, the intake funnel), so anything in it at close is a legible signal: either a placement is mid-flight or a rushed-use file was never placed. Surface what's there and ask: place it now (run the intake funnel's full check) or leave it staged — in which case confirm a **Pending placement fixes** entry exists for it, writing one if not. This is the belt-and-suspenders pair to the Pending entry: the entry nags by record, this prompt nags by state, so a staged file can't go invisible even if the entry was missed. Prompt-don't-perform: never place unprompted. (`finish_session_skill.md` Step 3 invokes this close-out, so the prompt rides the standard session close — no separate step there.)

**Index-entry refresh (every repo; a NONE repo for `NOTES_INDEX` only).** For the files this session touched (the same touched-set the close-out already derives from commits and modified files), check whether their typed-index rows' **live-claim fields** — the state cell of each kind (`typed_index_template.md`: `Claude status` and `User status`, `Stage`, `Verified`, `Used in`, a research repo's `MATERIALS_INDEX` row's `Reliability` once the document branch is active), the `Forms` cell as representations are made, `ledger` in `Where` once a ledger exists, and the `About` cell where a subject became live this session — still hold, and draft the updates; a thing the session created that has no row gets one in the index's header row. Discovery rides the `FOLDER_MAP` tree and the root map's root-documents block, never hardcoded names. The trailer line of every index touched is rewritten (`*Last updated: YYYY-MM-DD — <what changed>*`), the only date in the file. The user reviews → commit clean; no time → the updated row carries a trailing `[unreviewed]` marker (defined in `archetype_conventions.md` typed-index behavior), swept for review by the next index audit. This is the **write side** of the universal feeding process: the close keeps entries current, and `repo_audit_skill.md`'s index-audit mode is the periodic backstop — in steady state, entries go stale only when a close was skipped or rushed, which is exactly what the audit's evidence pass catches. Sibling to the floor's `FOLDER_MAP` status refresh (`structure_conventions.md`), which this close-out's catalog refresh implements (below). A NONE repo carries `NOTES_INDEX` alone, so the refresh runs there for note sets only. (`finish_session_skill.md` Step 3 invokes this close-out, so the refresh rides the standard session close — no separate step there.)

**Catalog refresh (every repo, NONE included).** A catalog on a navigation surface — a map's catalog, and the catalog of a standing document in `workspace/` or `workdesk/` (`standing_documents_template.md`: brainstorms, branch_logs, visuals, packages, admin, postits) — is a live claim, the same class as the live-claim fields above, and it goes stale the same way. For every folder the session's commits touched, the close-out brings the catalog current — a row added for each new file or stem (except in a `leaf` whose files a typed index registers: its map's one pointer row at that index is the whole catalog, `FOLDER_MAP_template.md`, and gets no per-file row; the index-entry refresh above keeps those files current), removed for each deleted one, a `packages/` row dated sent and never removed (the record of what went out survives the zip; the floor's rule 1), a map row's label refreshed, a moved entry's row moved to the map of the folder it went to, every map row under the kit header `| Path | What is here |` (`FOLDER_MAP_template.md`, the catalog: present contents only, no counts or dates in a row) — and rewrites the document's one trailer line in place (`*Last updated: YYYY-MM-DD — <what changed>*`; never a second line); a map found with no trailer gets one at the refresh. The touched set is the same one the close-out already derives; the surfaces are in `TRACKED_LOCATIONS`; the refresh is part of the close draft the user sees, and on an `unseen` close it still runs, since a stale catalog is a stale claim. A folder born this session already has its map, written empty at creation by the placement check (`CLAUDE.md`; the floor's leaf rule); the refresh fills its rows. This is also the universal layer's end-of-session `FOLDER_MAP` status refresh, which `finish_session_skill.md` Step 3 reaches by invoking this close-out in full; `repo_audit_skill.md`'s Check 3 is the backstop that reads a catalog against the folder's contents, and the audit fixes maps and standing documents between closes (Check 3 and Check 14 findings applied in repair mode). *(Documented predecessor, v6.3 to v6.5: the navigation-label refresh, which rewrote a live "Empty = ..." claim in the standing `README.md` and the parent map row; under `standing_documents_template.md` the resting state is a permanent line and the catalog is the live surface.)*

**Collaborator merge sweep (repos with a collaborator on the roster; `merge: owner`).** When the owner's session merges a collaborator's pull request — at close under `finish_session_skill.md` Step 2 or mid-session at the owner's request — read the merge for folders it created outside the collaborator's workdesk territory. Any such folder is swept into `workspace/staging/` in the same session and placed by the intake check (`structure_conventions.md`, "Collaborators"); the owner integrates it from there. The `merge: self` half runs at the owner's next session start (the freshness check, Pass 1). Prompt-don't-perform on the placement; the sweep to staging is proposed with the merge and done on the owner's yes.

**Promotion drift (archetype repos).** Surface — never perform — a **promotion candidate** at close, read off the repo's state, so it needs no storage and self-resurfaces until acted on. What counts by archetype: **research** — a root or line-level folder with a map and outputs and no `Stage:` word, or a working folder that has become a line of its own. **Promotion is a structural act** (`archetype_conventions.md`): on the user's yes the ruling and the unit's scaffold travel in one commit — the folder gets its map with the slot row, its `[P]` children, its index rows, its stage line, and its workstream entry here — never the ruling now and the structure later. *(Documented predecessor: through v6.3 research had no event for "a folder became a line".)*

**Mandatory, not optional.** Every session close triggers this. The asymmetry is intentional: losing the record is much worse than committing an unreviewed or unseen draft. An unreviewed draft can be corrected; a missing record cannot be reconstructed. A stale entry is worse than an unreviewed one, which is why the unseen path still rewrites.

**Edge case — session ends without a close-out signal.** If the user gets pulled away, their laptop dies, or the connection drops, no close signal is given and STATUS.md is not updated. The next freshness check will detect the gap — commits under a folder later than its entry's date — and propose the rewrites, entry by entry. This is acceptable degradation; trying to auto-update without the user's signal would be worse.

---

## Bootstrap procedure

How STATUS.md gets created the first time, in a repo that doesn't have one.

### Bootstrap during Part A (new repo setup)

When a new repo is being set up, `STATUS.md` is created during `PROJECT_SETUP.md` Part A as part of the initial folder/file creation. The template (`STATUS_template.md`) is copied to the repo root and filled by the pour rules of Step 7.5 part 2 from the setup interview and the scaffold:
- **Current state:** one entry per workstream the scaffold created (each line in a research repo, each folder of the bespoke skeleton that carries work in a NONE repo, plus `general` where the archetype has a spine, plus `repo`), each reading "repo just set up; nothing in flight" with today's date, Next from the interview where the user named a first move. The three subsections `(none)` / `(never)`.
- **Open questions:** initially empty unless the setup interview surfaced any.
- **Known issues:** initially empty.
- **Cluster activations:** written by `skills_curation_skill.md` Step 7.

The first commit on the new repo includes STATUS.md alongside the other initial files. Header flag: `reviewed` (because the user just confirmed every entry during the interview).

### Bootstrap during Part B (existing repo integration)

When an existing repo is being integrated with the kit for the first time, STATUS.md is bootstrapped as part of Part B's Skills Activation step. Claude:
1. Reads the repo's existing `CLAUDE.md`, all `FOLDER_MAP.md` files, recent `CHANGELOG.md` entries (if present), and recent commits (last 10–20 on `main`).
2. Drafts the workstream entries from what those artifacts reveal about each unit's current state — where it stands, Next, Waits on — and the open questions.
3. Walks the user through the draft entry by entry for review.
4. Once approved, STATUS.md is committed alongside the other Part B changes.

The Parking Lot section from the existing CLAUDE.md (if present) is migrated to STATUS.md's "Open questions" section, and the CLAUDE.md Parking Lot section is removed in the same commit.

Header flag: `reviewed`.

### Bootstrap during Part C (propagation to an already-integrated repo)

When a repo that was integrated against an older kit version is being upgraded, STATUS.md is bootstrapped as part of Part C's propagation. Same flow as Part B — Claude drafts from existing artifacts, the user reviews. The Parking Lot migration also runs at this step. **A STATUS.md that already exists is not bootstrapped again; it is rebuilt in form:** Part C Step 7.5, the conformance pass, rebuilds the file in template order — every section a slot, missing ones added empty or "never run", the header rewritten in place and its stack rotated, the comment guidance regenerated, closed records rotated mechanically — with every entry the repo wrote kept in its section (v6.3 backfilled missing sections only; v6.4 owns the form). **The one-time pour into the workstream form (v6.5):** a Current state written as a session log has no per-workstream entries to keep, so at the pass that first applies the v6.5 form the log rotates verbatim to the archive and the entries are drafted from the folders, the plans and the old narrative, one per workstream, and put to the user as an ask — the pour, not a rotation; the designed exception where the pass writes new text. The retired sections leave with their content per the structure section above.

---

## Folder bootstrap protocol

STATUS.md and the freshness check depend on folders existing. The universal `workspace/` subfolders, the `workdesk/` scaffold (`INDEX.md` + `admin/` + `postits/` + `collaborators/`), `feedback/` and `writing_notes/` (all defined in `structure_conventions.md`) are **created unconditionally, never asked about** — they are load-bearing homes for always-active skills, created up front as labeled-empty homes; an empty subfolder reads as state, never clutter. What varies by Part of `PROJECT_SETUP.md` is only *when* the creation happens:

**Part A (new repo):** the archetype/NONE scaffold creates the full layout at birth — the universal `workspace/` subfolders plus whatever else the scaffold specifies. No questions.

**Part B (existing repo, first integration):** any universal subfolder missing from the repo is created in the integration commit. If the repo has an existing arrangement doing the same job (a root `TODO.md` or a `general/to_do/` doing the workdesk queue's job, a conversations folder under another name), Claude proposes reconciling it into the universal home — for a to-do arrangement, item-by-item into the `workdesk/INDEX.md` queue — migration is the user's call (prompt-don't-perform), but the home is created either way.

**Part C (upgrade to a new kit version):** any universal subfolder still missing is created in the propagation commit. If the repo's `CLAUDE.md` carries a **Deferred folders** subsection from a pre-v4 integration, the listed folders are created and the subsection is removed in the same commit — the per-folder choice is superseded by the universal convention, and the removal is recorded in the propagation commit message rather than silently dropped. *(This replaces the v2.2 per-folder ask / Deferred-folders mechanism, retired when the `workspace/` subfolders became universal and load-bearing.)*

**First-use fallback (any repo, any time):** if a skill tries to use a folder that doesn't exist — which after integration should only happen in a repo not yet brought onto the current kit — the skill asks once: "this needs `[folder]` — create now, or exit?" If yes, the folder is created as part of the workflow's commit. If no, the skill explains what it can't do and exits.

---

## Composition with other skills

This skill is the **upstream session-start ritual and downstream session-close ritual** for every other skill in the kit.

- **`brainstorming_skill.md`** — saves brainstorms to `workspace/brainstorms/`, which is in `TRACKED_LOCATIONS`. The freshness check detects new brainstorms and surfaces them as candidates for entry rewrites.
- **`repo_conversations_skill.md`** — saves conversations to `workspace/claude_conversations/`, which is in `TRACKED_LOCATIONS`. Same freshness-check pickup. Its transcript format is also the form of the unseen-close transcript, which lives in the carryover home with no index row and is deleted at the retake unless promoted.
- **`writing_skill.md` Protocol 2** — drafts land in the deliverable's home folder (asked, not assumed; see that skill's *Placement is asked, not assumed* rule), which the recursive `FOLDER_MAP.md` scan in `TRACKED_LOCATIONS` covers wherever the archetype places it. Branch workflow events (creation, merge) appear in commits, which are also part of the audit.
- **`materials_processing_skill.md` and `document_processing_skill.md`** — registering a paper adds a row to the repo's paper-detail index and a document a row to its materials index, one row in one index (discovered from the root map's root-documents block, in the template's row); that index activity is caught by the recursive `FOLDER_MAP.md` scan and by commits.
- **`multisession_task_skill.md`** — owns the carryover (one bounded task across sessions; born at the stop, deleted at completion). The close check here is its gate's close-time trigger, and the entry's Resume field is its pointer.
- **`workstream_plan_skill.md`** — owns the workstream plan-file convention (`<stem>_PLAN.md` living with the work; plain default, scoped upgrade). This skill owns the STATUS.md surface for it: the entry shape (description + pointer + position), the close-out position refresh, the outgrowth catch, and the close line its Retire step writes. Plan files and the work they steer are seen by the freshness check through commits and the recursive `FOLDER_MAP.md` scan.
- **`repo_audit_skill.md`** — comprehensive infrastructure check, run on demand. Findings that resolve into repair commits are picked up by the next session's freshness check. Its **index-audit mode** is the read side of the index-entry refresh defined here: it sweeps `[unreviewed]` rows, verifies live claims on the `INDEX_AUDIT_INTERVAL` cadence, and stamps "Index audit last run" in `STATUS.md` on completion — the write-back that silences the close-side reminder.
- **`finish_session_skill.md`** — orchestrates the session close-out as a five-step sequence (uncommitted-work inventory → branch disposition → STATUS.md update → conversation save → confirm close). The STATUS.md close protocol defined above is Step 3 of that sequence, and the unseen path's transcript is its Step 4 made unconditional on that path. When a close-out signal fires (the user says "thanks," "good night," "we're done"), `finish_session_skill.md` is the single entry point; this skill is invoked from there.
- **`skills_curation_skill.md`** — writes the Cluster activations block (Step 7) at every propagation; the only writer of that section.

---

## Notes on scope

- **Generic skill, propagates to all content repos.** Lives in the canonical kit copy.
- **A canonical skills repo itself does not get a STATUS.md.** It is the kit factory, not a content repo.
- **STATUS.md is not a substitute for CHANGELOG.md.** `CHANGELOG.md` (in `skills/`) records kit version history. STATUS.md records the *content repo's* open work. They're different layers.
- **STATUS.md is not a substitute for `repo_conversations_skill.md`.** Saved conversations are detailed transcripts; STATUS.md is the curated open state. Both can coexist.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
