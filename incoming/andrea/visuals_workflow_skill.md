---
name: visuals-workflow
description: "Use this skill when authoring or revising visuals (figures, diagrams, charts) for a markdown deliverable that will ship to Word, PDF, or LaTeX. Covers the three-stage workflow: (1) in the markdown draft, each visual is specified by a sketch (ASCII rough shape for shape-driven visuals like funnels, hierarchies, logic maps with arrows, decision trees, flow diagrams; text-only layout box for stat cards, simple bar charts, comparison panels) plus a prose description; (2) sketches are reviewed on the branch alongside the markdown text; (3) after markdown is approved and merged, SVGs are iterated per visual, with previews shown in chat before committing. Does NOT cover the final embed step (SVG → PNG → Word/LaTeX/PDF) — that is handled by the format skill that drives the final build (a Word or LaTeX format skill of your own, `academic_paper_latex_skill.md`, etc.). Does NOT cover slide-deck visuals where the visual is the slide itself — those are handled by the slides skills."
triggers: >-
  "let's add visuals," "make a sketch for this," "we need a diagram here," "let's see the
  SVG"; a markdown deliverable that needs visuals beyond tables
---

# Visuals workflow

A skill for authoring visuals (figures, diagrams, charts) that ship inside markdown deliverables. The workflow separates *what the visual communicates* (decided early, in markdown) from *what the visual looks like* (iterated late, in SVG). This matters because the two phases have different costs of revision — changing a sketch in markdown is one paragraph edit; redoing an SVG is a render cycle. Decoupling them keeps cheap decisions cheap and expensive ones rare.

## When to use this skill

Read this skill when:

- The user says "let's add visuals," "make a sketch for this," "we need a diagram here," "show me the sketch first," "let's see the SVG," or "render it in chat first."
- The user says "let's make a graph," "make a figure," or "add a chart" — common words that overlap with skill vocabulary. **Pause and ask whether the user wants a sketch (i.e., whether this skill applies)** before proceeding. If the answer is no (e.g., a quick inline markdown table is fine), do not use this skill.
- A markdown deliverable that will ship to Word, PDF, or LaTeX needs visuals that aren't markdown-native tables.

Do not use this skill for:

