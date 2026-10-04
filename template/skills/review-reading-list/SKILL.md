---
name: review-reading-list
description: Use when the user says "what's on my reading list," "read the reading list," "let's look at [X] from my list," "review the reading list," "pick from my reading list," or similar. Pulls an item off READING_LIST.md, discusses it in depth, and appends the discussion notes to the paper's PAPER_SUMMARIES entry (or logs it in RESEARCH_LOG for non-paper items). Removes the item from the reading list when done.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Show the reading list
2. Wait for the user to pick an item — do NOT auto-pick
3. Open the source (paper text from papers/text/, OR fetch the URL for non-paper items)
4. Discuss with the user
5. Append discussion notes to PAPER_SUMMARIES (paper items only)
6. Log the review in RESEARCH_LOG
7. Remove the reviewed item from READING_LIST.md
</required>

# Reviewing an Item from the Reading List

Announce at start: "I'm using the Review-Reading-List skill to walk through an item together."

This skill assumes items are already on `READING_LIST.md`. Capture happens via the companion `add-to-reading-list` skill — do not add new items here.

## Step 1: Show the reading list

```bash
cat READING_LIST.md
```

If the file doesn't exist, or contains only the header (no entries), tell the user: *"Reading list is empty. Use `add-to-reading-list` to queue something."* Stop.

Otherwise, present the list to the user. For a short list (fewer than ~10 entries) show the whole file. For a longer list, present a numbered summary — one line per entry (date + reference + one-clause why) — and offer the full file on request.

## Step 2: Wait for the user to pick

Do not auto-pick. If the user just wanted to see the list (asked "what's on my reading list?" and doesn't follow up), stop here — a "show" is a valid endpoint.

Once they name an item, look it up in `READING_LIST.md` and pull its fields: **Reference**, **URL**, **File**, **Why**.

## Step 3: Open the source

The item is one of three shapes. Handle whichever applies:

**A. Paper in the collection (has a `File:` field pointing at `papers/<filename>.pdf`).** This is the default case — `add-to-reading-list` will have run `add-paper` at capture time if the paper wasn't already present. Read the extracted text:

```bash
cat papers/text/<filename>.txt
```

Even if the paper was discussed in an earlier session, re-read the sections relevant to the current angle rather than working from memory.

**B. Non-paper URL (has a `URL:` field, no `File:` field).** Fetch the URL with the WebFetch tool and read the content.

**C. Citation with no URL and no file (rare).** Report the situation to the user and ask how to proceed:
- (a) They paste the content into the chat
- (b) Discuss from what you both remember
- (c) Skip and remove from the list

## Step 4: Discuss

Ask the user how they want to open the discussion:
- Summarize the key claims first, then dig in?
- Or jump straight into a specific question or angle?

Then engage as a collaborator, not a lecturer. Use the **Why** field as the anchor — the point of this discussion is to serve the reason the item was saved. Push back where you disagree; flag what the piece gets right and where it's weak.

## Step 5: Append discussion notes to PAPER_SUMMARIES

**Paper items only. Skip for non-paper URLs and citation-only entries** — those don't have a `PAPER_SUMMARIES.md` entry to append to; the `RESEARCH_LOG` note in Step 6 is their record.

For a paper, find its existing entry in `PAPER_SUMMARIES.md` (the neutral summary written by `add-paper`). Append a new subsection at the bottom of that entry — do NOT rewrite the summary. The neutral summary stays as source-of-truth; discussion notes are the editorial framing.

Format (get today's date with `date -u +%Y-%m-%d`):

```markdown
#### Discussion notes ([YYYY-MM-DD])

- <a claim we found notable, a caveat, or a connection to other work>
- <what we thought was the strongest or weakest point>
- <how this changes our thinking on X, if it does>
```

Three bullets is a rough guide, not a limit. Capture what was actually said in the discussion — not a rehash of the summary above.

If the user reviews the same paper again in a future session, a second `#### Discussion notes ([date])` subsection gets appended below the first. Both are preserved, chronologically.

## Step 6: Log the review in RESEARCH_LOG

Append a line to the current session's entry in `docs/active/<branch>/RESEARCH_LOG.md`. If no session entry exists yet (this is the first thing done in the session), create one — same shape as `update-docs` produces.

**For a paper:**

```markdown
- Reviewed **<Reference>** — see `PAPER_SUMMARIES.md` for discussion notes.
```

**For a non-paper URL** (no `PAPER_SUMMARIES` entry to point at, so include the URL and a 1–2 sentence takeaway inline):

```markdown
- Reviewed **<Reference>** (<url>) — <one-line takeaway>. <optional second sentence with a key claim or a link to related work>.
```

**For a citation-only entry that got discussed from memory or pasted content:**

```markdown
- Reviewed **<Reference>** (no source fetched — discussed from <memory | pasted content>) — <one-line takeaway>.
```

The RESEARCH_LOG line is what future sessions grep for when they wonder "did we ever look at this?"

## Step 7: Remove the reviewed item from READING_LIST.md

Delete the entry (the bullet plus its sub-fields) from `READING_LIST.md`. The reading list is a queue — reviewed items graduate to `PAPER_SUMMARIES.md` / `RESEARCH_LOG.md` and don't linger on the list.

If `READING_LIST.md` is now empty (just the header remains), leave the file in place — future queueing still uses it.

If the review was interrupted or cut short and the user wants to come back to it, LEAVE the item on the list and instead update the RESEARCH_LOG line to say `Partially reviewed` — do not remove until the discussion is genuinely complete.

Do NOT commit — the user may want to look at another item, or edit the notes. `finish-convo` or a manual commit picks up all the changes at end of session.
