---
name: finish-session
description: "Housekeeping: the close-out ritual orchestrator for session end, the light cleaning at every close (the deep clean is repo_audit_skill.md). Sequences the five close-out steps in the right order — uncommitted-work inventory, branch disposition, STATUS.md update, conditional conversation save, confirm close — so nothing is missed. Does not re-implement those steps; points at the canonical skills (project_tracker_skill.md, repo_conversations_skill.md, writing_branch_skill.md, exploration_branch_skill.md) for the per-step procedure. Does NOT run for mid-session checkpoints, mid-session branch merges, or mid-session conversation saves — those go directly to the canonical skills without this orchestrator."
triggers: >-
  Every session close: "thanks," "good night," "we're done," "let's wrap up," "let's do
  housekeeping"; the close-out sequence, the repo's housekeeping
---

# Finish Session Skill

This skill defines the close-out ritual for a session: **housekeeping**, one of the kit's two words — the light cleaning at every close, as against the audit (`repo_audit_skill.md`), the deep clean that realigns the repo when the user asks for it. It is a **sequencing skill**: it does not duplicate work that other skills do, it orchestrates them in the right order so nothing is missed at session end.

The pieces of the close-out are already defined elsewhere: STATUS.md updates live in `project_tracker_skill.md`, conversation saves live in `repo_conversations_skill.md`, branch merges live in `writing_branch_skill.md` (and an exploration branch is finalized separately — per `exploration_branch_skill.md` — not at close). What this skill adds is (a) an explicit close-out trigger, (b) an ordered sequence so the pieces run in a sensible order, (c) a check for uncommitted work that none of the other skills owns, and (d) a single point of reference for "what happens when the user says we're done."

**What this skill is, and what it is not.** This skill defines the *checklist and ordering* for closing a session. It is **not** a re-implementation of STATUS.md updates, conversation saves, or merges — those remain in their canonical skills, and this skill points at them. The relationship: each step here is a one-line trigger ("if X, do Y per skill Z"); the per-step procedures stay in the canonical skills.

---

## When to use this skill

Read this skill when the user signals session close. Close-out signals include:
- "thanks," "thank you"
- "good night," "good morning" (when context indicates session end)
- "we're done," "let's wrap up," "let's stop here," "good stopping point"
- "save and stop," "wrap and commit"
- "let's do housekeeping," "do the housekeeping"
- Or any phrasing where the user is clearly closing the session.

Do not use this skill for:
- Mid-session checkpoints. There is no mid-session checkpoint discipline in this kit; if work matters, it gets committed when it lands. The session-start freshness check in `project_tracker_skill.md` reconstructs whatever drift accumulated.
- Branch merges that happen mid-session at the user's explicit request (those go straight to `writing_branch_skill.md` Step 6 without this skill running).
- An exploration-branch finalize, which is a deliberate mid-session act (per `exploration_branch_skill.md`), not a close-out step.
- Conversation saves that happen mid-session at the user's explicit request (those go straight to `repo_conversations_skill.md` Trigger 1 without this skill running).

---

## The close-out sequence

When a close-out signal fires, Claude runs the following five steps in order. Each step has a stop condition; do not advance until the current step is resolved.

### Step 1 — Inventory uncommitted work

Before anything else, scan for work touched this session that hasn't been committed yet. This is the gap none of the other skills owns.

Sources to check:
- Any file Claude has written to in this session that hasn't been committed **and pushed** (at Cowork, `git status` answers this directly; unpushed local commits count as uncommitted work for this purpose — they are invisible to every other session, per `github_api_workflow_skill.md`'s parallel-sessions convention).
- Drafts, indexes, brainstorms, notes, or other tracked artifacts modified in conversation but not yet committed.

If everything is committed and pushed, say so and move to Step 2.

If there are uncommitted changes:
1. Surface the list to the user.
2. Ask: "commit these now, defer to a later session, or discard?"
3. On the user's choice, act accordingly (commit, leave alone, or revert).
4. Then advance.

This step is not about being comprehensive — it's about catching the obvious gaps. The session-start freshness check in `project_tracker_skill.md` is the safety net for anything missed here.

### Step 1b — Dangling-reference scan (only if files moved or were deleted)

