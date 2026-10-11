---
name: design-deck-reconciliation
description: "Placing and reconciling a slide deck authored in a design tool outside the repo (Claude Design and the like) against the repo's own version of the same content. Covers: intake from staging and immediate placement under the `_DESIGN` name, layout-aware extraction of the deck's markdown mirror, the slide-level map to the source (splits, design-only slides, reordered blocks, drift), sorting divergences from defects internal to the deck, and routing the rulings into the product ledger. Does NOT cover: building a deck from the repo (an institutional slides skill of your own for the PowerPoint or Beamer variant, `academic_slides_skill.md` for conference talks); the ledger file convention itself (`product_ledger_skill.md`, which this skill routes to); or authoring the figures a deck uses (`visuals_workflow_skill.md`)."
triggers: >-
  A deck made in a design tool lands in staging or covers content the repo already holds; "map
  this design deck to the markdown." Not for building a deck from repo content
---

# Design Deck Reconciliation

A deck built in a design tool is authored outside the repo. It shares content with something the repo already holds — an outline, a slide markdown, often a deck the repo built itself — but it has no builder, nothing regenerates it, and nothing propagates between it and its source. This skill places such a deck and establishes, in writing, how it relates to what the repo already has.

It is a **consumer of `product_ledger_skill.md`**. That skill owns the ledger file and the rulings; this one owns the intake, the extraction, and the format-specific comparison that produces the divergences the ledger records.

## When to use this skill

Read this skill when:

- The user drops a `.pptx` in staging saying they made it in Claude Design or a similar tool.
- A deck arrives that covers content the repo already holds in another form.
- The user asks for a map between a design-tool deck and the repo's markdown.
- A previously placed design deck comes back changed.

Do not use this skill for:

- **Building a deck from repo content.** That is the slide-production skills; this skill never authors slides.
- **A deck that is a build output.** If a script produced it, it cannot diverge from its source by construction.
- **The ledger's own structure.** Route to `product_ledger_skill.md` rather than restating it.
- **A deck with no repo counterpart.** Place it, note its external origin in the ledger, and stop. There is nothing to reconcile until a sibling exists.

---

## Claude Design keeps the markdown text

**The rule.** When a deck built from repo markdown goes into Claude
Design, the tool is told to **keep the text written in the `.md` exactly as it is** and to
iterate from that text. It is never left free to rewrite the prose. Design work is layout,
hierarchy and visual treatment; the words are already decided.

**Why.** A design tool left free to rewrite regenerates the prose. The repo's markdown carries prose that has been
through review rounds and voice work; a design tool regenerating it discards that and
reintroduces wording nobody approved.

**If text genuinely has to change to fit a slide,** that is a change to raise with the user, not
one to absorb silently.

**Where the kept text comes from.** The deck markdown is itself a compression of the parts
(`product_ledger_skill.md`, "The derivation chain"): feedback on the deck routes to the parts
first, and the deck markdown is rebuilt from the revised source before the design deck is
touched again.

## Prerequisites

- `product_ledger_skill.md` — read it before step 6.
- `python-pptx` for extraction.
- The paired asset `skills/extract_design_deck_mirror.py`. It ships with this skill (the `workstream_plan` + `BLIND_SESSION` precedent) and is parameterized — deck path, output path, and visuals folder are arguments — so it runs against any deck from where it lives.

---

## Workflow

### 1. Identify before placing

Establish five things:

- Which **product** this deck is a representation of, and its stem.
- Whether a **source** exists in the repo (a slide markdown, an outline) and at what version.
- Whether a **sibling deck** exists — one the repo built itself.
- Whether this is a **first arrival** or a re-drop of a deck already placed. A re-drop is a `changed-outside` event on an existing ledger row, not a new representation.
- **Ask the user whether they edited the deck's text in the tool after the build, and what they approved when the tool asked during the build** (the build instruction tells the tool to ask before deciding alone, `writing_drafting_skill.md`, the slide file). Every time, before reading a single text difference; never inferred. Their answer sets what a difference is: their edit is the newest version of the text; a change they approved in the tool is their ruling, recorded as such and not raised again; a change they neither made nor approved is the tool's. Read without asking, every difference looks like the tool.

### 2. Place immediately

Placement does not wait on the analysis. Staging is a hold, not a home.

- **Name:** the product stem plus the `_DESIGN` marker — `<stem>_DESIGN.pptx`. The ALL_CAPS marker is one of the floor's content-file markers (`naming_conventions.md`, "Content-file markers", the closed list), an `ALL_CAPS` token on a lowercase stem.
- **Home:** beside the source markdown, not in a subfolder of its own.
- **Correct obvious filename defects** on the way in — tool-generated dates are often wrong — and say what was corrected.
- **Empty staging** and update the folder map in the same commit.

Placement, mirror, and folder-map update ship as **one atomic commit** per `github_api_workflow_skill.md`.

### 3. Extract the mirror

Run `extract_design_deck_mirror.py <deck.pptx>`. It writes `<stem>_text.md` beside the deck.

The extraction is layout-aware because design-tool decks defeat the naive approach in ways that are invisible until read closely:

