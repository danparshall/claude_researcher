# Design — token-dispenser MCP server; connector rewrite deferred

**Date:** 2026-08-31
**Branch:** github-mcp-migration
**Depends on:** [`mcp_migration_briefing.md`](mcp_migration_briefing.md) (problem statement), [`mcp_verification_report.md`](mcp_verification_report.md) (facts)
**Convo:** [`convos/20260831_github_mcp_verification.md`](convos/20260831_github_mcp_verification.md)

## Decision

Build a **token-dispenser**: a GitHub App installed on the user's repos, plus a minimal remote MCP server (attached to claude.ai as a custom connector) whose job is minting short-lived, per-session-scoped GitHub installation tokens. Sessions keep the existing git-clone-in-sandbox runtime unchanged — only the *source* of the token changes. The credentials block in Project Instructions loses the pasted PAT.

The briefing's preferred outcome — replace the PAT with GitHub's official MCP connector — is **deferred, not rejected**. Verification showed it is an entire runtime rewrite (no clone-shaped access; connector tokens never reach the sandbox; no commit-author override; PDF commits likely impossible), being paid for a beginner population that currently numbers zero. The verification report records everything needed to execute that rewrite when a real beta user justifies it.

### Why this shape won

- **Fixes the only real user's actual complaint** (paste-on-rotation) completely: rotation ceases to exist. Tokens are minted per session and die in an hour.
- **Zero runtime regression**: clone, local grep, real commits with per-session codenames, PDF commits, compare — all untouched.
- **Improves on today's worst practice**: Dan's occasional cross-repo sessions currently run on an all-repos PAT. With mint-time scoping, the broad grant lives server-side in the App installation; what enters chat context is always the narrow slice the session declared.
- **Preserves the legible two-repo story for IP/NDA-constrained users** at a stronger enforcement layer: they install the App on exactly two repos, and no mint request can exceed the installation.
- Briefing's design C (wrap every git op in a custom MCP server) is strictly dominated by this: same infra class, a fraction of the surface, none of the runtime loss.

## Architecture

```
claude.ai session                    Dan's infra                     GitHub
─────────────────                    ───────────                     ──────
mint_token(repos=[...]) ──MCP──▶  dispenser (CF Worker)
                                    │ verifies OAuth identity
                                    │ signs JWT w/ App private key ──▶ POST /app/installations/{id}/access_tokens
                                    │                                  {repositories: [...], permissions: {...}}
       ◀── {token, expires_at} ─────┘
git clone https://x-access-token:${TOKEN}@github.com/...   (unchanged §2.0b)
```

**GitHub App** (per adopting user; Dan registers his own):
- Permissions: `contents: read/write`, `issues: read/write`, `pull_requests: read/write`, `metadata: read`. Nothing else — no admin, no workflows, no account scopes.
- Installation: user's choice, and it is the *policy layer*. IP-constrained default: exactly `claude_research_config` + project repo(s). Flexible mode: broader installation; per-session narrowing happens at mint time.

