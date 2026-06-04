# 20260604 — Task skills design (task-create, task-remind, task-triage)

**Date:** 2026-06-04
**Branch:** task-skills
**Surface:** Claude Code (CLI)

## Summary

Brainstorm session to design a "task reminder" capability and reconcile it
with the existing `capture-task` and `triage-tasks` skills. Emerged from
issue [#13](https://github.com/danparshall/claude_researcher/issues/13)
(session-start reminder check), which the 2026-06-03 onboarding think-aloud
convo locked as a flat-file approach (`basic_config/reminders.md` read at
session start). That decision is now superseded: today's design uses GH
issues with a date-prefix encoding for fired-reminder-style items, unifying
"task" and "reminder" into one storage backend.

## Topics Explored

### Storage backend — Issues vs flat file

The original Issue #13 decision was a flat `REMINDERS.md` in `basic_config`,
chosen because claude.ai memory has no scheduled-task primitive. Today's
design re-evaluated and shifted to GH issues, on the grounds that:

- A real use case ("I emailed Sarah, remind me next week") needs persistent
  identity + history + a snoozeable date on the same object. Issues handle
  this natively; a flat file would force splitting state across two
  storage backends.
- The body-fetch cost concern is solvable by encoding the date in the title
  (`[YYYY-MM-DD] task description`) — `gh issue list --json number,title`
  is metadata-only, no body reads at session-start regardless of issue
  count.

### The three-skill split

Locked architecture:

- **`task-create`** — drafts title/summary from conversation, asks "when?"
  (with "no date" as a valid answer), creates GH issue with optional
  `[YYYY-MM-DD]` title prefix. Defaults to current repo;
  "my personal list" override routes to home repo.
- **`task-remind`** — runs every session-start automatically. Queries
  current repo + personal home repo, filters issues with date-prefix
  titles to overdue (≤ today), presents as two labeled sections, points
  to `task-triage` as escape valve for the full view. Owns
  snooze/acknowledge verbs on fired items.
- **`task-triage`** — user-invoked, on demand. Queries all user repos
  with `task` label. Largely renamed `triage-tasks`.

### Scope decision — current repo + home, not all-repos

`task-remind` queries two repos per session-start (current + home), with
explicit framing that items in *other* repos require running
`task-triage`. The "current repo only" variant was considered and rejected:
it quietly breaks the Issue #13 motivating case (egress-revisit reminder
set during bootstrap, intended to fire a week later — would only fire if
the user happened to be in a `basic_config` session, which is rare in
practice).

### Source-of-truth pattern — follow existing dotfiles flow

Investigated current organization:
- `capture-task` and `triage-tasks` live *only* in
  `~/code/dotfiles/nori-researcher/skills/` today — they were never
  ported to `claude_researcher/template/skills/`.
- The existing pattern for all 6 currently-shared researcher skills is:
  authored in dotfiles, ported to claude_researcher with provenance
  frontmatter + REST-adaptation banner.

Locked: follow the existing pattern. Author task-create / task-remind /
task-triage in dotfiles first, then port to claude_researcher.

### Behavioral principles surfaced

- **Periodic LIGHT explanation of back-end behavior** — lands as a
  behavioral note in `RESEARCHER.md` §0 Persona. When the agent does
  something the user might want to understand (cross-repo back-link
  decisions, snooze affordances, etc.), it briefly explains rather than
  silently executing.
- **Agent notes about the user** (separable new feature) — a dynamic,
  agent-authored complement to the user-authored static `personal_info.md`.
  Tracked as a separate issue, not in scope for task-skills.

## Decisions Made

- **3 skills, kebab-case naming:** `task-create`, `task-remind`,
  `task-triage`.
- **Storage:** GH issues with the `task` label.
- **Date encoding:** `[YYYY-MM-DD]` prefix in the issue title (mutable
  for snooze; no body reads at session-start).
- **`task-create` scope default:** current repo. Override: "my personal
  list" routes to home repo.
- **`task-remind` scope:** current repo + personal home repo, two labeled
  sections, points to `task-triage` for cross-repo view.
- **`task-triage` scope:** all repos with `task` label (rename of
  existing `triage-tasks`).
- **Source-of-truth pattern:** follow existing flow (authored in dotfiles,
  ported to claude_researcher with provenance + REST banner).
- **Surface adaptation:** runtime check (banner pattern from Wave 2/3).
- **Background subagent:** literal where possible (CLI uses Agent tool;
  web falls back to main-agent step).
- **`task-remind` fired-item actions:** offer close + snooze by default;
  strip-prefix only offered if user signals uncertainty ("ugh, I don't
  know when").
- **Cross-repo back-link:** when `task-create` routes to non-current
  repo, agent explicitly asks "do you want this task linked to this
  conversation file? (that's what I normally do)".
- **Home repo name:** `claude_research_config` (rename of `basic_config`).
  Not `dotfiles` — that may preexist with the user's own conventions and
  shouldn't be conscripted.

## Sequencing

Recommended order across branches:

1. **`basic_config` → `claude_research_config` rename** — mechanical, small
   blast radius, unblocks both other branches.
2. **`task-skills`** — builds the reminder infra that onboarding-UX prose
   wants to reference.
3. **`onboarding-ux-cleanup`** — inherits a clean home-repo name + working
   task-skills to point at.

## Open items (deferred to plan)

- How "home repo" is configured (likely a `home_repo` key in
  `personal_info.md` with default `<gh-user>/claude_research_config`)
- Exact REST-adaptation banner wording for each of the three skills
- CLI symlink/install mechanism for the three new skills (Wave 0
  infrastructure remains deferred)
- task-remind execution as literal subagent on CLI (Agent tool) vs
  session-start step on web
- Migration plan for users of existing `capture-task` / `triage-tasks`
  (trigger phrases, alias period?)

## Results

No code artifacts yet. Convo doc + two filed GH issues (rename, agent-notes
feature). Plan-writing (`docs/plans/NN_task_skills.md`) is the next step
against this branch.

## Captured Tasks

- [#14: Rename `basic_config` → `claude_research_config` across templates and runtime](https://github.com/danparshall/claude_researcher/issues/14) — captured 2026-06-04
- [#15: Consider adding an "agent notes about the user" file in the config repo](https://github.com/danparshall/claude_researcher/issues/15) — captured 2026-06-04
