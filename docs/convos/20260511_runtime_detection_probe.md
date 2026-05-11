# Runtime Detection Probe + System-Prompt-Aware CLAUDE.md Thread

**Date:** 2026-05-10 / 2026-05-11 (session straddled midnight)
**Branch:** main
**Predecessor convo:** [`20260510_skill_ports_initial_ship.md`](20260510_skill_ports_initial_ship.md) — that one wrapped the initial 15-skill ship with the prose REST-adaptation banner. This convo captures what happened *after* that finish-convo, when a different agent's session surfaced something better than a prose banner.

## Summary

The previous finish-convo had just closed the skills-ship arc. User then shared transcript of a different claude.ai session (the agent had been trying to add NBER papers to the knowledge base, hit web_fetch binary-blob limitations, and along the way discovered `IS_SANDBOX=yes` as an empirical claude.ai marker). User asked whether we should update the skill to handle that — opening question was effectively *"should runtime-environment detection be procedural rather than a prose banner?"* I argued the other agent's framing slightly undersold the insight: the env-var fork is architecturally better than the prose banner I'd shipped earlier today, and the same pattern (if pushed upstream into Nori Researcher) collapses the dual-implementation maintenance bucket from yesterday's 3-layer-Nori-chain discussion entirely.

Shipped two commits along this arc. First (`0802ec8`): replaced the one-line REST-adaptation banner in each of the 6 Researcher skills with a `## Runtime detection` header containing a bash probe (`$IS_SANDBOX=yes` OR `/mnt/skills/public` exists) and two prose branches (claude.ai sandbox: translate `git`/path idioms; Claude Code: follow as-is). Second (`1edbbc1`): when I probed my own environment to answer user's "can you tell if you're in Code?" question, I discovered `CLAUDECODE=1` is a positive Claude Code marker — meaning both environments have affirmative signals, not just claude.ai. Upgraded the probe to positive-marker detection on both sides plus an explicit `unknown` branch that surfaces misconfiguration rather than silently picking the wrong environment.

After shipping those, user raised the next architectural question: should the env-var probe live in `template/CLAUDE.md` (centralized, once per session) rather than repeated in each skill header? I sketched three scope options (centralize-only-in-this-repo, centralize-here-plus-upstream-Nori, leave-as-belt-and-suspenders) and pushed back gently that the right answer depends on which CLAUDE.md we mean — `template/CLAUDE.md` only reaches claude.ai sessions, while real convergence (one CLAUDE.md works in both environments) requires upstream Nori work. User parked the centralization question and opened a related but distinct thread: *"what's the difference in the system prompt between Code and claude.ai, and should we put environment-specific complementary content in CLAUDE.md?"* I gave a candid read separating what I can directly observe (my own Code system prompt — broadly characterizable from this session) from what I'd be guessing about (claude.ai's prompt, which I don't have access to). Argued that working backward from *observed behavioral gaps* is more reliable than trying to enumerate prompt diffs from speculation. User went off and investigated this externally on a claude.ai web agent so the actual load sequence could be inspected directly. **That thread is open and continues outside this convo.**

## Topics Explored