**Trigger:** this session moved, renamed, or deleted any tracked file. If nothing moved, skip — this step costs nothing to skip and is not part of a normal close-out.

**Why it exists.** When a file moves, the damage lands somewhere *other than where the work happened*: a `FOLDER_MAP` in an unrelated line, an index row, a live "before drafting, check X" instruction aimed at a future session. Each individual commit looks clean; the break is only visible repo-wide. Nothing else in the kit catches this — the session-start freshness check reconstructs *drift*, not *breakage*.

**How.** Grep the repo for the old paths and filenames (a tarball pull and a local `grep -rI` is far cheaper than per-file API reads). Then triage the hits:

- **Repair** — live infrastructure pointing at a moved file: `FOLDER_MAP` cross-references, index rows, `STATUS.md` instructions to future sessions. Fix by **repathing**, not rewriting: the target usually still exists, it just lives somewhere new. Where the file moved into an archive, say so in the pointer, so a future reader knows it is historical rather than current.
- **Leave** — historical records. Saved conversations, brainstorms, archived drafts, and a dated handoff or carryover record living with the work describe what was true when written; the repo does not rewrite records.
- **Leave** — coincidental string matches (a DOI, an ISBN, an unrelated filename). Check before assuming a hit is a reference.

Surface the findings, propose the repairs, and commit them with the rest of the close-out.

### Step 2 — Branch disposition (if applicable)

If session work happened on a branch, handle it **by branch type** — the two branch skills close out differently.

**Writing branch** (per `writing_branch_skill.md` — an ephemeral, single-document review branch): check whether it reached a natural stopping point.
- If the draft is complete and the user has approved it, ask: "ready to merge?"
  - If yes: follow `writing_branch_skill.md` Step 6 (merge to main, then ask about branch disposition).
  - If no: branch stays open for the next session. Note this in the STATUS.md update at Step 3.
- If the draft is mid-progress, do not ask about merging. The branch persists. Note state in STATUS.md at Step 3.

**Exploration branch** (per `exploration_branch_skill.md` — a long-lived branch testing whether a `main` claim holds): **stay light.** Do *not* prompt to merge. An exploration is finalized by a deliberate, separate act — the finalize protocol in `exploration_branch_skill.md`, invoked directly when the exploration is concluded, which can be mid-session and does not belong to session close. At close, just commit any work-in-progress to the branch and note the exploration's state in the STATUS.md update at Step 3 (it is already registered in the branch register, the catalog of `workspace/branch_logs/README.md`, from its creation; the close's catalog refresh keeps the row's Status current). The branch persists across sessions until it is finalized. This mirrors how a mid-session writing merge bypasses this skill and goes straight to `writing_branch_skill.md` Step 6 — finalizing is its own act, not a close-out step.

**Collaborator branch** (a `<id>_br_<topic>-<date>` branch in a collaborator's session — `structure_conventions.md`, "Collaborators"): the disposition is a **pull request, never a merge from this skill.** Commit the session's work to the branch (the STATUS entries of Step 3 and everything Steps 4–4c produce included), then open the pull request if none exists or push to it if one does (`gh pr create` / `git push`; mechanics per `github_api_workflow_skill.md`). Then by the roster's Merge column: `owner` — the pull request stays open for the owner, and the *Working on* block keeps its line; `self` — the collaborator merges it now if everything it touches is inside their territory, clears the *Working on* line, and leaves it open for the owner if it reaches outside (another line's files, the spine, shared trackers beyond `STATUS.md`). Note the pull request number in the `LOG.md` entry.

**In the owner's session, merging a collaborator's pull request** (at this step or mid-session) runs the **collaborator merge sweep** (`project_tracker_skill.md`): any folder the merge created outside the collaborator's workdesk territory is proposed for `workspace/staging/` and placed by the intake check on the owner's yes. A `merge: self` merge that happened between the owner's sessions is caught by the next session start's freshness check instead.

If no branch work was happening this session, skip this step.

### Step 3 — STATUS.md update

Mandatory. Follow `project_tracker_skill.md`'s session-close update protocol in full:
1. Draft the update.
2. Show the user.
3. If they review: commit clean (`reviewed` flag).
4. If they say "just commit it": commit as-is (`unreviewed` flag).
5. If they say "close now": commit without showing the draft (`unseen` flag).

