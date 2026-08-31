# Verification report — the four MCP-migration unknowns

**Date:** 2026-08-31
**Branch:** github-mcp-migration
**Author:** Fable session (CLI, pro), responding to `docs/mcp_migration_briefing.md`
**Method:** three parallel web-research agents against official GitHub + Anthropic docs and the `github/github-mcp-server` source. Facts below are doc-verified as of 2026-08-31; items marked **[MANUAL]** require a claude.ai web UI check that a CLI session cannot perform.

## Unknown 1 — Copilot subscription required?

**No.** docs.github.com states: "The GitHub MCP server is available to all GitHub users regardless of plan type." The `githubcopilot.com` hostname is infrastructure branding, not a paywall. Only tools fronting paid features (e.g., the `copilot` toolset that dispatches the Copilot coding agent) need a license — none of those are workflow-relevant.

Source: https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/set-up-the-github-mcp-server

## Unknown 2 — Tool surface vs. RESEARCHER.md's needs

**Covers most operations, but not the architecture.** ~100 tools across ~24 toolsets (defaults: context, repos, issues, pull_requests, users). Verified against `pkg/github/tools.go` and `repositories.go`:

Covered well:
- `push_files` commits **multiple files in one commit** (Trees API under the hood) — the old "one commit per file" Contents-API degradation is gone. `create_or_update_file`, `delete_file` also exist.
- History introspection: `list_commits`, `search_commits`, `get_commit` (with `detail=full_patch` for real diffs), `get_file_blame`.
- Branches (`create_branch`, `list_branches`), PRs (create/merge/update, `pull_request_read` with `get_files`/`get_diff`), issues (full read/write — covers task-remind/task-create), `search_code`, `get_repository_tree`.

Not covered:
- **Nothing clone-shaped.** No tarball/archive tool; full snapshot = tree listing + one call per file. The §2.0b git-native runtime (local working tree, grep over `papers/text/`, sandbox analysis over repo files) cannot be fed by the connector — connector OAuth tokens live server-side in Anthropic's infra and are never exposed to the code-execution sandbox.
- **No commit-author override.** Commits are attributed to the authenticated identity; the per-session codename convention (`Dan (web, repo, HHMM)` — concurrent-session disambiguation) cannot survive on MCP-written commits.
- **No compare-refs tool.** Branch-vs-main diffs require opening a PR (then `pull_request_read.get_diff`) or walking commits.
- **Binary content is doubtful.** `push_files`/`create_or_update_file` take plain-text `content` (server-side base64). Committing PDFs (`add-paper`'s `papers/` step) likely has no path. **[MANUAL — verify empirically before any design ships.]**

Structural upside not in the briefing: MCP-shaped writes are **instantly durable** — every write lands on the remote at tool-call time, so the entire "sandbox is ephemeral / push early / post-commit hook" failure class (§5.6, §2.0b hook) disappears.

Toolset selection is URL-path-based (`/mcp/x/{toolset}`, `/readonly` suffix) — usable from claude.ai, but only ONE toolset per URL without custom headers; the workflow needs repos+issues+pull_requests, so a claude.ai connector runs the default five-toolset surface (~50 tools).

Sources: github/github-mcp-server README, docs/remote-server.md, pkg/github/{tools,repositories}.go

## Unknown 3 — OAuth scope narrowness

**Two-repo scoping is plausible via the directory connector; the bare custom-connector path is broken.** The load-bearing discovery: **GitHub is in Claude's official connector directory** (claude.com/connectors/github; web, Desktop, mobile, Code), backed by a **GitHub App** (`github.com/apps/claude-github-mcp-connector`), not a classic OAuth app. GitHub App installations use the standard install flow with "All repositories" vs. **"Only select repositories"** — so restricting the grant to exactly `claude_research_config` + `<REPO>` should be achievable, manageable afterward at github.com/settings/installations.

Caveats:
- No doc spells out the exact consent screens claude.ai shows. If the app gets *authorized* without an *installation*, behavior falls back to broader user-authorization. **[MANUAL — connect and confirm the repo picker appears; then confirm a tool call against an unselected repo fails.]**
- Adding `api.githubcopilot.com/mcp/` as a URL-only **custom** connector will generally fail: the hosted server does **not** support Dynamic Client Registration (host-integration.md), which is claude.ai's default. Workarounds exist (self-registered GitHub App + manual client id/secret in the connector's Advanced settings — documented pattern, untested end-to-end; or fine-grained PAT via the `static_headers` beta, availability on individual Pro/Max accounts undocumented **[MANUAL]**).
- If any path lands on a classic OAuth-app grant, `repo` scope = all repos — blast-radius regression; refuse that path.

Sources: claude.com/connectors/github; github.com/apps/claude-github-mcp-connector; github-mcp-server docs/host-integration.md, policies-and-governance.md, scope-filtering.md; claude.com/docs/connectors/building/authentication

## Unknown 4 — Per-Project auto-enable

