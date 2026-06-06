# Add-paper first-use prompt (use-time half of #12)

**Date:** 2026-06-06
**Branch:** `add-paper-first-use-prompt`

## Summary

Started as a "what's outstanding?" check that walked through `task-remind` (no fired reminders — none of the 5 open `task`-labeled issues carry a `[YYYY-MM-DD]` prefix) and reconciled a contradiction in STATUS: the 2026-06-05 convo described PR #20 as "ready-to-merge" but `gh pr list --state open` was empty. Resolved via `gh pr list --state all`: PR #20 had actually merged at `9517ac2`, local main was 4 commits behind, the `bootstrap-egress-reminder` branch was a leftover. Re-fetched + recomputed: no real outstanding work-in-flight, only the backlog issues.

Picked off #12 ("add-paper: ask naming convention on first save (drop from bootstrap)"). Spent the bulk of the session on a three-part recall investigation prompted by Dan's intuition that "the change is in dotfiles": all three pieces of recall turned out misaligned with current state. (a) "The canonical source is in dotfiles": `~/code/dotfiles/nori-researcher/skills/add-paper/SKILL.md` is the pre-synthesis Wave 3 Nori baseline (single commit `91c93ac`, 128 lines, no `paper_naming` schema), while `template/skills/add-paper/SKILL.md` is the Plan 06/07 synthesized dispatcher (101 lines, Step 0 triage routing to per-protocol skills). Template is *ahead* of dotfiles for this skill — inverted from the documented pull-from-dotfiles pattern. (b) "install.sh creates a link in this repo": `install.sh` symlinks `~/code/dotfiles/nori-researcher/skills/<X>/SKILL.md` → `~/.nori/profiles/researcher/skills/<X>/SKILL.md` and (in a separate block) → `~/.claude/skills/<X>/SKILL.md`. Neither line writes into the `claude_researcher` repo. The repo's drift-prevention mechanism for skill bodies is the `nori_researcher_source: ...@<SHA>` provenance pin in frontmatter — a one-way pull, not a symlink. (c) "There's an open sync issue": `danparshall/dotfiles#20` exists, but scoped to `AGENTS.md` (CLI persona) vs `RESEARCHER.md` (Web persona) drift, with examples that are persona-instruction edits and a proposed fix that's an audit script diffing those two files. Skill-body drift via provenance-pin is not enumerated in #20; the third drift surface (install.sh `RESEARCHER_SKILLS` array vs renamed targets) was flagged in STATUS 2026-06-04 Phase 6.1 but not formally tracked.

On Dan's "more colleague sync" call, deferred all three drift questions (back-porting the synthesis to dotfiles, expanding #20 scope, or declaring template canonical for add-paper) and shipped only the use-time prompt for #12. Discovered en route that #12's first half ("drop from bootstrap") had already shipped silently in PR #16 (Plan 08 / onboarding-ux-cleanup): `BOOTSTRAP.md` §4 Batch 3 currently asks four questions (Git fluency, Mode, Home repo, Extra paper-source domains), no paper-naming; `personal_info.md.template` no longer carries the `<PAPER_NAMING_ACADEMIC>` / `<PAPER_NAMING_INSTITUTIONAL>` placeholders Plan 06 had added. So the remaining work was strictly the use-time half. Implementation: two parallel one-line edits in `paper-processing-academic/SKILL.md` and `paper-processing-institutional/SKILL.md`, each replacing the existing `If paper_naming.<key> is unset, fall back to the default above.` with a `**First-use prompt.**` block that shows the default plus one example, asks accept-or-override, and persists the chosen value as `- **Paper naming (academic|institutional):** <value>` under "Operating preferences" in `personal_info.md`. Only the protocol that fired gets asked. Committed as `b92d12e` on a fresh branch `add-paper-first-use-prompt` (cut from updated `main` at `9517ac2`); pushed to origin.

## Topics Explored

