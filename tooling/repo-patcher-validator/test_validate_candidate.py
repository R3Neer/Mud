from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_DIR = ROOT / "tooling" / "repo-patcher-validator"
RUNTIME_DIR = ROOT / "tooling" / "repo-patcher-runtime"
SCRIPT = VALIDATOR_DIR / "validate_candidate.py"
ORIGIN = "https://github.com/R3Neer/Mud.git"


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"git {' '.join(args)}: {result.stderr}")
    return result.stdout.strip()


def initialize_repo(path: Path) -> None:
    path.mkdir(parents=True)
    git(path, "init")
    git(path, "config", "user.name", "Validator Test")
    git(path, "config", "user.email", "validator@example.invalid")


class ValidatorIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.control = self.root / "control"
        initialize_repo(self.control)
        control_tooling = self.control / "tooling" / "repo-patcher-validator"
        control_tooling.mkdir(parents=True)
        shutil.copy2(VALIDATOR_DIR / "runtime_probe.py", control_tooling / "runtime_probe.py")
        git(self.control, "add", ".")
        git(self.control, "commit", "-m", "control")
        self.control_sha = git(self.control, "rev-parse", "HEAD")

        self.target = self.root / "target-source"
        initialize_repo(self.target)
        shutil.copytree(RUNTIME_DIR, self.target / "tooling" / "repo-patcher-runtime")
        (self.target / ".gitignore").write_text("generated/\n", encoding="utf-8")
        (self.target / "base.txt").write_text("base\n", encoding="utf-8")
        git(self.target, "add", ".")
        git(self.target, "commit", "-m", "required ancestor")
        self.required_ancestor = git(self.target, "rev-parse", "HEAD")
        (self.target / "head-only.txt").write_text("head\n", encoding="utf-8")
        git(self.target, "add", ".")
        git(self.target, "commit", "-m", "target head")
        git(self.target, "remote", "add", "origin", ORIGIN)
        self.target_sha = git(self.target, "rev-parse", "HEAD")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def package(
        self, *, plugin: str | None = None, nondeterministic: bool = False
    ) -> tuple[Path, dict[str, object]]:
        package = self.root / ("plugin.zip" if plugin else "candidate.zip")
        generator = (
            "from pathlib import Path; import os; Path('generated').mkdir(exist_ok=True); "
            "Path('generated/evidence.bin').write_bytes(os.urandom(16))"
            if nondeterministic
            else "from pathlib import Path; Path('generated').mkdir(exist_ok=True); "
            "Path('generated/evidence.bin').write_bytes(bytes([0, 255]))"
        )
        validator = (
            "from pathlib import Path; assert len(Path('generated/evidence.bin').read_bytes()) == 16"
            if nondeterministic
            else "from pathlib import Path; assert Path('generated/evidence.bin').read_bytes() == bytes([0, 255])"
        )
        manifest = textwrap.dedent(
            f"""\
            schema: 1
            id: validator-integration
            title: Validator integration
            repository:
              names: Mud
              remotes: {ORIGIN}
            compatibility:
              exact_head: {self.target_sha}
              required_ancestor: {self.required_ancestor}
              clean_worktree: true
            operations:
              - create:
                  path: result.txt
                  content: "validated\\n"
            generators:
              - name: deterministic ignored binary
                command:
                  - "{{python}}"
                  - "-c"
                  - "{generator}"
            validators:
              - name: generated binary exists
                command:
                  - "{{python}}"
                  - "-c"
                  - "{validator}"
            """
        )
        if plugin:
            manifest += "plugin:\n  file: plugin.py\n"
        with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("patch.yaml", manifest)
            if plugin:
                archive.writestr("plugin.py", plugin)
        raw = package.read_bytes()
        request: dict[str, object] = {
            "protocol": "mud-repo-patcher-validation/v1",
            "request_id": "integration-001",
            "repository": "R3Neer/Mud",
            "target_sha": self.target_sha,
            "package_sha256": hashlib.sha256(raw).hexdigest(),
            "package_size": len(raw),
            "trust_plugin": plugin is not None,
            "transport_kind": "logical_files",
        }
        return package, request

    def invoke(self, package: Path, request: dict[str, object]) -> tuple[subprocess.CompletedProcess[str], Path]:
        request_path = self.root / "request.json"
        request_path.write_text(json.dumps(request), encoding="utf-8")
        output = self.root / "evidence"
        result = subprocess.run(
            [
                sys.executable, str(SCRIPT),
                "--control-root", str(self.control),
                "--target-source", str(self.target),
                "--validation-root", str(self.root / "validation"),
                "--package", str(package),
                "--request", str(request_path),
                "--output", str(output),
                "--target-sha", self.target_sha,
                "--control-sha", self.control_sha,
                "--workflow-run-id", "123",
                "--run-attempt", "1",
            ],
            text=True, capture_output=True, encoding="utf-8", errors="replace", check=False,
        )
        return result, output

    def test_green_candidate_produces_reproducible_evidence_and_exact_zip(self) -> None:
        package, request = self.package()
        result, output = self.invoke(package, request)
        diagnostic = (output / "diagnostic.txt").read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout + diagnostic)
        report = json.loads((output / "result.json").read_text(encoding="utf-8"))
        self.assertEqual(report["conclusion"], "success")
        self.assertEqual((output / "candidate.zip").read_bytes(), package.read_bytes())
        reproducibility = json.loads((output / "reproducibility.json").read_text(encoding="utf-8"))
        self.assertEqual(reproducibility, {"differences": [], "status": "passed"})
        state = json.loads((output / "run-a-state.json").read_text(encoding="utf-8"))
        paths = {entry["relative_path"] for entry in state["filesystem_tree"]}
        self.assertIn("generated/evidence.bin", paths)
        applied = (output / "applied.patch").read_bytes()
        self.assertIn(b"result.txt", applied)
        self.assertIn(b"generated/evidence.bin", applied)
        self.assertEqual((output / "git-diff-binary.patch").read_bytes(), applied)
        self.assertIn("result.txt", (output / "diff-stat.txt").read_text(encoding="utf-8"))

    def test_plugin_writing_during_explain_is_rejected_as_preflight_side_effect(self) -> None:
        plugin = textwrap.dedent(
            """\
            def apply(ctx, manifest):
                (ctx.repo / "rogue.txt").write_text("side effect", encoding="utf-8")
            """
        )
        package, request = self.package(plugin=plugin)
        result, output = self.invoke(package, request)
        self.assertEqual(result.returncode, 1)
        report = json.loads((output / "result.json").read_text(encoding="utf-8"))
        self.assertEqual(
            report["failure_kind"],
            "unexpected_preflight_side_effect",
            (output / "diagnostic.txt").read_text(encoding="utf-8"),
        )
        self.assertEqual(report["preflight_command"], "explain")

    def test_nondeterministic_generator_is_rejected_between_clean_clones(self) -> None:
        package, request = self.package(nondeterministic=True)
        result, output = self.invoke(package, request)
        self.assertEqual(result.returncode, 1)
        report = json.loads((output / "result.json").read_text(encoding="utf-8"))
        self.assertEqual(report["failure_kind"], "not_reproducible")
        evidence = json.loads((output / "reproducibility.json").read_text(encoding="utf-8"))
        self.assertIn("filesystem_tree", evidence["differences"])

    def test_plugin_requires_explicit_trust(self) -> None:
        package, request = self.package(plugin="def apply(ctx, manifest):\n    pass\n")
        request["trust_plugin"] = False
        result, output = self.invoke(package, request)
        self.assertEqual(result.returncode, 1)
        report = json.loads((output / "result.json").read_text(encoding="utf-8"))
        self.assertEqual(report["failure_kind"], "plugin_not_authorized")


if __name__ == "__main__":
    unittest.main(verbosity=2)
