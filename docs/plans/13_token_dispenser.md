# Token-Dispenser Implementation Plan

**Goal:** Build a minimal remote MCP server that mints short-lived, per-session-scoped GitHub installation tokens, so claude.ai research sessions clone with ephemeral credentials and Dan never pastes a PAT again.

**Originating conversation:** [docs/convos/20260831_github_mcp_verification.md](../convos/20260831_github_mcp_verification.md) — design rationale in [docs/mcp_migration_design.md](../mcp_migration_design.md), facts in [docs/mcp_verification_report.md](../mcp_verification_report.md).

**Context:** The claude_researcher web workflow authenticates via a fine-grained PAT pasted into Project Instructions and rotated by hand. Verification showed the official GitHub MCP connector can't replace it without abandoning the git-clone-in-sandbox runtime (connector tokens never reach the sandbox). The dispenser changes only the token *source*: a GitHub App mints 1-hour installation tokens on demand, narrowed at mint time to the repos the session declares.

**Confidence:** High on the design direction (doc-verified against GitHub's App/token APIs and Anthropic's connector-auth docs). Medium on the Cloudflare specifics — the `workers-oauth-provider` + MCP-on-Workers path is well-trodden publicly but unverified by us; Phase 0 includes a cheap spike to de-risk it before real work.

**Architecture:** Two deliverables. (1) New repo — a Cloudflare Worker exposing one MCP tool, `mint_token`, behind OAuth (login-with-GitHub, owner-only allowlist); it signs an App JWT with the App private key and calls GitHub's installation-access-token endpoint with `repositories`/`permissions` narrowing. (2) This repo — template change set swapping the credentials block's pasted PAT for a pluggable token source (dispenser connector OR pasted PAT; both first-class).

**Branch:** dispenser code on `main` of the new repo (fresh project); template changes on `github-mcp-migration` here.

**Tech Stack:** Cloudflare Workers (free tier), TypeScript, `@cloudflare/workers-oauth-provider` (OAuth 2.1 + DCR), `@modelcontextprotocol/sdk` via the `agents` Workers package (Streamable HTTP transport), vitest + `@cloudflare/vitest-pool-workers` for tests, wrangler for deploy. GitHub REST: `POST /app/installations/{id}/access_tokens`.

---

## Phase 0 — Decisions and de-risk spike (~30 min)

1. **Dan decides:** app + repo name (proposal: `claude-researcher-tokens`), Cloudflare account to deploy under.
2. **Spike:** deploy Cloudflare's stock "remote MCP server with GitHub OAuth" example unmodified; attach it to claude.ai as a custom connector; confirm the DCR handshake completes inside Anthropic's 10-second OAuth timeout and a dummy tool call round-trips. **If this fails, stop and re-plan the hosting layer before writing any code.**
3. Delete the spike worker (or recycle it as the project skeleton).

## Phase 1 — GitHub App registration (manual, Dan + agent guidance, ~15 min)