- `task-remind` session-start check + reconciling PR #20's open-or-merged state via `gh pr list --state all`
- Diff between dotfiles `nori-researcher/skills/add-paper/SKILL.md` and template `template/skills/add-paper/SKILL.md` (architectural delta: dispatcher vs monolithic procedure)
- Drift-mechanism inventory across three surfaces: persona instructions (AGENTS.md/RESEARCHER.md), skill bodies (dotfiles → template via provenance pin), and install.sh wiring
- `dotfiles#20` issue body — scope and stated fix candidates
- Where the `paper_naming` keys are actually read (per-protocol skills' "Filename convention" paragraph at Step 1) and where they're declared to live (Scope section's "Where config keys live" pointing at `personal_info.md` "Operating preferences")
- Whether to put the first-use prompt in the dispatcher (Step 0.5 before Dispatch) or in each per-protocol skill (Step 1). Picked per-protocol on locality grounds: read-and-use is co-located in each skill's Step 1, dispatcher should stay thin

## Provisional Findings

- For the `add-paper` family specifically, template is *ahead* of dotfiles (Plan 06/07 synthesis was done in `claude_researcher` and never back-ported to dotfiles). If the documented "pull from dotfiles by SHA" pattern were ever invoked here, the synthesis would be lost. This is the inverse of the bug the provenance-pin pattern is supposed to prevent.
- `dotfiles#20`'s scope (AGENTS.md vs RESEARCHER.md persona) is narrower than the full drift surface. Skill-body drift and install-script drift are adjacent but separate; a generic "sync mechanism" framing risks conflating three independent gaps.
- Issue #12 was partially executed silently — when the originating onboarding-UX work (Plan 08) shipped "drop paper-naming from bootstrap", neither the issue nor the bootstrap-side commit referenced #12, so the issue still read as fully open. The use-time half remained genuinely unbuilt.

## Decisions Made

- **Defer the dotfiles/template sync question** for `add-paper` (and skill bodies generally). The three options enumerated mid-session — (1) treat template as canonical for `add-paper`, (2) back-port synthesis to dotfiles, (3) expand #20 to cover skill-body drift — all require colleague-level coordination Dan flagged as not-yet-ready. None blocked the immediate #12 use-time fix.
- **Implement #12's use-time prompt in the per-protocol skills**, not in the dispatcher. Locality: the format value is needed exactly where it's applied (Step 1 filename construction).
- **Persist as a markdown-header line** (`- **Paper naming (academic):** <value>`) under "Operating preferences" in `personal_info.md`, matching the existing `Git fluency` / `Mode` / `Home repo` pattern. (The skill-body prose uses dotted-key names like `paper_naming.academic_format` as advisory pointers; the actual schema is header-by-name.)
- **Don't reintroduce placeholders in `personal_info.md.template`.** Plan 08 removed them when dropping the bootstrap question; the first-use prompt now appends the field at use time. Keeps the template footprint minimal.

## Results

No data/figures produced this session; the deliverable is the two-file SKILL.md edit committed at `b92d12e`.

## Open Questions

- The dotfiles/template skill-body sync question (3 deferred options above). Worth a dedicated convo when ready.
- Whether `dotfiles#20` should be expanded in scope or whether a separate "skill-body drift" issue is cleaner. Lean toward the latter — different surfaces, different mechanisms.
- The third drift surface (install.sh `RESEARCHER_SKILLS` array) flagged in STATUS 2026-06-04 Phase 6.1 is still untracked. Consider whether to file as its own issue.
- PR for `add-paper-first-use-prompt` not yet created — small enough to merge directly when Dan's ready; no reviewer pass needed for a one-line behavior swap, but `nori-code-reviewer` could still surface something.
- Untracked `template/scripts/resolve_append_conflict.py` left alone per multi-terminal protocol — another session's WIP.

## Process notes

- Convo-name handshake (§2e) was missed at session start; convo named at finish-convo time as `add_paper_first_use_prompt` to match the branch.
- Dan's three pieces of misrecall about the dotfiles/template relationship were all defensible — each described a mechanism that *does* exist somewhere in the system, just not the one in play for `add-paper`. The investigation produced clean answers because the actual mechanisms are documented (provenance pins in frontmatter, install.sh source paths, STATUS Phase 6.1 note); future sessions wanting to navigate this should grep for `nori_researcher_source:` and read `install.sh`'s symlink blocks directly.
- TaskCreate harness reminder fired four times this session; ignored every time. Each piece of work (lookup, investigation, two-file edit, commit/push) was self-contained and well-tracked by the conversation itself; harness tasks would have added overhead without surfacing.

## Post-finish-convo: reviewer pass + PR

After `finish-convo` (commits `b92d12e` skill change + `5ac4b02` convo/STATUS), ran `finishing-a-development-branch` with the docs-branch heuristic from STATUS 2026-06-05: skipped `/simplify`, `/code-simplifier`, tests / lint / format / typecheck, webapp demo, and the `pr-review-guide` skill spawn (drafted PR body inline given small scope); ran `nori-code-reviewer` as the load-bearing step.

### Reviewer findings addressed (commit `9f9d006`)

- **M1 — runtime-detection block too narrow.** The block at lines 8-28 of each per-protocol skill enumerated only git verbs for sandbox REST translation, not arbitrary file writes — but the new persist call needs REST translation in sandbox too. Fix: generalize line 24 from "translate every `git add` / `git commit` / `git push` in this skill" to "translate every `git add` / `git commit` / `git push` and any other file write in this skill". Reviewer offered two options: (a) generalize the block, (b) narrow parenthetical at the persist site. Picked (a) on aging grounds — any future skill-body addition with a file write inherits the translation. Applied only to the two files in this PR's diff; other skills carrying the same block don't currently have non-git file writes to translate. If they get one, that's their PR.
- **M2 — persist mechanic under-specified.** Original wording "Persist as `- **Paper naming (X):** <value>` under 'Operating preferences'" left append-vs-update semantics and field ordering ambiguous. Fix: "appended after the last existing `- **...:**` line in 'Operating preferences'; if the line already exists (race with a concurrent edit), leave it as-is." Race-safe, explicit ordering. Two agents in two runtimes can't invent different conventions.
- **L1 — "first paper" over-claims user intent.** Operationally harmless (the prompt still fires correctly) but a downstream agent reasoning about user intent might over-trust the inference. Fix: "this is the user's first academic paper" → "treat this as a first-use case." Operationally identical, doesn't claim what's behind the absent field (counter-examples: deleted line, fresh checkout).

### Reviewer findings dismissed

- **LOW — em-dash + "(Enter to accept the default.)" parenthetical.** Reviewer noted "press Enter" might not literally apply in all sandbox harnesses. Agents reading skills generalize "press Enter" as "answer affirmatively" — not worth changing.
- **LOW — STATUS entry duplicates convo prose.** Reviewer noted some repos lean toward tight STATUS summaries; the bullet here is ~1100 words. **Kept dense intentionally** — this repo's existing 2026-06-04 / 2026-06-05 entries follow the same pattern (full file paths, commit SHAs, process findings inline). The STATUS "Recent sessions" section is the primary fresh-session lookup surface; density is a feature, not a bug.

### PR description additions per reviewer INFO

- **Dotfiles asymmetry** flagged in PR #22's Risk Highlights — "If the documented 'pull from dotfiles by SHA' pattern were ever invoked here, the synthesis would be lost — that's a known asymmetry, not introduced by this PR."
- **Sandbox-runtime resolution mechanism** flagged in PR #22's Risk Highlights — explicit call-out that commit `9f9d006`'s M1 fix is what makes the new persist call REST-translatable.

### PR state + procedural decisions

- **PR #22** created OPEN, MERGEABLE, mergeStateStatus CLEAN. No CI configured for this repo (matches PR #19 / #20 pattern). https://github.com/danparshall/claude_researcher/pull/22
- **Skipped step 14 of `finishing-a-development-branch`** (auto-`/loop` polling every 5 min for unresolved review threads). Dan's call: small docs PR he's about to review himself; the loop would auto-respond to his review comments as they land, which isn't the workflow here. The /loop pattern is designed for SWE PRs with reviewer back-and-forth, not single-author docs touch-ups.
- **Skipped `pr-review-guide` skill spawn** (step 9 of `finishing-a-development-branch`). For a 3-commit, two-file, markdown-only docs PR, the guide would have been brief and the inline draft covered the same ground (summary / risk highlights / suggested review path / test plan / reviewer notes).

### Process findings (additions)

- The `chain-hook-maintenance` block-on-`\n#`-in-heredoc fired during PR creation: the initial `gh pr create --body "$(cat <<'EOF' ... EOF)"` form contained `\n## Summary` headers which tripped the matcher. Routed around via Write-then-run (body to `/tmp/pr_body_add_paper_first_use.md`, then `gh pr create --body-file <path>`). This is the documented pattern; worked first try. Worth noting as another concrete instance for the chain-matcher curator's corpus.
- The docs-branch heuristic ("skip TLP/SWE steps, run `nori-code-reviewer`") held up well a second time. PR #19, PR #20, now PR #22 — three consecutive applications. Codified-enough to deserve promotion from the 2026-06-05 STATUS process-finding to either RESEARCHER.md or `finishing-a-development-branch`'s own SKILL.md as an explicit docs-branch sub-flow. Not done in this PR (scope), but worth filing.
