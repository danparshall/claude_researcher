---
name: iterative-writing-workflow
description: "A two-protocol workflow for knowledge work with Claude: one protocol for reading, thinking, and note-taking (fully interactive, step-by-step), and another for drafting written content (outline interactively, draft in one pass, revise in chunks). Use this skill whenever the user is working on a writing project that involves both research/reading and producing written deliverables — white papers, policy notes, reports, academic papers, book chapters, or any substantial document. Also use when the user asks to set up a writing workflow, wants to organize how they collaborate with Claude on a document, or says things like 'let's start writing,' 'how should we work on this,' or 'set up the project.' This skill is especially useful for projects where the user is both the thinker and the writer — where reading feeds into writing."
aitaxbid_source: ~/code/AITaxBID/skills/writing_skill.md@e0a736d (2026-05-02)
---

# Iterative Writing Workflow

A two-protocol system for collaborating with Claude on knowledge-intensive writing projects. Designed for projects where reading, thinking, and writing are interleaved — the user processes source material, develops ideas, and produces written deliverables over multiple sessions.

## When to use this skill

Use this whenever a project involves:

- Reading and processing source material (papers, reports, data)
- Taking notes and developing ideas interactively
- Producing written deliverables (reports, chapters, policy notes, papers)

The skill defines two distinct protocols — one for thinking work and one for writing work — because they have fundamentally different dynamics. Thinking work benefits from tight interactivity. Writing work benefits from Claude drafting in larger passes.

---

## Protocol 1: Reading, Thinking, and Note-Taking

**When to use:** The user is processing source material, taking notes, reacting to content, building understanding, or developing ideas that will later feed into writing.

**Core principle:** Fully interactive, user-driven pace. Claude does not move ahead without explicit go-ahead.

### Workflow

1. **Present the material** — Claude presents a summary or the source material for the user to review. When possible, present it as a rendered file in the side panel rather than dumping text inline in chat. No need to show full text unless the user asks.
2. **User reacts** — The user provides notes, reactions, questions, status labels, key takeaways. Claude answers questions, looks up details when asked, and engages with the user's thinking (see "Answering questions" below).
3. **Update notes** — Claude updates the relevant notes/tracking documents with the user's input. Show the proposed update to the user before committing (see "Show before committing" below).
4. **Do not move on** — Wait for the user to explicitly indicate they're done with the current item before presenting the next one. Do not ask "ready for the next one?" — let the user drive.

### Answering questions

When the user asks a question about the material — methodology, a specific detail, a cross-reference, institutional context — look it up and respond. This is part of the thinking process, not a distraction from it.

**Flesh out answers fully.** Give complete, step-by-step explanations — not compressed summaries. These explanations are valuable reference material later. Write as if the reader is coming back to this months from now and needs to understand the logic without re-reading the source. A good explanation given in chat today may become a note the user keeps for the duration of the project.

### Questions vs. instructions

The user's messages during note-taking can be questions ("what does this mean?"), instructions ("add that to the notes"), or ambiguous. The rule:

- **If a message could be a question rather than an instruction, answer the question first and wait.** Do not update notes or tracking documents until the user explicitly says to add or push.
- **When the user says "add that" or "add this to the notes"** after a fleshed-out explanation, add the **full explanation** to the notes — not a compressed version. The fleshed-out version is more useful for future reference. If the user wants a shorter version, they will say so.

### Sorting inputs

The user may label their inputs with different destinations. Common patterns:

- "for notes" / "add to notes" → the relevant notes file
- "for to-do" / "add to my list" → the to-do or tracker file
- A question or "clarify this" → answer in chat first, wait for go-ahead before adding anywhere

**Notes and to-dos are separate.** Never mix them. Notes capture understanding (what a document says, what it means, how it connects to other material). To-dos capture actions (things to follow up on, decisions to make, tasks to complete). Each goes in its own file or section.

### Pushing changes and saving

- Work interactively: user gives content, Claude drafts the note or update, user approves.
- **Always check with the user before committing changes** to notes, tracking documents, or the repo.
- **If moving to a new topic and there are uncommitted changes,** flag it: "We haven't saved yet — here's what I'd add to [file]. OK to save/push?" Wait for confirmation.

### Summary maintenance

When taking notes on a document, also review and improve the document's summary file if one exists — especially:
- Spelling out acronyms on first use so the summary is self-contained
- Adding relevance annotations for the project
- Fleshing out sections that are too compressed to be useful as standalone reference

Summary updates are saved alongside note updates.

### Session resumption

Multi-session projects need a way to pick up where the user left off. The protocol:

1. **Check the progress tracker** (if the project maintains one) for current status — which document is in progress, what's been covered, what's next.
2. **Do NOT search past chats or conversations.** The tracker is the single source of truth for where we left off. Past chats may be incomplete, out of order, or from a different context.
3. **Read the existing notes** to understand the current state of accumulated knowledge.
4. **Tell the user where we are and what's next,** then wait for their go-ahead.

If the project doesn't have a progress tracker, ask the user where they'd like to pick up.

### Key rules (summary)

