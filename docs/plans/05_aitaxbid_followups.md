# claude_researcher — AITaxBID Follow-ups (stub)

**Goal:** Consolidate audit-derived work still open after Plan 02 Wave 4 + W3.1 retrofit + Tier C decision. Plan 02 covered the original scoping on 2026-05-09; this plan re-scopes what's open given drift since then.

**Status:** Stub. Tasks scaffolded but not fleshed out — next session (WebUI) does the detailed scoping per task.

**Parent plans:**

- [`02_skill_ports.md`](02_skill_ports.md) — original wave-based plan; Waves 1–3 shipped, Wave 4 still open, W3.1 dropped at Wave 3 ship.
- [`04_sandbox_tooling_and_companion_cleanups.md`](04_sandbox_tooling_and_companion_cleanups.md) — may have already verified pandoc/LaTeX availability needed by W4.0 here; check before duplicating.

**Originating convos:**

- [`20260509_aitaxbid_skills_audit.md`](../convos/20260509_aitaxbid_skills_audit.md) — original audit findings (also on main via PR #1 → `6397c33`)
- [`20260512_audit_followup_and_plan05.md`](../convos/20260512_audit_followup_and_plan05.md) — audit follow-up reconciliation + Plan 05 scaffolding

**Confidence:** Low (stub). Each task needs detailed scoping next session.

**Branch:** main (build work, not exploration).

**Tracking issues:**

- [#3 — W3.1 fold-in (paper_processing → add-paper)](https://github.com/danparshall/claude_researcher/issues/3)

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

### W4.0 — Sandbox tooling pre-check (gate for W4.3)

Verify in the claude.ai sandbox what's available before designing the pandoc-regeneration step in `branch-document-review`. Cross-check Plan 04 first to avoid duplication.

To verify:

- pandoc
- LaTeX (`pdflatex`, `xelatex`)
- Python: `python-docx`, `pypandoc`, `python-pptx`

**Status:** Stub.

### W4.1 — Port `writing-skill` (Andrea Tier A)

Light-friction port of Andrea's `writing_skill.md`.

- Source: `~/code/AITaxBID/skills/writing_skill.md`
- Re-check SHA at session start; Andrea's kit may have evolved since 2026-05-09
- Defer to Andrea on Protocol 1 (Reading/Thinking) and Protocol 2 (Drafting) structure
- Strip AITaxBID-specific examples; keep workflow shape intact
- Stamp `aitaxbid_source` + SHA

**Status:** Stub.

### W4.2 — Decide diff mechanism for `branch-document-review`

Decision needed before W4.3. Plan 02 noted "slight preference for Compare API."

Options:

- GitHub Compare API (`/repos/{owner}/{repo}/compare/{base}...{head}`)
- Read-both-and-difflib (no API dependency)

**Status:** Stub.

### W4.3 — Port `branch-document-review` (Andrea's `BranchWorkflow_Skill`, Tier A)

Highest-priority port — best fit for the claude.ai web-UI audience because the bracketed-comment substrate works in any GitHub textbox.

- Source: `~/code/AITaxBID/skills/BranchWorkflow_Skill.md` (v2.0, 175 lines as of 2026-05-09; re-check SHA)
- **Keep intact:** `[bracketed comments]` convention; light-vs-heavy reviewer distinction; three-section report structure (comment-driven changes / direct edits silent / direct edits flagged); branch-naming convention (`<project-slug>-<purpose>-<date>`)
- **Adapt:** `git diff` → mechanism chosen in W4.2
- **Gate on W4.0:** pandoc-regeneration step ships only if pandoc is available; otherwise v1 ships without regeneration + a TODO
- Defer to Andrea on comment-classification rules (instruction / question / ambiguous)
- Stamp `aitaxbid_source` + SHA

**Status:** Stub.

### W3.1 retrofit — Fold AITaxBID synthesis into `add-paper`

**Tracking:** issue [#3](https://github.com/danparshall/claude_researcher/issues/3).

Plan 02 Wave 3 shipped `add-paper` without the AITaxBID synthesis. Retrofit:

- Step 0 academic-vs-institutional triage (three structural questions, two-or-more rule)
- Protocol A / Protocol B branching (filename + summary structure + BibTeX entry type)
- Summary Evolution Principle ((a)–(d) is a floor not a ceiling)
- `personal_info.md` schema extension: `paper_naming.academic_format` + `paper_naming.institutional_format`
- BOOTSTRAP.md interview Batch 3 paper-naming update
- Dual provenance stamp (first skill with both `nori_researcher_source` AND `aitaxbid_source`) — sets the precedent for future synthesis ports
- Defer to Andrea on Protocol B structure (commissioning context, document-type framework, etc.)

**Status:** Stub.

### Tier C decision — "Generic-skill" block format

**Open question, architecture-level.** Andrea's `CLAUDE_TEMPLATE.md` introduces each skill with a per-skill markdown block:

```markdown
## Paper Processing Workflow

> **Generic skill:** `skills/paper_processing.md`. The section below is the
> project-specific implementation — it adds parameters and any conventions
> that go beyond the generic skill.

[per-project parameters here]
```

The pattern cleanly separates portable content (the skill spec) from per-project parameters (PROJECT_QUESTION, BIB_FILE, etc.).

**Architectural mismatch to think through:** claude_researcher's `RESEARCHER.md` is upstream-shared (one canonical version for all users; no per-project content lives there). The `personal_info.md` surface carries user-level prefs but not per-project parameterization. So the question is *where* this pattern would live for us:

- **Option A:** In each `SKILL.md`. Each skill has its own "project parameters" section users fill in or default.
- **Option B:** In a new optional file users add to their research repo (e.g., `PROJECT_PARAMS.md`). Surfaced at session-start fetch.
- **Option C:** In `STATUS.md`. Extend its role from "where things are" to also "how this project parameterizes the generic skills."
- **Option D:** Skip. Our architecture handles this differently (skills are self-contained; users adapt in conversation, not in config).

**Not a rehash of `creating-skills`** (which is the meta-skill for *authoring* new skills). This is about *how the runtime instructions or project docs reference skills* once they exist.

**Status:** Stub. Decision needed in the WebUI session.

### W4.4 — Update `SKILL_INDEX.md`

Add a "Writing & document workflow" group between knowledge-management and working-style. Entries for `writing-skill` and `branch-document-review`.

**Status:** Stub.

### W4.5 — Ship commit

Per Wave 4 ship criterion (Plan 02): beta users have access to the writing workflow and the document-review pattern that fits the claude.ai web-UI audience.

**Status:** Stub.

---

## Open questions

- Andrea's AITaxBID kit may have evolved since 2026-05-09; re-check SHAs at session start. If Andrea's `SkillPropagation` repo is accessible, prefer that as canonical source.
- Sandbox tooling availability (pandoc, LaTeX) — see W4.0. Plan 04 may have addressed some of this already.
- Tier C architectural placement — see "Tier C decision" task above. Decide before the WebUI session puts work into a particular surface.
- After Plan 05 ships, should the `aitaxbid-skills-audit` branch be archived? The audit doc itself remains valuable as a reference; the branch is stale (14+ commits behind main as of this plan creation).
- Light-vs-heavy distinction was identified as a Tier B pattern in the audit but is only relevant if a reviewer/editor skill exists — i.e., it lands naturally with W4.3 (`branch-document-review`). No separate task needed.

## What this plan deliberately does NOT cover

- **`document_processing` port** (Plan 02 Wave 5, deferred by design). Requires full read of Andrea's 320-line source first; not on beta-user critical path. Re-prioritize in a future plan when ready.
- **`init-research-repo`** — already shipped per `template/skills/init-research-repo/SKILL.md`; no follow-up needed here.
- **Andrea's three style profiles** (`Andrea_Writing_Style_Profile.md`, `Andrea_FMM_Institutional_Style_Profile.md`, `Marta_Writing_Voice_Profile.md`) — content is person/institution-specific; the *pattern* (versioned voice profiles, applied on explicit request only, with `_PLAIN.md` backups) is portable as a meta-skill but isn't on the beta-user critical path.
- **Andrea's Parts C/D/E** (propagation infra, portability evaluation, improvement artifacts) — designed for full-kit-everywhere; doesn't fit on-demand fetch. Exception: Part D's portability framework could ship as a standalone skill if/when claude_researcher opens to community contributions.
