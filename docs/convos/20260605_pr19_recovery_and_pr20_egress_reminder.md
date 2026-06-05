# 20260605 — PR #19 crashed-session recovery + PR #20 bootstrap egress-revisit reminder ship

**Date:** 2026-06-05
**Branch:** bootstrap-egress-reminder (also touched: task-skills via PR #19 fix + merge; dotfiles main via parallel sync)
**Surface:** Claude Code (CLI)

## Summary

Two-act session. **Act 1 — recovery from a crashed session that had run `nori-code-reviewer` on PR #19 (Plan 09 / task-skills)**: the previous session died mid-verification of a "genuine bug" finding the reviewer had surfaced; today's session forensically located the crashed session's transcript at `.claude/projects/-Users-dan-code-claude-researcher/6dd742d4-….jsonl` line 712-713, recovered the full reviewer punch list, verified the critical finding (`home_repo` schema mismatch between `personal_info.md.template`'s seeded `- **Home repo:** <HOME_REPO>` format and the skills' grep instruction for snake_case `home_repo: <owner>/<repo>`) against current code, applied fixes to both `claude_researcher/template/skills/{task-create,task-remind}/SKILL.md` AND `dotfiles/nori-researcher/skills/{task-create,task-remind}/SKILL.md` (the symlink target the local CLI reads from), plus the two Important findings (RESEARCHER.md §2b field enumeration missing `Home repo`; `task-triage/SKILL.md:84,157` stale "Plan 09 Decision 6" citations), then merged PR #19 with a real merge commit (`5bb6da6`) preserving repin SHA-pin reachability per the standing convention.

**Act 2 — operationalized issue #13's narrower remaining scope**: the BOOTSTRAP §1b allow-all-egress branch's promise *"After bootstrap I can set up a reminder for you to revisit this setting in a week"* had no actual implementation; PR #19's `task-create`/`task-remind`/`task-triage` skills provide the surfacing mechanism but didn't include the bootstrap-side consumer. Branch `bootstrap-egress-reminder`: §1b language tightened to concrete *"I'll file a reminder issue"* (commit `8b89056`); Step 10 grew a new `### Egress-revisit reminder (first-time bootstrap only)` sub-step before the closing message that probes home_repo existence, dedupes against existing open reminders, ensures the `task` label exists, POSTs an issue with `[<today+7>] Revisit claude.ai network egress setting` title + `task` label + explanatory body, and captures `html_url` via response parse. Ran `nori-code-reviewer` again — surfaced 4 substantive findings (C1 JSON parse crash on non-JSON response; C2 silent 404 if HOME_REPO doesn't exist; S1+S2 mismatched user prompt vs agent instruction on "unsure"; S3 missing dedupe) plus several nits. Commit `5cc47bd` addressed all four; the bash recipe `bash -n` syntax check passes. S4 (label color divergence between bootstrap's `#0052CC` and `task-create`'s unspecified color) deferred as out-of-scope → issue #21.

This is the second session in a row where `nori-code-reviewer` found a real correctness bug before merge. The recovery from the crashed session vindicated the discipline of running the reviewer on docs-only branches — the standing finish-development-branch checklist mostly N/A for skill markdown (no tests, lint, typecheck, CI), but the reviewer step is where the value is. Recommend: future finish-development-branch invocations on docs branches should explicitly skip /simplify and /code-simplifier (TLP-specific) but ALWAYS run nori-code-reviewer.

## Topics Explored

### Crashed-session forensics

The session-start `git status` snapshot showed PR #19 open with no CI checks reported. User said: *"the last message I saw was 'The reviewer found a genuine bug!' and then the session crashed."* — strong signal that a reviewer subagent had run but the findings never got actioned.

Approach: grep `~/.claude/projects/-Users-dan-code-claude-researcher/*.jsonl` for "genuine bug" — only matches in the current session (user's own message) and an unrelated May 13 session. So either (a) the crashed session didn't persist that exact phrase verbatim, or (b) the crash happened in a session whose jsonl was modified at a different time than I expected.

Pivot: search broader for `simplif|nori-code-reviewer|code-simplifier` keywords plus session-mtime ordering. Found `6dd742d4-….jsonl` had a `nori-code-reviewer` Agent invocation at line 712 (timestamp `2026-06-04T22:25:24Z`) and the response at line 713 ("Good, no stale references. Both mentions are intentional...") followed by the full code-review punch list. Last lines of that session: a Read of RESEARCHER.md offset 168 and a grep of "Plan 09" in task-triage SKILL.md — verification work in progress when the session died.

The recovered punch list:
- **Critical:** `home_repo` schema mismatch.
- **Important:** §2b field enumeration omits Home repo; task-triage cites Plan 09 Decision 6 twice (plans don't ship with skill bundle, so WebFetch-based agents can't resolve the citation).
- **Nits 4-9:** Banner verb-list discipline clean; SKILL_INDEX entries correct; §2d.5 placement fine; §0 fifth trait clean; home_repo location split correct; minor `<gh-user>` literal-placeholder concern in task-create:76.

### PR #19 fix application

Critical fix direction debate: align skills to template (read `Home repo:` field by header name, matching sibling fields `Git fluency`/`Mode`) vs align template to skills (seed `home_repo: <owner>/<repo>` as snake_case key). Reviewer recommended the first option (lower blast radius); Dan agreed. Important fixes applied without further discussion.

Critical observation during the dotfiles sync prompt: `~/.claude/skills/{task-create,task-remind}/SKILL.md` are real symlinks pointing directly at `~/code/dotfiles/nori-researcher/skills/...` (NOT at `claude_researcher/template/skills/`), so a claude_researcher-only fix leaves the local CLI surface broken. User confirmed parallel fix. Dotfiles had a lot of unrelated WIP (`chain-hook-maintenance` work, `nori.json`, several test files, `update_claude_permissions.py`); targeted `git add <file>` discipline kept that uncommitted work out of the bug-fix commit. Pattern matches the Plan 09 Phase 6 session's same multi-terminal discipline.

PR #19 merged with `gh pr merge 19 --merge` (real merge commit, not squash/rebase) per PR body's explicit instruction about preserving the repin commits' SHA-pin reachability — same standing convention as PRs #8, #10, #16.

### Issue #13 narrowing

Three options surfaced — close + comment, close + file follow-up, leave open with narrowed scope. Dan picked **leave open with narrowed scope**: comment that the mechanism shipped via a different backend (GH Issues with `[YYYY-MM-DD]` prefix instead of `basic_config/reminders.md` markdown file), narrow the title to `BOOTSTRAP §1b: auto-file egress-revisit task-remind reminder on allow-all egress branch`. Both edits landed (rename via `gh issue edit`, comment via `gh issue comment`).

### PR #20 design

The mechanical question was *where* in BOOTSTRAP the reminder gets filed, given that §1b sometimes hands off to a fresh chat (§1c restart) where the "user picked allow-all" signal is lost. Options considered:
- (a) Persist the choice through the restart somehow — rejected; no clean mechanism.
- (b) Auto-file in §1b — rejected; PAT + home_repo aren't available yet.
- (c) File at the end of bootstrap (Step 10) and ASK the user post-hoc if needed — picked.

The §1b language got tightened to *"If you go with allow-all, after bootstrap I'll file a reminder issue..."* (sets the expectation; conditional on allow-all). Step 10 grew the sub-step that handles the conditional: in-this-chat config → agent knows; cross-chat config → ask once.

Repo placement: HOME_REPO, not specifically `claude_research_config`. Rationale: `task-remind` queries current-research-repo + home_repo at session-start; the reminder MUST land in home_repo to surface. Users who customize home_repo to something else (e.g., `dentist-reminders`) get the reminder routed there. The default home_repo (`<USERNAME>/claude_research_config`) preserves the original #13 intent.

### Second nori-code-reviewer pass — findings + dispositions

Reviewer ran against `bootstrap-egress-reminder` HEAD and produced 4 substantive findings + 5 nits + 4 holistic confirmations. Critical findings:

- **C1 (JSON parse crash):** `json.load(sys.stdin).get('html_url', fallback)` protects against a missing key in a valid dict, but raises `JSONDecodeError` if curl returns non-JSON (transient 5xx, HTML error page from an edge proxy, empty body). Crash at the absolute worst point in bootstrap. Wrapped both response parses (dedupe check + html_url extraction) in try/except.
- **C2 (silent 404 on missing HOME_REPO):** Step 4 Batch 3's home_repo question doesn't validate the repo exists; user could name `<gh-user>/not-yet-created` and the label/issue POSTs would 404 silently. Added a `curl -s -o /dev/null -w "%{http_code}"` probe at the top of the bash block; non-200 → skip the rest with explanatory note.
- **S1 (mismatched user prompt vs agent instruction on "unsure"):** Original prompt offered only two answers ("allow everything" or "domain allow-list"); agent instruction silently defaulted unsure → file. Fixed by updating the prompt to *"or you're not sure"* and tightening the agent instruction to file only on confirmed allow-all. Matches §1b's promise.
- **S2 (§1b ↔ Step 10 promise gap):** §1b said "if you go with allow-all"; Step 10 was broader (allow-all OR unsure). Resolved alongside S1 by tightening Step 10.
- **S3 (missing dedupe):** Verbal "first-time bootstrap" gate is observational, not programmatic; a returning-user path that re-runs full bootstrap (e.g., for a second research repo) would file a second reminder. Added a programmatic backstop: GET open `task`-labeled issues from HOME_REPO, skip if any matches the "Revisit claude.ai network egress" title.

Deferred: **S4 (label color divergence)** — bootstrap creates `task` label with `--color 0052CC`; `task-create/SKILL.md` Step 3 creates it without a color flag. First-creator-wins means visible color varies repo-by-repo. Reviewer suggested adding `--color 0052CC` to `task-create` for the canonical invariant. Filed as issue #21 because the fix would also touch dotfiles (parallel port) and is a different concern from the bootstrap-side consumer.

Nits skipped as defensible: N1 (BODY left exported), N2 (theoretical shell injection in python `-c`), N3 (BSD-then-GNU date portability — BOOTSTRAP only runs in Linux sandbox), N4 (`set -o pipefail`), N5 (`<ISSUE_URL>` placeholder convention).

Holistic confirmations from the reviewer: home_repo placement is right; `[YYYY-MM-DD]` title prefix matches task-remind's regex; `task` label is the entire filter signal; the reminder surfacing depends on the user running another session within ~a week.

Validation: extracted the embedded bash block via Python regex, ran `bash -n` against it (with `<HOME_REPO>` → `owner/repo` stub for syntactic validity). Exit 0 — well-formed.

## Provisional Findings

- **Crashed-session jsonl recovery is feasible from the `.claude/projects/` directory.** Each session's full transcript including Agent subagent invocations is persisted as line-delimited JSON; recovery is just `grep` + targeted line reads. Worth flagging that the jsonl mtime doesn't always match the last-content-timestamp (cf2 session's mtime was 21:09 local but last content was 20:39 UTC) — the file gets touched on session close, possibly explaining the mismatch.
- **`nori-code-reviewer` produced real value on both of the last two PRs.** PR #19 had a critical correctness bug (home_repo parser); PR #20 had a critical runtime crash bug + a silent-failure bug + a UX inconsistency + a dedupe miss. The pattern is: even for skill-markdown branches that don't have a traditional test suite, the reviewer's "what would actually go wrong at runtime" analysis catches things review-by-author misses.
- **The `finish-development-branch` skill checklist isn't well-fit to docs-only branches** — most steps (tests/lint/format/typecheck/CI/loop) are no-ops, but the reviewer step is the load-bearing one. Suggests either (a) a docs-branch variant of the skill, or (b) the skill's existing wording could be tightened to flag which steps are load-bearing on docs work specifically.

## Decisions Made

- **Fix #19's home_repo parser by aligning skills to template, not template to skills.** Skills read the `Home repo:` field by header name (matching `Git fluency`/`Mode` pattern). Lower blast radius than re-shaping the template.
- **Sync the fix to dotfiles in the same go.** Local CLI symlinks point at dotfiles, not via claude_researcher. Skipping dotfiles would leave the local CLI surface broken.
- **Issue #13 stays open with narrowed scope** (BOOTSTRAP §1b auto-seeding), not closed. The mechanism shipped via a different backend than #13's original spec; the bootstrap-side consumer is the remaining work.
- **Egress reminder lands in HOME_REPO**, not specifically `claude_research_config`. Required for `task-remind` surfacing to find it.
- **§1b promise is conditional on confirmed allow-all only.** Step 10 tightened to match — unsure users get a hand-off to file via `task-create` themselves.
- **S4 deferred to a follow-up issue (#21).** Touches `task-create` in another scope.

## Results

No standalone results files this session. The deliverables are:
- Bug fix commits: `5870ce3` (claude_researcher PR #19) + `60fd8e6` (dotfiles parallel sync).
- PR #19 merge commit: [`5bb6da6`](https://github.com/danparshall/claude_researcher/commit/5bb6da6).
- Bootstrap egress-reminder commits: [`8b89056`](https://github.com/danparshall/claude_researcher/commit/8b89056) (initial Step 10 sub-step) + [`5cc47bd`](https://github.com/danparshall/claude_researcher/commit/5cc47bd) (reviewer-driven hardening).
- PR #20 (open, MERGEABLE, CLEAN): https://github.com/danparshall/claude_researcher/pull/20
- Issue #13: narrowed title + operationalization comment.
- Issue #21 filed for S4 label-color follow-up.

## Open Questions

- **Should the `finish-development-branch` skill get a docs-branch variant?** Most steps are N/A for skill-markdown branches; the nori-code-reviewer step is the load-bearing one. A trimmed skill (or an early branch in the existing one) would reduce friction.
- **Should there be a programmatic test for the BOOTSTRAP bash recipes?** Currently the verification surface is `bash -n` syntax check (this session) + human reading. A `tools/check_bootstrap_recipes.py` that extracts the bash blocks and `bash -n`s each one would catch regressions; could also do `python3 -c "..."` syntax checks on the embedded python snippets.
- **The `<HOME_REPO>` doesn't-exist edge case (C2 in this session) is a latent issue in Step 4 Batch 3** — the question asks for `owner/repo` without validating. Worth a separate hardening pass eventually: probe the repo right after the user answers, surface if it 404s. Not urgent — the C2 fix here means the egress-reminder sub-step is robust to it, but other code paths in bootstrap (Step 7 seeding) probably aren't.
