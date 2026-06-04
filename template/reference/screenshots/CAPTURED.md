# Screenshot capture log

One row per screenshot in this directory. Update the date + variant when re-capturing.

| File | Captured | UI variant |
|------|----------|------------|
| `claude_egress_settings.png` | 2026-06-04 | claude.ai Pro account, Capabilities pane — "Allow network egress" toggle on, "Domain allowlist: All domains" with confirmation banner *"Claude can access all domains on the internet."* |
| `github_pat_create_form.png` | 2026-06-04 | github.com fine-grained PAT create form, top portion: token name, resource owner, expiration (90 days), beginning of Repository access |
| `github_pat_add_permissions.png` | 2026-06-04 | github.com PAT Permissions section, Add-permissions picker open with "cont" search filter (Contents visible to add); Administration already added |
| `github_pat_read_write_flip.png` | 2026-06-04 | github.com PAT page with Administration (Read and write), Contents (Read and write), Metadata (Read-only, Required) — the desired final configuration |

## Why this file

The claude.ai egress UI and the GitHub PAT UI have both changed multiple times in recent months (claude.ai per PR [#8](https://github.com/danparshall/claude_researcher/pull/8) history, GitHub historically). Screenshots inevitably go stale. This log records what was captured and when, so the next person updating them knows what to re-capture and against which UI variant.

## When to re-capture

- The Step the screenshot illustrates no longer matches the UI a fresh user sees.
- An agent or user reports the screenshot looks different from what they're seeing.
- A major redesign of either surface (claude.ai Settings, GitHub Settings) is publicly announced.

After re-capturing, update the row's `Captured` date and `UI variant` note above. Keep the filename stable so `template/BOOTSTRAP.md`'s inline image references don't have to change.
