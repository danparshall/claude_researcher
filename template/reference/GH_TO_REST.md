# `gh` → REST in the claude.ai sandbox

Skills are written with `gh` commands for the CLI. In the claude.ai sandbox, GraphQL is blocked, and most `gh` subcommands use it: `gh issue list`, `gh issue create`, `gh issue edit`, `gh pr list`, `gh label list` and `gh repo view` all fail with "GraphQL is not available" (verified 2026-10-07). Assume the same for every other `gh issue …` and `gh pr …`. `gh api <REST path>` works, as does `curl` against `api.github.com`.

The rules in RESEARCHER.md §2.0c ("REST through the proxy") apply to every row: only `repos/{owner}/{repo}/...` paths on attached repos, no `Authorization` header, and `-H "Content-Type: application/json"` on every `POST`, `PATCH` and `PUT`. Writes happen only when the user asked for them (§2.0c "Permission checks").

| Skill says | In the sandbox |
| --- | --- |
| `gh api user --jq .login` | `${USERNAME}` from Project Instructions (`/user` is not a repository-scoped path) |
| `gh repo view --json nameWithOwner` | `${USERNAME}/${REPO}` from Project Instructions |
| `gh issue list --label task --state open` | `GET /repos/{owner}/{repo}/issues?state=open&labels=task&per_page=100`, then drop entries that have a `pull_request` key. If 100 come back, fetch `&page=2` and so on. |
| `gh search issues --owner …` (`task-triage`) | No equivalent: the search API is refused ("sessions are bound to their configured repositories"). List issues repo by repo for the attached repos, and tell the user the cross-repo view is limited to those. |
| `gh issue create` | `POST /repos/{owner}/{repo}/issues` with `{"title", "body", "labels"}` |
| `gh issue edit <N> --title …` | `PATCH /repos/{owner}/{repo}/issues/<N>` with `{"title"}` |
| `gh issue close <N> --comment …` | `POST …/issues/<N>/comments` with `{"body"}`, then `PATCH …/issues/<N>` with `{"state": "closed"}` |
| `gh label list … \| grep -qx task` / `gh label create` | `GET /repos/{owner}/{repo}/labels/task` (200 = exists, 404 = missing) / `POST /repos/{owner}/{repo}/labels` with `{"name", "description"}` |
| `gh pr create` | `POST /repos/{owner}/{repo}/pulls` with `{"title", "head", "base", "body"}` |
| `gh pr view <N>` | `GET /repos/{owner}/{repo}/pulls/<N>` |
| `gh pr checks` | `GET /repos/{owner}/{repo}/commits/<sha>/check-runs` |
| `gh pr merge <N>` | `PUT /repos/{owner}/{repo}/pulls/<N>/merge` with `{"merge_method"}` |

Issue listing, creation and editing, the label lookup, the search refusal, and PR create, view, checks and merge were exercised in the sandbox on 2026-10-07. The comment, close and label-create rows are the standard REST calls but had not yet been run there when this was written.
