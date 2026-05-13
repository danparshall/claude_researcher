# claude_researcher — Plan 07: add-paper dispatcher refactor

**Goal:** Refactor `add-paper` from a unified dual-protocol skill into a thin triage/dispatcher that loads one of three per-protocol target skills (`paper-processing-academic`, `paper-processing-institutional`, future Wave 5 `document-processing`). While in there, pick up Andrea's richer Step 2 institutional rules that Plan 06 left out.

**Status:** Ready for execution. All architectural decisions resolved at design time. Execution-level scaffolding for a fresh agent: file paths, line ranges, exact strings, verification script.

**Parent plans:**

- [`06_w31_addpaper_synthesis.md`](06_w31_addpaper_synthesis.md) — the unified dual-protocol add-paper that Plan 07 refactors. Plan 06 explicitly chose "parameterize Nori's step structure (NOT duplicate)" (lines 26-28); Plan 07 reverses that decision on architectural grounds described in the originating convo. Plan 06's content is the raw material for Plan 07's split.
- [`05_aitaxbid_followups.md`](05_aitaxbid_followups.md) — W3.1 retrofit + Tier C decision. Plan 07 doesn't change Tier C (schema-split stays as Plan 06 shipped it).

**Originating convo:** [`20260513_plan06_w31_addpaper_synthesis_ship.md`](../convos/20260513_plan06_w31_addpaper_synthesis_ship.md) — the Post-ship discussion section captures the architectural pivot reasoning, Dan's framing ("triage and then load the skill relevant for the paper"), the three-option trade-off (defer / plan-then-execute / execute now) and Dan's choice of (b).

**Confidence:** Medium-high. Architecture is genuinely cleaner than the unified version (separation of triage from work; uniform routing including the deferred Wave 5 target; per-protocol files evolve independently). Risk surface is mechanical — splitting one file into three with correct cross-reference partitioning. Plan 06's just-shipped content is the source; no fresh source-text interpretation needed. The Step 2 institutional enrichment (true scope addition vs Plan 06) is small and source-bounded.

**Branch:** main (build work, not exploration).

**Tracking issue:** none filed yet — Plan 07 is a self-contained refactor; tracking lives in the plan + convo + STATUS chain. File an issue at execution time if scope grows.

---

## Decisions confirmed at design time (do NOT re-litigate)

These were pinned during the 2026-05-13 evening session post-Plan-06-ship discussion. Re-opening them risks unbounded scope; execute as specified.

### Names

- **Dispatcher:** stays `add-paper` (no rename). User-facing entry point; preserves the trigger phrase users already learned during Plan 06.
- **Protocol A target:** `paper-processing-academic`. Matches Andrea's source filename precedent (`paper_processing.md` / `document_processing.md`) and parallels the deferred Wave 5 `document-processing`.
- **Protocol B target:** `paper-processing-institutional`. Same naming logic.
- **Wave 5 (not in this plan):** `document-processing` — for non-paper documents (legislation, regulatory docs, ToRs, consultant deliverables). Still deferred per Plan 02; Plan 07 only adds the dispatcher pointer to it, not the skill itself.

Kebab-case throughout per Nori convention.

### Dispatch mechanism

**Option A — instruction-based handoff.** At the bottom of Step 0 in the dispatcher, after triage routes to Protocol A or Protocol B, the agent is instructed: *"Now read `template/skills/paper-processing-academic/SKILL.md` (or `paper-processing-institutional/SKILL.md`) and follow it from this point forward. You have already completed Step 0; the per-protocol skill picks up at Step 1 (its own first step)."*

This matches Nori's lazy-loading principle (only one per-protocol skill loaded per invocation) and the existing on-demand fetch pattern in §2d. **Rejected alternative:** pre-load both per-protocol files into context and branch. Heavier; no real edge case justifies the load.

### Per-type skills are independently invokable

A sophisticated user who already knows the protocol can invoke `paper-processing-academic` (or `-institutional`) directly without going through `add-paper`'s dispatch hop. Each per-protocol skill carries:

