# Proxy-only cutover

**Date:** 2026-10-10
**Branch:** proxy-only
**Surface:** Claude Code
**Machine:** pro
**Session:** Dan (pro, dotfiles, 20261010T1201, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-dotfiles/341dd750-e869-4d39-8c8e-965a528f1c44.jsonl

## Summary

Run from a dotfiles CLI session, driving a series of claude.ai web sessions in Dan's `dotfiles` Project as test runs. Dan opened with a web agent's account of a startup where its fetch of `personal_info.md` was blocked by a permission check, after which it took the commit identity from the repo's git log. Anthropic has moved every web user to the proxy sandbox (PR #73 / issue #72 added it alongside the token sandbox), so Dan wants the template switched fully to the proxy path and the Project Instructions trimmed to match.

The session tested what the auto-mode permission classifier on the web sandbox blocks. The first hypothesis, that the filename `personal_info.md` reads as personal data, was ruled out: byte-identical copies under `researcher_profile.md` and `researcher_config.md` fetched exactly as the original did, and no block in any run fell on reading the file. The blocks fell on the agent asking for repo access, and on actions the agent chose itself. Wording in the Project Instructions, including an explicit first-person authorization and later a fuller framing of the workflow, did not reliably clear them. A one-line authorization typed by Dan in chat did.

The design that worked: ask for read access to the project repo and the config repo at startup, and ask for push only at the first commit, right after the user's request that needs it. In that run the push request returned "already attached" and `git push` then succeeded with no further grant. That run also hit a block on a batch of issue closes the agent had decided on itself ([External System Writes]), which fits the same pattern. Plan 14 turns this into the template.

## Topics Explored

- Which repo is in charge of `personal_info.md`: dotfiles (`claude/personal_info.md`), pushed one way to `claude_research_config` by `sync_to_basic_config.py`. The subject, author, repo owner and instructing party are all the user, so a "personal data" flag on reading it is a false positive.
- Whether the filename trips the classifier. Two web sessions fetched `researcher_profile.md` and `personal_info.md` side by side; both went through. Ruled out.
- Whether Project Instructions carry the user's authority. Two wordings, four fresh sessions; see the table below. They do not, reliably.
- Whether in-chat authorization does. One session, blocked twice without it and approved twice with it.
- Asking for push later, at the point it is needed (Dan's idea). One session: startup reads approved, deferred push succeeded.

## Evidence

Add-repository requests at session start, without any in-chat authorization (all runs 2026-10-10, Dan's `dotfiles` Project, opus-5.5 web sessions):

| Run | Project Instructions | Read `claude_research_config` | Push `dotfiles` |
|---|---|---|---|
| 1 | bare first-person "I authorize…" | approved | blocked [Permission Grant] |
| 2 | bare first-person "I authorize…" | blocked [Permission Grant] | blocked [Permission Grant] |
| 3 | framing (what claude_researcher is, one repo per Project, connecting is my instruction) | approved | approved |
| 4 | framing, fresh session | approved | blocked [Permission Grant] |
| 2, after Dan typed an authorization in chat | (same) | approved | approved |
| 5 | read-only at startup, push deferred | approved (both repos, read) | requested at first commit: "already attached"; `git push` succeeded |

Other blocks seen:

- Original incident: the fetch of `personal_info.md` at startup, described by the agent as "personal-data handling" (exact text not captured).
- Run 1: the sandbox-type check in RESEARCHER.md (reads `IS_SANDBOX` and `GITHUB_TOKEN`): [Auto-Mode Bypass].
- Separate web test: an unrequested hash comparison of the two config files: [Third-Party Attack].
- This CLI session: copying `personal_info.md` to a new name in `claude_research_config`: [Sensitive-Source Provenance]. Dan ran the copy himself.
- Run 5: a batch closing five dotfiles issues Dan had not asked to close: [External System Writes]. The same session had already re-dated and commented on dotfiles #77 unasked; that write went through.

## Decisions Made

- **Switch fully to the proxy sandbox.** Remove the token path everywhere (Dan: "Anthropic changed this for everyone").
- **Startup asks for read only; push at the first commit.** Install the push hook only after the first push succeeds. If a check refuses a step, show the denial text and ask in chat; never keep making commits that cannot be pushed.
- **Issue and PR writes only when the user asked for them.**
- **Keep `personal_info.md`.** The rename was ruled out as a cause; the test copies `researcher_profile.md` and `researcher_config.md` in Dan's config repo are to be deleted.
- **Trim the Project Instructions.** Keep the workflow framing (what claude_researcher is, one repo per Project) for the agent's understanding; drop the token and the authorization wording.
- **The git-log identity inference** from the original incident: Dan judged it fine for his repos. No template change for it in this plan.

## Open Questions

- The classifier's behaviour is not deterministic: identical requests were approved in one session and refused in another. Six runs is a small sample.
- Whether a read-level attachment always permits push, or run 5's "already attached" was incidental. The template should not depend on it either way.
- Whether the proxy lets a session create repos (BOOTSTRAP Step 6) and whether the egress configuration in BOOTSTRAP Step 1 still applies on the proxy sandbox. Both untested.

## Artifacts

- Plan: `docs/plans/14_proxy_only.md`
- Issue: #72
- Test copies (to delete): `danparshall/claude_research_config` commits `6fb03c4` (`researcher_profile.md`) and `912c28c` (`researcher_config.md`)
- Run 5's own convo: `danparshall/dotfiles` `docs/convos/20261010_outstanding_triage.md` (commits `ea71f8a`, `8192e30`)
