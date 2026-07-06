# Skill Index

This is the manifest of skills available in `claude_researcher`. The runtime agent fetches this file at session start (per `RESEARCHER.md` §2d) to know what skills exist and when to use them. Individual `SKILL.md` files are **fetched on-demand** when their trigger conditions match — don't load all of them upfront.

**Status:** all sections live. The **Working-style skills** are SWE carryovers from upstream Nori — they don't touch git or filesystem axes and work as-is. The **Session lifecycle**, **Knowledge-management**, and **Task management** skills are Researcher-authored, shipped with a `## Runtime detection` header that probes both environments affirmatively: `$IS_SANDBOX` / `/mnt/skills/public` for claude.ai, `$CLAUDECODE=1` for Claude Code, with an `unknown` branch that surfaces misconfiguration instead of silently guessing. In claude.ai mode the runtime is clone-first per `RESEARCHER.md` §2.0b: the agent runs `git add` / `git commit` / `git push` directly against the project-repo clone at `/home/claude/<REPO>/`, reads skills from the local template clone, and translates only the `gh` issues/search/label/repo/api verbs the task-skills use into the GitHub Issues/Search REST endpoints from Project Instructions — Issues and Pulls remain REST surfaces. The REST Contents-API recipes (`write_update` / `write_new`) are the documented degraded fallback for when the §2.0b clone fails, surfaced to the user (one commit per file). The **Writing & document workflow** skills are AITaxBID-sourced (from Andrea Lopez-Luzuriaga's kit): `iterative-writing-workflow` is pure methodology with no git/CLI operations, and `branch-document-review` carries REST recipes (the GitHub refs/merges/compare endpoints) inline where they're needed — so neither needs the runtime-detection banner. The **Task management** triplet (`task-create`, `task-remind`, `task-triage`) is the newest addition (Plan 09, 2026-06-04), pinned to dotfiles `8b619b5`.

---

## Manifest contract

Each entry below has:

