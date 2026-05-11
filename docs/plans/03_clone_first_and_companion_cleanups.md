# Plan 03 — Clone-First Session Start, `CLAUDE.md` → `RESEARCHER.md` Rename, and Companion Cleanups

**Goal:** Replace per-file WebFetch of upstream template content with a single session-start `git clone`. Rename `template/CLAUDE.md` to `template/RESEARCHER.md` to free the conventional `CLAUDE.md` name for future per-repo use. Slim `_PROJECT_INSTRUCTIONS.md.template` down to credentials + clone command + RESEARCHER.md pointer. Document the stale-raw-CDN finding in STATUS.md so the lesson isn't lost.

**Originating conversation:** [`docs/convos/20260511_dogfooding_session.md`](../convos/20260511_dogfooding_session.md)

**Context:** A dogfooding pass on 2026-05-11 surfaced two coupled findings. First, `raw.githubusercontent.com` was serving 24+ hour stale content for `template/skills/SKILL_INDEX.md` despite the file being correct on `main` via the Contents API — much longer than the ~5-minute staleness the current `CLAUDE.md` appendix anticipates, and load-bearing for any agent following §2d's WebFetch-from-raw pattern. Second, an empirical test confirmed `git clone --depth 1` works in the claude.ai sandbox and completes in ~335ms for the 896K template repo. Together those findings make clone-first the better session-start primitive: faster, bypasses raw CDN entirely for upstream content, and lets the agent use `view`/`grep` over `template/skills/` instead of repeated WebFetch round-trips. The lazy-loading frame is preserved — the agent still reads skill bodies on-demand when triggers fire, just from local disk instead of network.

**Confidence:** High on Task 1 (clone-first verified empirically; rename is mechanical). High on Task 2 (template slimming follows directly from Task 1). High on Task 3 (documentation only). The one residual unknown is reliability of `git clone` under conditions other than the single sandbox test from 2026-05-11 — partially mitigated by the fallback path in Task 1.

**Architecture:** Three coordinated changes. Task 1 edits `template/CLAUDE.md` to add a new §2.0 (clone first) and adjusts §2d / §5 read paths from `raw.githubusercontent.com` URLs to local-disk paths under `/home/claude/.claude_researcher_template/`, then renames the file to `RESEARCHER.md` and sweeps references across the repo. Task 2 rewrites `_PROJECT_INSTRUCTIONS.md.template` as a minimal credentials-plus-pointer block (the REST recipes move into RESEARCHER.md, or get deleted entirely since the recipes are also written out in the current `CLAUDE.md` appendix and in skills). Task 3 adds a STATUS.md Known Issues entry documenting the empirical raw-CDN staleness observation.

**Branch:** main. (This repo is `main_only`; no feature branches.)

**Tech Stack:** Markdown editing only; no code changes. Empirical verification uses fresh claude.ai chats.

---

## Task 1 — Clone-first session start + `template/CLAUDE.md` → `template/RESEARCHER.md` rename

### What changes

In `template/CLAUDE.md` (which becomes `template/RESEARCHER.md`):

1. **Add new §2.0 before §2a** with the clone command and fallback semantics:
   - Primary: `git clone --depth 1 https://github.com/danparshall/claude_researcher.git /home/claude/.claude_researcher_template`
   - Fallback: if the clone fails, fall back to the current WebFetch-from-raw pattern in §2d and subsequent. Surface the failure to the user.
   - Freshness model paragraph: session-start snapshot, identical to current behavior. Optional `git pull` affordance for mid-session refresh if the user signals an upstream update.
2. **Adjust §2d** to read SKILL_INDEX.md from the local clone (`view /home/claude/.claude_researcher_template/template/skills/SKILL_INDEX.md`) rather than WebFetch. Keep the WebFetch path as the fallback branch.
3. **Adjust §5** ("For each skill you need, WebFetch its SKILL.md from the URL in SKILL_INDEX.md") to read from local clone first, WebFetch as fallback.
4. **Update the appendix** entry on raw-CDN staleness — the "~5 minutes" claim is empirically wrong by orders of magnitude. New language reflects clone-first as the primary architecture and notes the fallback's staleness exposure.

Then `git mv template/CLAUDE.md template/RESEARCHER.md` and sweep references:

- `template/BOOTSTRAP.md` — update step references and any `template/CLAUDE.md` mentions.
- `template/_PROJECT_INSTRUCTIONS.md.template` — references to CLAUDE.md become RESEARCHER.md (Task 2 will rewrite this file substantially anyway; do that pass coherently).
- `README.md` — change the parenthetical from "*(Will be renamed to `RESEARCHER.md`...)*" to the actual new name.
- `docs/plans/01_initial_build.md` — references in phase descriptions and the implementation tracker.
- `docs/plans/02_skill_ports.md` — any mentions in wave descriptions.
- Historical `docs/convos/*` — *leave alone*. They're a chronological record of what was true at the time, and renaming references would falsify that record. Out of scope here.

### Verification plan