- **Markdown-native tables.** Tables that render natively in markdown and would render acceptably in the final format don't need a sketch + SVG cycle. Just write the table.
- **Slide-deck visuals where the visual is the slide.** Those are handled by `academic_slides_skill.md` and any other slides skill the project keeps. This skill is for visuals embedded inside narrative markdown, not for whole-slide compositions.
- **The final embed step** — turning the SVG into a PNG (or other format) and embedding it in the Word/LaTeX/PDF build. The relevant format skill (the project's Word formatting skill, `academic_paper_latex_skill.md`, etc.) owns that step. This skill ends when the SVG is approved and committed.
- **Color-palette decisions.** The project's own color reference, if it has one — otherwise the color block in the relevant preamble — is the source of truth. This skill consumes the palette; it doesn't define it.

---

## Prerequisites

- A markdown deliverable in progress (typically on a branch per `writing_branch_skill.md`).
- A `workspace/visuals/` folder in the repo. In archetype repos it is **scaffolded up front as a labeled-empty home** (an empty `visuals/` means "no visuals made yet"); SVGs are born here on use. Present wherever this skill is active; if missing, create it with its standing document.
- For SVG generation: standard text-based SVG construction — no external rendering dependencies required beyond what's available in this environment.

---

## The three-stage workflow

### Stage 1 — In the markdown draft: sketch + description

Each visual is specified in the draft markdown with two blocks: a **sketch** (rough visual shape) and a **description** (prose specification). The pair is enough for the user to react to the visual choice without yet seeing the rendered SVG.

#### Sketch formats

There are two sketch formats, chosen by the nature of the visual:

**Shape sketch** — used for visuals whose meaning is carried by geometry. Funnels, hierarchies, **logic maps with arrows**, decision trees, flow diagrams. The sketch uses ASCII shapes inside a fenced code block, approximating the shape the SVG will take.

Example (funnel):
```
████████████████████████  400,000  Registered members
    ████████████          60,000   Borrowed this year
         ██                5,000   Used the e-book service
          █                1,200   >75% e-book loans
```

Example (logic map with arrows):
```
   [Premise A] ──┐
                 ├──→ [Conclusion]
   [Premise B] ──┘
```

**Layout sketch** — used for visuals whose meaning is carried by labels and numbers rather than geometry. Stat cards, simple bar charts, comparison panels. The sketch is a text-only layout box showing the structure.

Example (stat cards):
```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│     60%      │  │     45%      │  │     30%      │
│ no staff on  │  │  no reading  │  │  no evening  │
│     site     │  │     room     │  │    hours     │
└──────────────┘  └──────────────┘  └──────────────┘
```

Example (bar chart):
```
Branch A               ██░░░░░░░░░░░░░░  $14
Branch B               ████░░░░░░░░░░░░  $39
Network average        ████████████████  $95
                                          avg spend per member
```

Bar lengths in the sketch should approximate proportionality so the visual point is visible at sketch stage. Don't worry about precise pixels.

#### Description block

Below the sketch, a prose block specifying:

- **What the visual shows.** The substantive content — the numbers, the labels, the comparisons.
- **What it communicates.** The single point the reader should walk away with after seeing it.
- **Design choices that matter.** Orientation (horizontal vs. vertical bar chart), color emphasis (which bar should visually dominate, which color group is which), annotations (axis labels, value labels, percentages), and any constraint that affects production (must fit in one page-width column, must be colorblind-safe, etc.).

The description is not a specification of every pixel — it's the minimum spec needed for Stage 3 (SVG generation) to begin without asking clarifying questions.

#### Naming visuals in markdown

Each visual gets a short identifier used in section numbering and SVG filenames. Format: `<short_id>` is a short kebab- or snake-case slug describing the visual's content, not its position. Examples: `funnel`, `service_gap`, `branch_size`, `spend_per_member`.

The deliverable-relative reference is `Visual 3.1`, `Visual 3.2`, etc., but the SVG filename uses the semantic slug (see Stage 3).

#### Convention block in markdown

The sketch + description block is bracketed with a comment so it's clearly a visual spec, not body text:

```markdown
**Visual 3.1 — The funnel.**

*Sketch:*
```
████████████████████████  400,000
    ████████████          60,000
         ██                5,000
          █                1,200
```

*Description:* vertical funnel, four levels narrowing downward. Each level
labeled with absolute count on the right. Single color with decreasing opacity.
The visual point is the dramatic narrowing.

*Narrative (~80 words):* [the paragraph that sits next to this visual in the
finished document]
```

The narrative paragraph that sits next to the visual is co-located with the spec so the writer can see them together while drafting.

### Stage 2 — Markdown review (on the branch)

When the draft markdown is on the branch for review per `writing_branch_skill.md`, the sketches and descriptions are reviewed alongside the text. The user reacts to visual choices the same way they react to text — bracketed comments, direct edits to the sketch or description, or chat discussion.

Common edits at this stage:

- Change the visual format (e.g., "this should be stat cards, not a bar chart").
- Change what the visual shows (rows, labels, comparisons).
- Drop a visual entirely.
- Add a visual.
- Change the description (orientation, color, what the takeaway should be).

**No SVGs exist yet at this stage.** Editing a sketch is a one-paragraph change; editing an SVG that doesn't exist is impossible. This is the cheap-revision phase by design.

When markdown is approved and merged to main per `writing_branch_skill.md` Step 6, the visual specs are locked. Move to Stage 3.

### Stage 3 — SVG iteration (per visual, on main)

After markdown is merged, generate SVGs one at a time. The protocol:

1. **For each visual, in document order:**
   a. Read the sketch + description from the merged markdown.
   b. Generate an SVG draft.
   c. **Show the SVG as a preview in chat first** using the visualize tool — do not commit yet.
   d. Wait for the user's reaction. Iterate on the SVG (color, layout, labels, proportions, type weights) until they approve.
   e. Once approved, save the SVG to `workspace/visuals/<deliverable_stem>_<short_id>.svg` and commit to main, with its row in the repo's assets index (an archetype repo; found via the root map's root-documents block) in the header row that index carries (`typed_index_template.md`: `Asset · About · Where · Used in` — the file's stem, what the visual shows in Claude's words with a subject already named in a row keeping its words, the path, and the deliverable it is embedded in once the format skill embeds it), and its row in the visuals catalog (`standing_documents_template.md`, the reuse shelf).

2. **Repeat for every visual.** Do not batch — each SVG is iterated to approval before moving to the next. Batching means the user reviews five visuals at once with no way to react incrementally; serial iteration is faster overall.

3. **When all SVGs are committed**, delete the sketch and the description from the deliverable, then hand off to the format skill driving the final build (Word, LaTeX, PDF).

   **The sketch and the description are scaffolding, not content.** They exist so the user can react to what a visual communicates before anyone spends a render cycle on it; they are addressed to them, not to the reader of the finished document. Once the SVG exists it carries what they were describing, and leaving them in means the deliverable explains its own figures to an audience that can simply look at them. The same goes for any prose recording *why* a visual was designed the way it was — the color rule, the choice of treatment, the argument for one projection over another. That reasoning belongs in the skill, the palette or the commit message, and a reader of the deliverable does not need it.

   **The exception is a slide file for a deck built in a design tool** (Claude Design and the like): no SVG replaces the block, the tool draws the visual from the description, so the block stays in the slide file at its slide, under the head `**Visual N — <stem>.**`, for good (`writing_drafting_skill.md` step 1, "The slide file").

#### SVG file location and naming

- **Folder:** `workspace/visuals/` (single project-wide folder).
- **Filename:** `<deliverable_stem>_<short_id>.svg`, where:
  - `<deliverable_stem>` is the markdown file's basename without `.md` and without `_OUTLINE` or similar suffixes.
  - `<short_id>` is the semantic slug from Stage 1.

Examples:
- `annual_report_library_network_funnel.svg`
- `annual_report_library_network_service_gap.svg`
- `annual_report_library_network_spend_per_member.svg`

