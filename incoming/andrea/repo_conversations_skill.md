---
name: repo-conversations
description: "Save, index, and retrieve substantive conversations between the user and Claude that take place inside a repository — when the conversation used the repo's content and produced material worth keeping. Saved conversations are retrievable artifacts for later analytical work, NOT a resumption mechanism (where work was left off lives in STATUS.md and CLAUDE.md). Also offered proactively at a topic transition (when the user moves on to a new task after a substantive 3+ turn exchange), which saves the just-finished segment; session-end saving is owned by finish_session_skill.md. Does NOT apply to casual one-off questions or conversations where Claude didn't actually use the repo's content."
triggers: >-
  "save this conversation"; a multi-session topic worth finding later; proactively after a
  substantive exchange
---

# Repo Conversations Skill

This skill defines how to save, index, and retrieve conversations between a user and Claude that take place inside a repository — when those conversations are about the repo's contents and produce content the user wants to keep.

The point is to preserve high-value Q&A exchanges (where the user worked through something with Claude using the repo's content) so they can be retrieved later by topic, date, or content, **without Claude having to re-read every transcript**. Saved conversations are inputs for later analytical work — not deliverables.

**What saved conversations are, and what they are not.** A saved conversation is a *retrievable artifact* — a record of one substantive Q&A exchange, indexed for later lookup by topic or date. It is **not** a resumption mechanism. Where work was left off lives in `STATUS.md` and the trackers, not in the saved-conversations folder. When starting a new session and trying to figure out the project's current state, read the trackers. The Working Conventions in `CLAUDE.md` cover this rule canonically; this note is here so the reconciliation is visible from the skill side too.

---

## When to use this skill

Read this skill when:
- The user asks to save the current conversation, or asks to look up a past conversation.
- A substantive exchange (3+ Q&A turns on a coherent topic) reaches a topic transition — the user moves on to a different task while the session continues.
- The user asks "what did we say about X?" or anything that suggests they want to find a prior conversation.

Do not use this skill for:
- Casual one-off questions where nothing is asked to be saved.
- Conversations where Claude hasn't actually used the repo's content (general knowledge questions).

---

## Repo-specific parameters

Saved conversations live in `workspace/claude_conversations/`, the universal home every repo carries (`structure_conventions.md`), with the index `INDEX.md` beside them; neither is a parameter. Two parameters are read from the repo's `CLAUDE.md` **Repo parameters** table (`CLAUDE_template.md`, the single home for every parameter the always-active skills read); if the table does not define one, use the default given here.

| Parameter | Description | Default |
|---|---|---|
| `USER_IDS` | List of user identifiers used in this repo (if multiple users). A repo with a Collaborators roster in `CLAUDE.md` (`structure_conventions.md`, "Collaborators") takes the roster's id column | None — omit user identifier from naming and metadata if not defined |
| `TAG_THRESHOLD` | Number of saved conversations after which Claude offers to propose a tag vocabulary | 10 |

---

## Save triggers — when to write a transcript

There are two save triggers. Default = explicit. Proactive offer = secondary, when conditions are met.

### Trigger 1 — Explicit (default)

The user says something like:
- "save this"
- "save this conversation"
- "save this note"
- "let's keep this"
- "save what we just discussed"

When this happens, Claude proceeds straight to the save workflow. No confirmation needed unless the conversation is ambiguous (e.g., a long thread that touched multiple topics — Claude may ask which part to save, or whether to save it all).

### Trigger 2 — Proactive offer (secondary)

When **all** of the following are true, Claude proactively asks "Save this conversation?":

1. The conversation has had at least 3 substantive Q&A turns on a coherent topic.
2. Claude has used the repo's content (consulted the repo's sources, notes and materials, etc.) to answer.
3. The user has signaled a **topic transition** — moving on to a different task or subject while the session continues: "let's move on to the next task," "ok, next," "let's switch to Y," "moving on," "let's do X now," etc.

The transition signal is deliberately **not** a session-closure signal ("we're done," "good night," "thanks, that's all"). Session-end saving is owned by `finish_session_skill.md`, which asks about saving the conversation as part of its close-out sequence; pointing this proactive offer at closure signals too would double up. Topic transitions mean the session keeps going, so the two triggers never overlap.

