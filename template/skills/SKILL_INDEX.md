# Skill Index

This is the manifest of skills available in `claude_researcher`. The runtime agent fetches this file at session start (per `RESEARCHER.md` §2d) to know what skills exist and when to use them. Individual `SKILL.md` files are **fetched on-demand** when their trigger conditions match — don't load all of them upfront.

**Status:** all sections live. The **Working-style skills** are SWE carryovers from upstream Nori — they don't touch git or filesystem axes and work as-is. The **Session lifecycle** and **Knowledge-management** skills are Researcher-authored, shipped with a `## Runtime detection` header that probes both environments affirmatively: `$IS_SANDBOX` / `/mnt/skills/public` for claude.ai, `$CLAUDECODE=1` for Claude Code, with an `unknown` branch that surfaces misconfiguration instead of silently guessing. In claude.ai mode the agent translates Claude-Code idioms — `git add` / `git commit` / `git push`, and local paths like `/Users/<user>/.claude/skills/...` — into claude.ai-equivalents (REST `write_update` / `write_new` recipes from Project Instructions, and `raw.githubusercontent.com` URLs fetched via WebFetch). Proper REST adaptation — embedding the recipes inline rather than relying on translation — lands in [`docs/plans/02_skill_ports.md`](https://github.com/danparshall/claude_researcher/blob/main/docs/plans/02_skill_ports.md) Waves 2-3.

---

## Manifest contract

Each entry below has:

- **Name** (matches the skill's `SKILL.md` `name:` frontmatter)
- **Trigger** (when the agent should fetch and use it)
- **URL** (the upstream URL to WebFetch the `SKILL.md` from)

Skills are grouped by lifecycle role.

---

## Session lifecycle skills

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

- **Trigger:** user asks to add a paper to the collection ("add this paper", "save this PDF", "ingest these papers from `papers/`").
- **Modes:** download (URL → PDF → text → index) and orphan-ingestion (PDF already in `papers/` → rename per `paper_naming` → text → index).
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/add-paper/SKILL.md`

### audit-docs

- **Trigger:** user asks to audit `docs/` consistency, or you notice orphaned convos / unindexed plans / broken links.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/audit-docs/SKILL.md`

### audit-papers

- **Trigger:** user asks to audit `papers/`, or you notice PDFs without text extraction or summaries.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/audit-papers/SKILL.md`

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
