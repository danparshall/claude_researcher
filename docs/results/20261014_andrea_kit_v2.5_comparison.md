<!-- Generated during: convos/20261014_andrea_incoming_pr_review.md -->

# Andrea's starter package v2.5 vs our template skills

Source compared: PR #76 branch `andrea-incoming-starter-v2.5` (commit `cce827c`), `incoming/andrea/` — byte copy of `aflopezluzuriaga/SkillPropagation` `kit/starter_package/` @ `cf9e108` (v2.5, 2026-10-10; mirrors her kit v6.11). Ours: `template/skills/` at `main` `8e81408`.

Method: five parallel read-only agents, one per cluster, each read both sides in full. The orchestrator merged their reports and corrected one pairing (`skill_authoring` ↔ `creating-skills`: `creating-skills` is Dan's local CLI skill, not in `template/skills/`). **Not spot-checked line by line** — re-read the source passage before porting any item.

## Cross-cutting

Her kit is now a prescriptive system: a `FOLDER_MAP.md` in every folder, six hand-maintained typed root indexes, `workspace/` / `workdesk/` / `feedback/` working areas, an archetype declaration, and a propagation pass that pushes kit updates into many repos. Her git model is main-first (work is a folder on `main`; a branch is the exception), where ours is one branch per research line. Most of her new behavior hangs off that structure, so what transfers is mostly rules and ideas, not files.

## Pairs (ours ↔ hers)

**`add-paper` ↔ `materials_processing_skill.md`**: partial counterpart. Hers routes only and processes nothing itself. It sorts three ways: document vs paper ("would it get a BibTeX entry"), then academic vs institutional. Index rows carry a "Claude status" reading recommendation plus a "User status". It has a lookup discipline: index, then summary, then full text. *Take:* the document-vs-paper cut (with #6), maybe the reading-recommendation field.

**`paper-processing-academic` / `-institutional` ↔ hers**: forked from hers @ `e0a736d`; moderate divergence. She made three additions to both. (1) Summary section (e), "From the visual layer": what was learned from figures and tables, where an empty note is still informative. (2) A re-verify loop: a cheaper agent rates each claim supported / imprecise / unsupported / contradicted against the extract, and the summary gets a "Verified against the extract:" line. (3) A language rule: extract in the source language, never summarize from a translation, and a derived English reading copy can't be cited. Storage differs: one summary file per paper, filed via FOLDER_MAPs. *Take:* (e) and the re-verify loop.

**`iterative-writing-workflow` ↔ `writing_skill` + `writing_notes` + `writing_drafting`**: large divergence. Hers is split into a router plus two protocols. New in hers:
- a ~10k-word scale check at outline approval
- a compiled post-hoc outline plus a divergence table (planned vs drafted; intentional / drift / unclear)
- review-round checkpoints: a reminder at 3, insistence at 6
- a branch required for drafting
- notes kept in `writing_notes/` with an index row

*Take:* the scale check, the divergence table, and the round checkpoints.

**`branch-document-review` ↔ `writing_branch_skill.md`**: moderate divergence; the core steps are nearly verbatim. New in hers: a handover lock (no writes to the branch while the user may hold unsaved edits); read-before-edit with exact-string replacement only and a check of bulk-diff line counts; branch mechanics moved into her GitHub skill. Her branch names went back to `may-1` (ours, `MMdd`, sorts correctly; keep ours). *Take:* the lock and the exact-string rule.

**`add-deliverable` ↔ `product_ledger_skill.md`**: not a counterpart. LINEAGE tracks where a number came from (SHA-pinned). The ledger tracks which representation of a product is current (md/docx/pptx/translation) and events git can't see (sent, presented, feedback).

**`brainstorming` ↔ hers**: adapted from ours; she cut phases 3–5. She added "one reactable unit per turn", "the transition is its own turn", and an optional saved summary. *Take:* the turn rules.

**`finish-convo` + `update-docs` ↔ `finish_session_skill.md`**: adapted from ours; hers only sequences other skills. She dropped the push confirmation, the close-out sentinel, and the mid-session checkpoint, so hers can't replace ours. She added: a dangling-reference scan after moves and renames; an "unseen" close for interrupted sessions; reviewed / unreviewed / unseen flags. *Take:* the dangling-reference scan.

**`update-docs` ↔ `repo_conversations_skill.md`**: not a counterpart. Hers is a verbatim, tag-indexed transcript archive kept for retrieval, not for resuming. It would be a new skill if wanted.

**`start-research-line` / `finishing-a-research-branch` ↔ `exploration_branch_skill.md`**: not a counterpart (different git model). Notable: a result that overturns a main claim must not be git-merged, because the merge reports clean while main now contradicts itself. She also reads branches without checking them out.

**`audit-repo-structure` + `audit-status` + `audit-docs` ↔ `repo_audit_skill.md`**: independent overlap. Hers is one skill with 14 checks, about half on structure we lack. *Take:* the two finding classes, "drift fix" vs "requires decision", and the report-only / repair modes. Our `--prune` and false-positive lessons are ahead of hers.

**`task-*` ↔ `project_tracker_skill.md`**: mismatch. She has no GitHub-issue task system. Her tracker is a per-workstream STATUS entry (where it stands / Next / Waits on / Resume) rewritten each session, which conflicts with our rule that STATUS changes only when a line opens or closes. *Maybe:* Waits-on and Known-issues fields; per-entry staleness against commits.

**`write-a-plan` + `handle-large-tasks` ↔ `workstream_plan` + `multisession_task`**: different philosophies. Her "infinite-context test" separates a plan (belongs to the work) from a carryover (exists only because of context limits). Her plans live next to the work with a step table and a "we are here" marker. Scoped mode runs blind sessions with controlled reading scopes. Ours keeps TDD discipline.

**`init-*` + repo layout ↔ `PROJECT_SETUP`, `structure_conventions`, `archetype_conventions`, `research_archetype_spec`, `naming_conventions`, templates (~3.8k lines)**: maximally diverged. Hers uses a questionnaire, archetype triage, and a full skeleton at birth, plus retrofit and propagation modes. It has no `data/` lifecycle and no code scaffold. Our generated paper index, checked by a pre-commit hook, is more reliable than her hand-kept indexes. Her root-level cap: skeleton + at most 2 registered extras.

## Hers with no counterpart

- `agent_research_verification`: raw deep-research output is never citable; only the verification document is. Drafter, researcher, retriever, processor, and verifier work in separate chats. Six verdicts. An unretrieved source is `unverifiable`, never `confirmed`. A `LESSONS.md` accumulates agent failure modes.
- `own_document_verification`: checks your own draft claim by claim against the repo's held sources. It also produces a coverage report of uncheckable claims: cited-not-held / held-not-processed / held-but-silent / no citation.
- `document_processing` (issue #6): for legislation, memos, and terms of reference. Reliability labels, confidentiality tags, a summary that mirrors the source's structure, scanned-PDF detection.
- `github_api_workflow`: assumes no web push. Worth harvesting: a one-commit multi-file recipe via the Trees API; "atomicity is not isolation" (a Trees commit can silently revert a parallel change); the Contents API truncating files at ~1 MB.
- `BLIND_SESSION`, `cross_repo_import`, `skills_curation`, `skill_authoring`: tied to her kit-factory model; a few nuggets each.
- `translation_review` + log: a Spanish naturalness pass whose corrections are distilled into patterns.
- `visuals_workflow`: figure spec as ASCII + prose first, SVG after merge.
- `academic_paper_latex`, `academic_slides`, `latex_round_trip` (Overleaf round trip), `design_deck_reconciliation` (+ python-pptx extractor).
