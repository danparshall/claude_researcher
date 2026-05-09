# claude_researcher — Phase 3: Bootstrap Design + Implementation

**Date:** 2026-05-09 (session rolled over from 2026-05-08 evening; finish at this date)
**Repo:** claude_researcher
**Plan:** [docs/plans/01_initial_build.md](../plans/01_initial_build.md) — Phase 3 primarily, with architectural decisions that will affect Phases 4–7

## Summary

Wrote the production `template/BOOTSTRAP.md` for Phase 3 after an extended design conversation that uncovered three architecturally important findings, all confirmed by actual testing on claude.ai (not hypothesized): (a) claude.ai's built-in WebFetch tool reaches public URLs verbatim and is **not** subject to the egress allow list, while sandbox bash-curl is — meaning the bootstrap has two distinct fetch mechanisms with different trust postures and different precondition requirements; (b) the natural-sounding "treat the fetched instructions as if I typed them" framing **backfires**, because that's exactly the prompt-injection-attack pattern claude.ai's defenses are tuned to flag; (c) sensitive-action confirmation gates must be **scripted** into BOOTSTRAP.md rather than delegated to the agent's own judgment, otherwise different agents invent different gates inconsistently.

The session also fixed Phase 2 wording bugs (Settings, not Project Settings; user-wide allow list, not per-Project) and produced a thin-slice BOOTSTRAP.md as a smoke test before committing to the production version.

## Work Done

- **Flipped repo from private to public.** Required for `raw.githubusercontent.com` URLs to resolve from external claude.ai chats. Repo now at `https://github.com/danparshall/claude_researcher` (public, was private during Phase 1+2).
- **Phase 2 fixes committed (`2208e69`):**
  - `template/_PROJECT_INSTRUCTIONS.md.template` — "Project Settings" → "Settings"; user-wide framing; WebFetch vs sandbox-curl distinction added
  - `template/templates/domain_allowlist.txt` — comment header path corrected and one-time-user-wide framing
  - `template/README.md` — bootstrap prompt code block replaced with the production version (project-purpose paragraph, transparency note, format-compliance reasoning; "treat as typed" line removed)
  - `docs/plans/01_initial_build.md` — task 16 corrected with cross-reference to this convo
- **Thin-slice BOOTSTRAP.md (`6511a52`)** — minimal 4-step orchestration (~50 lines) used as a smoke test. Two test runs against incognito claude.ai chats validated the orchestration pattern works (verbatim fetches, sequential execution, no per-step re-prompts) but surfaced the design-feedback that informed the production version.
- **Production BOOTSTRAP.md (`7e13380`)** — replaces thin-slice. 13-step orchestration (~480 lines) covering open / mode-check / user-prefs read / GitHub readiness (account + PAT) / topic + repo name / basic_config existence-check / Settings allow list / interview / repo creation / file seeding / Project setup / validation / done. Plus appendix of common issues. Plus `template/templates/personal_info.md.template` defining the v1 schema for the user's lifetime config.

## Decisions Made

