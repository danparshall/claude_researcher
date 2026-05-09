# claude_researcher — AITaxBID skills audit

**Date:** 2026-05-09
**Repo:** claude_researcher
**Branch:** `aitaxbid-skills-audit` (worktree, branched from main at `c644479`)
**Plan:** [docs/plans/01_initial_build.md](../plans/01_initial_build.md) — informs Phases 4 (CLAUDE.md), 5 (skills), 6 (scripts). No new plan tasks created here; this is research output for Dan to act on selectively.
**Source repo audited:** `/Users/dan/code/AITaxBID` — Andrea Lopez-Luzuriaga's IADB FMM white paper repo. The skills kit there is **one version behind Andrea's canonical master** (its v2.0 CHANGELOG entry says "AITaxBID needs Phase 3 propagation post-v2.0 to catch up"). Andrea maintains canonical state in a separate `SkillPropagation` repo we did not access. Treat findings here as a snapshot of Andrea's working kit, not her latest design.

## Summary

Andrea's `skills/` directory is a sophisticated, versioned, propagatable kit (14 skill `.md` files + assets + meta-files, with `CHANGELOG.md`, `LastSkillUpdate/` snapshot, and a `PROJECT_SETUP.md` that defines five lifecycle parts: A new project / B existing repo integration / C update propagation / D portability evaluation / E improvement artifacts). Three categories of value for `claude_researcher`:

1. **Two skills directly portable to `template/skills/` with light edits** — `writing_skill.md` (two-protocol thinking-vs-drafting workflow) and `BranchWorkflow_Skill.md` (branch-based document review with bracketed inline comments — this one is *especially* aimed at the claude.ai-only audience because the comment substrate is the GitHub web UI textbox). Two more — `paper_processing.md` (with its Step 0 Protocol-A/Protocol-B triage) and `document_processing.md` (legislation / institutional reports — Nori has no analog) — are portable but require comparison/synthesis with Nori's `add-paper` before borrowing.
2. **Patterns to encode in `template/CLAUDE.md` directly, not as separate skills** — show-before-committing as a universal rule; tracker-is-source-of-truth-not-past-chats (claude.ai-specific discipline); 3+-repetition codification rule; Parking Lot section for undecided items; "group 2-3 questions, don't fire all at once" interview discipline; "do not infer — ask"; light-fixes-silent / heavy-issues-flagged judgment encoding.
3. **One template-structure pattern worth adopting in Phase 4's CLAUDE.md** — Andrea's per-skill section format `> **Generic skill:** skills/X.md. The section below is the project-specific implementation — it adds parameters and any conventions that go beyond the generic skill.` This cleanly separates portable content from per-project parameters.

Dan's read on Andrea's full-kit-everywhere propagation model (v2.0.1): on-demand fetching is the right choice for `claude_researcher` because Dan expects to maintain centrally for many users; users wanting a frozen version can clone. So Andrea's Parts C/D/E (propagation / portability / improvement artifacts) are *not* directly applicable as kit-management infrastructure — but Part D's portability framework is still valuable as a standalone skill for evaluating community-contributed improvements.

## Work Done

- Read Andrea's `README.md` and toplevel `skills/` directory inventory.
- Read full content of: `PROJECT_SETUP.md` (Parts A–E), `writing_skill.md`, `paper_processing.md`, `BranchWorkflow_Skill.md`, `CLAUDE_TEMPLATE.md`, `email_drafting.md`. Skimmed `CHANGELOG.md` (v2.0.1, v2.0, v1.3.1 entries).
- Did NOT read: `document_processing.md`, `academic_paper_latex_skill.md`, `academic_slides_skill.md`, `fmm_coordination_slides_skill.md`, `fmm_docx_formatting_skill.md`, the three style profiles (Andrea_Writing, Andrea_FMM, Marta_Voice), `word_preamble.js`, `latex_preamble.tex`, or any binary assets. The first two are next-priority reads if porting; the rest are FMM/IDB-specific and explicitly recommended NOT to port directly (the *patterns* — versioned voice profiles applied on explicit request only, with `_PLAIN.md` backups — are portable; the content is not).

