"""Profile-side check for the dotfiles → claude_researcher skill export.

`template/skills/.export_manifest.json` is written by the exporter in the
dotfiles repo (`export_profile_skills.py`) — it lists a sha256 per exported
file plus the dotfiles commit and the researcher-skillset version the
export came from. Exported skill dirs are build artifacts: never hand-edit
them in this repo; edit the source under dotfiles `nori-researcher/skills/`
and re-export. These tests catch a hand edit (hash mismatch), a hand-added
file the manifest doesn't list (the next export would delete it), and a
skill dir with no `SKILL_INDEX.md` entry (or an entry with no dir).

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


def _manifest_skills() -> dict:
    """The manifest's `skills` map, `{skill: {relpath: sha256}}`. A missing or
    empty map fails by name instead of KeyError-ing or passing vacuously."""
    skills = _load_manifest().get("skills")
    assert isinstance(skills, dict) and skills, (
        f"{MANIFEST.relative_to(REPO)} has no non-empty 'skills' map — exporter schema drift?")
    return skills


def _exporter_ignores(rel: Path) -> bool:
    """Files the exporter neither copies nor lists (its own exclusions)."""
    return rel.name == ".DS_Store" or "__pycache__" in rel.parts


def test_exported_files_match_manifest():
    mismatches = []
    for skill, files in _manifest_skills().items():
        for rel, digest in files.items():
            path = SKILLS_DIR / skill / rel
            actual = _sha256(path) if path.is_file() else None
            if actual != digest:
                mismatches.append(f"{skill}/{rel}")
    assert not mismatches, (
        "exported skill files differ from .export_manifest.json (hand-edited? "
        "edit the dotfiles source and re-export instead): " + ", ".join(mismatches))


def test_exported_dirs_have_no_unlisted_files():
    unlisted = []
    for skill, files in _manifest_skills().items():
        skill_dir = SKILLS_DIR / skill
        if not skill_dir.is_dir():
            continue  # test_exported_files_match_manifest reports the missing files
        for path in sorted(skill_dir.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(skill_dir)
            if _exporter_ignores(rel) or rel.as_posix() in files:
                continue
            unlisted.append(f"{skill}/{rel.as_posix()}")
    assert not unlisted, (
        "files in exported skill dirs that .export_manifest.json does not list — "
        "the next export deletes them (the exporter rmtree's each exported dir); "
        "add the file to the dotfiles source under nori-researcher/skills/ and "
        "re-export instead: " + ", ".join(unlisted))


def test_manifest_skills_have_index_entries():
    missing = sorted(s for s in _manifest_skills() if s not in _index_headings())
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
