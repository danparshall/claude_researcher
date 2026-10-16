# Token-dispenser Phase 0 prep → tabled

**Date:** 2026-08-31
**Branch:** github-mcp-migration
**Machine:** Dans-MacBook-Pro
**Surface:** Claude Code CLI (Fable) — concurrent with the sibling session that shelved plan 13 (`8fcbc5a`); this session started from the build handoff, the sibling from the connector-probe follow-up. Both converged on the same outcome independently.

## Summary

Fable CLI session picking up the plan-13 build handoff ("start with Phase 0 as a hard gate"). Pre-flight and account-free prep went cleanly: a web-research agent re-verified Cloudflare's stock `remote-mcp-github-oauth` recipe against current (Aug 2026) docs, and the spike scaffolded and dry-run-built locally with one dependency workaround. No accounts were created and no code was written.

The session pivoted when Dan challenged the premise — "Cloudflare? How did they get involved?" — surfacing that the hosting *platform* had been baked into plan 13 without being one of the four explicitly-resolved questions. The honest cost accounting that followed (Cloudflare account + GitHub App + OAuth server + standing service, owned forever, for a user base of one) flipped to "not worth it today"… then partially flipped back when Dan corrected the friction estimate: rotation is not one paste but **one paste per Project, and he has ~10 Projects**. That correction cuts *for* the dispenser (fixed cost, value scales with N) — but Dan tabled the build anyway, preferring a zero-infra interim. Meanwhile the sibling session, unprompted, had committed the same shelve decision with the same interim (annual-expiry PAT + paste-helper).

This session's doc contribution: the N≈10 quantification (now in plan 13's status area) and the Phase 0 prep notes (appended to plan 13), so a future pickup starts at `wrangler login` rather than at research.

## Topics Explored

- Current (Aug 2026) state of the Cloudflare remote-MCP-with-GitHub-OAuth template (web-research agent; findings in plan 13's prep notes)
- Why a hosted third party is intrinsic to the dispenser design (public HTTPS reachable from Anthropic's cloud, 10s OAuth timeout, always-on, holds the App private key) — and why Cloudflare specifically (free, zero-maintenance, the documented DCR-capable reference path)
- Cost-benefit of the dispenser vs. zero-infra alternatives, re-run twice: once at N=1 paste (dispenser loses), once at N≈10 pastes/rotation (dispenser's amortization argument revives)
- The 1-year fine-grained-PAT expiration option (the 90-day cadence was GitHub's default, not a requirement) — independently adopted as the interim by the sibling session

## Provisional Findings

- **Phase 0 prep verified account-free**: template live at the historical path; `--legacy-peer-deps` needed (workers-types v4/v5 peer skew); `/mcp`-only endpoint; DCR out-of-box; SQLite-DO free tier suffices; `McpAgent` deprecated → real build should use `createMcpHandler`. Full list: plan 13 "Phase 0 prep notes."
- **Rotation friction is ~10× the briefing's implicit estimate**: ~10 claude.ai Projects, one Project-Instructions paste each, per rotation. Same PAT, N pastes.
- **Process gap worth remembering**: plan 13 resolved four questions with Dan but never explicitly surfaced "a Cloudflare account will exist and hold a key that can mint tokens for your repos" as a decision. Platform choices that create standing third-party trust relationships should be resolved questions, not tech-stack lines.
- Honesty note on the interim: with ~10 Projects the practical PAT is broad-scoped (Dan's actual practice per the design doc), so the annual-expiry interim is a *long-lived, broad* credential in Project Instructions — exactly the exposure the dispenser design exists to kill. Accepted with eyes open; sharpens trigger (a) below.

## Decisions Made

- **Plan 13 tabled** (Dan, this session) — same outcome as the sibling session's shelve commit `8fcbc5a`; no accounts created, no spike deployed. Revisit triggers unchanged: recurring annoyance, real beta user, or ~Oct–Nov 2026.
- **Docs updated as the deliverable**: N≈10 scale addendum + Phase 0 prep notes appended to `docs/plans/13_token_dispenser.md`; this convo doc; STATUS.md session line. Branch parked (pushed), not merged.
- Spike scaffold at `/tmp/mcp-spike/` left to evaporate; nothing worth preserving beyond the notes.

## Results

- Plan 13 addenda (scale note + Phase 0 prep notes) — see [`docs/plans/13_token_dispenser.md`](../plans/13_token_dispenser.md)

## Open Questions

- At revisit time: does N≈10 (and growing?) clear the bar for the dispenser's fixed setup cost, given the paste is now annual?
- Unverified from prep: whether claude.ai falls back to `/sse` on a bare root URL (moot if `/mcp` is pasted explicitly); node-22-specific template behavior (absence of failure reports only).
- Session-start reminders went unprocessed by Dan's choice-by-omission (build handoff took priority); the fired list is in this session's transcript, and dotfiles #77 (grant applications) fires 2026-09-01.
