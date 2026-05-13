---
name: branch-document-review
description: "A branch-based workflow for collaborative document review when Claude and the user are co-producing a document. Use when the user wants to read and comment on a long markdown deliverable (slide content, talking points, briefing, narrative draft, paper) before signoff — especially when the markdown has companion artifacts (.docx, .pptx) generated from it. Edits live in the branch via inline bracketed comments or direct text changes; `main` only updates when review is done. Do NOT use for general-purpose branch work (experiments, code refactors, parallel versions) — those use plain git, not this skill."
aitaxbid_source: ~/code/AITaxBID/skills/BranchWorkflow_Skill.md@e0a736d (2026-05-02)
---

# Branch workflow for collaborative document review

**Applies to:** the specific case where Claude and the user are jointly producing a document and the user wants to read and comment on it before signing off — typically a long markdown deliverable (slide content, talking points, briefing, narrative draft, paper) that has companion artifacts (docx, pptx) generated from it.

**Does not apply to:** general-purpose branch use. If the user wants a branch for another reason (an experiment, a parallel version, a code refactor, anything that is not "review a document we are making together"), they will say so explicitly. That kind of work uses plain git, not this skill.

---

## Why this workflow exists

When a document goes through review and edits, working directly in `main` creates two problems:

1. **Edits scroll past in chat.** When the user reads the document at their own pace and reacts, their comments accumulate. If they send them all in one chat message, Claude has to parse a wall of edits and risks missing one. If they send them across several messages, intermediate state lives only in chat history.
2. **`main` becomes unstable.** A coworker pulling `main` mid-edit gets a half-finished document. The deck a coworker clicks to open three days from now should not be a draft.

The branch workflow solves both: edits go in the markdown file with inline notes, the branch holds intermediate state, and `main` only updates when review is done.

---

## When to use this workflow

**Use a branch when:**
- Claude and the user have produced a document together, and the user wants to review it before signoff.
- The document is markdown that drives companion artifacts (docx, pptx, etc.) — i.e., changes to the markdown require regeneration of dependent files.
- The deliverable will be touched by other people (coworkers, collaborators) and `main` should stay stable through the review.

**Skip the branch (work directly in `main`) when:**
- The change is a single small edit that takes one round.
- The task is exploratory drafting where the user is iterating in real time in chat and there is no document yet.
- The file is a working scratch document not consumed by anyone else.
- The user wants a branch for some reason other than reviewing a co-produced document — that is not what this skill is for.

When in doubt, propose the branch and let the user say no.

---

## The protocol

### Step 1 — Branch creation

When starting an edit round on a document, Claude creates a branch from `main`:

```bash
# Get the SHA of main
MAIN_SHA=$(curl -s -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$REPO/git/refs/heads/main" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['object']['sha'])")

# Create the branch
curl -s -X POST -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$REPO/git/refs" \
  -d "{\"ref\":\"refs/heads/BRANCH_NAME\",\"sha\":\"$MAIN_SHA\"}"
```

**Keep `MAIN_SHA` around** — Step 4 uses it as the base of the Compare API call to isolate this round's edits from anything that landed on `main` earlier.

**Branch naming convention:** `<project-slug>-<purpose>-<MMdd>`
- Project slug: short, kebab-case (e.g. `oecd-paper`, `tax-policy-brief`, `q3-report`).
- Purpose: `edits`, `restructure`, `redraft`, `review`.
- Date: `MMdd` format — 2-digit month + 2-digit day, no year (e.g. `0501` for May 1, `0615` for June 15). The 2-digit pattern keeps branch names **lexicographically sortable within a year**. Text-month formats (`may-1`, `jun-3`) break sort because alphabetical order puts December before January; numeric formats with single-digit days (`5-1`, `5-15`) sort wrong because `5-15` appears before `5-2`. `MMdd` avoids both failure modes. Year is omitted because branch lifetime is short and cross-year collisions are vanishingly rare.
- Examples: `oecd-paper-edits-0501`, `q3-report-redraft-0603`.

