---
name: writing-branch
description: "Branch-based workflow for collaboratively producing markdown documents that the user wants to review and edit before signoff. The branch is ephemeral — typically one session — and merges as a finished deliverable. Use whenever Claude and the user are jointly producing a document (slide content, talking points, briefings, narrative drafts, papers, literature mappings, research notes) and the user needs to read and react at their own pace before merging to main. Triggers automatically when Protocol 2 of writing_skill.md engages (outlining → branch). Branches hold markdown only — companion artifacts (docx, pptx, LaTeX) are built from main after merge. Does NOT apply to an exploration whose purpose is to test whether a claim on main holds (a robustness check, an alternative specification) — that is a long-lived, isolated exploration branch with its own skill (exploration_branch_skill.md); nor to general-purpose branch use (experiments, parallel versions, code refactors — plain git)."
triggers: >-
  Any co-produced document reviewed on a branch; merge at session close or on request
---

# Writing branch workflow for collaborative document review

**Status:** active.
**Owner:** the user.
**Applies to:** any case where Claude and the user are jointly producing a document and the user wants to read and comment on it before signing off. Typical examples: slide content, talking points, briefings, narrative drafts, papers, literature mappings, research notes — with or without companion artifacts (docx, pptx) generated from the markdown. The branch is ephemeral — it holds one document under review and closes at merge.

**Does not apply to:** an *exploration* — work whose purpose is to test whether a claim on `main` holds (a robustness check, an alternative specification, a re-analysis that could move a conclusion). That is a long-lived, isolated exploration branch with its own skill (`exploration_branch_skill.md`). Nor does it apply to general-purpose branch use (an experiment, a parallel version, a code refactor) — that is plain git. This skill is specifically the ephemeral, single-document review branch.

---

## Why this workflow exists

When a document goes through review and edits, working directly in `main` creates two problems:

1. **Edits scroll past in chat.** When the user reads the document at their own pace and reacts, their comments accumulate. If they send them all in one chat message, Claude has to parse a wall of edits and risks missing one. If they send them across several messages, intermediate state lives only in chat history.
2. **`main` becomes unstable.** A coworker pulling `main` mid-edit gets a half-finished document. The deck a coworker clicks to open three days from now should not be a draft.

The branch workflow solves both: edits go in the markdown file with inline notes, the branch holds intermediate state, and `main` only updates when review is done.

---

## When to use this workflow

**Use a branch when:**
- **Protocol 2 of `writing_skill.md` is engaged** — i.e., an outline is being built or has been built. Outlining triggers a branch automatically, at the point the outline is first saved (after the scale check). The branch holds the outline, the drafting-unit drafts, the compiled outline + divergence table, and the review. See `writing_skill.md` Protocol 2 step 1.
- Claude and the user have produced a document together (not via Protocol 2 — e.g., a doc imported from elsewhere, or a second pass on a finished doc) and the user wants to review it before signoff.
- The document is markdown — with or without companion artifacts (docx, pptx). The branch only ever holds markdown. Companion artifacts are built from `main` after merge (see Step 4 and Step 6).
- The deliverable will be touched by other people (a colleague, the RA, coworkers) and `main` should stay stable through the review.

**Skip the branch (work directly in `main`) when:**
- The change is a single small edit that takes one round.
- The task is exploratory drafting where the user is iterating in real time in chat and there is no outline yet (emails, short talking points, brief messages, single-slide bullets).
- The file is a working scratch document not consumed by anyone else.
- The user wants a branch to test whether a `main` claim holds — a robustness check, an alternative specification, anything whose purpose is to put a `main` claim at risk. That is an exploration branch (`exploration_branch_skill.md`), not this skill. For any other branch reason, use plain git.

When in doubt, propose the branch and let the user say no. But if Protocol 2 is engaged, there is no doubt — branch.

---

## The protocol

### Step 1 — Branch creation

When starting an edit round on a document, Claude creates a branch from `main` — mechanics per `github_api_workflow_skill.md` (the repo-access authority): `gh_create_branch` on claude.ai web, `git branch` + push at Cowork.

