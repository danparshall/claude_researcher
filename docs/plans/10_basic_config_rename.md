# claude_researcher — Plan 10: Rename `basic_config` → `claude_research_config`

**Goal:** Rename the default personal-config repo in the template from `basic_config` to `claude_research_config` across all live-code surfaces, so new users meeting the bootstrap have an obviously-named repo. Sweep all 33 references in 7 live-code files; leave historical convo + plan files untouched (timestamped record). Close issue [#14](https://github.com/danparshall/claude_researcher/issues/14) on merge.

**Status:** Ready for execution. Decision was locked in the 2026-06-04 task-skills design session; this plan is purely mechanical text substitution + SHA-pin discipline + STATUS update.

**Originating convo:** [`20260604_task_skills_design.md`](../convos/20260604_task_skills_design.md). The "Decisions Made → Home repo name" entry locked the new name as `claude_research_config` (not `dotfiles` — that name may collide with users' actual dotfiles repos and shouldn't be conscripted). The motivating need surfaced two days earlier in [`20260603_onboarding_ux_think_aloud.md`](../convos/20260603_onboarding_ux_think_aloud.md), where `basic_config` was implicitly flagged as opaque to a first-time user, but the explicit rename decision lives in the 2026-06-04 convo.

**Related prior work:**
- Issue [#14](https://github.com/danparshall/claude_researcher/issues/14) is the tracking issue; this plan operationalizes it.
- Plan 08 (`onboarding-ux-cleanup`, PR #16, merged 2026-06-04 as `ddf5410`) shipped while #14 was still open — its BOOTSTRAP/README/HUMANS edits used `basic_config`. This plan is the cleanup pass.
- Plan 09 (`task-skills`, written 2026-06-04 on its own branch) has a Phase 0 precondition that depends on this plan shipping first. Plan 09 will be unblocked when this PR merges. Plan 09's text already writes `claude_research_config` throughout — no re-sweep of Plan 09 needed after this plan ships.
- Issue [#13](https://github.com/danparshall/claude_researcher/issues/13) (session-start reminders) operationally lands in Plan 09's `task-remind`; not affected by this rename directly.

**Confidence:** High. Decision is settled, name is locked, surface area is small and bounded (mechanical grep + replace). One small open question about Dan's *real* existing repo on GitHub (Section "Open question" below) — answered out-of-band, doesn't gate this plan.

**Branch:** `basic-config-rename` (worktree at `.worktrees/basic-config-rename/`).

**Tracking issue:** [#14](https://github.com/danparshall/claude_researcher/issues/14).

**Tech stack:** Markdown text edits across `template/` and root-level docs; one re-run of `tools/repin.py` if SHA-pinned URLs in `template/BOOTSTRAP.md` or `README.md` change.

---

## Coupling concerns resolved at design time (do NOT re-open)

- **Historical docs are not swept.** All `docs/convos/*.md` and `docs/plans/01..08*.md` references to `basic_config` stay verbatim — they're timestamped historical record, and rewriting them retroactively claims the name was always `claude_research_config` (it wasn't). `docs/plans/09_task_skills.md` also stays as-is: its references mention `basic_config` only in the *context* of the rename itself (Phase 0 precondition, "see issue #14") and those phrasings remain accurate after this plan ships. Verification (Phase 3.1) explicitly grep-excludes `docs/convos/` and `docs/plans/0[1-8]_*.md`.
- **Dan's existing `<gh-user>/basic_config` repo on GitHub is out of scope.** This plan renames the *template's default* name. Dan's actual repo (the one created by his own bootstrap) is named `basic_config` today and stays named `basic_config` unless Dan renames it on GitHub side. The runtime fallback in Plan 09's `task-remind` reads `home_repo` from `personal_info.md` — Dan can set it to whatever his real repo is named regardless of the template default. See Open Question 1.
- **No skill files are affected.** `grep -rln basic_config template/skills/` returns empty as of branch creation. The rename does not touch any `template/skills/*/SKILL.md`. Confirmed; no need to re-verify during execution unless someone has added a new skill that references the config-repo name between plan write and execution.
- **SHA-pin discipline applies.** `README.md` line 25 has the bootstrap-entry URL pinned to a specific commit (`2dec9af` at time of writing); `template/BOOTSTRAP.md` has three in-flow template URLs pinned to `87f84ea`/successor. Any edit to `README.md` or `template/BOOTSTRAP.md` requires running `tools/repin.py` before merge to bump those pins — same as Plan 08's `4fbc745` / `2e9c11d` pair. This is the Plan 10 step that's NOT mechanical text replacement.
- **`_PROJECT_INSTRUCTIONS.md.template`'s placeholder semantics.** Line 13 references `<USERNAME>/basic_config` literally (not as a placeholder) — it's documenting what the PAT scope should target. Rename this to `<USERNAME>/claude_research_config`. The `<USERNAME>` / `<TOKEN>` / `<REPO>` placeholders themselves stay; we're only renaming the literal trailing component.

## Decisions confirmed at design time (do NOT re-litigate)

- **New name: `claude_research_config`.** Locked in the 2026-06-04 task-skills design convo. Not `dotfiles` (collides with users' real dotfiles repos); not `research_config` (drops the "claude" anchor that makes the purpose obvious from the repo list); not `personal_config` (less specific to the workflow). The chosen name is descriptive and unlikely to collide.
- **Sweep scope is live-code only.** Identified surface area at plan-write time: 33 references across 7 files (`template/BOOTSTRAP.md` 18, `STATUS.md` 6, `template/RESEARCHER.md` 5, plus 1 each in `template/_PROJECT_INSTRUCTIONS.md.template`, `template/ATTRIBUTION.md`, `README.md`, `HUMANS.md`). The verification grep in Phase 3.1 is the authoritative completeness check at execution time — counts may drift slightly if other branches merge first.
- **Substitution is case-sensitive, literal `basic_config` → `claude_research_config`.** No `BASIC_CONFIG` or `BasicConfig` variants exist (verified via `grep -ri 'basic[_-]config' template/ docs/plans/0[1-9]*.md README.md HUMANS.md STATUS.md`). If a variant appears at execution time, surface to Dan rather than silently handle.
- **Ship as a single commit + PR.** This is a mechanical, low-risk change with bounded surface area — no point splitting into multi-commit phases. One commit (or two if the SHA-pin bump is needed, paralleling Plan 08's pattern).

---

## Phase 1 — Mechanical sweep

### Task 1.1 — Update `template/BOOTSTRAP.md` (18 references)

**File:** `template/BOOTSTRAP.md`.

**Reference inventory** (line numbers as of plan-write time, will drift if other edits land first — use the grep result at execution time as authoritative):

```bash
grep -n 'basic_config' template/BOOTSTRAP.md
```

Lines roughly at 116 (glossary), 194 (Step 3 header), 196, 203 (curl URL), 208, 213 (returning-user message), 221, 308 (confirmation prompt), 323 (`<DESC>` value), 338, 379 (section header), 392 (README skeleton), 462 (RESEARCHER.md cross-link), 484 (verification expected-files list), 528 (PAT-rotation guidance), 550 (Step 9 expected runtime behavior), 570 (returning-user re-bootstrap path), 583 (troubleshooting).

**Steps:**

1. Read the file once to confirm it's roughly the expected shape (the 18-count and rough line positions match).
2. Do the substitution: every literal `basic_config` → `claude_research_config`. Use Edit with `replace_all: true` — there are no false positives (no `basic_config` substrings inside larger identifiers; verified at plan write).
3. Spot-check the changes around lines 116 (the glossary repo example), 308 (the user-facing confirmation prompt), 392 (the README skeleton seeded into the new repo), and 484 (the verification expected-files note) — these are the places where the rename is most user-visible.
4. Don't commit yet; the SHA-pin bump in Phase 2 may want to bundle.

**Don't:** rewrite surrounding prose to "improve" it during the sweep. Mechanical-only. Anything beyond literal substitution gets a follow-up issue, not a Plan 10 commit.

### Task 1.2 — Update `template/RESEARCHER.md` (5 references)

**File:** `template/RESEARCHER.md`.

**Reference inventory:**

```bash
grep -n 'basic_config' template/RESEARCHER.md
```

Approximately lines 25 (user-owned repos description), 168 (§2b header), 170, 176 (curl URL), 182 (404 handling).

**Steps:**

1. Edit with `replace_all: true`. Same logic as Task 1.1 — no false positives.
2. Spot-check §2b (the entire section is about fetching `personal_info.md` from the repo; the rename should read naturally throughout).

### Task 1.3 — Update single-reference files

Four files with one reference each. One Edit call per file:

- `template/_PROJECT_INSTRUCTIONS.md.template` (line 13) — PAT scope description.
- `template/ATTRIBUTION.md` (line 9) — "Downstream" enumeration.
- `README.md` (line 33) — interview-output description in the bootstrap prompt block.
- `HUMANS.md` (line 56) — "Where instructions to Claude live" section's `personal_info.md` mention.

**Steps:** four Edit calls, each substituting `basic_config` → `claude_research_config`. No surrounding prose changes.

### Task 1.4 — Update `STATUS.md` (6 references)

**File:** `STATUS.md`.

**Reference inventory:** look at branch summary line, Recent Sessions entries, possibly Open Questions section. Use:

```bash
grep -n 'basic_config' STATUS.md
```

**Subtle judgment call:** Recent Sessions entries are partly historical (they describe sessions that happened when the repo was named `basic_config`). If a Recent Session entry literally describes filing issue #13 with `basic_config/reminders.md` as the proposed location, that line is historical record and can stay — OR it can be updated with a parenthetical "(later renamed to `claude_research_config`)". Recommendation: do the literal substitution everywhere in STATUS.md, since STATUS is the *current state* document and the rename has shipped by the time anyone reads the post-merge STATUS. Past-tense convo entries with substituted name read as "we did X with the (now-renamed) repo" which is accurate.

**Override only if** a Recent Sessions entry has a quoted exact-string ("`basic_config/reminders.md`" inside backticks within prose describing a past decision). Quoted strings are usually verbatim historical references and should keep `basic_config`. Use judgment per occurrence; default to substitution.

**Steps:**

1. `grep -n 'basic_config' STATUS.md` to enumerate.
2. For each match, decide substitute-or-preserve per the rule above.
3. Apply edits.

### Task 1.5 — Single ship commit (or two if SHA-pin bump needed)

After Tasks 1.1-1.4, the working tree should have edits across 7 files. Diff-check before commit:

```bash
git diff --stat
```

Expected: 7 files changed (the 6 from 1.1-1.4 plus STATUS.md). If a file unexpectedly appears or doesn't, investigate.

Commit (heredoc form per Nori commit-author hook convention):

```bash
git add template/BOOTSTRAP.md template/RESEARCHER.md template/_PROJECT_INSTRUCTIONS.md.template \
        template/ATTRIBUTION.md README.md HUMANS.md STATUS.md
git commit -m "$(cat <<'EOF'
rename: basic_config → claude_research_config across templates and runtime (#14)
EOF
)"
```

**Don't:** push yet. The SHA-pin step in Phase 2 may add a second commit that bundles into the same PR.

---

## Phase 2 — SHA-pin bump (conditional)

### Task 2.1 — Decide if `tools/repin.py` needs to run

Phase 1's edits touched `README.md` (one ref) and `template/BOOTSTRAP.md` (18 refs). Both contain SHA-pinned `raw.githubusercontent.com` URLs. The pin-bump pattern from Plan 08 (commits `4fbc745` + `2e9c11d`) applies here.

```bash
python3 tools/repin.py --dry-run 2>&1 | head -20
```

If the dry-run output shows pending rewrites → run without `--dry-run`. The script makes two commits by necessity (a commit can't embed its own SHA; same constraint Plan 08 / 03 / repin-tooling all hit).

If the dry-run output shows no rewrites (the script considers the current README/BOOTSTRAP URLs already up to date), skip Phase 2.

### Task 2.2 — Verify the bumped pins resolve

After the two repin commits land, sanity check that the SHA-pinned URLs in `README.md` line 25 and `template/BOOTSTRAP.md`'s three template URLs all resolve via `curl -I`:

```bash
# Extract pinned URLs
grep -oE 'https://raw.githubusercontent.com/[^ )]+' README.md template/BOOTSTRAP.md | sort -u
# For each, curl -I and confirm 200
```

If any returns 404, the pin points at a commit that hasn't propagated yet (GH raw CDN is consistent within seconds for pushed commits, but the bumped commits aren't pushed yet at this point). Wait, retry, push, retry — or push first, then verify. Either order works; pushing first is simpler.

---

## Phase 3 — Verification + ship

### Task 3.1 — Verification grep

```bash
# Should return ZERO hits in live-code surface area
grep -rn 'basic_config' template/ README.md HUMANS.md STATUS.md tools/

# Should return ONLY historical / context references in plans + convos:
grep -rn 'basic_config' docs/
# Expected hits: docs/convos/*.md (historical record), docs/plans/01..09 (shipped plans + the
# Phase 0 precondition in Plan 09 + this Plan 10's own references). Confirm each surviving hit
# is *about* the rename or is timestamped historical record. Surface any unexpected live-code
# hit to Dan.

# Should return positive hits everywhere `basic_config` used to be:
grep -rn 'claude_research_config' template/ README.md HUMANS.md STATUS.md tools/
# Expected: ~33 hits (matching the pre-rename basic_config count).
```

Any check failing → investigate before pushing.

### Task 3.2 — Optional smoke: re-read user-visible blocks

Read these three blocks in `template/BOOTSTRAP.md` end-to-end to confirm the substitution reads naturally:

1. The glossary at §2a (line ~116 pre-rename).
2. The Step 6 confirmation prompt (line ~308 pre-rename).
3. The README skeleton seeded into the new repo (line ~392 pre-rename).

If any of these reads awkwardly (e.g., `claude_research_config` repeated too many times in close proximity such that a pronoun reduction would help), surface to Dan but don't auto-rewrite in this plan. Polish is a follow-up.

### Task 3.3 — Push, open PR, close #14

```bash
git push -u origin basic-config-rename
gh pr create --title "Rename basic_config → claude_research_config (#14)" \
             --body "$(cat <<'EOF'
## Summary
- Renames the default personal-config repo in the template from `basic_config` to `claude_research_config` so the purpose is obvious to new users at first contact.
- Sweeps 33 references across 7 live-code files (BOOTSTRAP.md, RESEARCHER.md, _PROJECT_INSTRUCTIONS.md.template, ATTRIBUTION.md, README.md, HUMANS.md, STATUS.md).
- Historical convos and shipped plans (01-09) left untouched as timestamped record.
- `tools/repin.py` re-run included if README/BOOTSTRAP SHA-pins required bumping.

## Test plan
- [ ] Verification grep returns 0 hits in live-code surfaces
- [ ] Verification grep on `claude_research_config` returns ~33 hits (matching pre-rename count)
- [ ] SHA-pinned URLs in README + BOOTSTRAP resolve via `curl -I`
- [ ] User-visible BOOTSTRAP blocks (glossary, confirmation prompt, README skeleton) read naturally

Closes #14.
EOF
)"
```

The `Closes #14` line auto-closes the issue on merge.

**Don't:** force-merge. Wait for Dan to review and merge.

---

## Open question

**Should Dan's existing `<gh-user>/basic_config` GitHub repo also be renamed?**

This plan only renames the *template's default*. The pre-existing `<gh-user>/basic_config` repo Dan created via his own bootstrap is unaffected on GitHub side.

Options:

1. **Leave it.** Dan's existing repo stays at `basic_config`. After Plan 09 ships, Dan sets `home_repo: <gh-user>/basic_config` in his `personal_info.md` (overriding the new template default of `<gh-user>/claude_research_config`). Forward compatibility intact; backward compatibility intact; no GitHub-side action needed.
2. **Rename via GH.** Dan renames the repo on github.com (Settings → Rename). GitHub auto-creates a redirect from the old URL for ~all-time. Dan then either edits his `personal_info.md` to the new name (or accepts the redirect). Slightly cleaner long-term identity; minimal real benefit.

Recommendation: option 1 unless Dan has a reason to renormalize. This is independent of Plan 10 shipping — Dan can flip whenever.

This plan does **not** include automation to rename the actual GitHub repo. The bootstrap creates `basic_config` (or, post-merge, `claude_research_config`) per the template default; existing users' real repos are theirs.

---

## Testing Plan

This is a mechanical text-substitution plan with no behavioral code. There is no automated test to write — the verification posture is purely grep-shaped.

I will run the Phase 3.1 verification grep as the structural audit — it confirms zero `basic_config` survives in live-code surfaces and roughly 33 `claude_research_config` references appear (matching the pre-rename count).

I will optionally smoke-read the three user-visible BOOTSTRAP blocks (Phase 3.2) for prose readability after the substitution.

I will NOT write any new test files. The Plan 08 / Plan 03 pattern for content-shaped renames is verification-by-grep, not test-by-pytest. This plan inherits that pattern.

NOTE: I will write *all* tests before I add any implementation behavior. (Strictly: the "test" here is the Phase 3.1 grep — write the verification script before doing Phase 1's substitutions, so the GREEN-after-RED discipline is honored even on a mechanical task.)

---

**Testing Details:** The Phase 3.1 verification is two grep calls plus a curl-I check on SHA-pinned URLs. The first grep confirms absence of the old name in live code; the second confirms presence of the new name with the expected count; the third confirms pinned URLs resolve. None of these are pytest-runnable — they're shell checks, run manually or scripted into a one-shot bash snippet. No mocks, no fixtures, no test framework. The behavior under test is *file contents* and *URL liveness*, both verifiable by direct inspection.

**Implementation Details:**
- 7 files touched: 4 in `template/`, 3 at root.
- 33 substitutions total (counts as of plan-write time; may drift if other branches merge first).
- One ship commit, or two if `tools/repin.py` bump is needed.
- Heredoc commit messages throughout (Nori commit-author hook bug).
- `Closes #14` in PR body auto-closes the tracking issue on merge.
- No skill files affected (verified at plan-write; re-verify at execution).
- No changes to `tools/repin.py` itself — just re-running it.
- The rename does NOT propagate to Dan's actual `<gh-user>/basic_config` repo on GitHub; that's a separate Dan-level decision (Open Question above).

**What could change:**
- **Surface count drift.** If `task-skills` (Plan 09) execution or another branch merges before this plan ships and touches one of the 7 files (`STATUS.md` most likely, since branch summaries get updated frequently), the reference count shifts. The verification grep at Phase 3.1 is the authoritative completeness check; trust it over the 33-count.
- **Edge case in `_PROJECT_INSTRUCTIONS.md.template`.** If a user has already substituted the template into their Project Instructions text (claude.ai web), the substitution lives in their claude.ai Project, not in this repo. Existing users' Project Instructions are not auto-updated by this plan; the next time they re-bootstrap (a fresh chat following the bootstrap prompt) they'll get the renamed template content.
- **Casing conventions in future skill names.** This plan asserts no `BASIC_CONFIG` / `BasicConfig` variants exist. Future code that case-converts could re-introduce one; revisit if a grep months from now surfaces a variant.

**Questions:**

1. **Does Dan want to also rename his real `<gh-user>/basic_config` repo on GitHub?** See Open Question above. Doesn't gate Plan 10; just a related Dan-action.
2. **Should the verification grep be checked in as a script** (e.g., `tools/verify_rename.sh`) for future similar plans, or run ad-hoc? Recommendation: ad-hoc for this one — it's grep, scripting it adds maintenance burden — but flag for consideration if this is the third mechanical rename and the pattern is recurring.
3. **STATUS.md historical Recent Sessions entries** — confirm the recommendation in Task 1.4 (default to substitution, override only on quoted-string historical references). Worth a sanity check at execution time, especially on the long-form entries describing the Plan 08 / task-skills sessions which mention `basic_config` in the context of decisions made about it.

---
