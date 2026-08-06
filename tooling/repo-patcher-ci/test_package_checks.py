from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("package_checks.py").resolve()


def write_package(path: Path, manifest: str, extra: dict[str, str] | None = None) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("patch.yaml", manifest)
        for name, content in (extra or {}).items():
            archive.writestr(name, content)


def inspect_plugin(package: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "plugin", "--package", str(package)],
        text=True,
        capture_output=True,
        check=False,
        encoding="utf-8",
        errors="replace",
        env=os.environ.copy(),
    )


class PackageInspectionTests(unittest.TestCase):
    def test_declarative_package_has_no_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "declarative.zip"
            write_package(package, """schema: 1
id: declarative
title: Declarative
operations:
  - assert_contains:
      path: AGENTS.md
      text: MUD
""")
            result = inspect_plugin(package)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "false")

    def test_plugin_is_detected_without_importing_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "plugin.zip"
            write_package(package, """schema: 1
id: plugin-test
title: Plugin test
plugin:
  file: plugin.py
""", {"plugin.py": "raise RuntimeError('plugin was executed during inspection')\n"})
            result = inspect_plugin(package)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "true")


if __name__ == "__main__":
    unittest.main(verbosity=2)
