# claude_researcher — Skill Ports Plan (wave-based)

**Goal:** Get skills shipped to beta users in ship-priority order, with a provenance/sync mechanism in place so the 3-layer propagation chain (Nori SWE → Nori Researcher → claude_researcher) doesn't drift silently.

**Parent plan:** [`01_initial_build.md`](01_initial_build.md) Phases 4.6, 5, and 6. This plan refines the execution order of those phases — it does NOT replace them.

**Originating convos:**

- [`20260509_aitaxbid_skills_audit.md`](../convos/20260509_aitaxbid_skills_audit.md) — surveyed Andrea's kit, identified portable skills
- [`20260509_phase6_skill_port_planning.md`](../convos/20260509_phase6_skill_port_planning.md) — translated audit into Phase 6 task expansions
- This session (to be captured at finish-convo) — established the SWE → Researcher → claude_researcher propagation framing, the "claude_researcher = Nori Researcher + non-CLI tricks" mental model, Andrea-as-collaborator, beta-users-imminent urgency

**Confidence:** Medium-high for Waves 0-2 (well-understood mechanism). Medium for Waves 3-4 (REST adaptation + AITaxBID synthesis have real work). Lower for Wave 5 (sandbox tooling unknowns + document-processing source not yet read in detail).

**Branch:** main (no separate research line — this is build work, not exploration).

**Status (as of 2026-05-09 evening):** Sketched, not started. Execution begins next session. Beta users may start checking the repo soon — time-to-first-usable-skill is a primary constraint.

---

## Why a separate plan

01's Phase 6 lists skill ports as undifferentiated tasks (34-44 + 40a-c). This plan **orders** them by ship-priority and adds two things 01 didn't anticipate:

1. **Provenance + sync infrastructure** for the 3-layer chain. SWE upstream changes propagate through Nori Researcher (which you author) to claude_researcher (which you author). Without provenance stamps, drift is invisible.

2. **Wave-based shipping** so beta users hit working skills early rather than a fully-finished kit late. SKILL_INDEX.md's current state (URLs that 404 until Phase 6 ships) is a poor first impression — Wave 1 fixes that within ~2 hours of work.

This plan also assumes:

