# GitHub MCP verification → token-dispenser design

**Date:** 2026-08-31
**Branch:** github-mcp-migration
**Machine:** Dans-MacBook-Pro
**Surface:** Claude Code CLI (Fable) — note: the briefing targeted a claude.ai web session; this session did the doc-verifiable parts from CLI and left the UI-only checks to a manual checklist.

## Summary

Fable session picking up the cold handoff in [`docs/mcp_migration_briefing.md`](../mcp_migration_briefing.md). Three parallel web-research agents resolved the briefing's four unknowns against official GitHub + Anthropic docs and the `github/github-mcp-server` source. Headline: the official GitHub MCP connector is free-tier accessible and likely scopeable to selected repos (via Claude's directory connector, backed by a GitHub App), but its tool surface is API-shaped — nothing clone-shaped exists, connector tokens never reach the code-execution sandbox, commits can't carry the per-session codename, and PDF commits likely don't work. So the briefing's preferred outcome ("delete the credentials block, add one line") was an illusion: adopting the connector means rewriting the runtime away from the git-clone-in-sandbox architecture Plan 03 deliberately migrated to.

Discussion with Dan reframed the decision from "which of the briefing's A/B/C" to "which runtime, for which audience." A design branch the briefing missed won: a **token-dispenser** — Dan-owned GitHub App + minimal Cloudflare Worker MCP server whose single tool mints 1-hour installation tokens at session start, with mint-time repo scoping. It keeps the clone runtime byte-for-byte, abolishes PAT rotation (Dan's actual complaint), and fixes a previously-undocumented bad practice: Dan's occasional cross-repo web sessions currently ride an all-repos PAT. Dan clarified the two-repo scoping story was always "legible posture for IP/NDA-constrained users" rather than his own practice — the dispenser serves both, since narrow users enforce at the App-installation layer while flexible users install broadly and mint narrow.

The connector-native runtime rewrite was deferred (not rejected) until a real beta user exists to justify paying the architecture cost — with the verification report preserving everything needed to execute it later.

## Topics Explored

- The four briefing unknowns: Copilot subscription requirement, tool surface vs. RESEARCHER.md's git ops, OAuth scope narrowness, per-Project connector auto-enable
- Why an MCP connector can never feed `git clone` (tokens held server-side by Anthropic; sandbox never sees them)
- GitHub MCP server tool surface in detail (`push_files` multi-file commits, no author override, no compare-refs, no archive/tarball, text-only content params)
- Claude connector directory's first-party GitHub connector (GitHub App `claude-github-mcp-connector`) vs. the broken URL-only custom-connector path (hosted server lacks DCR)
- claude.ai connector mechanics: account-level attachment, default-on in new chats, no Project-level config, private-Projects-only, static-headers beta
- Token lifetime economics: GitHub's 1-hour hard cap on installation tokens vs. Dan's days-long sessions → re-mint-on-demand pattern (only network git ops need a token)
- Mint-time scoping (`repositories`/`permissions` params on the installation-token API) as the answer to Dan's occasional cross-repo sessions
- Audience split: hypothetical novice beta users (connector UX win) vs. the one real user (clone-architecture win)

## Provisional Findings

- **No Copilot license needed** for the hosted GitHub MCP server — available to all GitHub users; the `githubcopilot.com` URL is branding.
- **Tool surface covers operations, not architecture**: multi-file single commits, PRs, issues, history introspection all present; clone-shaped access, commit-author override, compare-refs, and (probably) binary commits absent.
- **Two-repo OAuth scoping is plausible** via the directory connector's GitHub App install flow ("Only select repositories") — unverified in the actual claude.ai consent UI; the bare custom-connector-by-URL path fails (no DCR support server-side).
- **No per-Project connector auto-enable exists**, but account-level connectors are default-available in new chats, so the feared per-chat toggle dance doesn't materialize. Connectors work only in private Projects.
- **MCP-shaped writes are instantly durable** — would eliminate the ephemeral-sandbox/push-early failure class entirely (a genuine point in the deferred rewrite's favor).
- **First-party GitHub integration on claude.ai is file-sync only** (Project knowledge), not tool access — the template's "until Anthropic supports GitHub integration" premise only half-fell.
- Anthropic docs flag that enabled MCP connectors bypass sandbox network-egress restrictions for exfiltration purposes — belongs in the template threat model regardless of design.
- Full findings with sources: [`docs/mcp_verification_report.md`](../mcp_verification_report.md).

## Decisions Made

- **Build the token-dispenser; defer the connector rewrite.** Design doc: [`docs/mcp_migration_design.md`](../mcp_migration_design.md). Rationale: fixes the only real user's actual complaint with zero runtime regression; the rewrite optimizes for users who don't exist yet.
- **Rejected within the design**: non-expiring vended tokens (recreates long-lived-credential-in-context), no-auth on the dispenser (unauthenticated token minter), Dan-hosted multi-tenancy (wrong trust shape — adopters register their own App + Worker).
- **Two-layer scoping policy**: App installation = the legible enforcement layer for IP/NDA-constrained users; mint-time narrowing = per-session least privilege for flexible users. v1 dispenser mints for any installed repo (logged); per-repo allowlist deferred to v2.
- **Keep `tools/fill_project_instructions.py`** — the PAT path remains a first-class template option for zero-infra users, so the paste-helper stays useful (briefing had left its fate contingent).
- **Session interaction note**: Dan called out over-use of opaque option labels ("A′/B′/D") mid-discussion — matches RESEARCHER.md §0's "refer to sections by names, avoid non-standard jargon." Restated plainly thereafter.
- Implementation plan: [`docs/plans/13_token_dispenser.md`](../plans/13_token_dispenser.md) (written immediately after this checkpoint).
- **Plan questions resolved same session** (recorded in the plan): TypeScript accepted; repo public and named `claude-researcher-tokens` so academic adopters can point agents at it; reuse the GitHub App's OAuth creds for the login check; merge timing approved — Dan's imminent PAT rotation doubles as the post-merge check and, once the dispenser ships, plausibly his last paste (via the paste-helper's debut).

## Results

- [`docs/mcp_verification_report.md`](../mcp_verification_report.md) — the four unknowns resolved with sources + a 10-minute manual claude.ai UI checklist (commit `d70a5e9`)
- [`docs/mcp_migration_design.md`](../mcp_migration_design.md) — chosen design, architecture, threat-model delta, template change set (commit `565788e`)

## Open Questions

- Does the claude.ai consent flow for the directory GitHub connector actually surface the "Only select repositories" picker? (Manual checklist item 1–3 — decisive for the deferred rewrite, optional for the dispenser.)
- Does `workers-oauth-provider`'s DCR handshake fit claude.ai's 10-second OAuth endpoint timeout? (Expected yes; plan 13 Phase 0 spike verifies before any real code.)
- Can `push_files` really not carry binary content? Expect-failure test lives in the manual checklist; matters for the deferred rewrite's `add-paper` story.
- v2 candidates: per-repo mint allowlist, mint-event notifications.