One case at the close is unconditional: in a collaborator's session whose roster row says `merge: owner`, the close offers the save whether or not the three conditions hold (`finish_session_skill.md` Step 4). The mandatory record of that session is the `LOG.md` entry's Decisions block (`structure_conventions.md`, "Collaborators"); the saved conversation is the transcript behind it, read at the owner's review only when the block does not answer. Saving stays the person's choice.

A topic transition is also the moment a just-finished topic is most likely to get buried, which is exactly why it is the right place to catch it. And because the user is leaving topic X for something else, the exchange worth saving is the **X segment** — so this offer naturally produces a *segment* save (see "Saving a segment of a conversation" below): Claude proposes the cut ("save from where we picked up X to here?") and confirms before writing.

If any of those is missing, do not offer. The proactive offer is meant to catch genuinely useful exchanges the user might forget to save — not to add noise.

If the user declines a proactive offer, do not offer again for that same topic in the session.

### What is NOT a trigger

- One-off factual questions (e.g., "what's the publication date of the agency's annual report?") with a one-line answer.
- Conversations where Claude did not consult the repo (general knowledge questions, formatting help, planning conversations about what to do next).
- Conversations the user explicitly says are draft/exploratory and not to be saved.

When no save trigger fires, no file is created. The folder does not collect every conversation — only the ones the user wants to keep.

---

## File naming

Each saved conversation is one file. Naming convention:

- **With user identifiers** (when `USER_IDS` is defined): `YYYY-MM-DD_<who>_<short-tag>.md`
  - Example: `2026-05-08_jsmith_survey-design.md`
- **Without user identifiers** (when `USER_IDS` is not defined): `YYYY-MM-DD_<short-tag>.md`
  - Example: `2026-05-08_survey-design.md`

`<short-tag>` is a 2–4 word slug describing the topic. Use hyphens between words (`survey-design`, `sampling-frame`, `response-rates`). The slug should match (or anticipate) one of the conversation's tags.

If two conversations on the same day from the same user are on different topics, they get two separate files (different short-tags).

If the user revisits a topic on a later day, that becomes a new file with a shared tag — not an append. The index links them by tag.

---

## Transcript file format

Each saved conversation file has this structure:

```markdown
# <Short-tag, human-readable> — YYYY-MM-DD

## Metadata

| Field | Value |
|---|---|
| Date | YYYY-MM-DD HH:MM |
| Who | <user identifier — only if USER_IDS is defined> |
| Scope | Full conversation — or: Segment, from the start of the discussion of X |
| Main questions | (1) ... (2) ... (3) ... |
| Tags | tag-1, tag-2, tag-3 |
| Sources cited | path/to/file1, path/to/file2, ... |

---

## Transcript

**User:** <user message>

**Claude:** <Claude's response>

**User:** <user message>

**Claude:** <Claude's response>

...
```

### Field rules

- **Date** — YYYY-MM-DD HH:MM in the user's local time when known; otherwise UTC.
- **Who** — the user identifier from `USER_IDS`. Omit the row entirely if `USER_IDS` is not defined for the repo.
- **Scope** — `Full conversation`, or `Segment — from <where the topic began>` when only part of a session is saved (see "Saving a segment of a conversation"). The row may be omitted for a full conversation; it is required for a segment, so a later reader knows the "Main questions" reflect only the saved part.
- **Main questions** — 1 to 3 of the questions the user actually asked, in their own words (or a faithful condensation). Phrased as questions, not as topics. These are the primary retrieval cue.
- **Tags** — short, lowercase, hyphen-separated. 2–6 tags per conversation. Free-form during the bootstrap phase (before `TAG_THRESHOLD` is reached); from the controlled vocabulary afterward (see "Tag vocabulary" below).
- **Sources cited** — repo-relative paths to files Claude actually consulted to answer. Comma-separated. Empty if Claude answered from general knowledge alone.

### Transcript content

