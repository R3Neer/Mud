from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from snapshot import capture_repository, repository_difference


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout


class SnapshotTests(unittest.TestCase):
    def test_ignored_files_and_index_changes_are_observable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "Mud"
            repo.mkdir()
            git(repo, "init")
            git(repo, "config", "user.name", "Snapshot Test")
            git(repo, "config", "user.email", "snapshot@example.invalid")
            (repo / ".gitignore").write_text("ignored/\n", encoding="utf-8")
            (repo / "tracked.txt").write_text("one\n", encoding="utf-8")
            git(repo, "add", ".")
            git(repo, "commit", "-m", "fixture")

            before = capture_repository(repo)
            (repo / "ignored").mkdir()
            (repo / "ignored" / "binary.dat").write_bytes(b"\x00\xff")
            after_ignored = capture_repository(repo)
            self.assertIn("filesystem_tree", repository_difference(before, after_ignored))
            self.assertEqual(before["status_porcelain_z"], after_ignored["status_porcelain_z"])

            (repo / "tracked.txt").write_text("two\n", encoding="utf-8")
            git(repo, "add", "tracked.txt")
            after_index = capture_repository(repo)
            self.assertNotEqual(
                after_ignored["index_physical_sha256"], after_index["index_physical_sha256"]
            )
            self.assertNotEqual(after_ignored["index_semantic"], after_index["index_semantic"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