## Decisions Made

- **On-demand fetch model is right for `claude_researcher`** (Dan's call, recorded here for the record). Andrea's full-kit-everywhere model (v2.0.1) was reached after she explicitly tested opt-in for a month and abandoned it. Different ergonomics: Andrea's users want a stable per-project snapshot they own; `claude_researcher` expects centralized maintenance for many non-CLI users, where always-fresh wins because most users won't upgrade explicitly. Users wanting a frozen version fork the public repo. So Andrea's Parts C/D/E are not direct inputs.
- **Audit work lives on `aitaxbid-skills-audit` branch** in a worktree, separate from Phases 4-6 active development on main. `.worktrees/` directory and `.gitignore` line added in setup; one-time scaffolding for this repo. No `data/` to symlink, no project setup files, no test suite — the worktree is essentially just an isolated checkout for this convo.
- **No plan tasks created from this audit.** The recommendations are advisory inputs to Phases 4-6 already specified in `docs/plans/01_initial_build.md`. Dan decides which to actually pull in.

## Findings — directly portable skills (Tier A)

### `writing_skill.md` — two-protocol writing workflow

**Source:** `~/code/AITaxBID/skills/writing_skill.md` (last updated 2026-04-11). Has YAML frontmatter (`name: iterative-writing-workflow`, multi-paragraph description). 169 lines.

**Protocol 1 (Reading / Thinking / Note-Taking):** fully interactive, user-driven pace. Claude does not move ahead without explicit go-ahead. Key sub-rules: present material in side panel rather than inline chat dump; answer questions with full step-by-step explanations because they become reference material; "if a message could be a question rather than instruction, answer the question first and wait"; when adding to notes, keep the *full* version not a compressed one; show before committing; never search past chats — tracker is source of truth.

**Protocol 2 (Drafting):** plan interactively, draft in one pass, revise in chunks. Steps: overall outline → detailed subsection outline → agree on length → Claude drafts full subsection in one pass → review and revise in chunks → check overall outline → repeat. Drafting unit is the subsection ("1.2 The productivity channel"), not full chapter. Insight stated explicitly: "Claude produces better writing in larger passes, the user produces better thinking in tighter loops — separate them so each party does what they're best at."

**Why port:** Generic, no FMM contamination, perfectly aimed at our researcher/professor/policy audience. The thinking-vs-drafting separation is the kind of insight a public skill should embody. A "Setting up for a new project" section at the end lists the parameters CLAUDE.md should define (source material format, notes structure, to-do/tracker structure, progress tracker, deliverable format, style profiles, version control, subsection sizing, lookup order) — clean parametrization.

**Edits needed if porting:** strip Andrea-specific examples, drop the "PAT-via-curl" assumption (Andrea's version assumes API access — true for us too but mention should generalize). Otherwise near-zero edits.

### `BranchWorkflow_Skill.md` — branch-based document review

**Source:** `~/code/AITaxBID/skills/BranchWorkflow_Skill.md` (last updated 2026-05-02, v2.0). 175 lines.

**Mechanism:** Andrea opens markdown in the GitHub web UI (or local git) and writes inline `[bracketed comments]` in plain language with no required tag vocabulary. Examples from the skill: `[this is wrong, fix it]`, `[too long, cut to one sentence]`, `[change "12 puntos" to "12 puntos del PIB"]`, `[move this to slide 8]`, `[not sure about this paragraph — what do you think]`, `[check that Bellon 2022 is the right citation here]`. Andrea may also rewrite text directly without a comment. Claude detects via `git diff` against the branch-creation commit, classifies each bracketed comment as instruction / question / ambiguous (asks before acting on substantive changes), strips brackets from final text, and proofreads direct edits with light-vs-heavy distinction.

**Light fixes (silent):** typos, missing/wrong accents (esp. Spanish), capitalization, punctuation, citation formatting (e.g., `Adan et al, 2023` → `Adan et al. 2023`).
**Heavy issues (surfaced, never auto-fixed):** terminology drift, document-internal inconsistency, voice mismatch.

**Report-back has three sections:** comment-driven changes / direct edits — light fixes applied silently / direct edits — heavy issues flagged.

**Why port (high priority):** *Exactly* fits `claude_researcher`'s audience — non-CLI users editing through a browser. The bracketed-comment substrate works in any text box. The "light silent / heavy flagged" rule is good general judgment encoding for any reviewer skill. Andrea's branch naming convention (`<project-slug>-<purpose>-<date>`, e.g., `marta-oecd-edits-may-1`) is a reasonable default.

**Edits needed if porting:** Andrea's skill assumes pandoc-based docx/pptx regeneration as part of the loop ("If the edited file is a markdown source for a Word document → regenerate the `.docx` with pandoc"). The claude.ai sandbox has Python and basic tooling; whether it has pandoc is verifiable but unknown to me right now. Either gate the regeneration step on tool availability or strip it for v1 and add later. Otherwise highly portable.

### `paper_processing.md` — but compare to Nori `add-paper` first

**Source:** `~/code/AITaxBID/skills/paper_processing.md` (v2.0, 2026-05-02). 320 lines.

**Novel feature: Step 0 triage.** Three structural questions decide Protocol A (academic-style) vs Protocol B (institutional-style): (1) Does it have an abstract vs. an executive summary? (2) Does it pose a research question or hypothesis? (3) Does it report new estimates the authors produced from data they analyzed? Two-or-more "yes" → A; two-or-more "no" → B. Border cases: multilateral working papers usually A; institutional monographs usually B at document level; country case studies usually B.

**Protocol A:** filename `Author_shortTitle_year.pdf`, BibTeX `@article` / `@unpublished`. Summary sections (a) thesis / (b) methodology + findings (precise: name datasets, name countries, name methods) / [(c) conditional section if `CONDITIONAL_SECTION` is defined] / (d) relevance to `PROJECT_QUESTION`.

**Protocol B:** filename `institution_shortTitle_year.pdf` (`imf_g20RevenueAdmin_2025`, `worldBank_taxCapacity_2024`, `brazilRfb_confiaProgram_2024`), BibTeX `@techreport` / `@book` / `@inbook` with double-braced institutional author (`author = {{International Monetary Fund}}`). Summary section (a) covers commissioning context; (b) covers document type / frameworks-and-databases drawn on / headline synthesized findings / policy framework / country case studies; (d) covers "what position does this report represent" + cross-references to other library entries.

**"Summary evolution principle":** the (a)–(d) structure is a floor not a ceiling. As the user works with a paper over time, the summary grows. Do not trim expanded summaries back to the minimal format.

**Why port (with comparison work):** Nori's `add-paper` covers the academic case but has nothing equivalent to Protocol B for institutional reports. Researchers in policy / economics / development / tax / regulation deal with G20 / IMF / World Bank / OECD / UN flagship reports constantly. The Step 0 triage is a clean primitive worth lifting. The summary evolution principle is wise (and matches research-mode thinking — provisional understanding accumulates).

**Risks if porting blindly:** double-coverage with Nori's `add-paper`; the BibTeX assumption may not match a non-LaTeX user; the `CONDITIONAL_SECTION` parameter is a project-specific filter that needs to be optional. Recommend: side-by-side comparison with Nori's `add-paper` first, picking best elements from each, before producing a `claude_researcher` version. Don't blind-port either one.

### `document_processing.md` — institutional / operational documents

**Status:** NOT read in detail. Andrea's `README.md` describes scope: legislation, government regulatory documents, terms of reference, consultant deliverables. The pipeline (per `PROJECT_SETUP.md` Phase 3 Skills Activation table) is: rename / extract / summarize / classify / index / cross-reference. Configuration: reliability labels (Citable / Validated / Under construction / Working draft / Flagged), confidentiality labels (PUBLIC / INTERNAL / CONFIDENTIAL), folder organization (default: by source institution).

**Why port:** Nori has no analog. Researchers in policy/social sciences deal with these documents as much as academic papers. Worth a full read and port in a follow-on session.

## Findings — patterns for `template/CLAUDE.md` (Tier B/C)

Encode these directly in CLAUDE.md as conventions, not separate skills:

- **Show-before-committing, universally.** Every Andrea skill has it; same insight that drove our Phase 3 scripted confirmation gates. Worth promoting from per-step pattern to a rule applying to all writes.
- **Tracker is source of truth, NOT past chats.** Verbatim from `writing_skill.md`: *"Do NOT search past chats or conversations. The tracker is the single source of truth for where we left off."* This is a claude.ai-specific discipline — past chats are temptingly available but unreliable. Loudly name STATUS.md / RESEARCH_LOG.md as the canonical resumption mechanism.
- **3+-repetition codification rule.** *"If the user asks for the same type of task 3+ times, check whether it should be codified as a rule in this file."* Sharp threshold — avoids both premature and too-late codification.
- **Parking Lot section** in CLAUDE.md for undecided items, items move out as decided. Beats pretending we've decided.
- **Interview discipline:** "Group 2-3 questions, don't fire all at once." "If the user has already answered some in their opening message, skip those questions." Already partly in our BOOTSTRAP.md; reinforce.
- **"Do not infer — ask"** when recipient/intent/audience is uncertain. *"A confident output based on wrong assumptions is worse than a quick clarifying question."*
- **Light vs. heavy distinction** in any reviewer / editor / proofreader skill: mechanical things silent, anything touching terminology / consistency / voice surfaced for user decision.

## Findings — Phase 4 CLAUDE.md template-structure pattern

Andrea's `CLAUDE_TEMPLATE.md` uses a clean per-skill section format:

```markdown
## Paper Processing Workflow

> **Generic skill:** `skills/paper_processing.md`. The section below is the
> project-specific implementation — it adds parameters and any conventions
> that go beyond the generic skill.

When a PDF is provided to add to `papers/`, follow the full protocol in
`skills/paper_processing.md` with these project-specific parameters:

- **PROJECT_QUESTION:** "..."
- **CONDITIONAL_SECTION:** "..."
- **BIB_FILE:** `references.bib` (repo root)
- **PAPERS_INDEX:** `PAPERS_INDEX.md` (repo root)
```

Plus HTML comments throughout marking what to customize / delete / keep. Plus a "Parking Lot (To Be Defined)" section. Plus a "Working Conventions" section listing iterative workflow / CLAUDE.md is living / repetition rule / "uploaded = repo" / skills stay in skills/.

**Why useful for Phase 4:** the per-skill block pattern (`Generic skill: ... The section below is the project-specific implementation`) is the cleanest way to separate portable content from per-user-or-per-project parameters. Worth adopting in `template/CLAUDE.md`.

## Findings — what NOT to port

- **The three style profiles** (`Andrea_Writing_Style_Profile.md`, `Andrea_FMM_Institutional_Style_Profile.md`, `Marta_Writing_Voice_Profile.md`). Content is person/institution-specific. Pattern (versioned voice profiles, applied only on explicit request, with `_PLAIN.md` backup before styling, "draft first style second" principle, two-pass rule for stacked styles) is portable as a meta-skill.
- **`fmm_docx_formatting_skill.md`, `word_preamble.js`, `latex_preamble.tex`, `fmm_coordination_slides_skill.md`, all PNG assets** — FMM/IDB-branded. Verify what claude.ai sandbox actually has (LaTeX? pandoc?) before designing generic equivalents.
- **`email_drafting.md` content** — Andrea's voice + tone-by-recipient mapping (Marta / Alejandro & Phil / collaborators / group / external) is hers. *Workflow shape* (identify recipient type → ask for clarifications → "for sensitive emails offer 2-3 strategic approaches with tradeoffs" → draft → revise) is portable as `email_drafting_skeleton.md` with the user populating their own voice.
- **Parts C / D / E of `PROJECT_SETUP.md`** (propagation / portability evaluation / improvement artifacts) — designed for Andrea's full-kit-everywhere model with separate `SkillPropagation` repo. Doesn't fit on-demand fetch. **Exception:** Part D's portability evaluation framework ("is this generic or project-specific? what stays / what gets parameterized / what gets dropped?") is a thoughtful tool that could ship as its own skill for evaluating community-contributed improvements, if/when `claude_researcher` opens to PRs.

## Bugs / Friction Surfaced

- **AITaxBID's kit is one version behind canonical.** v2.0 CHANGELOG: "AITaxBID needs Phase 3 propagation post-v2.0 to catch up." Treat findings here as snapshot, not latest. If borrowing more than the surface, ask Dan whether Andrea's `SkillPropagation` repo is accessible.
- **HEAD progressed during this session.** Started at `a368f55`; worktree branched off `c644479` (Phase 4 in active progress on main with new `20260509_phase4_runtime_and_skill_index.md` convo). My pre-flight reads were stale by the time I created the branch — correct branching point but worth flagging.
- **Did not read `document_processing.md` or the academic-LaTeX/slides skills.** If those become priority, follow-up session needed.

## Open Questions (carry-forward)

- **Phase 4 CLAUDE.md adoption decisions:** which Andrea-patterns to encode (show-before-committing, tracker-not-past-chats, repetition rule, Parking Lot, "do not infer — ask")? Which framing to use? Recommend at least the per-skill section pattern + tracker-not-past-chats discipline.
- **Phase 5/6 skill porting decisions:** which order? Recommended order: `writing_skill.md` (low-friction port, high value) → `BranchWorkflow_Skill.md` (medium friction, very high value for claude.ai web-UI audience) → `paper_processing.md` (requires Nori comparison) → `document_processing.md` (requires read first) → portability-evaluation as standalone skill (low priority until `claude_researcher` opens to community contributions).
- **claude.ai sandbox tooling check:** does it have pandoc? LaTeX? Python with `python-docx`? `pypdf`? The plan's task list mentions verifying `pypdf` before Phase 5; same kind of check needed for any docx/pptx/LaTeX pipeline before designing equivalents to Andrea's `word_preamble.js` / `latex_preamble.tex` / pandoc-using BranchWorkflow regeneration step.
- **Naming / namespace decisions when porting:** Andrea uses `writing_skill.md`, `paper_processing.md`, `BranchWorkflow_Skill.md` — inconsistent (`_skill` suffix sometimes, sometimes not; CamelCase sometimes, snake_case sometimes). `claude_researcher` should pick a convention before porting.

## What's Next

This branch is ready to be left in place (or merged advisory-only) at Dan's discretion. The convo doc is the deliverable. No code changes here. If/when porting individual skills, recommend per-skill branches (`port-writing-skill`, `port-branch-workflow-skill`, etc.) so each port can be reviewed atomically.

If Dan wants the next-priority follow-on read in a fresh session: `document_processing.md` (because Nori has no analog and policy/social-science researchers need it) and Andrea's three style profiles (to extract the *pattern* into a meta-skill spec, not the content).

## Provenance

- **AITaxBID repo path read:** `/Users/dan/code/AITaxBID/skills/`
- **Files read in full:** `README.md`, `skills/PROJECT_SETUP.md`, `skills/writing_skill.md`, `skills/paper_processing.md`, `skills/BranchWorkflow_Skill.md`, `skills/CLAUDE_TEMPLATE.md`, `skills/email_drafting.md`
- **Files skimmed:** `skills/CHANGELOG.md` (first ~100 lines, v2.0.1 / v2.0 / v1.3.1 entries)
- **Files NOT read:** `document_processing.md`, `academic_paper_latex_skill.md`, `academic_slides_skill.md`, `fmm_coordination_slides_skill.md`, `fmm_docx_formatting_skill.md`, `Andrea_Writing_Style_Profile.md`, `Andrea_FMM_Institutional_Style_Profile.md`, `Marta_Writing_Voice_Profile.md`, `word_preamble.js`, `latex_preamble.tex`, all `LastSkillUpdate/` mirrors, all PNG assets
