# Screenshot capture log

One row per screenshot in this directory. Update the date + variant when re-capturing.

| File | Captured | UI variant |
|------|----------|------------|
| `claude_egress_settings.png` | 2026-10-13 | claude.ai Pro account, Settings → Capabilities — "Allow network egress" on, domain allowlist "All domains". Some text is highlighted from a selection. |
| `claude_connectors_github.png` | 2026-10-13 | claude.ai Settings → Connectors — GitHub Integration showing a checkmark as connected. |
| `github_new_repo_private.png` | 2026-10-13 | github.com/new — visibility menu open with Private highlighted. |
| `github_app_repo_access.png` | 2026-10-13 | The installed Claude GitHub App's configure page: its permissions, and Repository access offering both "All repositories" and "Only select repositories". |
| `claude_permission_mode_auto.png` | 2026-10-13 | claude.ai chat box with the permission-mode menu open and Auto selected. |

`github_pat_read_write_flip.png` was retired 2026-10-10 (plan 14, proxy-only) and deleted 2026-10-15; it is in git history if ever needed.

## Why this file

The claude.ai settings UI and GitHub's UI have both changed multiple times. Screenshots inevitably go stale. This log records what was captured and when, so the next person updating them knows what to re-capture and against which UI variant.

## Where these are used

All five are shown in `README.md` (`## Quick start` → "Setup at a glance") and, as copies, on clauderesearch.ai (`site-claude-researcher/images/`). Re-capture both places together. They are **not** referenced from `template/BOOTSTRAP.md`: the agent reads BOOTSTRAP as markdown source and can't show images to the user.

## When to re-capture

- The Step the screenshot illustrates no longer matches the UI a fresh user sees.
- A user reports the screenshot looks different from what they're seeing.
- A major redesign of either surface (claude.ai Settings, GitHub Settings) is publicly announced.

After re-capturing, update the row's `Captured` date and `UI variant` note above. Keep the filename stable so `README.md`'s image references don't have to change.
