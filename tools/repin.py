#!/usr/bin/env python3
"""Re-pin claude_researcher's SHA-pinned raw.githubusercontent.com URLs.

claude.ai's web_fetch serves stale cached snapshots of raw.githubusercontent.com
URLs, so the bootstrap entry point and the templates it fetches mid-flow are
pinned to immutable commit SHAs (see docs/convos/20260520_bootstrap_sha_pin.md).
Those SHAs must be bumped whenever BOOTSTRAP.md or a pinned template changes,
or collaborators fetch stale content. This script does that bump.

It makes two commits, by necessity: a commit cannot embed its own SHA, so the
README's BOOTSTRAP.md URL must point at the commit that already contains the
finalized BOOTSTRAP.md.

  commit 1  BOOTSTRAP.md's in-flow template URLs  -> the pre-script HEAD
  commit 2  README.md's bootstrap-entry URL       -> commit 1

Run from the repo root, on a feature branch. Does not push. The branch must be
merged with a real merge commit (not squash/rebase) so the pinned commits stay
reachable from main's history.
"""
import argparse
import re
import subprocess
import sys

OWNER_REPO = "danparshall/claude_researcher"

# URLs the bootstrap fetches via web_fetch and must therefore be SHA-pinned.
# Anything not listed here (e.g. the /main/ RESEARCHER.md clone-fallback URLs)
# is intentionally left alone.
BOOTSTRAP_PINNED_PATHS = [
    "template/templates/domain_allowlist.txt",
    "template/templates/personal_info.md.template",
    "template/_PROJECT_INSTRUCTIONS.md.template",
]
README_PINNED_PATH = "template/BOOTSTRAP.md"


def repin_refs(text, managed_paths, new_ref):
    """Rewrite the <ref> segment of raw.githubusercontent.com URLs.

    For each path in managed_paths, every URL of the form
    raw.githubusercontent.com/<OWNER_REPO>/<ref>/<path> has its <ref> replaced
    with new_ref. URLs for other repos, or for paths not in managed_paths, are
    left untouched. Returns (new_text, replacement_count).
    """
    count = 0
    for path in managed_paths:
        pattern = re.compile(
            r"(raw\.githubusercontent\.com/" + re.escape(OWNER_REPO) + r"/)"
            r"[^/\s]+"
            r"(/" + re.escape(path) + r")"
        )
        text, n = pattern.subn(r"\g<1>" + new_ref + r"\g<2>", text)
        count += n
    return text, count


def git(*args):
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Re-pin SHA-pinned raw.githubusercontent.com URLs. "
        "Makes two commits on the current feature branch; see module docstring."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report the would-be rewrites without writing files or committing"
        " (allowed on main, since it touches nothing)",
    )
    return parser


def short_ref(ref):
    return ref[:10] if re.fullmatch(r"[0-9a-f]{40}", ref) else ref


def repin_file(path, managed_paths, new_ref, commit_message, dry_run=False):
    """Rewrite path's pinned URLs to new_ref; commit if anything changed.

    With dry_run=True, reports the would-be rewrite and touches nothing
    (no file write, no git calls). Returns True if a commit was made.
    """
    with open(path) as f:
        original = f.read()
    updated, n = repin_refs(original, managed_paths, new_ref)
    if updated == original:
        print(f"{path}: already current, nothing to re-pin")
        return False
    if dry_run:
        print(
            f"{path}: DRY RUN — would re-pin {n} URL(s) -> {short_ref(new_ref)}"
        )
        return False
    with open(path, "w") as f:
        f.write(updated)
    git("add", path)
    git("commit", "-m", commit_message)
    print(f"{path}: re-pinned {n} URL(s) -> {new_ref[:10]}, committed")
    return True


def main(argv=None):
    args = build_parser().parse_args(argv)

    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if branch == "main" and not args.dry_run:
        sys.exit("refusing to run on main — switch to a feature branch first")

    head = git("rev-parse", "HEAD")

    # Commit 1 — BOOTSTRAP.md's in-flow template URLs point at the pre-script
    # HEAD, whose tree carries the current template files.
    repin_file(
        "template/BOOTSTRAP.md",
        BOOTSTRAP_PINNED_PATHS,
        head,
        f"repin: BOOTSTRAP.md template-fetch URLs -> {head[:10]}",
        dry_run=args.dry_run,
    )
    # In a dry run commit 1 is never made, so the README's target ref cannot
    # exist yet; report against a placeholder. The rewrite count is unaffected.
    bootstrap_commit = (
        "<commit-1, created at run time>" if args.dry_run
        else git("rev-parse", "HEAD")
    )

    # Commit 2 — README's entry URL points at the commit that now holds the
    # finalized BOOTSTRAP.md.
    repin_file(
        "README.md",
        [README_PINNED_PATH],
        bootstrap_commit,
        f"repin: README bootstrap-entry URL -> {short_ref(bootstrap_commit)}",
        dry_run=args.dry_run,
    )

    if args.dry_run:
        print("\nDRY RUN — no files written, no commits made.")
        return
    print(
        "\nDone. Review with `git log` / `git diff main`, then open a PR.\n"
        "Merge it with a merge commit (not squash/rebase) so the pinned "
        "commits stay reachable from main."
    )


if __name__ == "__main__":
    main()
