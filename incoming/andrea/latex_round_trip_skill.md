---
name: latex-round-trip
description: "The review round trip for a paper whose live LaTeX source is edited outside the repo (Overleaf and the like, with co-authors), the repo holding a copy. Covers: the markdown review copy regenerated from the current source each round, the branch round run on that copy, the apply register (line number, original text, proposed text) the user works from by hand in the external editor, the source coming home and the diff that reads the co-authors' edits, and the ledger events. Does NOT cover: authoring or styling the LaTeX itself (`academic_paper_latex_skill.md`); the branch loop's own mechanics (`writing_branch_skill.md`, which this skill runs on a copy); the ledger file convention (`product_ledger_skill.md`, which this skill routes to); or a paper the repo authors, where the LaTeX is built from `main` after merge and no round trip exists."
triggers: >-
  A review round on a paper whose LaTeX source lives in Overleaf or another external editor;
  "this came back from Overleaf," "my co-author sent the new .tex," "make me the list of
  changes to apply in Overleaf"
---

# LaTeX Round Trip

Some papers are authored in LaTeX in an external editor, Overleaf most often, where co-authors
edit alongside the user. The live source is there. The repo holds a copy of the `.tex` and its
inputs, and nothing the repo does lands in the source by itself. The kit's branch workflow
assumes the reverse, a markdown file that is the live source and a merge that lands the change.
This skill is the round trip for the other case: Claude's review edits travel out as a register
the user applies by hand, and the co-authors' edits come home as a refreshed copy read by diff.

It is the paper sibling of `design_deck_reconciliation_skill.md`, and like it a **consumer of
`product_ledger_skill.md`**: that skill owns the ledger and its events; this one owns the review
copy, the register and the refresh.

## When to use this skill

Read this skill when:

- The user asks for a review or editing round on a paper whose `.tex` lives in Overleaf or
  another external editor.
- The user says the source came back from Overleaf or from a co-author, or drops a new `.tex`
  in staging for a paper the repo already holds.
- The user asks for the list of changes to apply by hand in the external editor.

Do not use this skill for:

- **A paper the repo authors.** Its LaTeX is a companion artifact built from `main` after the
  merge (`writing_branch_skill.md`, Convention 5); there is no external source and no round
  trip.
- **Writing or styling the LaTeX.** That is the LaTeX skills; this skill never authors the
  source.
- **The ledger's own structure.** Route to `product_ledger_skill.md` rather than restating it.

---

## The three files

| File | What it is | Lifetime |
|---|---|---|
| `<stem>.tex` and its inputs (`tables/`, `graphs/`, `references.bib`) | The repo's **copy** of the live source; Claude never edits it except at the refresh (step 6) | Standing |
| `<stem>_review_<YYYY-MM-DD>.md` | The **review copy**: the source converted to markdown for one round, the surface the branch loop runs on | One round; deleted at the refresh that closes the round |
| `latex_changes_<YYYY-MM-DD>.md` | The **apply register**: what the user applies by hand in the external editor, one per round | Standing, beside the draft; the round's record |

All three live in the paper's draft folder beside the source. The register's date is the round's
date, hyphenated ISO, the floor's leading-date form (`naming_conventions.md`); the review copy
carries the same date. Neither takes a content-file marker: the floor's closed list is widened
by a kit change only, and a dated stem finds these two by eye.

## Workflow

### 1. Confirm the source is current

Before any round, ask the user whether the repo's `.tex` is the version now in the external
editor. If it is not, run the refresh (step 6) first, so the review copy and the register's line
numbers describe the file the user will be editing. A register cut against a stale copy sends the user to
the wrong lines.

### 2. Regenerate the review copy

Convert the current `.tex` to markdown as `<stem>_review_<date>.md`, keeping the section
structure, the prose, the equations and the citation keys so a reviewer can read the argument
whole. Regenerate it every round from the current source; never carry a review copy from one
round into the next, and never edit it as if it were a source.

**Tables wrapped in `\resizebox` do not render in the review copy.** Nor do most `\input`
tables. A fix inside such a table cannot be seen in context on the review copy; read and
check it in the `.tex` directly, and say so in the register's row for that change.

### 3. Run the branch round on the review copy

