---
name: github-api-workflow
description: "The repo-access authority: how a session reads, writes, branches, and merges the repo in each working environment. Read the environment branch first — a local clone with working git push (Cowork) uses plain git and gh; a claude.ai web session (git push blocked by the egress proxy) uses the GitHub REST API recipes: Contents API for single-file work, Trees API for atomic multi-file commits, branch recipes, and safety rules against silent data loss. Also owns the parallel-session and mixed-environment coordination convention (session-boundary hygiene; the collision surface is tracking machinery). Other skills point here for commit and branch mechanics instead of carrying their own."
triggers: >-
  At the start of any session that will commit, and whenever commit, branch or merge mechanics
  are needed; the repo-access authority for both environments
---

# GitHub API Workflow — the repo-access authority

One skill that says how a session reads, writes, branches, and merges the repo in each working environment. Every other skill that needs commit or branch mechanics points here instead of carrying its own; which mechanics apply depends on the environment branch below, so take the branch first.

## The environment branch (read first)

Two environments, one test at session start:

- **Cowork (local clone).** The repo is a local working copy (e.g. a folder of clones on the user's machine) with a shell and working `git push`. → Use **plain git and `gh`** — see the next section. The API recipes further down are not for this environment, but the *disciplines* they encode (one logical change = one commit, verify after write, rename-reference completeness, parallel-session hygiene) bind here identically.
- **claude.ai web.** The repo is visible through an access token/connector and `git clone`/`git push` is blocked (the egress proxy rejects CONNECT tunnels). → Use the **GitHub REST API recipes** that make up the rest of this skill — the web branch.

If unsure, the test is mechanical: run `git status` in the repo. A working tree that answers means Cowork; no shell or no working tree means the web branch.

## Cowork: plain git and gh

Ordinary git covers everything the web branch's recipes exist to reconstruct:

| Need | Web branch (API) | Cowork |
|---|---|---|
| Read a file / list a directory | `gh_read` / `gh_list` | the filesystem |
| Single-file commit | Contents API (`gh_put`) | `git add` + `git commit` + `git push` |
| Atomic multi-file commit | Trees API (`gh_atomic_commit`) | one `git commit` covering the whole batch |
| Move / rename | `gh_move` (verify-before-delete) | `git mv`, in the same commit as the reference rewrites |
| Branch create / delete | `gh_create_branch` / `gh_delete_branch` | `git branch` / `git push origin -d` |
| Read on a branch without checkout | `gh_read(path, ref=branch)` | `git show <branch>:<path>` |
| Merge | `gh_merge` | `git merge` |
| Recover an old version | `gh_read(path, ref=sha)` | `git show <sha>:<path>` |

GitHub-side operations beyond git (issues, releases, repo metadata) go through `gh`. What carries over from the web branch unchanged, because it is discipline rather than transport:

- **One logical change is one commit.** A multi-file batch that must land together goes in a single `git commit` — atomicity is free here; do not fragment it into per-file commits.
- **A rename is not complete until references are rewritten** — the whole section below applies verbatim; only the mechanics (`git mv` + `grep`) differ.
- **GitHub is the single source of truth.** Sync at session start, push at session close — the full rule is in **Parallel sessions and mixed environments**, next.
- **Never force-push, never resolve a conflict silently.** A rejected push or a merge conflict stops the work and goes to the user.

## Parallel sessions and mixed environments

Live coordination between parallel sessions is impossible — a web session and a Cowork session cannot see each other mid-flight, and two web sessions cannot either. The convention is **session-boundary hygiene**, which keeps the overlap windows small:

- **Web sessions:** the concurrency discipline of the web branch — re-read shared files immediately before building each blob, guard the head SHA, verify after committing. Codified in **Concurrency — atomicity is not isolation** below.
- **Cowork sessions:** sync at session start (fetch, and pull if cleanly behind, before working); commit **and push** at close — unpushed local commits are invisible to every other session and to GitHub as the source of truth, so leaving them overnight recreates the very hazard this convention exists to close. A rejected push means another session landed first: stop, surface the conflict to the user, never force-push.
- **Mixed web + Cowork:** the two rules above are the whole mechanism; there is no third rule, because no channel exists for one.

**What actually collides.** Parallel sessions on one repo take two shapes — fully independent tasks, or steps of a workstream plan — and in both shapes the *content* surfaces are divided by construction (different artifacts, or a plan's scoped steps). The collision zone is the shared **tracking machinery**: `STATUS.md`, `workdesk/INDEX.md`, `<KIT_FOLDER>/CHANGELOG.md`, the indexes and `FOLDER_MAP`s, and the plan file itself (position lines, report logs). That is why the at-risk file list in the concurrency section reads the way it does. Treat machinery files with the re-read-immediately-before-write rule at close-out in both environments — on Cowork: pull, re-apply the update to the current content, then push. **One session per clone, one task per session**: two sessions in one clone share the index, HEAD and the working tree, so a landing commit stages explicit paths only and never `git add -A`, close-outs run one at a time, and a second task in an active clone gets its own session or waits.

The machinery-only guarantee is earned, not free: it holds because the division of work is respected. Don't point two sessions at the same artifacts; the plan's step table or an explicit task split is what makes parallel sessions safe.

**Parallel people (repos with a collaborator on the roster — `structure_conventions.md`, "Collaborators").** A collaborator works from their own clone, so the shared-clone hazards above (shared index, HEAD, working tree) do not arise between people; what remains is ordinary merge conflict on the files two people both write. The convention keeps that surface small. A collaborator writes directly on `main` only inside `workdesk/collaborators/<id>/` (their `INDEX.md` and `LOG.md`); everything else goes on a `<id>_br_<topic>-<date>` branch and reaches `main` through a pull request (`gh pr create --base main --head <branch> --title ... --body ...` at Cowork; the Pulls API on web), merged by the owner or, for a `merge: self` collaborator, by themselves inside their territory. `STATUS.md` is the one shared tracker collaborators edit, in two short entries carried by the pull request; the header paragraph is the owner's, which is what keeps two open pull requests off the same lines. The division of work is declared, not inferred: each collaborator's *Working on* block names their territory, and the owner's sessions read the blocks before a bulk move or an edit inside one — a claim, not a lock. The re-read-immediately-before-write rule applies to the collaborator files exactly as to the other machinery: both sides append to the same `INDEX.md`, so pull before writing a row and push right after.

---

## The web branch — the GitHub REST API

Everything from here down is the **web branch**: repository operations via the GitHub REST API, for sessions where git push is blocked. The workflow is built around the Contents API and uses Python's standard library (`urllib`) as the primary client. Shell + curl is documented as a fallback for trivial operations only. Typical uses:

- Reading or writing individual files in a known repository.
- Moving or renaming files (the API has no native rename — must be copy then delete).
- Bulk operations (e.g., renaming many files, restructuring folders) where reliability matters.

## Contents API vs Trees API: which to use

The GitHub REST API offers two paths for writing to a repo, and the right choice depends on whether the operation touches one file or many.

**Use the Contents API (`/repos/.../contents/{path}`) when:**
- You're editing, creating, or deleting a single file.
- You're moving or renaming a single file (use `gh_move` below — verify-before-delete is mandatory).
- The operation is naturally one file at a time and partial state across files isn't a concern.

This is the default for most content-repo session work — drafting an email file, updating one skill, replacing one figure. The Contents API is simpler, fewer concepts, and one call does the whole job.

**Use the Trees API (`/repos/.../git/blobs`, `/git/trees`, `/git/commits`, `/git/refs`) when:**
- You're changing more than one file in a logically-coupled batch — e.g., renaming many files at once, restructuring a folder, applying a multi-file consolidation, or any update where some files reference others.
- Partial success would leave the repo in a broken state (file A references file B; if A lands but B's rename doesn't, the repo is internally inconsistent).
- You want one clean commit in history rather than 25 commits each describing a partial step.

The Trees API gives you **atomicity for free**: you upload all the file contents as blobs, build one tree describing the desired repo state, create one commit pointing at it, and update the branch ref. Any failure before the ref update leaves the repo unchanged. There is no half-applied state to clean up.

The Trees API is also what prevents the silent-corruption failure mode the Contents API is vulnerable to: there is no separate-write-then-delete sequence to fail between, because the entire change is described in one tree object before the commit ever happens.

### Quick decision rule

- **One file** → Contents API.
- **More than one file, and they should land together** → Trees API.
- **Bulk operations of any kind** → Trees API.

The cost of getting this wrong falls asymmetrically: using the Trees API for a single-file change is a few extra lines of code. Using the Contents API for a multi-file batch is how you lose data. When in doubt, prefer the Trees API.

## Prerequisites

The calling project should provide:
- `TOKEN` — a GitHub personal access token (fine-grained, with Contents read/write on the repo).
- `REPO` — the repository in `owner/name` form (e.g., `your-username/your-repo`).
- `USERNAME` — the GitHub username for commit attribution.

**Cross-repo reads.** The read helpers (`gh_get` / `gh_list` / `gh_read`) resolve the repository from the `REPO` global, so reading from a *second* repo just means pointing `REPO` at that repo's `owner/name` with the token scoped to both repos. This is read-only: writes (`gh_put` / `gh_delete` / the Trees-API recipes) always target the home repo. No kit workflow uses this from the web branch anymore — cross-repo work (including `cross_repo_import_skill.md`) is Cowork-only, reading local clones — but the capability stands documented for ad-hoc cross-repo reads the user explicitly authorizes.

## Core Principle: Use Python, Not Shell

Shell + `curl` works for reading and for trivially-sized writes, but breaks silently when:
- The file is binary (images, PDFs, .docx).
- The base64-encoded content exceeds shell argument-length limits (typically files larger than a few hundred KB).
- The commit message contains apostrophes, quotes, or backticks that conflict with shell-interpolated payloads.

**Use Python `urllib.request` for any non-trivial operation.** It handles binary content, arbitrary message strings, and provides reliable error visibility. The Python recipes below are the canonical implementations.

## Python Recipes

The following functions are the recommended building blocks. Copy them into a single Python file in the working session.

**Reads.** Read `main` through `?ref=<head sha>` (resolve the head first) or the Trees API by default — a bare Contents read can return a stale copy hours after a commit landed.

```python
import json, urllib.request, base64

TOKEN = "..."           # set from project context
REPO = "owner/name"     # set from project context
USERNAME = "username"   # set from project context

def gh_get(path, ref=None):
    """Get file metadata and content. Returns dict or None if 404."""
    url = f'https://api.github.com/repos/{REPO}/contents/{urllib.request.quote(path)}'
    if ref:
        url += f'?ref={ref}'
    req = urllib.request.Request(url, headers={'Authorization': f'token {TOKEN}'})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError:
        return None

def gh_list(path):
    """List a directory. Returns list of items or None if path doesn't exist or isn't a dir."""
    data = gh_get(path)
    return data if isinstance(data, list) else None

def gh_read(path, ref=None):
    """Read file content as bytes.
    Uses the blob API (`/git/blobs/{sha}`), not the Contents API, because
    the Contents API silently truncates files larger than ~1 MB — it returns
    metadata (sha, size) but the `content` field is empty or partial. Routing
    all reads through the blob API costs one extra round trip per call but
    works uniformly for any file size and avoids zero-byte corruption."""
    meta = gh_get(path, ref=ref)
    if not meta or 'sha' not in meta:
        return None
    url = f'https://api.github.com/repos/{REPO}/git/blobs/{meta["sha"]}'
    req = urllib.request.Request(url, headers={'Authorization': f'token {TOKEN}'})
    try:
        with urllib.request.urlopen(req) as r:
            data = json.load(r)
        return base64.b64decode(data['content'])
    except urllib.error.HTTPError:
        return None

def gh_put(repo_path, content_bytes, msg):
    """Create or update a file. Returns True on success, False on failure.
    Always re-fetches the sha immediately before write to avoid stale-sha conflicts."""
    existing = gh_get(repo_path)
    payload = {
        'message': msg,
        'committer': {'name': USERNAME, 'email': f'{USERNAME}@users.noreply.github.com'},
        'content': base64.b64encode(content_bytes).decode()
    }
    if existing and 'sha' in existing:
        payload['sha'] = existing['sha']
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}/contents/{urllib.request.quote(repo_path)}',
        data=json.dumps(payload).encode(),
        method='PUT',
        headers={'Authorization': f'token {TOKEN}', 'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as r:
            return True
    except urllib.error.HTTPError as e:
        print(f"PUT FAILED ({repo_path}): {e.read().decode()[:300]}")
        return False

def gh_delete(path, msg):
    """Delete a file. Returns True on success, False on failure."""
    existing = gh_get(path)
    if not existing or 'sha' not in existing:
        return False  # already gone
    payload = {
        'message': msg,
        'committer': {'name': USERNAME, 'email': f'{USERNAME}@users.noreply.github.com'},
        'sha': existing['sha']
    }
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}/contents/{urllib.request.quote(path)}',
        data=json.dumps(payload).encode(),
        method='DELETE',
        headers={'Authorization': f'token {TOKEN}', 'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as r:
            return True
    except urllib.error.HTTPError as e:
        print(f"DELETE FAILED ({path}): {e.read().decode()[:300]}")
        return False
```

## Move / Rename — single file (Contents API)

For a **single** file move or rename, the Contents API path below is the right tool. For **multiple** files, skip this section and use the Trees API recipe further down — it gives you atomicity and avoids the silent-corruption failure mode this section's safety check exists to catch.

**The GitHub Contents API has no rename or move operation.** Moving a file means: read the source content, write it to the destination, then delete the source. Each step can fail independently, and **the most dangerous failure mode is silent corruption: the destination ends up created at zero bytes (or with corrupted content) but the success-detection logic doesn't catch it, so the source gets deleted, and the file's content is lost.**

To prevent this, every single-file move via the Contents API MUST verify the destination's size before deleting the source. Treat this as non-negotiable.

```python
def gh_move(src_path, dst_path, msg):
    """Move (rename) a file safely.
    Reads source, writes destination, VERIFIES destination size matches source size,
    only then deletes the source. Returns True on full success."""

    # 1. Read source — gh_read goes through the blob API and works for any size.
    #    Fetch metadata separately so we have authoritative size for the safety check.
    src_meta = gh_get(src_path)
    if not src_meta or 'size' not in src_meta:
        print(f"MOVE FAILED: source not found: {src_path}")
        return False
    src_size = src_meta['size']
    content_bytes = gh_read(src_path)
    if content_bytes is None or len(content_bytes) != src_size:
        got = len(content_bytes) if content_bytes is not None else 0
        print(f"MOVE FAILED: read size mismatch (got {got}, expected {src_size}): {src_path}")
        return False

    # 2. Write destination
    if not gh_put(dst_path, content_bytes, msg):
        print(f"MOVE FAILED: could not write destination: {dst_path}")
        return False

    # 3. VERIFY destination size — this is the safety check
    dst_data = gh_get(dst_path)
    dst_size = dst_data.get('size', 0) if dst_data else 0
    if dst_size != src_size:
        print(f"MOVE ABORTED: size mismatch at destination "
              f"(src={src_size}, dst={dst_size}). Source NOT deleted: {src_path}")
        return False

    # 4. Only now is it safe to delete the source
    if not gh_delete(src_path, f"{msg} (delete original)"):
        print(f"MOVE PARTIAL: destination written and verified, "
              f"but source delete failed: {src_path}")
        return False

    return True
```

**Rules for single-file moves:**
1. **Verify size before deleting.** No exceptions. If the destination size doesn't match the source size, abort and leave the source intact. The user can retry or investigate.
2. **Never trust the success message of a put without re-fetching.** A `PUT` returning HTTP 200 is not proof the file was correctly written. Re-fetching size is.
3. **Each step is independent.** If `gh_put` succeeds but verification fails, the destination exists at the wrong size. Either delete the bad destination and retry, or surface it to the user.
4. **For more than one file, do not loop `gh_move`.** Use the Trees API recipe below — it commits all the moves atomically in one operation, so there is no half-applied state to clean up if anything goes wrong.

## Multi-file changes — use the Trees API

When a single logical operation spans more than one file — renaming a batch, restructuring folders, applying a coordinated update where files reference each other — use the Git Trees API. It commits all the changes atomically: either every file lands at its new state in one commit, or nothing changes. There is no partial state to recover from.

### Why this is safer than looping the Contents API

The Contents API processes one file at a time, with each PUT or DELETE being its own commit. A 25-file batch becomes 25-50 commits, each of which can succeed or fail independently. If any of them fail (or worse, silently corrupt as in the Move/Rename pattern), the repo ends up in a half-applied state and you have to figure out which files got through before you can recover.

The Trees API inverts this. You upload the file contents as blobs (each upload is independent and stateless — no SHA-juggling), then describe the entire desired repo state as a single tree object, then create a single commit pointing at that tree, then update the branch ref to point at the commit. Until the ref update succeeds, the repo is unchanged. After it succeeds, every file in the batch is at its new state in one atomic commit.

There is no separate-write-then-delete sequence for the Trees API to corrupt — additions, modifications, and deletions are all expressed as differences between the new tree and the parent tree, evaluated together at commit time.

### The four-step pattern

1. **Upload each new or modified file's content as a blob.** This returns a SHA for each blob.
2. **Build a tree object** that lists every file in the repo's new state. For unchanged files, reference their existing SHAs (read from the parent tree); for changed files, reference the new blob SHAs from step 1; for deleted files, omit them; for renames, use the new path with the same blob SHA as the old path.
3. **Create a commit** with the new tree's SHA as its tree, the current branch HEAD as its parent, and a commit message describing the whole batch.
4. **Update the branch ref** to point at the new commit. This is the atomic moment — before this call, the repo is unchanged.

### Recipe — atomic multi-file commit

```python
def gh_get_branch_head(branch="main"):
    """Get the current commit SHA of a branch."""
    url = f'https://api.github.com/repos/{REPO}/git/refs/heads/{branch}'
    req = urllib.request.Request(url, headers={'Authorization': f'token {TOKEN}'})
    with urllib.request.urlopen(req) as r:
        return json.load(r)['object']['sha']

def gh_get_commit_tree(commit_sha):
    """Get the tree SHA from a commit."""
    url = f'https://api.github.com/repos/{REPO}/git/commits/{commit_sha}'
    req = urllib.request.Request(url, headers={'Authorization': f'token {TOKEN}'})
    with urllib.request.urlopen(req) as r:
        return json.load(r)['tree']['sha']

def gh_create_blob(content_bytes):
    """Upload content as a blob; return its SHA."""
    payload = {
        'content': base64.b64encode(content_bytes).decode(),
        'encoding': 'base64'
    }
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}/git/blobs',
        data=json.dumps(payload).encode(),
        method='POST',
        headers={'Authorization': f'token {TOKEN}', 'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)['sha']

def gh_create_tree(base_tree_sha, changes):
    """Build a new tree as a delta against base_tree_sha.
    `changes` is a list of dicts:
      - To add or modify a file: {'path': 'foo/bar.md', 'mode': '100644', 'type': 'blob', 'sha': blob_sha}
      - To delete a file:        {'path': 'foo/bar.md', 'mode': '100644', 'type': 'blob', 'sha': None}
      - To rename a file:        delete old path AND add new path with same blob_sha
    Unchanged files do not need to be listed — they're inherited from base_tree_sha.
    """
    payload = {'base_tree': base_tree_sha, 'tree': changes}
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}/git/trees',
        data=json.dumps(payload).encode(),
        method='POST',
        headers={'Authorization': f'token {TOKEN}', 'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)['sha']

def gh_create_commit(tree_sha, parent_sha, msg):
    """Create a commit object referencing the tree."""
    payload = {
        'message': msg,
        'tree': tree_sha,
        'parents': [parent_sha],
        'author': {'name': USERNAME, 'email': f'{USERNAME}@users.noreply.github.com'},
        'committer': {'name': USERNAME, 'email': f'{USERNAME}@users.noreply.github.com'}
    }
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}/git/commits',
        data=json.dumps(payload).encode(),
        method='POST',
        headers={'Authorization': f'token {TOKEN}', 'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)['sha']

def gh_update_ref(commit_sha, branch="main"):
    """Atomically advance the branch ref to point at commit_sha.
    This is the moment of truth — before this call succeeds, the repo is unchanged."""
    payload = {'sha': commit_sha, 'force': False}
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}/git/refs/heads/{branch}',
        data=json.dumps(payload).encode(),
        method='PATCH',
        headers={'Authorization': f'token {TOKEN}', 'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as r:
            return True
    except urllib.error.HTTPError as e:
        print(f"REF UPDATE FAILED: {e.read().decode()[:300]}")
        return False

def gh_atomic_commit(file_changes, msg, branch="main"):
    """Apply a batch of file changes as one atomic commit.
    `file_changes` is a list of dicts:
      - {'path': 'foo.md', 'content': b'...'}              → add or update
      - {'path': 'foo.md', 'delete': True}                 → delete
      - {'path': 'old.md', 'rename_to': 'new.md',
         'content': b'...'}                                → rename (and optionally edit)
    Returns the new commit SHA on success, None on failure."""
    head_sha = gh_get_branch_head(branch)
    base_tree_sha = gh_get_commit_tree(head_sha)
    tree_changes = []
    for fc in file_changes:
        if fc.get('delete'):
            tree_changes.append({'path': fc['path'], 'mode': '100644',
                                 'type': 'blob', 'sha': None})
        elif fc.get('rename_to'):
            # Delete old path, add new path with new content (or copied content)
            tree_changes.append({'path': fc['path'], 'mode': '100644',
                                 'type': 'blob', 'sha': None})
            blob_sha = gh_create_blob(fc['content'])
            tree_changes.append({'path': fc['rename_to'], 'mode': '100644',
                                 'type': 'blob', 'sha': blob_sha})
        else:
            blob_sha = gh_create_blob(fc['content'])
            tree_changes.append({'path': fc['path'], 'mode': '100644',
                                 'type': 'blob', 'sha': blob_sha})
    new_tree_sha = gh_create_tree(base_tree_sha, tree_changes)
    new_commit_sha = gh_create_commit(new_tree_sha, head_sha, msg)
    if gh_update_ref(new_commit_sha, branch):
        return new_commit_sha
    return None
```

### Worked example — rename 25 files in one commit

```python
# Read all 25 sources
files = [{'old': f'old/file_{i}.md', 'new': f'new/file_{i}.md'} for i in range(25)]
changes = []
for f in files:
    content = gh_read(f['old'])
    if content is None:
        raise SystemExit(f"Could not read {f['old']} — aborting before any commit.")
    changes.append({'path': f['old'], 'rename_to': f['new'], 'content': content})

# One atomic commit. Either all 25 renames land or none do.
new_sha = gh_atomic_commit(changes, "Restructure: rename 25 files from old/ to new/")
if new_sha:
    print(f"Done. Commit: {new_sha}")
else:
    print("Commit failed; repo unchanged.")
```

If any individual blob upload, tree creation, or commit creation fails, the function raises before the ref update — and since the ref update is the only step that changes the repo, the repo is unchanged. No half-applied renames, no recovery needed.

### Notes on the Trees API

- **The blob upload step is per-file, but stateless.** No SHA-juggling between writes; each blob upload is independent. If one fails, retry it; nothing has been committed yet.
- **`base_tree` lets you express only the delta.** You don't have to list every unchanged file in the new tree — just the changes. The API inherits the rest from `base_tree`.
- **Renames are expressed as delete-old + add-new with the same blob SHA.** No content needs to be re-uploaded for a pure rename — Git's content-addressed storage means the new tree just points at the same blob under a new path.
- **Mode `100644`** is for regular files. For directories (`040000`), symlinks (`120000`), or executables (`100755`), see GitHub's Git Trees API docs.
- **`force: false` on the ref update** is the safe default — it prevents the update if HEAD has moved since you started. If you actually want to overwrite a divergent state (rare), set `force: true` deliberately.

### Concurrency — atomicity is not isolation

**`base_tree` protects only the paths your tree does *not* list.** For any path you *do* list, your blob replaces whatever is at that path in the parent commit — wholesale, with no merge and no conflict. So a Trees-API commit is atomic against *itself* and defenceless against *anyone else*. If another session committed to a file between the moment you read it and the moment you build its blob, your commit silently reverts their change. The ref update succeeds, the commit looks clean, and nothing in the API response tells you anything was lost.

This is the same hazard the Contents API has, and the Trees API does **not** fix it — a dangerous thing to get wrong, because the Trees API is otherwise the safer tool and it is easy to read "atomic" as "safe." Atomic means all-or-nothing across *your* files. It says nothing about other writers.

**The rule: for every shared file, re-read it immediately before building its blob** — not at the start of the session, not when you began drafting the edit. Then apply your edit to *that* content. Files at risk are the ones many sessions touch: the root indexes, `FOLDER_MAP.md`, `STATUS.md`, changelogs, the workdesk queue.

```python
# WRONG — content read minutes ago, edited in the meantime by another session
content = my_edited_copy_from_earlier
sha = gh_create_blob(content.encode())

# RIGHT — re-read, then re-apply the edit to current content
current = gh_read('MATERIALS_INDEX.md')          # live, seconds before the write
content  = apply_my_edit(current.decode())        # anchor-based insert, not a whole-file overwrite
sha = gh_create_blob(content.encode())
```

Two supporting habits:

- **Guard the ref update.** Capture the head SHA at the start of the batch and re-check it immediately before `PATCH`ing the ref. If it moved, another session committed while you worked: stop, re-read the shared files, rebuild. `force: false` is the API-side version of the same guard.
- **Verify after committing, not just before.** Re-read the shared files and confirm *both* your additions and the other session's are present. A commit that reports success is not evidence that nothing was lost — the only evidence is reading the result.

**If you do clobber something,** the fix is additive, not a revert: read the pre-clobber version at the overwritten commit's SHA (`gh_read(path, ref=<sha>)`), re-apply your edit on top of it, and commit the union. Never `revert` your own commit to recover theirs — that discards yours in exchange. And say so plainly: a silent overwrite that gets silently repaired teaches nobody, and this hazard recurs.

Session-boundary hygiene for parallel and mixed-environment sessions — including the Cowork side of this same hazard — is codified in **Parallel sessions and mixed environments**, near the top of this file.

### Renaming is not complete until references are rewritten

A rename or move re-points a blob to a new path; because Git storage is content-addressed, **nothing inside any file changes automatically**. The mechanical move is the easy half. A rename pass is only complete once the *references* are rewritten too, in two places that are easy to half-do:

1. **Files that point at the moved file** — the obvious case.
2. **The moved files themselves** — old-path and old-*name* references in their own body survive the move untouched. Migrating `A/` → `B/` must rewrite `A/`-references *inside the moved files*, not only in files that point at them. (This is the internal-reference lesson: a blob-move carries no content edits.)

When grepping for what to rewrite, match **all the forms the reference takes**, or you will miss some:

- **Both path shapes** — trailing-slash (`inputs/X/`) *and* bare (`inputs/X`). A sweep keyed on one misses prose mentions in the other.
- **Path *and* bare name** — renaming `AboutFolder.md` → `FOLDER_MAP.md` leaves stale `AboutFolder` *name* mentions in prose that a path-only sweep skips.

Done right, every reference to the old path/name resolves to the new one afterward; a surviving old-name mention is the bug — the same reference-resolution check Tier 1 runs after a redesign.


## Branches — create, read by ref, merge, delete

On the web branch git push is blocked, so branch work goes through the API,
not through `git`. The read helpers already take a `ref`; these recipes add the
create / merge / delete primitives. Both `writing_branch_skill.md` and
`exploration_branch_skill.md` call them (at Cowork, via the plain-git
equivalents in the mapping table above).

```python
def gh_create_branch(branch, from_branch="main"):
    """Create a new branch ref at from_branch's current HEAD. True on success."""
    head = gh_get_branch_head(from_branch)   # the Trees-API helper above
    if not head:
        print(f"BRANCH FAILED: source branch not found: {from_branch}")
        return False
    body = json.dumps({"ref": f"refs/heads/{branch}", "sha": head}).encode()
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}/git/refs',
        data=body, method='POST',
        headers={'Authorization': f'token {TOKEN}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status in (200, 201)
    except urllib.error.HTTPError as e:
        print(f"BRANCH FAILED ({e.code}): {branch} — already exists?")
        return False

def gh_merge(head, base="main", msg="merge"):
    """Merge head into base via the merges API. Returns the merge commit dict,
    None on conflict (409) / nothing-to-merge (204) / error.
    A clean writing-branch merge, or a held/null/additive exploration merge,
    uses this. An OVERTURNING exploration merge does NOT — see
    exploration_branch_skill.md: stage via gh_read(path, ref=branch) into
    workspace/staging/ instead, because a git-merge lands both the old and the
    new claim and reports no conflict while main is now self-contradictory."""
    body = json.dumps({"base": base, "head": head, "commit_message": msg}).encode()
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}/merges',
        data=body, method='POST',
        headers={'Authorization': f'token {TOKEN}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"MERGE: {e.code} ({'conflict' if e.code == 409 else 'nothing to merge / error'})")
        return None

def gh_delete_branch(branch):
    """Delete a branch ref. True on success (HTTP 204)."""
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}/git/refs/heads/{branch}',
        method='DELETE', headers={'Authorization': f'token {TOKEN}'})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status == 204
    except urllib.error.HTTPError:
        return False
```

**Reading on a branch — the `?ref=` discipline.** Never check out a branch to
read it. The read helpers already take `ref`: `gh_read(path, ref=branch)` and
`gh_get(path, ref=branch)` return a file as it stands on that branch. This is how
you orient on an open exploration without a checkout — subject index →
the branch register (`workspace/branch_logs/README.md`) → the in-branch `FOLDER_MAP.md` via `gh_read(..., ref=branch)`
— and how an overturning merge pulls branch content into `workspace/staging/`.

**Writing on a branch.** Use `gh_atomic_commit(file_changes, msg, branch=branch)`
(above) — it takes the branch as a parameter and commits atomically to it. Prefer
it over single-file Contents-API writes for anything more than a one-line note.

## Bulk Operations

For any bulk operation — moving or renaming many files, restructuring folders, applying coordinated edits across files — use the Trees API recipe above. It commits the whole batch atomically, eliminates the silent-corruption failure mode, and produces one clean commit in history instead of dozens.

The Contents-API fallback (looping `gh_move` or `gh_put` sequentially with verification on each) is documented here only for environments where the Trees API isn't available for some reason. If you have to use it: run the operations sequentially (not in parallel — rate limits and SHA conflicts compound) and audit sizes after.

```python
def audit_sizes(paths):
    """Print sizes of all paths. Useful as a post-batch sanity check
    after Contents-API bulk operations."""
    for p in paths:
        d = gh_get(p)
        size = d.get('size') if d else 'MISSING'
        print(f"  {size}: {p}")
```

Zero-byte files are the smoking gun for the corruption mode the Trees API is designed to prevent.

## Recovery from Failed Moves

If a move silently corrupted destination content (zero bytes) and the source was already deleted, the file is recoverable from the repository's commit history.

```python
def gh_get_at_commit(path, commit_sha):
    """Get file content as it existed at a specific commit."""
    return gh_read(path, ref=commit_sha)

def gh_commits_for_path(path, per_page=20):
    """List commits that touched a path."""
    url = f'https://api.github.com/repos/{REPO}/commits?path={urllib.request.quote(path)}&per_page={per_page}'
    req = urllib.request.Request(url, headers={'Authorization': f'token {TOKEN}'})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def recover_from_history(old_path):
    """Find the most recent commit where old_path had non-zero content. Return its content."""
    for c in gh_commits_for_path(old_path):
        data = gh_get(old_path, ref=c['sha'])
        if data and 'content' in data and data.get('size', 0) > 0:
            return base64.b64decode(data['content'])
    return None
```

The recovery flow: identify all zero-byte destinations, look up their pre-move source path, fetch the last non-zero version of the source from history, and re-upload to the correct destination.

## Shell Fallback (read-only and tiny writes)

Shell + `curl` is acceptable only for:
- Reading a file (any size).
- Listing a directory.
- Writing or deleting tiny text files where the commit message has no special characters.

Avoid for everything else. Examples for the read case:

```bash
# Read file content
curl -s -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$REPO/contents/PATH" \
  | python3 -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"

# List a directory
curl -s -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$REPO/contents/PATH" \
  | python3 -c "import sys,json; [print(f\"{i['type']:5} {i['name']}\") for i in json.load(sys.stdin)]"
```

For writes, do not use shell variable interpolation to inject base64 content into curl — use Python.

## Common Pitfalls

- **Contents API truncation at ~1 MB.** The Contents API endpoint (`/repos/{REPO}/contents/{path}`) silently truncates files larger than ~1 MB: metadata fields like `sha` and `size` are returned correctly, but the `content` field is empty or partial. A `base64.b64decode` of the truncated content yields zero bytes with no error. The `gh_read` recipe above avoids this by always fetching content via the blob API (`/git/blobs/{sha}`). Never read content directly from a `gh_get` response — go through `gh_read`. This is the bug class the size-verification step in `gh_move` exists to catch, but prevention is better than detection.
- **Stale sha errors.** If two writes to the same path happen close together, the second may use the sha from before the first. Always re-fetch sha immediately before write (`gh_put` does this).
- **Silent overwrite between concurrent sessions.** The dangerous cousin of the stale-sha error, and it produces *no* error at all: a write from a stale base is accepted, and the other session's change is gone. Affects the Trees API as much as the Contents API. See **Concurrency — atomicity is not isolation**.
- **Apostrophes and quotes in commit messages.** Safe in Python's `json.dumps`. Will break shell-interpolated payloads. Another reason to use Python.
- **Binary files.** Always read and write as bytes, never as decoded text. The base64 round-trip in the recipes above is content-agnostic.
- **404 vs empty response.** A 404 means the path doesn't exist; an empty list means the directory is empty; neither is an error.
- **Rate limits.** The Contents API has per-token limits. For batches of more than a handful of operations, prefer the Trees API recipe above — one commit hits the API far less often than per-file PUTs. For Contents-API loops, add a `time.sleep(1)` between calls.

## Coverage of the web branch

Between the Trees API recipe and the branch recipes above, the web branch covers
the full range a push-blocked session needs: atomic multi-file commits, folder
restructures, coordinated batch operations, and branch create / read-by-ref /
merge / delete. Nothing in scope requires git — which matters because on the web
branch there is no git to reach for. The git-vs-API choice itself is not made
here: it was made once, at the environment branch at the top of this file.
*(This section replaces the older "When to Stop and Use Git Directly" framing,
which treated the API as the fallback and git as the goal — the wrong mental
model on both sides of the environment branch: at Cowork git isn't a fallback,
it's the default; on the web there is no git at all.)*

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
