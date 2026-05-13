# claude_researcher — AITaxBID Follow-ups

**Goal:** Consolidate audit-derived work that remained open after Plan 02 — Wave 4 ports, W3.1 retrofit, Tier C decision. Plan 02 covered the original scoping on 2026-05-09; this plan re-scopes what's open given drift since then and resolves the architectural decisions Wave 4 was blocked on.

**Status:** Fleshed out 2026-05-13 (Claude Code session — preferred surface for Wave 4 ports because Andrea's source files are filesystem-only; see "Source-access from WebUI" under Open questions). All architectural decisions resolved; ready for execution.

**Parent plans:**

- [`02_skill_ports.md`](02_skill_ports.md) — original wave-based plan; Waves 1–3 shipped, Wave 4 still open, W3.1 dropped at Wave 3 ship.
- [`04_sandbox_tooling_and_companion_cleanups.md`](04_sandbox_tooling_and_companion_cleanups.md) — verified pandoc 3.1.3 / python-docx 1.2.0 / git 2.43.0 on 2026-05-11; W4.0 here just spot-checks pandoc.

**Originating convos:**

- [`20260509_aitaxbid_skills_audit.md`](../convos/20260509_aitaxbid_skills_audit.md) — original audit findings (also on main via PR #1 → `6397c33`)
- [`20260512_audit_followup_and_plan05.md`](../convos/20260512_audit_followup_and_plan05.md) — audit follow-up reconciliation + Plan 05 scaffolding
- [`20260513_plan05_flesh_out.md`](../convos/20260513_plan05_flesh_out.md) — flesh-out session (this plan's current shape)

**Confidence:** Medium-high. Each task has a concrete deliverable list, dependencies are mapped, and the two architectural decisions (W4.2 diff mechanism, Tier C placement) have reasoned recommendations. Remaining uncertainty is in port-time details (SHA drift, naming finalization) rather than plan structure.

**Branch:** main (build work, not exploration).

**Tracking issues:**

- [#3 — W3.1 fold-in (paper_processing → add-paper)](https://github.com/danparshall/claude_researcher/issues/3)
- [#4 — add-paper: scaling discipline](https://github.com/danparshall/claude_researcher/issues/4) — companion follow-on, sequenced after W3.1

---

## Principles for this plan

### Defer to Andrea on methodological details

For skills that are Andrea's, or that overlap strongly with hers, defer to Andrea on methodological decisions. She's been doing pure-GitHub web-UI work for several years; her conventions are field-tested in exactly the audience claude_researcher targets.

Examples of methodological details to defer:

- The `[bracketed comments]` convention in BranchWorkflow — don't substitute another markup
- Light-vs-heavy reviewer distinction (typos/accents silent vs. terminology/voice flagged)
- Two-protocol structure for writing (Protocol 1 Reading/Thinking, Protocol 2 Drafting)
- Step 0 academic-vs-institutional triage questions in paper_processing
- Protocol B summary structure for institutional reports

Adapt only where the architecture forces it (REST API instead of local git; on-demand fetch instead of full-kit propagation; sandbox availability instead of local pandoc). Port the methodology intact.

### Naming convention: Nori

Use Nori convention for skill names: **kebab-case directory** + `SKILL.md` inside. claude_researcher will integrate more strongly with Nori going forward; naming consistency is load-bearing.

Examples:

- `template/skills/writing-skill/SKILL.md` (not `writing_skill/SKILL.md` or `writingSkill/SKILL.md`)
- `template/skills/branch-document-review/SKILL.md`

---

## Tasks

### W4.0 — Sandbox tooling spot-check (gate for W4.3)

Cross-checked against [`template/reference/SANDBOX_TOOLING.md`](../../template/reference/SANDBOX_TOOLING.md) on 2026-05-13: the only Wave 4 hard dependency is `pandoc`, which was verified at 3.1.3 on 2026-05-11. Andrea's `BranchWorkflow_Skill.md` makes LaTeX explicitly conditional (*"no regeneration unless Andrea has set up the LaTeX pipeline"*), and `.pptx` regeneration applies only to slide-source projects — neither is on the Wave 4 critical path. `pypandoc` is documented as a fallback in the workaround table and isn't needed while pandoc is present.

**Concrete action:** In the next WebUI session (any chat, not necessarily a port chat), confirm pandoc still reports 3.1.3. If changed, update SANDBOX_TOOLING.md. If unchanged, W4.3 proceeds without further probing.

**Deferred per tooling-protocol cadence (on-discovery only):**

- `pdflatex` / `xelatex` (conditional in Andrea's source)
- `python-pptx` (slide-source projects only)
- `pypandoc` (fallback for pandoc; only relevant if pandoc itself flips to unavailable)

**Status:** Ready — spot-check only. Not blocking W4.1.

### W4.1 — Port Andrea's writing skill (Tier A)

Light-friction port of Andrea's `writing_skill.md`. Pure-thought skill (planning, drafting, revising) — no git/CLI operations, so **no REST-adaptation banner is needed** (unlike Wave 2/3). This makes it more like a Wave 1 SWE carryover in adaptation profile than a Wave 2/3 Researcher skill.

**Source (re-check SHA at port time):**

- Path: `~/code/AITaxBID/skills/writing_skill.md`
- SHA at scoping: `e0a736d` (2026-05-02), 169 lines
- Source-access: filesystem-only — see "Source-access from WebUI" under Open questions. Port runs from Claude Code, not claude.ai WebUI.

**Naming decision (open):**

Andrea's YAML frontmatter names the skill `iterative-writing-workflow`. Plan 05's introduction example uses `writing-skill`. Both are kebab-case. Per the "defer to Andrea" principle, Andrea's own name is the default — it's already kebab-case and more descriptive. The `writing-skill` shorthand survives in Plan 05's example as illustration of the convention, not as a renaming directive. **Recommendation:** use `iterative-writing-workflow`. **Confirm at port time.**

**Transformations needed (minimal):**

1. **Add provenance frontmatter** above Andrea's existing `name`/`description` frontmatter:
   ```yaml
   aitaxbid_source: ~/code/AITaxBID/skills/writing_skill.md@e0a736d (2026-05-02)
   ```
   First Tier-A port establishes the `aitaxbid_source` precedent (Wave 1 carryovers use `nori_swe_source`; Wave 2/3 use `nori_researcher_source`; AITaxBID-derived skills use `aitaxbid_source`).
2. **Rephrase project-config references.** Andrea's source twice mentions "your project's CLAUDE.md" (in "Adapting to your project" under Protocol 1, and "Setting up for a new project" at the bottom). Replace with: *"your project's `RESEARCHER.md`, `STATUS.md`, or equivalent coordination file."* This aligns with the post-Plan-03 rename and acknowledges that claude_researcher splits coordination across two files where AITaxBID had one.
3. **Drop the footer** *"Last updated: April 11, 2026"* — provenance is captured in frontmatter now.
4. **Leave Andrea's content otherwise intact.** Specifically: the two-protocol structure, "answer questions inline and fully," "questions first, actions second," "show before committing," "do NOT search past chats" — all are field-tested methodological choices and align with existing RESEARCHER.md conventions (§5 working conventions, §2e session resumption).

**Compatibility check — no friction expected:**

- "Show before committing" → already in RESEARCHER.md §5 (general principle) and applied scoped here to notes/tracking writes specifically.
- "Do NOT search past chats" → reinforces the existing tracker-not-past-chats discipline.
- "Style profiles" reference (in Protocol 2 setup checklist) — keep, with a one-line addition: *"if you don't have a style-profiles doc, you can create one — ask the agent to draft a versioned `<project>_Style_Profile.md` from a sample of your prior writing."* This makes the reference actionable for users new to the pattern without dragging Andrea's three project-specific profiles into Plan 05's scope (which excludes them by design — see "What this plan deliberately does NOT cover").

**Destination:** `template/skills/iterative-writing-workflow/SKILL.md` (or `template/skills/writing-skill/SKILL.md` if the naming question lands the other way).

**Status:** Ready — execute from Claude Code with filesystem access. ~15–30 min including SKILL_INDEX update.

### W4.2 — Decide diff mechanism for branch-document-review

Andrea's source uses `git diff <creation-commit> <branch-tip>` at Step 4 to isolate Mode 2 direct edits from Mode 1 bracketed comments. For claude_researcher we need a sandbox-compatible substitute. Plan 02 noted "slight preference for Compare API"; this task locks the decision.

**Options reconsidered (now that sandbox `git` 2.43.0 is confirmed available per SANDBOX_TOOLING.md):**

| Option | Mechanism | Round-trips | Architectural fit | Faithful to Andrea |
|---|---|---|---|---|
| A — GitHub Compare API | `GET /repos/{owner}/{repo}/compare/{base}...{head}` returns `files[]` with unified `patch` per file | 1 | Best — REST-first matches existing fetch patterns; no clone state to manage | Medium — unified diff, not direct `git diff` output |
| B — Read-both-and-difflib | Two Contents API fetches (base, branch-tip) + `difflib.unified_diff` locally | 2 | OK — same on-demand-fetch pattern; more flexible parsing | Medium — same diff shape, more code |
| C — `git clone` + `git diff` | Clone the user's research repo at branch-review time; run Andrea's exact `git diff` invocation | 1 (HTTPS clone) | Mixed — most faithful but introduces clone-state management for user repos; cost scales with repo size | High — verbatim |

**Recommendation: Option A (Compare API).**

Reasoning:

- One round-trip, lowest sandbox cost. The Compare response is JSON with `files[].patch` per changed file — directly parseable to identify added/removed/modified lines.
- Matches the architectural commitment (REST-first; no per-skill clone state).
- The "faithful to Andrea" gap is small: Andrea's local `git diff` produces unified diff format, and the Compare API also returns unified diff per file. Parsing logic is the same.
- Option C's clone-state question is non-trivial: clone shallow? clone fresh each invocation? cache across invocations? Not worth answering for a marginal faithfulness gain.

**Loose end the port needs to resolve:** the Compare API caps single-page responses at 300 files. Wave 4 documents are typically single-markdown-file edits, so this is not in scope, but the port spec should mention the cap so a future multi-file extension knows where the cliff is.

**Status:** Recommendation made (Option A). Dan can override at port time. W4.3 assumes Option A for the Step 4 spec below.

### W4.3 — Port Andrea's branch-document-review (Tier A)

Highest-priority port — best fit for the claude.ai web-UI audience because the bracketed-comment substrate works in any GitHub textbox. Andrea's source is already partially REST-aware (Steps 1 and 6 ship REST recipes verbatim); the only real adaptation is Step 4's `git diff` → Compare API.

**Source (re-check SHA at port time):**

- Path: `~/code/AITaxBID/skills/BranchWorkflow_Skill.md`
- SHA at scoping: `e0a736d` (v2.0, 2026-05-02, 178 lines)
- Source-access: filesystem-only — port runs from Claude Code.

**Naming decision:** `branch-document-review` per Plan 05's stub example. Andrea's title ("Branch workflow for collaborative document review") doesn't have a YAML frontmatter `name` field to defer to. Confirmed kebab-case.

**Keep intact (defer-to-Andrea content):**

- `[bracketed comments]` convention — the bracketed-text substrate is the load-bearing methodological choice; do not substitute another markup (e.g. HTML comments, fenced blocks)
- Mode 1 / Mode 2 distinction (bracketed comments vs. direct text edits)
- Comment-classification rules: instruction vs. question vs. ambiguous → ask before acting
- Light-vs-heavy proofreading distinction (typos/accents/punctuation silent; terminology/voice/consistency surfaced)
- Three-section report structure: comment-driven changes / direct edits silent / direct edits flagged
- "Never push edits to `main` while a branch is open for that document" rule
- "Branches accumulate per project" — new branch per edit round, don't reuse
- Pandoc regeneration step for `.docx` companion artifacts (gated on W4.0 — pandoc 3.1.3 confirmed; no further gating needed)
- LaTeX-pipeline path left as Andrea wrote it (conditional)
- `.pptx` regeneration path left as Andrea wrote it (conditional; python-pptx availability not probed per W4.0 trim — if a project hits this path and python-pptx is missing, it's an on-discovery cadence trigger per the tooling protocol)

**Adapt for claude_researcher:**

1. **Step 4 — diff mechanism.** Replace `git diff <creation-commit> <branch-tip>` with the Compare API call locked in W4.2:
   ```bash
   curl -s -H "Authorization: token $TOKEN" \
     "https://api.github.com/repos/$REPO/compare/$BASE_SHA...$BRANCH"
   ```
   Parse the `files[].patch` unified-diff payload to identify Mode 2 direct edits (lines added/removed/modified that don't fall inside `[...]` blocks). Surface the Compare API's 300-file response cap as a one-line note so future multi-file extensions know where the cliff is.
2. **Branch-naming convention.** Andrea uses `<project-slug>-<purpose>-<date>` with `mmm-d` for date (e.g. `marta-oecd-edits-may-1`). claude_researcher convo names use `YYYYMMDD`. **Recommendation:** keep Andrea's format verbatim — branch lifetime is typically short so the year-ambiguity in `mmm-d` rarely bites, and the format is part of her field-tested workflow. **Confirm at port time** if Dan prefers `YYYYMMDD` for cross-convention consistency.
3. **Provenance frontmatter:** `aitaxbid_source: ~/code/AITaxBID/skills/BranchWorkflow_Skill.md@e0a736d (2026-05-02)`.
4. **Drop the footer** *"Last updated: May 2, 2026 — v2.0 (initial version, added in v2.0 from AdmWorkFMM v1.4 work)"* — provenance is in frontmatter now. The version history is Andrea's internal kit detail, not relevant to the ported version.
5. **Strip "Andrea" / "Marta" name references** throughout. Andrea's source addresses her own collaboration with Marta and the RA by name. The port replaces these with role-generic terms: "Andrea" → "the user" or "the reviewer"; "Marta" → "a coworker"; "the RA" → "a colleague." Drop the "Owner: Andrea Lopez-Luzuriaga" line.

**No REST-adaptation banner needed** for the Wave 2/3 style. Andrea's Steps 1 and 6 already ship REST recipes verbatim; Step 4 is the only adaptation and it lives inline. Adding a banner would be redundant.

**Destination:** `template/skills/branch-document-review/SKILL.md`

**Status:** Ready — execute from Claude Code with filesystem access. Sequence after W4.1. Larger than W4.1 (~30–60 min) because of Step 4's diff-parsing logic and the name-stripping pass.

### W3.1 retrofit — Fold AITaxBID synthesis into add-paper

**Tracking:** issue [#3](https://github.com/danparshall/claude_researcher/issues/3).

**Companion (after W3.1):** issue [#4 — add-paper: scaling discipline](https://github.com/danparshall/claude_researcher/issues/4). Covers lookup discipline (grep+offset reading), length guidelines (~10% with 2000-word ceiling), two-stage file structure with migration trigger, multi-repo destination logic, and the "Beyond this summary" affordance. Sequenced after W3.1 — same SKILL.md, but the scaling layer benefits from real user data (~5 papers) before threshold calibration.

Plan 02 Wave 3 shipped `template/skills/add-paper/SKILL.md` with the simpler Nori shape (one filename convention, one summary template, no BibTeX). The fold-in adopts Andrea's dual-protocol structure as a strict superset.

**Sources (re-check SHAs at port time):**

- Andrea: `~/code/AITaxBID/skills/paper_processing.md`, SHA `e0a736d` (2026-05-02, 320 lines)
- Nori-Researcher: existing `template/skills/add-paper/SKILL.md` (already on main; the retrofit target)
- Source-access: filesystem-only on Andrea's side — execute from Claude Code.

**Deliverables (in order of dependency):**

1. **Step 0 triage** — three structural questions (abstract vs. executive summary; research question/hypothesis; new estimates from data); two-or-more rule routes Protocol A vs. Protocol B. Defer to Andrea on the question phrasing.
2. **Filename convention parameterization.** Current SKILL.md hardcodes `AuthorLast_Year__short_description.pdf`. Replace with read-from-config: `paper_naming.academic_format` + `paper_naming.institutional_format` from `personal_info.md`. Defaults:
   - Academic: `Author_shortTitle_year.pdf` (Andrea's Protocol A convention)
   - Institutional: `institution_shortTitle_year.pdf` (Andrea's Protocol B convention)
   - Note: BOOTSTRAP smoke-test path used `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf`. The fold-in either keeps that as a third format option or supersedes it; **decide at port time** based on which conventions users in the wild already have.
3. **Replace Step 4 summary template** with Andrea's dual-protocol (a)/(b)/(c)/(d) shape — Protocol A emphasis (thesis / methodology / conditional / relevance) for academic; Protocol B emphasis (purpose+commissioning / doc-type+frameworks+findings+policy / conditional / position+cross-refs) for institutional.
4. **Add Summary Evolution Principle** as a paragraph: "(a)–(d) is a floor, not a ceiling. Expanded summaries with worked examples, cross-references, and the user's own notes are expected and desirable. Do not trim expanded summaries back to the minimal format."
5. **Add BibTeX step** (new functionality — currently `add-paper` doesn't write BibTeX). Gated on `BIB_FILE` being defined in `personal_info.md`:
   - Protocol A → `@article` / `@unpublished` with cite key matching filename
   - Protocol B → `@techreport` / `@book` / `@inbook` with double-braced institutional author
   - If `BIB_FILE` is unset, skip step silently (no breaking change for users without BibTeX).
6. **Add the `document_processing.md` pointer** for legislation / regulatory docs / consultant deliverables — Andrea routes these to a different skill. claude_researcher hasn't ported `document_processing` yet (Plan 02 Wave 5, deferred), so the pointer is currently aspirational. Leave it in with a "deferred — see Wave 5" note.
7. **Schema extensions, split per Tier C (Option C — STATUS.md project params):**
   - **`personal_info.md` (user-level, all projects):**
     - `paper_naming.academic_format` (required if Protocol A papers ever ingested)
     - `paper_naming.institutional_format` (required if Protocol B papers ever ingested)
   - **STATUS.md "Project parameters" section (per-project):**
     - `PROJECT_QUESTION` (required — feeds Section (d) relevance writing)
     - `CONDITIONAL_SECTION` (optional — defines what Section (c) filters for)
     - `BIB_FILE` (optional — gates Step 5)
     - `PAPERS_INDEX` (optional — defaults to `PAPER_INDEX.md`)
     - `paper_summaries.structure` (optional, default `single-file` — resolves the W3.1 file-structure mismatch)
8. **BOOTSTRAP.md interview update** — Batch 3 paper-naming question expands to ask both academic and institutional formats; offer Andrea's defaults so users can hit Enter. Also collect `PROJECT_QUESTION` here (already roughly captured in the existing topic question — needs a tighter prompt).
9. **Dual provenance frontmatter** — first skill carrying both:
   ```yaml
   nori_researcher_source: <path>@<SHA>
   aitaxbid_source: ~/code/AITaxBID/skills/paper_processing.md@e0a736d (2026-05-02)
   ```
   Sets the precedent for future synthesis ports. Order: Nori-Researcher first (it's the base), AITaxBID second (it's the augmentation).

**Defer to Andrea on (unmodified content):**

- Three triage questions and the two-or-more rule
- Protocol A summary section emphasis (thesis / data+sample+identification / etc.)
- Protocol B summary section emphasis (commissioning context / document-type framework / etc.)
- Borderline-case guidance in Step 0 (multilateral working papers usually A, monographs usually B, etc.)
- Cite-key convention (`Author_shortTitle_year` ↔ filename)
- "Working papers from multilateral institutions are usually Protocol A" guidance

**Out of scope (flagged but not addressed in W3.1):**

- **Implementing the per-file branch.** Tier C (Option C) gives us the config slot (`paper_summaries.structure: single-file | per-file` in STATUS.md project parameters) and W3.1 declares `single-file` as the default to preserve current behavior. But the actual code path that *handles* the `per-file` value (writing to `papers/summaries/SUMMARY_*.md` instead of appending to `PAPER_SUMMARIES.md`) is not in W3.1's scope — defer to a follow-up once at least one user actually wants the per-file structure. Until then the config knob exists but only `single-file` is exercised.
- **Claude status / User status framework** (Andrea's Step 6A/6B) — adds a reading-recommendation label per paper. Not in Plan 05 stub's deliverable list; could be a separate follow-up if Dan wants it.
- **Lookup Protocol** (Andrea's three-tier index → summary → text fallback) — already implicit in Nori workflow but not formalized; minor.

**Destination:** existing `template/skills/add-paper/SKILL.md` (in-place edit, not a new file).

**Status:** Ready — execute from Claude Code with filesystem access. Estimated ~45–60 min including the personal_info.md and BOOTSTRAP.md updates. Sequence: independent of Wave 4 — can run before, after, or interleaved.

### Tier C decision — "Generic-skill" block format

**Pattern:** Andrea's `CLAUDE_TEMPLATE.md` introduces each skill with a markdown block linking the upstream skill spec to project-specific parameters:

```markdown
## Paper Processing Workflow

> **Generic skill:** `skills/paper_processing.md`. The section below is the
> project-specific implementation — it adds parameters and any conventions
> that go beyond the generic skill.

[per-project parameters here]
```

This separates portable content (the skill spec) from per-project parameters (PROJECT_QUESTION, BIB_FILE, summary file structure, etc.). The question is *where* in claude_researcher's architecture these parameters live.

**Surface options (re-stated with full reasoning):**

| Option | Surface | Pros | Cons |
|---|---|---|---|
| A | In each `SKILL.md` | Localized; spec + params travel together | Breaks upstream-shared model; most skills have no params; sync infrastructure (Wave 0) becomes harder |
| B | New `PROJECT_PARAMS.md` in research repo | Clean separation of concerns; scales if params proliferate | New file → BOOTSTRAP scaffold, RESEARCHER.md fetch update, new schema doc, more for users to learn |
| C | Extend `STATUS.md` role | No new file; STATUS.md already fetched at session start; absorbs the addition cheaply | Mixes "live state" with "static config"; STATUS.md grows |
| D | Skip | Simplest; no architecture change | Doesn't solve the problem — users re-explain PROJECT_QUESTION etc. every fresh chat (the §1.5 tracker-not-past-chats failure mode) |

**Decision: Option C — extend STATUS.md.**

**Reasoning (at full strength):**

1. Project params are *config*, not *state*. They change rarely. A dedicated "Project parameters" section at the top of STATUS.md absorbs Andrea's full set (~6 fields) without making the doc unwieldy.
2. Option B's separation-of-concerns upside is mostly aesthetic at this scale. The two-file overhead (BOOTSTRAP, RESEARCHER.md, schema doc) is real; one-file extension is cheap.
3. Option A's localization benefit is undercut by the upstream-shared cost. Most SKILL.md files have zero project params (`brainstorming`, `systematic-debugging`, `test-driven-development`, etc.) — putting an empty params section in every one is anti-pattern.
4. Option D leaves users re-explaining context to fresh agents indefinitely, which is exactly Andrea's tracker-not-past-chats lesson.

**Re-evaluation trigger for Option B:** if project parameters proliferate beyond ~15 fields per project, the STATUS.md extension would become unwieldy and a separate `PROJECT_PARAMS.md` file would scale better. Current expectation: ~6 fields (PROJECT_QUESTION, CONDITIONAL_SECTION, BIB_FILE, PAPERS_INDEX, two paper_naming formats); revisit if we discover ~3x that volume in the wild.

**Personal info vs. project parameters — explicit split (was muddled in the W3.1 stub):**

| Lives in `basic_config/personal_info.md` (user-level, all projects) | Lives in `STATUS.md` Project parameters (per-project) |
|---|---|
| `paper_naming.academic_format` (user's preferred convention) | `PROJECT_QUESTION` (this project's research question) |
| `paper_naming.institutional_format` (user's preferred convention) | `CONDITIONAL_SECTION` (this project's relevance filter) |
| Git fluency, role, tier dial, etc. (existing fields) | `BIB_FILE` (this project's BibTeX filename, if any) |
| | `PAPERS_INDEX` (this project's index filename, default `PAPER_INDEX.md`) |
| | `paper_summaries.structure` (single-file vs. per-file — resolves the W3.1 file-structure mismatch) |

**Concrete STATUS.md addition** (proposed format):

```markdown
## Project parameters

Per-project configuration the skills read at runtime. Update only when the project's scope or conventions change.

- `PROJECT_QUESTION`: <one-sentence research question>
- `CONDITIONAL_SECTION`: <relevance filter, or "unset">
- `BIB_FILE`: <filename, or "unset">
- `PAPERS_INDEX`: <filename, default `PAPER_INDEX.md`>
- `paper_summaries.structure`: `single-file` | `per-file` (default: `single-file`)
```

**Knock-on edits required after Tier C lands:**

1. **W3.1 schema update** — move PROJECT_QUESTION / CONDITIONAL_SECTION / BIB_FILE / PAPERS_INDEX out of personal_info.md and into the STATUS.md project-parameters section. Keep paper_naming formats in personal_info.md (user-level).
2. **`init-research-repo` SKILL.md** — seed the "Project parameters" section in new STATUS.md files.
3. **BOOTSTRAP.md** — the interview's Batch 3 paper-naming step writes the user-level formats to personal_info.md; a new (or modified) step prompts for PROJECT_QUESTION and writes it to STATUS.md project parameters.
4. **RESEARCHER.md §2** — note that STATUS.md now also carries project parameters; reading STATUS.md is already part of session-start, so no additional fetch.
5. **`add-paper` SKILL.md** — the W3.1 fold-in reads project parameters from STATUS.md (not personal_info.md as the stub initially said).

**Status:** Recommendation made — Option C. Dan can override before W3.1 executes. Knock-on edits scheduled with W3.1 execution (they bundle naturally with the schema work).

### W4.4 — Update `SKILL_INDEX.md`

Add a "Writing & document workflow" group between knowledge-management and working-style. Entries for `writing-skill` and `branch-document-review`.

**Status:** Stub.

### W4.5 — Ship commit

Per Wave 4 ship criterion (Plan 02): beta users have access to the writing workflow and the document-review pattern that fits the claude.ai web-UI audience.

**Status:** Stub.

---

## Open questions

- ~~**Source-access from WebUI**~~ — **partially resolved 2026-05-13.** Wave 4 ports (W4.1, W4.3, W3.1) execute from Claude Code with filesystem access to `~/code/AITaxBID/skills/`. Andrea's source SHA at scoping: `e0a736d` (2026-05-02). The WebUI source-access question remains open for any future port that has to run from WebUI; revisit if/when that happens.
- Andrea's AITaxBID kit may have evolved since 2026-05-09; re-check SHAs at port time. SHA at scoping: `e0a736d` (2026-05-02, applies to `writing_skill.md`, `BranchWorkflow_Skill.md`, `paper_processing.md`). If Andrea's `SkillPropagation` repo is accessible, prefer that as canonical source.
- ~~Sandbox tooling availability (pandoc, LaTeX)~~ — **resolved 2026-05-13 via W4.0.** pandoc 3.1.3 was verified 2026-05-11; LaTeX + pptx + pypandoc deferred to on-discovery cadence. W4.3 ships without LaTeX/pptx hard dependencies.
- ~~Tier C architectural placement~~ — **resolved 2026-05-13.** Option C (extend STATUS.md role) locked. See "Tier C decision" task above for reasoning + knock-on edits.
- After Plan 05 ships, should the `aitaxbid-skills-audit` branch be archived? The audit doc itself remains valuable as a reference; the branch is stale (14+ commits behind main as of this plan creation).
- Light-vs-heavy distinction was identified as a Tier B pattern in the audit but is only relevant if a reviewer/editor skill exists — i.e., it lands naturally with W4.3 (`branch-document-review`). No separate task needed.
- **Branch-naming format for `branch-document-review`** — Andrea's `mmm-d` format vs. claude_researcher's `YYYYMMDD` elsewhere. W4.3 defers to Andrea per principle; confirm or override at port time.
- **Default filename convention for `add-paper`** — three formats in play (Nori, BOOTSTRAP smoke-test, Andrea). W3.1 parameterizes via personal_info.md but doesn't pick a default; decide at port time.

## What this plan deliberately does NOT cover

- **`document_processing` port** (Plan 02 Wave 5, deferred by design). Requires full read of Andrea's 320-line source first; not on beta-user critical path. Re-prioritize in a future plan when ready.
- **`init-research-repo`** — already shipped per `template/skills/init-research-repo/SKILL.md`; no follow-up needed here.
- **Andrea's three style profiles** (`Andrea_Writing_Style_Profile.md`, `Andrea_FMM_Institutional_Style_Profile.md`, `Marta_Writing_Voice_Profile.md`) — content is person/institution-specific; the *pattern* (versioned voice profiles, applied on explicit request only, with `_PLAIN.md` backups) is portable as a meta-skill but isn't on the beta-user critical path.
- **Andrea's Parts C/D/E** (propagation infra, portability evaluation, improvement artifacts) — designed for full-kit-everywhere; doesn't fit on-demand fetch. Exception: Part D's portability framework could ship as a standalone skill if/when claude_researcher opens to community contributions.