Once a branch exists, Claude points the user to it and tells them which files to edit.

### Step 2 — User edits in the branch

The user opens the markdown files in the branch (via VS Code, GitHub web UI, or any text editor) and works in two modes — interchangeably, in the same file:

**Mode 1 — Inline bracketed comments.** The user writes their thoughts in plain language inside square brackets, in their own words. Examples:

```
[this is wrong, fix it]
[too long, cut to one sentence]
[change "12 puntos" to "12 puntos del PIB"]
[move this to slide 8]
[not sure about this paragraph — what do you think]
[check that Bellon 2022 is the right citation here]
```

There is no fixed vocabulary or required tag — the user writes what they mean and Claude figures out what to do. The principle: brackets signal "this is a note for Claude, not document content."

**Mode 2 — Direct edits to the text.** The user may rewrite a paragraph, replace a sentence, or restructure a list directly, without leaving an instruction. The new text *is* the edit.

Both modes are valid and can appear in the same file at the same time.

**How Claude reads bracketed comments.** Claude infers what the comment means from its content:

- If it reads as an instruction (e.g. "fix the typo", "change X to Y", "delete this", "move to slide 8") → Claude does the thing, and asks first if it's substantive enough to involve a choice.
- If it reads as a question or expression of uncertainty (e.g. "not sure about this", "what do you think", "is this the right framing") → Claude treats it as a discussion item, not an instruction. Claude responds in chat or in the report-back, but does not edit the document.
- If it's ambiguous (could be either) → Claude asks before acting.

If the user wants the action interpretation forced, they can write something unambiguous like "yes, do it" or "fix this." If they want the question interpretation forced, a question mark or "not sure" makes it clear.

### Step 3 — User edits on the remote

The user always edits the markdown files directly in the branch via the GitHub web UI (or local git, if they prefer — the substance is the same: edits are committed to the branch, not pasted in chat).

The user signals end-of-round with phrases like "ready," "done," "go ahead," or "take it from there." At that point Claude pulls the latest branch state.

This skill does not support a "paste edits in chat" path. Edits live in the branch, not in chat. Discussion of edits — questions, decisions, framing — happens in chat; the edits themselves do not.

### Step 4 — Claude applies the edits and proofreads direct changes

Claude pulls the latest branch state. The user's edits come in two flavors and are handled differently:

**Mode 1 — Bracketed comments.** Claude applies what each comment asks for, per the interpretation rules in Step 2 (action vs. question vs. ambiguous). Claude strips the brackets from the final text after applying. Anything ambiguous gets surfaced in the report-back without auto-editing.

**Mode 2 — Direct edits (the user wrote new text in place).** Claude detects these by calling the GitHub Compare API to diff the branch tip against the branch-creation commit. `BASE_SHA` is the value captured as `MAIN_SHA` in Step 1.

```bash
curl -s -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$REPO/compare/$BASE_SHA...$BRANCH_NAME"
```