The round is `writing_branch_skill.md`'s loop, run on the review copy: the branch is created and
registered, the user reads the copy and edits it in brackets or in place, Claude applies and
reports back. The branch holds the review copy and, at the end, the register; it never holds a
changed `.tex`. The lock, the read-before-edit rule and the round-count checkpoints apply as
written there.

### 4. Write the apply register

At the end of the round, every change that survived review goes into
`latex_changes_<date>.md`, in the form the user works from by hand: **for each change, the line
number in the `.tex`, the original text, and the proposed text.**

- **A contents table at the top:** one row per change, its number, the file and line, and a
  few words on what it does. The user reads the table to see the round at a glance and to tick
  changes off.
- **One block per change below the table:** the number and line as the heading, then
  **Original** and **Proposed**, each quoted whole in a fenced block so it can be selected and
  pasted. Changes to a table input name that file and its line.
- **Within-line edits wherever possible**, so line numbers do not shift as the user works down the
  list. Where a change must add or remove lines, it goes last in the register and the block
  says which later lines move.
- **The original text is the anchor, the line number a locator.** The register says so at its
  head: if the editor's line differs, find the Original text; if the Original text is not
  there, the source has moved on and the change is re-cut at the next refresh, never guessed.
- **Two changes on one line are two blocks in order**, the second written against the line as
  the first leaves it.
- **A change marked optional is marked in the table**, so the user can skip it without reading
  the block.

### 5. Merge the round

The user's "merge" lands the review copy and the register on `main` (`writing_branch_skill.md`,
Step 6). Nothing else changes in the merge: the repo's `.tex` is still the copy from before the
round, and stays so until they have applied the register and the source comes home.

### 6. Refresh: the source comes home

When the user brings the current source from the external editor, as a download or a paste into
staging, the refresh is one commit:

- The repo's `.tex` and its inputs are replaced by the incoming files, whole; never patched by
  hand from the register.
- **The diff between the old copy and the new one is the read.** It shows two things at once:
  the register applied (every Original gone, every Proposed present) and the co-authors' own
  edits (everything else in the diff). Report both, the co-authors' edits by section, and read
  drift in both directions: a change they made and a change of Claude's they undid or altered
  are both findings.
- A register change not found applied is listed as open; the user says whether it was skipped on
  purpose or is still to do, and an open change is re-cut against the new line numbers in the
  next round's register.
- The review copy of the closed round is deleted in the refresh commit; the register stays as
  the round's record.

### 7. Log to the ledger

The refresh is a `changed-outside` event on the paper's `.tex` row in the product ledger
(`product_ledger_skill.md`), with the co-authors' edits summarized and a pointer to the
register. A co-author's edit that contradicts something the repo holds as decided is a
divergence for the ledger's table, logged open for the user's ruling, never adjudicated at the
refresh. A paper with no ledger yet gets one at its first refresh: that is the first event git
cannot see.

---

## Key rules

- **The repo's `.tex` is a copy.** Claude edits it only at the refresh, whole, from the
  incoming source. A hand edit to the copy is a change the external editor will never see.
- **Confirm the source is current before cutting a register.** Line numbers against a stale
  copy are wrong on arrival.
- **The register is the deliverable of the round.** The review copy is scaffolding; the branch
  merge lands no LaTeX.
- **Original text anchors, line number locates.** Never the other way round.
- **Table fixes are checked in the source**, since the review copy does not show them.
- **Do not adjudicate a co-author's edit at the refresh.** Log it; the user rules.

## Edge cases

**The source moved while a round was open.** A co-author edited in the external editor between
the review copy's cut and the register's application. Line numbers may be off; the Original
text still finds each change. At the refresh, any register change whose Original text is gone is
re-cut against the new source, not forced in.

**The user applied part of the register.** Normal; the refresh reports the applied and the open
changes separately, and the open ones travel into the next register with new line numbers.

**The paper has a markdown twin the repo authors** (a policy note drawn from the paper, a deck).
That twin is a derivative in the ledger's chain, rebuilt from the refreshed source when it is
behind; it is never edited to match the register.

**The external editor has git sync.** If Overleaf's git bridge is turned on for the project,
the refresh can be a pull and the register can become a commit on the bridge; the register is
still written, since co-authors read it as the record of what changed and why. Not yet lived;
written here so the first such case has a starting point.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