**No Project-level connector configuration exists** (consistent across docs; matching open feature request anthropics/claude-code#25566). But the practical impact is mild: once added at account level, connectors are **available in new chats by default** — the per-chat toggle is chiefly for disabling; the "tool access mode" (Auto default / Always / On-demand) governs loading. No per-chat enable dance expected. Two consequences:

- The connector is account-wide: every chat (not just the research Project) carries GitHub access. Cuts the other way from the old worry.
- **Connectors only work in private Projects** (support docs) — fine for this workflow.
- Exact toggle stickiness after a manual per-chat disable is undocumented. **[MANUAL if it ever matters.]**

Sources: support.claude.com articles 11175166, 11176164, 13730515, 9517075

## Adjacent findings that affect the design

1. **First-party GitHub integration ≠ tool access.** claude.ai's built-in GitHub integration (all plans, incl. Free) only syncs repo files into Project knowledge — no commits/PRs/issues. Not a replacement, but potentially a complement (bulk read of repo files without burning tool calls).
2. **Custom-connector auth options** (for any self-hosted design): OAuth with DCR out of the box, CIMD, manual client id/secret, no-auth, static bearer headers (beta, org-framed). Pure `client_credentials` M2M is not supported; OAuth endpoints must answer within 10s.
3. **Threat-model note for the design doc:** Anthropic's own docs flag that when MCP connectors are enabled, sandbox network-egress restrictions no longer bound exfiltration — a prompt-injected session can leak data through the connector. Not a regression vs. PAT-in-context (which is strictly worse: the credential itself is in context), but it belongs in the template's security framing.
4. **Doc lag is real in this area** — github-mcp-server's own install-claude.md contradicts the newer claude.com directory page about Desktop OAuth support. Prefer the directory page; re-verify anything surprising.

## Verdict against the briefing's A/B/C ranking

- **A as written ("delete credentials block, add one line") does not exist.** Auth-wise A is in reach (free, directory connector, likely 2-repo scoping); architecture-wise it means rewriting the runtime from git-native (clone, local reads, real commits, codename authorship) to API-shaped tool calls — the very architecture Plan 03 migrated away from. A is a real candidate but as a *runtime rewrite*, not a credentials swap.
- **B as written doesn't fix the complaint** — the PAT (and its rotation paste) survives for the git half.
- **C is strictly dominated** by a smaller variant the briefing missed: a **token-vending MCP server** (design D) — GitHub App installed on the two repos + a minimal hosted MCP server whose one tool mints ~1-hour installation tokens at session start. Keeps the clone architecture byte-for-byte (only the token source changes), kills rotation entirely (tokens ephemeral by construction), preserves two-repo scoping. Cost: real hosted infra with real OAuth (no-auth is unacceptable for a token minter), and — decisive for the public template — every adopter must register an app + deploy a server, or trust a multi-tenant service. Fine as a power-user add-on; wrong as the template default.

The actual decision is therefore not "A vs B vs C" but **which runtime the template should standardize on** (connector-native MCP ops vs. PAT-fed git-native), possibly split by user tier. That decision is argued in the design discussion, not here.

## Manual verification checklist (claude.ai web, ~10 min)

1. Settings → Connectors → add **GitHub from the connector directory**. During OAuth: does a repo-selection ("Only select repositories") screen appear? Select only the two repos.
2. In a throwaway **private** Project chat: is the connector available without a per-chat toggle? List the tools it exposes.
3. Ask the session to read a file from `claude_research_config` (selected repo) — should succeed — and from an unselected repo — should fail. Confirms installation-scoped tokens.
4. Have it `push_files` a two-file commit to a scratch branch of a scratch repo; check commit author attribution on GitHub.
5. Attempt a small binary (PDF) commit via the connector. Expect failure; confirm.
6. (Optional, for the D branch) Check whether "Request headers" appears under Advanced settings when adding a custom connector — reveals static_headers beta availability on this account.

## Empirical results — checklist items 1–3 (Dan, 2026-08-31, Pro account)

Ran the same day, and the docs-derived optimism above did not survive contact with the UI:

- **Item 1 FAILED — no repo-picker.** claude.ai Settings → Connectors → GitHub led to a plain GitHub OAuth sign-in/authorize flow. No "All repositories vs. Only select repositories" screen appeared at any point.
- **The dedicated App never materialized.** After the flow, github.com/settings/applications shows exactly one authorized GitHub App: **"Claude"** (the Claude *Code* PR/Issues app, marked "Never used") — no `claude-github-mcp-connector` authorization, no new installation on the `danparshall` account. Whatever the connectors page connected, it is not the GitHub-App-installation flow the docs describe.
- **Item 3 FAILED — private repos unreachable.** A fresh claude.ai session cannot access Dan's private repos.

Interpretation (pending the follow-up research pass): the GitHub entry in claude.ai's consumer connector UI appears to be the file-sync integration and/or an authorize-without-install grant, not a working MCP tool connector with installation-scoped repo access. **Consequence for the deferred connector-native rewrite: its one advantage over the PAT (credential UX with narrow scoping, no infra) is empirically absent on a consumer Pro account as of 2026-08-31.** The token-dispenser design (see `mcp_migration_design.md`) is unaffected — it uses its own custom connector with its own OAuth server, a different mechanism whose viability is tested by plan 13's Phase 0 spike before any build.
