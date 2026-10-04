---
name: add-to-reading-list
description: Use when the user says "add to reading list," "save this for later," "queue this," "read later," "add [X] to my reading list," or similar. Captures a paper, blog post, or other doc for later engagement by appending an entry to READING_LIST.md at repo root with a short "why" so future-you remembers what saved it. If the item is a paper we don't already have in the collection, defers to the add-paper skill first.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Identify the item (reference, URL, why)
2. If it's a paper we don't already have, defer to the add-paper skill
3. Append the entry to READING_LIST.md (create the file if missing)
4. Report what was captured
</required>

# Adding to the Reading List

Announce at start: "I'm using the Add-To-Reading-List skill to queue this for later."

The reading list is a lightweight queue of docs the user has flagged as "worth engaging with, but not now." Companion skill: `review-reading-list` pulls items off the list for deep reading + discussion.

## Step 1: Identify the item

Pull three fields from what the user just said (and the surrounding conversation):

- **Reference** — title, citation, or short descriptor (e.g., `Foo & Bar 2024 — "Distillation Sabotage in RLHF"`, `Karpathy blog on nanoGPT`).
- **URL** — the link, if one was provided or is obvious from context. Blank is fine for citation-only entries.
- **Why** — one line: why the user wants to read this. Draw from the conversation ("relevant to the flare-design threat model," "background for the coalition-building convo," "cited in Y"). This field is the reason the item was saved; without it, future-you can't tell whether to still care. If nothing in the context makes it obvious, ask one short question.

<good-example>
- **Why:** cited as the counter-case in the coalition convo; check whether its threat model actually holds.
</good-example>
<bad-example>
- **Why:** looks interesting.
</bad-example>

## Step 2: If it's a paper we don't already have, defer to add-paper

Check whether the item is already in the papers collection:

```bash
ls papers/ 2>/dev/null | grep -i "<author-or-keyword>"
```

**Defer to the `add-paper` skill** when the item is a paper (arxiv link, journal URL, DOI, direct PDF, or a URL the user has said they'll Print-to-PDF) AND it is not already in `papers/`. That skill obtains the PDF, extracts text, and writes the `PAPER_SUMMARIES.md` entry (the index row is generated from it). Return here with the resulting filename to reference in Step 3.

**Skip this step** when:
- The item is already in `papers/` (use the existing filename in Step 3).
- The item is a blog post, article, or other non-paper URL — those live as URL-only reading-list entries unless the user asks to keep the item in the collection (then `add-paper`, which handles non-PDF sources).
- The item is a citation with no URL and no PDF — captured as a reference-only entry.

## Step 3: Append to READING_LIST.md

If `READING_LIST.md` does not exist at repo root, create it:

```markdown
# Reading List

Docs, papers, and articles queued for deeper engagement. Pull items off with the `review-reading-list` skill.

---
```

Append the new entry at the bottom of the file. The list is a queue — new items go last so first-in, first-out is the natural default; the user can reorder manually if they want a different priority.

Get today's date with `date -u +%Y-%m-%d` and format the entry:

```markdown
- **[YYYY-MM-DD]** <Reference>
  - URL: <url or "none">
  - File: `papers/<filename>.pdf` (omit this line if the item isn't a paper in the collection)
  - Why: <one-line reason>
```

## Step 4: Report

```
Captured to READING_LIST.md:
  Reference: <ref>
  URL:       <url or "none">
  File:      <path or "none">
  Why:       <why>
```

If `add-paper` was invoked in Step 2, mention that the paper is now in the collection so the user knows the summary already exists (the reading list is queueing the deeper engagement, not the initial ingest).

Do NOT commit — the user may be queueing multiple items in a row, or may want to edit the entry first.

# Common Mistakes

**Blocking on approval**
- Problem: Turning a two-second "save this" into a round-trip discourages the user from queueing at all.
- Fix: Draft and append. The Step 4 report is the review surface; the user can edit `READING_LIST.md` or say "fix that entry."