The response is JSON; the `files[]` array carries one entry per changed file with a unified-diff `patch` field. Parse each patch: any added/modified line that doesn't sit inside a `[...]` bracketed-comment block is a Mode 2 direct edit. Mode 1 brackets are filtered out at this step so they're not double-counted (they'll be handled in their own Step-2 interpretation pass).

> **Compare API note.** A single page caps at 300 changed files. Document-review rounds are almost always one or two files, well under the cap. If a future multi-file extension needs more, paginate using the `Link` header.

Claude proofreads each direct edit:

- **Light proofreading — silent fixes.** Typos, missing or wrong accents (especially for Spanish), capitalization, punctuation, citation formatting (e.g., reformatting "Adan et al, 2023" → "Adan et al. 2023"). Claude just applies these.
- **Heavy proofreading — surface as a note.** Terminology drift (e.g., the user wrote "brecha" but the doc convention is "distancia"), inconsistency with the rest of the document, voice or style mismatch. Claude does *not* auto-fix these. Instead, Claude raises them in the report-back with a parenthetical reminder that the user should have left a comment for these — i.e., heavy issues are discussed before action, never silently corrected.

After applying Mode 1 actions and Mode 2 light fixes, Claude regenerates any dependent artifacts:

- If the edited file is a markdown source for a Word document → regenerate the `.docx` with pandoc.
- If the edited file is the slide content document → regenerate the `.pptx`.
- If the edited file is a narrative for a paper → no regeneration unless the user has set up the LaTeX pipeline.

Claude pushes everything to the **branch**, not to main.

### Step 5 — Claude reports back

After applying, Claude confirms what was changed and what's now in the branch, with three sections:

- **Comment-driven changes.** Files updated per the user's bracketed comments. Comments that needed interpretation (i.e. ambiguous — could be instruction or question) are surfaced. Comments Claude read as questions or expressions of uncertainty get Claude's response here. Verification requests (e.g. comments asking Claude to check a fact or citation) get the result here.
- **Direct edits — light fixes applied silently.** A short list of mechanical fixes Claude made to the user's direct edits (typos corrected, accents added, etc.). One line each, mostly for transparency. The user can skim or skip.
- **Direct edits — heavy issues flagged.** Anything Claude noticed in the user's direct edits that crosses into terminology, consistency, or voice — *not auto-fixed*, surfaced for the user to decide. Each item includes a parenthetical reminder that the user should have left a comment in this case, so the heavy issue gets resolved before action.

This becomes the next checkpoint — the user reads it, decides if another round is needed, and either iterates or merges.

### Step 6 — Merge to main

When the user says "merge" or "ready to merge" or "looks good, merge it":

```bash
# Merge the branch into main via the API
curl -s -X POST -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$REPO/merges" \
  -d "{\"base\":\"main\",\"head\":\"BRANCH_NAME\",\"commit_message\":\"Merge BRANCH_NAME: brief summary of what changed\"}"
```

Claude reports the merge SHA and confirms `main` is updated. The branch can stay as a record of the edit round (the user may want to look at it later) or be deleted. **Default: keep the branch** unless the user explicitly says to delete it.

---

## Conventions for Claude

1. **Branch creation is at Claude's initiative when the trigger conditions are met.** The user does not need to ask. Claude proposes: "I'm setting up a branch `<name>` for this round of edits." If the user wants to skip the branch, they say so.

2. **Never push edits to `main` while a branch is open for that document.** Pushing to both creates conflicts. The branch is the authoritative version while it's open.

3. **Always regenerate the dependent files in the same edit round.** Don't leave the markdown updated and the docx stale — that confuses the user and downstream readers.

4. **Inline notes get stripped from the output, not preserved.** The final markdown that lives in main is clean text. The user's notes are processing instructions, not document content.

5. **If the user's note is ambiguous, ask before applying.** Don't guess on substantive changes. For typo-level fixes, just apply.

6. **For the user's direct edits, light fixes are silent and heavy issues are surfaced.** Mechanical things (typos, accents, punctuation, citation formatting) get fixed without comment. Anything that crosses into terminology, consistency, or voice is *never* auto-fixed — it goes in the heavy-issues section of the report-back so the user can decide. The principle: if the user wanted Claude to make the call on a heavy issue, they would have left a comment.

7. **At end of round, surface every interpretation Claude made.** If the user wrote "tighten this paragraph" and Claude rewrote it three different ways, Claude says so and shows the result.

8. **Branches accumulate per project.** If the user opens a second round of edits, create a new branch (e.g. `oecd-paper-edits-0502`) — do not reuse the previous branch. Each branch represents one closed edit round.

---

## What this workflow doesn't cover

- **General-purpose branch use.** This protocol is specifically for the document-review case. If the user wants a branch for any other reason, they will say so and use plain git, not this skill.
- **Code review.** Code collaboration uses standard PR-based git flow but isn't formalized here.
- **Multi-author editing.** If a coworker is also editing the document at the same time, this protocol breaks. Tell the user immediately if that happens.
- **Permissions.** This protocol assumes the user's PAT has write access to the repo. If Claude can't push to the branch, the PAT doesn't have the right permissions.