- You maintain the **Nori Researcher** skillset upstream (you're the author).
- You **do not maintain** the Nori SWE skillset (someone else does at Nori).
- Andrea Lopez-Luzuriaga is a **collaborator** on this repo, but her AITaxBID kit has its own upstream maintained separately by her.

---

## Provenance + sync architecture

### Frontmatter convention

Every ported `SKILL.md` carries one of three provenance fields in its YAML frontmatter:

```yaml
---
name: test-driven-development
description: ...
nori_swe_source: ~/.claude/skills/test-driven-development/SKILL.md
nori_swe_sha: <git-sha-of-source-at-port-time>
---
```

```yaml
---
name: finish-convo
description: ...
nori_researcher_source: ~/.claude/skills/finish-convo/SKILL.md
nori_researcher_sha: <git-sha>
---
```

```yaml
---
name: branch-document-review
description: ...
aitaxbid_source: ~/code/AITaxBID/skills/BranchWorkflow_Skill.md
aitaxbid_sha: <git-sha>
---
```

The `<sha>` is the SHA of the source file in its repo at port time. `git log -1 --format=%H -- <path>` gives it. Stamping with `git rev-parse HEAD:<path>` is also fine — pick one and stay consistent.

**Why three flavors?** Different upstream maintainers, different drift-handling. SWE drifts you didn't cause; Researcher drifts you did; AITaxBID drifts Andrea did.

### Sync script (Wave 0)

`template/scripts/sync_carryovers.sh` (or `.py` if you prefer Python — Dan's preference per global CLAUDE.md leans Python for non-trivial). Reads a list of SWE-carryover skill names; for each one, copies `~/.claude/skills/<skill>/SKILL.md` → `template/skills/<skill>/SKILL.md`, captures the source SHA, stamps it into the frontmatter.

Run when you notice SWE upstream has moved. Idempotent. Doesn't touch Researcher-derived or AITaxBID-derived skills.

### Drift-check script (Wave 0)

`template/scripts/check_drift.py`. For each skill in `template/skills/`, reads the provenance frontmatter, compares the stamped SHA against the current upstream SHA, prints a list of "these need attention." **Doesn't auto-update** — surfaces work for you to act on. Run periodically; could be a pre-commit hook later.

---

## Waves

### Wave 0 — Provenance + sync infrastructure (~1 hour)

**Ship criterion:** sync_carryovers + check_drift exist and run cleanly against an empty `template/skills/`.

- W0.1 Add `nori_swe_source` / `nori_researcher_source` / `aitaxbid_source` to the SKILL.md frontmatter convention. Document in `template/skills/SKILL_INDEX.md` (top of file, "Provenance" section).
- W0.2 Write `template/scripts/sync_carryovers.sh` (or `.py`). Reads a list of SWE carryover names; copies + stamps from local Nori install. Idempotent.
- W0.3 Write `template/scripts/check_drift.py`. Walks `template/skills/`, reads provenance frontmatter, compares stamped SHA against current upstream SHA, prints diff summary. No auto-update.
- W0.4 Commit: `Wave 0: provenance + sync infrastructure`.

### Wave 1 — SWE carryovers (~1-2 hours) — **SHIPS FIRST**

**Ship criterion:** beta user opening a session sees `SKILL_INDEX.md` with working URLs for all 9 carryover skills. Pure-thought skills work immediately because they don't touch any of the 8 environmental axes.

Skills (all from `~/.claude/skills/`):

- `brainstorming`
- `test-driven-development`
- `testing-anti-patterns`
- `systematic-debugging`
- `root-cause-tracing`
- `creating-debug-tests-and-iterating`
- `receiving-code-review`
- `write-a-plan`
- `handle-large-tasks`

Tasks:

- W1.1 Run `sync_carryovers.sh` to populate `template/skills/<skill>/SKILL.md` for all 9 carryovers with provenance stamped.
- W1.2 Spot-check each: any internal file-path references that assumed local filesystem? (Most won't; flag exceptions.) Adjust as needed.
- W1.3 Update `SKILL_INDEX.md` — confirm the 9 entries point at the now-real URLs; remove the "URLs 404 until Phase 6 lands" stub language at the top.
- W1.4 Commit: `Wave 1: SWE carryovers shipped (9 skills)`.

### Wave 2 — Session lifecycle (~2-3 hours) — **CRITICAL**

**Ship criterion:** beta users can complete a session end-to-end. Without these, the runtime can't checkpoint progress and STATUS.md / RESEARCH_LOG.md never get written.

Skills:

- `finish-convo` (REST-adapt; replace `git add`/`commit`/`push` with sequential `write_update()` calls)
- `update-docs` (same shape, no separate commit step — every PUT is a commit on REST)

Tasks:

- W2.1 Port `finish-convo` from `~/.claude/skills/finish-convo/SKILL.md`. Embed REST recipes inline (Phase 5 helpers come later). Stamp `nori_researcher_source` + SHA. Note in skill body: "produces ~3 commits per session-end on Contents API; v2 atomic-commit helper will collapse this."
- W2.2 Port `update-docs` from `~/.claude/skills/update-docs/SKILL.md`. Same shape.
- W2.3 Smoke-test: in a fresh claude.ai chat, run a session that ends with finish-convo. Verify: convo summary written, RESEARCH_LOG.md updated, STATUS.md "Recent sessions" updated, all via REST.
- W2.4 Update `SKILL_INDEX.md` entries.
- W2.5 Commit: `Wave 2: session lifecycle (finish-convo, update-docs)`.

### Wave 3 — Knowledge management (~4-5 hours)

**Ship criterion:** beta users can add papers, audit their structure. The repo becomes useful for actual research work.

Skills:

- `add-paper` (download mode + Protocol B fold-in from AITaxBID — see 01 task 36 expanded)
- `add-paper` (orphan ingestion mode — see 01 task 37)
- `audit-docs` (read-only, simpler)
- `audit-papers` (read-only, with orphan-PDF detection that hands off to add-paper orphan mode)

Tasks:

- W3.1 Port `add-paper` download mode from `~/.claude/skills/add-paper/SKILL.md`. **Fold in Andrea's Step 0 academic-vs-institutional triage and Protocol B summary structure** per 01 task 36. Naming: `paper_naming.academic_format` + `paper_naming.institutional_format` in `personal_info.md`. Stamp BOTH `nori_researcher_source` (for the workflow shape) AND `aitaxbid_source` (for the Protocol B additions). First skill with dual provenance — sets the precedent for any future synthesis ports.
- W3.2 Port `add-paper` orphan ingestion mode (extend the same skill).
- W3.3 Port `audit-docs`. Read-only; mostly straight `read_file` + `list_dir` calls.
- W3.4 Port `audit-papers`. Same shape; add orphan-PDF detection.
- W3.5 Verify `pypdf` availability in claude.ai sandbox (existing 01 task 31 dependency). If not pre-installed, document the `pip install` requirement in the skill body.
- W3.6 Update `SKILL_INDEX.md` entries.
- W3.7 Commit: `Wave 3: knowledge-management skills (add-paper × 2, audit-docs, audit-papers)`.

### Wave 4 — AITaxBID Tier A (~3-4 hours)

**Ship criterion:** beta users have access to the writing workflow and the document-review pattern that especially fits the claude.ai web-UI audience.

Skills:

- `writing-skill` (low-friction port; AITaxBID source ~169 lines)
- `branch-document-review` (real REST adaptation for the diff axis)

Tasks:

- W4.1 Port `writing-skill` from `~/code/AITaxBID/skills/writing_skill.md`. Strip Andrea-specific examples; normalize frontmatter. Stamp `aitaxbid_source` + SHA. ~1 hour.
- W4.2 Decide branch-document-review diff approach (open question from 01): GitHub Compare API vs. read-both-and-difflib. Slight preference for Compare API.
- W4.3 Port `branch-document-review`. Real REST adaptation — replace `git diff` with chosen mechanism. Light/heavy review distinction ports verbatim. **Pandoc regeneration step gated on sandbox-tooling check**: if pandoc unavailable, ship v1 without regeneration + a TODO. ~2-3 hours.
- W4.4 Update `SKILL_INDEX.md` — add new "Writing & document workflow" group between knowledge-management and working-style.
- W4.5 Commit: `Wave 4: AITaxBID Tier A (writing-skill, branch-document-review)`.

### Wave 5 (deferred) — document-processing + init-research-repo

**Defer until specific need.** `init-research-repo` is bootstrap-only (not normally invoked at runtime); `document-processing` requires reading 277 lines of source first. Neither is on the beta-user critical path.

Skills:

- `document-processing` (AITaxBID source not yet read in detail)
- `init-research-repo` (Nori Researcher source; bootstrap-only)

Tasks (when scheduled):

- W5.1 Read AITaxBID `document_processing.md` in full (3-4 hours including port).
- W5.2 Port `init-research-repo`. Mostly a wrapper over Phase 5's `create_repo.py` + `seed_repo.py`.

---

## Phase 5 helpers — when to land

01's Phase 5 (helper scripts: `rest_helpers.py`, `create_repo.py`, `seed_repo.py`, `extract_pdf_text.py`) is **NOT** prerequisite for shipping skills. Wave 2-4 skills can embed REST recipes inline using the Custom Instructions recipes the smoke-test agent already proved.

**Recommended timing:** start Phase 5 helpers between Wave 2 and Wave 3, OR after Wave 3. Reason: by then you'll have 4 REST-adapted skills with embedded recipes, and the patterns to extract will be obvious. Refactor the embedded recipes into helper calls in a single follow-on commit per skill.

This trades a small amount of refactor work later for a meaningfully faster ship of Waves 1-3.

---

## Phase 4.6 CLAUDE.md retrofit — when to interleave

The five Tier B/C universal rules from the AITaxBID audit (tracker-not-past-chats, 3+-repetition codification, Parking Lot, "do not infer — ask," show-before-committing universalized) belong in `template/CLAUDE.md`. ~30-60 min of focused edits.

**Recommended timing:** after Wave 1, before Wave 2. CLAUDE.md gets one cohesive update that lands when there are real skills for it to coordinate.

---

## Ship-readiness criteria summary

| Wave | What proves it shipped |
|---|---|
| **0** | `sync_carryovers` and `check_drift` exist; run without error against empty `template/skills/` |
| **1** | 9 carryover SKILL.md files exist with provenance stamped; SKILL_INDEX URLs resolve; agent in fresh chat can fetch one and use it |
| **2** | Session in fresh chat ends with finish-convo; convo summary + RESEARCH_LOG + STATUS.md updated via REST |
| **3** | Paper added end-to-end (download → text extract → index update); audit-docs and audit-papers run read-only without error |
| **4** | writing-skill produces the two-protocol thinking/drafting flow; branch-document-review correctly identifies bracketed comments in a test diff |
| **5** | (deferred — defined when scheduled) |

---

## Open questions specific to this work

- **Sandbox tooling matrix.** Which Python packages are pre-installed in claude.ai's sandbox? `pypdf` (Wave 3), `pandoc` (Wave 4), `python-docx` (Wave 5). Worth a single 30-min consolidated check before Wave 3 → record in `template/reference/SANDBOX_TOOLING.md`.
- **`branch-document-review` diff approach.** GitHub Compare API vs. read-both-and-difflib. Decide at start of Wave 4. Slight preference for Compare API.
- **`raw.githubusercontent.com` allow-list miss at BOOTSTRAP Step 8** (carry-forward from 01's Open Questions). Independent of skill ports but might surface during Wave 1's smoke-testing of carryover URLs. Investigate then.
- **Synthesis-skill provenance pattern.** Wave 3's `add-paper` will be the first skill with TWO provenance sources (Nori Researcher + AITaxBID). The frontmatter convention needs to handle this cleanly. Decision: allow multiple provenance fields per skill; `check_drift.py` checks all of them.
- **SKILL_INDEX.md trimming during transition.** Currently lists 14 skills; only 0 are ported. Beta users hitting the repo before Wave 1 lands could see misleading availability. **Mitigation:** before any beta user is told about the repo, trim SKILL_INDEX.md to only list ported skills + a note that the kit is in active development. Wave 1 commits would re-add carryover entries.
- **Provenance for skill expansions over time.** When you fix a bug in Nori Researcher's `finish-convo` and want it to flow to claude_researcher's REST-adapted version: do you re-port (re-stamp SHA, possibly losing claude.ai-specific tweaks) or merge selectively? Recommend selective merge with stamped SHA bumping; document the workflow when the first such update happens.

---

## What this plan deliberately does NOT cover

- **Phase 9 collaborator walkthrough** (the meaningful real-world test). Independent of skill work; runs in parallel as candidate availability lines up.
- **Phase 4.5 collaborator mode (v1.1).** Out of scope for v1.
- **Per-user-repo `CLAUDE_TEMPLATE.md`.** Open question; revisit after Wave 4.
- **Atomic-commit Git Data API helper** (v2 work). Skills in v1 accept multi-commit-per-write.
- **Skill-level testing infrastructure.** Smoke-test-in-real-chat is the v1 test. Unit tests for skills aren't planned.
