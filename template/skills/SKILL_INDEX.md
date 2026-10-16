# Skill Index

This is the manifest of skills available in `claude_researcher`. The runtime agent fetches this file at session start (per `RESEARCHER.md` §2d) to know what skills exist and when to use them. Individual `SKILL.md` files are **fetched on-demand** when their trigger conditions match — don't load all of them upfront.

**Status:** all sections live. The **Working-style skills** are SWE carryovers from upstream Nori — they don't touch git or filesystem axes and work as-is. The **Session lifecycle**, **Knowledge-management**, and **Task management** skills are Researcher-authored; surface detection and `{{skills_dir}}` resolution happen once in `RESEARCHER.md` §2.0a, and each skill keeps only a two-line surface note after its frontmatter. In claude.ai mode the runtime is clone-first per `RESEARCHER.md` §2.0b: the agent runs `git add` / `git commit` / `git push` directly against the project-repo clone at `/home/claude/<REPO>/`, reads skills from the local template clone, and translates only the `gh` issues/search/label/repo/api verbs the task-skills use into the GitHub Issues/Search REST endpoints from Project Instructions — Issues and Pulls remain REST surfaces. The REST Contents-API recipes (`write_update` / `write_new`) are the documented degraded fallback for when the §2.0b clone fails, surfaced to the user (one commit per file). The **Writing & document workflow** skills are AITaxBID-sourced (from Andrea Lopez-Luzuriaga's kit): `iterative-writing-workflow` is pure methodology with no git/CLI operations, and `branch-document-review` carries REST recipes (the GitHub refs/merges/compare endpoints) inline where they're needed — so neither needs surface handling beyond §2.0a. The **Task management** triplet (`task-create`, `task-remind`, `task-triage`) is the newest addition (Plan 09, 2026-06-04), pinned to dotfiles `8b619b5`.

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

