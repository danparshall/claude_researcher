# claude_researcher — Audit follow-up reconciliation + Plan 05 stub

**Date:** 2026-05-12 (with carryover into 2026-05-13)
**Repo:** claude_researcher (dev repo)
**Branch:** main
**Surface:** claude-code (CLI)
**Plan:** [`docs/plans/05_aitaxbid_followups.md`](../plans/05_aitaxbid_followups.md) created this session as a stub for next-session WebUI work.

## Summary

This session spanned the audit follow-up question ("how much of the 2026-05-09 AITaxBID audit has actually landed on main?") plus several adjacent threads: a HUMANS.md addition explaining where instructions to Claude live, a README opening-paragraph tightening, the deprecation of `template/README.md`, a Nori `commit-author` hook bug found and fixed upstream + locally + via dotfiles note, and a Plan 05 stub scaffolding the open AITaxBID-derived work.

Substantive output: one new plan doc (Plan 05), three Markdown edits committed to main (HUMANS section, README opening + grammar fix, template/README.md deletion), two GH issues filed on this repo (env-indicator-in-convo-names, W3.1 retrofit), one GH issue filed upstream (Nori hook bug `tilework-tech/nori-skillsets#496`), one in-place patch to the installed Nori hook, and one dotfiles note describing how to re-apply the fix on Dan's desktop. The aitaxbid-skills-audit branch remains untouched on disk and on origin; an untracked `template/README.md` in the main worktree was left alone per multi-terminal protocol.

The reconciliation portion produced a clean Done-vs-Open map for the 2026-05-09 audit's three tiers: most Tier B (CLAUDE.md/RESEARCHER.md patterns) has landed; all Tier A (skill ports) is still open; Tier C (per-skill block format) is still open as an architectural decision. The two Tier A items in Plan 02's Wave 4 (`writing-skill`, `branch-document-review`) are the immediate next-session work, with the W3.1 fold-in retrofit as a side track.

## Work Done

### Documentation edits to main

- **HUMANS.md**: added "Where instructions to Claude live" section (commit `a535723`) explaining the surfaces where info gets stored — `~/.claude/CLAUDE.md`, per-repo CLAUDE.md, claude.ai Settings "Personal preferences," Project Instructions, upstream `RESEARCHER.md` (read from local clone), and `personal_info.md` in basic_config. Frames `personal_info.md` as the canonical home for user prefs and gives examples of in-conversation update phrasing.
- **README.md**: tightened opening paragraph (commit `f3a00c3`) — added a goal/accessibility sentence ("unlock the full power of Agentic-based research, even for a researcher with no special knowledge of git or AI"), then dropped a redundant "approach" via follow-up fix (`37f77c4`).
- **`template/README.md`**: deleted (commit `f3a00c3`). It was kept as a "future-state Phase 10 promotion target" but had drifted (still referenced `CLAUDE.md` after the rename to `RESEARCHER.md`). Phase 10 will require a README pass anyway; using the root README as the base then is simpler than maintaining two.

### Nori hook bug

