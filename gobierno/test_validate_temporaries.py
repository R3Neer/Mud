from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import validate_temporaries


class TemporaryTomlTests(unittest.TestCase):
    def validate_files(self, files: dict[str, str]):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            return validate_temporaries.validate(root)

    def test_accepts_complete_toml_metadata(self) -> None:
        active, errors = self.validate_files(
            {
                "profile.toml": (
                    'temporary = true\n'
                    'temporary-reason = "Migration"\n'
                    'temporary-delete-when = "Migration complete"\n'
                )
            }
        )
        self.assertEqual(errors, [])
        self.assertEqual([str(item.path) for item in active], ["profile.toml"])

    def test_rejects_incomplete_toml_metadata(self) -> None:
        _active, errors = self.validate_files({"profile.toml": "temporary = true\n"})
        self.assertTrue(any("temporary-reason" in error for error in errors))
        self.assertTrue(any("temporary-delete-when" in error for error in errors))

    def test_rejects_temporary_false(self) -> None:
        _active, errors = self.validate_files({"profile.toml": "temporary = false\n"})
        self.assertTrue(any("temporary: false" in error for error in errors))

    def test_reports_malformed_temporary_toml(self) -> None:
        _active, errors = self.validate_files({"profile.toml": "temporary = true ???\n"})
        self.assertTrue(any("TOML temporal inválido" in error for error in errors))

    def test_rejects_expired_toml_deadline(self) -> None:
        _active, errors = self.validate_files(
            {
                "profile.toml": (
                    'temporary = true\n'
                    'temporary-reason = "Migration"\n'
                    'temporary-delete-when = "Migration complete"\n'
                    "temporary-delete-after = 2000-01-01\n"
                )
            }
        )
        self.assertTrue(any("venció el 2000-01-01" in error for error in errors))

    def test_ignores_unrelated_malformed_toml(self) -> None:
        active, errors = self.validate_files({"other.toml": "not valid toml"})
        self.assertEqual(active, [])
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
