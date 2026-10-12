"""Project Instructions version: one value, stated consistently.

Each Project Instructions template carries its version twice: in the title
line (`# Project Instructions — ... (v2.0)`, what a user sees when comparing
pasted text) and in the `PI_VERSION="2.0"` line (what a session checks).
The runtime docs (`RESEARCHER.md`, `LITE.md`) state the current version a
session compares against. These tests fail if any of those disagree, so a
version bump has to touch all of them.

Runnable standalone (`python3 tools/test_pi_version.py`) or under pytest
(`pytest tools/`).
"""
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FULL_TEMPLATE = REPO / "template" / "_PROJECT_INSTRUCTIONS.md.template"
LITE_TEMPLATE = REPO / "template_lite" / "_PROJECT_INSTRUCTIONS_LITE.md.template"
RESEARCHER = REPO / "template" / "RESEARCHER.md"
LITE = REPO / "template_lite" / "LITE.md"

TITLE_RE = re.compile(r"\A# Project Instructions — .*\(.*\bv(\d+\.\d+)\)\n")
VAR_RE = re.compile(r'^PI_VERSION="(\d+\.\d+)"$', re.MULTILINE)
CURRENT_RE = re.compile(
    r'current\s+Project\s+Instructions\s+version\s+is\s+\*\*(\d+\.\d+)\*\*\s+\(`PI_VERSION="(\d+\.\d+)"`\)'
)


def _template_versions(path: Path) -> tuple:
    text = path.read_text()
    title = TITLE_RE.search(text)
    var = VAR_RE.findall(text)
    assert title, f"{path.name}: title line has no '(... vN.M)' version"
    assert len(var) == 1, f'{path.name}: expected exactly one PI_VERSION="N.M" line, found {len(var)}'
    return title.group(1), var[0]


def _current_version(path: Path) -> str:
    found = CURRENT_RE.findall(path.read_text())
    assert len(found) == 1, f"{path.name}: expected one 'current Project Instructions version is' statement, found {len(found)}"
    bold, var = found[0]
    assert bold == var, f"{path.name}: states **{bold}** but PI_VERSION=\"{var}\""
    return bold


class PIVersionTest(unittest.TestCase):
    def test_full_template_title_matches_var(self):
        title, var = _template_versions(FULL_TEMPLATE)
        self.assertEqual(title, var)

    def test_lite_template_title_matches_var(self):
        title, var = _template_versions(LITE_TEMPLATE)
        self.assertEqual(title, var)

    def test_researcher_md_matches_full_template(self):
        self.assertEqual(_current_version(RESEARCHER), _template_versions(FULL_TEMPLATE)[1])

    def test_lite_md_matches_lite_template(self):
        self.assertEqual(_current_version(LITE), _template_versions(LITE_TEMPLATE)[1])


if __name__ == "__main__":
    sys.exit(unittest.main())
