# 20260511 — Clone-First Ship (Plan 03) + Phase 4.6 Retrofit

**Session goal at start:** Execute Plan 03 — clone-first session start, `CLAUDE.md` → `RESEARCHER.md` rename, slim `_PROJECT_INSTRUCTIONS.md.template`, STATUS Known Issue for stale-raw-CDN. Phase 4.6 retrofit added mid-session and completed in the same chat.

**Outcomes:** All of Plan 03 plus all of Phase 4.6 shipped. Nine substantive commits on `main`. `template/CLAUDE.md` deleted; `template/RESEARCHER.md` lives at 462 lines with the new §1.5 (Resumption discipline), §5 Working conventions block (don't-infer-ask, show-before-committing, codify-after-third-repetition), and §8 (Parking Lot). `_PROJECT_INSTRUCTIONS.md.template` slimmed 55% (4375 → 1831 bytes). STATUS.md has the empirical 24+ hour stale-CDN entry.

## Three substantive findings worth recording

**1. The stale-CDN problem was confirmed in this very session, not just retrospectively.** The session-start agent WebFetched `template/CLAUDE.md` from `raw.githubusercontent.com` per the existing Custom Instructions and received a pre-`31bb358` version of the file — 390 lines, missing the convo-name handshake (§2e), the catch-up-source rule, and the artifact-graph section that yesterday's commit had shipped to `main` ~24 hours earlier. The Contents API returned the correct 390-line file with all three new sections. The user noticed the omission ("did you get a note to propose a convo name up-front?") and the agent verified the discrepancy. This is the same pathology Plan 03 documents in its Known Issue entry, observed live during Plan 03's own execution. Concrete number: at the time of observation, raw CDN was at least ~24 hours behind upstream `main`, not the "~5 minutes" the pre-Plan-03 CLAUDE.md appendix anticipated.

**2. No stub keeper for the old path.** Plan 03 specified deleting `template/CLAUDE.md` outright. The agent flagged that this would break existing Projects' Custom Instructions (which still hardcode the `template/CLAUDE.md` URL) and proposed three options: stub keeper, manual-update chore, or hybrid. User clarified: the project is `<48 hours old, alpha status, back-compat is not a strong requirement. Path chosen: outright delete, accept that existing Projects (this Project and `research-knowledge-base`) need their Custom Instructions manually re-pasted before next session.

**3. Resumption discipline placement.** Plan 01's task 26.6.1 said add the tracker-not-past-chats rule "as new §1.5 or top of §2." The 2026-05-11 dogfooding session had already shipped a partial version as the "Catch-up source" paragraph in §2e. Decision: lift to §1.5 as its own standalone section, collapse the §2e paragraph to a one-line backreference. Reason: §2e is positioned after fetches when the agent is about to respond — late enough that an agent already drifting toward `conversation_search` would not be deflected. Top-of-file placement reflects that the rule applies universally, not just during catch-up.

## Sequence of work

### Phase: Plan 03 Task 1 — RESEARCHER.md + reference sweep + delete

Wrote `template/RESEARCHER.md` (commit `915a094`) from the live Contents-API version of `CLAUDE.md` (sha `d2370dc`, 391 lines). Seven surgical edits applied in `/home/claude/RESEARCHER.md` before push:

- Rewrote opening paragraph to describe clone-first session start
- Updated "Two fetch mechanisms" → "Three fetch mechanisms" (clone primary, WebFetch fallback for upstream, sandbox curl for user repos)
- Added §2.0 with the clone command (`git clone --depth 1 https://github.com/danparshall/claude_researcher.git /home/claude/.claude_researcher_template`), shallow clone (no upstream history needed), freshness-model paragraph (session-start snapshot, optional `git pull` for mid-session refresh)
- §2d: SKILL_INDEX read changed from WebFetch to `view /home/claude/.claude_researcher_template/...`, WebFetch retained as fallback
- §5 Implementation: TDD skill read switched to local
- §5 Skills-on-demand: rewrote heading from "Skills are fetched on-demand" to "Skills are read on-demand"; primary path now local `view`, fallback WebFetch
- Appendix raw-CDN entry: replaced "~5 minutes" claim with "24+ hours" empirical observation; noted clone-first as the routing-around
- §7 issue-reporting: SHA capture rewritten to use `cd /home/claude/.claude_researcher_template && git rev-parse HEAD` (the cloned commit) as primary, Contents API as alt

Reference sweep across the non-historical files (commits `53cc57b` README, `4eb2f81` BOOTSTRAP, `cf16fb8` 01_initial_build, `2134492` 02_skill_ports):
- README: file-list bullet renamed, parenthetical about future rename dropped
- BOOTSTRAP: three surgical edits — line 440 (upstream pointer URL), line 528 (Step 9 expected-behavior description rewritten for clone-first), line 535 (troubleshooting entry rewritten, with empirical 24+ hour stale-CDN note)
- 01_initial_build: principled split — Phase 4 historical descriptions and tracker row left intact (accurate record of past phase); Phase 4.5 deferred references, Phase 4.6 retrofit task descriptions, Phase 6 task descriptions, and Open Questions updated to RESEARCHER.md. Section 4.6 intro rewritten to be explicit: *"committed `681ed9d` as `template/CLAUDE.md`, restructured through `42648a4`, and renamed to `template/RESEARCHER.md` by Plan 03"*
- 02_skill_ports: Phase 4.6 retrofit section title and prose updated; left Andrea-CLAUDE.md and Dan-global-CLAUDE.md references alone (different files)

Then deleted `template/CLAUDE.md` (commit `28c36f8`) — Task 1 complete.

### Phase: Plan 03 Task 2 — slim _PROJECT_INSTRUCTIONS.md.template

Rewrote from 82 lines to 37 lines (commit `b599058`). What survived: title, credentials block with `<TOKEN>`/`<USERNAME>`/`<REPO>` placeholders (so BOOTSTRAP's substitution mechanism stays simple), clone command, fallback WebFetch, "Ordering" rule from yesterday's `52abf78` (updated to RESEARCHER.md), and the "if anything looks inconsistent, surface the mismatch" closer. What was removed: the "Why this uses the GitHub REST API" preamble (contained the empirically-wrong claim about `git clone` not working in claude.ai's sandbox), the detailed REST recipes for read/write/list (live in RESEARCHER.md and skills now), the old "Where to start every session" pointer at `template/CLAUDE.md`.

### Phase: Plan 03 Task 3 — STATUS Known Issue

Appended one Known Issue bullet to `STATUS.md` (commit `0003d5e`) covering the 24+ hour raw-CDN staleness observation, calling out the dual evidence (SKILL_INDEX.md from 2026-05-10 plus CLAUDE.md observed this session), noting Plan 03's clone-first routes around it for the primary path while the fallback retains the exposure, and giving the workarounds (Contents API fallback URL, noop edit to force cache refresh, or just wait).

### Phase: Phase 4.6 retrofit (added mid-session)

User asked what was next on the todo list; the agent enumerated Phase 4.6 + verification + sandbox-tooling matrix + Wave 4 ports + beta session + deferred items, and recommended Phase 4.6 as highest-leverage (already partially shipped, context fresh from Plan 03, ~30-60 min). User approved continuation in the same session, with the option of a handoff if context was getting tight. Agent self-assessed as fine, proceeded.

Five universal rules added to RESEARCHER.md (commit `86dfeb3`):

- **§1.5 — Resumption discipline (new section)** — promotes the tracker-not-past-chats rule from §2e to a top-of-file universal. Operational rules: don't call `conversation_search`/`recent_chats` at session start, verify user recollections of past work against the trackers before responding, only fall back to chat-history search if the user explicitly asks for something not in the trackers. §2e's old "Catch-up source" paragraph collapsed to a one-line backreference.
- **§5 Working conventions block (new subsection)** — three rules:
  - *Don't infer — ask.* "A confident output based on wrong assumptions is worse than a quick clarifying question." Exception carved out for cases where stating the assumption inline and letting the user correct it is cheaper than a confirmation round-trip.
  - *Show before committing.* Every write gets at least a one-line narration before the tool call. The "Confirmation gates scripted in this file" section was updated with an intro line tying it to this universal — the scripted gates are now the emphatic cases, not the only cases.
  - *Codify after the third repetition.* Sharp threshold for promoting a repeated user request to a rule. Three escape valves: add to RESEARCHER.md (universal rule), STATUS.md (project-specific), or a skill (reusable workflow).
- **§8 Parking Lot (new section)** — home for open questions about RESEARCHER.md itself. Seeded with two entries: banner-vs-proper-REST adaptation for ported Researcher skills (resolved when first beta session exercises one), Phase 9 collaborator walkthrough (resolved when a real candidate is available).
- Top-of-file document-structure outline updated to include §1.5 and §8.

## Notable design decisions

- **Single commit for the retrofit** (per Plan 01 task 26.6.7's commit-message proposal) rather than per-rule commits. Trade-off: more diff to review in one go vs. cleaner history. The whole block is internally referential (the §5 Working conventions intro references the gates section it modifies, the §2e backreference depends on §1.5 existing) so a single commit is structurally honest.
- **§1.5 over top-of-§2.** §2 is the session-start fetch sequence; §1.5 sits as a pre-work rule alongside §1 (calibration). Conceptually cleaner: §1 + §1.5 are constraints the agent applies before any fetching happens; §2 is the fetching itself.
- **Working conventions positioned between Planning and Artifact graph** (not at top of §5 as a preamble). Reasoning: the three modes (research, implementation, planning) describe *what* the agent does in each mode; the working conventions describe *how* writes happen regardless of mode. Putting them after modes-of-work but before the artifact-handling specifics (graph, skills, gates) gives them the right scope.

## Manual follow-ups (Dan)

1. **Update Custom Instructions in both Projects.** This Project (`claude_researcher`) and `research-knowledge-base`. Source content: `https://api.github.com/repos/danparshall/claude_researcher/contents/template/_PROJECT_INSTRUCTIONS.md.template` (Contents API URL is reliable; the raw-CDN URL for the same path may itself be stale by 24+ hours, which is darkly funny but real). Substitute `<TOKEN>`, `<USERNAME>`, `<REPO>` with real values per Project. Without this, next session in either Project will 404 on the old CLAUDE.md path.
2. **Verification chat.** Open a fresh chat in `claude_researcher` after step 1; confirm the agent clones, reads RESEARCHER.md from local, fetches `personal_info.md` and `STATUS.md` via Contents API, and greets correctly. Plan 03 Task 1's verification plan.
3. **Update Plan 01's Phase 4.6 tracker row** from `📋 Spec'd` to `✅ Done` — small cleanup, separate from the retrofit commit itself. (Agent does this as a closeout commit, not waiting for user.)

## Commits on `main` (this session)

| SHA | Message |
|---|---|
| `915a094` | RESEARCHER.md: clone-first session start (Plan 03 Task 1, part 1/3) |
| `53cc57b` | README: rename CLAUDE.md to RESEARCHER.md, drop future-rename parenthetical (Plan 03) |
| `4eb2f81` | BOOTSTRAP: sweep CLAUDE.md to RESEARCHER.md; reflect clone-first session start (Plan 03) |
| `cf16fb8` | 01: sweep forward-looking CLAUDE.md refs to RESEARCHER.md (Plan 03) |
| `2134492` | 02: Phase 4.6 retrofit section — file target now RESEARCHER.md (Plan 03) |
| `28c36f8` | template/CLAUDE.md: delete (Plan 03 Task 1 complete) |
| `b599058` | _PROJECT_INSTRUCTIONS.md.template: slim (Plan 03 Task 2) |
| `0003d5e` | STATUS: Known Issue entry for 24+ hour stale CDN (Plan 03 Task 3) |
| `86dfeb3` | Phase 4.6: RESEARCHER.md retrofit — universalize tracker discipline, codification, parking lot, do-not-infer, show-before-committing |

## What's next (carried forward)

Highest priority for next session: **#2 verification chat** above. **#3 Plan 01 tracker update** happens at session wrap (this convo). After those: sandbox tooling matrix (Wave 4 prerequisite), then Wave 4 AITaxBID Tier A ports (`writing-skill` first, ~1 hour). Wave 0 provenance infra remains deferred. Phase 4.5 collaborator mode and Phase 9 walkthrough wait for a real candidate.