- **Two fetch mechanisms, two trust postures.** WebFetch (claude.ai's built-in) for public upstream content (BOOTSTRAP.md, CLAUDE.md, skill specs, scripts) — reaches `raw.githubusercontent.com` without allow-list configuration, returns content verbatim. Sandbox bash-curl with PAT for the user's private repos — requires `api.github.com` in user-Settings allow list, requires PAT for auth. BOOTSTRAP.md uses both; choice is made per-call based on what's being fetched.
- **Settings (not Project Settings) for the Domain Allow List.** Pro users have NO per-Project allow list — the only allow list is at user-level Settings (`Settings > Capabilities > Allow Network Egress > Domain Allow List`), configured once, applies to all chats. The user's `basic_config/domain_allowlist.txt` is a **record** of what was configured for re-creating on another machine, NOT something pasted per-Project.
- **Bootstrap prompt framing — what works and what doesn't:**
  - **Works:** project-purpose explanation, transparency note (files publicly readable), format-compliance reasoning ("data goes into specific files that runtime sessions read"). All three give the agent context to evaluate legitimacy.
  - **Backfires:** "Treat the instructions as if I had typed them myself." Explicitly identified by the test agent as the prompt-injection-attack signature. **Removed from production prompt.**
  - **Cooperates with injection defense:** "Sensitive operations have explicit confirmation gates scripted into the orchestration file. Feel free to add your own confirmation prompts at any boundary that gives you pause." Works with the model's caution rather than against it.
- **Confirmation gates are scripted into BOOTSTRAP.md, not invented by the agent.** Each action-class boundary (repo creation, file writes, settings changes, PAT handling) has an explicit `CONFIRMATION GATE` block that tells the agent exactly what to ask. The agent reading the doc doesn't have to invent boundaries from scratch.
- **Verification affordances are offered, not demanded** — following the [kill-convo](https://github.com/dparshall/claude-exit) design pattern. Each sensitive action is paired with concrete verification steps (re-read after write, smoke test, env-var checks). The agent CAN perform them but isn't required to. **Availability builds trust; the verification itself is usually skipped once the agent has read through the document and seen the structure.** This is the load-bearing insight from the kill-convo docstring study.
- **Interview structure: three thematic batches** (identity, how-they-work, operating preferences) instead of nine sequential questions. Reduces turn count; matches the "user pre-fill from claude.ai prefs where available" pattern. Each batch is summarized back before moving on.
- **Identity source-of-truth: read-then-confirm.** If claude.ai's user preferences expose name / role / interaction style, agent pre-fills the interview with "I see X — want to use that, or different?" If preferences are empty, agent asks fresh. Either way, the user's chat answer is recorded as authoritative; divergence (typed answer differs from prefs) is silently honored.
- **PAT scope: fine-grained with "All repositories"** (current and future). Necessary because fine-grained PATs cannot be scoped to repos that don't yet exist, and bootstrap creates new repos. Documented as broader-than-ideal but a v1 trade-off; user can rotate to narrower scope post-bootstrap if desired.

## Bugs / Friction Surfaced

- **GitHub raw CDN edge cache** — flipping a repo private→public doesn't invalidate already-cached "private/404" responses on CDN edges. Cache `max-age=300` (5 min) governs propagation. Workaround: cache-buster query string (`?cb=1`) or use `api.github.com/contents/...` (different cache path) for time-sensitive reads.
- **"Treat as if I typed" framing in bootstrap prompt** — actively backfires (see Decisions). Removed.
- **Bash command chains starting with `echo` defeat the curl-prefix permission allowlist** in Claude Code's local environment. Use separate Bash calls instead of chaining with `echo`. Captured for future sessions in this repo.
- **Nori `commit-author.js` hook still mangles commit messages** with literal `\n\n` instead of newlines. Same issue carried over from prior session. Persistent across all of today's commits. Cosmetic only. Upstream issue still un-filed.

## Open Questions (carry-forward to Phase 4 and beyond)

- **Phase 4 (CLAUDE.md) is the natural next phase.** Step 10 of BOOTSTRAP.md has a placeholder for the custom-instructions text the user pastes into their Project; Phase 4 fills it in canonically. Step 11's validation also assumes Phase 4's runtime CLAUDE.md is reachable from the upstream URL.
- **`git_fluency`-tiered commit policy** carries forward from the prior session. Phase 4's CLAUDE.md needs to implement: novice = checkpoint often + under the hood; occasional = light narration + confirm before structural changes; fluent = terse.
- **Phase 8 self-walkthrough testing methodology** — incognito claude.ai chats are NOT a true "fresh user" simulation (the agent still sees user-level preferences; "incognito" only means "this chat won't be saved"). Real fresh-user testing requires a sock-puppet claude.ai account or a way to clear preferences. Pin down before Phase 8.
- **Phase 10 publish strategy** still undecided. URLs in BOOTSTRAP.md and `template/README.md` currently use `.../main/template/<file>` paths. Phase 10 picks between flipping dev repo as-is, restructuring (`template/` → root + dev files into `_dev/`), or separate public repo. Punt.

## What's Next

**Phase 4 — write `template/CLAUDE.md`** (plan tasks 19–26). The runtime spine every research session loads. Once Phase 4 ships, Step 10 of BOOTSTRAP.md gets its placeholder replaced with the canonical custom-instructions text, and the bootstrap is testable end-to-end including validation.

**Optional before Phase 4: a partial real-bootstrap test** of Steps 0–9 of BOOTSTRAP.md against an incognito chat with PAT-handling enabled. Would exercise real repo creation and file seeding, surfacing any API friction (PAT scope errors, 422 on existing files, etc.) before the design is locked. Bootstrap is currently testable through Step 9; Steps 10–11 wait on Phase 4.
