# RESEARCH_LOG

Sessions with no research line, newest first. Line sessions log in `docs/active/<line>/RESEARCH_LOG.md`.

- 2026-10-10: [Dan (pro, dotfiles, 20261010T1201, opus-5.5)] Six web test sessions showed the auto-mode classifier refuses startup push requests whatever Project Instructions say, while read-at-startup plus push-at-first-commit went through; the `personal_info.md` filename was ruled out as a cause. Plan 14 removes the token path and adopts that access design (branch `proxy-only`, issue #72). — docs/convos/20261010_proxy_only_cutover.md

- 2026-10-07: [Dan (web, claude_researcher, 20261007T0753, fable-5.1)] The web sandbox now routes GitHub through Anthropic's proxy, which refuses pushes made with a pasted PAT; after connecting GitHub, installing the Claude GitHub App and approving repos per session, the workflow runs token-free, and RESEARCHER.md + resolve-runtime-issue now support both sandboxes (branch `sandbox-proxy-migration`, issue #72). — docs/convos/20261007_sandbox_proxy_migration.md
- 2026-10-04: [Dan (air, claude_researcher, 20261004T1750, opus-5.5)] Uploaded researcher@1.0.28 (all 19 customs bundled, verified via an anonymous package download), made the upload checklist agent-runnable, and closed dotfiles #96. Changes in dotfiles. — docs/convos/20261004_registry_upload_1.0.28.md