The transcript is the **verbatim conversation**, not a summary. The point of the transcript layer is to preserve the actual exchange for later processing — other protocols handle summarization, theming, or extraction.

When transcribing:
- Use **User:** and **Claude:** as turn labels.
- Preserve the user's words exactly. Do not clean up typos or rephrasing — they are part of the record.
- For Claude's responses: preserve the substance. If a response was very long, abridging is acceptable but flag it with `[...abridged for length]`.
- Code blocks, tables, and quotes from the repo are preserved as-is.

---

## Index file (`INDEX.md`)

A single flat index, `INDEX.md` in the folder, lists every saved conversation. The index is the first lookup layer when retrieving past conversations.

### Format

```markdown
# Index — Claude Conversations

This index lists every saved conversation in this folder. To find a past conversation: scan the index by tag, date, or user; open the candidate transcript's metadata table to confirm; only open the full transcript if needed.

<!-- slot: catalog -->
| Date | Who | Main question(s) | Tags | File |
|---|---|---|---|---|
| 2026-05-08 14:30 | jsmith | Survey design + the sampling frame | survey-design, sampling-frame | [link](2026-05-08_jsmith_survey-design.md) |
| 2026-05-09 09:15 | mlee | Response rates — the threshold for reweighting | response-rates, reweighting | [link](2026-05-09_mlee_response-rates.md) |
<!-- /slot -->

<!-- slot: notes -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->
```

### Column rules

- **Date** — date and time, matching the transcript metadata.
- **Who** — the user identifier. Omit the column entirely if `USER_IDS` is not defined. A `Who` column standing where `USER_IDS` is `none` is dropped at the pass, its one value kept in the row's text if it says something.
- **Main question(s)** — 1-line condensation of the questions field, suitable for at-a-glance scanning.
- **Tags** — same as the metadata table.
- **File** — markdown link to the transcript file.

Sort: most recent at the top.

The markers are the kit's one notation (`structure_conventions.md`, "Slots and markers, one
notation"): the header row inside `slot: catalog` is kit form, regenerated at every propagation so
a column added here reaches every repo; the rows are the repo's.

### Index updates

Every time a new transcript is saved, the index gets a new row. The index exists from the repo's birth as the folder's standing document (`standing_documents_template.md` points here for the body); a repo without one gets it at the next propagation.

---

## Retrieval — using the index

When the user asks "what did we say about X?" or "do we have a conversation about Y?", follow this lookup sequence:

**Step 1 — `INDEX.md`.** Read the index. Filter rows by tag, date, user, or main question. Identify candidate transcripts.

**Step 2 — Metadata table at the top of each candidate transcript.** Open only the candidates from Step 1. Read the metadata table. Confirm whether the conversation actually addresses the user's question.

**Step 3 — Full transcript.** Open the full transcript only when the metadata confirms it's the right conversation, and only the relevant portions if the transcript is long.

Do **not** read every transcript top-to-bottom by default. The index and metadata layers exist precisely to avoid that.

---

## Tag vocabulary

### Bootstrap phase — free-form tags

Until the folder reaches `TAG_THRESHOLD` saved conversations, tags are free-form. Claude proposes tags at save time based on the conversation's content; the user can accept, edit, or override.

Recommended approach during bootstrap:
- Use lowercase, hyphenated, 1–3-word tags.
- Reuse existing tags from prior conversations when appropriate (check the index).
- 2–6 tags per conversation.

### Threshold phase — propose a vocabulary

When the folder count reaches `TAG_THRESHOLD` (default 10), at the next save Claude offers:

> "We now have N saved conversations. Want me to propose a tag vocabulary based on what's accumulated, and retag existing conversations to align with it?"

The user has three options:
- **Accept** — Claude reviews the existing tags, proposes a controlled vocabulary (typically 8–20 tags), gets the user's approval, and runs a retag pass on existing transcripts and the index.
- **Defer** — Claude doesn't ask again until the count grows by some amount the user specifies (e.g., "ask me at 15"). The folder stays in bootstrap mode.
- **Decline permanently** — the folder stays free-form indefinitely. Claude does not ask again.

The user's choice is recorded in the index's `notes` slot so the decision persists across sessions.