- Its own `## Runtime detection` block (identical to add-paper's; copy verbatim)
- Its own `<required>` TodoWrite block
- Its own announce-at-start line: *"I'm using the paper-processing-academic skill (Protocol A — academic paper)"* or equivalent for institutional
- Its own Steps 1-6 (no Step 0; that stays in dispatcher)

**Rejected alternative:** require dispatch via add-paper. Would have meant a "this skill is invoked via add-paper" disclaimer at the top of each per-protocol file. Lower flexibility; same maintenance cost. The independently-invokable shape is the default Nori pattern.

### What stays in `add-paper` after refactor

The dispatcher contains, in order:

1. Frontmatter (dual provenance preserved; description revised to reflect the dispatcher role)
2. `## Runtime detection` (unchanged from current)
3. `<required>` TodoWrite block — **shrinks to 2 entries**: "Triage (Step 0)" + "Load and follow the routed per-protocol skill"
4. `## Scope` — revised to enumerate the three dispatch targets (academic → `paper-processing-academic`; institutional → `paper-processing-institutional`; non-paper → `document-processing` deferred). The "Where config keys live" sub-note stays (it's general-purpose and the per-protocol skills each reference back to it).
5. `# Adding a Paper` H1 + announce-at-start line: *"I'm using the Add Paper skill — first I'll triage the document, then dispatch to the appropriate per-protocol skill."*
6. `## Step 0: Triage` — content unchanged from Plan 06 (the three structural questions, two-or-more routing rule, borderline-case guidance, Step-differs table). The table is preserved as a quick reference for users skimming, even though the actual step content lives in the per-protocol files.
7. **Dispatch instruction** — new paragraph at end of Step 0, formatted as a bash-style decision tree the agent literally executes:

   ```markdown
   **Dispatch:**

   - **Protocol A → academic** → Read `template/skills/paper-processing-academic/SKILL.md` and follow it from Step 1 onward. Step 0 (this skill) is already complete.
   - **Protocol B → institutional** → Read `template/skills/paper-processing-institutional/SKILL.md` and follow it from Step 1 onward. Step 0 (this skill) is already complete.
   - **Non-paper document** (legislation, regulatory docs, ToRs, consultant deliverables) → use `document-processing` (currently deferred per Plan 02 Wave 5; if you hit this branch, fall back to manual handling and surface to the user).
   ```

8. `# Common Mistakes` — kept, scoped to dispatcher-level mistakes only:
   - "Forgetting Step 0 triage" (preserved from Plan 06)
   - "Reading keys from the wrong file" (preserved; central to the schema-split story; the per-protocol skills each reference back to this note rather than duplicating it)
   - **New:** "Trying to do the full workflow in `add-paper`" — problem: agent ignores the dispatch instruction and tries to execute Steps 1-6 from this file; fix: after Step 0, read and follow the routed per-protocol skill. (Anti-pattern surfaced during plan-design; pre-empt at execution time.)

Everything from `## Step 1: Obtain the PDF` through `## Step 6: Stage files` plus `# Adding Multiple Papers` is **removed** from add-paper. Moves to the per-protocol skills (each gets its own variant).

### What moves to `paper-processing-academic/SKILL.md` (new)

The Protocol A branch of every step, in self-contained form:

- Frontmatter with dual provenance + description scoped to Protocol A
- `## Runtime detection` block (verbatim copy from add-paper)
- `<required>` TodoWrite block — 5 entries: Obtain PDF / Extract text / Add to index / Add to PAPER_SUMMARIES (Protocol A shape) / Update BibTeX (gated) / Stage files. Renumber per the standalone numbering (Step 1 through Step 5 or Step 6 depending on whether the gated BibTeX step counts).
- Announce-at-start: *"I'm using the paper-processing-academic skill (Protocol A — academic paper)."*
- Brief preamble: *"This skill handles the Protocol A workflow for academic-style papers. Triage to Protocol A was already done by `add-paper` Step 0 — if you're reading this skill directly without going through `add-paper`, confirm the document is academic-style before proceeding (abstract present, research question/hypothesis, original empirical or theoretical contribution from data the authors analyzed)."*
- Pointer to dispatcher for config-key schema: *"Configuration keys (`PROJECT_QUESTION`, `CONDITIONAL_SECTION`, `BIB_FILE`, `PAPERS_INDEX`, `paper_summaries.structure`) live in the research repo's `STATUS.md` under `## Project parameters`. Filename format keys (`paper_naming.academic_format`) live in the user's `personal_info.md`. See `add-paper/SKILL.md` Scope section for full schema details."*
- Step 1: Obtain the PDF — Protocol A filename convention only (academic default `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf` with kebab-case `{Slug}` and the common-surname `SurnameF` disambiguation rule). Drop all references to Protocol B's institutional format.
- Step 2: Extract text — verbatim from Plan 06's Step 2 (no protocol-specific differences for academic).
- Step 3: Add to PAPER_INDEX (config-aware via PAPERS_INDEX) — verbatim from Plan 06.
- Step 4: Add to PAPER_SUMMARIES — **Protocol A summary template only** (sections a/b/c/d with academic emphasis). Drop the Protocol B block. Keep the `paper_summaries.structure: per-file` warning + fallback paragraph (still applies to both protocols).
- Step 5: Update BibTeX (gated on `BIB_FILE`) — Protocol A entry types only (`@article` / `@unpublished`). Drop the `@techreport` / `@book` / `@inbook` Protocol B paragraphs.
- Step 6: Stage files — verbatim from Plan 06.
- Adding Multiple Papers — adapted: *"If the user asks to add several papers at once, process each through all 6 steps (including dispatcher's Step 0 triage) before moving to the next."*
- Common Mistakes — Protocol A-specific subset: Writing summaries from the abstract only / Adding numbers without context / Forgetting to update PAPER_INDEX when updating PAPER_SUMMARIES. Drop the dispatcher-level mistakes (those stay in add-paper).
- **Summary evolution principle** paragraph — verbatim from Plan 06.

### What moves to `paper-processing-institutional/SKILL.md` (new)

Same structural shape as `paper-processing-academic` but for Protocol B, with one true scope addition:

- Frontmatter with dual provenance + description scoped to Protocol B
- `## Runtime detection` block (verbatim copy)
- `<required>` TodoWrite block — 5-6 entries paralleling academic
- Announce-at-start: *"I'm using the paper-processing-institutional skill (Protocol B — institutional report)."*
- Brief preamble (parallels academic; triage came from add-paper Step 0, or confirm institutional-style if invoked directly)
- Pointer to dispatcher for config-key schema (same as academic)
- Step 1: Obtain the PDF — Protocol B institutional filename convention only (default `{Institution}_{ShortTitle}_{Year}.pdf`, lowercase acronym / camelCase ShortTitle, multi-institution co-publication rules, multi-institution working-group acronym rules, naming-ambiguity ask-user rule). Drop all references to academic format.
- **Step 2: Extract text — PROTOCOL B ENRICHMENT (true scope addition vs Plan 06).** This is the place where Andrea's source has rules that didn't survive Plan 06's "keep Step 2 as-is" decision. Lift verbatim from Andrea's `paper_processing.md` lines 192-197:
  - "Institutional reports often have heavy front matter (foreword, acknowledgments, list of acronyms, list of figures and boxes)."
  - **Preserve the acronym list verbatim** — these are reference material for downstream work.
  - **Preserve boxes and figure captions with their key data** — these often carry the report's quotable findings.
  - **Strip decorative front matter** (forewords, dedications) unless they contain substantive framing.
- Step 3: Add to PAPER_INDEX (config-aware via PAPERS_INDEX) — verbatim. Optional: add Andrea's "Outlet" column guidance from her lines 222-224 (describe document type rather than journal — examples: "IMF G20 background note", "World Bank Policy Research Working Paper"). Worth surfacing; Plan 06 dropped it for brevity.
- Step 4: Add to PAPER_SUMMARIES — **Protocol B summary template only** (sections a/b/c/d with institutional emphasis: purpose+commissioning / doc-type+frameworks+databases+findings+policy / conditional / position+cross-references). Drop the Protocol A block. Keep the `paper_summaries.structure: per-file` warning + fallback.
- Step 5: Update BibTeX (gated on `BIB_FILE`) — Protocol B entry types only (`@techreport` with double-braced institutional author, `@book` for monographs, `@inbook` for chapters). Drop Protocol A `@article` paragraphs.
- Step 6: Stage files — verbatim.
- Adding Multiple Papers — adapted (same shape as academic).
- Common Mistakes — Protocol B-specific subset. Consider adding: *"Reading only the executive summary"* — problem: institutional reports often bury key numbers in boxes and figure captions, which the executive summary often omits; fix: scan boxes and figures captured by Step 2.
- **Summary evolution principle** paragraph — verbatim from Plan 06.
- Optional: "Working papers from multilateral institutions are usually Protocol A" + "Monographs with chapter-level empirical work are still Protocol B at the document level" — Andrea's lines 244-249. These are routing notes; might fit better in add-paper's Step 0 borderline-case section than here. **Decision: keep in add-paper's Step 0** (where the routing happens). Don't duplicate.

### Per-protocol skill provenance frontmatter

Each per-protocol skill carries dual provenance just like the dispatcher does:

```yaml
nori_researcher_source: nori-skillsets add-paper v1.0.0 (ported to claude_researcher in 0bbd419, 2026-05-10)
aitaxbid_source: ~/code/AITaxBID/skills/paper_processing.md@e0a736d (2026-05-02)
```

(Same SHA; same Nori upstream. Description differs per protocol.)

The Plan 07 split happens after Plan 06's ship commit `454018f`, so the per-protocol skills' provenance still traces back to `0bbd419` (the original Nori port) and `e0a736d` (Andrea's source). The intermediate `454018f` ship is captured in the convo + commit graph, not in the frontmatter.

### `SKILL_INDEX.md` updates

Three entries in the knowledge-management section (where `add-paper` currently lives):

- `add-paper` — existing entry. Update description: "Triage skill: routes academic-style papers to `paper-processing-academic`, institutional-style reports to `paper-processing-institutional`, non-paper documents to `document-processing` (deferred). Run Step 0 here; the routed per-protocol skill handles Steps 1-6."
- `paper-processing-academic` — new entry. Description: "Protocol A workflow for academic-style papers (research with hypothesis + original data analysis). Usually invoked via `add-paper`'s Step 0 dispatch; can be invoked directly when the protocol is already known."
- `paper-processing-institutional` — new entry. Description: "Protocol B workflow for institutional-style reports (synthesis/policy documents from multilaterals, governments, working groups). Usually invoked via `add-paper`'s Step 0 dispatch; can be invoked directly when the protocol is already known. Step 2 carries institutional-specific extraction rules (preserve acronyms, preserve boxes/figure captions, strip decorative front matter)."

Order within the section: dispatcher first, then alphabetical for the two per-protocol entries (`paper-processing-academic` before `paper-processing-institutional`).

### No back-compat shim

Same principle as Plan 06 D-No-back-compat: alpha users (if any exist by execution time — likely zero) who invoked the old unified add-paper get a different shape now. The dispatcher still handles their existing trigger phrases ("add this paper"); the dispatch hop is transparent because the agent reads the routed skill on the same turn.

Edge case: an agent in the middle of a long-running multi-paper add session at the moment of the upgrade. The next paper triggers a dispatch hop; the agent has to read one more SKILL.md mid-flight. Mechanically fine; no user-visible disruption beyond a brief "reading the routed skill" mention.

### Source SHA verification (do NOT skip)

Re-verify Andrea's `paper_processing.md` is byte-identical to `e0a736d` at execution time:

```bash
git -C ~/code/AITaxBID diff --stat e0a736d HEAD -- skills/paper_processing.md
```

Empty output = no drift; proceed. If non-empty: surface to the user before continuing. The Step 2 institutional enrichment relies on Andrea's source being unchanged; new content there might affect the port.

---

## Pre-flight reads (do FIRST, before any edits)

1. **`STATUS.md`** (repo root) — current state, recent sessions, Plan 06 ship entry, this plan's place in the sequence.
2. **`docs/plans/06_w31_addpaper_synthesis.md`** — the unified add-paper that Plan 07 splits. The current `template/skills/add-paper/SKILL.md` is Plan 06's deliverable; read Plan 06 to understand the design constraints that landed there (dual provenance, Tier C schema split, document-processing pointer placement, etc.).
3. **`docs/plans/07_add_paper_dispatcher_refactor.md`** (this plan) — execution-level spec.
4. **`docs/convos/20260513_plan06_w31_addpaper_synthesis_ship.md`** — the originating convo, especially the "Post-ship discussion" section that captures Dan's architectural pivot reasoning.
5. **Source files (read in full):**
   - `~/code/AITaxBID/skills/paper_processing.md` (320 lines, SHA `e0a736d`) — Andrea's source. Pay particular attention to lines 192-197 (Step 2B institutional extraction rules — the true scope addition for Plan 07).
   - `template/skills/add-paper/SKILL.md` (~281 lines as shipped in `454018f`) — the source of the split. Read carefully so you know exactly what content moves where.
6. **Files you'll also edit (skim first):**
   - `template/skills/SKILL_INDEX.md` (locate the knowledge-management section).

**Pre-flight check (after reads, before edits):**

```bash
git status --short  # working tree should be clean except for plan 07 itself (already on main)
git -C ~/code/AITaxBID rev-parse HEAD  # capture for the convo summary later
```

---

## Tasks

Sequence matters: D1 and D2 create the new files first (so D3's dispatch instructions point at real files). D3 strips down add-paper. D4 updates SKILL_INDEX.

### D1 — Create `template/skills/paper-processing-academic/SKILL.md`

Create new file. Content: lift the Protocol A subset of current `add-paper/SKILL.md` per the "What moves to `paper-processing-academic/SKILL.md`" section above.

Specific extraction targets from current add-paper:

- Frontmatter: copy verbatim; revise description to "Protocol A workflow for academic-style papers — rename → extract → index → dual-protocol summary (Protocol A shape) → BibTeX → stage. Triage by `add-paper` Step 0 routes here." Keep both `nori_researcher_source` and `aitaxbid_source`.
- Runtime detection block: lines 6-26 verbatim copy.
- `<required>` TodoWrite block: rewrite to 5 entries (1. Obtain PDF / 2. Extract text / 3. Add to PAPER_INDEX / 4. Read paper + write Protocol A summary / 5. Update BibTeX if BIB_FILE defined / 6. Stage). Renumber from 1, not from 0 — the dispatcher's Step 0 is already complete by the time this skill runs.
- Drop the `## Scope` section (lives in dispatcher).
- New `# Adding an Academic Paper` H1 + announce-at-start line.
- New preamble: *"This skill handles the Protocol A workflow for academic-style papers. Triage to Protocol A was already done by `add-paper` Step 0 — if you're reading this skill directly without going through `add-paper`, confirm the document is academic-style before proceeding (abstract present, research question/hypothesis, original empirical or theoretical contribution from data the authors analyzed)."*
- New schema pointer: *"Configuration keys (`PROJECT_QUESTION`, `CONDITIONAL_SECTION`, `BIB_FILE`, `PAPERS_INDEX`, `paper_summaries.structure`) live in the research repo's `STATUS.md` under `## Project parameters`. Filename format keys (`paper_naming.academic_format`) live in the user's `personal_info.md`. See `add-paper/SKILL.md` Scope section for full schema details."*
- Steps 1-6: lift the Protocol A branch of each step from current add-paper. Drop Protocol B paragraphs entirely. Specifically, in Step 1 keep only the academic filename rule (not the institutional one); in Step 4 keep only the Protocol A summary block (not Protocol B); in Step 5 keep only `@article` / `@unpublished` (not `@techreport` etc.).
- Summary evolution principle paragraph: verbatim from Plan 06.
- Common Mistakes: Protocol-A-relevant subset (Writing summaries from abstract only / Adding numbers without context / Forgetting to update PAPER_INDEX when updating PAPER_SUMMARIES). Drop the dispatcher-level mistakes.
- Adding Multiple Papers: adapted text (mention dispatcher Step 0 in the per-paper iteration).

Target length: ~170-200 lines.

### D2 — Create `template/skills/paper-processing-institutional/SKILL.md`

Create new file. Structure parallels D1 but for Protocol B, with the Step 2 institutional enrichment.

Specific extraction targets:

- Frontmatter: dual provenance + description revised to "Protocol B workflow for institutional-style reports — rename → extract (institutional rules: preserve acronyms / boxes / figure captions) → index → dual-protocol summary (Protocol B shape) → BibTeX → stage. Triage by `add-paper` Step 0 routes here."
- Runtime detection: verbatim copy.
- TodoWrite block: 5-6 entries paralleling academic.
- `# Adding an Institutional Report` H1 + announce-at-start line.
- Preamble parallels academic; confirm institutional-style if invoked directly (no abstract, no own hypothesis, synthesis/position document).
- Schema pointer (same as academic, except mention `paper_naming.institutional_format` instead of academic format).
- Step 1: Protocol B filename only. Include multi-institution co-publication rule + working-group acronym rule + multi-institution naming-ambiguity ask-user rule (from current add-paper).
- **Step 2 (institutional enrichment — the true scope addition):**
  - Standard extraction logic (pdftotext / pymupdf / Read fallback) — copy from current add-paper Step 2.
  - **NEW:** insert after the standard extraction logic, before "Verify the extraction is reasonable":
    ```markdown
    **Institutional reports often have heavy front matter** (foreword, acknowledgments, list of acronyms, list of figures and boxes). Three specific rules apply:

    - **Preserve the acronym list verbatim.** Institutional acronyms (TADAT, ISORA, RA-GAP, PIAAC, etc.) are reference material for downstream work. The list usually appears in the report's front matter; keep it intact in the extracted text.
    - **Preserve boxes and figure captions with their key data.** These often carry the report's quotable findings — numbers and statements that the executive summary omits. Capture the box/figure caption text and any tables it contains.
    - **Strip decorative front matter** (forewords, dedications) unless they contain substantive framing. The line is judgment-based: if the foreword contains a thesis statement or policy position the report is building on, keep it; if it's pure ceremony, drop it.
    ```
- Step 3: Add to PAPER_INDEX. Optional addition (Andrea's "Outlet" column guidance, paper_processing.md lines 222-224): describe document type rather than journal — IMF G20 background note, World Bank Policy Research Working Paper, OECD policy paper, etc. Worth surfacing; small addition.
- Step 4: Protocol B summary template only. Verbatim from current add-paper's Protocol B block.
- Step 5: `@techreport` / `@book` / `@inbook` only. Drop `@article` paragraphs.
- Step 6: Stage. Verbatim.
- Summary evolution principle: verbatim from Plan 06.
- Common Mistakes: Protocol-B-relevant subset. Add: *"Reading only the executive summary"* — problem: institutional reports often bury key numbers in boxes and figure captions, which the executive summary omits; fix: scan boxes and figures captured by Step 2's preserve-boxes rule.
- Adding Multiple Papers: adapted.

Target length: ~190-220 lines.

### D3 — Refactor `template/skills/add-paper/SKILL.md` into the dispatcher

Rewrite (not edit-in-place — the structural change is too large for line-range edits to be clean).

Final structure per the "What stays in `add-paper`" section. Target length: ~80-100 lines.

Key elements:

- Frontmatter unchanged on `name`/provenance; description revised: "Triage skill: routes academic-style papers to `paper-processing-academic`, institutional-style reports to `paper-processing-institutional`, non-paper documents to `document-processing` (deferred). Step 0 triage runs here; the routed per-protocol skill handles Steps 1-6."
- Runtime detection block: verbatim from current.
- TodoWrite block: 2 entries.
- Scope section: revised to enumerate the three dispatch targets. The "Where config keys live" sub-note stays (general-purpose; per-protocol skills reference back to it).
- `# Adding a Paper` H1 + revised announce-at-start.
- `## Step 0: Triage` — content unchanged from Plan 06 (three questions, two-or-more rule, borderline cases including the multilateral-working-papers / monograph-empirical-chapters guidance from Andrea's lines 244-249, Step-differs table).
- Dispatch instruction at end of Step 0 (per "Dispatch mechanism" decision above).
- `# Common Mistakes` — dispatcher-level only (Forgetting Step 0 triage / Reading keys from the wrong file / Trying to do the full workflow in `add-paper`).

Delete everything from current Step 1 through Step 6, plus `# Adding Multiple Papers` (lives in per-protocol skills now), plus the protocol-content-specific Common Mistakes.

### D4 — Update `template/skills/SKILL_INDEX.md`

Locate the knowledge-management section. Update the existing `add-paper` entry's description (now describes triage role). Add two new entries in alphabetical order after `add-paper`:

- `paper-processing-academic` — entry per "SKILL_INDEX.md updates" section above.
- `paper-processing-institutional` — entry per same section.

If the section ordering doesn't naturally put these after `add-paper`, slot them in by their own alphabetical position. Just make sure they're discoverable.

---

## Verification & sanity checks (do BEFORE committing)

After all edits, run:

```bash
# 1. Verify source SHA hasn't drifted
git -C ~/code/AITaxBID diff --stat e0a736d HEAD -- skills/paper_processing.md
# expect empty

# 2. All three SKILL.md files have dual provenance
for f in template/skills/add-paper/SKILL.md \
         template/skills/paper-processing-academic/SKILL.md \
         template/skills/paper-processing-institutional/SKILL.md; do
  echo "--- $f ---"
  head -10 "$f" | grep -E 'nori_researcher_source|aitaxbid_source'
done
# expect both keys present in all three files

# 3. add-paper no longer contains Step 1-6 content (dispatcher only)
grep -E '^## Step [1-6]' template/skills/add-paper/SKILL.md
# expect no matches (only Step 0 should remain)

# 4. paper-processing-academic contains Protocol A content, no Protocol B
grep -c 'Protocol B\|@techreport\|institutional_format' template/skills/paper-processing-academic/SKILL.md
# expect 0 (Protocol B references are not in the academic file)

# 5. paper-processing-institutional contains Protocol B content, no Protocol A
grep -c '@article\|academic_format\|Protocol A' template/skills/paper-processing-institutional/SKILL.md
# expect 0 (Protocol A references are not in the institutional file)

# 6. Institutional Step 2 enrichment landed (Andrea's three rules)
grep -E 'acronym list verbatim|boxes and figure captions|decorative front matter' \
  template/skills/paper-processing-institutional/SKILL.md
# expect 3 matches (one per rule)

# 7. Cross-reference partitioning still clean across all three files
for f in template/skills/add-paper/SKILL.md \
         template/skills/paper-processing-academic/SKILL.md \
         template/skills/paper-processing-institutional/SKILL.md; do
  echo "--- $f personal_info.md mentions ---"
  grep -n 'personal_info.md' "$f"
  echo "--- $f STATUS.md mentions ---"
  grep -n 'STATUS.md' "$f"
done
# expect personal_info.md only pairs with paper_naming.*
# expect STATUS.md only pairs with PROJECT_QUESTION / CONDITIONAL_SECTION / BIB_FILE / PAPERS_INDEX / paper_summaries.structure

# 8. SKILL_INDEX has three correctly-ordered entries
grep -E 'add-paper|paper-processing-academic|paper-processing-institutional' \
  template/skills/SKILL_INDEX.md
# expect all three; order: add-paper first (dispatcher entry point), then per-protocol entries

# 9. Dispatch instruction landed in add-paper
grep -E 'paper-processing-academic|paper-processing-institutional' template/skills/add-paper/SKILL.md
# expect matches in the Dispatch block at end of Step 0

# 10. No orphaned "Step 1A" / "Step 2A" / etc. (Andrea's source convention) leaked in
grep -E 'Step [1-6][AB]' template/skills/add-paper/SKILL.md \
  template/skills/paper-processing-academic/SKILL.md \
  template/skills/paper-processing-institutional/SKILL.md
# expect no matches — per-protocol files renumber from 1, dispatcher only has Step 0
```

If any check fails, fix before committing.

---

## Commit strategy

Single ship commit per the Plan 06 pattern. Suggested message:

```
plan 07 ship: add-paper dispatcher refactor

Splits the unified dual-protocol add-paper (shipped 454018f in Plan 06)
into a thin triage/dispatcher plus two per-protocol target skills, per
the architectural pivot captured in convos/20260513_plan06_w31_addpaper
_synthesis_ship.md "Post-ship discussion".

- template/skills/add-paper/SKILL.md — refactored to dispatcher.
  Step 0 triage + dispatch instruction + scope + "where config keys
  live" note + dispatcher-level common mistakes. ~80 lines (from ~281).

- template/skills/paper-processing-academic/SKILL.md — new file.
  Protocol A workflow lifted from old unified add-paper, scoped to
  academic-style papers. Independent of dispatcher (invocable directly
  when protocol is known). ~180 lines.

- template/skills/paper-processing-institutional/SKILL.md — new file.
  Protocol B workflow lifted from old unified add-paper PLUS Andrea's
  institutional Step 2 rules that Plan 06 left out (preserve acronym
  list verbatim, preserve boxes and figure captions with key data,
  strip decorative front matter). Optional Andrea-line-222-224 "Outlet"
  column guidance also picked up. ~200 lines.

- template/skills/SKILL_INDEX.md — add-paper description revised
  (triage role); two new entries for the per-protocol skills.

Architecture: add-paper's Step 0 triages, then instructs the agent
to read the routed per-protocol skill and follow from Step 1. Lazy-
load pattern matches the existing on-demand fetch model. Per-protocol
skills are independently invokable for sophisticated users.

Future Wave 5 document-processing slots in as the third dispatch
target (non-paper documents); dispatcher's Step 0 already points at
it; the skill itself stays deferred per Plan 02.

Schema split (Plan 06 Tier C Option C) preserved unchanged: per-user
paper_naming.* in personal_info.md; per-project keys in STATUS.md
## Project parameters. Per-protocol skills each carry a back-pointer
to add-paper's Scope section for the full schema details.

Sources verified byte-identical to scoping SHA e0a736d at commit time.
```

Push to origin after committing.

### Post-ship actions

1. **Update STATUS.md** with a Plan 07 ship entry in "Recent sessions". Update the "Plans" list to mark Plan 07 shipped.
2. **Update the dispatcher's "Where config keys live" Scope section** if any per-protocol skill references back to it — verify the back-pointer text in each per-protocol skill matches the actual heading name in the dispatcher.
3. **Run finish-convo** at end of session — create a new convo file, update STATUS.md, commit + push the docs. Wrap commit is separate from the Plan 07 ship commit so the ship commit is bisectable on its own.
4. **No issue to close** — Plan 07 is self-contained (no tracking issue was filed).

---

## What this plan deliberately does NOT cover

- **`document-processing` (Wave 5) port itself.** The dispatcher's Step 0 points at it as the off-route target, but the skill stays deferred per Plan 02. Port in a separate plan when scheduled.
- **`per-file` summary code path.** Still forward-compat-only; the warning + fallback paragraph survives the split intact in both per-protocol skills (no behavior change).
- **issue #4 (add-paper scaling discipline).** Still sequenced after ~5 papers of real user data; orthogonal to the dispatcher refactor.
- **issue #5 (style-profile creation meta-skill).** Andrea-assigned; independent of Plan 07; will land separately if/when Andrea drafts.
- **First real beta session.** Plan 07's architectural improvement is independent of empirical validation. Beta-test happens whenever it happens; Plan 07 ships clean architecture in the meantime.
- **Wave 0 (provenance + sync infrastructure).** Stays deferred until drift becomes a real concern.
- **Renaming `add-paper` to something more descriptive of its dispatcher role.** Considered (e.g., `process-paper`); rejected to preserve the trigger phrase users already learned in Plan 06.

---

## Open questions (for the implementing agent to raise if hit)

- **Independent-invocation discoverability.** Should the per-protocol skills be listed in SKILL_INDEX with a stronger "usually invoked via dispatcher" note, or trust the SKILL_INDEX descriptions plus the per-protocol skill preambles? **Recommendation:** trust the descriptions; don't add a separate "dispatched-only" tag. If beta data shows users frequently invoke per-protocol skills directly by mistake, add a tag later.
- **SKILL_INDEX section placement.** All three skills logically belong to knowledge-management. Confirm there's no better section. **Recommendation:** keep all three in knowledge-management together.
- **What if the source SHA has drifted?** If Andrea pushes to AITaxBID between Plan 06's ship and Plan 07's execution and the changes affect `paper_processing.md` lines 192-197 (the Step 2B rules), surface to the user before proceeding. The institutional enrichment relies on those specific rules being current.
- **TodoWrite renumbering.** Per-protocol skills should number from 1, not 0. The dispatcher's TodoWrite block ends with a step that says "Load and follow the routed skill" — when the agent reads the routed skill, its TodoWrite block adds 5-6 more entries. **Recommendation:** treat the renumbering as agent-side concern; don't try to coordinate numbering across two files. Each skill's TodoWrite block is locally consistent.
- **"Reading only the executive summary" Common Mistake in paper-processing-institutional** — is this worth adding given that the new Step 2 rules already address it implicitly? **Recommendation:** include it. The Common Mistake makes the connection explicit (institutional reports → key numbers buried in boxes → executive summary insufficient) and surfaces a failure mode that experience suggests is common.
- **Existing alpha users' STATUS.md or personal_info.md.** No backfill needed — Plan 07 doesn't change the schema. The schema-split from Plan 06 stands.

---

## Estimated effort

~45-60 minutes for a fresh agent who reads pre-flight materials and follows the deliverable-by-deliverable spec. The work is mechanical (split one file into three, add Andrea's Step 2 rules to one of the three), not exploratory. Two new SKILL.md files at ~180-200 lines each; one ~80-line dispatcher; SKILL_INDEX entries. Verification (10 checks) + commit at the end adds ~10 min.

Below the budget of Plan 06's 45-60 min estimate (which involved interpreting Andrea's source for the first time and resolving the Tier C schema split). Plan 07 is execution against fixed content; lower cognitive load.
