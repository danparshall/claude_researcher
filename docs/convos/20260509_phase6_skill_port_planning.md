# claude_researcher — Phase 6 skill port planning (post-AITaxBID audit)

**Date:** 2026-05-09
**Repo:** claude_researcher
**Branch:** main (planning session, no worktree — light touch on plan + a new convo)
**Plan:** [`docs/plans/01_initial_build.md`](../plans/01_initial_build.md) — adds Phase 4.6 (CLAUDE.md retrofit) and Phase 6 task expansions for AITaxBID-sourced skills
**Predecessor convos:**

- [`docs/convos/20260509_aitaxbid_skills_audit.md`](20260509_aitaxbid_skills_audit.md) — landed this session via squash-merge of PR #1 (commit `6397c33`)
- [`docs/convos/20260509_phase4_runtime_and_skill_index.md`](20260509_phase4_runtime_and_skill_index.md) — established the Phase 4 production CLAUDE.md the retrofit modifies

## Summary

Translated the AITaxBID skills audit's three-tier recommendation set into concrete plan tasks. Three buckets of work emerged:

1. **Phase 4.6 — CLAUDE.md retrofit** (new section in plan). Five Tier-B/C patterns get encoded in `template/CLAUDE.md` as universal rules: tracker-not-past-chats discipline, 3+-repetition codification rule, Parking Lot section, "do not infer — ask," and show-before-committing universalized. The shipped Phase 4 CLAUDE.md has *partial* coverage of each — they live as per-step practice in §4–§6 confirmation gates rather than as universal rules. Each retrofit task names the target CLAUDE.md section and what specifically to add.

