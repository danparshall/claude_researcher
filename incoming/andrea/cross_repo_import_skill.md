---
name: cross-repo-import
description: "Workflow for importing already-processed material from another repo into this one — pulling files that were created or processed elsewhere and giving them a proper home here. Cowork only: the source is another local clone under repos/, read directly from the filesystem. Use when material that lives in a different repo needs to be brought in and placed, not re-made. The import is read-only on the source — nothing in the source repo is edited, committed, or deleted — except in the hand-over mode, where material moves to its single home repo and the sending copy is retired after the home has committed it. Does NOT cover a sweep that compares `skills/` across repos (run from your canonical skills repo, if you keep one); does NOT cover exporting or pushing material OUT to another repo outside the hand-over mode; does NOT cover placing material already inside this repo (that is the intake funnel's placement check — structure_conventions.md); does NOT cover plain git operations."
triggers: >-
  "import X from repo Y," "bring in the material from [repo]," "hand X over to [repo]," a
  workdesk row saying a hand-over is owed; Cowork only. Not a skills sweep, not export
---

# Cross-repo import workflow

**Environment: Cowork only.** This workflow reads a second repo's local clone
under `repos/`. If this is a claude.ai web session, stop and tell the user this
needs to run at Cowork — do not improvise a web-side alternative (the
token-re-scoping version of this workflow is retired). At Cowork, open by
stating the direction — "importing from `<source repo>` into `<this repo>`" —
and wait for the user's confirmation before proceeding (Step 1 owns this
confirmation). The one web-workable path is the user-bridged variant in Edge
cases: they place the material in `workspace/staging/` themselves and the
workflow resumes at Step 3.

**Status:** active.
**Owner:** the user.
**Applies to:** bringing **already-processed** material in from another repo — source PDFs, extracts, summaries, notes, a finished deliverable — and landing it **typed and placed** in this repo, not dumped at root. Universal: any repo can run an import, including a NONE repo.

**Does not apply to:** the discovery sweep that compares `skills/` across repos (run from your canonical skills repo, if you keep one); exporting material *out* of this repo (import is read-only on the source); placing a file that is already in this repo (the intake funnel / folder-creation placement check); general git use.

---

## Why this workflow exists

Importing by hand has a recurring failure mode (the "ghost"): the *derived* form gets pulled — an extract, a summary, a built `.docx` — while the *source* it came from is left behind in the other repo. Later the source is needed and it is gone from view. The fix is a staging step where the keep / drop / what-must-come-too decision is made deliberately **before** anything lands, instead of file-by-file on the fly. The staging home and its lifecycle are defined once in `structure_conventions.md` (the intake funnel); this skill owns the cross-repo **step-by-step** — one caller of that funnel — and points back there rather than redefining it.

## The source boundary (read first)

The source repo is another local clone under `repos/` on the user's machine. The import reads it from the filesystem — no tokens, no API. Two rules frame everything:

- **Read-only on the source.** Nothing is written to, committed in, or deleted from the source repo. Its clone stays exactly as it was (a `git fetch`/clean pull to sync it before reading is the one allowed touch). The hand-over mode (below) is the one exception, under its own four rules.
- **One direction.** Material comes *in*; this skill never pushes anything out. Exporting is a different act and is not covered here. The hand-over mode is an import into the home repo followed by the retirement of the sending copy; it pushes nothing.

*(Documented predecessor: through v2.0.0 this skill was built for claude.ai web, where reading a second repo required the user to re-scope the access token to both repos and back — Steps 2 and 7 were token reminders. On Cowork the token boundary does not exist; the selection discipline below is what remains, unchanged.)*

## Workflow

1. **Confirm the import — direction first.** State the direction explicitly and get the user's confirmation of it: **from `<source repo>` into `<this repo>`**. Then confirm what is being brought in (which files / folder) and roughly what it is (source material, derived artifacts, a deliverable). If the source repo isn't named, ask. The direction line is not ceremony: at Cowork every clone is equally visible and writable, so nothing physical marks which repo is home — the web era's one-repo-per-session anchor is gone, and the explicit from→into statement replaces it.