- **Do not skip ahead.** The user may need multiple rounds of discussion on one item.
- **Answer questions inline and fully.** Look things up and respond with complete explanations — they become reference material.
- **Questions first, actions second.** If it might be a question, answer before updating anything.
- **Full version, not compressed.** When adding explanations to notes, keep the full version.
- **Track cross-references.** When a concept in one source connects to another, note it. These connections are valuable.
- **Show before committing.** Before updating any notes or tracking documents, show the user the proposed update and wait for approval.
- **Flag uncommitted work** before changing topics.
- **Depth varies.** Some items get a brief note, others get extensive treatment. Follow the user's lead.

### Adapting to your project

This protocol is generic. To use it in a project, define the following in your project's `RESEARCHER.md`, `STATUS.md`, or equivalent coordination file:

- What source material looks like (papers, reports, interview transcripts, data files)
- What notes documents you maintain (a master notes file, a tracking table, cross-reference docs) and where they live
- What to-do or tracker documents you maintain, separate from notes
- What status labels the user uses (e.g., "must-read," "flagged," "done")
- What order items are processed in (index order, user's choice, priority-based)
- Whether the project has a progress tracker for session resumption, and where it lives
- The lookup order for answering questions (which files to check first, which are last resort)

---

## Protocol 2: Drafting Written Content

**When to use:** The user wants to produce a written deliverable — a chapter, section, policy note, report, or any substantial document.

**Core principle:** Plan interactively, draft in one pass, revise in chunks. This yields better prose than drafting section-by-section with approval gates, because Claude can manage flow, avoid repetition, and keep arguments coherent across the full drafting unit.

### Workflow

1. **Overall outline** — Claude proposes a structure for the full document or chapter. The user and Claude work on it interactively until the user is satisfied. Save the approved outline.
2. **Detailed outline of the next subsection** — Before drafting, build a detailed outline for the specific subsection to be written: key arguments, evidence to cite, sources to reference, internal structure, and approximate length. This is interactive — Claude proposes, the user shapes.
3. **Agree on length** — Based on the detailed outline, agree on a target length for the subsection (e.g., "about 2 pages," "800 words," "keep it tight"). This happens during step 2.
4. **Claude drafts the full subsection** — One pass, no mid-draft checkpoints. Claude writes the complete subsection based on the approved detailed outline.
5. **Review and revise in chunks** — The user reviews the draft and flags what works and what doesn't. Revisions happen by chunks (a paragraph, a transition, an argument that needs restructuring) — not line-by-line, not full rewrites.
6. **Check the overall outline** — After finishing a subsection, step back: does the overall outline still hold? Has writing this subsection revealed that something downstream needs to change? Update the outline if needed and save.
7. **Repeat** from step 2 for the next subsection.

### Key rules

- **The drafting unit is the subsection** (e.g., "1.2 The productivity channel"), not a full chapter. Subsections are large enough to have a coherent argument, small enough to review without fatigue.
- **The planning steps (1–3) are still interactive.** Do not skip the outline or jump to drafting. The outline work is where the user thinks through the project — it's not overhead, it's the point.
- **The drafting step (4) is NOT interactive.** Claude produces the full subsection in one pass. This yields better prose (coherent flow, no repetition, consistent argument).
- **Outlines are living documents.** They get updated as writing reveals new structural needs (step 6). Always save updated outlines.

### Why this works

The insight behind this protocol: Claude produces better writing in larger passes, but the user produces better thinking in tighter loops. The protocol separates these two activities — tight loops for planning, larger passes for prose — so each party does what they're best at.

The overall outline → detailed outline → draft → revise cycle also helps the user think through the project incrementally. Each detailed outline forces a decision about what a subsection will argue and what evidence supports it. This surfaces structural problems early, before prose is written, when they're cheap to fix.

---

## How the two protocols interact

In a typical project, the user alternates between protocols:

1. **Protocol 1** — Process source material, take notes, develop ideas
2. **Protocol 2, step 1** — Use the accumulated understanding to build an overall outline
3. **Protocol 1** — Continue processing material (may reveal new angles)
4. **Protocol 2, steps 2–7** — Draft subsections, revising the outline as needed
5. **Protocol 1** — Go back to sources to check a claim, fill a gap, or process new material
6. **Protocol 2** — Continue drafting

The protocols are not sequential phases — they interleave throughout the project. The user will signal which mode they're in. When in doubt, ask.

---

## Setting up for a new project

When adopting this skill for a new project, document the following in your project's `RESEARCHER.md`, `STATUS.md`, or equivalent coordination file:

- **Source material format** — What are the inputs? (PDFs, reports, data, transcripts)
- **Notes structure** — What tracking documents do you maintain? Where do they live?
- **To-do / tracker structure** — Separate from notes. Where do action items go?
- **Progress tracker** — For session resumption: where is the file that records what's been covered and what's next?
- **Deliverable format** — What's the output? (Word doc, LaTeX, markdown, slides)
- **Style profiles** — Do you have writing style guides? When should they be applied? If you don't have a style-profiles doc, you can create one — ask the agent to draft a versioned `<project>_Style_Profile.md` from a sample of your prior writing.
- **Version control** — How are outlines and drafts saved? (Git, file system, cloud storage)
- **Subsection sizing** — What's a typical subsection length in your project? (This calibrates step 3 of Protocol 2)
- **Lookup order** — When answering questions about source material, what files should Claude check first? (e.g., index → summaries → full text → source files)
