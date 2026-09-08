"""Profile-side check for the dotfiles → claude_researcher skill export.

`template/skills/.export_manifest.json` is written by the exporter in the
dotfiles repo (`export_profile_skills.py`) — it lists a sha256 per exported
file plus the dotfiles commit and the researcher-skillset version the
export came from. Exported skill dirs are build artifacts: never hand-edit
them in this repo; edit the source under dotfiles `nori-researcher/skills/`
and re-export. These tests catch a hand edit (hash mismatch) and a skill
dir with no `SKILL_INDEX.md` entry (or an entry with no dir).

Runnable standalone (`python3 tools/test_skill_manifest.py`) or under pytest
(`pytest tools/`). The manifest half skips until the first export lands.
"""
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "template" / "skills"
MANIFEST = SKILLS_DIR / ".export_manifest.json"
SKILL_INDEX = SKILLS_DIR / "SKILL_INDEX.md"
HEADING_RE = re.compile(r"^### (\S+)\s*$", re.MULTILINE)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _skill_dirs():
    return sorted(p.name for p in SKILLS_DIR.iterdir()
                  if p.is_dir() and (p / "SKILL.md").is_file())


def _index_headings():
    return set(HEADING_RE.findall(SKILL_INDEX.read_text(encoding="utf-8")))


def test_every_skill_dir_has_a_skill_index_entry():
    missing = [name for name in _skill_dirs() if name not in _index_headings()]
    assert not missing, f"skill dirs with no `### <name>` entry in SKILL_INDEX.md: {missing}"


def test_every_skill_index_entry_has_a_dir():
    dirs = set(_skill_dirs())
    orphans = sorted(h for h in _index_headings() if h not in dirs)
    assert not orphans, f"SKILL_INDEX.md entries with no skill dir: {orphans}"


def _load_manifest() -> dict:
    """The manifest, or a skip (pytest honors unittest.SkipTest) before the
    first export has landed."""
    if not MANIFEST.is_file():
        raise unittest.SkipTest(f"no export manifest yet at {MANIFEST.relative_to(REPO)}")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_exported_files_match_manifest():
    manifest = _load_manifest()
    mismatches = []
    for skill, files in manifest["skills"].items():
        for rel, digest in files.items():
            path = SKILLS_DIR / skill / rel
            actual = _sha256(path) if path.is_file() else None
            if actual != digest:
                mismatches.append(f"{skill}/{rel}")
    assert not mismatches, (
        "exported skill files differ from .export_manifest.json (hand-edited? "
        "edit the dotfiles source and re-export instead): " + ", ".join(mismatches))


def test_manifest_skills_have_index_entries():
    manifest = _load_manifest()
    missing = sorted(s for s in manifest["skills"] if s not in _index_headings())
    assert not missing, f"exported skills with no SKILL_INDEX.md entry: {missing}"


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"ok   {name}")
            except unittest.SkipTest as exc:
                print(f"skip {name}: {exc}")
            except Exception as exc:  # noqa: BLE001 — standalone runner
                failures += 1
                print(f"FAIL {name}: {exc}")
    sys.exit(1 if failures else 0)
