# claude_researcher — Plan 11: Clone-first banner sweep (issue #27 follow-through)

**Written:** 2026-06-09, claude.ai web session (`lobby_analysis` Project, cross-repo per Dan's go-ahead).
**Executes:** fresh session per Nori flow (plan-then-fresh-session).
**Branch:** `clone-first-banner-sweep` (this plan lands on it; execution continues it; PR at the end).
**Tracks:** [issue #27](https://github.com/danparshall/claude_researcher/issues/27) (partial — the skill-sweep slice) + `RESEARCHER.md` §8 Parking Lot entry "Banner vs. proper-REST adaptation for ported Researcher skills" (2026-05-11 → 2026-06-08).

## Why now

PR #28 (merged 2026-06-09, commit `4f56936` → merge `3b89447`) shipped the §2.0b clone-first
runtime: the project repo is cloned at session start and native git is the supported write path.
The skill kit was NOT swept in that PR (deliberately — separable diff, tracked in the Parking
Lot). Result: **the runtime spec and the skill kit currently contradict each other.** Eleven
skills carry a "Runtime detection" banner whose claude.ai branch instructs the agent to
*translate `git add`/`commit`/`push` into Contents API recipes* — i.e., to translate away the
exact commands §2.0b tells it to run. A fresh agent that trusts the banner regresses to
one-PUT-per-file; one that notices the contradiction stalls or guesses. Empirically confirmed
live in the 2026-06-09 web session that wrote this plan: `finish-convo`'s banner, read alongside
the post-#28 RESEARCHER.md, gives opposite instructions for the same write.

This plan fixes **wrong** instructions only. It does not optimize functional-but-suboptimal
ones (see D3), and it does not decide gh adoption (see D2). Scope discipline keeps the diff
reviewable and keeps #27's real design knobs from being snuck in.

## Inventory (verified against `23fe45a`, 2026-06-09)

Banner carriers — `grep -l "translate every" template/skills/*/SKILL.md` — 11 files in two
variants:

**Group A — git-verbs-only banner (8):** `add-paper`, `audit-docs`, `audit-papers`,
`finish-convo`, `init-research-repo`, `paper-processing-academic`,
`paper-processing-institutional`, `update-docs`.

**Group B — git-verbs + gh-verbs banner (3):** `task-create`, `task-remind`, `task-triage`.
Per STATUS 2026-06-04, each has a *calibrated* verb list (task-create widest; task-remind drops
`gh issue create` + `gh search issues`; task-triage read-only). The calibration must survive
the rewrite.

**Explicit non-targets:**

- `receiving-code-review` — matches the Parking Lot's broader `git add\|git commit\|...` grep
  but carries **no banner** (zero hits on "Runtime detection"/"translate"); its git verbs are
  body content that is now correct to run directly. No edit.
- `branch-document-review` — no banner; inline REST recipes (refs create, Compare API, merges
  API) that still **work**. Deferred per D3.
- `iterative-writing-workflow` + the 9 Wave-1 SWE carryovers — no git/filesystem surface or no
  banner. No edit.

Pin exposure: `grep` of `README.md` + `template/BOOTSTRAP.md` for SHA-pinned
`raw.githubusercontent` URLs shows **none reference `template/skills/`** — no
`tools/repin.py` run required. Re-verify at execution **by grep, not by `repin.py --dry-run`**:
per [#18](https://github.com/danparshall/claude_researcher/issues/18) that flag is silently
ignored and the script commits for real.

## Decisions recommended at plan-writing (Dan to ratify before execution)

- **D1 — Banner rewrite, not banner removal.** The runtime-detection probe block (the
  `$IS_SANDBOX` / `$CLAUDECODE` bash) is still correct and still load-bearing for Claude Code
  sessions reading the same file from dotfiles-synced paths. Only the **"If `claude.ai
  sandbox`"** paragraph and one stale clause in the **"If `unknown`"** paragraph change.
  Canonical replacement text in Task 1.1.
- **D2 — Group B keeps REST for gh verbs.** Shipped §2.0b explicitly keeps Pulls + Issues on
  REST ("PR creation/merge … uses the Pulls API", "task-remind's issue queries … use the Issues
  API"). The gh-CLI adoption proposed in #27 (verified installable, real upside) is a separate
  decision with its own knobs (install timing, token hygiene via `GH_TOKEN`) — it stays on #27
  and is **not** decided here. The Group B rewrite therefore says: git verbs → run directly;
  gh verbs → still translate to the Issues-API endpoints. If gh adoption later ships, Group B
  gets a second one-line touch; that's acceptable churn for keeping this diff
  contradiction-only.
- **D3 — `branch-document-review` deferred.** Its REST recipes are functional, and the local-git
  equivalents are behavior changes worth their own verification (e.g., Compare API → `git diff
  $BASE_SHA...$BRANCH` removes the 300-file cap but changes failure modes; merge-via-API vs
  local merge+push differ under branch protection). File a follow-up issue at execution time
  ("branch-document-review: prefer local-git equivalents under §2.0b clone") rather than
  folding it in.
- **D4 — SKILL_INDEX status block + manifest contract updated.** The top-of-file status block's
  "the agent translates Claude-Code idioms … into claude.ai-equivalents (REST `write_update` /
  `write_new` recipes …)" paragraph is the manifest-level statement of the wrong instruction;
  rewrite per Task 2. The "Manifest contract" section's **URL** bullet gains the local-clone
  path as primary (one sentence; the 18 per-entry URLs stay as stated fallbacks — no churn).
- **D5 — Parking Lot entry resolved, not just edited.** Per §8's own conventions, the resolved
  item is **deleted** from RESEARCHER.md and its resolution recorded here (this plan) + in the
  ship commit message. The companion appendix already carries the "Resolved 2026-06-08" note
  for the Git-Data-API limitation; no further RESEARCHER.md edits needed.
- **D6 — #27 narrowed, not closed.** After ship, comment on #27: skill sweep done (link
  commit), remaining scope = gh adoption decision + commit-shaping/push-recovery/verification
  conventions if Dan still wants them formalized beyond what §2.0b shipped.
- **D7 — dotfiles twins NOT touched by this plan.** The dotfiles copies of `task-*` (and the
  Nori-side `AGENTS.md`) describe Claude Code runtime, where nothing changed. The banner being
  rewritten exists only in the `template/skills/` ports (it's the claude.ai branch of the
  probe). One-way provenance pins (`nori_researcher_source: …@8b619b5`) are unaffected because
  the banner sits **outside** the pinned body (inserted between frontmatter and body at
  port time — same surface the original banners landed on). Verify at execution that each edit
  touches only the banner region, never the pinned body (Task 3 check 4).

## Phase 1 — Banner rewrite

### Task 1.1 — Group A (8 files)

In each file's `## Runtime detection` section, replace the **"If `claude.ai sandbox`:"**
paragraph with:

> **If `claude.ai sandbox`:** the user's project repo is already cloned at
> `/home/claude/<REPO>/` per `RESEARCHER.md` §2.0b — run the `git add` / `git commit` /
> `git push` commands in this skill directly from that working tree. Translate local skill
> paths like `/Users/<user>/.claude/skills/...` to the template clone at
> `/home/claude/.claude_researcher_template/template/skills/...`. Only if the §2.0b clone
> failed (degraded REST fallback, surfaced to the user) do you translate `git add` /
> `git commit` / `git push` into the Contents API recipes from your Project Instructions.

And in the **"If `unknown`:"** paragraph, replace the stale parenthetical
`(running \`git push\` in a sandbox with no git, or writing REST calls against a local working tree)`
with `(operating against the wrong working tree, or using the wrong write path for the
environment)`. The sandbox has git; the old rationale is from the pre-clone architecture.

Exact-match note for execution: the 8 banners were stamped from one pattern but verify with
`git diff` per file; any drift (e.g., add-paper's wider verb list, if present) gets the same
semantic edit, hand-adjusted.

### Task 1.2 — Group B (3 files)

Same two edits as Task 1.1, **plus** retain (do not delete) each file's gh-verb translation
sentence, re-anchored so it can't be misread as covering git verbs. Canonical form (verb list
stays per-skill-calibrated — copy each file's existing list verbatim):

> The `gh` verbs in this skill (<existing per-skill list>) still translate to the GitHub REST
> endpoints from your Project Instructions (`GET/POST/PATCH /repos/{owner}/{repo}/issues`,
> `GET /search/issues`, `GET /user`) — Issues and Pulls remain REST surfaces per
> `RESEARCHER.md` §2.0b. (gh-CLI adoption is tracked separately in upstream issue #27.)

### Task 1.3 — Single commit for Phase 1

One commit, all 11 files: `skills: rewrite claude.ai runtime banners for §2.0b clone-first
(issue #27 sweep)`. Body names Groups A/B and the two non-targets with the reason each is
untouched.

## Phase 2 — Manifest + Parking Lot

### Task 2.1 — `template/skills/SKILL_INDEX.md`

Status block: rewrite the runtime-translation paragraph to state the §2.0b reality — git verbs
run directly against `/home/claude/<REPO>/`; gh/issue verbs translate to the Issues API; the
REST Contents-API recipes are the documented degraded fallback. Manifest contract: extend the
**URL** bullet with "Primary read path is the local template clone
(`/home/claude/.claude_researcher_template/template/skills/<name>/SKILL.md`); the URL is the
WebFetch fallback when the §2.0a clone is absent."

### Task 2.2 — `template/RESEARCHER.md` §8

Delete the "Banner vs. proper-REST adaptation" Parking Lot item (resolution: this plan +
Phase 1 commit). Leave the Phase-9 collaborator item untouched.

### Task 2.3 — Commit

`SKILL_INDEX + RESEARCHER §8: manifest text matches clone-first runtime; resolve Parking Lot
banner item`.

## Phase 3 — Verification + ship

### Task 3.1 — Verification script (Python, `/tmp/plan11_verify.py`)

1. Zero hits: `grep -rn "into the REST \`write_update\`" template/skills/` (old primary-path
   phrase gone everywhere).
2. 11 hits exactly: banners referencing `§2.0b` in `template/skills/*/SKILL.md`; assert the
   file set equals Groups A+B (catches both a missed file and an accidental edit to a
   non-target).
3. Zero hits for "Runtime detection" in `receiving-code-review` and `branch-document-review`
   (non-targets stayed untouched), and `iterative-writing-workflow` unchanged
   (`git diff --stat` empty for it).
4. Provenance safety: for each Group A/B file, `git diff` touches only the region between the
   frontmatter close and the first body heading (the banner), never below it.
5. Parking Lot: `grep -c "Banner vs. proper-REST" template/RESEARCHER.md` == 0.
6. Pin exposure re-check by grep (NOT `repin.py --dry-run`, per #18): no SHA-pinned URL in
   README/BOOTSTRAP references an edited file.

### Task 3.2 — Ship

PR from `clone-first-banner-sweep` via the docs-branch sub-flow (skip TLP/SWE steps; run
`nori-code-reviewer`; inline PR body). Real merge commit not strictly required (no SHA-pins
reference this branch) but harmless if conventions prefer it. Post-merge: D6 comment on #27;
file the D3 follow-up issue for `branch-document-review`.

## Open questions for Dan (ratify or override at kickoff)

- **Q1:** D2 — confirm gh adoption stays out of scope (banner says "REST per §2.0b" for gh
  verbs), or fold gh-CLI in now and accept the bigger diff + the install-timing/token-hygiene
  knobs landing in this plan.
- **Q2:** D3 — confirm `branch-document-review` defers to a follow-up issue.
- **Q3:** Estimated execution: ~45-60 min (11 mechanical edits with hand verification, 2 doc
  edits, verify script, PR). If that estimate is wrong at kickoff, say so before starting.