**Dispenser server**:
- Cloudflare Worker (free tier), MCP over streamable HTTP.
- Auth: OAuth 2.1 with dynamic client registration (claude.ai's default; supported by `workers-oauth-provider`). Identity backend: "log in with GitHub"; the server authorizes only the owning user's GitHub account. **No-auth is forbidden** — an unauthenticated token minter is a credential leak with a URL.
- One tool: `mint_token(repos: string[], permissions?: subset)` → `{token, expires_at, repos, permissions}`. Defaults: `repos=[claude_research_config, <REPO>]`, permissions = the App's full (still-minimal) set; config repo commonly needs only `contents:read` — sessions may request read-only.
- Mint-time scoping uses the installation-token API's `repositories` + `permissions` narrowing parameters.
- Logs every mint (timestamp, repo list, client) to a durable store; auditability substitutes for v1 allowlisting.

**Runtime changes (template repo)** — the concrete change set:
1. `_PROJECT_INSTRUCTIONS.md.template` — credentials block: drop `TOKEN`; keep `USERNAME`/`REPO`; add "token source" stanza: *either* the dispenser connector (name it, tell the agent to call `mint_token` before §2.0b) *or* a pasted fine-grained PAT (unchanged path, stays fully supported for users without dispenser infra).
2. `RESEARCHER.md` §2.0b — clone recipe reads the token from whichever source Project Instructions declared. Add the freshness rule: **before any network git operation (clone/fetch/pull/push), if the minted token is older than ~50 minutes, call `mint_token` again and `git remote set-url origin` with the fresh token.** Local operations (read/grep/edit/commit) need no token.
3. `RESEARCHER.md` §2b — `personal_info.md` fetch: same token works against the Contents API (`Authorization: token` accepts installation tokens); no change beyond the source.
4. `resolve-runtime-issue` skill — add recovery row: git network op returns 401/403 mid-session → re-mint, set-url, retry once; if the mint itself fails, surface (connector disabled, App uninstalled, or dispenser down).
5. Post-commit hook — unchanged; its push failure already surfaces loudly, and the new recovery row covers the expired-token case.
6. `tools/fill_project_instructions.py` — **keep.** The PAT path remains a first-class template option; the helper reduces its friction.

## Token lifetime

Installation tokens are hard-capped at 1 hour by GitHub — not configurable. Accepted because: (a) tokens are only needed at network git operations; days-long sessions re-mint via a single agent-invoked tool call, no human in the loop; (b) the short life is the security property — a token leaked via transcript or prompt-injection exfil is near-certainly dead. Explicitly rejected: vending non-expiring GitHub-App *user* tokens (expiry-disabled), which would recreate the long-lived-credential-in-context exposure this design exists to kill.

## Threat model (delta vs. today)

| Vector | Today (PAT in Project Instructions) | This design |
|---|---|---|
| Credential in chat context | 90-day PAT, every session, full grant | 1-hour token, scoped to session's declared repos |
| Cross-repo sessions | all-repos PAT (actual practice) | broad grant server-side; narrow mint in context |
| Prompt-injected session | can exfil the PAT (durable) | can exfil a dying token; can request mints for any *installed* repo — bounded by installation choice, logged; per-repo allowlist deliberately deferred to v2 (revisit if installations broaden) |
| New surfaces | — | dispenser server compromise (holds App private key → tokens for all installations; mitigations: minimal App permissions, CF secrets storage, Dan-only authz); Anthropic stores the dispenser OAuth grant server-side (same class as any connector) |
| Exfil via connector egress | n/a | connector egress bypasses sandbox egress restrictions (Anthropic-documented); dispenser's egress surface is mint-only |

Residual honesty note: the minted token still enters model context and lands in `.git/config`, same hygiene rules as today (§2.0b PAT-hygiene block applies verbatim).

## What this deliberately does not do

- **No connector-native runtime rewrite** (deferred; see verification report §Verdict + manual checklist items 1–3, which should still be run while fresh — the repo-picker question decides that path's viability).
- **No multi-tenancy.** Template users wanting dispenser mode register their own App + deploy their own Worker (docs will make this a recipe). Dan hosting a shared minter would make him a custodian of other researchers' repo access — wrong trust shape for this project.
- **No change to the Project ≡ repo isolation discipline** (§4). Mint-time flexibility governs *credentials*; the runtime rule against bridging repo contexts stands on its own.

## Implementation home

The dispenser is its own codebase (like `claude-flare`): suggest new repo `danparshall/claude-researcher-tokens` (name TBD with Dan). Implementation plan to be written via `write-a-plan` when Dan schedules the build; the template-side change set (items 1–6 above) lands in this repo on this branch, gated on the dispenser existing.

## Open items

1. Repo/app naming; where the Worker lives (Cloudflare account).
2. Verify `workers-oauth-provider` DCR handshake against claude.ai's 10s OAuth-endpoint timeout (well-trodden path; expect fine).
3. Manual checklist items 1–3 from the verification report (connector repo-picker) — optional for this design, decisive for the deferred rewrite.
4. v2 candidates: per-repo mint allowlist; mint notifications (e.g., via claude-flare-style ping) if installations broaden.
