#!/usr/bin/env python3
"""Fill the Project Instructions template with USERNAME, REPO, and a fresh PAT.

The claude_researcher Project Instructions text (template/_PROJECT_INSTRUCTIONS.md.template)
carries three placeholders — <USERNAME>, <REPO>, and <TOKEN> — that must be
substituted whenever the PAT is rotated or a new Project is created for a
different research repo. Doing that by hand invites typos and, worse, invites
skipping the rotation because the friction is annoying — bad UX degrades
security posture.

This script prompts for the PAT with hidden input, substitutes it into a
locally-held copy of the template, and pipes the filled result to the system
clipboard (pbcopy on macOS, xclip on Linux). The PAT is never written to disk,
echoed to stdout, or logged.

Defaults:
  --username   auto-detected via `gh api user -q .login`, else
               `git config --get github.user`
  --repo       auto-detected as basename(git rev-parse --show-toplevel)
               of the current working directory

Substitution policy:
  <USERNAME> and <REPO> are substituted globally — the descriptions read more
  naturally with concrete values.
  <TOKEN> is substituted ONLY inside the `TOKEN="<TOKEN>"` line. The prose
  description of <TOKEN> retains the placeholder syntax as a reference to the
  bash variable above it; this keeps the token from appearing twice in the
  filled text (mild secrets-hygiene improvement) and keeps the description
  readable.

Usage:
  python3 tools/fill_project_instructions.py
  python3 tools/fill_project_instructions.py --username alice --repo my-lab
  python3 tools/fill_project_instructions.py --stdout > /tmp/filled.md
"""
from __future__ import annotations

import argparse
import getpass
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "template" / "_PROJECT_INSTRUCTIONS.md.template"

TOKEN_LINE_LITERAL = 'TOKEN="<TOKEN>"'


def detect_username() -> str | None:
    """Return GitHub username from gh CLI or git config, else None."""
    for cmd in (
        ["gh", "api", "user", "-q", ".login"],
        ["git", "config", "--get", "github.user"],
    ):
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        value = result.stdout.strip()
        if value:
            return value
    return None


def detect_repo() -> str | None:
    """Return basename of the current repo's toplevel, else None."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    toplevel = result.stdout.strip()
    if not toplevel:
        return None
    return Path(toplevel).name


def copy_to_clipboard(text: str) -> str | None:
    """Pipe text to a system clipboard tool. Return the tool name used, or None."""
    for cmd, name in (
        (["pbcopy"], "pbcopy"),
        (["xclip", "-selection", "clipboard"], "xclip"),
        (["wl-copy"], "wl-copy"),
    ):
        try:
            subprocess.run(cmd, input=text, text=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        return name
    return None


def fill_template(template: str, username: str, repo: str, token: str) -> str:
    """Substitute placeholders per the policy in the module docstring."""
    if TOKEN_LINE_LITERAL not in template:
        raise ValueError(
            f"template does not contain expected literal {TOKEN_LINE_LITERAL!r}; "
            "template shape may have changed — update this script"
        )
    filled = template.replace(TOKEN_LINE_LITERAL, f'TOKEN="{token}"', 1)
    filled = filled.replace("<USERNAME>", username)
    filled = filled.replace("<REPO>", repo)
    return filled


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--username",
        help="GitHub username (default: auto-detect via gh / git config)",
    )
    parser.add_argument(
        "--repo",
        help="Target research repo name, not owner/repo (default: current git repo basename)",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=TEMPLATE_PATH,
        help=f"Template path (default: {TEMPLATE_PATH.relative_to(REPO_ROOT)})",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print filled template to stdout instead of copying to clipboard",
    )
    args = parser.parse_args()

    username = args.username or detect_username()
    if not username:
        print(
            "error: --username not given and could not auto-detect "
            "(tried `gh api user` and `git config --get github.user`)",
            file=sys.stderr,
        )
        return 2

    repo = args.repo or detect_repo()
    if not repo:
        print(
            "error: --repo not given and current directory is not inside a git repo",
            file=sys.stderr,
        )
        return 2

    if not args.template.exists():
        print(f"error: template not found at {args.template}", file=sys.stderr)
        return 2

    template = args.template.read_text()

    print(f"username: {username}", file=sys.stderr)
    print(f"repo:     {repo}", file=sys.stderr)
    print("paste a fresh fine-grained GitHub PAT (input hidden):", file=sys.stderr)
    token = getpass.getpass(prompt="", stream=sys.stderr).strip()
    if not token:
        print("error: empty PAT", file=sys.stderr)
        return 2

    try:
        filled = fill_template(template, username, repo, token)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.stdout:
        sys.stdout.write(filled)
        return 0

    tool = copy_to_clipboard(filled)
    if tool:
        line_count = len(filled.splitlines())
        print(
            f"filled template ({line_count} lines) copied to clipboard via {tool}.",
            file=sys.stderr,
        )
        print(
            "paste into claude.ai -> Project -> Instructions.", file=sys.stderr
        )
        return 0

    print(
        "warning: no clipboard tool found (pbcopy/xclip/wl-copy); "
        "printing to stdout instead",
        file=sys.stderr,
    )
    sys.stdout.write(filled)
    return 0


if __name__ == "__main__":
    sys.exit(main())
