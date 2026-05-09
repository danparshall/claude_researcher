# claude_researcher — Phase 4: CLAUDE.md + SKILL_INDEX stub

**Date:** 2026-05-09 (same day as Phase 3 production)
**Repo:** claude_researcher
**Plan:** [docs/plans/01_initial_build.md](../plans/01_initial_build.md) — Phase 4 (tasks 19–26) + Phase 6 task 43 (SKILL_INDEX stub) + Phase 4.5 (new v1.1 stub authored this session)

## Summary

Wrote the production `template/CLAUDE.md` for Phase 4 — the runtime spine every research session loads. 7 numbered sections (calibration, session-start fetch, branch resolution, project confusion, runtime workflow, wrap-up, issue reporting) plus appendix and a known-v1-limitations section. Brainstorming surfaced one architecture pivot during execution: **the PAT and curl recipes belong in the Project's Custom Instructions field, not in an uploaded `_PROJECT_INSTRUCTIONS.md` file** — the consequence flowed through to BOOTSTRAP.md (Step 10 collapsed onto a single Custom Instructions paste; the file-upload subsection deleted; Step 11 cause list updated) and to the canonical CLAUDE.md (which now treats Custom Instructions as the authoritative credential location). Also wrote a `SKILL_INDEX.md` manifest stub so CLAUDE.md's session-start fetch sequence has a real target while per-skill SKILL.md files wait for Phase 6, and authored a new Phase 4.5 plan section spec'ing collaborator mode for v1.1 (direct-collaborator on private repo, narrower than fork-based or org-based alternatives).

The session followed Phase 3's pattern: brainstorm-first (3 question rounds plus a real-time scope correction), then ship the MVP. Dan's "let's do MVP and see what feedback we get" mid-session signal locked in solo-only v1 with collaborator support cleanly deferred.

## Work Done

- **Brainstorming convo (3 question rounds):**
  - Round 1: branch model — Model A (git branches per research line) is default; Model B (main_only) is an opt-in for solo repos. Field lives in research repo's STATUS.md as a top-of-file `workflow_mode` value (default `branches` if absent).
  - Round 2: section order (Order B — calibration first) and calibration style (centralized + inline tier reminders).
  - Round 3: PAT placement (Custom Instructions, not file). This turned into a real architecture pivot.
  - Real-time scope correction: Dan flagged that the grad-student/professor model breaks the OWNER==USERNAME assumption. Discussed three collaborator paths (direct-collaborator vs fork vs GitHub org) and settled on direct-collaborator for v1.1 with the other two as later options.
- **Phase 4 production (`681ed9d`):**
  - `template/CLAUDE.md` — ~330 lines. Calibration-first ordering. `(novice: explain X; fluent: just do it)` inline reminders at branch creation, file delete, archive, PR merge, and force-op gates. Forward-compat hedge in §6 step 2: 405/422 from PR-merge stops the flow gracefully, so collaborator mode is a small additive change in v1.1 rather than a rewrite. Known v1 limitations explicitly listed: no collaborator mode, no atomic commits, no auto branch protection, skills pinned to `main`.
  - `template/skills/SKILL_INDEX.md` — manifest stub. URLs 404 until Phase 6 ports each skill, but the contract (name + trigger + URL, grouped by lifecycle role) is locked. Listed: 3 lifecycle, 3 knowledge-management, 9 working-style; plus 7 explicitly-not-ported with rationale.
  - `template/BOOTSTRAP.md` Step 10 collapsed onto Custom Instructions paste — file-upload subsection deleted, "don't upload as file" call-out added, verification affordance switched to "spot-check no literal placeholders remain".
  - `template/BOOTSTRAP.md` Step 11 cause list updated — removed "file not uploaded" cause and the "Phase 4 hasn't shipped" cause; added "CLAUDE.md upstream URL unreachable" with CDN propagation note.
  - `template/_PROJECT_INSTRUCTIONS.md.template` — URL fix: `/main/CLAUDE.md` → `/main/template/CLAUDE.md` to match BOOTSTRAP.md and the still-unsettled Phase 10 publish strategy.
  - `docs/plans/01_initial_build.md` — task 26 wording updated to reflect the architecture pivot; new Phase 4.5 section appended spec'ing v1.1 collaborator mode (6 sub-tasks: OWNER/USERNAME split, BOOTSTRAP joining-vs-creating branch, branch protection in seed_repo.py, role field in personal_info.md, wrap-up flow split, PAT scope guidance for collaborators).

## Decisions Made