2. **Phase 6 task expansions** (additions to existing phase). Two Tier-A direct ports (`writing-skill`, `branch-document-review`), one fold-in (Protocol-A/B triage + institutional-report summary structure → expand existing `add-paper`), one new skill (`document-processing` — Nori has no analog, audit didn't read source in full). Three new tasks plus an update to the existing `add-paper` tasks.

3. **Deferred** — portability-evaluation skill (audit's Part D adaptation, only meaningful if/when claude_researcher opens to community contributions); per-user-repo `CLAUDE_TEMPLATE.md` (Andrea's pattern; separate design question — its applicability to claude_researcher's flat-research-repo design isn't obvious).

## Decisions Made

- **Port order matches the audit's recommendation:** writing-skill (low-friction, high value) → branch-document-review (medium friction, very high value for claude.ai web-UI audience) → expand add-paper for Protocol B → document-processing (read source first; port if Nori truly has no analog). Sequencing rationale: each port is bigger than the last, and the early ones surface sandbox-tooling unknowns that affect the harder ones.

- **Skill naming convention is Nori-style.** Kebab-case directory, `SKILL.md` inside, frontmatter with `name:` (matching directory) and `description:`. `writing_skill.md` → `template/skills/writing-skill/SKILL.md`. `BranchWorkflow_Skill.md` → `template/skills/branch-document-review/SKILL.md`. `document_processing.md` → `template/skills/document-processing/SKILL.md`. The Nori convention wins over Andrea's mixed snake/Camel because it matches the carry-overs already in the SKILL_INDEX (`finish-convo`, `add-paper`, `audit-docs`, etc.).

- **`paper_processing.md` is a fold-in to existing `add-paper`, not a separate skill.** The audit explicitly warned against double-coverage. The cleanest synthesis: keep Nori's `add-paper` as the entry point and architecture; lift Andrea's Step 0 academic-vs-institutional triage and Protocol B institutional summary structure (commissioning context / document type / frameworks-and-databases / headline synthesized findings / policy framework / country case studies / position) into add-paper's flow. Dan's `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf` paper_naming format remains primary; document Andrea's `institution_shortTitle_year.pdf` as a secondary convention for users in policy/economics who use BibTeX-citable institutional reports heavily.

- **`branch-document-review` requires real adaptation, not "near-zero edits."** Andrea's skill assumes local `git diff` against the branch-creation commit to find bracketed comments. For claude_researcher's REST-only world, the equivalent is: read the file at `?ref=<branch>` AND `?ref=main`, compute the diff in Python (sandbox-side), parse the bracketed-comment delta. That's a real port, not a copy-paste. Also, Andrea's pandoc-based docx/pptx regeneration loop ("If the edited file is a markdown source for a Word document → regenerate the `.docx` with pandoc") needs a sandbox-tooling check before we know whether to ship it in v1 or stub it.

- **Sandbox-tooling check is gated, not upfront.** `pypdf` is already on the Phase 5 task list. `pandoc`, `python-docx`, LaTeX availability are unknown and only matter when `branch-document-review` ships. Defer that check until the port begins; if pandoc unavailable, ship v1 of the skill without regeneration plus a TODO. Don't block earlier ports on it.

- **Tier B/C CLAUDE.md patterns become explicit Phase 4.6 tasks**, not vague aspirations. Each has a target section in CLAUDE.md so the retrofit work is concrete and reviewable. The retrofit is a single commit ("Phase 4.6: CLAUDE.md retrofit") rather than five trickled commits.

- **Per-user-repo `CLAUDE_TEMPLATE.md` is deferred, with a tracked open question.** Andrea's pattern of a per-project CLAUDE.md with `Generic skill: ... project-specific implementation` blocks is portable in form, but claude_researcher's design currently has STATUS.md + personal_info.md serve part of that role and runs the *runtime* CLAUDE.md from upstream. Whether each user's research repo would benefit from its own short CLAUDE.md (project-specific parameters that override or extend upstream) is a real design question deferred until Phase 6 ports actually demonstrate (or fail to demonstrate) the need.

## Findings — Phase 4.6 retrofit details

Five tasks. Each names the source pattern from the audit, the target section in `template/CLAUDE.md`, and what specifically gets added. Current coverage in CLAUDE.md is "partial" for all five — they live as per-confirmation-gate or per-step practice, not as universal rules.

- **Tracker-not-past-chats (target: new §1.5 or top of §2).** Verbatim source: *"Do NOT search past chats or conversations. The tracker is the single source of truth for where we left off."* claude.ai-specific discipline because past chats ARE available but unreliable. Currently absent from CLAUDE.md. Add as: "Resumption mechanism is STATUS.md + RESEARCH_LOG.md, NOT past chats. If a user references 'last time we said X,' verify against the trackers; do not trust chat memory."

- **3+-repetition codification (target: new working-conventions block under §5).** Source: *"If the user asks for the same type of task 3+ times, check whether it should be codified as a rule in this file."* Sharp threshold; avoids premature and too-late codification both. Currently absent. Add as a self-improvement directive.

- **Parking Lot section (target: new §8 or Appendix).** Source: Andrea's CLAUDE_TEMPLATE.md ships a "Parking Lot (To Be Defined)" section for undecided items; items move out as decided. Currently absent — under-determined items in this CLAUDE.md live in `docs/plans/` only. Add a Parking Lot section here so the runtime instruction set has a stable home for self-tracked open questions.

- **"Do not infer — ask" universalized (target: new working-conventions block under §5).** Source: *"A confident output based on wrong assumptions is worse than a quick clarifying question."* Existing §4 (project confusion) and §3c (no-match branch resolution) are specific applications. Promote to a universal rule alongside the codification rule.

- **Show-before-committing universalized (target: new working-conventions block under §5).** Existing CLAUDE.md scripts gates at sensitive boundaries (§3 branch creation, §5 destructive deletes, §6 archive/merge). Audit recommends promoting to a universal rule applied to *all* writes. Add as: "Before any write to the user's repos, briefly state what you're about to write and why. The user can interject before the commit lands." Reframes per-gate confirmations as the default rather than exceptions.

The sixth Tier-B pattern from the audit (per-skill `Generic skill: ... project-specific implementation` block format) lives in Andrea's `CLAUDE_TEMPLATE.md`, which is a *per-user-repo* artifact. claude_researcher doesn't currently ship a per-user-repo CLAUDE.md template; whether to is a separate design question (open question below). Tracked but not in the retrofit.

## Findings — Phase 6 expansion details

Three new ports plus an update to existing add-paper tasks. Each scoped concretely so an implementing agent (or future Dan) knows where to start.

- **Port `writing-skill`** (`template/skills/writing-skill/SKILL.md`). Source: `~/code/AITaxBID/skills/writing_skill.md` (169 lines). Adaptation: strip Andrea-specific examples (FMM-specific phrasing in some sections), drop the bash-is-fine-for-trivial-things contamination from her CLAUDE.md, keep the two-protocol thinking-vs-drafting split intact. The "Setting up for a new project" section at the end of her skill becomes the per-user parameter list that the runtime CLAUDE.md or per-project CLAUDE.md would override. Frontmatter `name:` = `writing-skill`, description captures the two-protocol shape. Estimated effort: ~1 hour, mostly trimming.

- **Port `branch-document-review`** (`template/skills/branch-document-review/SKILL.md`). Source: `~/code/AITaxBID/skills/BranchWorkflow_Skill.md` (178 lines). Real adaptation needed: replace local `git diff` with REST-API-mediated diff (read file at two refs, diff in Python sandbox-side, parse bracketed-comment delta). Light/heavy review distinction (typos/accents/punctuation silent vs. terminology drift / inconsistency / voice flagged) ports verbatim. Pandoc regeneration step gated on sandbox-tooling check; ship v1 without it if pandoc unavailable. Frontmatter `name:` = `branch-document-review`. Estimated effort: ~2-3 hours including the diff-parsing helper. Highest-value port for the claude.ai-only audience.

- **Expand `add-paper` for Protocol B** (existing `template/skills/add-paper/SKILL.md`, planned for Phase 6 task 36-37). Update task 36 (download mode) to include Step 0 academic-vs-institutional triage from Andrea's `paper_processing.md` (320 lines). Three structural questions decide A vs B: abstract vs executive summary; research question vs no; new estimates vs no. Two-or-more "yes" → Protocol A (Nori's existing flow with light Protocol-A summary structure tweaks); two-or-more "no" → Protocol B (institutional summary structure, BibTeX `@techreport` / `@book` / `@inbook` with double-braced institutional author). Naming: keep Dan's `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf` for Protocol A; document Andrea's `institution_shortTitle_year.pdf` as the Protocol B convention. The audit's "summary evolution principle" (the (a)-(d) structure is a floor not a ceiling — let summaries grow over time) ports verbatim into the skill body.

