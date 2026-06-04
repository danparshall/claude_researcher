# 20260604 — Plan 08 onboarding UX ship (Phase 1 + Phase 2 + screenshot pivot)

**Date:** 2026-06-04
**Branch:** onboarding-ux-cleanup
**Surface:** Claude Code (CLI)

## Summary

Execution session against the 2026-06-03 think-aloud convo. Wrote Plan 08
(`docs/plans/08_onboarding_ux.md`, 374 lines) lifting Decisions Made +
Resolutions sections from the think-aloud; Captured Tasks (#11/#12/#13)
deferred to their own execution. Dispatched Phase 1 to a `general-purpose`
subagent with worktree isolation; 7 commits shipped in ~11 minutes. Then
three mid-session additions: a git/GitHub/repo glossary in BOOTSTRAP §2a
(Q5 follow-up), a pivot of screenshot placement from BOOTSTRAP inline to
README "Setup at a glance" after recognizing `web_fetch` returns markdown
source rather than rendered images, and a HUMANS.md attribution naming Dan
as maintainer of the Nori Researcher skillset with web-only framing.

Branch state at session end: 12 commits ahead of origin
(`f8573c3..c35cd3e`), all pushed. Multi-session coordination with a
parallel task-skills session in another terminal worked cleanly — zero
file overlap today, future-merge risks identified and triaged.

## Topics Explored

### Plan 08 writing

Plan structure: header → coupling concerns resolved at design time
(paper-naming fallback via existing add-paper defaults, reminders mechanism
deferred to #13 as a unit, website out of scope at #11) → decisions
confirmed (no relitigation) → Phase 1 (9 tasks, prose + RESEARCHER.md
rules) → Phase 2 (2 tasks, screenshots) → Phase 3 pointer-only → testing
(read-throughs + greps + optional dogfood) → what could change → 4
questions with recommendations.

### Phase 1 execution via worktree-isolated subagent

Dispatched with `isolation: "worktree"` + `run_in_background: true`.
Subagent worked in `.claude/worktrees/agent-a63ed158a7e2a96b1/`. 7 commits:

1. README slim-down (Task 1.1)
2. HUMANS.md durability subsection (Task 1.2)
3. BOOTSTRAP §§0/1b/2b prose pass — timing claim, allow-all egress default,
   PAT affordance ("happy to explain") (Tasks 1.3-1.5)
4. BOOTSTRAP §4 interview restructure — drop paper-naming, reword
   git-fluency to concept-check, per-batch closers (Task 1.6 + Task 1.7's
   template field drop folded in)
5. RESEARCHER.md §4 NDA/IP project-repo isolation paragraph (Task 1.8)
6. Terminology sweep — orchestration / fork / shell command / my VM /
   the VM gone from user-facing prose; egress UI-label survives in
   step-by-step instructions (Task 1.9)
7. HUMANS.md drop paper-naming field reference (follow-up after sweep)

Subagent accepted plan's Q1/Q2/Q3 recommendations as given. Raised a new Q5
on standalone `repo` surviving in user-spoken scripts (BOOTSTRAP §0 + §8 +
§10): rewording forces 3-way collision with "claude.ai Project" + "research
project," cost > benefit. Surfaced for parent-session decision rather than
guessing.

### Mid-session: BOOTSTRAP §2a glossary (Q5 follow-up)

Dan's call on Q5: accept the surviving `repo` mentions, but add an early
glossary so the user knows what git / GitHub / repo mean before the
surviving usage hits. Inserted a 3-bullet glossary at the top of §2a (the
first operational mention of GitHub), folding "do you have a GitHub
account?" into the closing line so we don't double-ask. Pattern mirrors
the PAT affordance ("ask me to explain") and the git-fluency concept-check
elicitation.

### Multi-session coordination with task-skills

Mid-session, observed the main worktree had been switched to `task-skills`
branch by another active terminal session. Read their convo
(`docs/convos/20260604_task_skills_design.md`) to assess merge-conflict
risk:

- **Today's diff overlap:** zero — task-skills only touched STATUS.md
  (~4 lines) and added a new convo doc.
- **Future-merge risks:**
  - `basic_config` → `claude_research_config` rename (issue #14) — this
    branch references `basic_config` throughout including the new §2a
    glossary; task-skills wants the rename to land first per their
    sequencing. Rename PR sweeps when it ships.
  - `personal_info.md.template` — task-skills likely to add `home_repo`
    field; this branch removed `paper_naming` fields. Same file,
    different sections, low risk.
  - `RESEARCHER.md` — task-skills wants a §0 Persona note about periodic
    LIGHT explanation; this branch added §4 NDA/IP rule. Far apart, low risk.

Dan's choice: continue this branch as planned (using `basic_config`); let
the rename PR sweep references later. Smallest deviation; smallest cost.

### Phase 2 screenshot capture + pivot

Initial plan: file 4 PNGs in `template/reference/screenshots/`, reference
inline in BOOTSTRAP §1b (1 image) and §2b (3 images). Dan captured via
macOS `screencapture` after a VS Code restart, dropped to
`~/Pictures/screenshots/`; agent copied to the worktree with target
filenames + wrote a CAPTURED.md sidecar (capture date + UI variant per
image).

Initial commit (`0a67101`) shipped all 4 with inline BOOTSTRAP references.
Dan then asked: "will the screenshots show in the chat?" Honest answer:
**no.**
- `web_fetch` returns markdown source text, not rendered images.
- Agent sees `![alt](relative_path)` as literal text.
- The "share the link with them" instruction I wrote into the image refs
  was incomplete — agent had a relative path, not a sharable URL.

Pivot: move screenshots to README "Setup at a glance" section, right above
the bootstrap prompt block. User reads README directly (it IS the entry
point); GitHub web view renders the images; no agent rendering needed.
Trimmed to 2 screenshots (egress toggle + final PAT permissions state).
Dropped the 2 unused PNGs (`github_pat_create_form.png`,
`github_pat_add_permissions.png`); trimmed CAPTURED.md sidecar accordingly.

### HUMANS.md attribution + web-only framing

Two final asks bundled into one HUMANS.md edit in the "Where this comes
from" section's Researcher paragraph:
- Attribution: Dan Parshall maintains the Nori "Researcher" skillset,
  including many academic-specific skills.
- Framing: `claude_researcher` is "basically as close as we could get to
  that skillset in a web-only format" — makes the lineage explicit
  instead of merely implied by "design DNA comes from" + architectural
  detail.

Both land via em-dash insertion + semicolon-bridged web-only sentence
within the existing paragraph.

## Decisions Made

- **Plan 08 structure: 3 phases.** Phase 1 (prose + RESEARCHER.md rules)
  → Phase 2 (screenshots) → Phase 3 (website, out of scope per #11).
- **Phase 1 via subagent worktree isolation.** Worked well — 7 commits
  in ~11 minutes, no main-worktree disruption, clear final report.
- **Q1/Q2/Q3 from Plan 08:** subagent's recommendations all accepted
  (README About one-line attribution; Reporting Issues pointer with
  agent affordance; per-batch closer inside blockquote).
- **Q5 (new): residual `repo` in user-spoken scripts left as-is.**
  Renaming forces 3-way collision with "claude.ai Project" + "research
  project"; cost > benefit. §2a glossary mitigates by defining the terms
  upfront.
- **task-skills coordination: continue this branch as planned.** Use
  `basic_config` throughout; rename PR (#14) sweeps references when it
  ships per task-skills' own sequencing.
- **Screenshots: 2 in README, not 4 in BOOTSTRAP.** Recognizing
  `web_fetch`'s markdown-source-not-rendered-images behavior; placing
  visuals at the user's actual entry point.
- **HUMANS.md attribution:** Dan as Researcher skillset maintainer +
  `claude_researcher` framed as web-only sibling.

## Branch state

12 commits on `onboarding-ux-cleanup`, all pushed (`f8573c3..c35cd3e`):

```
c35cd3e HUMANS.md: note Dan as Researcher skillset maintainer + web-only framing
f78df07 screenshots: move from BOOTSTRAP inline to README setup section
0a67101 add screenshots for egress + PAT setup steps     (partially superseded by f78df07)
b230fe8 convo: BOOTSTRAP §2a add git/GitHub/repo glossary
4ba104b convo: HUMANS.md drop paper-naming from personal_info field list
2911726 convo: terminology sweep per onboarding think-aloud
78b91a0 convo: RESEARCHER.md project-repo isolation rule (NDA/IP)
7ff34f1 convo: BOOTSTRAP §4 interview restructure
7b6953a convo: BOOTSTRAP §§0/1b/2b prose pass
d4c8e00 convo: HUMANS.md add durability subsection
4a9eebf convo: README slim-down per onboarding think-aloud
7fca62d plan: 08_onboarding_ux from 20260603 think-aloud convo
```

## Open items

- **PR via `finishing-a-development-branch`** — pending; Dan said
  "actually finish-branch" so the PR-creation flow runs after this
  finish-convo. Skill is SWE-shaped; docs-PR adaptation: skip /simplify,
  tests, linters, type-check, webapp demo, CI; keep PR creation, optional
  nori-code-reviewer fresh-eyes, optional /loop for review.
- **`tools/repin.py` re-run before merge.** README still pins
  `2dec9af`; BOOTSTRAP has substantially changed. Without re-pinning, the
  README's quick-start URL fetches stale content — same recurrence Plan
  03 / PR #10 already addressed in the egress-rewrite case.
- **`basic_config` rename coordination at merge time.** Either rename
  PR (#14) ships first and we rebase, or this PR ships first and rename
  sweeps. Sequencing per task-skills' convo prefers the first.
- **Phase 1 dogfood read-through** (Plan 08 Phase 1 testing item 3) —
  not done. Optional but high-leverage; the fresh-chat web exercise of
  the new flow is the natural test of whether the §2a glossary, §1b
  allow-all, §2b PAT affordance, and §4 interview restructure actually
  read clean to a new user.
- **#11 (website)** — separate scope; orthogonal to merging this branch.
- **#12 (add-paper first-save naming prompt)** — defaults catch users
  until #12 ships; no regression on this branch.
- **#13 (reminders mechanism)** — may need re-scoping given task-skills'
  task-create/task-remind GH-issues-with-date-prefix design has
  superseded #13's flat-file plan.

## Process notes

- **cwd persistence quirk.** Mid-session, the shell cwd silently moved
  from the agent worktree back to the main worktree (which had been
  switched to task-skills). Manifested when `git status` returned
  task-skills and `mkdir template/reference/screenshots` landed in the
  wrong worktree. Recovery: explicit absolute paths for every file op,
  `git -C <path>` for every git op. Worth flagging — `cd` persistence
  across Bash tool calls *did* hold within short windows, but state can
  shift across long sessions or task-notification turns.
- **Subagent's Q5 call was sound.** Worth noting because the temptation
  was to override and force full removal of `repo`. The 3-way
  disambiguation cost (claude.ai Project / research project / GitHub
  repo) is real; subagent correctly identified it as a leave-or-rewrite
  tradeoff worth surfacing.
- **`finishing-a-development-branch` skill is SWE-shaped.** Most steps
  (npm test, cargo test, linters, type-check, webapp demo, /simplify,
  /code-simplifier) don't apply to a docs-only PR. Adapted by skipping
  with rationale; kept the PR-creation backbone.
- **Subagent worktree isolation: net positive.** Clean separation,
  no main-worktree disruption during the subagent's run, fast-forward
  merge worked. The locked worktree stays until clean-worktrees skill
  is invoked later.
