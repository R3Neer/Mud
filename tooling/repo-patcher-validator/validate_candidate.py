from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from package_safety import PackageSafetyError, validate_zip_bytes
from snapshot import capture_repository, repository_difference


PROTOCOL = "mud-repo-patcher-validation/v1"
RESULT_PROTOCOL = "mud-repo-patcher-validation-result/v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
SECRET_NAMES = {
    "ACTIONS_ID_TOKEN_REQUEST_URL",
    "ACTIONS_ID_TOKEN_REQUEST_TOKEN",
    "GITHUB_TOKEN",
    "GH_TOKEN",
}


class ValidationFailure(RuntimeError):
    def __init__(self, kind: str, message: str, *, command: str | None = None):
        super().__init__(message)
        self.kind = kind
        self.command = command


@dataclass
class CommandResult:
    label: str
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode != 0:
        raise ValidationFailure(
            "infrastructure_error",
            f"git {' '.join(args)} failed in {repo}: {result.stderr or result.stdout}",
        )
    return result.stdout


def normalized_remote(value: str) -> str:
    value = value.strip().removesuffix(".git")
    if value.startswith("git@"):
        host, path = value[4:].split(":", 1)
        return f"{host}/{path}".lower()
    value = re.sub(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", "", value)
    value = value.split("@")[-1]
    return value.strip("/").lower()


def candidate_environment(runtime_root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in os.environ.items():
        upper = key.upper()
        if (
            upper in SECRET_NAMES
            or upper.endswith("_TOKEN")
            or "SECRET" in upper
            or "PASSWORD" in upper
            or "CREDENTIAL" in upper
        ):
            continue
        result[key] = value
    result["PYTHONPATH"] = str(runtime_root)
    result["PYTHONDONTWRITEBYTECODE"] = "1"
    return result


class Validator:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.control = args.control_root.resolve()
        self.target = args.target_source.resolve()
        self.package = args.package.resolve()
        self.request_path = args.request.resolve()
        self.output = args.output.resolve()
        self.runtime = self.target / "tooling" / "repo-patcher-runtime"
        self.probe = self.control / "tooling" / "repo-patcher-validator" / "runtime_probe.py"
        self.transcript: list[str] = []
        self.checks: list[dict[str, Any]] = []
        self.request: dict[str, Any] = {}
        self.runtime_info: dict[str, Any] = {}
        self.protected_before: dict[str, Any] = {}

    def initialize_artifacts(self) -> None:
        self.output.mkdir(parents=True, exist_ok=True)
        for name in (
            "preflight-explain-before.json", "preflight-explain-after.json",
            "preflight-check-before.json", "preflight-check-after.json",
            "run-a-state.json", "run-b-state.json", "run-a-convergence.json",
            "run-b-convergence.json", "reproducibility.json",
            "protected-planes-before.json", "protected-planes-after.json",
        ):
            write_json(self.output / name, {"status": "not_run"})
        for name in ("applied.patch", "git-diff-binary.patch", "diff-stat.txt"):
            (self.output / name).write_bytes(b"")

    def validate_request(self) -> None:
        try:
            self.request = json.loads(self.request_path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValidationFailure("request_contract_error", f"invalid request JSON: {exc}") from exc
        required = {
            "protocol", "request_id", "repository", "target_sha", "package_sha256",
            "package_size", "trust_plugin", "transport_kind",
        }
        if set(self.request) != required:
            raise ValidationFailure("request_contract_error", "request fields do not match v1 schema")
        if self.request["protocol"] != PROTOCOL or self.request["repository"] != "R3Neer/Mud":
            raise ValidationFailure("request_contract_error", "wrong protocol or repository")
        request_id = self.request["request_id"]
        if not isinstance(request_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}", request_id):
            raise ValidationFailure("request_contract_error", "invalid request_id")
        if not isinstance(self.request["target_sha"], str) or not SHA40.fullmatch(self.request["target_sha"]):
            raise ValidationFailure("request_contract_error", "invalid target_sha")
        if not isinstance(self.request["package_sha256"], str) or not SHA64.fullmatch(self.request["package_sha256"]):
            raise ValidationFailure("request_contract_error", "invalid package_sha256")
        if type(self.request["package_size"]) is not int or self.request["package_size"] < 1:
            raise ValidationFailure("request_contract_error", "invalid package_size")
        if type(self.request["trust_plugin"]) is not bool:
            raise ValidationFailure("request_contract_error", "invalid trust_plugin")
        if self.request["transport_kind"] not in {"zip_base64", "logical_files"}:
            raise ValidationFailure("request_contract_error", "invalid transport_kind")

    def check_package(self) -> None:
        raw = self.package.read_bytes()
        actual_hash = hashlib.sha256(raw).hexdigest()
        if len(raw) != self.request["package_size"] or actual_hash != self.request["package_sha256"]:
            raise ValidationFailure("package_identity_mismatch", "candidate size or SHA-256 changed")
        try:
            zip_info = validate_zip_bytes(raw)
        except PackageSafetyError as exc:
            raise ValidationFailure("unsafe_package", str(exc)) from exc
        shutil.copyfile(self.package, self.output / "candidate.zip")
        shutil.copyfile(self.request_path, self.output / "request.json")
        self.checks.append({"check": "package_identity", "status": "passed", **zip_info})

    def check_sources(self) -> None:
        target_sha = self.request["target_sha"]
        if self.args.target_sha and target_sha != self.args.target_sha:
            raise ValidationFailure("request_contract_error", "request target_sha differs from workflow input")
        for root, expected, label in (
            (self.target, target_sha, "target-source"),
            (self.control, self.args.control_sha, "control"),
        ):
            actual = run_git(root, "rev-parse", "HEAD").strip().lower()
            if actual != expected:
                raise ValidationFailure("wrong_checkout", f"{label} HEAD is {actual}, expected {expected}")
            if run_git(root, "status", "--porcelain=v1", "--untracked-files=all").strip():
                raise ValidationFailure("dirty_protected_plane", f"{label} is not clean")
        origin = run_git(self.target, "remote", "get-url", "origin").strip()
        if normalized_remote(origin) != normalized_remote(self.args.expected_origin):
            raise ValidationFailure("wrong_origin", f"unexpected target origin: {origin}")
        if not self.probe.is_file() or not (self.runtime / "repo_patcher").is_dir():
            raise ValidationFailure("missing_control_or_runtime", "validator or target runtime is missing")

    def record_protected(self, name: str) -> dict[str, Any]:
        value = {
            "control": capture_repository(self.control),
            "target_source": capture_repository(self.target),
        }
        write_json(self.output / name, value)
        return value

    def run_command(self, label: str, argv: list[str], *, cwd: Path | None = None) -> CommandResult:
        result = subprocess.run(
            argv,
            cwd=cwd or self.control,
            env=candidate_environment(self.runtime),
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        command = CommandResult(label, argv, result.returncode, result.stdout, result.stderr)
        self.transcript.extend(
            [f"===== {label} =====", f"argv: {json.dumps(argv, ensure_ascii=False)}",
             f"exit: {result.returncode}", "--- stdout ---", result.stdout,
             "--- stderr ---", result.stderr, ""]
        )
        self.checks.append({"check": label, "status": "passed" if result.returncode == 0 else "failed"})
        return command

    def require_command(self, label: str, argv: list[str], *, cwd: Path | None = None) -> CommandResult:
        result = self.run_command(label, argv, cwd=cwd)
        if result.returncode != 0:
            raise ValidationFailure(
                "candidate_validation_failed",
                f"{label} failed with exit code {result.returncode}\n{result.stderr or result.stdout}",
                command=label,
            )
        return result

    def probe_command(self, command: str, *, repo: Path | None = None) -> list[str]:
        argv = [sys.executable, str(self.probe), command, "--runtime-root", str(self.runtime)]
        if repo is not None:
            argv.extend(["--repo", str(repo)])
        if command != "runtime":
            argv.extend(["--package", str(self.output / "candidate.zip")])
        return argv

    def runtime_and_plugin(self) -> bool:
        runtime = self.require_command("vendored runtime", self.probe_command("runtime"))
        self.runtime_info = json.loads(runtime.stdout)
        package = self.require_command("package metadata", self.probe_command("package"))
        metadata = json.loads(package.stdout)
        plugin = bool(metadata["plugin_present"])
        if plugin and not self.request["trust_plugin"]:
            raise ValidationFailure("plugin_not_authorized", "package contains an unauthorized Python plugin")
        return plugin

    def clone(self, label: str) -> Path:
        destination = self.args.validation_root.resolve() / label / "Mud"
        destination.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["git", "clone", "--no-checkout", "--no-hardlinks", str(self.target), str(destination)],
            text=True, capture_output=True, encoding="utf-8", errors="replace", check=False,
        )
        if result.returncode != 0:
            raise ValidationFailure("infrastructure_error", f"clone {label} failed: {result.stderr}")
        run_git(destination, "config", "core.autocrlf", "false")
        run_git(destination, "config", "core.longpaths", "true")
        run_git(destination, "remote", "set-url", "origin", self.args.expected_origin)
        run_git(destination, "checkout", "--detach", self.request["target_sha"])
        if run_git(destination, "status", "--porcelain=v1", "--untracked-files=all").strip():
            raise ValidationFailure("infrastructure_error", f"clone {label} is dirty")
        return destination

    def repo_patcher(self, command: str, repo: Path | None, plugin: bool, *extra: str) -> list[str]:
        argv = [sys.executable, "-m", "repo_patcher", command, str(self.output / "candidate.zip")]
        if repo is not None:
            argv.extend(["--repo", str(repo)])
        if plugin:
            argv.append("--trust-plugin")
        argv.extend(extra)
        return argv

    def preflight(self, repo: Path, command: str, plugin: bool) -> None:
        before_name = f"preflight-{command}-before.json"
        after_name = f"preflight-{command}-after.json"
        before = capture_repository(repo)
        write_json(self.output / before_name, before)
        result = self.run_command(command, self.repo_patcher(command, repo, plugin))
        after = capture_repository(repo)
        write_json(self.output / after_name, after)
        differences = repository_difference(before, after)
        if differences:
            raise ValidationFailure(
                "unexpected_preflight_side_effect",
                f"{command} modified: {', '.join(differences)}",
                command=command,
            )
        if result.returncode != 0:
            raise ValidationFailure(
                "candidate_validation_failed",
                f"{command} failed with exit code {result.returncode}\n{result.stderr or result.stdout}",
                command=command,
            )

    def apply(self, label: str, repo: Path, plugin: bool) -> dict[str, Any]:
        emit = self.output / ("applied.patch" if label == "run-a" else "run-b-applied.patch")
        self.require_command(
            f"{label} apply",
            self.repo_patcher("apply", repo, plugin, "--emit-diff", str(emit)),
        )
        self.require_command(f"{label} git diff --check", ["git", "diff", "--check"], cwd=repo)
        state = capture_repository(repo)
        write_json(self.output / f"{label}-state.json", state)
        return state

    def convergence(self, label: str, repo: Path) -> dict[str, Any]:
        before = capture_repository(repo)
        result = self.run_command(f"{label} convergence plan", self.probe_command("plan", repo=repo))
        after = capture_repository(repo)
        changed_paths: list[str] | None = None
        if result.returncode == 0:
            changed_paths = json.loads(result.stdout)["changed_paths"]
        differences = repository_difference(before, after)
        evidence = {
            "status": "passed" if result.returncode == 0 and not changed_paths and not differences else "failed",
            "changed_paths": changed_paths,
            "state_differences": differences,
            "before": before,
            "after": after,
        }
        write_json(self.output / f"{label}-convergence.json", evidence)
        if result.returncode != 0:
            raise ValidationFailure(
                "candidate_validation_failed",
                f"{label} convergence planning failed\n{result.stderr or result.stdout}",
                command=f"{label} convergence plan",
            )
        if changed_paths:
            raise ValidationFailure("not_convergent", f"{label} still proposes: {changed_paths}")
        if differences:
            raise ValidationFailure("convergence_side_effect", f"{label} planning modified: {differences}")
        return after

    def compare_runs(self, left: dict[str, Any], right: dict[str, Any]) -> None:
        fields = ["head", "index_semantic", "status_porcelain_z", "diff_binary", "filesystem_tree"]
        differences = [field for field in fields if left[field] != right[field]]
        evidence = {"status": "passed" if not differences else "failed", "differences": differences}
        write_json(self.output / "reproducibility.json", evidence)
        if differences:
            raise ValidationFailure("not_reproducible", f"run-a and run-b differ: {differences}")

    def export_git_evidence(self, repo: Path) -> None:
        diff = subprocess.run(
            ["git", "diff", "--binary", "--no-ext-diff"], cwd=repo, capture_output=True, check=True
        ).stdout
        (self.output / "git-diff-binary.patch").write_bytes(diff)
        stat_text = run_git(repo, "diff", "--stat")
        (self.output / "diff-stat.txt").write_text(stat_text, encoding="utf-8")

    def execute(self) -> None:
        self.initialize_artifacts()
        self.validate_request()
        self.check_package()
        self.check_sources()
        self.protected_before = self.record_protected("protected-planes-before.json")
        plugin = self.runtime_and_plugin()
        self.require_command("package-info", self.repo_patcher("package-info", None, False))
        run_a = self.clone("run-a")
        run_b = self.clone("run-b")
        self.preflight(run_a, "explain", plugin)
        self.preflight(run_a, "check", plugin)
        state_a = self.apply("run-a", run_a, plugin)
        converged_a = self.convergence("run-a", run_a)
        if state_a != converged_a:
            raise ValidationFailure("convergence_side_effect", "run-a state changed during convergence")
        state_b = self.apply("run-b", run_b, plugin)
        converged_b = self.convergence("run-b", run_b)
        if state_b != converged_b:
            raise ValidationFailure("convergence_side_effect", "run-b state changed during convergence")
        self.compare_runs(state_a, state_b)
        self.export_git_evidence(run_a)

    def finish_protected(self) -> None:
        if not self.protected_before:
            return
        after = self.record_protected("protected-planes-after.json")
        differences = [key for key in self.protected_before if self.protected_before[key] != after[key]]
        if differences:
            raise ValidationFailure("protected_plane_modified", f"modified protected planes: {differences}")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Deterministic MUD RepoPatcher candidate validator")
    result.add_argument("--control-root", type=Path, required=True)
    result.add_argument("--target-source", type=Path, required=True)
    result.add_argument("--validation-root", type=Path, required=True)
    result.add_argument("--package", type=Path, required=True)
    result.add_argument("--request", type=Path, required=True)
    result.add_argument("--output", type=Path, required=True)
    result.add_argument("--target-sha")
    result.add_argument("--control-sha", required=True)
    result.add_argument("--workflow-run-id", type=int, required=True)
    result.add_argument("--run-attempt", type=int, required=True)
    result.add_argument("--expected-origin", default="https://github.com/R3Neer/Mud.git")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if not SHA40.fullmatch(args.control_sha):
        raise SystemExit("--control-sha must be a lowercase 40-character SHA")
    if args.target_sha is not None and not SHA40.fullmatch(args.target_sha):
        raise SystemExit("--target-sha must be a lowercase 40-character SHA")
    if args.workflow_run_id < 1 or args.run_attempt < 1:
        raise SystemExit("run identifiers must be positive")
    validator = Validator(args)
    conclusion = "success"
    failure_kind: str | None = None
    preflight_command: str | None = None
    diagnostic = "Validation succeeded."
    try:
        validator.execute()
    except ValidationFailure as exc:
        conclusion = "infrastructure_error" if exc.kind == "infrastructure_error" else "failure"
        failure_kind = exc.kind
        preflight_command = exc.command
        diagnostic = str(exc)
    except Exception as exc:  # defensive artifact production for unexpected failures
        conclusion = "infrastructure_error"
        failure_kind = "unexpected_validator_error"
        diagnostic = f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"
    try:
        validator.finish_protected()
    except ValidationFailure as exc:
        conclusion = "failure"
        failure_kind = exc.kind
        diagnostic = str(exc)
    validator.output.mkdir(parents=True, exist_ok=True)
    (validator.output / "diagnostic.txt").write_text(diagnostic + "\n", encoding="utf-8")
    (validator.output / "transcript.txt").write_text("\n".join(validator.transcript), encoding="utf-8")
    write_json(validator.output / "checks.json", validator.checks)
    request = validator.request
    artifact_files = sorted(
        {path.name for path in validator.output.iterdir() if path.is_file()} | {"result.json"}
    )
    result = {
        "protocol": RESULT_PROTOCOL,
        "request_id": request.get("request_id", "invalid-request"),
        "workflow_run_id": args.workflow_run_id,
        "run_attempt": args.run_attempt,
        "control_sha": args.control_sha,
        "target_sha": request.get("target_sha", args.target_sha or "0" * 40),
        "package_sha256": request.get("package_sha256", "0" * 64),
        "package_size": request.get("package_size", 1),
        "runtime_version": validator.runtime_info.get("version"),
        "conclusion": conclusion,
        "failure_kind": failure_kind,
        "preflight_command": preflight_command,
        "diagnostic": diagnostic,
        "artifact_files": artifact_files,
    }
    write_json(validator.output / "result.json", result)
    return 0 if conclusion == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