- Identified `commit-author.js` PreToolUse hook mangling single-line `git commit -m "msg"` invocations into commit messages with literal `\n\n` characters around the appended Nori footer. Heredoc-style commits were unaffected.
- Root-caused to line 30 of `build/src/cli/features/claude-code/hooks/config/commit-author.js`: `\\n\\n` in a JS template literal produces the literal two-character string `\n\n`, which bash inside `"..."` does not interpret as newlines.
- Filed upstream: [`tilework-tech/nori-skillsets#496`](https://github.com/tilework-tech/nori-skillsets/issues/496) with reproduction, root cause, suggested one-character fix, and explanation of why the heredoc path works.
- Patched locally: changed `\\n\\n` → `\n\n` on line 30 of the installed `commit-author.js`. Verification: parallel-agent dotfiles commit `1009852` came through with proper multi-line formatting, confirming the fix is live.
- Wrote `notes_nori_commit_author_fix.md` in `~/code/dotfiles/` (committed by parallel agent as `1009852`) describing the patch location, before/after diff, when to re-apply (npm update, version bumps), and verification steps.

### Audit follow-up reconciliation

Mapped the 2026-05-09 audit's findings against current main (`37f77c4`):

- **Tier B (CLAUDE.md/RESEARCHER.md patterns) — DONE except light-vs-heavy.** Show-before-committing, tracker-not-past-chats, 3+-repetition codification, Parking Lot, "Don't infer — ask," and interview-discipline batching all landed on RESEARCHER.md / BOOTSTRAP.md. Light-vs-heavy is contingent on porting a reviewer skill (i.e., lands naturally with W4.3).
- **Tier A (skill ports) — ALL OPEN.** None of `writing_skill.md`, `BranchWorkflow_Skill.md`, `paper_processing.md` synthesis, or `document_processing.md` has been ported. The Wave 3 ship of `add-paper` *did not include* the W3.1 AITaxBID synthesis (Step 0 triage + Protocol B summary structure for institutional reports) — grep against `template/skills/add-paper/SKILL.md` for the relevant terms returned nothing.
- **Tier C (per-skill block format) — OPEN.** No occurrences of Andrea's `> **Generic skill:** ...` block pattern in RESEARCHER.md or any SKILL.md. Architectural question deferred to next session.

### `template/README.md` mystery — characterized, not resolved

An untracked `template/README.md` (mtime 2026-05-12 06:23) appeared in the main worktree despite being deleted in commit `f3a00c3`. Investigation:

- Working-tree file content is byte-identical to the `aitaxbid-skills-audit` branch's HEAD version.
- That branch is 1 commit ahead of *its* fork point but 14 commits behind current main. It still has `template/README.md` because it forked off before the deletion.
- The aitaxbid worktree itself (`.worktrees/aitaxbid-skills-audit/`) is currently clean.
- A parallel agent reported the same observation independently around the same time, with the same uncertainty about origin.

Best explanation: a session this morning operating with the aitaxbid branch's content (via `git show aitaxbid:template/README.md > ...` or `cp` from the worktree) restored the file into the main worktree, possibly for an audit or comparison, then didn't clean up. File was left alone per multi-terminal protocol.

### Plan 05 stub created

[`docs/plans/05_aitaxbid_followups.md`](../plans/05_aitaxbid_followups.md) (commit `04f6ec0`, 174 lines). Stub-only — tasks scaffolded but not detailed. Scaffolded tasks: W4.0 sandbox tooling pre-check, W4.1 `writing-skill` port, W4.2 diff-mechanism decision, W4.3 `branch-document-review` port, W3.1 retrofit (tracks issue #3), Tier C decision (4 options enumerated), W4.4 SKILL_INDEX update, W4.5 ship commit. Bakes in two principles: defer to Andrea on methodological details, and use Nori kebab-case naming convention.

## Decisions Made

- **Defer to Andrea on methodological details.** For skills that are hers or overlap strongly (Protocol B for institutional reports, `[bracketed comments]` convention, two-protocol writing structure, light-vs-heavy reviewer rule), defer to Andrea — she's been doing pure-GitHub web-UI work for years and her conventions are field-tested for exactly this audience. Adapt only where the architecture forces it (REST instead of local git; on-demand fetch instead of full-kit propagation). Written into Plan 05's "Principles" section.
- **Use Nori kebab-case naming convention for ported skills.** `writing-skill/SKILL.md`, `branch-document-review/SKILL.md`, etc. Rationale: claude_researcher will integrate more strongly with Nori going forward.
- **Tier C parameterization belongs in user research repos, not upstream.** Resolves the architectural question raised in Plan 05's Tier C task — `RESEARCHER.md` is upstream-shared so it can't carry per-project content, but a per-project parameterization file *can* live in each user's research repo. Rules out Plan 05's Option D (skip); narrows to Options B (new `PROJECT_PARAMS.md`) or C (extend STATUS.md). Final pick deferred to next session.
- **`template/README.md` deprecated** in favor of root README (dual maintenance had drifted; Phase 10 will require a README pass anyway).
- **Plan 05 is a stub** — task scaffolding only, fleshing out happens next session on the WebUI.

## Findings — process and self-awareness

- **Nori hook bug pattern is broader than this one instance.** Pre-existing commits `2208e69`, `f8b8e1b` (Phase 2 era) have the same literal-`\n\n` mangling. The bug has been latent in commit history for days. Workaround until upstream lands: always use the heredoc commit-message pattern.
- **Multi-terminal protocol works.** Two independent agents (this one + parallel) flagged the `template/README.md` mystery without either touching the file. Convergent caution is the right default when state can't be cleanly explained.
- **Main-sync at session start matters.** Missed at the top of this session; surfaced later as "local main is 14 commits behind origin" right when trying to push. The session protocol's `git fetch origin && git rev-parse main origin/main` step is load-bearing.
- **Confirmation of full Claude Code system prompt.** Self-introspection question from Dan ("was your system prompt the full Claude Code or just '.'?") answered: full Claude Code. Concrete markers: `You are Claude Code, Anthropic's official CLI for Claude` preamble, full tool framework, `# Environment` block (Platform: darwin, Shell: zsh, model "Opus 4.7 (1M context)"), `# Session-specific guidance`, `# auto memory` pointing at the memory dir. Useful evidence for the runtime-detection probe work (issue #2): in CLI, the system prompt itself is unambiguously CLI; the cleaner web/cli signal is presence-vs-absence of this scaffolding.
- **Context management guidance is minimal in the system prompt.** Just "write down important information from tool results in your response, since results may be cleared later" + the auto-compression note. The implication: mirror SHAs, line numbers, and decisions into prose, and rely on durable artifacts (commits, issues, plan docs, convo files) for resumption — same lesson as RESEARCHER.md §1.5's tracker-not-past-chats discipline.

## Bugs / Friction Surfaced

- **Nori `commit-author` hook mangles single-line `-m` commits.** Tracked upstream as `tilework-tech/nori-skillsets#496`. Local patch applied; dotfiles note written. Will need re-applying after npm update / version bumps until upstream lands.
- **W3.1 fold-in was dropped at Wave 3 ship.** Tracked as [`#3`](https://github.com/danparshall/claude_researcher/issues/3). `add-paper` ships without Step 0 academic-vs-institutional triage, without Protocol B summary structure, and without the schema extension for `paper_naming.academic_format` / `paper_naming.institutional_format`. Plan 05 includes W3.1 retrofit as a task.
- **`template/README.md` resurfacing in working tree.** Origin not fully explained; characterized in "Work Done" above. Leaving the untracked file alone for now; will resolve via merge or cherry-pick once Plan 05 lands.
- **Convo-name handshake missed at session start.** §2e specifies the handshake should happen in the first or second response; it didn't this session. Name (`20260512_audit_followup_and_plan05`) proposed at finish-convo time instead. Worth folding the handshake into the session-start checklist more visibly, or treating "no name yet by message 3" as a Hook condition.

## Open Questions (carry-forward)

- **Tier C placement** in user research repos: Option B (new `PROJECT_PARAMS.md`) vs Option C (extend STATUS.md role). Decision needed in WebUI session.
- **Andrea's AITaxBID kit may have evolved since 2026-05-09.** Re-check SHAs at next session start. If Andrea's `SkillPropagation` repo is accessible, prefer that as canonical source.
- **Sandbox tooling availability for W4.3** — Plan 04 may have addressed pandoc/LaTeX/python-docx; verify before W4.3 designs around regeneration step.
- **`aitaxbid-skills-audit` branch lifecycle.** After Plan 05 ships, should the branch be archived? The audit doc itself remains valuable as a reference; the branch is stale (14+ commits behind).
- **W3.1 retrofit timing** — fold into Plan 05 alongside Wave 4, or treat as separate ship?
- **Env-indicator-in-convo-names** ([issue #2](https://github.com/danparshall/claude_researcher/issues/2)) — three open questions on retroactive rename, axis granularity, and position confirmation. Tracked durably; not blocking.

## What's Next

- Next session: WebUI work on Plan 05 Wave 4 (W4.0 sandbox check → W4.1 writing-skill → W4.2 diff-decision → W4.3 branch-document-review → W4.4 SKILL_INDEX → W4.5 ship). W3.1 retrofit can interleave or follow.
- Re-check SHAs of Andrea's source files at session start; her kit may have evolved.
- Decide Tier C placement (Option B vs C) in WebUI session before any work depends on it.

## Provenance

- **Commits this session (claude_researcher repo):**
  - `a535723` — HUMANS.md: add "Where instructions to Claude live" section
  - `f3a00c3` — README: tighten opening + delete template/README.md
  - `37f77c4` — README: drop redundant "approach" for cleaner reading (rebased from `04da025`)
  - `04f6ec0` — plan 05: AITaxBID follow-ups stub
- **GH issues filed:**
  - `danparshall/claude_researcher#2` — Add environment indicator (web/cli) to convo names
  - `danparshall/claude_researcher#3` — Plan 02 W3.1: re-fold AITaxBID Step 0 + Protocol B into add-paper
  - `tilework-tech/nori-skillsets#496` — commit-author hook writes literal `\n\n` for single-line `-m` commits
- **Dotfiles changes (committed by parallel agent):**
  - `1009852` — Add `notes_nori_commit_author_fix.md`
  - `0326713` — Implement bash-loop / eval / find-delete deny rules (unrelated parallel work; surfaced in this session's git survey)
- **Local patch (not in any commit):**
  - `/opt/homebrew/lib/node_modules/nori-skillsets/build/src/cli/features/claude-code/hooks/config/commit-author.js` line 30: `\\n\\n` → `\n\n`
- **Working-tree state left untouched:**
  - `/Users/dan/code/claude_researcher/template/README.md` (untracked; resolution deferred)
