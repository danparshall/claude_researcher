# 20260604 — Plan 09 Phases 1 + 2 execution: task-skills authored in dotfiles, home_repo wired into claude_researcher

**Date:** 2026-06-04
**Branch:** task-skills
**Surface:** Claude Code (CLI)

## Summary

Execution session against Plan 09 ([`docs/plans/09_task_skills.md`](../plans/09_task_skills.md)), written 2026-06-04 by the prior `task-skills` design session. Phase 0 precondition (`basic_config` → `claude_research_config` rename via issue #14 / PR #17) confirmed shipped. **Phases 1 and 2 executed end-to-end** in this session: three dotfiles commits shipping the renames + new `task-remind` skill (pushed to `origin/main`), and three `claude_researcher` commits shipping the `home_repo` config wiring + the session's convo doc (pushed to `origin/task-skills`). Phases 3-7 remain for a future session.

Mid-session coordination event: another agent was actively working in `~/code/dotfiles` on the chain-hook-maintenance branch (uncommitted edits to `nori-researcher/nori.json` + `docs/active/chain-hook-maintenance/probes/`). Discovered this after staging the first `git mv` (capture-task → task-create); paused, undid the rename, asked the user, and resumed once they confirmed the other agent was done. The coordination did surface one fact worth recording: `nori-researcher/nori.json` doesn't reference any of the skill names being renamed (`capture-task`, `triage-tasks`, or the new `task-*` names), so there was no content-level collision risk — only the shared-branch push race.

## Topics Explored

### Phase 0 — Precondition check

Plan 09 Task 0.1 specifies `gh issue view 14 --json state` + `grep -rn 'basic_config' template/ docs/`. Both checks ran:
- Issue #14: `CLOSED` at `2026-06-04T19:33:45Z` (closed via PR #17 merge).
- `basic_config` hits: 5 total, all in `docs/convos/` (historical narrative). Zero in `template/`. The plan's decision tree blocks on `template/` hits, so this is clean.

The grep return reaffirmed an artifact-curation note: convo docs are historical-narrative artifacts and shouldn't be swept for terminology updates; the rename SHA hooks up cleanly to the convo language only via reading order, not by mutation. Same principle as STATUS.md "Critical note for fresh agents" — flat layout is intentional.

### Phase 1.1 — task-create (rename of capture-task)

The substantive edits to the moved file:
- YAML `name: Capture-Task` → `name: Task-Create`, trigger phrases extended with three new ones (`remind me later`, `add a reminder`, `track this with a date`) — appended to the existing list, no removals (Plan's Coupling Concerns: existing triggers survive verbatim).
- Step 1 target-repo table: replaced `<gh-user>/dotfiles` fallback with the home_repo / claude_research_config flow per Decision 7. Added a paragraph about reading `home_repo` from `personal_info.md` + missing-file-is-soft-failure semantics.
- **New Step 2.5 ("Ask when?")** between Step 2 (draft) and Step 3 (ensure label). Body covers ISO/relative/no-date accept paths, the BSD/GNU `date` fallback, and conditional re-presentation of the draft if a prefix is added.
- Cross-repo back-link prompt at the top of Step 5 per Decision 8.
- Common Mistakes additions: "Forgetting to ask 'when?'" and "Routing a personal task to the current research repo." Updated "Creating the issue on the wrong repo" to reference home_repo + the LIGHT-explanation discipline (RESEARCHER §0).

**One port-time fix worth recording:** my first pass mis-structured the numbering — I split Step 2 into "Step 2 (draft)" + "Step 3 (Present for approval)" + Step 2.5, which pushed Steps 4-6 to 5-7 and created a duplicate `Step 4` header. The plan's actual intent (re-read carefully) was *insert* Step 2.5 between existing Step 2 and Step 3 without renumbering downstream. Fixed by restoring the present-for-approval block to Step 2's end and keeping Step 2.5 as the date-logic + conditional-re-present step. Net structure: Steps 1, 2, 2.5, 3, 4, 5, 6 — plan-faithful.

Commit: `baa7120`, 213 insertions / 161 deletions. Heredoc form to avoid the Nori commit-author hook bug (per the plan and per RESEARCHER.md §5).

### Phase 1.2 — task-remind (new skill)

Authored from scratch following the plan's skeleton in Task 1.2 step 2. Concrete bodies for each of 6 steps:
- Step 1: detect GH user + home_repo. Read `personal_info.md`; default to `<gh-user>/claude_research_config` if `home_repo` unset. If current repo == home_repo, query once (no double-fetch).
- Step 2: metadata-only `gh issue list` calls (`--json number,title,url,updatedAt`); fail-soft per-repo (one repo unavailable doesn't block the other).
- Step 3: regex `^\[(\d{4}-\d{2}-\d{2})\] (.*)$`; lexicographic ISO-8601 string compare against `date -u +%Y-%m-%d` (no date library needed since ISO sorts correctly as strings).
- Step 4: two labeled sections; bail early with one line if both empty; strip the prefix from displayed titles (redundant with the parenthetical fire-date); compute "today / yesterday / N days ago".
- Step 5: close / snooze / skip default menu; **strip-prefix only offered on uncertainty signal** ("ugh, I don't know," "someday," etc.) per Decision 12. LIGHT-explanation discipline: announce mutations after they happen.
- Step 6: cross-repo escape valve pointer to `task-triage` (one line; no auto-run).

Common Mistakes section authored fresh (7 entries) covering the foreseeable error modes: fetching bodies, auto-snoozing, running every turn, showing future-dated reminders, showing non-dated tasks, menu-dumping all four actions upfront, hardcoding home repo.

Commit: `fe0d52d`, 155 insertions.

### Phase 1.3 — task-triage (rename of triage-tasks)

Smaller edit set than task-create — the body is unchanged in substance except for Decision 6 (date-prefixed items stay in the inventory inline with non-dated tasks). Changes:
- YAML `name: Triage-Tasks` → `name: Task-Triage`; prepended `task-triage` and `/task-triage` to trigger phrases; kept `/triage-tasks` for back-compat (Decision 9: no alias period, existing phrases survive in description).
- Announce line updated.
- New top-of-body paragraph: date-prefixed items render inline with their prefix visible; fired-vs-pending split belongs to `task-remind` at session-start.
- Step 3 example row updated to show a `[YYYY-MM-DD]`-prefixed item rendered with the prefix intact.
- Step 5 deep-dive example: `cd /path/to/repo` + `git show` → `git -C /path/to/repo show` (preferred form per dotfiles permission policy; not strictly required since the original wasn't a chain, but models the right pattern).
- Common Mistakes: added "Filtering out date-prefixed items" with the Decision 6 rationale.
- All references to companion skill `capture-task` updated to `task-create`.

Commit: `8b619b5`, 16 insertions / 9 deletions, detected by git as a rename (similarity 64%).

### Phase 1.4 — Verify + push

- `ls ~/code/dotfiles/nori-researcher/skills/` after the three commits showed exactly `task-create`, `task-remind`, `task-triage` (no stale `capture-task` or `triage-tasks`).
- Three commits sitting on top of the other agent's `3af3b82` (chain-hook-maintenance reconcile).
- `git push` published all four commits (other agent's + mine) to `origin/main`. The other agent's pre-existing uncommitted leftover (`nori.json` modified, `probes/settings.json` deleted, untracked probes) was unaffected — all my staging was targeted (`git add <specific-file>`).

### Phase 2.1 — Add `home_repo` to `personal_info.md.template`

The template (`template/templates/personal_info.md.template`) is sparser than Plan 09's prose anticipated — no `<GH_USER>` or `<TOPIC>` placeholders (those live elsewhere; the template only carries identity + history + how-I-work + operating-preferences blocks). Port-time call: add `home_repo` under `## Operating preferences` alongside git fluency and mode, since all three are user-level identity-shaped values that fit the same shape. Added a narrative paragraph below the field explaining its role — task-create override target and task-remind second query target — matching the template's existing inline-narrative documentation style (no HTML comments, no markdown `#` comments).

Commit: `165aaae`, 3 insertions.

Note: this edit invalidates the SHA-pin in BOOTSTRAP.md line 383 (currently `8c732081`, pre-edit). Plan 09 Task 7.2 calls out a pre-merge `tools/repin.py` run; the commit message records the dependency for the next session.

### Phase 2.2 — Extend BOOTSTRAP §4 Batch 3 to ask for `home_repo`

Batch 3 grows from 3 to 4 questions. Plan called for "after GH-user capture" — Step 2a captures `<USERNAME>` long before Step 4, so any spot in Batch 3 satisfies that ordering. Slotted as Q3 between Mode (Q2) and Extra paper-source domains (Q4); keeps preference-shaped questions grouped before the situational one.

Question phrasing concretized with a use-case example (the dentist reminder), since first-time users without Plan 09 context need a hook for what `home_repo` is *for*. Default substitution path documented after the question block: `<USERNAME>/claude_research_config` if Enter / silence, override accepted as `owner/repo`. LIGHT-explanation block per RESEARCHER §0 covers the "what does that mean?" case with a one-paragraph (not menu-dump) explanation. Silence-is-consent — not a hard-required question.

Commit: `f5f6eea`, 5 insertions / 4 deletions.

### Convo doc + push checkpoint

Mid-session per user request: write the convo doc capturing Phase 1, commit it, then continue. Commit `082e1a2` (109 insertions). After Phase 2 also shipped, pushed `task-skills` to `origin/task-skills` (3 commits ahead → 0).

## Provisional Findings

- **The plan's pre-baked Coupling Concerns + Decisions blocks did their job.** The "do NOT re-litigate" framing held — when I caught myself re-deriving the numbering decision in Phase 1.1, the plan's clear "insert Step 2.5" wording was the catch-and-revert trigger. Similar dynamic during Decision 12 (strip-prefix conditionality): the plan's heuristic ("only on uncertainty signal") was concrete enough to write the conditional branch around, not abstract enough to need re-thinking.
- **The BSD/GNU date fallback is a real cross-environment concern.** task-create's Step 2.5 documents both forms (`date -u -v+7d` BSD, `date -u -d '+7 days'` GNU). I haven't tested either at runtime in this session — the conversion logic ships as instructions for the runtime agent, who'll try one and fall back. If both fail on a minimal sandbox, the skill surfaces it to the user and asks for an ISO date. That's a reasonable degraded-mode behavior; the alternative (importing a date library, building a parser) was rejected by the plan as overkill.
- **The "no alias period" Decision 9 is OK in practice because the trigger phrases survive.** I kept all the old trigger phrases (`"triage,"` `"what should I work on,"` `"/triage-tasks"`) in `task-triage`'s YAML description, so a user typing any of those still lands in the right place. Only the *YAML name* and *directory* changed. No back-compat layer needed beyond preserving the description.
- **Cross-agent dotfiles coordination went smoothly with one explicit pause.** When the user surfaced the parallel-agent concern, undoing the staged `git mv` cost nothing (no edits yet) and let me proceed cleanly later. The targeted `git add <file>` discipline meant the other agent's uncommitted work was never accidentally pulled into my commits. Worth recording as a multi-terminal hygiene pattern.

## Decisions Made

All decisions in this session were execution of pre-locked plan decisions (Plan 09 Coupling Concerns and Decisions Made blocks). No new decisions to record; no plan revisions.

One small port-time formatting call not pre-specified: the cross-repo back-link prompt in `task-create` Step 5 is presented as a `> *italic blockquote*` paragraph with the `<target-repo>` placeholder rendered as inline code. The plan provided the exact prompt text; I chose the rendering shape to match the surrounding "When prompting, ask:" pattern in Step 1.

Another: the LIGHT-explanation rationale in `task-create` Step 1 and `task-remind` Step 5 is delivered as a one-clause aside ("one clause, not a paragraph" / "briefly say what the mutation was") with a parenthetical pointer back to `RESEARCHER.md` §0. The plan asked for this discipline; the shape lands as inline mentions, not a dedicated section.

## Results

No standalone results files (no tables, figures, or experiment output). The artifacts are commits.

**Dotfiles (`github.com:danparshall/dotfiles`, on `main`):**
- `baa7120` task-create — rename + 'when?' step + home_repo routing (213 / 161)
- `fe0d52d` task-remind — new skill, session-start reminder check over date-prefixed issues (155 new)
- `8b619b5` task-triage — rename + surface date-prefix on inventory rows (16 / 9)

**claude_researcher (`github.com:danparshall/claude_researcher`, on `task-skills`):**
- `082e1a2` convo: Plan 09 Phase 1 dotfiles ship (109 new, this convo doc)
- `165aaae` personal_info: add home_repo field for task-skills routing (3 / 0)
- `f5f6eea` BOOTSTRAP: ask for home_repo with default in §4 Batch 3 (5 / 4)

3 skill files in `~/code/dotfiles/nori-researcher/skills/`: `task-create/SKILL.md` (213 lines), `task-remind/SKILL.md` (155 lines new), `task-triage/SKILL.md` (132 lines, was 128).

## Open Questions

None blocking the next Phase. Two carried forward from Plan 09 that this session didn't touch:
- Q3 (`task-remind` filtering for far-future dates) — Plan says no; this session encoded the strict `<= today` filter in Step 3, so this is now settled in code (modulo runtime testing).
- Q5 (does `task-triage` need a `task` label requirement?) — Out of scope; plan defers to "revisit if it bites." Not exercised yet.

## Next Steps (this branch)

Session ended after Phase 2. Remaining phases for the next session:

- **Phase 3**: port the three skills from dotfiles to `claude_researcher/template/skills/` with provenance frontmatter (`nori_researcher_source:` pinned to dotfiles HEAD at port time — for this set, `8b619b5` or later) + REST-adaptation banner per the Wave 2/3 pattern. Three new directories: `template/skills/task-create/`, `template/skills/task-remind/`, `template/skills/task-triage/`. Banner verbs to list inline include `gh issue create`, `gh issue list`, `gh issue edit`, `gh issue close`, `gh search issues`, plus the standard `git add` / `commit` / `push` translation.
- **Phase 4**: wire task-remind into session-start (`template/RESEARCHER.md` §2 + dotfiles `nori-researcher/AGENTS.md`).
- **Phase 5**: SKILL_INDEX.md additions (new "Task management" section) + RESEARCHER.md §0 LIGHT-explanation principle as a fifth tier-independent trait.
- **Phase 6**: migration verification (`~/.claude/skills/` symlinks, if any) + CLI smoke test (Plan 09 Task 6.2). Web smoke test (6.3) deferred.
- **Phase 7**: verification script (Plan 09 Task 7.1) + `tools/repin.py` (Plan 09 Task 7.2 — required since 165aaae edited a SHA-pinned template) + STATUS.md update + `finish-convo` + PR via `finishing-a-development-branch`.

**Suggested handoff sentence:** On `task-skills` at `f5f6eea` — Plan 09 Phases 0-2 shipped (Phase 1 in dotfiles at `8b619b5` on origin/main; Phase 2 home_repo wiring in claude_researcher commits `165aaae` + `f5f6eea`); next session executes Phase 3 (port 3 skills to template/skills/ with provenance frontmatter pinned to dotfiles `8b619b5` and the Wave 2/3 REST-adaptation banner), then Phases 4-7 per the plan.

## Process notes

- TaskCreate used (5 tasks for the 4 Phase 1 sub-tasks + Phase 0 verification). Plan 09's pre-baked structure made the task list a thin mirror of the plan's task numbering; TaskCreate added value mostly as a checkpoint for "did I actually push after committing?" The plan itself is the substantive checklist.
- Convo-name handshake (§2e) happened at session start via AskUserQuestion (proposed `20260604_plan09_phase1_dotfiles_ship`, accepted "yes — propose a name now"). Smoother than the 2026-06-04 task-skills design session, which Dan flagged in its convo doc as a missed handshake.
- Multi-terminal protocol exercised once (the dotfiles other-agent pause). Worked correctly: pause, undo, ask user, resume, targeted staging throughout.