- **Read `document_processing.md` and port as `document-processing`** (`template/skills/document-processing/SKILL.md`). Source: `~/code/AITaxBID/skills/document_processing.md` (277 lines). Audit did not read this in detail — the first task is a careful read. Scope per Andrea's README: legislation, government regulatory documents, terms of reference, consultant deliverables. Pipeline: rename / extract / summarize / classify / index / cross-reference. Reliability labels (Citable / Validated / Under construction / Working draft / Flagged) and confidentiality labels (PUBLIC / INTERNAL / CONFIDENTIAL) are configurable parameters that should be optional in the ported skill (most users won't have an INTERNAL/CONFIDENTIAL distinction). Nori has no analog; this is meaningful new capability. Estimated effort: ~3-4 hours including the source-read.

- **SKILL_INDEX.md updates** (Phase 6 task 43). Add three entries (writing-skill, branch-document-review, document-processing) under appropriate sections — likely a new "Writing & document workflow" group between "Knowledge-management skills" and "Working-style skills (carried over from upstream Nori)."

## Findings — what got deferred

- **Portability-evaluation skill** (audit's Part D adaptation). Useful only when community contribution opens up — claude_researcher v1 is solo-author. YAGNI for v1, possibly v2.0 when the public repo invites contributions.
- **Per-user-repo `CLAUDE_TEMPLATE.md`.** See decisions above — separate design question deferred until Phase 6 ports demonstrate need (or its absence).
- **Andrea's three style profiles** (Andrea_Writing, Andrea_FMM, Marta_Voice) and her email_drafting workflow. Audit recommends *patterns* are portable as meta-skills (versioned-voice-profile-applied-on-explicit-request, draft-first-style-second), but content is person/institution-specific. Skip in Phase 6; revisit if writing-skill ports cleanly and a user asks for voice-profile support.
- **`fmm_docx_formatting_skill.md`, `word_preamble.js`, `latex_preamble.tex`, slides skills.** FMM/IDB-branded; no portable content. Skip entirely.

## Open Questions (carry-forward)

- **Sandbox tooling matrix.** Does claude.ai's sandbox have `pandoc`, LaTeX (`pdflatex`), `python-docx`? `pypdf` is on the Phase 5 task list (existing task 31). Worth doing one consolidated check and recording in `template/reference/SANDBOX_TOOLING.md` — referenced by every subsequent skill port. The check itself is one bash session in a fresh claude.ai chat with the allow-list configured. Pure information gathering.

- **`branch-document-review` diff-parsing approach.** Two implementation paths: (a) GitHub Compare API (`GET /repos/{owner}/{repo}/compare/{base}...{head}`) returns a unified diff per file — easiest, but rate-limit-aware; (b) read both files via Contents API and diff in Python with `difflib`. (a) preserves git-native diff semantics; (b) is more flexible and avoids extra API calls when files are already cached. Slight preference for (a). Decide at port time.

- **Subsection-sized drafting in writing-skill.** Andrea's "drafting unit is the subsection" rule was written against academic-paper structure. Does it generalize to research notes / blog drafts / policy memos? Likely yes (subsection ≈ "smallest coherent revisable chunk"), but worth surfacing in the ported skill as a parameter the user can adjust rather than asserting silently.

- **bracketed-comment vocabulary in `branch-document-review`.** Andrea explicitly avoids requiring a tag vocabulary — any bracketed natural language works. Should claude_researcher follow her lead, or seed a small recommended vocabulary (`[fix]`, `[?]`, `[cite]`, `[move]`) for users who want one? Audit recommends following Andrea verbatim. Defaulting to that; user can self-organize.

- **Per-user-repo CLAUDE_TEMPLATE.md (cross-reference to deferred).** Resolve after Phase 6 ports, when we know whether the project-specific-parameters question actually bites.

- **Reconciling `paper_naming` with Andrea's institutional convention** (open since the audit was written). When add-paper is expanded with Protocol B, both `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf` and `institution_shortTitle_year.pdf` need to coexist. Likely outcome: both are valid, agent picks based on Step 0 triage outcome, both are documented in personal_info.md's `paper_naming` field as "academic_format" + "institutional_format" pair.

## Bugs / Friction Surfaced

- **Step 8 `raw.githubusercontent.com` allow-list miss (smoke-test artifact, not blocking).** The agent at Step 8 of the bootstrap walkthrough tried sandbox curl to `raw.githubusercontent.com` to fetch `_PROJECT_INSTRUCTIONS.md.template`, got blocked by the allow-list, and gracefully fell back to a stale WebFetch cache from earlier in the same chat. Two possibilities to investigate: (a) BOOTSTRAP Step 1's allow-list paste instructions don't actually result in `raw.githubusercontent.com` being added (UI quirk or instruction defect), or (b) the architectural rule "WebFetch reaches public upstream content" was supposed to mean the agent uses WebFetch (not curl) for `raw.githubusercontent.com` reads — in which case Step 8 needs an explicit "use WebFetch, not curl" callout. Either way, the workaround masked the bug. NOT blocking — Step 9 validation passed end-to-end despite this — but worth a small follow-on commit when investigated.

- **Step 8 minor cosmetic: the substitute-everywhere rule produced a "tautological prose line"** with the user's PAT appearing twice in the rendered Custom Instructions block (once in the bash assignment, once in a prose tautology). Harmless but slightly unprofessional in a credentials-bearing block. Worth tightening the substitute-everywhere rule to skip prose contexts later.

## Phase 4 status update (post-validation)

**Step 9 validation passed.** End-to-end test:

- Agent correctly fetched CLAUDE.md from upstream via WebFetch
- Set env vars from Custom Instructions
- Fetched `personal_info.md` from `basic_config` via PAT/curl (private repo path) ✓
- Fetched STATUS.md + README.md from `research-knowledge-base` ✓
- Fetched SKILL_INDEX.md from upstream ✓
- Presented orientation correctly: named the user, identified interaction style (light narration), recognized `branches` workflow mode, listed available skills, offered three natural next-step options

This validates: the calibration tier dial, the two-fetch-mechanism architecture, the Custom Instructions credential payload, the SKILL_INDEX-as-manifest contract, and the §3 branch-resolution-from-empty-repo fallback. Phase 4 is genuinely complete. STATUS.md should be updated by finish-convo at session end.

## What's Next

- This convo + plan diff is the deliverable for this session. No skill bodies written yet.
- **Phase 4 closure:** STATUS.md gets updated to reflect Step 9 pass at session end (finish-convo). The `raw.githubusercontent.com` finding becomes a small follow-on TODO, not a blocker.
- **Suggested next session:** start [`docs/plans/02_skill_ports.md`](../plans/02_skill_ports.md) Wave 0 (provenance + sync infrastructure, ~1 hr) then Wave 1 (SWE carryovers, ~1-2 hr). 9 working skills in `template/skills/` within ~3 hours. Wave 2 (session lifecycle) and Phase 4.6 (CLAUDE.md retrofit) come next.

---

## Continuation (later same evening) — Phase 7+ scope, publish strategy, Nori chain, wave-based plan

After the Phase 4 Step 9 validation result, the session continued with several additional decisions and one new plan doc. Captured below in the order they happened.

### Phase 7+ scope reduction recognized

User asked "what else is happening in Phase 5/6?" then "what's in Phase 7+?" — answering forced us to look at the original plan against the actual smoke-test-driven evolution. **Most of Phase 7-10 is already retired implicitly:** BOOTSTRAP.md absorbed `WHY_REST.md` / `PAT_SETUP.md` / `PROJECT_SETUP.md` content during the Phase 4 restructure; today's smoke test was effectively Phase 8's self-walkthrough; Phase 10 task 58 (publish strategy) and task 59 (README bootstrap prompt) and task 60 (test from clean machine) are all done in different shapes than originally specified.

**Real remaining work in Phases 7-10:**

- **Phase 9 collaborator walkthrough** — only remaining test that materially de-risks v1; everything before proves it works *for Dan*. User noted "external user part is already underway."
- Phase 10 task 61 (placeholder issue to validate pre-filled URL) — ~15 min.
- Phase 8 timing re-test in fresh chat with no edits — ~30 min.
- (optional) Phase 7 screenshots if Phase 9 surfaces friction.

The **Implementation Status Tracker** at the top of `01_initial_build.md` was added to make nominal-vs-actual phase state legible at a glance. Updated several times during this session as decisions came in.

### Publish strategy revisited and resolved

Status: **resolved as status-quo with framing repair.** Original Phase 10 task 58 default was "leave docs/ in dev repo only; revisit if collaborators ask 'why did you decide X?'." On 2026-05-09 the dev repo was flipped public to enable smoke-test reads from `raw.githubusercontent.com` — that bypassed the original default without a deliberate decision.

User clarified: **Andrea Lopez-Luzuriaga is a collaborator on this project**, which removes the only real concern with `docs/convos/` being public (the AITaxBID audit naming her). Decision: keep dev-repo-public; add an "About" section to the root `README.md` that frames the project as a Dan + Andrea collaboration sharing learnings with the academic community. Done in commit `a18ef92` (initial) + `048d140` (linked to personal websites: danparshall.com, andrealopezluzuriaga.com) + `8a8b9cf` (TLD fix to .net).

The "About" framing converts the candor of `docs/convos/` from "internal-asides leaked" to "deliberate transparency" — which is closer to the truth anyway.

### Andrea invited as collaborator (operationally)

User provided GitHub handle `aflopezluzuriaga`. Invited via `gh api -X PUT /repos/.../collaborators/aflopezluzuriaga -f permission=push`. Standard Write role. Invitation pending Andrea's acceptance.

### Three-layer Nori propagation chain established

User clarified the architectural framing: **`claude_researcher` = Nori Researcher + non-CLI tricks**. User authors the Nori Researcher skillset; Researcher leverages parts of the Nori SWE skillset (which user does NOT author). So the propagation chain has 3 layers:

```
Nori SWE          (external upstream; user doesn't author)
   ↓
Nori Researcher   (user authors; depends on SWE for working-style skills)
   ↓
claude_researcher (user authors; depends on Researcher; adds REST adaptations)
```

Implication: **changes to SWE upstream don't reach claude_researcher unless the user carries them forward through both layers.** A drift-detection mechanism is real value, not premature abstraction.

### Skill categorization by adaptation effort

Building on the AITaxBID audit's tier framing + the propagation chain, skills bucket into three categories with different upstream relationships:

- **SWE carryovers** (~9 skills: brainstorming, TDD, debugging, etc.) — pure-thought skills, touch zero environmental axes, no REST adaptation needed. Ports are essentially `cp` + provenance stamp.
- **Researcher skills** (finish-convo, update-docs, add-paper, audit-*, init-research-repo, write-a-plan, handle-large-tasks) — user authors both Nori (local) and claude_researcher (REST) implementations. Real adaptation work where they touch the file I/O / commit semantics axes.
- **AITaxBID-derived skills** (writing-skill, branch-document-review, document-processing) — separate upstream maintainer (Andrea), snapshot pattern with deferred propagation.

Frontmatter convention: each ported `SKILL.md` carries one (or more) of `nori_swe_source` / `nori_researcher_source` / `aitaxbid_source` with stamped SHA at port time. Multiple sources allowed for synthesis ports (Wave 3's `add-paper` will be the first — Researcher workflow + AITaxBID Protocol B fold-in).

### Wave-based skill-port plan written

Created [`docs/plans/02_skill_ports.md`](../plans/02_skill_ports.md), commit `2d2ba27`. Wave-based execution plan ordered for time-to-first-usable-skill given beta users imminent:

- **Wave 0** Provenance + sync infrastructure (~1 hr)
- **Wave 1** SWE carryovers — 9 skills via `cp` + stamp (~1-2 hr) → **first ship-ready state**
- **Wave 2** Session lifecycle (finish-convo, update-docs) — ~2-3 hr
- **Wave 3** Knowledge management (add-paper × 2, audit-docs, audit-papers) — ~4-5 hr
- **Wave 4** AITaxBID Tier A (writing-skill, branch-document-review) — ~3-4 hr
- **Wave 5** Deferred (document-processing, init-research-repo)

Plan also locks in: Phase 5 helpers slot between Waves 2 and 3 (skills can embed REST recipes inline pre-Phase-5); Phase 4.6 CLAUDE.md retrofit interleaves between Wave 1 and Wave 2; Phase 9 collaborator walkthrough runs in parallel.

**Beta-user-imminent caveat surfaced in the plan:** before any beta user is pointed at the repo, `SKILL_INDEX.md` should be trimmed to only-ported skills. Currently lists 14 skills, none of which exist as `SKILL.md` files yet — fetch failures would be a poor first impression.

## Decisions Made (continuation)

- **Publish strategy: status quo + About section.** Dev repo stays public including `docs/`. Andrea is a collaborator so naming her is fine. Root README has an About section linking to both personal websites.
- **Andrea added as repo collaborator** (`aflopezluzuriaga`, Write permission). Operational, not just textual.
- **3-layer propagation chain is the correct mental model.** Drives the provenance frontmatter convention, sync script, and drift-detection check.
- **Provenance per skill is per-source** — multiple sources allowed for synthesis ports. Wave 3's `add-paper` exercises this first.
- **Wave-based shipping** over phase-based. 01_initial_build.md's Phase 5/6/4.6 task structure is preserved; 02_skill_ports.md adds the *ordering* layer optimized for time-to-first-usable-skill.
- **Phase 5 helpers are NOT prerequisite** for Wave 2-4 skill ports. Skills embed REST recipes inline initially; refactor to helpers between Waves 2 and 3.

## Open Questions (continuation, carry-forward)

- **`SKILL_INDEX.md` trimming timing.** When does it happen — before Wave 1, alongside Wave 1, or as a pre-emptive Wave 0 task? Listed in 02_skill_ports.md Open Questions but not assigned a wave.
- **Synthesis-skill provenance YAML shape.** Decision deferred to Wave 0 (frontmatter convention is locked there before Wave 1 starts stamping). Multiple top-level keys (`nori_researcher_source`, `aitaxbid_source`) vs. a single list vs. nested — pick at Wave 0.
- **`raw.githubusercontent.com` Step 8 finding** (carry-forward from earlier in this session). Not investigated. Fold into Wave 1 smoke-test of carryover URLs since the same allow-list mechanism is involved.
- **Phase 9 candidate.** User mentioned "external user part is already underway" — implies a specific candidate is in motion. Not named; not blocking.

## Provenance

- **Source convo audited:** `docs/convos/20260509_aitaxbid_skills_audit.md` (149 lines, just merged via PR #1)
- **Source repo (re-grounding):** `/Users/dan/code/AITaxBID/skills/` — confirmed file presence and line counts for `writing_skill.md` (169 lines), `BranchWorkflow_Skill.md` (178 lines), `paper_processing.md` (320 lines), `document_processing.md` (277 lines, not yet read in detail)
- **Nori comparison points:** `~/.claude/skills/add-paper/SKILL.md` (128 lines), `~/.claude/skills/finish-convo/SKILL.md` (42 lines), `~/.claude/skills/update-docs/SKILL.md` (103 lines)
- **CLAUDE.md state read:** `template/CLAUDE.md` (production, post-Phase-4) — confirmed §1–§7 + Appendix structure; partial coverage analysis grounded in actual section content
- **SKILL_INDEX.md state read:** `template/skills/SKILL_INDEX.md` — confirmed manifest contract and existing groupings; new entries fit under a new "Writing & document workflow" group
- **Plan file state read:** `docs/plans/01_initial_build.md` — Phase 4 complete, Phase 4.5 deferred for collaborator mode, Phase 6 currently has tasks 34-44; new Phase 4.6 + Phase 6 expansions slot cleanly
