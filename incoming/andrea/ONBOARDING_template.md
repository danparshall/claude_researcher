# Welcome, <Name> — <the task in a few words>, and how to get into it

<!--
  ONBOARDING.md is written for a person. The collaborator reads it once, when they join, and
  their Claude presents it to them the first time they work together: the "read ONBOARDING.md"
  row in their Waiting on table stands until it has been read. Their Claude takes the repo from
  CLAUDE.md, the maps and STATUS.md as any session does; from this file it takes the reading
  list, the order in which to put the repo in front of the person. Six parts, the headings
  fixed; "How this repo works" and "Working with your Claude" open with a kit block, the same
  text in every repo, regenerated whole by the conformance pass, and close with the repo's own
  slot. The owner's session writes the slots; the pass never rewrites them
  (skills/PROJECT_SETUP.md Step 7.5 part 2). The convention is
  skills/structure_conventions.md, "Collaborators".
-->

**Written:** <YYYY-MM-DD>, at the owner's instruction, when <Name> joined the repo to work on
<scope>. <Or, for a person who had access before the convention: when the collaborator
convention was set up and every person with access got a folder; <Name> has had access since
<when>, so this document orients you to how the repo is organized now rather than introducing
the project.> The owner is the contact for anything this file leaves open.

**Review:** <draft, pending the owner's review | reviewed by the owner: YYYY-MM-DD>.

## What the task is, in one paragraph

<One paragraph a newcomer can read without the repo: what the piece of work is, what it
consumes, what it produces, and why it matters to the project. Name the headline output.>

## How this repo works (read this before anything else)

The same rules hold in every repo the owner runs; this list is the part of them a person with
write access meets. Your Claude knows the rest.

- **`CLAUDE.md` at the repo root is the rulebook.** Your Claude reads it at the start of every
  session, before anything else, and then your folder, `workdesk/collaborators/<id>/`. You do
  not need to read it yourself; ask your Claude for any rule in it.
- **Four rules for collaborators** (in short in `CLAUDE.md`'s Collaborators section, in full
  in `skills/structure_conventions.md`, "Collaborators"). Your folder is the only place you
  write directly on `main`. Everything else goes on a branch named `<id>_br_<topic>-<date>`
  and reaches `main` through a pull request <that the owner merges | that you merge yourself
  when it stays inside your territory>. Your queue, `INDEX.md` beside this file, is the
  two-way channel with the owner: *Waiting on <Name>* is what they hand you, *For the owner* is
  what you hand back, and the *Working on* block above them says what you are on. `LOG.md`
  beside it is your session log, one entry per session with what was done and the decisions
  taken. Every session that ends with a pull request leaves its decisions there: the owner
  reads them beside your pull request, so they can check the work and teach from it, and their
  notes come back to you through your queue.
- **Every content folder carries a `FOLDER_MAP.md`** saying what the folder holds and why.
  When lost, ask your Claude for the map of the folder you are in.
- **`STATUS.md` at the root says what is open**, one entry per workstream: where it stands,
  the next move, who it waits on. Your workstream has an entry of its own, and your Claude
  rewrites it at the end of every session. That entry, not this file, is where the work
  stands today.
- **Nothing enters the repo by being dropped in it.** Anything new — a report, a colleague's
  note, a dataset — lands in `workspace/staging/` and is filed from there: renamed, its text
  extracted, summarized, registered in the indexes. Before asking for a document or
  processing one, your Claude greps the indexes; a hit means the repo already holds it and
  the work starts from what is there.
- **The indexes are how things are found.** The root `FOLDER_MAP.md` for the structure, the
  typed indexes for what has been filed and produced, every folder's map for what it holds.
  Ask your Claude rather than browsing.
- **What is waiting lives in queues, not in chat.** `workdesk/INDEX.md` at the root is
  the owner's own queue; yours is the channel with them. Feedback on the repo's products — a
  meeting's comments, an emailed note — is recorded in the root `feedback/` folder, one dated
  entry per person, and the queue points at it until it is absorbed.
- **Material from someone without access** goes to the line's `inputs_from_team/` folder,
  unmodified and attributed; you place it on your branch like anything else.
- **Nothing is deleted.** A superseded document goes to an archive folder with a banner saying
  what replaced it; a version that must stay citable is kept beside the live one. Dated
  records keep their old paths on purpose.