1. Create the GitHub App (Settings → Developer settings → GitHub Apps): permissions `contents: read&write`, `issues: read&write`, `pull_requests: read&write`, `metadata: read`; webhooks off; "Only on this account."
2. Install it. **Installation choice is the policy layer**: Dan installs broadly (flexible mode); the docs will tell IP/NDA-constrained adopters to install on exactly `claude_research_config` + project repo.
3. Generate + download the App private key; record App ID. Also create the separate GitHub **OAuth app** (or reuse the GitHub App's OAuth credentials) for the dispenser's login-with-GitHub identity check; callback = the Worker's OAuth callback URL.

## Phase 2 — Repo scaffold (~20 min)

1. `gh repo create` (private is fine to start), scaffold from the spike/example: `wrangler.toml`, TS config, vitest config.
2. Store secrets via `wrangler secret put`: `GH_APP_ID`, `GH_APP_PRIVATE_KEY`, `GH_OAUTH_CLIENT_ID`, `GH_OAUTH_CLIENT_SECRET`, `ALLOWED_GITHUB_LOGIN` (= `danparshall`).
3. Commit scaffold.

## Phase 3 — Core minting logic (TDD)

Write ALL tests first (vitest, GitHub REST mocked at the fetch boundary — see Testing Plan for why this doesn't degrade into testing mocks), watch them fail, then implement minimally:

1. Failing test: App JWT builder produces RS256 JWT with `iss` = App ID, `iat` skewed −60s, `exp` ≤ 10 min (GitHub's rules).
2. Failing test: installation resolution — given the authenticated login, resolve the App installation ID (`GET /app/installations`), error clearly if the App isn't installed.
3. Failing test: `mintToken({repos})` calls `POST /app/installations/{id}/access_tokens` with exactly the requested `repositories` list and the (optional) narrowed `permissions`; returns `{token, expires_at, repos, permissions}` passed through from GitHub's response.
4. Failing test: GitHub 422 (repo not in installation) surfaces as a clear tool error naming the repo, not a stack trace.
5. Failing test: defaulting — no `repos` argument → `["claude_research_config"]` + configured default project repo (env var `DEFAULT_REPO`, optional).
6. Failing test: every mint appends a log record `{ts, repos, permissions, client_id}` (Workers Analytics Engine or console-structured — decide in-implementation; test the call, structure only).
7. Run tests → all fail → implement → all pass → commit.

## Phase 4 — MCP + OAuth wiring (TDD where testable)

1. Failing test: an authenticated MCP session whose GitHub login ≠ `ALLOWED_GITHUB_LOGIN` is refused at authorization time (the OAuth callback rejects; no tokens ever minted for it).
2. Wire `workers-oauth-provider` (DCR on; login-with-GitHub identity) around the MCP handler; register the single `mint_token` tool with a JSON schema: `repos: string[]` (optional), `permissions` (optional enum subset), and a description that tells the calling agent about the 1-hour lifetime and the re-mint rule.
3. Tests pass → commit → `wrangler deploy`.

## Phase 5 — Attach and verify end-to-end (manual, Dan)

1. claude.ai Settings → Connectors → add custom connector with the Worker URL; complete the GitHub login; confirm the tool appears in a new chat.
2. In a throwaway chat: call `mint_token` for a scratch private repo → `git clone https://x-access-token:${TOKEN}@github.com/...` in the sandbox → commit → push. Must succeed.
3. Negative checks: mint for a repo **not** in the installation → clear error; wait >60 min (or revoke) → push fails 401 → re-mint → `git remote set-url` → push succeeds. This validates the recovery path before we document it.
4. Second-browser check: attempt the connector OAuth as a non-Dan GitHub account → refused.

## Phase 6 — Template change set (this repo, `github-mcp-migration` branch)

Per the design doc's numbered list — each its own commit:

1. `template/_PROJECT_INSTRUCTIONS.md.template`: replace the `TOKEN=` line with a **token source** stanza — *either* "the `<dispenser-name>` connector is attached; call `mint_token` before the §2.0b clone" *or* the pasted-PAT block (verbatim today's text). Keep `USERNAME`/`REPO`.
2. `template/RESEARCHER.md` §2.0b: token acquisition from the declared source; add the freshness rule (before any network git op, if the token is >50 min old, re-mint + `git remote set-url origin`). §2b: note the same token works in the `Authorization: token` header.
3. `template/skills/resolve-runtime-issue/SKILL.md`: add recovery row — network git op 401/403 with dispenser source → re-mint, set-url, retry once; mint itself failing → surface (connector off / App uninstalled / dispenser down).
4. New `template/reference/TOKEN_DISPENSER.md`: adopter recipe (register App, deploy Worker, attach connector) pointing at the dispenser repo's README.
5. Sweep check: `grep -rn "TOKEN" template/` — every remaining PAT mention must be inside the explicitly-PAT-path text, not assumed-universal.

## Phase 7 — Docs + wrap

1. Dispenser repo README: what it is, threat model summary (link back to the design doc), setup recipe, explicit "no multi-tenancy — run your own" note.
2. This repo: finish-convo; decide with Dan whether the branch merges now (template changes are live once merged — Project Instructions in the actual claude.ai Project must be updated in the same breath, one last paste).

**Testing Plan**

I will write unit tests (vitest, Workers pool) for the minting core: JWT claim correctness, installation resolution, request narrowing (the exact `repositories`/`permissions` payload GitHub receives), 422 handling, defaulting, and mint logging — mocking only the GitHub REST boundary (the external service), never our own logic; assertions are on our code's observable behavior (requests emitted, values returned, errors raised). I will write an authorization test proving a non-allowlisted GitHub identity cannot reach the tool. The OAuth/DCR handshake and real-GitHub minting cannot be meaningfully unit-tested and are covered by the Phase 0 spike plus the Phase 5 manual end-to-end checklist (clone/push with a minted token, out-of-installation refusal, expiry-and-re-mint drill, stranger-login refusal).

NOTE: I will write *all* tests before I add any implementation behavior.

**Implementation Details**

- Single MCP tool by design; resist scope creep (no repo-listing tool, no revoke tool — v1).
- Tool description must teach the *calling agent* the lifetime + re-mint rule; that text is load-bearing UX.
- GitHub App JWTs: RS256, `iat` backdated 60s for clock skew, ≤10 min expiry — Workers `crypto.subtle` handles RS256 natively.
- Installation token endpoint returns `expires_at`; pass it through verbatim so agents can implement the 50-min freshness check without guessing.
- `ALLOWED_GITHUB_LOGIN` is a single login for v1 — matches the no-multi-tenancy decision.
- Cloudflare free tier suffices (a mint is ~2 subrequests; usage is a handful/day) — no spend from savings beyond $0.
- Private key lives only in Worker secrets; never in the repo, never in any log.
- Template changes are additive/alternative — the PAT path text must remain byte-comparable to today's so zero-infra users see no change.

**What could change:**

- If the Phase 0 spike shows claude.ai's DCR ↔ `workers-oauth-provider` handshake failing, hosting/auth layer re-plans (options: CIMD, manual client id/secret in the connector's Advanced settings, different host) — the minting core is unaffected.
- If a real beta user materializes, the deferred connector-native runtime rewrite (verification report) may supersede parts of Phase 6's template wording.
- The manual checklist's repo-picker finding doesn't affect this plan but decides the deferred rewrite's viability.

**Questions** — all four resolved by Dan, 2026-08-31 (this session):

1. **TypeScript accepted.** Python preference waived for this project; the TS surface is small and the auditable logic (JWT claims, narrowing payload) is readable regardless.
2. **Public repo, named `claude-researcher-tokens`** — explicitly so academic adopters can point their agents at it as the reference implementation.
3. **Reuse the GitHub App's own OAuth credentials** for login-with-GitHub — "simple is better."
4. **Merge timing approved.** Dan was about to rotate the PAT anyway, so the post-merge state gets checked in the same breath as the rotation — a convenient live test of the (unchanged) PAT path, and the natural moment to attach the dispenser once built, making that rotation the last one.

---