**Branch naming convention:** `<project-slug>-<purpose>-<date>`
- Project slug: short, kebab-case (e.g. `reviewer-agency`, `survey-paper`, `annual-report`).
- Purpose: `edits`, `restructure`, `redraft`, `review`.
- Date: `mmm-d` format (e.g. `may-1`, `jun-15`).
- Examples: `reviewer-agency-edits-may-1`, `survey-paper-redraft-jun-3`.
- **Collaborator branches** (repos with a collaborator on the roster — `structure_conventions.md`, "Collaborators"): any branch not the owner's carries the person first — `<id>_br_<topic>-<date>`, e.g. `sam_br_server-checks-sep-10` — so the author of every branch is visible in the branch list, and none collides with the owner's hyphenated names. A collaborator's branch closes as a pull request, not a Step 6 merge; who merges is the roster's Merge column (`CLAUDE.md` Collaborators). Review of a collaborator's pull request with the owner as reviewer — this skill's roles inverted, the collaborator's Claude applying their comments — is not yet written; it is the open piece, to be written at the first such review.

**Register it at creation:** one row in the branch register, the catalog of `workspace/branch_logs/README.md` on `main` (`structure_conventions.md`, "Exploration-branch artifacts"; the body in `standing_documents_template.md`) — the branch, the date, what it holds, the folder or workstream it extends, Status `open` — so a later session finds work that lives on the branch without scanning git. **From a temporary worktree** (a branch cut in a clone other sessions share): sync first; write the row on `main` when that is safe (the clone's `main` clean, no parallel session committing to it), otherwise on the branch, where it reaches `main` with the merge. Until then a session reading `main` does not see the branch; that window is the accepted cost. A collaborator's Claude writes the row for its own branch. At Step 6 the row is annotated `merged <date> into <path>`; a branch dropped without a merge is annotated `abandoned <date>`.

Once a branch exists, Claude points the user to it and tells them which files to edit.

**That sentence is the handover, and it starts a lock.** From the moment Claude points the user to the branch until they signal end-of-round at Step 3, the branch is theirs and Claude does not write to it. See Convention 3.

### Step 2 — The user edits in the branch

The user opens the markdown files in the branch (via VS Code, GitHub web UI, or any text editor) and works in two modes — interchangeably, in the same file:

**Mode 1 — Inline bracketed comments.** The user writes their thoughts in plain language inside square brackets, in their own words. Examples:

```
[this is wrong, fix it]
[too long, cut to one sentence]
[change "12 points" to "12 percentage points"]
[move this to slide 8]
[not sure about this paragraph — what do you think]
[check that Smith 2022 is the right citation here]
```

There is no fixed vocabulary or required tag — the user writes what they mean and Claude figures out what to do. The principle: brackets signal "this is a note for Claude, not document content."

**Mode 2 — Direct edits to the text.** The user may rewrite a paragraph, replace a sentence, or restructure a list directly, without leaving an instruction. The new text *is* the edit.

Both modes are valid and can appear in the same file at the same time.

**How Claude reads bracketed comments.** Claude infers what the comment means from its content:

- If it reads as an instruction (e.g. "fix the typo", "change X to Y", "delete this", "move to slide 8") → Claude does the thing, and asks first if it's substantive enough to involve a choice.
- If it reads as a question or expression of uncertainty (e.g. "not sure about this", "what do you think", "is this the right framing") → Claude treats it as a discussion item, not an instruction. Claude responds in chat or in the report-back, but does not edit the document.
- If it's ambiguous (could be either) → Claude asks before acting.

If the user wants the action interpretation forced, they can write something unambiguous like "yes, do it" or "fix this." If they want the question interpretation forced, a question mark or "not sure" makes it clear.

### Step 3 — The user edits on the remote

The user always edits the markdown files directly in the branch via the GitHub web UI (or local git, if they prefer — the substance is the same: edits are committed to the branch, not pasted in chat).

The user signals end-of-round with phrases like "ready," "done," "go ahead," or "take it from there." At that point Claude pulls the latest branch state.

This skill does not support a "paste edits in chat" path. Edits live in the branch, not in chat. Discussion of edits — questions, decisions, framing — happens in chat; the edits themselves do not.

### Step 4 — Claude applies the edits and proofreads direct changes

Claude pulls the latest branch state. The user's edits come in two flavors and are handled differently:

**Mode 1 — Bracketed comments.** Claude applies what each comment asks for, per the interpretation rules in Step 2 (action vs. question vs. ambiguous). Claude strips the brackets from the final text after applying. Anything ambiguous gets surfaced in the report-back without auto-editing.

**Mode 2 — Direct edits (the user wrote new text in place).** Claude detects these by comparing the current branch state to the branch-creation commit (`git diff <creation-commit> <branch-tip>`). Anything that changed but isn't a bracketed comment is a direct edit. Claude proofreads each direct edit:

- **Light proofreading — silent fixes.** Typos, missing or wrong accents (especially for Spanish), capitalization, punctuation, citation formatting (e.g., reformatting "Smith et al, 2023" → "Smith et al. 2023"). Claude just applies these.
- **Heavy proofreading — surface as a note.** Terminology drift (e.g., the user wrote "brecha" but the doc convention is "distancia"), inconsistency with the rest of the document, voice or style mismatch. Claude does *not* auto-fix these. Instead, Claude raises them in the report-back with a parenthetical reminder that the user should have left a comment for these — i.e., heavy issues are discussed before action, never silently corrected.

After applying Mode 1 actions and Mode 2 light fixes, Claude pushes the updated markdown to the **branch** (not to main).

**Companion artifacts are not built on the branch.** If the markdown has companion artifacts (docx, pptx, LaTeX), they stay at whatever state they had on `main` when the branch was created — *the branch never contains a regenerated artifact*. The reason: the user iterates on markdown across multiple rounds, and rebuilding the artifact on every round wastes effort and clutters the branch. Artifacts are produced only after the markdown is approved and merged (see Step 6).

### Step 5 — Claude reports back

After applying, Claude confirms what was changed and what's now in the branch, with three sections:

- **Comment-driven changes.** Files updated per the user's bracketed comments. Comments that needed interpretation (i.e. ambiguous — could be instruction or question) are surfaced. Comments Claude read as questions or expressions of uncertainty get Claude's response here. Verification requests (e.g. comments asking Claude to check a fact or citation) get the result here.
- **Direct edits — light fixes applied silently.** A short list of mechanical fixes Claude made to the user's direct edits (typos corrected, accents added, etc.). One line each, mostly for transparency. The user can skim or skip.
- **Direct edits — heavy issues flagged.** Anything Claude noticed in the user's direct edits that crosses into terminology, consistency, or voice — *not auto-fixed*, surfaced for the user to decide. Each item includes a parenthetical reminder that the user should have left a comment in this case, so the heavy issue gets resolved before action.

This becomes the next checkpoint — the user reads it, decides if another round is needed, and either iterates or merges.

### Step 6 — Merge to main

When the user says "merge" or "ready to merge" or "looks good, merge it", Claude merges the branch into `main` — mechanics per `github_api_workflow_skill.md` (the repo-access authority): `gh_merge` on claude.ai web, `git merge` + push at Cowork; the merge commit message names the branch and summarizes what changed. A merge conflict stops the work and goes to the user — never resolved silently.

Claude reports the merge SHA and confirms `main` is updated.

**Companion files in the merge.** When the branch holds a draft produced via `writing_skill.md` Protocol 2, the merge includes both the draft (`<name>.md`) and the compiled outline + divergence table (`<name>_OUTLINE.md`) as a pair — they're approved together at Protocol 2 step 11 and merged together. Both ship in `main`.

**Building companion artifacts after merge.** If the merged markdown drives a docx, pptx, or LaTeX deliverable, Claude builds the artifact from `main` once the user asks. If the user does not ask, no artifact is built — the markdown on `main` is the deliverable. The build happens on `main`, not on the branch (the branch is closed at merge).

**Branch disposition — ask every merge.** After the merge, Claude asks the user whether to keep or delete the branch. There is no default. Branches are not part of the repo's history unless the user says so. Ask every round, no carryover from prior decisions. If they say delete, Claude deletes the branch (mechanics per `github_api_workflow_skill.md`). If they say keep, the branch stays and Claude does nothing further.

---

## Conventions for Claude

1. **Branch creation is at Claude's initiative when the trigger conditions are met.** The user does not need to ask. Claude proposes: "I'm setting up a branch `<name>` for this round of edits." If the user wants to skip the branch, they say so.

2. **Never push edits to `main` while a branch is open for that document.** Pushing to both creates conflicts. The branch is the authoritative version while it's open.

3. **The branch belongs to the user from handover until they close the round. Claude does not write to it in that window.** Handover happens the moment Claude points them to the branch at Step 1. The window closes when they say the round is done, send their edits, or explicitly ask for a change to be made. Inside it Claude does not touch the file for **any** reason: not a correction Claude is confident about, not a number they asked for in chat, not an improvement that seems obviously good. If something needs to change mid-round, Claude says so in chat and waits.

   **Why this is a prohibition and not a check.** The user's edits may live only in a browser tab or an unsaved editor buffer — invisible to git, to the remote, and to every tool Claude has. "Pull first and look" would report a clean tree and wave Claude through. Not writing is the only protection that works.

   *(The protocol's turn-taking already implied this; it was never stated as a prohibition, and the implication was not enough.)*

4. **Read the file immediately before editing it, and replace only exact text.** Never replace a region located by its boundaries — headings, line numbers, indices, "everything between A and B". Boundary replacement deletes whatever sits inside the region with no conflict and no warning, which is exactly how a person's comments disappear. Exact-string replacement fails loudly when the file has changed underneath, and **that failure is the point.** This applies to every file a person may have open, not only to branches.

   **And verify what a bulk edit touched before committing it.** A script or a pattern reaches further than its author pictures. Read the diff before committing: check the changed-line count against what you expected, and read at least one hunk outside the region you were aiming at. Reporting a rule as applied when a skip condition silently excluded most of its targets is the same class of error as writing over someone's work, and it is caught the same way.

5. **Branches hold markdown only. Companion artifacts (docx, pptx, LaTeX) are built from `main` after merge, only when the user asks.** Do not regenerate or push artifacts to the branch under any circumstances. Stale artifacts on `main` during a review round are expected — they reflect the last merged version of the markdown, not the in-flight branch.

6. **Inline notes get stripped from the output, not preserved.** The final markdown that lives in main is clean text. The user's notes are processing instructions, not document content.

7. **If the user's note is ambiguous, ask before applying.** Don't guess on substantive changes. For typo-level fixes, just apply.

8. **For the user's direct edits, light fixes are silent and heavy issues are surfaced.** Mechanical things (typos, accents, punctuation, citation formatting) get fixed without comment. Anything that crosses into terminology, consistency, or voice is *never* auto-fixed — it goes in the heavy-issues section of the report-back so the user can decide. The principle: if the user wanted Claude to make the call on a heavy issue, they would have left a comment.

9. **At end of round, surface every interpretation Claude made.** If the user wrote "tighten this paragraph" and Claude rewrote it three different ways, Claude says so and shows the result.

10. **Branches accumulate per project.** If the user opens a second round of edits, create a new branch (e.g. `reviewer-agency-edits-may-2`) — do not reuse the previous branch. Each branch represents one closed edit round.

11. **Round-count checkpoints: at the third round in one session, remind; at the sixth, insist very strongly.** When one session has applied three review rounds to the same document, Claude checks how much of its context window the session has consumed and reminds the user that a fresh session may serve the remaining rounds better; they can wave it off. At six rounds Claude insists very strongly, and if Claude judges its own execution risk high that judgment is Claude's to act on, not the user's to override. The failure this guards is invisible from inside the session: round-by-round patching compresses prose into the dense register the plain-register rule bans, and the session doing the patching cannot see it.

12. **A version is cut at the feedback intake, not on the branch.** When the merged document goes to a reviewer and the first feedback comes back, a byte-exact copy of what went out is cut into `versions/` beside the document (`structure_conventions.md`, "Versions vs. archive"; the ledger's `versioned` event). The branch holds edit rounds, not versions: a round is the user's own pass and produces no copy.

---

## What this workflow doesn't cover

- **Exploration branches.** Work whose purpose is to test whether a `main` claim holds is a long-lived, isolated exploration branch — see `exploration_branch_skill.md`. This protocol is the ephemeral, single-document review case only.
- **General-purpose branch use.** Any other branch reason (an experiment, a parallel version, a code refactor) uses plain git, not this skill.
- **Code review.** Code collaboration uses standard PR-based git flow but isn't formalized here.
- **Multi-author editing.** If a coworker is also editing the document at the same time, this protocol breaks. Tell the user immediately if that happens.
- **A paper whose live LaTeX source is edited outside the repo** (Overleaf, co-authors). The branch loop still runs, but on a markdown review copy regenerated from the source each round, and the round lands as an apply register the user works from by hand, never as a merge into the `.tex` — `latex_round_trip_skill.md` owns that case; Convention 5's "built from `main` after merge" applies only to a paper the repo authors.
- **Permissions.** Per `github_api_workflow_skill.md`'s environment branch.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
