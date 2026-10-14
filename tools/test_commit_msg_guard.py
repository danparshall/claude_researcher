"""commit-msg guard: a web commit goes out under the session codename or not at all.

`template/hooks/commit-msg` is installed into every clone a web session
makes (RESEARCHER.md §2.0b). It reads the session's write-once identity
file and refuses any commit whose author name is not that file's CODENAME.
The failure it prevents: after a Project move the sandbox reboots, global
git config resets to `Claude`, and a fresh clone commits under the wrong
name (plan 16, docs/plans/16_session_identity_lock.md).

These tests install the real hook into temp repos and drive real
`git commit` calls; they check only whether the commit landed and what the
refusal tells the agent to do.

Runnable standalone (`python3 tools/test_commit_msg_guard.py`) or under
pytest (`pytest tools/`).
"""
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOOK = REPO / "template" / "hooks" / "commit-msg"

SESSION_ID = "0e1f2a3b-test-session"
CODENAME = "Dan (web, canary-policy, 20261014T2059, opus-5.5)"


class CommitMsgGuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.identity_dir = self.tmp / "session-identity"
        self.identity_dir.mkdir()
        self.identity_file = self.identity_dir / f"{SESSION_ID}.env"
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.repo = self.tmp / "clone"
        self.env = {
            "PATH": os.environ["PATH"],
            "HOME": str(self.home),
            "GIT_CONFIG_NOSYSTEM": "1",
            "CLAUDE_CODE_SESSION_ID": SESSION_ID,
            "SESSION_IDENTITY_DIR": str(self.identity_dir),
        }
        self._git("init", "-q", str(self.repo), cwd=self.tmp)
        self._git("config", "user.name", CODENAME)
        self._git("config", "user.email", "parshall.dan@gmail.com")
        self._git("config", "commit.gpgsign", "false")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args],
            cwd=cwd or self.repo,
            env=self.env,
            capture_output=True,
            text=True,
        )

    def _write_identity(self, codename=CODENAME):
        self.identity_file.write_text(
            f"SESSION_ID='{SESSION_ID}'\n"
            f"CODENAME='{codename}'\n"
            "COMMIT_EMAIL='parshall.dan@gmail.com'\n"
            "CONVO='pending'\n"
        )

    def _install_hook(self, hooks_dir=None):
        target_dir = hooks_dir or (self.repo / ".git" / "hooks")
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / "commit-msg"
        shutil.copy(HOOK, target)
        target.chmod(target.stat().st_mode | stat.S_IXUSR)

    def _commit(self, *extra):
        (self.repo / "notes.md").write_text(f"change {len(self._log())}\n")
        self._git("add", "notes.md")
        return self._git(*extra, "commit", "-q", "-m", "test commit")

    def _log(self):
        out = self._git("log", "--format=%an")
        return out.stdout.splitlines() if out.returncode == 0 else []

    def test_codename_author_commits(self):
        self._write_identity()
        self._install_hook()
        result = self._commit()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self._log(), [CODENAME])

    def test_other_author_is_refused_with_the_fix(self):
        self._write_identity()
        self._install_hook()
        result = self._commit("-c", "user.name=Claude")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self._log(), [])
        self.assertIn(CODENAME, result.stderr)
        self.assertIn(str(self.identity_file), result.stderr)

    def test_near_miss_codename_is_refused(self):
        self._write_identity()
        self._install_hook()
        rebuilt = "Dan (web, canary-policy, 20261014T2131, opus-5.5)"
        result = self._commit("-c", f"user.name={rebuilt}")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self._log(), [])
        self.assertIn(CODENAME, result.stderr)

    def test_missing_identity_file_is_refused_with_setup_pointer(self):
        self._install_hook()
        result = self._commit()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self._log(), [])
        self.assertIn(str(self.identity_file), result.stderr)
        self.assertIn("RESEARCHER.md §2.0b", result.stderr)

    def test_unset_session_id_is_refused_with_setup_pointer(self):
        self._write_identity()
        self._install_hook()
        del self.env["CLAUDE_CODE_SESSION_ID"]
        result = self._commit()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self._log(), [])
        self.assertIn("RESEARCHER.md §2.0b", result.stderr)

    def test_guard_works_under_core_hookspath(self):
        self._write_identity()
        self._git("config", "core.hooksPath", ".githooks")
        self._install_hook(self.repo / ".githooks")
        refused = self._commit("-c", "user.name=Claude")
        self.assertNotEqual(refused.returncode, 0)
        accepted = self._commit()
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        self.assertEqual(self._log(), [CODENAME])


if __name__ == "__main__":
    sys.exit(unittest.main())
