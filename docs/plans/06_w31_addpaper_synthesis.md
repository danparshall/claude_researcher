# claude_researcher — Plan 06: W3.1 add-paper synthesis + Tier C schema

**Goal:** Execute Plan 05's W3.1 retrofit + Tier C knock-on edits — fold Andrea's `paper_processing.md` into the existing `add-paper` skill, parameterize filename conventions, add BibTeX, split schema across `personal_info.md` (user-level) and STATUS.md (per-project Project parameters section), and update related touchpoints (BOOTSTRAP, RESEARCHER, init-research-repo).

**Status:** Ready for execution. All architectural decisions resolved in originating convos. This plan is execution-level scaffolding for a fresh agent — file paths, line ranges, exact strings.

**Parent plan:** [`05_aitaxbid_followups.md`](05_aitaxbid_followups.md) — sections "W3.1 retrofit — Fold AITaxBID synthesis into add-paper" and "Tier C decision — Generic-skill block format". Plan 06 is the implementation-level companion; Plan 05 carries the strategic reasoning.

**Originating convos:**

- [`20260513_plan05_flesh_out.md`](../convos/20260513_plan05_flesh_out.md) — W3.1 + Tier C flesh-out (the 9 deliverables, the schema split table, the Tier C Option C rationale)
- [`20260513_writing_and_branch_review_ports.md`](../convos/20260513_writing_and_branch_review_ports.md) — W4 ship session + Plan 06 design (port-time decisions for W3.1 made at end of session: BOOTSTRAP-style placeholders, two-format split confirmed, pipeline parameterization strategy)

**Confidence:** High. The architecture is fully spec'd in Plan 05; this plan just adds the execution-time concretizations (exact placeholder defaults, file line ranges, frontmatter strings) so a fresh agent can run with zero session-context loss.

**Branch:** main (build work, not exploration).

