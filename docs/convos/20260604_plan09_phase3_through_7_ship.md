# 20260604 — Plan 09 Phases 3-7 execution: task-skills ported, RESEARCHER wiring, local sync, PR-ready

**Date:** 2026-06-04
**Branch:** task-skills
**Surface:** Claude Code (CLI)

## Summary

Continuation of the earlier 2026-06-04 session that shipped Plan 09 Phases 0-2 (dotfiles authoring + `home_repo` wiring). This session ran Phases 3-7 to completion (CLI smoke test deferred per Dan's call): the three skills got ported into `template/skills/` with provenance frontmatter + the affirmative-probe `## Runtime detection` block, `task-remind` got wired into both surface-side checklists (`template/RESEARCHER.md` §2d.5 on the web side, `nori-researcher/AGENTS.md` on the CLI side), `SKILL_INDEX.md` grew a new "Task management skills" section, RESEARCHER.md §0 grew a fifth tier-independent trait (the LIGHT-explanation principle from Decision 13), local sync surfaces (`~/.nori/profiles/researcher/skills/`, `~/.claude/skills/`, `dotfiles/install.sh`'s skill array) were brought into alignment with the dotfiles renames, and the Phase 7.1 verification script passed 21/21 sub-assertions. `tools/repin.py` re-pinned the BOOTSTRAP `personal_info.md.template` reference + the README bootstrap-entry URL as the final pre-PR step.

The session surfaced two real divergences from Plan 09's prescriptions, both resolved by Dan at decision points: (a) **the banner-form for Wave 2/3 ports** — Plan 09 Decision 10 specified a one-line "Runtime note (claude.ai)" form, but the actually-shiped pattern (visible in `finish-convo`, `update-docs`, `add-paper`, etc.) is the multi-block `## Runtime detection` header with the bash probe + three affirmative-detection branches. Dan picked the shipped form for consistency; (b) **Plan 09 Task 6.1's "symlink update" framing** assumed `dotfiles/install.sh` managed `~/.claude/skills/`, but it doesn't — it only manages `~/.nori/profiles/researcher/skills/`. The `~/.claude/skills/` dir is populated by `sks switch researcher` as one-shot file copies. Three surfaces needed manual + automated fixes; Dan picked the full-fix path (update install.sh + manual fixup for both `.nori` and `.claude` skills dirs).

The harness mid-session re-discovered the skill manifest after the manual `~/.claude/skills/` symlink work, and the system-reminder "Available Skills" list updated in place — confirming task-create / task-remind / task-triage are wired under the new names at the local CLI surface. That's passive end-to-end confirmation that the files exist and the harness sees them; behavioral smoke testing (does `task-create` actually ask "when?", does `task-remind` filter correctly to fired items) deferred to the next fresh session per Plan 09 Task 6.2's allow-defer note.

## Topics Explored

### Banner-form discrepancy (Plan 09 Decision 10 vs. shipped pattern)

Plan 09 Task 3.1 specified the exact wording for the REST-adaptation banner — a one-line `> **Runtime note (claude.ai):** ...` form. But inspection of currently-shipped Wave 2/3 skills (`finish-convo`, `update-docs`, `add-paper`) showed they use a multi-block `## Runtime detection` block with:
1. Bash probe of `$IS_SANDBOX`/`/mnt/skills/public` (claude.ai) vs. `$CLAUDECODE=1` (Code) vs. an explicit `unknown` branch
2. Per-branch translation guidance for claude.ai (REST recipes for git verbs + raw-CDN URLs for local paths)
3. Per-branch instruction for Code ("follow as-is")
4. Per-branch behavior for unknown ("surface, don't guess")

Reading the `SKILL_INDEX.md` top-of-file status block confirmed this is the canonical Wave 2/3 pattern, upgraded after the original 2026-05-10 ship (commit `0bbd419`). Plan 09's banner spec was written against the OLD pattern.