### Post-threshold — controlled vocabulary

After acceptance, all new conversations use tags from the approved vocabulary. New tags are added only when the user approves an addition.

The controlled vocabulary lives in the index's `notes` slot. Every save consults that list before tagging.

---

## Saving a segment of a conversation

A save can cover an entire conversation or a coherent **segment** of one — the part since a topic began. This is a first-class path, not an exception. It is the normal output of the Trigger 2 proactive offer (which fires at a topic transition, so the segment is the topic being left), and it is also available on explicit request ("save this conversation since we started talking about X").

**Identifying the boundary.** Before writing, Claude proposes the cut point and confirms it — it does not write until the user agrees:

- If the user named a boundary ("since we started on X"), Claude proposes it back concretely — "save from your message about X (the one starting '<first few words>') to here?" — and writes only on confirmation.
- If the boundary is unclear, Claude proposes its best guess of where the topic began and asks the user to adjust. There is no scanning for a boundary the user hasn't roughly indicated; Claude proposes, the user corrects.

**Recording that it is a segment.** The transcript's metadata `Scope` row notes that the file is a segment and where it starts, so a later reader knows it is not the whole session and that the "Main questions" reflect only the saved part. Everything else — naming, index row, tags, retrieval — is identical to a full save; the only difference is the `Scope` row and that the transcript begins at the cut point rather than the start of the session.

---

## Save workflow — step by step

When a save trigger fires:

1. **Identify the user identifier** (if `USER_IDS` is defined). In a repo with a Collaborators roster the session already knows who is present (`project_tracker_skill.md`, session-start step 0) — use that; otherwise, if unclear (e.g., the user might be either of two people), ask. In a collaborator's session the saved file and its index row are committed to the collaborator's branch and reach `main` through the pull request (`finish_session_skill.md`).
2. **Determine the short-tag** for the filename. Propose to the user; let them accept or override. The short-tag should match (or be one of) the conversation's tags.
3. **Construct the metadata table.** Fill in date, who, scope (full or segment), main questions (1–3), tags, sources cited.
4. **Build the transcript** in the format above. For a segment save, start at the confirmed cut point rather than the beginning of the session.
5. **Show the proposed file to the user** (the metadata table and a brief description of the transcript) and ask for approval before writing.
6. **On approval, write the file** to `workspace/claude_conversations/<filename>.md`.
7. **Update `INDEX.md`** — add a new row at the top (or create the index if it doesn't exist).
8. **Commit** — both files in one commit. Commit message: `Save conversation: <short-tag> (<who if applicable>, YYYY-MM-DD)`.
9. **If the folder count just crossed `TAG_THRESHOLD`**, offer the vocabulary proposal (see "Tag vocabulary" above).

---

## Editing or deleting saved conversations

Saved conversations are records. Editing or deleting requires explicit user instruction.

- **Edit** — only if the user identifies a specific factual error in the transcript or metadata. The transcript content itself (what was said) is not edited; metadata can be corrected. If the user wants to add a note about a saved conversation (e.g., "this discussion led to X decision"), append it as a `## Follow-up note` section at the bottom of the transcript with a date.
- **Delete** — only on explicit user request. Update the index to remove the corresponding row.

---

## Cross-references

This skill connects to:

- The repo's main lookup sequence (`CLAUDE.md`). Saved conversations are a layer in the lookup, typically between the repo's curated notes and materials and its raw sources.
- `document_processing_skill.md` and `materials_processing_skill.md` — saved conversations may serve as inputs to a later, more formal processing step (e.g., a saved conversation about the survey design might inform a future research note).
- `writing_skill.md` — saved conversations can be sources cited when drafting a deliverable.

---

## What this skill does NOT do

- It does not summarize or theme conversations. The transcript is verbatim. Other protocols handle synthesis later.
- It does not auto-save. A save only happens when a trigger fires.
- It does not maintain a per-topic or per-source secondary index. The flat `INDEX.md` plus tags is the only retrieval structure.
- It does not version transcripts. A saved conversation is an immutable record (with the narrow exceptions in "Editing or deleting" above).

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
