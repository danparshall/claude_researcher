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

After the continuation section below: **Plan 04** is the queued work — see [`docs/plans/04_sandbox_tooling_and_companion_cleanups.md`](../plans/04_sandbox_tooling_and_companion_cleanups.md). It absorbs the original "sandbox tooling matrix" item plus three new cleanups surfaced in this session's continuation. The fresh-chat verification of clone-first remains pending (Plan 03's own verification plan covers it; no separate plan needed). Wave 4 (AITaxBID Tier A ports) kicks off after Plan 04 Task 1 lands. Wave 0 provenance infra remains deferred. Phase 4.5 collaborator mode and Phase 9 walkthrough wait for a real candidate (both now tracked in RESEARCHER.md §8 Parking Lot).

---

## Continuation — post-ship discussion and Plan 04

After the wrap-up artifacts shipped (convo file, STATUS, Plan 01 tracker), the user asked two questions: (a) "what's the next phase to work on?" and (b) "did you do finish-convo?" — and a third smaller one along the way that turned out to be more substantive than either.

### Procedural correction — finish-convo was improvised, not run

The agent had written the convo file, updated STATUS recent-sessions, and updated Plan 01's tracker row — but had not actually `view`'d `template/skills/finish-convo/SKILL.md` or `update-docs/SKILL.md` before doing so. The user flagged this with the note that the announcement matters for scrollback affordance (so the user can scroll back and see "I'm running finish-convo" and know full state was checked in). Honest answer surfaced: skill was bypassed, artifacts shipped are structurally equivalent to what the skill prescribes (convo file, STATUS entry, no PR/merge/conclusions-rewrite), but procedural compliance was zero. The fix going forward is simply to `view` the skill at wrap time and announce — which is exactly what the show-before-committing rule shipped in Phase 4.6's §5 Working conventions block now requires for *every* write, not just sensitive ones. The procedural slip happened in the same session that universalized the rule that would have prevented it; recording the irony here so the next session takes the show-before-committing rule seriously from turn one.

A small side-finding worth noting: `update-docs/SKILL.md`'s `<required>` block directs the agent to use `TodoWrite`. That tool exists in Claude Code, not in claude.ai. This is exactly the kind of cross-surface gap that the REST-adaptation banner (Wave 2/3, parked in §8) is supposed to cover, but the banner only addresses git-command translation, not arbitrary tool name translations. Plan 04 doesn't take this on; surfacing here so it's findable when the banner-vs-proper-REST empirical question gets evidence.

### Terminology correction — "Custom Instructions" → "Project Instructions"

The user noted that the Anthropic UI fields are called **"Project Instructions"** (project-level) and **"Instructions for Claude"** (user-level). The project's docs (RESEARCHER.md, BOOTSTRAP.md, parts of 01_initial_build.md, HUMANS.md, this very convo file's earlier text) have been calling the project-level field "Custom Instructions" — wrong term, propagated. The slim `_PROJECT_INSTRUCTIONS.md.template` shipped earlier today happens not to say "Custom Instructions" anywhere (luck, not design). To answer the user's practical question: copying just the Project Instructions content into that field is sufficient — credentials are project-scoped, they don't belong in user-level "Instructions for Claude" anyway. The sweep itself is Plan 04 Task 2.

### Surface attribution gap — 2026-05-10 was Claude Code

The user asked whether `20260510_skill_ports_initial_ship.md` was from a Claude Code session, since no matching chat appeared in his WebUI list. Confirmed: yes — the convo body has 5 references to `~/.claude/skills/<name>/SKILL.md` paths, which is Dan's local Mac filesystem (the claude.ai sandbox can't see that path). Structural evidence is decisive; the convo file is unambiguously a Claude Code artifact. This is consistent with STATUS's note that the 2026-05-11 dogfooding session was *the* pivot from Code-primary to WebUI-primary use.

Worth-noting structural observation: convo files currently don't record which surface they were written from. Distinguishing Code vs. WebUI convos has two non-trivial downstream uses: (1) the banner-vs-proper-REST empirical question in §8 Parking Lot wants honest evidence about REST-translation success rates, which requires being able to tell convos apart by surface; (2) HUMANS.md's multi-surface framing has actual data behind it rather than just narrative. Solution is one line in the convo summary template: add `Surface: claude.ai | claude-code`. Folded into Plan 04 as Task 3.

### Human-readable chat title at the §2e handshake

The user proposed a new piece of design: have the §2e convo-name handshake offer both the file slug (canonical identifier) AND a human-readable rendering of it (for the WebUI title field), so the user can paste the title into the chat-rename field and the WebUI chat list becomes a navigable index into `docs/convos/`. The file slug stays canonical (single authoritative ID); the title is derived from the slug by a deterministic rule. Bidirectional coupling for ~5 seconds of effort per session.

Mapping rule agreed-upon: drop the date prefix, replace underscores with spaces, sentence-case, em-dash for compound concepts, hyphen for compound words within a single concept. Example: `20260511_clone_first_ship` → "Clone-first ship"; `20260510_skill_ports_initial_ship` → "Skill ports — initial ship"; `20260509_phase4_runtime_and_skill_index` → "Phase 4 runtime and skill index". Plan 04 Task 4 lands the §2e edit and the full mapping table for existing convos.

This affordance is WebUI-specific in practice — Claude Code doesn't have a comparable chat-title concept that the user sees in a scrollback list, so the parenthetical is informational there and the agent should not feel obligated to invent a title when the runtime probe detects Claude Code.

### Plan 04 written and linked

Per the user's request ("write the next plan, and be sure it's linked"), agent read `write-a-plan/SKILL.md` (announcing this time), drafted Plan 04 with the four-task structure above following write-a-plan's prescribed header/footer/granularity. Plan 04 lives at `docs/plans/04_sandbox_tooling_and_companion_cleanups.md` (commit `2781b45`); STATUS Plans-list and Suggested-next-session both updated to link it (commit `910c80a`).

### Additional commits from the continuation

| SHA | Message |
|---|---|
| `2781b45` | plan: 04 — sandbox tooling matrix + companion cleanups (terminology sweep, Surface field, handshake rename slug) |
| `910c80a` | STATUS: link Plan 03 (shipped) and Plan 04 (queued) in Plans list; Suggested next session points at Plan 04 |
| (this commit) | convo: 20260511_clone_first_ship — append continuation (Plan 04 + procedural lessons + terminology fix) |

### Procedural notes for whoever picks up Plan 04 next session

- The fresh-chat verification of clone-first (Plan 03 Task 1 verification plan) is **not** in Plan 04; it's done independently in a separate fresh chat by Dan when convenient. It's not a session of "work" in the usual sense, more a smoke check.
- Plan 04's four tasks can be split across two sessions if context budget is tight: Task 1 + Task 3 in a fresh chat (Task 1 is the actual fresh-chat work, Task 3 is a one-line skill edit that can fold in), then Tasks 2 + 4 in a follow-on. Or all four in one session if it stays focused — total estimated effort is 60-90 min.
- The `TodoWrite` translation gap (mentioned above) is genuinely worth tracking somewhere more durable than this convo. Possible homes: (a) §8 Parking Lot as a separate item alongside banner-vs-proper-REST, or (b) STATUS Open Questions. Defer the decision to whoever picks up Plan 04.
