# claude_researcher — Plan 09: Task skills (task-create / task-remind / task-triage)

**Goal:** Ship three kebab-case skills (`task-create`, `task-remind`, `task-triage`) over a single GH-issues-with-`task`-label backend, with date-prefixed titles (`[YYYY-MM-DD] ...`) encoding reminder fire-dates. Authored in `~/code/dotfiles/nori-researcher/skills/` (the source of truth for shared Researcher skills); ported to `claude_researcher/template/skills/` with provenance frontmatter + a REST-adaptation banner per the Wave-2/3 pattern. Adds a `home_repo` config key to `personal_info.md` so cross-repo back-link routing has a single source of truth, and wires `task-remind` into session-start on both surfaces.

**Status:** Ready for execution. All architectural decisions locked in the originating convo; this plan is a sequence of mostly-mechanical text edits plus a few small new files, with the structural calls already made.

**Originating convo:** [`20260604_task_skills_design.md`](../convos/20260604_task_skills_design.md). The convo's **Decisions Made** + **Sequencing** sections are the input. The convo's **Open items (deferred to plan)** section is the input to this plan's **Decisions confirmed at design time** block below — i.e., this plan resolves them.

**Related prior work:**
- The 6 currently-shared Researcher skills (`finish-convo`, `update-docs`, `add-paper`, `audit-docs`, `audit-papers`, `init-research-repo`) shipped via the Wave 2/3 pattern in commits `0bbd419` and the Plan 06 `454018f` rewrite — the porting recipe (provenance frontmatter + one-line REST-adaptation banner between frontmatter and body) is established and unchanged here.
- `capture-task` and `triage-tasks` exist today in `~/code/dotfiles/nori-researcher/skills/` only — they were never ported to `claude_researcher/template/skills/`. This plan is their first port, simultaneous with their reshape.
- Issue [#13](https://github.com/danparshall/claude_researcher/issues/13) (session-start reminders) was the original trigger. Plan 08 (`onboarding-ux-cleanup`, merged 2026-06-04 as PR #16) deliberately deferred the reminder-write mechanism here so it ships as a unit. The forward-reference sentence in BOOTSTRAP §1b (allow-all + "we'll revisit in a week") becomes operational when this plan ships.
- Issue [#14](https://github.com/danparshall/claude_researcher/issues/14) (`basic_config` → `claude_research_config` rename) is sequenced **before** this plan executes — see Phase 0 Preconditions. This plan writes against the post-rename name throughout.
- Issue [#15](https://github.com/danparshall/claude_researcher/issues/15) (agent-notes-about-user file) is separate scope; this plan does not touch it.

**Confidence:** High on the architecture (date-prefix encoding, 3-skill split, GH-issues backend, current+home repo scope for `task-remind`) — those resolved through a Socratic pushback exchange in the convo and have load-bearing reasoning. Medium on a few execution details (exact wording of the REST-adaptation banner; whether `task-remind` runs as a literal subagent on CLI vs. inline main-agent step) — these are deferred to port-time judgment with the recommendations below.

**Branch:** `task-skills`.

**Tracking issue:** none for this plan itself. Companion issues #14 (precondition), #13 (this plan operationalizes), #15 (separate scope) all have coverage.

**Tech stack:** Markdown skills (LLM-executed instructions, no test-runnable code); `gh` CLI for GitHub Issues read/write; one new YAML field in `personal_info.md`; one new session-start RESEARCHER.md instruction.

---

## Coupling concerns resolved at design time (do NOT re-open)

These were thought through before writing the plan. The implementing agent should not re-derive them.

- **`task-create` is an *upgrade* of `capture-task`, not a parallel skill.** Same triggers ("add a task," "capture this," "track this for later"), same backend, same back-link discipline — plus a "when?" question with optional `[YYYY-MM-DD]` title prefix and `home_repo` routing override. In dotfiles we **rename the directory and update the YAML `name`**; existing trigger phrases survive verbatim in the frontmatter `description`. No alias period needed — Dan is the only user of these skills today.
- **`task-triage` is a *rename* of `triage-tasks`.** Body is unchanged in substance except for one filter consideration (Decision 6 below). YAML `name` and directory both rename. Existing "/triage-tasks" trigger phrase in the description survives during the alias transition (Decision 9 below).
- **`task-remind` is a wholly new skill.** No precedent in dotfiles. Reads at session-start, queries metadata only, presents two labeled sections (current repo + home repo), offers snooze/close verbs on fired items.
- **`home_repo` lives in `personal_info.md`, not STATUS.md.** Per the Plan 06 schema split (user-level vs. per-project), `home_repo` is a user-level identity-shaped value (the user's "personal todo lives here" repo). Default to `<gh-user>/claude_research_config`. STATUS.md continues to hold per-project keys only.
- **#14 (rename) lands first.** This plan's text writes `claude_research_config` everywhere it would otherwise have written `basic_config`. If #14 has NOT shipped at execution time, see Phase 0 — execution stops until it does. The rename is a 1-commit branch; not worth interleaving.
- **No `add-paper`-style dispatcher.** The 3-skill split is along *intent* axes (create / remind / triage), not protocol axes. They share a backend but each does one thing the others don't. No third-party routing layer needed.
- **REST-adaptation banner is the Wave-2/3 one-liner, unchanged.** Form: `> **Runtime note (claude.ai):** This skill assumes a CLI environment with `gh` and `git` available. When run in the claude.ai sandbox, translate `gh issue create` / `gh issue list` / `gh search issues` into the GitHub REST API recipes from your Project Instructions; translate `git add`/`commit`/`push` into the `write_update` / `write_new` recipes likewise.` — exact wording finalized in Phase 3, Task 3.1.

## Decisions confirmed at design time (do NOT re-litigate)

Lifted from the convo's Decisions Made section + the Open items resolved here. Re-opening these blows scope unboundedly.

- **Decision 1.** 3 skills, kebab-case naming: `task-create`, `task-remind`, `task-triage`.
- **Decision 2.** Storage: GH issues with the `task` label. Single backend across all three skills.
- **Decision 3.** Date encoding: `[YYYY-MM-DD]` prefix in the issue title. Mutable for snooze. No body reads needed at session-start filtering.
- **Decision 4.** `task-create` scope default: current repo. Override: "my personal list" (any reasonable paraphrase) routes to `home_repo`.
- **Decision 5.** `task-remind` scope: current repo + `home_repo`. Two labeled sections in the output. Points to `task-triage` for cross-repo view.
- **Decision 6.** `task-triage` scope: all user repos with `task` label. **Includes** date-prefixed items (they're still tasks); presents them with the date visible so the user sees both fired-already and not-yet-fired items in one place. The fired-vs-pending split is `task-remind`'s job at session-start; `task-triage` is for the rest.
- **Decision 7.** `home_repo` config: new YAML key in `personal_info.md`, default `<gh-user>/claude_research_config`. Read by `task-create` (override target) and `task-remind` (second query target). If unset, the agent reads `gh api user --jq .login` and constructs the default at runtime; missing/empty `personal_info.md` is not a hard failure.
- **Decision 8.** Cross-repo back-link affordance: when `task-create` routes to a non-current repo (the "my personal list" path), the agent explicitly asks the user: *"Do you want this task linked back to today's convo doc? That's what I normally do, but the convo lives in this repo and the issue lives in another, so the link is one-way."* Honor the answer; default is yes.
- **Decision 9.** Migration: no alias period. `capture-task` and `triage-tasks` directories are renamed in place (`git mv`). All existing trigger phrases survive in the YAML `description` of the new skills, so a user typing "add a task" continues to land in the right place.
- **Decision 10.** Surface adaptation: REST-adaptation banner (Wave-2/3 pattern), one-line, identical across all three ported skills (only the example commands differ). Empirically evaluating banner-vs-proper-REST is the still-open Wave 2/3 question (Plan 02); this plan does not re-decide it.
- **Decision 11.** `task-remind` CLI execution: **runs as the main-agent inline at session start**, not as a literal Agent-tool subagent. Rationale: (a) the work is small (one or two `gh` calls + a short presentation); (b) the agent needs to ask the user follow-up questions about fired items, which subagent isolation makes awkward; (c) parity with the web surface (which has no subagent affordance) is structurally simpler. The convo's "background subagent" framing is honored on web by reading like a backgrounded check; on CLI by being the first thing the main agent does after pre-flight reads.
- **Decision 12.** `task-remind` fired-item action menu: by default offer **close** and **snooze** (mutates date prefix to a future ISO date). Strip-prefix (convert "reminder" to "open task with no date") is offered **only** if the user signals uncertainty about when to revisit ("ugh, I don't know when"). The skill body documents the heuristic so the agent doesn't menu-dump every option.
- **Decision 13.** Behavioral note for `RESEARCHER.md` §0 ("periodic LIGHT explanation of back-end behavior"): added as a single sentence in §0 Persona. NOT a new skill; NOT a tier-keyed elaboration. It governs how `task-create`'s cross-repo affordance (Decision 8) and `task-remind`'s snooze affordance are explained to the user. Wording finalized in Phase 5.

---

## Phase 0 — Preconditions

### Task 0.1 — Verify #14 (`basic_config` rename) has shipped

**Why:** Every file this plan touches that mentions a config repo name writes `claude_research_config`. If #14 hasn't merged to `main`, those references will collide on merge.

**Check:**

```bash
gh issue view 14 --json state --jq .state
git log origin/main --oneline | grep -i 'basic_config\|claude_research_config\|rename' | head
grep -rn 'basic_config' template/ docs/ 2>/dev/null | head -5
```

**Decision tree:**
- Issue #14 is `CLOSED` *and* `grep` returns no `basic_config` hits in `template/` → proceed to Phase 1.
- Issue #14 is still `OPEN` or `grep` still finds `basic_config` → **stop**. Surface to Dan: "Plan 09 expects #14 to have shipped first. Should I (a) wait, (b) take on #14 within this branch, or (c) write `basic_config` instead and let the rename PR sweep these?" Default recommendation is (a); (b) creates a wide-scope branch; (c) defeats the whole sequencing intent.

**Don't:** silently substitute `basic_config` if #14 is still open. The wrong default leaks into shipped skills.

---

## Phase 1 — Dotfiles (source of truth)

Author the three skills in `~/code/dotfiles/nori-researcher/skills/`. This is the upstream — the `claude_researcher` ports in Phase 3 derive from these files.

Working directory for this phase: `~/code/dotfiles/`. Use `git -C ~/code/dotfiles` for all git ops (the `cd <path> && git ...` chain is denied; see CLAUDE.md).

### Task 1.1 — Rename `capture-task` → `task-create`

**Files:**
- `~/code/dotfiles/nori-researcher/skills/capture-task/SKILL.md` → `~/code/dotfiles/nori-researcher/skills/task-create/SKILL.md`
- (Frontmatter and body edits per below)

**Steps:**

1. `git -C ~/code/dotfiles mv nori-researcher/skills/capture-task nori-researcher/skills/task-create`
2. Open the moved file. Update YAML `name: Capture-Task` → `name: Task-Create`. **Keep the existing `description` field's trigger phrases verbatim** ("add a task," "capture this," etc.) — they're the user-typed trigger surface and shouldn't churn. Append the new triggers to the existing list: *"remind me later," "add a reminder," "track this with a date."*
3. Update the Announce line: `"I'm using the Capture-Task skill"` → `"I'm using the Task-Create skill"`.
4. **Insert a new Step 2.5: "Ask when?"** between the current Step 2 (Draft title/summary) and Step 3 (Ensure label). Body:

   > *"Should this fire on a specific date, or is it open-ended? Saying a date turns this into a reminder you'll see at session-start; saying 'no date' keeps it on the regular triage list. You can always re-date later by editing the issue title."*
   >
   > Accept any of: an ISO date (`2026-06-11`), a relative date (`next Monday`, `in a week`, `tomorrow`), or "no date" / "open-ended" / "skip" / silence (interpreted as no date).
   >
   > Convert relative dates to ISO via `date -u -v+7d +%Y-%m-%d` (BSD/macOS) or `date -u -d '+7 days' +%Y-%m-%d` (GNU/Linux); the agent picks the one that works in the current shell. If both fail (some sandbox environments), surface the issue and ask the user for an ISO date directly.
   >
   > If a date is given, prepend `[YYYY-MM-DD] ` to the title in Step 2's draft. Re-present the draft with the prefix so the user sees the encoded form before approval.

5. **Update the target-repo table in Step 1** to:

   | Situation | Target repo |
   |---|---|
   | In a git repo with a GH remote | That repo |
   | Not in a git repo, OR no GH remote | Read `home_repo` from `personal_info.md`; fall back to `<gh-user>/claude_research_config` if unset |
   | User says "my personal list" / "personal task" / "real-world task" | Same: `home_repo` or fallback |
   | User overrides with a specific repo | What they said |

6. **Add the cross-repo back-link prompt (Decision 8)** in Step 5 (Back-link from convo doc). New paragraph at the top of Step 5:

   > If the target repo is **not** the current repo (the "personal list" path), the convo doc lives in a different repo than the issue. Ask the user: *"Do you want this task linked back to today's convo doc? That's what I normally do, but the convo lives in this repo and the issue lives in `<target-repo>`, so the link is one-way."* Default to yes if they're silent; honor a no.

7. **Update Common Mistakes** to add one entry: *"Forgetting to ask 'when?'" — Problem: the date-prefix encoding is the whole mechanism that lets `task-remind` find reminders cheaply. Skipping the question means reminders get filed as regular tasks and never fire. Fix: always ask in Step 2.5, even if context strongly implies a date.*

8. **Commit** (heredoc form to avoid the Nori commit-author hook bug):

   ```bash
   git -C ~/code/dotfiles add nori-researcher/skills/task-create/SKILL.md
   git -C ~/code/dotfiles commit -m "$(cat <<'EOF'
   task-create: rename capture-task, add 'when?' step + home_repo routing
   EOF
   )"
   ```

**Don't:** drop the existing trigger phrases from the description. Don't pre-emptively change the Nori commit-author footer behavior — the heredoc workaround is the established practice.

### Task 1.2 — Create `task-remind` (new skill)

**File:** `~/code/dotfiles/nori-researcher/skills/task-remind/SKILL.md` (new)

**Steps:**

1. Create the directory: `mkdir -p ~/code/dotfiles/nori-researcher/skills/task-remind`
2. Write `SKILL.md` with the following structure (concrete text to be filled in at execution time, modeled on `task-create`'s shape):
   - YAML frontmatter: `name: Task-Remind`, description = trigger phrases (`"check reminders," "what's pending," "session-start reminders"` — though the primary invocation is auto-load at session-start, not user-typed).
   - Announce line: `"I'm using the Task-Remind skill to check for any pending reminders before we get going."`
   - **Step 1: Detect GH user and `home_repo`.** Read `personal_info.md`; if `home_repo` is set, use it; else `gh api user --jq .login` and construct `<gh-user>/claude_research_config`.
   - **Step 2: Query both repos, metadata only.** Two parallel `gh issue list` calls, one per repo, filtering `--label task --state open` and capturing `--json number,title,url,updatedAt`. Bodies are NOT fetched — the title prefix is the whole filter signal.
   - **Step 3: Filter to fired items.** Parse titles matching the regex `^\[\d{4}-\d{2}-\d{2}\] `; compare the prefix date to today (`date -u +%Y-%m-%d`); fired = prefix `<= today`.
   - **Step 4: Present two labeled sections.**
     ```
     == In <current-repo> ==
       #<N>  <title without prefix>     (fired YYYY-MM-DD, <N days ago>)

     == In <home-repo> ==
       #<N>  <title without prefix>     (fired YYYY-MM-DD, <N days ago>)
     ```
     If a section is empty, omit it. If **both** sections are empty, output one line: *"No reminders pending. Continuing with session-start."* and stop.
   - **Step 5: Per-fired-item action prompt.** For each fired item, offer:
     - *Close* (`gh issue close <N> --comment "Done"`)
     - *Snooze N days* (rewrite the prefix to today + N via `gh issue edit <N> --title "[<new-date>] <rest>"`)
     - *Skip* (no action this session)
     - *Strip prefix* — **only** offered if the user signals uncertainty about when to revisit (heuristic: phrases like *"ugh, I don't know,"* *"not sure when,"* *"someday"*). When offered, it becomes the regular-task form: title becomes `<rest>` with no prefix; the item moves out of `task-remind`'s view and into `task-triage`'s.
   - **Step 6: Cross-repo escape valve.** End with a single line: *"Want a full view of every open task across all your repos? Run task-triage."* (Decision 5 echoes the convo's "current+home, with escape valve" framing.)
   - **Common Mistakes** section with at least three entries:
     - *Fetching issue bodies* — wastes I/O and context; title prefix is the entire filter signal.
     - *Auto-snoozing on the user's behalf* — the user picks the new date; the agent does not infer (matches the "don't infer — ask" rule in `RESEARCHER.md` §5).
     - *Running on every turn instead of only session-start* — `task-remind` is a once-per-session pre-flight check, not a heartbeat.
3. **Commit:**

   ```bash
   git -C ~/code/dotfiles add nori-researcher/skills/task-remind/SKILL.md
   git -C ~/code/dotfiles commit -m "$(cat <<'EOF'
   task-remind: new skill for session-start reminder check over date-prefixed issues
   EOF
   )"
   ```

**Don't:** add a snooze-default-of-7-days. The user picks.

### Task 1.3 — Rename `triage-tasks` → `task-triage`

**Files:**
- `~/code/dotfiles/nori-researcher/skills/triage-tasks/SKILL.md` → `~/code/dotfiles/nori-researcher/skills/task-triage/SKILL.md`

**Steps:**

1. `git -C ~/code/dotfiles mv nori-researcher/skills/triage-tasks nori-researcher/skills/task-triage`
2. Update YAML `name: Triage-Tasks` → `name: Task-Triage`. Keep the existing `description` field's trigger phrases verbatim, but append `"task-triage"` (the new canonical phrase) at the front of the list.
3. Update the Announce line.
4. **Step 3 (Present inventory): show date prefix when present.** Per Decision 6, date-prefixed items stay in the inventory; just render the prefix as part of the title so the user sees both fired and not-yet-fired alongside each other. No filter, no separate section.
5. **Step 4 (Conversational priority): no change** — the framing questions and ordering proposal logic are surface-agnostic to whether items are dated.
6. **Commit:**

   ```bash
   git -C ~/code/dotfiles add nori-researcher/skills/task-triage/SKILL.md
   git -C ~/code/dotfiles commit -m "$(cat <<'EOF'
   task-triage: rename triage-tasks, surface date-prefix on inventory rows
   EOF
   )"
   ```

**Don't:** filter out date-prefixed items. They're tasks too; the user wants the full view.

### Task 1.4 — Verify dotfiles state + push

```bash
ls ~/code/dotfiles/nori-researcher/skills/ | grep -E 'task-(create|remind|triage)|capture-task|triage-tasks'
# Expected: only task-create, task-remind, task-triage.

git -C ~/code/dotfiles log --oneline -5
git -C ~/code/dotfiles push
```

If any of the old names linger (`capture-task`, `triage-tasks`), `git mv` didn't take — investigate before continuing.

---

## Phase 2 — `home_repo` config wiring

### Task 2.1 — Add `home_repo` field to `personal_info.md.template`

**File:** `template/templates/personal_info.md.template`

**Steps:**

1. Open the template. Find the section that holds user-level identity-shaped fields (next to GH username, paper-naming formats, etc. — per the Plan 06 schema split).
2. Add a new line:

   ```
   home_repo: <gh-user>/claude_research_config
   ```

   with a `<HOME_REPO>` placeholder for BOOTSTRAP substitution, parallel to the existing `<GH_USER>` / `<TOPIC>` placeholders.

3. Add a short comment line above it: `# Used by task-create and task-remind to route personal (non-research-project) tasks.`
4. Commit:

   ```bash
   git add template/templates/personal_info.md.template
   git commit -m "$(cat <<'EOF'
   personal_info: add home_repo field for task-skills routing
   EOF
   )"
   ```

**Don't:** put `home_repo` in `STATUS.md`. It's user-level, not per-project — see Decision 7.

### Task 2.2 — Extend BOOTSTRAP §4 Batch 3 to populate `home_repo`

**File:** `template/BOOTSTRAP.md` §4 (interview), Batch 3 (the same batch that — after Plan 08 — no longer asks for paper-naming).

**Steps:**

1. Find Batch 3. Locate the spot where post-Plan-08 it asks about GitHub identity + git fluency.
2. Add a one-line question after GH-user capture:

   > *"Want me to default your 'personal tasks' (the ones not tied to a research project) to a separate repo? I'll use `<gh-user>/claude_research_config` if you don't specify."*

   Accept the default silently (press-enter affordance, matching the Plan 06 paper-naming pattern); accept `owner/repo` overrides; if the user expresses confusion ("what does that mean?"), give the LIGHT explanation per `RESEARCHER.md` §0: *"`task-create` and `task-remind` will route stuff like 'remind me about the dentist next month' to this repo, so it doesn't clutter your research project's issue list."*
3. After the answer, substitute `<HOME_REPO>` into `personal_info.md` per the existing substitution pattern.
4. Commit:

   ```bash
   git add template/BOOTSTRAP.md
   git commit -m "$(cat <<'EOF'
   BOOTSTRAP: ask for home_repo with default in §4 Batch 3
   EOF
   )"
   ```

**Don't:** make this a hard-required question. Default + enter-to-accept is the affordance.

---

## Phase 3 — Port skills to `claude_researcher`

Ports follow the established Wave 2/3 recipe: copy the SKILL.md from dotfiles, add a provenance frontmatter block, insert a one-line REST-adaptation banner between frontmatter and body.

### Task 3.1 — Finalize the REST-adaptation banner wording (one-time)

**Decision:** the exact wording for these three skills, drafted in the Coupling Concerns section above. Restated here as a port-time judgment call:

```markdown
> **Runtime note (claude.ai):** This skill assumes a CLI environment with `gh` and `git` available. When run in the claude.ai sandbox, translate `gh issue create` / `gh issue list` / `gh search issues` into the GitHub REST API recipes from your Project Instructions; translate `git add`/`commit`/`push` into the `write_update` / `write_new` recipes likewise.
```

If port-time inspection of the SKILL.md bodies surfaces a `gh` subcommand not listed (e.g., `gh issue edit` in `task-remind`'s snooze action), **add it to the banner**, not as a separate note. One banner, every relevant verb listed.

### Task 3.2 — Port `task-create`

**Files:**
- Source: `~/code/dotfiles/nori-researcher/skills/task-create/SKILL.md`
- Destination: `template/skills/task-create/SKILL.md` (new directory)

**Steps:**

1. `mkdir -p template/skills/task-create`
2. Copy the dotfiles source into the destination.
3. **Insert provenance frontmatter** between the existing YAML and the body. The pattern (from add-paper's dual-source frontmatter, Plan 06):

   ```yaml
   ---
   name: Task-Create
   description: <existing description>
   nori_researcher_source: nori-researcher/skills/task-create/SKILL.md@<dotfiles-SHA>
   ---
   ```

   Capture the dotfiles SHA via `git -C ~/code/dotfiles rev-parse HEAD` at port time. Verify byte-identity between dotfiles source at that SHA and the destination body (mod the banner + frontmatter) via diff before committing.
4. **Insert the REST-adaptation banner** (Task 3.1) immediately after the frontmatter, before the first body section.
5. Commit:

   ```bash
   git add template/skills/task-create/SKILL.md
   git commit -m "$(cat <<'EOF'
   port: task-create from dotfiles with REST-adaptation banner
   EOF
   )"
   ```

### Task 3.3 — Port `task-remind`

Same structure as Task 3.2, substituting `task-remind`. Note the banner verbs include `gh issue edit` (snooze) and `gh issue close`.

### Task 3.4 — Port `task-triage`

Same structure as Task 3.2, substituting `task-triage`. Note the banner verbs include `gh search issues` (the cross-repo query).

---

## Phase 4 — Wire `task-remind` into session-start

### Task 4.1 — Add session-start instruction to `template/RESEARCHER.md`

**File:** `template/RESEARCHER.md`, §2 (session-start checklist).

**Steps:**

1. Find the §2 enumeration of session-start steps. After the existing pre-flight reads (STATUS.md, README.md, branch-level RESEARCH_LOG.md if applicable) and before any work-mode dispatch, add:

   > **Step 2.X — Check task reminders.** Read and follow `template/skills/task-remind/SKILL.md`. This is a once-per-session check, not a heartbeat. If there are no reminders pending, the skill outputs a single line and you continue. If there are, surface them before any work-mode dispatch so the user can decide whether to handle a reminder or proceed with the planned session.

   The exact step number depends on existing numbering — slot it after STATUS.md/README.md/RESEARCH_LOG.md reads but before the convo-name handshake (§2e). The principle: reminders are catch-up information, not work; surface them where the user is still in "what's the state of the world" mode.

2. Commit:

   ```bash
   git add template/RESEARCHER.md
   git commit -m "$(cat <<'EOF'
   RESEARCHER: wire task-remind into §2 session-start sequence
   EOF
   )"
   ```

**Don't:** add `task-remind` to the calibration block or any tier-keyed section. It runs identically regardless of `git_fluency`.

### Task 4.2 — CLI session-start hook (dotfiles `AGENTS.md`)

**File:** `~/code/dotfiles/nori-researcher/AGENTS.md`

**Steps:**

1. Find the session-start workflow checklist in AGENTS.md (the Nori-managed block that gets switched in via `sks switch researcher`).
2. After the existing pre-flight reads (STATUS.md, README.md, RESEARCH_LOG.md), add a one-bullet item:

   > Read `/Users/dan/.claude/skills/task-remind/SKILL.md` if a session-start reminder check is wanted. (Auto-on for `nori-researcher` profile; the skill self-exits cheaply if there are no pending reminders.)

   Defer to dan's judgment at execution time on exact placement — AGENTS.md is profile-author-territory.

3. Commit in dotfiles:

   ```bash
   git -C ~/code/dotfiles add nori-researcher/AGENTS.md
   git -C ~/code/dotfiles commit -m "$(cat <<'EOF'
   AGENTS: add task-remind to session-start checklist
   EOF
   )"
   ```

**Don't:** require `task-remind` to fire before the convo-name handshake. If the user has zero reminders the skill returns in one line; if they have reminders they're news, and news belongs before naming.

---

## Phase 5 — Cross-cutting docs updates

### Task 5.1 — Update `template/skills/SKILL_INDEX.md`

**File:** `template/skills/SKILL_INDEX.md`

**Steps:**

1. Open the index. Find the section structure — Plan 02 / Plan 07 established knowledge-management vs. writing-vs-working-style sections.
2. Add a new "Task management" section (or extend the closest existing section) with three entries:

   - `task-create` — Convert "I should remember to do X" into a tracked GH issue, with optional `[YYYY-MM-DD]` fire-date prefix for reminder-style items. Replaces the old `capture-task`.
   - `task-remind` — Session-start check for fired reminders in current repo + `home_repo`. Reads metadata only.
   - `task-triage` — Cross-repo open-task inventory + conversational priority discussion. Read-only. Renamed from `triage-tasks`.

3. **Remove or update any prior references** to `capture-task` or `triage-tasks` in SKILL_INDEX.md. They didn't ship to `claude_researcher` per the convo's mid-session surprise, so there's likely nothing to remove on the claude_researcher side; verify via grep.
4. Update the status block at the top of SKILL_INDEX.md (currently reads "all sections live" with the REST-adaptation caveat) to note that the task-skills triplet is the newest addition.
5. Commit:

   ```bash
   git add template/skills/SKILL_INDEX.md
   git commit -m "$(cat <<'EOF'
   SKILL_INDEX: add task-create / task-remind / task-triage
   EOF
   )"
   ```

### Task 5.2 — Add the LIGHT-explanation principle to `RESEARCHER.md` §0

**File:** `template/RESEARCHER.md` §0 Persona.

**Steps:**

1. Find §0 Persona's four tier-independent traits (follow instructions, push back on bad ideas, don't make decisions silently, stay organized) — per Plan 03's `0c99e5b` and Plan 04's retrofit work.
2. Add a fifth sentence (or extend "don't make decisions silently") with the new behavioral rule:

   > **Briefly explain back-end behavior the user might want to understand.** When the agent does something the user didn't explicitly request — e.g., routing a task to a different repo because it's flagged personal, snoozing a reminder by mutating an issue title — say one sentence about *why*, not silently execute. Calibrate length to context: a one-clause aside in the next message, not a paragraph.

3. Commit:

   ```bash
   git add template/RESEARCHER.md
   git commit -m "$(cat <<'EOF'
   RESEARCHER §0: add LIGHT-explanation principle for back-end behavior
   EOF
   )"
   ```

**Don't:** make this a tier-keyed elaboration. It applies at all `git_fluency` levels — the *content* of the explanation may vary (a `fluent` user gets a terser version), but the principle of explaining is universal.

---

## Phase 6 — Migration of existing callers

### Task 6.1 — Verify dotfiles `~/.claude/skills/` symlinks updated

**Why:** If Dan's local `~/.claude/skills/` directory has symlinks pointing at the old `capture-task` / `triage-tasks` paths in dotfiles, they break after the rename in Phase 1.

**Steps:**

1. `ls -la ~/.claude/skills/ | grep -E 'task-create|task-remind|task-triage|capture-task|triage-tasks'`
2. If old-name symlinks exist, replace them:

   ```bash
   rm ~/.claude/skills/capture-task
   rm ~/.claude/skills/triage-tasks
   ln -s ~/code/dotfiles/nori-researcher/skills/task-create ~/.claude/skills/task-create
   ln -s ~/code/dotfiles/nori-researcher/skills/task-remind ~/.claude/skills/task-remind
   ln -s ~/code/dotfiles/nori-researcher/skills/task-triage ~/.claude/skills/task-triage
   ```

   Or whatever sync mechanism the dotfiles `install.sh` uses — defer to its idempotent reinstall path if it exists.

3. Verify via `ls -la ~/.claude/skills/task-create` (and the others) that the symlink resolves.

**Don't:** delete the dotfiles directories — only the local `~/.claude/skills/` symlinks need updating.

### Task 6.2 — Manual smoke test in a fresh CLI session

**Why:** Per Plan 02's empirical-first principle, we don't ship without one real run.

**Steps:**

1. Open a fresh Claude Code session in any research repo with `gh` available.
2. Trigger `task-create` via natural language: *"add a task: re-check egress allow-list next week."*
3. Verify the agent: asks "when?", accepts the relative date, computes ISO, prepends to title, creates the issue with `[YYYY-MM-DD]` prefix and `task` label, back-links to the current convo doc (or prompts about cross-repo back-link if routed to home).
4. Open a new fresh session in the same repo. Verify `task-remind` runs at session-start and finds the just-filed reminder if the prefix date is today or earlier (override with a manual edit if needed for the smoke test).
5. Snooze it. Verify the title is rewritten with a future date and the next session doesn't show it.
6. Trigger `task-triage`. Verify the full inventory shows both dated and undated items in the same view (Decision 6).
7. Record observations in a session-end convo update; surface any divergence from the plan to Dan before continuing.

**Don't:** mark this plan shipped without running the smoke test. The whole runtime-detection caveat from Wave 2/3 applies here.

### Task 6.3 — claude.ai web smoke test (deferred to first real web session)

**Why:** The REST-adaptation banner approach is still empirically untested at the runtime layer (Plan 02 §8 Parking Lot item). These three skills are good first-evidence targets because they exercise `gh issue create` / `gh issue list` / `gh search issues` / `gh issue edit` / `gh issue close` — a broader-than-paper-processing API surface.

**Steps:**

1. Note in this plan's wrap-up (Phase 7 commit message) that the web-side smoke test is pending.
2. Surface to Dan for scheduling alongside Plan 02's existing first-beta-session ask. Don't gate plan-shipping on it.

---

## Phase 7 — Verification, ship, PR

### Task 7.1 — Verification script

Run a small check before the final commit (no test framework — this is a content audit):

```bash
# 1. All three skills exist in both surfaces
ls ~/code/dotfiles/nori-researcher/skills/task-create/SKILL.md
ls ~/code/dotfiles/nori-researcher/skills/task-remind/SKILL.md
ls ~/code/dotfiles/nori-researcher/skills/task-triage/SKILL.md
ls template/skills/task-create/SKILL.md
ls template/skills/task-remind/SKILL.md
ls template/skills/task-triage/SKILL.md

# 2. Old names are gone in dotfiles
! ls ~/code/dotfiles/nori-researcher/skills/capture-task/ 2>/dev/null
! ls ~/code/dotfiles/nori-researcher/skills/triage-tasks/ 2>/dev/null

# 3. Provenance frontmatter present in all three ports
grep -l 'nori_researcher_source:' template/skills/task-create/SKILL.md template/skills/task-remind/SKILL.md template/skills/task-triage/SKILL.md

# 4. REST-adaptation banner present in all three ports
grep -l 'Runtime note (claude.ai)' template/skills/task-create/SKILL.md template/skills/task-remind/SKILL.md template/skills/task-triage/SKILL.md

# 5. SKILL_INDEX references all three
grep -c 'task-create\|task-remind\|task-triage' template/skills/SKILL_INDEX.md
# Expected: 3 or more

# 6. RESEARCHER.md mentions task-remind in §2
grep -n 'task-remind' template/RESEARCHER.md

# 7. personal_info.md.template has home_repo field
grep -n 'home_repo' template/templates/personal_info.md.template

# 8. No stale basic_config references in this branch's diff
git diff main...HEAD -- template/ docs/ | grep -i 'basic_config' || echo "clean"

# 9. claude_research_config references look right
grep -rn 'claude_research_config' template/ docs/plans/09_task_skills.md
```

Any check failing → fix before ship commit.

### Task 7.2 — Re-run `tools/repin.py` if any of `README.md` / `BOOTSTRAP.md` / pinned templates changed

Per Plan 08's pattern and the 2026-05-20 SHA-pin discipline: if Phase 2's BOOTSTRAP edit touched any SHA-pinned template URL, the pins need to be bumped before merge.

```bash
python3 tools/repin.py --dry-run
```

Inspect the diff. If non-empty, run without `--dry-run` and commit the two SHA bumps the script makes (parallel to Plan 08's `4fbc745` + `2e9c11d` pair). If empty (likely, since this plan doesn't touch README's bootstrap-entry URL), skip.

### Task 7.3 — Update STATUS.md

**File:** `STATUS.md`

**Steps:**

1. Add a "Recent sessions" entry at the top of the section per repo convention. Format matches existing entries — bolded date + 1-paragraph summary mentioning Phases shipped, files touched, key decisions exercised at execution, smoke test result.
2. **If `task-skills` is being merged as part of this ship**, also update the "Branch" summary line under "Current state" to mark task-skills as merged with the PR number and merge commit SHA (matching the Plan 08 / repin-tooling pattern).
3. Commit:

   ```bash
   git add STATUS.md
   git commit -m "$(cat <<'EOF'
   STATUS: Plan 09 shipped — task-create / task-remind / task-triage live
   EOF
   )"
   ```

### Task 7.4 — Run `finish-convo`, push, open PR via `finishing-a-development-branch`

Follow the established pattern:

1. `/finish-convo` to checkpoint the session's convo doc + push.
2. `/finishing-a-development-branch` to create the PR. PR description should:
   - Summarize the three skills shipped + the `home_repo` config + the §0 + §2 RESEARCHER.md additions.
   - Link to issue #13 (which this operationalizes).
   - Note the deferred web smoke test (Task 6.3) so review knows what's empirically validated and what isn't.
   - Reference Plan 08 (PR #16) as the merged precondition for the §1b allow-all + revisit pairing.

---

## Testing Plan

These are content/instruction-shaped skills (Markdown for an LLM to follow), not code with test-runnable behavior. The verification posture is therefore Plan-08-style: layered manual checks rather than automated tests.

I will run the Phase 7.1 verification script as the structural audit — it catches missing files, missing frontmatter, missing banners, missing cross-references, stale `basic_config` strings, and absent `home_repo` plumbing. This audit verifies *file structure*, not behavior.

I will run the Phase 6.2 CLI smoke test as the behavioral verification — file → trigger phrase → expected agent action → expected GH issue / convo back-link / mutation. This exercises the actual user-visible behaviors (does `task-create` ask "when?"; does `task-remind` filter to fired items via the date prefix; does `task-triage` show dated items alongside undated; does `task-create`'s personal-list path route to `home_repo` and ask the back-link question per Decision 8).

I will defer the Phase 6.3 web smoke test as a documented deferred validation, surfaced to Dan, because (a) it requires a fresh claude.ai session orchestrated by the user, and (b) it's the existing Wave 2/3 empirical question, not new scope.

NOTE: I will write *all* tests before I add any implementation behavior. (Strictly: in this content-shaped plan, the "test" is the verification script in 7.1 — write it before running 7.1.)

---

**Testing Details:** The Phase 7.1 verification script is the only thing that resembles a test artifact. It checks file existence, frontmatter presence, banner presence, cross-references, stale strings — all *structural* properties of the shipped artifacts. It deliberately does **not** lint or parse the skill bodies for behavioral correctness; that's the smoke tests in 6.2 (CLI, mandatory before ship) and 6.3 (web, deferred). The smoke tests verify *behavior*: a real GH issue gets created with the right prefix when the user asks for a date; `task-remind` returns the one-line no-pending output when there are no fired items; the title prefix is what gets mutated on snooze (not the body). No mocks; everything runs against the user's real GH account in a research repo.

**Implementation Details:**
- Skill bodies are Markdown for an LLM. There is no code under test in the traditional sense.
- `gh` CLI is the runtime dependency on both surfaces; `web` translates via the REST banner.
- `home_repo` defaults to `<gh-user>/claude_research_config` at runtime if unset — no hard failure on missing key.
- Date math uses `date -u` with BSD/GNU fallback; the agent picks the form that works in the current shell.
- The Nori commit-author hook still requires heredoc-form commit messages; honor it throughout.
- Snooze mutates the title prefix, not the body. The body is never read by `task-remind`.
- `task-triage` does NOT filter date-prefixed items — they appear inline with undated tasks (Decision 6).
- Old skill directory names (`capture-task`, `triage-tasks`) are `git mv`'d in place; no alias period (Decision 9).
- All three ported skills get the same REST-adaptation banner (different verbs listed inline).
- No new tooling, no new dependencies, no new tests beyond the verification script.

**What could change:**
- **REST-adaptation banner vs. proper REST adaptation.** If the Wave 2/3 empirical question (Plan 02 §8 Parking Lot) resolves against the banner approach, all three ported skills get rewritten to inline REST recipes — same shape, fuller adaptation work. This plan doesn't pre-judge.
- **`task-remind` execution model.** Currently inline main-agent (Decision 11). If web sandbox behavior at runtime turns out to handle subagent-style isolation poorly OR if the user asks for batched no-user-interaction mode, the framing shifts to a literal background step (still possible without an Agent tool — the agent just runs the skill silently when the no-pending case fires).
- **`home_repo` default name.** Currently `<gh-user>/claude_research_config`, contingent on issue #14 shipping with that name. If #14 ships with a different name, all the references in this plan need a sweep before execution.
- **`task-triage` filter.** Decision 6 says no filter on dated items. If real use shows the inventory gets dominated by long-tailed reminders, a future revision could add a *display* convention (collapse-by-default a "snoozed" group) without changing the underlying query.
- **Date-prefix encoding format.** Currently `[YYYY-MM-DD] `. If natural-language parsers in future skills want a richer encoding (recurrence, timezone), the prefix shape can extend — but session-start filtering depends on a regex match, so any extension preserves the leading `[YYYY-MM-DD]` shape.

**Questions:**

1. **Confirm `<gh-user>/claude_research_config` as the `home_repo` default.** Issue #14 specifies the rename name; this plan inherits it. Sanity-check at execution time that #14 actually shipped with that exact name (not `personal_config`, not `research_config`, etc.). If it didn't, sweep the plan's references before Phase 2.

2. **CLI session-start hook placement in dotfiles `AGENTS.md`.** Task 4.2 defers exact placement to Dan since `AGENTS.md` is profile-author-territory. Recommend before convo-name handshake; confirm at execution.

3. **Should `task-remind` filter out items with prefix dates in the *far future* (say, >30 days out)?** No — they're snoozed reminders, not currently relevant, and the metadata-only query is cheap; the filter is on `<= today`, anything beyond is silently skipped at the date-compare step. This question is asked here so the implementing agent doesn't get clever and add a far-future cutoff.

4. **Smoke test ordering — CLI first vs. web first.** Plan recommends CLI first (Phase 6.2) because the source-of-truth body is local and the failure mode is "agent didn't follow instructions" rather than "REST translation broke." Web smoke test (6.3) is deferred because it's the existing Wave 2/3 empirical question. Confirm or override at execution.

5. **Does `task-triage` need a `task` label requirement?** All three skills assume `task`-labeled issues. If a user has tracked tasks without the label (legacy from before `capture-task` standardized on it), this plan doesn't sweep them. Out of scope; can revisit if it bites in practice.

---
