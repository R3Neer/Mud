from __future__ import annotations

import subprocess
import sys
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROFILE = Path(__file__).with_name("mud-es-en.toml")


class TranslationToolingTests(unittest.TestCase):
    def test_profile_contract(self) -> None:
        data = tomllib.loads(PROFILE.read_text(encoding="utf-8-sig"))
        self.assertIs(data["temporary"], True)
        self.assertEqual(data["language"], {"source": "ES", "target": "EN-GB"})
        self.assertGreater(len(data["terms"]), 200)
        self.assertGreater(len(data["protected"]["literals"]), 80)
        self.assertIn("title", data["frontmatter"]["translate"])
        self.assertIn("status", data["frontmatter"]["preserve"])
        self.assertIn("behavior", data["style"]["forbidden"])
        self.assertGreater(len(data["style"]["guidance"]), 5)
        self.assertIn("para", data["checks"]["probable-source"])

    def test_glossary_is_generated(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("render_glossary.py")), "--check"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