- **No title placeholder is set**, so the title is the largest type in the header band, not `shapes.title`.
- **Eyebrows** (small-caps section labels) sit wholly above the title and are captured separately; any other text, however high on the slide, is body, so a split list's first row is not taken for header text.
- **Nav rails** — persistent section indexes running across a chapter — must be dropped **by geometry, not by frequency**. Frequency also catches genuine callout numerals, and a frequency filter silently removes the "4" from "4 design options."
- **Callouts** are a big number and a caption in separate shapes; they are joined vertically (`**87%** — of respondents…`) or horizontally for label/value rows.
- **Chrome pictures** — repeating on four or more slides, or covering the slide — are template decoration, not content.
- **Speaker notes** are captured. In a design-tool deck they often carry content that exists nowhere else.
- **Highlights**: a highlighted run in the deck (the user's usual way of marking a decision in the tool) is carried as `==text==`, one pair of markers per highlighted phrase. The markers belong to the mirror, not the slide: read them as the user's marks at step 1's attribution, and route them at step 5 like their other edits in the tool.

**The mirror is never hand-edited.** It is reproducible from the deck, which is the one property it would otherwise lack, since the deck itself is not reproducible from anything. Re-run the script after any change.

**Sanity-check the extraction before trusting it.** Read the title list end to end. Repeated titles across a run of slides are the signature of chrome being read as content.

### 4. Build the map

`<stem>_DESIGN_MAP.md`, beside the deck. Slide-level correspondence between the source and the design deck.

Align by **content**, not by slide number. The numbers stop corresponding the moment the design deck inserts a divider. A workable method: token-overlap scoring of each design slide against each source slide to propose the alignment, then read both to confirm. Report the method and its limits — the correspondence is mechanical and reliable, the drift readings are judgment.

The map records four things numbers alone hide:

- **Splits** — one source slide becoming two.
- **Design-only slides** — dividers, roadmaps, framing slides with no source counterpart.
- **Reordered blocks** — content lifted out of its source sequence, which is usually a structural argument the source does not make. Say what the argument is.
- **Drift**, in both directions — content the design deck asserts that the source does not, and **cuts**, source content the deck no longer carries (a dropped closing sentence, a shortened block, a removed lead-in, a note promoted to the slide). Cuts are found only by a **line-by-line pass over each source slide against its mapped design slide**; a read of the design slide finds additions and misses cuts.

**Check the arithmetic.** Source slides mapped, plus design-only slides, plus splits, must equal the design deck's slide count. It is a cheap check that catches a missed slide.

### 5. Sort the findings into two bins

Before asking the user anything:

- **Divergence from the source** — a question for the user, carrying step 1's attribution (their edit, or the tool's; a change they approved in the tool is already ruled and is recorded, not asked). Which way it goes, the source following the deck or the deck reverting, is the user's ruling at the ledger, never the intake's.
- **Defect internal to the deck** — a slide contradicting its own speaker notes, a total not matching its rows. This has no counterpart in the source, no authority ruling resolves it, and presenting it as a divergence is a category error. Report it separately, and flag it as urgent if the deck is about to be presented.

### 6. Route the rulings to the ledger

Read `product_ledger_skill.md`. The divergences become ledger entries, `open` by default; the deck becomes a representation row with the source markdown as its **named parent**, at the source's version. Do not adjudicate at intake — that is the ledger's discipline and it is deliberate.

If no ledger exists for the product, render the representation sketch and stop for the user's reaction before writing it.

Where the deck is a translation, the user's text edits in the tool (step 1's attribution) are also correction pairs: hand them to `translation_review_skill.md`'s close-out, "the design-tool round".

### 7. Guard the source

If the source markdown is live input to a build script, and any divergence is ruled or presumed in the deck's favor, put a warning at the head of the source naming the open items and stating that the builder will reissue superseded content. Without it, a future rebuild silently reintroduces what the deck superseded.

---

## Key rules

- **Place first, analyze second.** Staging empties in the placement commit.
- **Never hand-edit the mirror.** Re-run the script.
- **Read the extracted title list before trusting the mirror.** Repeated titles mean chrome was read as content.
- **Align on content, never on slide number.**
- **Ask who edited, and what was approved in the tool, before reading a difference; the direction of every divergence is the user's ruling.**
- **A defect inside the deck is not a divergence.**
- **Do not adjudicate at intake.** Log open; the user rules on their next pass.
- **The two decks do not synchronize.** The repo-built variant regenerates from its source; the design deck regenerates from nothing. A content change in one does not propagate. The map and the ledger are the only places the correspondence is written down — say so wherever either is referenced.

---

## Edge cases

**A re-drop of an already-placed deck.** Not a new representation. Log `changed-outside` against the existing row, re-run the extraction, rebuild the map, and check whether any open divergence has been silently resolved by the new version — a resolved divergence still needs its ledger entry closed, or the ledger describes a conflict that no longer exists.

**The design deck has been presented.** Its content has been asserted whatever the repo says. Mark the representation `presented` in the ledger with the audience and date, and treat internal defects in it as urgent rather than deferrable if a further presentation is coming.

**Feedback arrives on the design deck.** Expected — it is the artifact the audience was holding, and it is the one with no builder. The ledger's `feedback` event carries a routing decision naming which representation absorbs the change. Do not let comments live only in the deck.

**Pictures shared with the repo.** Some pictures in the deck may be byte-identical to visuals in the repo. `--visuals DIR` names them in the mirror, which makes it visible which figures are shared and which are design-variant artwork with no repo source.

**The deck's speaker notes contradict its slides.** A defect, not a divergence — but whether it matters depends on who presents. If the user presents their own deck, its notes are their line or two a slide (`writing_drafting_skill.md`, the presenter question), and they may close the contradiction no-change. Record the reasoning and the reopening condition (a deck built for someone else to deliver), or the next session will "fix" it as an oversight.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
