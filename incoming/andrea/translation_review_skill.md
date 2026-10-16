---
name: translation-review
description: "Review pass for Spanish translations of deliverables — naturalness, not proofreading. The translations are accurate; the failure mode is Spanish that sounds translated. The user's ear is the reviewer of record; this skill externalizes their corrections so Claude's first-pass Spanish improves over time. Activation rides the Voice and style cluster — wherever the voice skills are active, this skill is too. Does NOT cover a language in which the user cannot judge naturalness (a review in such a language would be a different design with a different reviewer, not this skill stretched); does NOT relax the voice skills' structure and conciseness discipline (see the boundary section); does NOT modify the writing-branch flow (it rides it unchanged)."
triggers: >-
  Translating any deliverable to Spanish, and at the review round of a translated branch;
  the user's corrections go to the companion log
---

# Translation review — natural Spanish

**Status:** active.
**Owner:** the user.
**Applies to:** any deliverable translated into Spanish — papers, policy notes, slides content, briefs — and, since v2.3.0, any deliverable **written in Spanish from the start** (the section "Written in Spanish from the start", below). Both moments: the **first pass** (apply the distilled patterns below while translating or drafting) and the **review round** (capture the user's corrections so the patterns grow).
**Companion file:** `translation_corrections_log.md` — the append-only raw trail of correction pairs. The two files travel together as a pair (the format-cluster pattern: skill + companion).

---

## The failure mode and the purpose

Claude's Spanish translations are **correct but unnatural**: accurate in meaning, faithful to the English structure, and yet they read as translated — a native reader hears the English underneath. This is not a proofreading problem; there is usually nothing to *fix* in the grammar. It is a naturalness problem, and the instrument that detects it is **the user's ear**. Claude may self-flag candidates while translating ("this sentence reads translated to me"), but the authoritative correction is always theirs.

The purpose of this skill is to externalize that tacit instrument, pair by pair: every correction the user makes is captured as *unnatural → natural → why*, the recurring kinds get distilled into the patterns section below, and Claude applies the patterns on the next first pass. The payoff runs in one direction — **they correct less over time**, because the first-pass Spanish absorbs what their ear has already taught.

## The boundary against the project's voice profile

The project's voice profile, if it has one, will normally impose an anti-circularity discipline on translation: the English version's structure, conciseness, and forward-moving paragraph logic are preserved; the translation must not drift toward long setups, qualifiers, and circular paragraphs. **That discipline holds. This skill works below it.** Naturalness lives at the sentence's joints — punctuation habits, connectors, calques, register, word choice — not at the level of structure or argument. A sentence can be recast to sound like Spanish while the paragraph it sits in stays English-disciplined: claims early, paragraphs that land, no throat-clearing. Nothing in this skill, the patterns section, or the corrections log is ever a license to reintroduce the circular conventions that discipline pushes against. If a proposed pattern would loosen structure rather than naturalize a joint, it is out of scope by definition.

## Scope: Spanish only

This skill covers **Spanish**. A language in which the user cannot judge naturalness is excluded *with a reason*, not deferred: the design's premise is that the reviewer's ear is the instrument, and it works only where the user's ear is strong enough to adjudicate naturalness (their call). A review loop in such a language would need a different reviewer of record — a native-speaker colleague — and is therefore a different design, not this skill with the language swapped.

## The review protocol — rides the writing-branch flow

The mechanism is the existing `writing_branch_skill.md` flow, **reused, not modified**:

1. Claude translates the deliverable **on a branch** (Protocol per `writing_branch_skill.md` Step 1; the normal `<slug>-<purpose>-<date>` naming, purpose `review` or `edits`). While translating, Claude applies every pattern in the distilled-patterns section and may flag sentences it suspects still read translated.
2. The user reads the Spanish **in the branch and corrects in place** (writing-branch Mode 2 direct edits). Optional bracketed whys when time allows — `[suena a inglés — en español va con coma]` — but no annotation is required; the correction alone is enough.
3. **The diff is the pair-capture.** When they signal the round is done, the branch diff against the translation commit yields every unnatural → natural pair for free — their review effort stays exactly what it would have been without this skill.
4. Merge per the writing-branch flow, then run the close-out below.

**One seam with writing-branch Step 4, stated explicitly:** in a translation-review round, the user's direct corrections are **authoritative on naturalness** — Claude applies them and never "proofreads" them back toward its own phrasing. The heavy-proofread flag (terminology drift, internal inconsistency) applies only to genuine within-document conflicts — e.g. the same term corrected two different ways in one round — never to second-guessing their naturalness call.

## Capture beyond the branch — the in-chat round and the design-tool round

Two more places the user's corrections arrive, each captured into the same close-out.

**The in-chat round.** A translation that would not earn a branch is reviewed in chat: the repo declares `WORKFLOW_MODE: main_only`, or the piece is too short for an outline (a component paragraph, slide labels, a form's fields; the drafting skill's own test). Claude shows the Spanish with the distilled patterns applied and may flag a sentence it suspects still reads translated. The user's reply is the review round: each correction in it is an unnatural → natural pair, captured from the reply as the branch round captures it from the diff; an approval with no corrections logs nothing. The corrected text is committed on `main`.

**The design-tool round.** When a Spanish deck goes into Claude Design and the user edits its text there, their edits come back through the reconciliation map (`design_deck_reconciliation_skill.md` Step 4, the differences they attribute to themselves at Step 1): each text edit is a pair, the repo's Spanish as it went to the tool → their Spanish in the deck. The reconciliation's Step 6 hands them here beside the ledger rulings.

In both rounds the close-out four-step runs unchanged and the seam rule holds: their corrections are authoritative on naturalness and are never proofread back.

## The close-out four-step

After the merge (or at session close if the merge waits):

1. **Walk the diff.** Collect every correction as an unnatural → natural pair.
2. **Draft the whys.** For each pair, Claude drafts a one-line why naming the *kind* of problem (em-dash habit, calqued connector, register, word choice…). The user confirms the batch, fixing only the wrong ones — the annotation cost lands on Claude, not them.
3. **Append to the log.** Write the confirmed pairs to `translation_corrections_log.md` in the entry format defined there. Append-only; existing entries are never edited.
4. **Maturity check.** If a correction *kind* is recurring across the log, **propose** a patterns-section edit — prompt-don't-perform, approved like any skill change. On approval, edit this file's patterns section; if you keep a canonical skills repo, the change travels back to it, so every repo inherits it.

There is **no pre-built taxonomy.** The why names the kind in plain words; categories emerge from the log as kinds recur. (Punctuation, connectors, calques, and register are expected to emerge — they are not pre-written as sections.)

## Distilled patterns

*This section grows from the corrections log via the maturity check. It is the layer Claude applies on every first pass. Seeded with the two patterns the user has already named; everything else earns its way in through recurrence.*

- **Em-dashes (seed).** Em-dash interruptions are an English habit; Spanish prose recasts them — usually with commas, parentheses, or a colon, sometimes by splitting the sentence. Do not carry the English em-dash structure into the Spanish sentence by default.
- **Carried-over connectors (seed).** English connectors translated one-for-one ("however" → "sin embargo" in every slot, "in turn," "moreover" chains) read translated. Choose the connector Spanish would use at that joint — or none; Spanish often links with syntax where English inserts a connector word.
- **Abstract noun phrases.** English carries an idea comfortably in an abstract noun phrase; Spanish reaches for the concrete thing, the actor and the action, or a subordinate clause. A label or heading built on *declaración de…*, *la utilización de…*, *la parte de…* names a document or a quantity where the reader wants the thing itself, and it reads translated even when the grammar is faultless. Recast before it ships: *la utilización de los datos* → *cómo se usan los datos*. The pull is strongest in titles, headings and slide labels, where English compression is tightest.

## Written in Spanish from the start

A document drafted in Spanish with no English source — a project document, a note for a client, a
Spanish deck — is not a translation, and the anti-calque patterns above are only half of what it
needs. The other half is the conventions of Spanish prose as the user writes it:

- **No em-dash, anywhere.** Spanish prose does not interrupt with the em-dash; a comma, a colon,
  parentheses or a new sentence does the job. The rule of the voice profiles (sparing in English, none in Spanish) is the same rule; here it applies from
  the first draft, not at review.
- **The template-furniture exemption.** Text the document inherits from a form or a template — a
  funder's headings, a fixed clause, a field label, a signature block — keeps its form, em-dashes
  and anglicisms included; it is not the user's prose and is not edited toward their voice. The
  drafting session marks it once in the outline so the review round skips it.
- **Spanish typography.** Opening question and exclamation marks; the quotation marks the house
  uses («» in institutional documents, "" where the template already uses them); numbers with the
  house's thousands and decimal separators (an organization's document follows the organization's Spanish style, a
  client's follows the client's); a space before the percent sign only where the house does it;
  months and days in lower case. The house is named in the outline at step 1 of the drafting skill
  and applied throughout; a mixed document is a defect.
- **The review round is the in-chat round or the branch round above**, and every correction is a
  pair for the log like any other: a Spanish-first document's corrections are the same learning.

This is a section of this skill and not a skill of its own because the reviewer, the patterns and
the log are the same; a second language or a second reviewer would make it one.

## The companion log and its lifecycle

`translation_corrections_log.md` is the raw trail: every confirmed pair, append-only, never edited or pruned locally. Its lifecycle: pairs accumulate locally; if you keep a canonical skills repo, they travel back to it and merge into a shared log, and matured patterns are folded into this file's patterns section; when the skill is refreshed, the file reconciles per `PROJECT_SETUP.md` Part C's per-file local-modification handling, so local pairs are never silently dropped.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