**Tracking issue:** [#3 — W3.1 fold-in (paper_processing → add-paper)](https://github.com/danparshall/claude_researcher/issues/3). Companion follow-on: [#4 — add-paper scaling discipline](https://github.com/danparshall/claude_researcher/issues/4), sequenced after this plan ships and the skill has ~5 papers of real user data.

---

## Decisions confirmed at design time (do NOT re-litigate)

These were pinned during the 2026-05-13 PM session via AskUserQuestion. Re-opening them risks unbounded scope; execute as specified.

### Pipeline strategy: parameterize Nori's step structure (NOT duplicate)

Andrea's `paper_processing.md` duplicates the pipeline across Protocol A and Protocol B sections (Steps 1A/2A/3A/... and 1B/2B/3B/...) — but her own intro says: *"The pipeline is identical for both (rename → extract → summarize → index → BibTeX); only filename convention, summary emphasis, and BibTeX entry type differ."* So the fold-in keeps Nori's 5-step structure (Obtain → Extract → Index → Summary → Stage) and **parameterizes within each step** by Protocol A vs Protocol B outcome from Step 0. This avoids a ~50% length increase from duplication while preserving Andrea's structural distinction. **Defer to Andrea on the content** of each parameterized section (filename convention details, summary emphasis breakdown, BibTeX entry type choice), per Plan 05's "Defer to Andrea on methodological details" principle.

### Filename placeholder semantics: BOOTSTRAP-style

`{FirstAuthor}` = first listed author's surname. `{LastAuthor}` = last listed author's surname. For solo papers, special-case to single-surname (e.g., `Acemoglu_2024__simple-macroeconomics-ai.pdf`, not `Acemoglu_Acemoglu_2024__...`). This was already established in BOOTSTRAP Batch 3 (lines 241-256) for the academic case — the W3.1 fold-in adopts it as the academic default.

### Academic vs institutional: keep Andrea's two-format split

Two separate fields in `personal_info.md`: `paper_naming.academic_format` + `paper_naming.institutional_format`. Step 0 triage routes each paper to one or the other. This preserves Andrea's field-tested distinction and matches the schema Plan 05 W3.1 deliverable 7 spec'd. **Do not collapse to a single format with a smart `{Author}` placeholder** (rejected at port time on grounds that it loses the triage distinction).

### Defaults

| Field | Default | Source / rationale |
|---|---|---|
| `paper_naming.academic_format` | `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf` | BOOTSTRAP smoke-test format established 2026-05-09; common-surname disambiguation rule (`SurnameF`) carries through (see BOOTSTRAP lines 243-247) |
| `paper_naming.institutional_format` | `{Institution}_{ShortTitle}_{Year}.pdf` | Andrea's Protocol B convention (`paper_processing.md` line 176). Example: `imf_g20RevenueAdmin_2025.pdf`. Lowercase institution + camelCase shortTitle. |
| `PAPERS_INDEX` | `PAPER_INDEX.md` | Nori singular convention (not Andrea's `PAPERS_INDEX.md` plural). Existing Nori add-paper uses singular; preserve to avoid breaking existing users. |
| `paper_summaries.structure` | `single-file` | Preserves current Nori behavior (one `PAPER_SUMMARIES.md`). `per-file` is the config knob exposed for future users but the code path that *handles* per-file is NOT implemented in this plan — deferred per Plan 05 W3.1 out-of-scope list. |
| `BIB_FILE` | (unset, optional) | When unset, the new Step-5 BibTeX path is skipped silently. No breaking change for existing users. |
| `CONDITIONAL_SECTION` | (unset, optional) | When unset, summary section (c) is omitted. |

### Provenance frontmatter (first dual-provenance skill)

```yaml
nori_researcher_source: nori-skillsets add-paper v1.0.0 (ported to claude_researcher in 0bbd419, 2026-05-10)
aitaxbid_source: ~/code/AITaxBID/skills/paper_processing.md@e0a736d (2026-05-02)
```

Order: Nori-Researcher first (it's the base), AITaxBID second (it's the augmentation/synthesis). The Nori upstream has no clean SHA (the `nori.json` at `~/.claude/skills/add-paper/nori.json` records version `1.0.0` only; no commit hash exposed), so the convention uses `<version>` + `(ported in <claude_researcher commit>, <date>)`. Sets the precedent for future synthesis ports.

### Source SHA verification (do NOT skip)

Andrea's `paper_processing.md` was verified byte-identical to scoping SHA `e0a736d` (2026-05-02) on 2026-05-13. Re-verify at execution time:

```bash
git -C ~/code/AITaxBID diff --stat e0a736d HEAD -- skills/paper_processing.md
```

Empty output = no drift; proceed. If non-empty, surface the drift to the user before continuing.

### Target final structure for `add-paper/SKILL.md`

D1 (Step 0 triage) and D6 (Scope) both insert content into the existing skill — they need to be sequential. Pin the final structure as:

```
---
<frontmatter — D9>
---

## Runtime detection
<existing block, unchanged>

<required>
<existing TodoWrite block, unchanged>
</required>

## Scope                              ← D6 inserts here (before # Adding a Paper)

# Adding a Paper
<announce-at-start line — keep>

## Step 0: Triage                     ← D1 inserts here (after H1, before Step 1)

## Step 1: Obtain the PDF             ← D2 modifies this step (read filename from config)
## Step 2: Extract text               ← keep
## Step 3: Add to PAPER_INDEX.md      ← keep (config-aware via PAPERS_INDEX)
## Step 4: Add to PAPER_SUMMARIES.md  ← D3 + D4 replace contents
## Step 5: Update BibTeX              ← D5 inserts new step (gated on BIB_FILE)
## Step 6: Stage files                ← was Step 5; renumber + add .bib when present

# Adding Multiple Papers              ← keep
# Common Mistakes                     ← keep, optionally add "Forgetting Step 0 triage"
```

### `paper_summaries.structure: per-file` behavior when set but unimplemented

The config knob exists as a forward-compat hook; the actual per-file code path is deferred per Plan 05 W3.1 out-of-scope. If a user sets `paper_summaries.structure: per-file` in STATUS.md project parameters: **the skill warns the user inline that per-file is not yet implemented and falls back to `single-file` for the current paper.** Suggested wording for the warning:

> "Note: `paper_summaries.structure: per-file` is configured but the per-file code path isn't implemented in this version of `add-paper`. Falling back to `single-file` (appending to `PAPER_SUMMARIES.md`) for this paper. The config knob is honored once per-file ships."

Non-breaking; the user sees the override clearly. Pinned by Dan 2026-05-13.

### No back-compat shim for the old `Paper naming format` field

The current `personal_info.md.template` has a single `**Paper naming format:** `<PAPER_NAMING>`` line. Plan 06 D7 replaces it outright with two new lines (`<PAPER_NAMING_ACADEMIC>` + `<PAPER_NAMING_INSTITUTIONAL>`). **The rewritten `add-paper` skill does NOT read the old `Paper naming format` field as a fallback.** Existing alpha users will get a breaking change: their old format string in `personal_info.md` is no longer read by `add-paper`. They get the new defaults until they manually edit their `personal_info.md` to the new shape (or re-run BOOTSTRAP).

This is acceptable per Dan's call 2026-05-13: *"they're alphas and they deserve breaking changes."* Document in the commit message + add a STATUS.md "Recent sessions" note after shipping so any alpha users picking up new behavior have a pointer.

---

## Pre-flight reads (do FIRST, before any edits)

A fresh agent has no session context. Read these in order:

1. **`STATUS.md`** (repo root) — current state of claude_researcher, recent sessions, this plan's place in the larger sequence
2. **`docs/plans/05_aitaxbid_followups.md`** — full W3.1 section (lines ~178-240) + Tier C section (lines ~244-310). Plan 06 is the execution-level companion; Plan 05 carries the strategic reasoning Plan 06 assumes
3. **`docs/convos/20260513_plan05_flesh_out.md`** — section "W3.1 — add-paper retrofit spec" + section "Tier C decision — Option C (extend STATUS.md role)"
4. **`docs/convos/20260513_writing_and_branch_review_ports.md`** — the W4 ship convo (so you understand the `aitaxbid_source` precedent set there)
5. **Source files (read in full):**
   - `~/code/AITaxBID/skills/paper_processing.md` (320 lines, SHA `e0a736d`) — Andrea's source
   - `template/skills/add-paper/SKILL.md` (current 151 lines) — the target of the in-place edit
6. **Files you'll also edit (skim first):**
   - `template/templates/personal_info.md.template` (40 lines)
   - `template/skills/init-research-repo/SKILL.md` (170 lines — Step 3 STATUS.md seeding is at lines 74-114)
   - `template/RESEARCHER.md` §2c (lines 184-200) and §2e (line 211 onward; informational)
   - `template/BOOTSTRAP.md` Batch 3 (lines 235-256), Step 5b (lines 272-276), Step 7 STATUS.md seed (lines 400-421)

**Pre-flight check (after reads, before edits):**

```bash
git status --short  # working tree should be clean except for plan 06 itself
git -C ~/code/AITaxBID rev-parse HEAD  # capture for the convo summary later
```

---

## Tasks

Sequence matters for some of these (filename param flows downstream into BOOTSTRAP). Suggested order: D1 → D2 → D3 → D4 → D5 → D6 → D9 (all in `add-paper/SKILL.md`, one rewrite) → D7 (personal_info template + define STATUS.md Project parameters block) → knock-on edits → D8 (BOOTSTRAP, which depends on D7's schema being settled).

### D1 — Step 0 triage in add-paper/SKILL.md

Add a new section between the existing `## Runtime detection` block and `# Adding a Paper`. Content port-from Andrea verbatim (with name-stripping if any — Andrea's source uses neutral language throughout, no Marta/RA references in `paper_processing.md`):

- Three structural questions (abstract vs executive summary; research question/hypothesis; new estimates from data)
- "Two or more 'yes' → Protocol A; two or more 'no' → Protocol B" routing
- Borderline-case guidance (multilateral working papers usually A; institutional monographs usually B; country case studies usually B; IDB Discussion Papers — triage on structure not publisher)
- Pointer to `document_processing.md` for legislation / regulatory docs / consultant deliverables (currently aspirational — Wave 5 deferred per Plan 02)

**Source:** Andrea's lines 61-87 (Step 0 + the Step-differs table).

### D2 — Filename convention parameterization in add-paper/SKILL.md

Replace the hardcoded line 48 (`**Filename convention:** `AuthorLast_Year__short_description.pdf``) and its example list (lines 49-51) with read-from-config logic:

```markdown
**Filename convention:** Read from the user's `personal_info.md` `paper_naming` field, selecting by Step 0 outcome:

- **Protocol A (academic):** `paper_naming.academic_format`, default `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf`. Common-surname disambiguation: render `{Surname}F` (surname + first-name initial, no separator) when collisions are likely — Anglo surnames (Smith, Jones, Patel, Singh) and East Asian (Wang, Li, Chen, Zhang, Liu, Kim, Park, Choi, Tanaka, Suzuki, Sato). For solo authors, single surname only (drop the duplicate). Example: `Acemoglu_Restrepo__2026--ai-jobs.pdf`, `SmithJ_2024--stress-sleep.pdf`.
- **Protocol B (institutional):** `paper_naming.institutional_format`, default `{Institution}_{ShortTitle}_{Year}.pdf`. Institution = short acronym, lowercase (`imf`, `oecd`, `un`); for governments, country + agency in camelCase (`brazilRfb`, `mexicoSat`). ShortTitle = two descriptive words in camelCase. Example: `imf_g20RevenueAdmin_2025.pdf`, `oecd_taxAdmin30_2023.pdf`.

If `paper_naming` is unset in `personal_info.md`, fall back to the defaults above.
```

**Source for institutional details:** Andrea's lines 174-188 (Step 1B). Carry over her notes on multi-institution co-publication ("lead with principal author institution; use working-group acronym if co-branded") as a sub-bullet or callout.

### D3 — Replace Step 4 summary template with dual-protocol shape

Replace lines 92-117 of current `add-paper/SKILL.md` (the `## Step 4: Add to PAPER_SUMMARIES.md` block + its Important list) with the dual-protocol structure. Branch on Protocol A vs Protocol B:

- **Protocol A (academic):** section (a) thesis/research-question/contribution; (b) methodology+key-findings (data sources/sample/method/identification/effect sizes — the precision principle); (c) conditional (only if CONDITIONAL_SECTION defined AND paper has matching content); (d) relevance to PROJECT_QUESTION
- **Protocol B (institutional):** section (a) purpose/commissioning context/principal thesis/relation to companion reports; (b) document type+frameworks+findings+policy framework+country case studies; (c) conditional (same as A); (d) relevance + "what position does this represent" + cross-references in existing library

**Source:** Andrea's lines 110-130 (Protocol A summary) + lines 199-220 (Protocol B summary). Lift verbatim per defer-to-Andrea; minor edits to thread in `PROJECT_QUESTION` / `CONDITIONAL_SECTION` config-key references (those land in STATUS.md project parameters per D7, not personal_info.md as Andrea's source assumes).

### D4 — Summary Evolution Principle paragraph

Add immediately after the dual-protocol summary template:

```markdown
**Summary evolution principle.** The (a)–(d) structure above is a **floor, not a ceiling**. As the user works with a paper over time (asking questions, requesting explanations, cross-referencing with other papers), the summary should grow. Expanded summaries with worked examples, accessible explanations of technical concepts, cross-references, and the user's own notes are expected and desirable. Do not trim or reorganize expanded summaries back to the minimal format.
```

**Source:** Andrea's lines 131-133. Use her exact phrasing.

### D5 — BibTeX step (gated on BIB_FILE)

Insert a new Step 5 between current Step 4 (Summary) and current Step 5 (Stage). Renumber the current Stage step to Step 6.

```markdown
## Step 5: Update BibTeX (if `BIB_FILE` is defined in STATUS.md project parameters)

If `BIB_FILE` is unset, skip this step silently.

Add a new entry to the project's `.bib` file. The cite key follows the filename convention (matches the filename without the `.pdf` extension).

**Protocol A entries** use `@article` for published work or `@unpublished` for working papers. Required fields: `title`, `author`, `year`, plus `journal` / `note` / `institution` as appropriate. Always include an `abstract = {}` field — copy the paper's abstract verbatim, do not paraphrase.

**Protocol B entries** use `@techreport` for institutional reports, `@book` for monographs published as books, or `@inbook` for chapters within institutional monographs. Required fields for `@techreport`:
- `author = {{Institution Name}}` — **double braces** preserve casing and prevent BibTeX from treating "Fund" or "Bank" as a surname
- `title`, `institution`, `year`
- `type` — describe the document type (e.g., "G20 Background Note", "Policy Research Working Paper")
- `month` — when relevant
- `note` — for institutional team, lead authors, partner institutions
- `abstract` — copy from the report's executive summary if no separate abstract exists

For `@book` / `@inbook`, include `publisher`, `address`, and `isbn` if available.
```

**Source:** Andrea's lines 145-147 (Step 5A) + 226-238 (Step 5B).

### D6 — document_processing.md pointer

In the introduction section of `add-paper/SKILL.md` (after the existing top-of-file frontmatter + Runtime detection + before Step 0), add a scope note:

```markdown
## Scope

This skill processes two kinds of documents:

- **Academic-style papers** — research-oriented documents with original empirical or theoretical contribution (journal articles, working papers, dissertations, white papers structured as research). Routed to **Protocol A** by Step 0 triage.
- **Institutional-style reports** — substantive analytical documents that synthesize evidence, position a framework, or advise on policy, but do not present the authors' own original research with a stated hypothesis (G20 background notes, IMF/World Bank/OECD/UN flagship reports, multilateral working-group papers, regional development bank policy reports). Routed to **Protocol B** by Step 0 triage.

For **legislation, government regulatory documents, terms of reference, and consultant deliverables tied to a single project**, use `document-processing` instead — not this skill. (Note: `document-processing` is deferred per Plan 02 Wave 5; the pointer is currently aspirational.)
```

**Source:** Andrea's lines 16-23 + 247-249.

### D7 — Schema split per Tier C Option C

Two files to edit:

**File A: `template/templates/personal_info.md.template`**

Replace line 35 (`- **Paper naming format:** `<PAPER_NAMING>``) with two fields:

```markdown
- **Paper naming (academic):** `<PAPER_NAMING_ACADEMIC>`
- **Paper naming (institutional):** `<PAPER_NAMING_INSTITUTIONAL>`
```

**File B: Define the STATUS.md Project parameters block** (used by init-research-repo D-knock-on-1 and BOOTSTRAP D8 and add-paper D3/D5).

Canonical format (this is the schema for the new section — keep this consistent across the three files that seed it):

```markdown
## Project parameters

Per-project configuration the skills read at runtime. Update only when the project's scope or conventions change.

- `PROJECT_QUESTION`: <one-sentence research question — feeds add-paper Step 4 section (d) relevance writing>
- `CONDITIONAL_SECTION`: <relevance filter, or `unset` — defines what add-paper Step 4 section (c) extracts>
- `BIB_FILE`: <filename, or `unset` — gates add-paper Step 5>
- `PAPERS_INDEX`: <filename, default `PAPER_INDEX.md`>
- `paper_summaries.structure`: `single-file` (default) | `per-file` (config knob; per-file code path not yet implemented — Plan 05 W3.1 out-of-scope item)
```

In `add-paper/SKILL.md` (likely the introduction or scope section), add a note pointing readers at where the schema lives: *"The four `PROJECT_QUESTION` / `CONDITIONAL_SECTION` / `BIB_FILE` / `PAPERS_INDEX` keys live in the research repo's STATUS.md under `## Project parameters`. The two `paper_naming` keys live in the user's `personal_info.md`."*

### D8 — BOOTSTRAP.md interview update

Two locations to edit:

**Location 1: Batch 3 paper-naming question (lines 235-256)**

The current question asks one format only. Extend to ask both. Keep the existing default + disambiguation rule for academic; add the institutional default. Suggested rewrite (preserve the existing structure; this is a content extension, not a rewrite of the batch):

```markdown
> 3. **Paper naming conventions** — when I save papers to your repo, the filename format depends on whether the paper is academic-style (research with hypothesis + data) or institutional-style (synthesis/policy report). Two defaults:
>
>    - **Academic default:** `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf`. Common-surname disambiguation: `SurnameF` (surname + first-name initial, no separator) when collisions are likely — Anglo (Smith, Jones, Patel, Singh) and East Asian (Wang, Li, Chen, Zhang, Liu, Kim, Park, Choi, Tanaka, Suzuki, Sato — use judgment). Solo papers: single surname only (drop the duplicate). Example: `Vaswani_Polosukhin__2017--attention-is-all-you-need.pdf`, `SmithJ_2024--stress-sleep.pdf`.
>    - **Institutional default:** `{Institution}_{ShortTitle}_{Year}.pdf`. Institution = short acronym, lowercase (`imf`, `oecd`, `un`); for governments, country + agency in camelCase (`brazilRfb`). ShortTitle = two descriptive words in camelCase. Example: `imf_g20RevenueAdmin_2025.pdf`.
>
>    Press Enter to accept both defaults, or specify your own format(s) — you can override one and keep the default for the other."
```

Record as **two fields**: `<PAPER_NAMING_ACADEMIC>` + `<PAPER_NAMING_INSTITUTIONAL>`. Update the canonical-text paragraph at lines 252-256 to capture both formats and the disambiguation rule (for academic).

**Location 2: Step 5b (line 274) + the Step 7 STATUS.md seed (lines 400-421)**

Step 5b currently records `<TOPIC>` from the one-sentence project question. **Tighten the prompt** to capture both:
- `<TOPIC>` (existing — short topic phrase used as repo description)
- `<PROJECT_QUESTION>` (new — the one-sentence research question Andrea's summaries reference for section (d))

These may be byte-identical for many users. Suggested phrasing: *"That sentence is also your `PROJECT_QUESTION` — the question your paper summaries will measure relevance against. If you'd phrase it differently for that purpose, give me a tighter version; otherwise I'll use the same sentence for both."*

Step 7's STATUS.md seed (lines 400-421) currently has `## What this repo is`, `## Current state`, `## Recent sessions`, `## Archived research lines`. **Insert** a `## Project parameters` section between `## What this repo is` and `## Current state`, using the canonical format from D7 File B. Substitute `<PROJECT_QUESTION>` from Step 5b; leave `CONDITIONAL_SECTION`, `BIB_FILE` as `unset` (users can edit later); default `PAPERS_INDEX: PAPER_INDEX.md` and `paper_summaries.structure: single-file`.

### D9 — Dual provenance frontmatter

In `template/skills/add-paper/SKILL.md`, replace the current frontmatter (lines 1-4) with:

```yaml
---
name: add-paper
description: Add a paper to the research collection — Step 0 triage routes to academic or institutional protocol; pipeline runs rename → extract → summary (dual-protocol) → index → BibTeX. Ensures every paper is fully integrated.
nori_researcher_source: nori-skillsets add-paper v1.0.0 (ported to claude_researcher in 0bbd419, 2026-05-10)
aitaxbid_source: ~/code/AITaxBID/skills/paper_processing.md@e0a736d (2026-05-02)
---
```

The description is rewritten to reflect the new dual-protocol shape; keep it concise (one sentence ideally). **`name:` is lowercase `add-paper`** — the prior `Add-Paper` Title-Case was normalized to kebab-case in a name-cleanup commit immediately before Plan 06 lands.

---

## Knock-on edits

These bundle naturally with D7 since they all touch the STATUS.md project-parameters seam.

### Knock-on 1 — `init-research-repo/SKILL.md` seeds Project parameters

Edit `template/skills/init-research-repo/SKILL.md` Step 3 (lines 74-114). The current heredoc seeds STATUS.md with `## Archived Research Lines` and `## Recent Sessions` sections. **Insert** a `## Project parameters` section using the canonical format from D7 File B. Place it after `## Current Focus` (the minimal-seed branch at lines 94-114) and after the equivalent position in the append branch (lines 78-90).

The seeded values are placeholder-style (since init-research-repo runs on an existing repo without bootstrap context, it can't ask the user):

```markdown
## Project parameters

Per-project configuration the skills read at runtime. Update only when the project's scope or conventions change.

- `PROJECT_QUESTION`: [to be filled in — one-sentence research question]
- `CONDITIONAL_SECTION`: unset
- `BIB_FILE`: unset
- `PAPERS_INDEX`: PAPER_INDEX.md
- `paper_summaries.structure`: single-file
```

Update Step 5's "Tell the user what was created" output (lines 130-144) to mention the new section.

### Knock-on 2 — RESEARCHER.md §2c note

Edit `template/RESEARCHER.md` §2c (line 194-199). The current text says: *"STATUS.md tells you what's currently active, recent sessions, the archived-research-lines table, and may contain a top-of-file `workflow_mode` field"*. Add a sentence at the end of that paragraph:

```markdown
STATUS.md may also carry a `## Project parameters` section listing per-project config (`PROJECT_QUESTION`, `CONDITIONAL_SECTION`, `BIB_FILE`, `PAPERS_INDEX`, `paper_summaries.structure`). Skills that need these values read them from STATUS.md — no extra fetch since STATUS.md is already part of session-start.
```

### Knock-on 3 — add-paper reads project parameters from STATUS.md (not personal_info.md)

This is implicit in D3/D5/D7 but worth pinning explicitly so the implementing agent doesn't accidentally have add-paper try to read PROJECT_QUESTION from personal_info.md. Andrea's source assumes everything's in CLAUDE.md; the Tier C split moves the per-project keys to STATUS.md while keeping the per-user keys (paper_naming) in personal_info.md. Verify after writing: grep the new add-paper SKILL.md for `personal_info.md` and `STATUS.md` mentions and ensure they reference the right keys in each location.

---

## Verification & sanity checks (do BEFORE committing)

After all edits, run:

```bash
# 1. Verify byte-identical to scoping SHA (no drift since plan was written)
git -C ~/code/AITaxBID diff --stat e0a736d HEAD -- skills/paper_processing.md
# expect empty output

# 2. Verify add-paper has dual provenance
head -10 template/skills/add-paper/SKILL.md | grep -E 'nori_researcher_source|aitaxbid_source'
# expect both keys present

# 3. Verify no stale "CLAUDE.md" references in the new add-paper (per Plan 03 rename)
grep -n 'CLAUDE.md' template/skills/add-paper/SKILL.md
# expect empty (or only inside fenced code blocks if any)

# 4. Verify Project parameters section appears in all 3 seed locations
grep -l 'Project parameters' template/BOOTSTRAP.md template/skills/init-research-repo/SKILL.md
# expect both files listed

# 5. Verify personal_info.md.template has the two new fields
grep -E 'PAPER_NAMING_ACADEMIC|PAPER_NAMING_INSTITUTIONAL' template/templates/personal_info.md.template
# expect both placeholders present

# 6. Verify RESEARCHER.md §2c mentions Project parameters
grep -n 'Project parameters' template/RESEARCHER.md
# expect at least one match in §2c

# 7. Verify audit skills aren't broken by the new schema
grep -E 'PROJECT_QUESTION|CONDITIONAL_SECTION|BIB_FILE|paper_summaries.structure' \
  template/skills/audit-docs/SKILL.md template/skills/audit-papers/SKILL.md
# expect no matches — audit skills don't currently read project parameters, so no edits
# needed unless the new schema breaks something. If matches appear, investigate before shipping.
```

If any of these fail, fix before committing.

---

## Commit strategy

Single ship commit per Plan 05's "ship as a coherent unit" pattern (matches Plan 04 and W4 ship in commit `9ca89b8`). Suggested message:

```
plan 06 W3.1 ship: add-paper synthesis + Tier C schema split

Folds Andrea's paper_processing.md into the existing add-paper skill
per Plan 05 W3.1 (deliverables 1-9 + Tier C knock-on edits). First
skill carrying dual provenance frontmatter (nori_researcher_source +
aitaxbid_source).

- template/skills/add-paper/SKILL.md — full rewrite. Step 0 triage
  (academic vs institutional via Andrea's three-question rule); filename
  conventions parameterized via personal_info.md (academic default
  {FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf, institutional default
  {Institution}_{ShortTitle}_{Year}.pdf); dual-protocol summary template
  (a/b/c/d); Summary Evolution Principle paragraph; new BibTeX step
  gated on BIB_FILE; document_processing.md pointer (Wave 5 aspirational).
  Pipeline-structure choice: parameterize Nori's 5-step shape by Protocol
  A/B instead of duplicating across A-suffix / B-suffix steps.

- template/templates/personal_info.md.template — Paper naming split into
  academic + institutional fields.

- template/BOOTSTRAP.md — Batch 3 extended to ask both formats with
  defaults; Step 5b tightens TOPIC capture to also pin PROJECT_QUESTION;
  Step 7 STATUS.md seed inserts the new Project parameters section.

- template/skills/init-research-repo/SKILL.md — STATUS.md seed inserts
  Project parameters section with placeholder values.

- template/RESEARCHER.md §2c — notes STATUS.md now carries project
  parameters (no extra fetch since STATUS.md is already part of
  session-start).

Tier C Option C locked: per-user paper_naming formats stay in
personal_info.md; per-project keys (PROJECT_QUESTION, CONDITIONAL_SECTION,
BIB_FILE, PAPERS_INDEX, paper_summaries.structure) live in STATUS.md
under `## Project parameters`.

paper_summaries.structure has single-file as default; per-file code path
deferred (Plan 05 W3.1 out-of-scope) — only the config knob exists, no
code path that handles per-file value yet.

Sources verified byte-identical to scoping SHA e0a736d at commit time.
```

Push to origin after committing (per Nori branch-hygiene rule + matches the W4 ship pattern).

### Post-ship actions

1. **Close [issue #3](https://github.com/danparshall/claude_researcher/issues/3)** — W3.1 fold-in is done. Reference the ship commit SHA in the close message.
2. **Leave [issue #4](https://github.com/danparshall/claude_researcher/issues/4) open** — scaling discipline (lookup discipline, length guidelines, two-stage file structure, multi-repo logic, "Beyond this summary" affordance) is sequenced for a later session after ~5 papers of real user data accumulate. Threshold calibration in #4 depends on that data.
3. **Run finish-convo** at end of session — create a new convo file, update STATUS.md with the W3.1 ship entry, commit + push the docs. Standard Nori workflow; the wrap commit is separate from the W3.1 ship commit so the W3.1 commit is bisectable on its own.

---

## What this plan deliberately does NOT cover

- **`per-file` summary code path** — Plan 05 W3.1 out-of-scope. Only the config knob (`paper_summaries.structure: per-file`) exists after this plan; the actual code that writes to `papers/summaries/SUMMARY_*.md` is deferred until at least one user actually wants per-file.
- **Claude status / User status framework** (Andrea's Steps 6A/6B) — adds a reading-recommendation label per paper. Not in Plan 05's deliverable list; tracked as a separate future follow-up if it comes up.
- **Lookup Protocol** (Andrea's three-tier index → summary → text fallback) — already implicit in Nori workflow but not formalized; minor and deferred.
- **Andrea's three style profiles** (`Andrea_Writing_Style_Profile.md`, etc.) — content is person/institution-specific; out of scope per Plan 05.
- **issue #4 (add-paper scaling discipline)** — sequenced AFTER this plan ships AND ~5 papers of real user data accumulate. Includes lookup discipline (grep+offset reading), length guidelines (~10% with 2000-word ceiling), two-stage file structure with migration trigger, multi-repo destination logic, "Beyond this summary" affordance. Don't pre-implement.
- **Wave 5 `document-processing` port** — deferred per Plan 02. This plan only adds the aspirational *pointer* to that skill.

---

## Open questions (for the implementing agent to raise if hit)

- **Filename slug format inside `{Slug}`** — kebab-case vs snake_case? BOOTSTRAP Batch 3 uses underscore-separated (`attention_is_all_you_need`); existing Nori add-paper says "Use snake_case for the description" (line 50). Andrea uses camelCase (`simpleAI`). **Recommendation:** kebab-case (`attention-is-all-you-need`) for filesystem-friendliness and URL-safety. **Confirm at execution time** if a different convention is wanted.
- **Lowercase year vs uppercase `{Year}`** — cosmetic. Recommend `{Year}` (capitalized as placeholder, since it's a token) but render as lowercase 4-digit (`2026` not `Year` or `Y2026`).
- **PAPER_INDEX vs PAPERS_INDEX casing** — Plan 05 W3.1 D7 spec says `PAPERS_INDEX` (Andrea's plural). Defaults to `PAPER_INDEX.md` (Nori singular). The config-key name and the filename it refers to don't need to match — this is fine but worth noting. **Recommendation:** keep as-is to preserve Nori's existing filename while allowing per-project overrides.
- **What about existing users' STATUS.md files** (Dan's `claude_researcher` itself, any beta users)? Should we backfill the `## Project parameters` section on existing repos? **Recommendation:** no — claude_researcher itself is a meta dev repo, not a research repo, so the section isn't needed there. Beta users will get the section the next time they bootstrap a new repo or pull through BOOTSTRAP again. Existing add-paper invocations on existing repos: the skill falls back to defaults when keys are absent, so no breaking change.

---

## Estimated effort

~45-60 minutes for a fresh agent who reads pre-flight materials and follows the deliverable-by-deliverable spec without re-litigating decisions. The `add-paper/SKILL.md` rewrite is the biggest single piece (~250-300 lines target). Other edits are surgical (1-2 sections per file). Verification + commit at the end adds ~10 min.