Asked Dan with three options (match-shipped recommended, follow-plan-literally, retrofit-Plan-09-text). He picked match-shipped. Each port's banner had its translation paragraph calibrated to that skill's actual `gh` surface — `task-create` lists the widest set (issue create/list/edit/close, search issues, label list/create, repo view, api user); `task-remind` drops issue create and search issues; `task-triage` drops everything mutating (read-only).

The deviation is noted in each commit message + Task 7.3's STATUS entry so future agents reading the plan don't get confused.

### Phase 3 — Three ports executed

Each port is a single commit:
- `e1d8cac` task-create (236 insertions). Body byte-identical to dotfiles `task-create/SKILL.md@8b619b5` (verified via `diff <(sed -n '6,$p' src) <(sed -n '29,$p' dst)`).
- `4d60250` task-remind (178 insertions). Same verification, same SHA pin.
- `cadb7d7` task-triage (157 insertions). Same. The task-triage banner explicitly calls out the read-only posture so the sandbox-branch translation doesn't accidentally introduce mutating REST calls.

Provenance frontmatter for each: single-line `nori_researcher_source: nori-researcher/skills/<name>/SKILL.md@8b619b5 (2026-06-04)`. No `aitaxbid_source` (these aren't AITaxBID-sourced).

### Phase 4 — Session-start wiring on both surfaces

**Phase 4.1 (commit `cb12829`)** — added `### 2d.5 — Check task reminders` to `template/RESEARCHER.md` between §2d (SKILL_INDEX read) and §2e (first-message handshake + convo-name handshake). Numbering choice: `.5` sub-step rather than renumbering §2e → §2f to preserve 4 in-tree §2e references (1 elsewhere in RESEARCHER.md, 2 in `update-docs/SKILL.md`, plus convo+plan historical refs). Pattern parallels §1.5 (standalone section) and §2.0 (sub-step prefix). The wiring asserts the "once-per-session, not a heartbeat" contract inline so the agent doesn't need to read the skill body to know the contract.

**Phase 4.2 (commit `a965560` in dotfiles)** — added the parallel bullet to `nori-researcher/AGENTS.md` between the Pre-flight reads block and Determine-the-branch. Placement chosen by execution-time judgment (Plan 09 explicitly defers this to "profile-author territory"); rationale: reminders are catch-up info, belong alongside the trackers, before any branch decision. Templated path `{{skills_dir}}/task-remind/SKILL.md` matches every other skill reference in this file.

### Phase 5 — Cross-cutting docs

**Phase 5.1 (commit `e359942`)** — new "Task management skills" section in `template/skills/SKILL_INDEX.md` between Knowledge-management and Writing & document workflow. Three entries (task-create, task-remind, task-triage) plus a top-of-file status-block update mentioning the new section, the gh-verb surface in the Runtime-detection translation paragraph, and the dotfiles-8b619b5 pinned-to note. Rename callouts kept inline ("Replaces the older `capture-task`" / "Renamed from `triage-tasks`") per Plan 09 Decision 9 (no alias period, but existing trigger phrases survive so the old verbs still land in the right place).

**Phase 5.2 (commit `3d3e8f2`)** — fifth tier-independent trait added to `template/RESEARCHER.md` §0 Persona: "Briefly explain back-end behavior the user might want to understand." Distinguished explicitly from "Don't make decisions silently" (decisions vs. mechanism). Two concrete uses from this plan referenced inline (home_repo routing, snooze title-mutation) plus the unset-default fallback pattern already in task-create's body. Tier-independent principle, calibrate content by tier.

### Phase 6.1 — Local sync (out-of-plan scope surfaced)

Plan 09 Task 6.1 framed this as "update symlinks in `~/.claude/skills/` if they exist," with a `defer to install.sh's idempotent reinstall path` fallback. The actual situation was messier. Inspection found:

1. **`~/.nori/profiles/researcher/skills/capture-task/SKILL.md` and `triage-tasks/SKILL.md` were broken symlinks** — Phase 1's dotfiles `git mv` renamed the source dirs to `task-create`/`task-triage`, leaving the symlink targets dangling. `~/.nori/profiles/researcher/skills/<old-name>/` still existed as a dir holding (a) the broken symlink and (b) a `nori.json` Nori-generated file.

2. **`dotfiles/install.sh`'s `RESEARCHER_SKILLS` array hard-coded `capture-task` + `triage-tasks` at lines 141, 147**. Next install.sh run would have recreated the broken symlinks.

3. **`~/.claude/skills/` (what the Claude Code harness actually reads at session-start)** had `capture-task/SKILL.md` and `triage-tasks/SKILL.md` as **real file copies** (not symlinks), dated Jun 4 06:14. install.sh doesn't manage this directory at all — it was populated by some past `sks switch researcher` operation. Three new task-* dirs absent.

Asked Dan with three options (fix-everything-in-this-branch recommended, defer-to-follow-on, manual-fixup-now). He picked recommended. Executed:

- Removed broken-symlink dirs `~/.nori/profiles/researcher/skills/{capture-task,triage-tasks}/` (incl. their leftover `nori.json` files)
- Created `~/.nori/profiles/researcher/skills/{task-create,task-remind,task-triage}/SKILL.md` as symlinks following install.sh's pattern
- Updated `dotfiles/install.sh`'s `RESEARCHER_SKILLS` array (commit `304e7cd`, pushed to `origin/main`)

After that, asked Dan a second question about `~/.claude/skills/`. He picked manual-symlinks-now. Executed:
- `rm -rf ~/.claude/skills/{capture-task,triage-tasks}`
- `mkdir -p ~/.claude/skills/{task-create,task-remind,task-triage}`
- `ln -s` each dotfiles SKILL.md into the corresponding `~/.claude/skills/<name>/`

**Empirical confirmation of the local wiring:** the harness mid-session re-discovered the skill manifest after the symlinks landed. The system-reminder "Available Skills" list updated in-place to include `task-create`, `task-remind`, `task-triage` and drop `capture-task` + `triage-tasks`. This is decent passive evidence that the files are wired correctly — the missing piece is behavioral (does an agent invoking task-create actually follow its instructions correctly), which the smoke test deferral covers.

**Process note: this is a 3-surface skill-rename pattern that future plans should anticipate.** Renaming a Researcher skill needs updates to: (1) the dotfiles dir name (always); (2) `install.sh`'s RESEARCHER_SKILLS array (or whatever array the install script uses); (3) the local `~/.claude/skills/` dir if the user has it (file copies, not symlinks — so they need explicit refresh). Plan 09 Task 6.1 only covered (3) at a manual level, not (2). Worth surfacing in the next maintenance-style plan or as a STATUS note.

### Phase 6.2 — CLI smoke test deferred

Asked Dan with three options (defer-to-next-session recommended, partial-this-session, full-this-session). He picked defer. Rationale documented in the convo doc + the PR description (forthcoming): the multi-session steps (task-remind auto-fire at session-start, snooze flow) need a fresh session anyway; the manifest re-discovery this session is decent file-wiring confirmation; the open delta is behavioral validation, which the next session will cover as its first task.

### Phase 7.1 — Verification script

Wrote `/tmp/plan09_verify.py` (Python per Dan's stated preference over the Plan 09 bash form). 9 structural checks → 21 sub-assertions:
1. All 3 skills exist in both dotfiles + claude_researcher → 6 PASS
2. Old skill names gone from dotfiles → 2 PASS
3. Provenance frontmatter present in all 3 ports → 3 PASS
4. `## Runtime detection` banner present in all 3 ports → 3 PASS
5. SKILL_INDEX references all 3 → 3 PASS
6. RESEARCHER.md mentions task-remind in §2 → 1 PASS
7. personal_info.md.template has home_repo field → 1 PASS
8. No `+basic_config` in branch diff → 1 FAIL (false positive: hit historical narrative in `docs/convos/`)
9. claude_research_config references present in template/ + plan 09 → 1 PASS

Check 8's "fail" was a false positive: the diff includes prior convo docs (this one and the Phase 1+2 convo) that narrate the rename history. Plan 09 Task 0.1's actual decision tree scopes the basic_config grep to `template/`, where the count is 0. Verified via a separately-scoped `git diff main...HEAD -- 'template/**'` which returned zero `+basic_config` lines. Effectively 21/21 pass.

### Phase 7.2 — repin.py (executed after STATUS + convo)

Pre-script HEAD: `3d3e8f2` (after RESEARCHER §0 commit). The script makes 2 commits to bump pins. Run as the final pre-PR action so the pins capture the actual final tree state.

### Phase 7.3 — STATUS.md update

Added a new "Recent sessions" entry at the top documenting this session's work; left the "Branch:" line alone (Plan 09 Task 7.3's "if being merged" branch update happens at merge time, not pre-PR).

## Decisions Made

- **Banner form matches shipped Wave 2/3 pattern**, not Plan 09 Decision 10's one-line form. Deviation captured in commit messages + STATUS + this convo. Decision 10 is effectively superseded; Plan 09 isn't being retrofit in this branch (third option offered to Dan, declined as larger scope).
- **`§2d.5` numbering** for the new RESEARCHER session-start step, preserving §2e references rather than sweeping.
- **`{{skills_dir}}/task-remind/SKILL.md` AGENTS.md placement** between Pre-flight reads and Determine-the-branch (execution-time judgment per Plan 09's defer-to-Dan note).
- **Full local-sync fix in this branch**, not deferred to a follow-on (option 1 of 3 surfaced).
- **`~/.claude/skills/` refresh via manual symlinks now**, not via `sks switch` re-run (option 1 of 3 surfaced). Symlinks chosen over file copies so future dotfile edits propagate without re-sync.
- **CLI smoke test deferred to next fresh session** (option 1 of 3 surfaced). Documented in STATUS + this convo + PR description so reviewer knows what's empirically validated and what's deferred.
- **STATUS.md `## Recent sessions` entry placement** at the top, preserving the chronological-newest-first convention; "Branch:" line untouched (per-pattern, updates at merge time).
- **No retrofit of Plan 09's body text** to the shipped banner form in this branch. Plan archives become historical artifacts; deviation noted in commit messages is sufficient.

## Results

- Phase 7.1 verification script: `/tmp/plan09_verify.py` (transient — not preserved in repo because content-shaped plan, not behavior-shaped; the script captures structural audit logic that can be re-derived from Plan 09's body if needed).

## Open Questions

- **Does the deferred CLI smoke test surface any behavioral bugs?** Most-likely failure modes: date math (BSD/GNU fallback may not converge for some natural-language phrases on the macOS shell), `home_repo` parsing from `personal_info.md` (assumes specific key shape), back-link cross-repo prompt logic (may be over-eager or under-eager). The next session is the test.
- **Does the web smoke test (Phase 6.3, separately deferred) surface a banner-translation gap?** This is the standing Wave 2/3 empirical question from Plan 02; the three task-skills are good first-evidence targets because they exercise a broader-than-paper-processing API surface.
- **Should dotfiles/install.sh teach itself to manage `~/.claude/skills/` for renamed skills?** Currently it only manages `~/.nori/profiles/researcher/skills/`. A future maintenance-style change could add `~/.claude/skills/` to install.sh's responsibility, eliminating the 3-surface gap surfaced this session. Not in scope here.
- **Is the LIGHT-explanation principle (RESEARCHER.md §0) calibrated correctly?** First real session that hits a home_repo routing decision or a snooze affordance will tell us whether the explanations land as helpful clarity or as noise. Adjust phrasing in §0 if data accumulates.
