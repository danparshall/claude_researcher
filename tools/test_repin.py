"""Tests for tools/repin.py — the SHA re-pin URL-rewrite logic.

Runnable standalone (`python3 tools/test_repin.py`) or under pytest.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repin import repin_refs

DOMAIN_ALLOWLIST = "template/templates/domain_allowlist.txt"
BOOTSTRAP = "template/BOOTSTRAP.md"
RESEARCHER = "template/RESEARCHER.md"

NEW = "ce9ba20abcdef0123456789abcdef0123456789a"  # a plausible 40-hex sha


def test_rewrites_sha_pinned_url():
    old = "abc1234000000000000000000000000000000000"
    text = (
        "see https://raw.githubusercontent.com/danparshall/claude_researcher/"
        f"{old}/{DOMAIN_ALLOWLIST} for domains"
    )
    out, n = repin_refs(text, [DOMAIN_ALLOWLIST], NEW)
    assert n == 1
    assert NEW in out
    assert old not in out
    assert DOMAIN_ALLOWLIST in out  # the path is preserved, only the ref changes


def test_rewrites_main_ref_url():
    text = (
        "https://raw.githubusercontent.com/danparshall/claude_researcher/"
        f"main/{DOMAIN_ALLOWLIST}"
    )
    out, n = repin_refs(text, [DOMAIN_ALLOWLIST], NEW)
    assert n == 1
    assert f"/{NEW}/{DOMAIN_ALLOWLIST}" in out
    assert "/main/" not in out


def test_leaves_unmanaged_path_untouched():
    # RESEARCHER.md is intentionally left on /main/ (the clone-fallback URLs).
    text = (
        "https://raw.githubusercontent.com/danparshall/claude_researcher/"
        f"main/{RESEARCHER}"
    )
    out, n = repin_refs(text, [DOMAIN_ALLOWLIST, BOOTSTRAP], NEW)
    assert n == 0
    assert out == text


def test_leaves_other_repo_untouched():
    text = (
        "https://raw.githubusercontent.com/someone/otherrepo/"
        f"main/{DOMAIN_ALLOWLIST}"
    )
    out, n = repin_refs(text, [DOMAIN_ALLOWLIST], NEW)
    assert n == 0
    assert out == text


def test_rewrites_every_occurrence():
    url = (
        "https://raw.githubusercontent.com/danparshall/claude_researcher/"
        f"old0000000000000000000000000000000000000/{DOMAIN_ALLOWLIST}"
    )
    text = f"{url} ... and again {url}"
    out, n = repin_refs(text, [DOMAIN_ALLOWLIST], NEW)
    assert n == 2
    assert out.count(NEW) == 2


def test_idempotent_when_already_pinned():
    text = (
        "https://raw.githubusercontent.com/danparshall/claude_researcher/"
        f"{NEW}/{DOMAIN_ALLOWLIST}"
    )
    out, _ = repin_refs(text, [DOMAIN_ALLOWLIST], NEW)
    assert out == text  # re-pinning to the same ref changes nothing


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e!r}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