- **CLAUDE.md is calibration-first.** Section §1 reads `git_fluency` (fetched in §2) and sets the verbosity dial before everything else. Inline tier reminders at sensitive boundaries (branch creation, archive, merge, force) act as cheap insurance against drift in long sessions.
- **Novice tier is explicitly pedagogical with promotion path.** Translates every git concept inline ("a branch is like a separate workspace…"), checkpoints under the hood without asking, and after several comfortable sessions can suggest the user update their `git_fluency` to `occasional`. Designed for the professor + grad student model where a new student is novice and the agent slowly upskills them.
- **Workflow modes: `branches` (default) vs `main_only` (opt-in).** Each research line is a git branch by default; solo repos that don't want PRs can flip to `main_only`. The mode is a top-of-file field in the research repo's STATUS.md. Wrap-up §6 has different paths per mode.
- **PAT in Custom Instructions, not file.** Custom Instructions are in every chat's context from the very first message — the agent has credentials and recipes before any fetch happens. Strictly better than file-upload for an authentication-bearing payload. The canonical Custom Instructions text is `_PROJECT_INSTRUCTIONS.md.template` with TOKEN/USERNAME/REPO substituted; the bootstrap WebFetches it, substitutes, and instructs the user to paste.
- **§6 wrap-up handles protected `main` gracefully (forward-compat for v1.1 collaborator mode).** Step 2 of the merge flow distinguishes 200 (proceed) from 405/422 (branch protection, surface PR URL and stop). Solo case = self-merge. Collaborator case = open-and-stop. The directory move to `docs/historical/` is a separate session for the owner. This means v1.1 collaborator mode is additive (split OWNER/USERNAME, add joining-vs-creating bootstrap branch, add branch protection in seed_repo.py) rather than rewriting CLAUDE.md.
- **v1.1 collaborator path is direct-collaborator, not fork or org.** Direct-collaborator (professor adds student as collaborator on their personal repo) keeps a single source of truth (one STATUS.md, one `docs/active/`), works with fine-grained PATs scoped to a repo the user doesn't own, and matches the "shared lab notebook" mental model. Forking is heavier (each fork drifts; cross-fork PRs); GitHub orgs are cleaner at scale (defer to v2.0).
- **`personal_info.md` schema for upskilling: just track current `git_fluency` tier.** Agent observes user comfort and suggests promotion at appropriate moments; user accepts manually. No target field, no session counter — YAGNI for v1.

## Bugs / Friction Surfaced

- **`_PROJECT_INSTRUCTIONS.md.template` had wrong CLAUDE.md URL** (`/main/CLAUDE.md` instead of `/main/template/CLAUDE.md`). Fixed in this session's commit. Caught by the "verify URL consistency across files" pre-draft scan.
- **STATUS.md "Phase 3 caveats" subsection is now stale** — the caveats (Step 10 placeholder, Step 11 cause #5) are resolved by Phase 4 shipping. Should be removed in this session's STATUS.md update.
- **Nori `commit-author.js` hook still mangles commit messages** with literal `\n\n` instead of newlines. Persistent across all today's commits. Cosmetic only. Upstream issue still un-filed; tracked across multiple repos.

## Open Questions (carry-forward)

- **Phase 5 vs Phase 6 ordering.** Phase 5 = Python helper scripts in `template/scripts/` (`rest_helpers.py`, `create_repo.py`, `seed_repo.py`, `extract_pdf_text.py`). Phase 6 = port each upstream Nori SKILL.md and adapt to REST. The two phases interleave: skills call the helpers, but skills also stand on their own as documents. Likely sensible to do Phase 5 first (so skills have helpers to call) but worth confirming when next session opens.
- **Real-world test of CLAUDE.md.** Phase 3's lesson was that incognito claude.ai chats validate orchestration patterns surprisingly well, and that "treat as if I typed" framing backfires. Phase 4's CLAUDE.md needs a similar smoke test before Phase 5/6 build on top of it. Likely a ~30-minute session: open a fresh claude.ai chat in a Project, paste the canonical Custom Instructions text (with real PAT/USERNAME/REPO), and see whether the agent fetches CLAUDE.md, follows the §2 sequence, and greets the user correctly. Surfaced behaviors will inform any §1 / §2 fixes.
- **Collaborator mode v1.1 timing.** Phase 4.5 spec is committed but not scheduled. The natural trigger is when Dan's first real collaborator (a grad student or professor) needs the workflow. Until then, v1 ships with the limitation documented and collaborators wait. Not a v1 blocker.
- **Phase 10 publish strategy still undecided.** URLs throughout BOOTSTRAP.md, CLAUDE.md, SKILL_INDEX.md, and `_PROJECT_INSTRUCTIONS.md.template` use `.../main/template/<file>` paths. Phase 10 picks between flipping dev repo as-is, restructuring (`template/` → root + dev files into `_dev/`), or separate public repo. Punt continues.
- **Skill SHA pinning vs. `main`.** SKILL_INDEX.md URLs point at `main`. If a skill ships a breaking change, in-flight Project files keep their CLAUDE.md fetch from `main` and could break. YAGNI for v1; revisit when first real bug surfaces.

## What's Next

**Phase 5 — helper scripts (`template/scripts/`)** is the natural next phase. Then Phase 6 — port and adapt skills. Phase 5 first means skills have working helpers to call; Phase 6 first means skill bodies are written and helpers slot in later. Slight preference for Phase 5 first, but worth confirming.

**Real-world test of CLAUDE.md** is a smaller pre-Phase-5 session — paste the Custom Instructions into a fresh claude.ai Project and watch the runtime agent's first session unfold. Same shape as Phase 3's incognito-chat smoke tests. Likely surfaces small fixes to §1 / §2 / §3 before the heavier Phase 5/6 work builds on top.