- `$IS_SANDBOX=yes` as empirical claude.ai marker (surfaced by another agent's session).
- `/mnt/skills/public` directory existence as belt-and-suspenders fallback for claude.ai detection (more architecturally stable than env-var name).
- `$CLAUDECODE=1` as positive Claude Code marker (discovered when user asked "can you tell if you're in Code?" and I ran the probe in this session). Family of related vars: `$CLAUDE_CODE_ENTRYPOINT=cli`, `$CLAUDE_CODE_EXECPATH=...`, `$CLAUDE_CODE_SESSION_ID=...` — multiple positive signals available.
- Positive-marker detection on both sides vs. absence-inference. The shift matters: absence-inference silently picks the wrong branch if a single env var disappears (rename, custom shell, stripped env); affirmative-on-both-sides + `unknown` fallback surfaces misconfiguration.
- Whether the probe belongs in each skill header (where it lives now) vs. centralized in CLAUDE.md (parked).
- What system prompts each environment ships with, and what CLAUDE.md should add to complement them. Argued for compensate-observed-gaps over enumerate-prompt-diffs. User externalized this investigation.
- The web_fetch-binary-blob platform limitation (from the other agent's session) — not fixable from skill side; an Anthropic feature request (write binaries to sandbox path, return path instead of opaque blob). Logged here for visibility.
- The dual-implementation maintenance question from yesterday: if env-var fork goes upstream into Nori Researcher's CLAUDE.md template, the "Researcher skills (dual-implementation maintenance)" bucket collapses — single skill body works in both environments.

## Provisional Findings

- **Both runtime environments expose reliable positive markers.** Not just claude.ai (`IS_SANDBOX`, `/mnt/skills/public`) but Claude Code too (`CLAUDECODE`, `CLAUDE_CODE_ENTRYPOINT`, `CLAUDE_CODE_EXECPATH`, `CLAUDE_CODE_SESSION_ID`). This is better than the symmetric setup the other agent's session implied — we don't have to detect Code by absence-of-claude.ai-markers.
- **A procedural env-var probe is architecturally better than a prose banner for cross-environment skills.** The banner relies on the agent remembering and applying advice; the probe is a step the agent runs and branches on. The shipped skills now follow the procedural pattern.
- **The convergence path is real.** If env-var fork lives upstream in Nori Researcher's CLAUDE.md template, the same skill body works in both Code (which reads ~/.claude/CLAUDE.md installed by `sks switch researcher`) and claude.ai (which reads `template/CLAUDE.md` via WebFetch). That kills the dual-implementation maintenance question for both skills and CLAUDE.md.
- **Designing environment-specific CLAUDE.md content without inspecting the actual system prompts is building on sand.** I argued for the empirical approach (work backward from observed behavioral gaps); user agreed and ran the inspection externally on a web agent.

## Decisions Made

- **Probe lives in each of 6 Researcher skill headers (for now).** Not centralized to CLAUDE.md yet. Centralization is the next-thread question once user returns from the external system-prompt investigation.
- **Probe uses positive markers on both sides + explicit `unknown` fallback.** Old absence-inference probe was strictly worse; replaced same-day.
- **Probe order: claude.ai first, then Code, then unknown.** Rationale: claude.ai is the more constrained environment; if for any reason both sets of markers fired (env-var leak across environments — unlikely but possible), defaulting to claude.ai mode is the safer choice since it expects fewer tools.
- **Centralization of probe → parked** pending external system-prompt-comparison thread.
- **System-prompt-aware CLAUDE.md design → research thread, externalized.** User running this in a claude.ai web session so the actual prompt load sequence can be inspected directly. Continuation outside this convo file.

## Results

- **Commit [`0802ec8`](https://github.com/danparshall/claude_researcher/commit/0802ec8):** replaced one-line REST-adaptation banner with `## Runtime detection` env-var probe in 6 Researcher skills (`finish-convo`, `update-docs`, `add-paper`, `audit-docs`, `audit-papers`, `init-research-repo`). +91 lines net. Architectural improvement over prose banner.
- **Commit [`1edbbc1`](https://github.com/danparshall/claude_researcher/commit/1edbbc1):** upgraded probe from absence-inference to positive-marker detection plus `unknown` fallback branch. +43 lines net. Same 6 skills.
- **SKILL_INDEX.md status block updated twice** along this arc to accurately describe the probe shape — first describing the env-var probe pattern (after `0802ec8`), then upgrading the description to reference the positive-marker shape (after `1edbbc1`).
- **No STATUS.md / convo update for this arc until this very finish-convo.** The previous finish-convo at `9bed7e0` had already wrapped the skills-ship arc; the runtime-detection arc opened immediately after and ran on its own through two commits before pausing here.

## Open Questions

- **Where does the probe ultimately live?** Three options sketched: (1) centralize in `template/CLAUDE.md` only, rip from skill headers — claude.ai works, Code side unaffected; (2) centralize + keep skill probes as belt-and-suspenders — slight duplication but self-contained skills; (3) full convergence — add same probe to upstream Nori Researcher CLAUDE.md template, then one CLAUDE.md works in both environments. Parked pending the system-prompt thread.
- **What does the external system-prompt comparison reveal?** Specifically: what behaviors does each prompt do well, what gaps do they leave that a complementary CLAUDE.md should fill, and how much should the two CLAUDE.md flavors actually diverge vs. converge? Pending user's external investigation.
- **Should the env-var fork pattern be pushed upstream into Nori Researcher's CLAUDE.md template?** Architecturally collapses the dual-implementation maintenance problem from yesterday's 3-layer-chain discussion. Cost: an upstream PR + async wait on review. Benefit: ongoing maintenance simplification across both skills and CLAUDE.md.
- **web_fetch binary-blob limitation.** Anthropic feature request: have web_fetch write binaries to a sandbox path (e.g., `/tmp/web_fetch_<hash>.pdf`) and hand the path back, rather than eliding to opaque `[binary data]`. Not fixable from our side. Worth filing an issue with Anthropic.
- **Four add-paper-specific improvements** from the other agent's session (claude.ai fallback chain paragraph, standardized PDF-missing-marker convention, arXiv-mirror-first hint for econ papers, named-allowlist suggestion on egress block). Not addressed in this arc. Should go into `02_skill_ports.md` as a Wave-2/3-proper task list when those waves get done properly.

## Continuation

User externalized the system-prompt-comparison thread to a claude.ai web agent for direct inspection of the load sequence. That investigation lands in a future session — when it does, the centralization question (above) can be answered from real data rather than from my speculation about prompt content. Worth picking up next session, alongside the unfinished items above.

## Deferred from this arc

- Wave 0 of `02_skill_ports.md` (provenance + sync infrastructure) — still deferred from yesterday. Drift not yet a real concern.
- Phase 4.6 (CLAUDE.md retrofit from AITaxBID audit) — still the natural next chunk per STATUS.md's prior suggestion, but waiting on the system-prompt thread result might change what goes into CLAUDE.md.
- Wave 4 (AITaxBID Tier A: `writing-skill`, `branch-document-review`) — untouched.

---

## Postscript (added at finish-convo time, after rebase against `origin/main`)

While this finish-convo was being written, a **parallel dogfooding session** had already run on `origin/main` and shipped 9 commits (`09719f9` through `7c6a5c6`). That session — captured in [`20260511_dogfooding_session.md`](20260511_dogfooding_session.md) — *is* the system-prompt-comparison thread this convo described as "externalized." It ran in claude.ai (so Dan could feel beta-user friction firsthand) and resolved several of the open questions logged above:

- **System-prompt comparison:** done. Canonical claude.ai prompt at `platform.claude.com/docs/en/release-notes/system-prompts`; community-maintained Code reference at `Piebald-AI/claude-code-system-prompts`. The 2026-05-08 layer-analysis finding (claude.ai base thin + CLAUDE.md does the work; Code base opinionated + CLAUDE.md overrides) generalizes.
- **Stale `raw.githubusercontent.com` finding:** the audit caught 24+ hour stale stub content on the CDN. CLAUDE.md's prior assumption of ~5 minute staleness was off by at least an order of magnitude. This invalidates the WebFetch-from-raw pattern that the env-var probe's claude.ai-mode prose translation referenced.
- **Clone-first session-start design:** `git clone --depth 1` in the sandbox completes in 335ms for the 896K template repo. Bypasses the CDN entirely, lets the agent `view`/`grep` over `template/skills/` directly.
- **Plan 03** ([`docs/plans/03_clone_first_and_companion_cleanups.md`](../plans/03_clone_first_and_companion_cleanups.md)) is queued: clone-first edit + `template/CLAUDE.md` → `template/RESEARCHER.md` rename + `_PROJECT_INSTRUCTIONS.md.template` slimming + STATUS Known Issues entry for stale-CDN.

**What this means for the probe arc:**

- The `## Runtime detection` env-var probe shipped in commits `0802ec8` / `1edbbc1` is *still correct* as a per-session sandbox-vs-Code detection step. Clone-first doesn't change that.
- However, the probe's claude.ai-mode prose ("Translate local paths like `/Users/<user>/.claude/skills/...` into `https://raw.githubusercontent.com/.../template/skills/...` URLs") is now half-obsolete: clone-first means the agent reads `template/skills/<name>/SKILL.md` from a local checkout, not via `raw.githubusercontent.com`. The path-translation guidance should be updated to "read from the cloned `template/skills/<name>/SKILL.md`" when Plan 03 lands.
- The centralization question ("does the probe live in CLAUDE.md or in each skill?") is still open. Clone-first arguably makes centralization easier — CLAUDE.md runs the probe once at session-start and sets a `$RUNTIME` variable other skills can read. Worth revisiting alongside Plan 03 implementation.
- The dual-implementation-collapse argument (env-var fork upstream into Nori Researcher) is unaffected and still worth pursuing.

This Postscript exists because the rebase that produced this commit surfaced the parallel work *during* finish-convo, and the original body framed the system-prompt thread as still-pending when it was already done. The body is preserved as the chronologically faithful record of what I knew when I wrote it; this Postscript is the integrating note.