This convention ensures (a) all visuals for a deliverable are visible together when the folder is sorted alphabetically, and (b) the binding between SVG and source markdown is obvious from the filename.

#### Color and style

If the project has its own color reference — a palette file, or the color block in the preamble it builds with — use it. Otherwise, default to a neutral two- or three-color palette with one accent color reserved for the visual's punchline (the bar that dominates, the highlighted dot, the funnel's bottom level).

Visuals shipping to a Word or PDF document should use solid colors that print acceptably in grayscale. Visuals shipping to slides may use more saturation.

---

## Key rules

- **No SVG generation before markdown is merged.** If the sketch changes after an SVG is rendered, the SVG is wasted. The cheap-revision phase is the sketch phase; respect the ordering.
- **One SVG at a time in Stage 3.** Serial iteration with chat previews. No batched delivery of multiple SVGs without intermediate approval.
- **The SVG preview is shown in chat first, then committed.** Never commit an SVG to main that the user hasn't seen rendered. The chat preview is the approval gate.
- **The skill ends at SVG approval.** The format conversion and embedding step belongs to the format skill (Word, LaTeX, PDF), not this one. This skill commits the SVG and stops.
- **Common-word triggers require a confirmation question.** When the user says "let's make a graph" or "make a figure" or "add a chart," ask whether they want a sketch before proceeding. These phrases overlap with skill vocabulary; assuming the skill applies is a frequent error.
- **The sketch must be enough for review.** If the sketch is so abstract that the user can't tell what the visual will look like, it's a bad sketch. Add labels, numbers, and rough proportions until the visual choice is reviewable from the sketch alone.
- **Visuals get semantic names, not positional ones.** `funnel`, not `figure_3_1`. Positional names break when sections move; semantic names survive restructuring.

---

## Edge cases

### A visual that's already a markdown table

If a visual would work as a markdown table that renders acceptably in the final format, skip this skill entirely. Use a markdown table inline in the draft. This skill is for visuals where markdown can't carry the format — funnels, stat cards, bar charts with visual emphasis, diagrams.

### A visual that turns out to need redesign during Stage 3

If, while generating the SVG in Stage 3, the sketch turns out to be wrong (the chart doesn't communicate well, the funnel has the wrong proportions), do not silently redesign in the SVG. Pause, name the issue, and propose either (a) revising the sketch in main and starting Stage 3 again for that visual, or (b) updating the visual spec to match what the SVG should show. The decision is the user's, not the SVG generator's.

### A visual reused across deliverables

If the same SVG genuinely serves multiple deliverables (same numbers, same design), keep one copy in `workspace/visuals/` and let both deliverables reference it. The filename should still use a semantic slug; if the original deliverable is gone, the slug should still make sense. If the deliverable stem doesn't naturally apply (because the visual is reused), use a project-level stem like `<project>_<short_id>.svg`.

### A visual that needs to be a true image (not SVG)

If the visual is a photograph, a screenshot, or a complex rendered image that can't be authored as SVG, this skill doesn't apply. Use the format skill's image-handling guidance directly. The sketch + description workflow is for vector visuals that we author.

### A non-communicative asset (an equation, a logo, a rendered formula)

An asset that carries no message of its own — an equation rendered as an image, a logo, a formula block, a rendered table of symbols — is not a visual in this skill's sense: there is no visual choice for the user to react to, so the three-stage loop does not run. It is produced once, reviewed once for correctness (the symbols, the numbering, the rendering against the source), and filed in `workspace/visuals/` under the same naming, its catalog row's Stage reading `exempt — correctness review YYYY-MM-DD`. A caption, a highlight or a label that argues something makes it a visual again, and the loop runs.

---

## Worked example

A report to a city council on a library network used this skill. The outline specified six visuals for Section 3: a funnel, three sets of stat cards, two bar charts, and an optional synthesis visual. Each was sketched in the outline before the report was drafted. During the markdown review round, the user pushed back on the bar-chart orientation (asking for horizontal not vertical) and dropped the synthesis visual; both edits cost one paragraph each. After the markdown merged, the six SVGs were generated one at a time, with the funnel taking three iterations and the others taking one each. Total elapsed time was a fraction of what it would have been if SVGs had been generated alongside an unstable markdown.

The visuals folder ended with:

```
workspace/visuals/
  annual_report_library_network_funnel.svg
  annual_report_library_network_service_gap.svg
  annual_report_library_network_footprint.svg
  annual_report_library_network_branch_size.svg
  annual_report_library_network_spend_per_member.svg
```

The Word build, handled by the project's Word formatting skill, converted each SVG to PNG and embedded them at the marked positions in the markdown.

---

## Setting up for a new project

The first time this skill runs in a project:

1. Confirm `workspace/visuals/` exists. Present wherever this skill is active; if missing, create it with its standing document.
2. Confirm whether the project has a palette reference. If yes, point Stage 3 at it.
3. Update the project's `CLAUDE.md` skills table to list this skill if it's been activated for the project.

No further configuration is required.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