- **Name** (matches the skill's `SKILL.md` `name:` frontmatter)
- **Trigger** (when the agent should fetch and use it)
- **URL** (the upstream URL to WebFetch the `SKILL.md` from). Primary read path is the local template clone (`/home/claude/.claude_researcher_template/template/skills/<name>/SKILL.md`); the URL is the WebFetch fallback when the §2.0a clone is absent.

Skills are grouped by lifecycle role.

---

## Session lifecycle skills

### start-research-line

- **Trigger:** user wants to start a new research line ("start a new line", "cut a branch for X", "let's begin Y"). Bundles branch creation + `docs/active/<line>/` scaffold + `RESEARCH_LOG.md` seed + STATUS.md Active Research Lines table update as one atomic ceremony, so future session-start reads see the line at a glance.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/start-research-line/SKILL.md`

### finish-convo

- **Trigger:** user signals end of session ("good stopping point", "let's wrap", "save and stop"). Lighter wrap-up than the full research-line merge in `RESEARCHER.md` §6.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/finish-convo/SKILL.md`

### update-docs

- **Trigger:** mid-session checkpoint ("save what we've got"). Same writes as finish-convo without the "session is ending" framing.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/update-docs/SKILL.md`

### init-research-repo

- **Trigger:** during bootstrap only — not normally invoked at runtime. Used by `BOOTSTRAP.md` Step 9 to seed a fresh research repo.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/init-research-repo/SKILL.md`

---

## Knowledge-management skills

### add-paper

- **Trigger:** user asks to add a paper to the collection ("add this paper", "save this PDF", "ingest these papers from `papers/`"). Triage skill: routes academic-style papers to `paper-processing-academic`, institutional-style reports to `paper-processing-institutional`, non-paper documents to `document-processing` (deferred). Run Step 0 here; the routed per-protocol skill handles Steps 1-6.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/add-paper/SKILL.md`

### paper-processing-academic

- **Trigger:** Protocol A workflow for academic-style papers (research with hypothesis + original data analysis). Usually invoked via `add-paper`'s Step 0 dispatch; can be invoked directly when the protocol is already known.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/paper-processing-academic/SKILL.md`

### paper-processing-institutional

- **Trigger:** Protocol B workflow for institutional-style reports (synthesis/policy documents from multilaterals, governments, working groups). Usually invoked via `add-paper`'s Step 0 dispatch; can be invoked directly when the protocol is already known. Step 2 carries institutional-specific extraction rules (preserve acronyms, preserve boxes/figure captions, strip decorative front matter).
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/paper-processing-institutional/SKILL.md`

### audit-docs

- **Trigger:** user asks to audit `docs/` consistency, or you notice orphaned convos / unindexed plans / broken links.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/audit-docs/SKILL.md`

### audit-papers

- **Trigger:** user asks to audit `papers/`, or you notice PDFs without text extraction or summaries.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/audit-papers/SKILL.md`

---

## Task management skills

These three skills share a single GitHub-Issues backend (issues with the `task` label, `[YYYY-MM-DD]` date prefix in the title encoding fire-date for reminder-style items). `home_repo` from `personal_info.md` routes "personal" tasks away from the current research repo; default is `<gh-user>/claude_research_config`.

### task-create

- **Trigger:** user says "add a task," "capture this," "track this for later," "remind me later," "add a reminder," "track this with a date," or similar. Converts the TODO into a tracked GH issue with optional `[YYYY-MM-DD]` fire-date prefix. Replaces the older `capture-task`.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/task-create/SKILL.md`

### task-remind

- **Trigger:** session-start auto-load (wired into `RESEARCHER.md` §2d.5). Queries current repo + `home_repo` for open issues with a `[YYYY-MM-DD]` title prefix `<= today`. Reads metadata only — no body fetches. Also responds to "check reminders," "what's pending," "/task-remind."
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/task-remind/SKILL.md`

### task-triage

- **Trigger:** user says "task-triage," "triage," "what should I work on," "/task-triage," or wants a cross-repo view of pending work. Cross-repo open-task inventory + conversational priority discussion. Read-only (does not modify issues). Renamed from `triage-tasks`.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/task-triage/SKILL.md`

---

## Writing & document workflow skills

### iterative-writing-workflow

- **Trigger:** user is working on a writing project that involves both research/reading and producing written deliverables (white papers, policy notes, reports, academic papers, book chapters). Also use when user asks to set up a writing workflow, wants to organize how they collaborate on a document, or says things like "let's start writing," "how should we work on this," or "set up the project."
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/iterative-writing-workflow/SKILL.md`

### branch-document-review

- **Trigger:** Claude and the user are jointly producing a document and the user wants to read and comment on it before signoff — typically a long markdown deliverable with companion artifacts (`.docx`, `.pptx`) generated from it. Do **not** use for general-purpose branch work (experiments, code refactors, parallel versions) — those use plain git.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/branch-document-review/SKILL.md`

---

## Working-style skills (carried over from upstream Nori)

### brainstorming

- **Trigger:** user is developing a rough idea and needs structured questioning to refine it. Use **before** writing implementation plans or code.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/brainstorming/SKILL.md`

### test-driven-development

- **Trigger:** implementing any feature or bugfix in code. Write the test first, watch it fail, write minimal code to pass.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/test-driven-development/SKILL.md`

### testing-anti-patterns

- **Trigger:** writing or changing tests, adding mocks, tempted to add test-only methods to production code.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/testing-anti-patterns/SKILL.md`

### systematic-debugging

- **Trigger:** any bug, test failure, or unexpected behavior — before proposing fixes.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/systematic-debugging/SKILL.md`

### root-cause-tracing

- **Trigger:** errors deep in execution where you need to trace back through the call stack to find the original trigger.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/root-cause-tracing/SKILL.md`

### creating-debug-tests-and-iterating

- **Trigger:** difficult debugging task where you need to replicate a bug or behavior in a test to see what's going wrong.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/creating-debug-tests-and-iterating/SKILL.md`

### receiving-code-review

- **Trigger:** code review feedback arriving, especially when feedback seems unclear or technically questionable.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/receiving-code-review/SKILL.md`

### write-a-plan

- **Trigger:** a research conversation has produced something ready to implement, and you need to capture the plan in a doc that an implementing agent (with no prior context) can follow.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/write-a-plan/SKILL.md`

### handle-large-tasks

- **Trigger:** a task is large enough that completing it in one session will exhaust the context window.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/handle-large-tasks/SKILL.md`

---

## Skills intentionally not ported

These skills exist in upstream Nori but don't apply to `claude_researcher`'s claude.ai runtime. Listed here so the agent doesn't search for them.

- `use-worktree`, `clean-worktrees` — local-filesystem-only; no parallel to git worktrees in claude.ai sandbox.
- `webapp-testing`, `building-ui-ux` — out of scope for v1 (no webapp frontend in research workflow).
- `using-screenshots` — claude.ai handles images natively in chat.
- `finishing-a-development-branch` — collapsed into `RESEARCHER.md` §6 wrap-up (the merge-PR-and-archive flow lives in RESEARCHER.md, not a skill).
- `updating-noridocs` — Nori-specific; no Nori on the web side.
- `maintaining-decision-docs` — out of scope for v1 research repos.

---

## How skills are added

When a new skill is ported (Phase 6 work), add an entry above with the same three fields. Keep the lifecycle grouping. Skills can be removed by moving them to "Skills intentionally not ported" with a rationale.