After Task 1 lands, open a fresh claude.ai chat in this Project and observe:

1. Custom Instructions tell the agent to fetch RESEARCHER.md (Task 2 handles updating Custom Instructions in this Project; for verifying Task 1 in isolation, the agent fetching the still-old CLAUDE.md path will 404 and fall back gracefully — that's also useful to confirm the fallback works).
2. The agent's session-start sequence calls `git clone` and reads RESEARCHER.md from `/home/claude/.claude_researcher_template/template/RESEARCHER.md`.
3. The agent reads SKILL_INDEX.md from local disk (no `raw.githubusercontent.com` WebFetch for that file).
4. A skill fetch (e.g., asking the agent to use `brainstorming`) reads from local disk without a network round-trip.
5. Search the repo for residual `template/CLAUDE.md` references — should be zero in non-historical files.

Failure-mode check: temporarily break the clone (e.g., point at a nonexistent repo URL in a one-off test, or block github.com), confirm the fallback to WebFetch fires and the session still functions.

## Task 2 — Slim `_PROJECT_INSTRUCTIONS.md.template`

### What changes

Rewrite `template/_PROJECT_INSTRUCTIONS.md.template` to roughly this shape:

```markdown
# Project Instructions — claude_researcher

This Project uses the `claude_researcher` toolkit. Full runtime instructions
live upstream in RESEARCHER.md; the agent fetches them at session start.

## Credentials (yours; do not share, do not commit)

TOKEN="<YOUR_FINE_GRAINED_PAT>"
USERNAME="<YOUR_GITHUB_USERNAME>"
REPO="<YOUR_RESEARCH_REPO_NAME>"

## Session start

Your first action is to clone the upstream template, then read RESEARCHER.md
from the clone. If the clone fails, WebFetch RESEARCHER.md as fallback.

  Clone (primary):
    git clone --depth 1 https://github.com/danparshall/claude_researcher.git \
      /home/claude/.claude_researcher_template

  Fallback (if clone fails):
    WebFetch https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/RESEARCHER.md

Then follow RESEARCHER.md's session-start sequence.
```

What gets *removed* relative to the current template:

- The "Why this uses the GitHub REST API" preamble (contains an empirically wrong claim about `git clone` not working; cleaner to delete than to correct here).
- The detailed REST recipes for reading/writing/listing (those live in RESEARCHER.md and are documented at the right level there).
- The "Where to start every session" pointer at template/CLAUDE.md (replaced by the simpler RESEARCHER.md pointer above).

`BOOTSTRAP.md` Step 8 (Custom Instructions paste) needs a corresponding tweak: the substitution it performs on the template (filling in TOKEN/USERNAME/REPO) stays simple — just the three values, no recipe-block injection.

### Verification plan

1. Bootstrap a fresh Project using the updated template (full BOOTSTRAP.md walkthrough in an incognito claude.ai chat). Confirm the resulting Project's Custom Instructions are ~20 lines and contain only the credentials + clone command + pointer.
2. Open a fresh chat in the newly-bootstrapped Project. Confirm session start runs cleanly: clone fires, RESEARCHER.md reads from local, agent picks up correctly.
3. For *existing* Projects (research-knowledge-base, etc.): Task 1's CLAUDE.md edit propagates automatically next session (the agent fetches the new RESEARCHER.md, which uses the clone). The Custom Instructions in those existing Projects still have the old REST recipes — that's fine for backwards compatibility (the recipes still work; they're just redundant). Optional: a one-time chore to paste the slimmed Custom Instructions into existing Projects. Document this in HUMANS.md as an optional upgrade step.

## Task 3 — STATUS.md Known Issues entry for stale-raw-CDN

### What changes

Add an entry to the "Known issues" section of `STATUS.md` (right after the existing `commit-author.js` entry):

> **`raw.githubusercontent.com` serves stale content for >24 hours after a write.** Empirically observed on 2026-05-11 for `template/skills/SKILL_INDEX.md`: the Contents API returned the correct (updated) file on `main`, but `raw.githubusercontent.com` was still serving the old stub content from before the 2026-05-10 ship — over 24 hours later. The current `CLAUDE.md` appendix anticipates ~5 minute staleness; reality is at least an order of magnitude longer in some cases. Plan 03's clone-first design routes around this for the primary path, but the fallback WebFetch path retains the exposure. If a future agent reports template content that doesn't match `main`, the raw CDN is the most likely culprit; the fix is either to wait, force a cache refresh by editing the file with a noop change, or fall back to the Contents API URL.

### Verification plan

No mechanical verification needed — this is a documentation change. The check is just that the entry lands in the right section of STATUS.md and is discoverable by future agents reading STATUS.md at session start.

## Dependencies and ordering

1. **Task 1 first** (substantive; everything else assumes RESEARCHER.md exists and clone-first is real). Land as a single commit: rename + content edits + reference sweep across the non-historical files. Commit message proposal: `RESEARCHER.md: clone upstream template at session start; rename from CLAUDE.md`.
2. **Task 2 immediately after Task 1.** Template-update commit, separate from Task 1 so the rename history stays clean. Commit message proposal: `_PROJECT_INSTRUCTIONS.md.template: slim to credentials + clone command + RESEARCHER.md pointer`.
3. **Task 3 can land in parallel or right after.** Independent. Could even be folded into Task 1's commit, but cleaner as its own small commit. Proposal: `STATUS.md: document raw-CDN staleness as a Known Issue`.

Estimated total time: 60-90 minutes for all three. Task 1 dominates (the reference sweep is the time-eater).

## Out of scope

The following were considered but explicitly *not* included:

- **Per-user-repo `CLAUDE.md` / `CLAUDE_TEMPLATE.md`** (the Andrea/AITaxBID pattern). Freeing the `CLAUDE.md` name via the rename *enables* this future work but doesn't deliver it. STATUS.md flags it as deferred until Phase 6 ports demonstrate need.
- **Phase 4.6 universal-rule retrofits** (the five Tier-B/C patterns from the AITaxBID audit). Those land into `RESEARCHER.md` cleanly *after* Plan 03 — but they're a separate body of work tracked in `docs/plans/01_initial_build.md`.
- **Collaborator mode** (v1.1; Phase 4.5). Touches OWNER/USERNAME split and branch protection — orthogonal to the clone-first work.
- **Renaming references in historical `docs/convos/`**. Falsifies the chronological record. Convos are append-only history.
- **`PERSONA=researcher` extensibility hook.** Considered during the originating conversation, rejected on YAGNI grounds — the project is deliberately single-purpose; if users want more, "install Nori" remains the answer.
- **Mid-session `git pull` affordance.** Possibly useful, but adds surface area for unclear benefit. Defer until a real use case appears.
- **Replacing the fallback WebFetch path with Contents API `?ref=main` reads.** The Contents API doesn't suffer the same CDN staleness, but the fallback path is already a degraded mode; switching it to Contents API gains marginal robustness for complexity that's not worth it right now.

---

**Testing Details:** No code, so no test suite. Verification is empirical (incognito-chat smoke tests), described per-task above. The most load-bearing test is the post-Task-2 fresh-bootstrap walkthrough — it exercises the full chain (BOOTSTRAP.md → Custom Instructions paste → clone → RESEARCHER.md read → session-start sequence → skill fetch from local).

**Implementation Details:**
- Clone command verified empirically on 2026-05-11: `git clone --depth 1 https://github.com/danparshall/claude_researcher.git /home/claude/.claude_researcher_template` completes in ~335ms for the 896K repo. No PAT needed (public repo).
- The `git push` claim in the current CLAUDE.md appendix ("Standard git clone and git push won't reach github.com") was always wrong for clone over HTTPS; it remains plausibly correct for push (PAT-in-URL is the ick that motivated REST). The new prose should be "clone-for-reads, REST-for-writes" rather than the current "REST because git won't work."
- Task 1's reference sweep touches: `template/BOOTSTRAP.md`, `template/_PROJECT_INSTRUCTIONS.md.template`, `README.md`, `docs/plans/01_initial_build.md`, `docs/plans/02_skill_ports.md`. Historical convos are left untouched.
- Existing Projects get Task 1's benefit automatically next session (no user action). For Task 2's slimmer Custom Instructions, each existing Project needs a one-time paste; HUMANS.md can document this as an optional upgrade chore.
- The CLAUDE.md → RESEARCHER.md rename also frees `template/CLAUDE.md` for use as a *generic* template that users could optionally place at their own research repo root for per-repo overrides. Not done here, but the naming change opens the door.

**What could change:** If `git clone` reliability under wider conditions is worse than the single 2026-05-11 test suggests (sandbox transient outages, github.com rate limits, regional latency), the fallback path's exposure to raw-CDN staleness becomes more load-bearing than this plan assumes. Worth instrumenting clone success/failure rate during early dogfooding — even an informal note in `docs/convos/` after each beta session would do. If failures cluster, the fallback may need to be upgraded from "WebFetch raw" to "WebFetch Contents API" to dodge the staleness issue. Also: if Anthropic changes the sandbox's network egress posture (more restrictive or more permissive), Task 1's clone command may need adjustment.

**Questions:**
- Should the slimmed `_PROJECT_INSTRUCTIONS.md.template` retain *any* prose about "why" (the design choice of clone-first), or is the pure-commands version best? Lean: pure commands. The "why" lives in HUMANS.md and RESEARCHER.md's appendix.
- After the rename, should `template/CLAUDE.md` be re-created as an *empty placeholder* with a comment pointing at RESEARCHER.md, to avoid confusion for users who land at that path by muscle memory? Lean: no — a 404 on the old path is a clearer signal than a stub.
- Does Task 1 want a `## Recent sessions` entry in STATUS.md for the eventual landing, or is the commit message sufficient? Lean: yes, normal session entry — STATUS.md is the durable record.

---
