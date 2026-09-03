from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from tooling.translation import check_migration


ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = Path(__file__).with_name("snapshots") / "help.txt"
HELP_CASES = (
    ("decisions", ("tooling/decisions/manage_decisions.py", "--help")),
    ("questions", ("tooling/questions/validate_questions.py", "--help")),
    ("temporaries", ("governance/validate_temporaries.py", "--help")),
    ("editorial", ("governance/validate_spec_editorial.py", "--help")),
    ("grammar", ("specification/grammar/validate_grammar.py", "--help")),
    ("syntax", ("specification/syntax/validate_syntax_model.py", "--help")),
    ("translation-check", ("tooling/translation/check_migration.py", "--help")),
    ("glossary", ("tooling/translation/render_glossary.py", "--help")),
    ("decisions-migrate", ("tooling/decisions/manage_decisions.py", "migrate", "--help")),
    ("decisions-generate", ("tooling/decisions/manage_decisions.py", "generate", "--help")),
    ("decisions-validate", ("tooling/decisions/manage_decisions.py", "validate", "--help")),
    ("questions-validate", ("tooling/questions/validate_questions.py", "validate", "--help")),
    ("questions-generate", ("tooling/questions/validate_questions.py", "generate", "--help")),
)


def invoke(*arguments: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "ascii"
    if env:
        environment.update(env)
    return subprocess.run(
        [sys.executable, *arguments],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="ascii",
        env=environment,
    )


class HelpSnapshotTests(unittest.TestCase):
    def test_all_help_pages_match_snapshot(self) -> None:
        sections: list[str] = []
        for name, arguments in HELP_CASES:
            completed = invoke(*arguments)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(completed.stderr, "")
            self.assertNotIn("\x1b[", completed.stdout)
            sections.append(f"SNAPSHOT {name}\n{completed.stdout}")
        actual = "".join(sections).rstrip() + "\n"
        self.assertEqual(actual, SNAPSHOT.read_text(encoding="ascii"))

    def test_short_help_alias_is_supported(self) -> None:
        completed = invoke("governance/validate_temporaries.py", "-h")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn(" MUD TEMPORARIES\n", completed.stdout)

    def test_help_does_not_regenerate_glossary(self) -> None:
        glossary = ROOT / "notes" / "glosario-de-traduccion-es-en.md"
        before = glossary.read_bytes()
        completed = invoke("tooling/translation/render_glossary.py", "--help")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(glossary.read_bytes(), before)


class OutputContractTests(unittest.TestCase):
    def test_invalid_global_help_is_actionable(self) -> None:
        completed = invoke("governance/validate_temporaries.py", "--help", "extra")
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn("R3CLI.Help.InvalidArguments", completed.stderr)
        self.assertIn("Try:", completed.stderr)

    def test_version_is_intentionally_unknown(self) -> None:
        completed = invoke("governance/validate_temporaries.py", "--version")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("unrecognized arguments: --version", completed.stderr)

    def test_forced_colour_and_no_colour(self) -> None:
        coloured = subprocess.run(
            [sys.executable, "tooling/translation/render_glossary.py", "--check", "--colour", "always", "--ascii"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(coloured.returncode, 0, coloured.stderr)
        if os.name != "nt":
            self.assertIn("\x1b[", coloured.stdout)
        plain = invoke(
            "tooling/translation/render_glossary.py",
            "--check",
            env={"NO_COLOR": "1"},
        )
        self.assertEqual(plain.returncode, 0, plain.stderr)
        self.assertNotIn("\x1b[", plain.stdout)
        self.assertTrue(plain.stdout.startswith("+ "))

    def test_missing_r3cli_has_no_traceback(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-E", "-S", "governance/validate_temporaries.py", "--help"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn("python -m pip install -r tooling/requirements.txt", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)


class TranslationAdapterTests(unittest.TestCase):
    @staticmethod
    def completed(returncode: int, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess([], returncode, stdout, stderr)

    def run_adapter(self, translation: subprocess.CompletedProcess[str]) -> tuple[int, str, str]:
        successes = [self.completed(0), self.completed(0), self.completed(0)]
        with patch.object(check_migration.subprocess, "run", side_effect=[translation, *successes]):
            stdout = StringIO()
            stderr = StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = check_migration.main(["--r3translate", "fake", "--colour", "never", "--ascii"])
        return result, stdout.getvalue(), stderr.getvalue()

    def test_translation_findings_are_rendered_and_exit_one_is_preserved(self) -> None:
        payload = {"findings": [{"code": "Translation.ForbiddenSpelling", "message": "Forbidden spelling.", "line": 7}], "ok": False}
        result, stdout, stderr = self.run_adapter(self.completed(1, json.dumps(payload)))
        self.assertEqual(result, 1)
        self.assertEqual(stdout, "")
        self.assertIn("line 7: Forbidden spelling. [Translation.ForbiddenSpelling]", stderr)

    def test_malformed_translation_json_is_an_actionable_error(self) -> None:
        result, stdout, stderr = self.run_adapter(self.completed(0, "not-json"))
        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("Mud.Translation.InvalidProviderOutput", stderr)
        self.assertIn("Try:", stderr)


if __name__ == "__main__":
    unittest.main()