The draft carries `RECORD.md`'s rows beside the entry rewrites, on every path (the tracker
protocol's "The record"): what became true of the project at the big-picture level this session.

Do not skip. Do not abbreviate. The skill exists for a reason and this step is its main trigger.

**Collaborator session (repos with a collaborator on the roster):** the same delegation applies, and the tracker protocol's collaborator branch produces the collaborator's own workstream entry on the branch, the collaborator's own queue reconciled, and the **`LOG.md` entry** — done, decisions, open — written directly on `main` in the collaborator's folder, which is the one direct write the convention allows. The Decisions block is **found by the five-event walk**, never judged (`structure_conventions.md`, "Collaborators", the `LOG.md` form): walk the conversation for the person choosing, the session asking and acting on the answer, a stated assumption, a drop or deferral, and a reading taken of an instruction that admitted more than one; write one decision per hit with its fields — unsure, asked (the instruction verbatim, when the decision was a reading), why, rejected, applied where, review state per the Merge column — and, when the walk finds nothing, the one-line *No decisions* form. The LOG entry is the immediate record; the STATUS entries reach `main` when the pull request merges.

Edge case — if the session is closing because the user is being interrupted (laptop dying, called away mid-conversation, etc.) and they explicitly say "I have to go right now" or "close now": the tracker's **unseen path**. Rewrite the touched STATUS.md entries with the best draft Claude can produce, then run **Step 4 unconditionally** — the conversation is saved verbatim as the **unseen-close transcript**, into the carryover home with no index row, and each touched entry's Resume field names it — and commit transcript and STATUS.md together, flag `unseen`. Skip Step 5 only, since the user is gone. The transcript is a resume record, read first at the retake and deleted there by default (`project_tracker_skill.md`, "The unseen path"). Better an `unseen` STATUS.md with its transcript than no update at all.

### Step 4 — Conversation save (conditional)