2. **Locate and sync the source clone.** Find the source repo under `repos/`. Sync it with its remote first (`git fetch`; pull if cleanly behind) — importing from a stale clone imports stale material. If the clone has diverged or has uncommitted changes, flag it to the user before reading. If the repo is **not cloned locally** (or is one the user can't clone), switch to the user-bridged path in Edge cases.

3. **Copy the named material into `workspace/staging/`.** A plain filesystem copy from the source clone into this repo's `workspace/staging/` — binaries are just files here, no special handling. Nothing lands in the tree yet.

4. **Select in staging — the keep / drop / what-must-come-too call.** This is where the ghost problem is prevented, and it happens **here, before placement**. For each item, identify whether it is a **source** or a **derived** form, and whether its counterpart also needs to come: the kit keeps **both forms** when both carry information (the source PDF *and* its extract), so importing a derived artifact while orphaning its source is the failure to catch. Drop genuine working residue that has no reason to live here. Surface the keep/drop list to the user; nothing leaves staging until they confirm.

5. **Place each kept item by the repo's normal placement rules.** Hand off to the intake funnel's full check (`structure_conventions.md`), where placement is a lookup: a kind the repo already has a home for is placed and registered without asking, and what landed where is said, and only a kind with no declared home, or a probable duplicate, is proposed — origin-typed intake for the archetype repos (`materials_processing_skill.md` and the paper branches), the placement proposal otherwise. Read the target home from the current `FOLDER_MAP`s/indexes; an import re-files into *this* repo's shape and is **not** governed by how the source repo had it organized. Register each landed item in the right index/`FOLDER_MAP`.

   **Two ways to land a summary.** The full integration is the default: the imported summary is re-processed under `materials_processing_skill.md` at landing, rewritten to this repo's template and against this repo's question, and its row is set like any paper processed here. **When there is no time**, the summary lands as is, to be usable now, with three things written in the same commit: the paper row's `Claude status` reads `Flagged — imported from <repo> <date>, not integrated`; the home's map carries one provenance paragraph for the batch (the source repo and paths, what the summaries were written for, what they lack against this repo's question); and a `workdesk/INDEX.md` queue row for the full integration (Action: do, the batch named, pointing at the paragraph), because when to spend the re-processing is the user's call. The flag and the paragraph do not go away until the paper is re-processed; the queue row clears then.

6. **Empty staging.** Once everything kept is placed, clear `workspace/staging/` back to its labeled-empty resting state.

## The hand-over mode

Some material has a single home repo: a paper, a deck or a reference collection that one repo holds as canonical and other repos only copy. When such material was made or received in a repo other than its home, it is **handed over**: the home imports it, and only then does the sending repo retire its own copy. The trigger is a workdesk queue row in the sending repo saying the hand-over is owed; a periodic maintenance pass, if you run one, clears every open one, and the user can run one sooner. Four rules:

- **One home repo, one other repo at a time.** The session names the home repo and writes in one other repo at a time, never two in one step.
- **Every commit states the direction** the material moves ("<repo> to <home repo>", "<home repo> to <repo>").
- **No document is ever held nowhere.** The sending copy is deleted only after the home has committed its canonical file.
- **The import half goes through staging** (Steps 3 to 5), **and a file the home adopts byte-identical is checked by hash**: write the copy from the source clone's committed blob (`git -C <source repo> show HEAD:<path>`), check its hash (`git hash-object --no-filters`) against HEAD's blob, and check again on the staged file before the commit. A working copy checked out with CRLF hashes differently although clean, so the comparison is to HEAD's blob, never to the working file alone.

The sequence: in the home repo, run Steps 1 to 6 with the sending repo as the source, and commit. The home may adopt the sending repo's processed files as its canonical ones, byte-identical. Then, in the sending repo: delete what the home now holds (a source PDF, for example), replace any processed file the repo still needs with a byte-exact copy from the home, written the same way, with its provenance in the folder's `FOLDER_MAP.md` row (the home repo's path and the date), repoint the index rows, close the queue row, and commit. *(Documented predecessor, to v6.10: import one-directional only, with no path for material that entered outside its home.)*

## Key rules

- **Always state the direction: from which repo, into which repo.** At confirmation (Step 1) and in every record the import leaves — the staging keep/drop list, index/`FOLDER_MAP` registrations, the commit message. With all clones visible at Cowork, an unstated direction is how material lands in the wrong repo.
- **Read-only on the source.** Reads (plus a clean sync) only; never write to, commit in, or delete from the other repo's clone. The source stays exactly as it was. The one exception is the hand-over mode's second half, after the home has committed.
- **Select before placing.** The keep/drop decision is made in staging (Step 4), not file-by-file during placement. This is the ghost-problem fix; do not skip it.
- **Don't orphan a source.** Before dropping a source form, confirm its derived form carries everything needed — and vice versa. When unsure, keep both (the kit's keep-both-forms rule).
- **Re-file into this repo's shape.** Placement reads this repo's maps; the source repo's organization does not carry over.
- **An imported summary carries no authority it did not earn here.** Landed as is, its row says `not integrated`, and a claim from it is read through its `TEXT_` extract before it carries weight in a deliverable; the note stands until the paper is re-processed.

## Edge cases

- **A big, multi-session import.** If selection and placement won't finish in one session, it is a candidate for a carryover (`multisession_task_skill.md`); the half-imported state lives in `workspace/staging/` meanwhile, which is exactly what staging is for.
- **Source material the other repo had indexed.** Don't carry its index entries verbatim — re-index here per this repo's placement rules (Step 5).
- **Source repo not cloned locally (or not the user's to clone) — the user-bridged path.** The user obtains the material themselves and drops it into this repo's `workspace/staging/`; the workflow resumes at Step 4 (select). This is also the one variant a claude.ai web session can run, since it needs no cross-repo read.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
