# Review note for PR #75: "the web sandbox" is two surfaces

**Date:** 2026-10-11
**Branch:** claude/claude-researcher-github-workflow-4zbkxm
**Surface:** Claude Code on the web (claude.ai/code session)
**Session:** Dan (web, claude_researcher, 20261011T1812, fable-5.1) · https://claude.ai/code/session_012eBo35M5n6wc4arnoGMs15
**For:** the local (CLI) agent reviewing PR #75 before merge. Evidence: [20261011_ccw_surface_probe.md](20261011_ccw_surface_probe.md).

## The claim

PR #75 writes about "the web sandbox" as one environment. There are two surfaces on the same proxy infrastructure, and they differ in ways the template's text depends on:

- **Project chats** on claude.ai (where plan 14's seven runs happened).
- **Claude Code on the web** at claude.ai/code (where this session ran).

Both route GitHub through the same proxy, both set `/mnt/skills/public`, `IS_SANDBOX=1`, `CLAUDECODE=1` and `GITHUB_TOKEN=proxy-injected`, and both use the same `add_repo` tool with the same reply text. The template's surface check cannot tell them apart. Past that point they diverge. Several sentences in the PR are true on one surface and false on the other, so the question for the reviewer is which surface the template claims to support, and the PR should say.

## What differs

| | Project chat (plan 14 runs) | Claude Code on the web (this session) |
| --- | --- | --- |
| Working tree | `/home/claude/<repo>`; agent clones | `/home/user/<repo>`; already cloned, shallow, before turn one |
| Project repo attach | by the agent, refused 3 of 7 | pre-attached; system prompt has a "Repository Scope" list naming it |
| Branch | agent's choice (§3) | harness assigns `claude/<slug>` and forbids pushing elsewhere |
| Git identity | unset | preset `Claude <noreply@anthropic.com>` |
| `register_repo_root` | present in some sessions only | present |
| GitHub MCP server (`mcp__github__*`) | not reported | present; PR and issue reads worked |
| Non-GitHub hosts | 200 (`example.com`, `arxiv.org`; plan 15 T3, same account) | 403 from the egress gateway; per-environment Network access setting |
| `personal_info.md` read | refused 3 of 4 | allowed, first try |
| Classifier refusals | attach, full clone, profile read, push | one: a batch of read-only commands, cleared when split |

Sample sizes: seven sessions on one side, one on the other, different models (Opus 5.5 there, Fable 5.1 here), and a classifier that is not deterministic. The rows about paths, branch, identity, scope list and network are structural and will hold; the rows about refusals are a sample.

## Where the PR text is true on one surface only

1. **§2.0b** clones to `/home/claude/${REPO}` (23 mentions of `/home/claude/` in RESEARCHER.md, 3 in LITE.md, 1 in each Project Instructions template, 2 in `resolve-runtime-issue`). On Claude Code on the web the clone exists at `/home/user/${REPO}` and the add-repository reply names that path in its `workspace` field. A second clone to `/home/claude` would work but leaves the harness's clone, branch and stop hook pointing at the other tree.
2. **§3 branch resolution** picks line branches or `main`. Claude Code on the web forbids pushing to any branch but the assigned one. Following §3 there means either a refused push or an instruction violation.
3. **BOOTSTRAP Step 1** says `curl -sI https://example.com` returning 200 means egress is on. On Claude Code on the web it returns the gateway's 403 under the default environment policy while GitHub works, and the fix is the environment's Network access setting, not claude.ai's Domain allowlist. A BOOTSTRAP run from this surface would send the user to the wrong setting.
4. **§2.0c "No add-repository tool at all → stop"** is right on both. But **"Projects have no pre-attached repo list"** (PR description, "Known open") is a Projects fact; Claude Code on the web has one, which is why the project-repo attach refusals cannot happen there.
5. **§2b's "the permission check has refused this read in most test sessions"** is a Projects observation stated as a property of the sandbox. One session here allowed it. The guidance (carry on without it, don't ask for a go-ahead) is still fine; the sentence should name the surface.

## Findings that hold on both surfaces

These are worth folding into the PR regardless of the decision below:

- **`GH_TO_REST.md` is missing routes the proxy now advertises.** The GraphQL refusal message lists REST endpoints for review threads (`GET /repos/{o}/{r}/pulls/{n}/ccr/review_threads`), resolving and unresolving a thread (`POST .../ccr/comments/{id}/resolve`, `/unresolve`), auto-merge (`PUT` or `DELETE .../ccr/auto_merge`) and draft toggles (`POST .../ccr/ready_for_review`, `.../ccr/convert_to_draft`). The review-threads route returned 200 here. `branch-document-review` and `finishing-a-research-branch` are the consumers.
- **`gh auth status` reports the proxy token as invalid** while `gh api <repo path>` works. If any text suggests it as a check, drop it.
- **Take the working-tree path from the add-repository reply** (`workspace`) rather than hardcoding it. One `WORKDIR` variable set once in §2.0c and used everywhere makes the path question go away on both surfaces, and §2.0b gets one line: if the repo is already cloned at that path, use it; don't clone again (the reply says the same).
- **Expect a preset identity.** The codename step already overrides `user.name` and `user.email`; one sentence saying the preset `Claude <noreply@anthropic.com>` is normal stops an agent from treating it as a sign the user's profile was read wrongly.

## Recommendation

Decide the target surface before merging, and write it into RESEARCHER.md's opening. Two options:

- **A. Projects only (recommended for this merge).** Smallest change. Add one paragraph near the surface check: this template is written for claude.ai Project chats; a claude.ai/code session shares the GitHub path but has its own working tree, branch and network rules, and this file does not cover them. Fold in the surface-independent findings above. Open an issue for option B.
- **B. Both surfaces.** Needs `WORKDIR`, a branch rule ("on a surface that assigns a branch, work there and tell the user"), a network note in BOOTSTRAP and `resolve-runtime-issue`, and a way to tell the surfaces apart (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` and `CLAUDE_CODE_ENTRYPOINT=remote` were set here; whether Project chats set them is unknown and would need one probe). Larger, and it widens a PR that is already 22 files.

Why A: the Projects surface is where the users are, the PR's evidence was gathered there, and the sentences that are wrong on the other surface are wrong in ways that mislead rather than break. Shipping with a stated scope is better than shipping with an implied one.

What I would not do: merge with "the web sandbox" left as a single thing. The next person to hit a `/home/user` tree or a refused push to `main` from a claude.ai/code session will read the template as broken, when it was never written for that surface.

## Open

- Whether Project chats have the GitHub MCP server. If they do, several REST recipes have a tool equivalent the classifier may treat differently, and that is a bigger change to the template than anything here.
- Whether the Project-chat refusals are rarer on Fable 5.1 than on Opus 5.5. One session on a different surface can't say.