Check the `repo_conversations_skill.md` proactive-offer conditions:
1. Did the conversation have 3+ substantive Q&A turns on a coherent topic?
2. Did Claude consult the repo's content (papers, inputs, drafts, etc.) to answer?
3. The user has signaled closure (this is implicit — the close-out is why we're here).

If all three are true: offer the save per `repo_conversations_skill.md` Trigger 2.
- If the user accepts: follow the save workflow in `repo_conversations_skill.md`.
- If the user declines: skip.

If any of the three is false (e.g., it was a short admin exchange): skip silently. Do not offer; the conditions aren't met.

**Collaborator session with `merge: owner`:** offer the save unconditionally, after the `LOG.md` entry of Step 3 is written, whatever the three conditions say. The LOG entry's Decisions block is the mandatory record; the transcript is the person's to add, and the owner's review (`structure_conventions.md`, "Reviewing a collaborator's decisions") opens it only when the block does not answer. A decline is a decline; do not ask twice.

The order matters: STATUS.md is updated *before* the conversation-save offer. Two reasons: (a) STATUS.md is mandatory and should not be blocked by the optional save; (b) if the user declines the save, Claude has already done the most important close-out work.

### Step 4b — Model-fit capture (conditional)

Two quick checks, riding between the save offer and the close confirmation;
both usually produce nothing, and when neither applies, skip silently.

1. **Anything for the kit?** Did this session produce a kit observation not yet
   logged to the channel — a correction from the user that restated something a
   skill file already in play covers (a misfire: the file was present but not
   load-bearing; the in-the-moment offer lives in `CLAUDE.md`'s Working
   Conventions), a kit defect noticed in passing, a note about a kit file left
   in a working file or a STATUS entry? If so, offer now to log the
   `[SKILL-FEEDBACK]` entry in `<KIT_FOLDER>/CHANGELOG.md` — model version included,
   per the entry format in `structure_conventions.md`, whose same-commit rule
   this step backstops.
2. **Voice-deliverable divergence row.** Was a voice profile applied to a
   deliverable this session? Add a workdesk queue row (`workdesk/INDEX.md`) —
   Action: **do**, "give Claude the final version of <deliverable>" — so the
   session that receives the user's final version builds the divergence document
   (Claude's styled draft vs. their final, the deltas) and logs its
   `[SKILL-FEEDBACK]` entry on the profile, per `structure_conventions.md`'s
   channel section.

### Step 4c — Feedback capture (conditional)

One quick check, usually producing nothing: did the user mention feedback from a
person this session — a meeting, an email, comments on a deliverable relayed in
conversation — that is not yet filed in the repo's `feedback/` folder? If so,
offer to file it: a dated entry under `feedback/<person>/`, and, when the
product has a ledger, the `feedback` event logged pointing at it (per
`product_ledger_skill.md`). The failure this guards is feedback whose only
record is the user's memory or the chat scrollback. If they decline or nothing
was mentioned, skip silently. (The in-the-moment capture — filing feedback when
it first comes up and drives a change — is the primary mechanism; this check is
the safety net for mentions that slipped past it.)

**Steps 4 to 4c in a collaborator session.** Everything they produce — a saved
conversation and its index row, a `[SKILL-FEEDBACK]` entry in
`<KIT_FOLDER>/CHANGELOG.md`, a `feedback/<person>/` entry — is repo content or a shared
tracker, so it is committed to the collaborator's branch and reaches `main`
through the pull request, beside the STATUS entries of Step 3. The
voice-divergence row of Step 4b goes to the collaborator's own `INDEX.md`
(*For the owner*, Action: do), never to `workdesk/INDEX.md`. The `LOG.md` entry
stays the session's only direct write on `main`.

### Step 5 — Confirm close

Once Steps 1–4 are resolved, confirm to the user that the session is wrapped. A one-line "STATUS.md committed, [conversation saved | no save needed], [branch merged | branch stays open | pull request #N opened, waiting for the owner | pull request #N merged | no branch work]. Until next time." (In a collaborator's session, "STATUS.md committed" reads "STATUS entries on the branch, LOG entry on main.")

Then stop. Do not pull them into another exchange.

---

## What this skill does NOT do

- **Does not redefine the STATUS.md draft format.** That lives in `project_tracker_skill.md`. This skill says "follow that protocol;" it does not repeat the protocol.
- **Does not redefine the merge mechanics.** Writing-branch merges live in `writing_branch_skill.md` Step 6; an exploration-branch finalize lives in `exploration_branch_skill.md` and is invoked directly, never re-implemented here.
- **Does not redefine the conversation-save format.** That lives in `repo_conversations_skill.md`.
- **Does not introduce a mid-session checkpoint.** If the user wants to save mid-session, they can invoke any of the underlying skills directly. This skill only fires on close-out signals.
- **Does not assume a code-implementation hand-off.** The upstream `claude_researcher` `finish-convo` skill includes an "ask about creating a plan doc" step tied to their `write-a-plan` skill. The user's kit does not have an implementation-planning skill (`writing_skill.md` Protocol 2 already covers turning conversations into structured deliverables). If the user later adds a code-implementation planning skill, this skill's sequence will need a new step; for now, the gap is intentional.

---

## Composition with other skills

This skill is the **downstream session-close orchestrator** that wires together the kit's existing close-out pieces.

- **`project_tracker_skill.md`** — owns the STATUS.md update protocol. This skill triggers it (Step 3).
- **`repo_conversations_skill.md`** — owns the conversation-save protocol. This skill triggers it conditionally (Step 4).
- **`writing_branch_skill.md`** — owns the writing-branch merge protocol (Step 6 there). This skill triggers it conditionally (Step 2 here).
- **`exploration_branch_skill.md`** — owns the exploration finalize protocol. This skill does *not* trigger it; at close it stays light on an exploration branch and notes state (Step 2). Finalizing is a separate, deliberate act, invoked directly.
- **`github_api_workflow_skill.md`** — owns the commit mechanics used in Step 1. This skill does not duplicate the commit recipes; it points at the canonical patterns.

Now that this skill ships, the close-out sequence has a single entry point.

---

## Notes on scope

- **Generic skill, propagates to all content repos.**
- **A canonical kit repo does not use this skill at session close.** If you keep one, its close-out discipline is "commit the kit changes per the consolidation workflow," governed by that repo's own consolidation skill, not this one.
- **No `update-docs` analog.** The upstream `claude_researcher` has a separate `update-docs` skill for mid-session checkpoints. This kit deliberately does not port it.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