- <The one or two conventions of this repo that bite on day one, for example the `original/`
  vs `project/` split or the provenance rule for numbers. Only what this repo adds; the rules
  above are already there.>

## The reading list, in order

Read these in sequence; each assumes the ones before it. Your Claude puts them in front of
you in this order.

1. **`<path>`** — <what it is and why it comes first; usually the live specification or the
   design of record. What to take from it>.
2. **`<path>`** — <...>.
<Five to eight rows. Say for each what the reader should take from it. Mark provenance-only
rows ("read its banner; do not build from it") so an archived design is not mistaken for a
live one.>

## Your assignment (as of <YYYY-MM-DD>)

Settled when you joined: <what is done, in one or two sentences>. Handed to you, in order:

1. **<First step>** — <what it needs and what depends on it>.
2. **<...>**
<Then the build, the draft or the analysis, and where its outputs land.>

This part is written once. Where the work stands today is your workstream's entry in
`STATUS.md`, which your Claude reads and rewrites; what waits on you is your queue.

## Working with your Claude

This repo is built to be worked with Claude, and the documents above are written so a Claude
session can explain them. Your Claude follows the repo's protocols on its own, and some of
them show up as things it does or asks without being told. This is the list, in the order you
will meet them, so that each one is recognizable when it comes.

- **At the start of every session** it establishes whose session this is, from the git name
  or by asking you, reads `CLAUDE.md` and then your folder, and takes what is waiting from
  your queue. The first time, what is waiting is this document.
- **When you bring something new** — a report, a colleague's note, a dataset — it puts it in
  `workspace/staging/` and files it from there: rename, extract, summarize, register. Before
  producing anything it greps the indexes, and it may tell you the repo already holds what
  you asked for.
- **When a new folder or file is needed** it asks where it belongs before creating it, and it
  never moves a folder on its own call. If you ask it to skip the check, it records the
  pending placement rather than dropping it.
- **When you draft or edit a document** it works on a branch named `<id>_br_<topic>-<date>`
  and asks you at the end whether the work is ready for the pull request. For an experiment
  it offers an exploration branch, which can be discarded.
- **When a task will not finish in one session** it offers a carryover: a short file that
  records where you stopped, so the next session resumes from it instead of from memory.
- **When a piece of work has grown steps and open decisions** it offers a plan file for the
  workstream, and your `STATUS.md` entry then points at it with a one-line position.
- **When your instruction can be read more than one way** it tells you which reading it took
  before it continues, and the same when it goes ahead on an assumption rather than asking.
  Those moments are written into your `LOG.md` entry at the close, with your sentence beside
  what it did, so a result that is not what you expected can be traced to the instruction
  rather than written off as a hallucination.
- **When a decision is the owner's** — a merge, a placement ruling, anything the rules mark as
  theirs — it does not decide. It opens a *For the owner* row and tells you so.
- **When you say "thanks"** it closes the session: it rewrites your workstream's entry in
  `STATUS.md` on your branch, writes your `LOG.md` entry (what was done, the decisions with
  what it was unsure of, what is open), reconciles your queue, opens or pushes the pull
  request, and asks whether to save the conversation. Say yes when a decision was made in
  chat; the saved conversation gets an index row and is findable later, and the owner's review
  reads it when the log entry alone does not answer.
- **When you have to leave**, say "close now." It writes the close without showing it to you
  and saves the transcript as a resume record for the next session.

Habits that work here:

- **Ask it to explain, not just summarize.** The documents carry their reasoning, and Claude
  can unpack any step. If a document contradicts what you were told, ask Claude to check
  `STATUS.md` and the folder maps; the repo's trackers are the source of truth, not memory.
- **Have Claude verify paths before following them.** Dated records (saved conversations,
  archived plans) deliberately keep old folder paths; the live documents on the reading list
  are current.
- **When you have a question for the owner**, have Claude add a row to *For the owner* rather than
  waiting for a meeting; their sessions read that table at session start.
- **Early on, ask your Claude to walk you through the skills.** `CLAUDE.md` carries a table
  of the workflows this repo has installed — processing a paper or a document, drafting,
  translating, producing a Word file or a slide deck, and more. Ask it to explain what each
  one does, so you know what is at hand before you need it.
- <A habit this repo adds, if any, for example a standing convention that Claude explains the
  reasoning behind every recommendation.>

---
<!-- Kit file marker below: the template's own version line, not part of the repo file. -->
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