- **Trigger:** user signals end of session ("good stopping point", "let's wrap", "save and stop"). Lighter wrap-up than `finishing-a-research-branch`. Writes convo doc + a one-line RESEARCH_LOG entry (never STATUS.md, except a LITE repo's `## Sessions` entry), commits, pushes, confirms the push, and ends with the close-out sentinel line. Branch stays open.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/finish-convo/SKILL.md`

### finishing-a-research-branch

- **Trigger:** user signals the research line is done and ready to merge ("done", "ready to ship", "let's merge it"). Full close-out ceremony: confirmation gate, finish-convo checkpoint + audit-docs on the still-open line, move `docs/active/<branch>/` → `docs/historical/<branch>/`, move the STATUS row Active → Archived (rolling Archived rows beyond the newest 10 into `HISTORY.md`), then PR + merge — or, for a main-direct line, push `main` with no PR. Use `finish-convo` instead for mid- or end-of-session checkpoints that keep the branch open.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/finishing-a-research-branch/SKILL.md`

### update-docs

- **Trigger:** mid-session checkpoint ("save what we've got"). Same writes as finish-convo without the "session is ending" framing: convo doc (with a `**Session:**` header line) + one-line RESEARCH_LOG entry; STATUS.md untouched (LITE `## Sessions` excepted).
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/update-docs/SKILL.md`

### init-research-repo

- **Trigger:** an existing repo (or one created outside bootstrap) needs the research doc structure — not normally invoked at runtime. `BOOTSTRAP.md` Step 7 seeds new repos with its own inline files and does not call this skill. Scaffolds `docs/active/`, `docs/historical/`, `data/{raw,interim,processed,reference}/` with a README, a sensible `.gitignore` (Python + Cookiecutter-DS data pattern), STATUS.md's Project parameters + Active/Archived Research Lines sections, an empty HISTORY.md, and README.md if absent. Seed files live in its `templates/`. For a repo that will hold papers it hands off to `init-paper-collection`.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/init-research-repo/SKILL.md`

### init-paper-collection

- **Trigger:** a research repo will hold papers and has no `PAPER_SUMMARIES.md` yet — usually reached from `init-research-repo`. Creates `papers/` and `papers/text/`, seeds `PAPER_INDEX.md` and `PAPER_SUMMARIES.md` with the generated-block markers and an empty `paper_index.toml` from its `templates/`, installs the check-only pre-commit hook and sets `core.hooksPath`, then runs `paper-index` `index` + `check`. Never overwrites an existing file; a legacy-format collection is a migration, not a seed.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/init-paper-collection/SKILL.md`

### init-code-scaffold

- **Trigger:** a research repo starts needing to hold code and doesn't have `src/` yet — the researcher is about to write more than a one-off script. Lazy companion to `init-research-repo`; creates `src/<pkg>/`, `scripts/`, `tests/`, `notebooks/`, `pyproject.toml`, `.python-version` using `uv`. Skip for pure-reading, pure-writing, or papers-only repos.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/init-code-scaffold/SKILL.md`

---

## Knowledge-management skills

### add-paper

- **Trigger:** user asks to add a paper to the collection ("add this paper", "save this PDF", "ingest these papers from `papers/`"), or a blog post / thread worth keeping. One flow: obtain the source (filename per the user's `Paper naming format`, else the default), extract text, write the `PAPER_SUMMARIES.md` entry in the metadata contract (`### <slug>`, `**Title:**`, bold bullets incl. `Focus` / `One-liner` / `Related` / `Summarized`), then `paper-index` `index` + `check` — rows are generated, never hand-written. Non-PDF sources get a `Text extraction` bullet. Institutional reports may follow `paper-processing-institutional`'s fuller body. Bulk (4+): per-paper subagents write entry fragments; the orchestrator inserts them serially.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/add-paper/SKILL.md`

### paper-processing-academic

- **Trigger:** Protocol A workflow for academic-style papers (research with hypothesis + original data analysis): the (a)–(d) summary body plus BibTeX, under the same metadata-contract header `add-paper` writes. Invoke directly when a project uses Protocol A summaries. Andrea's fork, maintained here.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/paper-processing-academic/SKILL.md`

### paper-processing-institutional

- **Trigger:** Protocol B workflow for institutional-style reports (synthesis/policy documents from multilaterals, governments, working groups), under the same metadata-contract header `add-paper` writes. `add-paper` points institutional reports here. Andrea's fork, maintained here. Step 2 carries institutional-specific extraction rules (preserve acronyms, preserve boxes/figure captions, strip decorative front matter).
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/paper-processing-institutional/SKILL.md`

### audit-docs

- **Trigger:** user asks to audit `docs/` consistency, or you notice orphaned convos / unindexed plans / broken links.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/audit-docs/SKILL.md`

### audit-papers

- **Trigger:** user asks to audit `papers/`, or you notice PDFs without text extraction or summaries. Structure via `paper-index` `check`; then a scoped accuracy pass that verifies entries against `papers/text/` (numbers checked against the source tables). Fixes go in entries, then `index` + `check`.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/audit-papers/SKILL.md`

### paper-index

- **Trigger:** user asks to regenerate `PAPER_INDEX.md` / `PAPER_RELATED.md` or check them against `PAPER_SUMMARIES.md` ("regen the index", "run paper-index check", "the counts are stale"), or wants to add the check-only pre-commit hook to a paper-collection repo. Bundles the stdlib-only `paper_index.py` dispatcher with `index` / `check` / `counts` subcommands; PAPER_SUMMARIES.md is the source of truth and everything else (INDEX marker blocks, RELATED reverse index, the SUMMARIES header count) is derived from it. Python 3.9+.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/paper-index/SKILL.md`

### condense-summary

- **Trigger:** user asks to condense a summary, write or shorten an entry's one-liner / index row ("condense this summary", "the index row for X is too long", "backfill one-liners for section Y"). Brings the `PAPER_SUMMARIES.md` entry up to complete first (reads the source if the entry lacks numbers or a Relevance paragraph), then writes `Focus` and the ≤50-word `One-liner`, renames the related-entries field to `Related`, and regenerates the row with `paper-index`. Bundles `condense_check.py` (stdlib, Python 3.9+).
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/condense-summary/SKILL.md`

### add-to-reading-list

- **Trigger:** user says "add to reading list", "save this for later", "queue this", "read later". Appends an entry with a short "why" to `READING_LIST.md` at repo root; a paper not yet in the collection goes through `add-paper` first.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/add-to-reading-list/SKILL.md`

### review-reading-list

- **Trigger:** user says "what's on my reading list", "review the reading list", "let's look at X from my list". Pulls an item off `READING_LIST.md`, discusses it in depth, appends the discussion notes to the paper's `PAPER_SUMMARIES.md` entry (or the RESEARCH_LOG for non-paper items), and removes it from the list.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/review-reading-list/SKILL.md`

### add-deliverable

- **Trigger:** user is about to create an outward-facing deliverable — a paper, memo, bill response, briefing, essay, testimony, or any artifact leaving the repo for an external audience ("start a paper," "let's draft the memo," "cut a target for the bill response"). Creates `deliverables/<target>/` with a seeded `LINEAGE.md` capturing which research lines fed the deliverable (pinning merge-commit SHAs, not branch HEADs) and where citable numbers came from. Tiered rigor: light claim+source+SHA default, upgrade to fuller Method-column format for numbers that will be defended externally.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/add-deliverable/SKILL.md`

### audit-repo-structure

- **Trigger:** user asks to check the repo's folder layout against the framework's guardrails ("audit the layout", "is this repo tidy", "check folder structure", "guardrails audit"), or you notice signs of drift (root-level `results/`/`output/`/`reports/`, `project_docs/` alongside `docs/`, loose PDFs at root, `deliverables/<target>/` without `LINEAGE.md`, partial code scaffold). Walks nine finding buckets (A: root sprawl; B: duplicate doc dirs; C: workstream shadow taxonomy; D: root accumulation; E: `data/` non-conformance; F: partial code scaffold; G: LINEAGE gaps; H: notebook rot; I: standing exceptions). Reports bucket-at-a-time, no auto-fix, respects the operational-repo caveat (`policy-levers/`-style repos legitimately deviate from research-first defaults). Surfaces cross-audit patterns in the summary — e.g., repeated Bucket C exceptions signal the repo may want the deferred operations-mode archetype.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/audit-repo-structure/SKILL.md`

### audit-status

- **Trigger:** user asks to audit STATUS.md, check repo hygiene, or make sure STATUS is current after several sessions of active work ("audit STATUS", "check repo hygiene", "STATUS looks stale"). Cross-references Active/Archived Research Lines tables against actual git branch state (merged vs unmerged); verifies Archived Material references resolve (consolidated dirs OK, pending-deletion branches suppressed); mode-aware schema checks (Recent Sessions presence is a finding in branches mode; capped in main_only) and bloat flags (soft >200 lines, firm >300 in branches mode); reports derived last-activity-per-line recency. Requires clone-first mode (§2.0b); stops cleanly in degraded REST fallback.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/audit-status/SKILL.md`

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

## Runtime / meta skills

### resolve-runtime-issue

- **Trigger:** a session-start fetch, git operation, or REST call fails in a way that isn't self-explanatory — a GitHub proxy refusal (repo not attached, repo not found, API path not available, GitHub not connected, app not installed, `gh` blocked), a refused permission check, network error, non-fast-forward push (with the safe append-conflict recovery), protected-branch push, lost sandbox state, missing config, stale raw-CDN read. Contains the recovery table that used to live in RESEARCHER.md's Appendix.
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/resolve-runtime-issue/SKILL.md`

### report-upstream-issue

- **Trigger:** user reports a bug in `claude_researcher` itself (this file, the skills, the bootstrap, the template scripts) — not a problem with their own research. Produces a pre-filled GitHub issue URL against the upstream repo; the user clicks to file. Enforces the MUST-NOT list for issue-body contents (no credentials, no research-repo contents, no identifying info without consent).
- **URL:** `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/report-upstream-issue/SKILL.md`

---

## Skills intentionally not ported

These skills exist in upstream Nori but don't apply to `claude_researcher`'s claude.ai runtime. Listed here so the agent doesn't search for them.

- `use-worktree`, `clean-worktrees` — local-filesystem-only; no parallel to git worktrees in claude.ai sandbox.
- `webapp-testing`, `building-ui-ux` — out of scope for v1 (no webapp frontend in research workflow).
- `using-screenshots` — claude.ai handles images natively in chat.
- `finishing-a-development-branch` — the research-line analogue is `finishing-a-research-branch`; there's no separate development-branch flow in this template.
- `updating-noridocs` — Nori-specific; no Nori on the web side.
- `maintaining-decision-docs` — out of scope for v1 research repos.

---

## How skills are added

When a new skill is ported (Phase 6 work), add an entry above with the same three fields. Keep the lifecycle grouping. Skills can be removed by moving them to "Skills intentionally not ported" with a rationale.

**Exported skills are build artifacts.** The skills listed in `template/skills/.export_manifest.json` are copied here automatically from the dotfiles `researcher` skillset (`export_profile_skills.py` in that repo) and overwritten on every export — never edit those `SKILL.md` files in this repo; edit the source in dotfiles `nori-researcher/skills/<name>/` and let the export land. To bring another skill under the export: add its `### <name>` entry here **first** (the exporter refuses a skill with no entry), then add the name to the exporter's whitelist. `pytest tools/` is the pre-PR check for this repo — `tools/test_skill_manifest.py` fails on a hand-edited export or a skill dir with no entry here.
