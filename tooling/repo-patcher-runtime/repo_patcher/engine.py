from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from .commands import execute_commands, preflight_commands
from .context import PatchContext
from .errors import ApplyRollbackError, RepoPatcherError
from .gitops import head, run_git, verify_compatibility
from .manifest import load_manifest
from .models import Manifest
from .operations import apply_declarative_operations
from .plugin import load_plugin
from .transaction import RepositoryTransaction


@dataclass
class PatchPlan:
    manifest: Manifest
    context: PatchContext
    has_plugin: bool


@dataclass
class ApplyResult:
    manifest: Manifest
    changed_paths: list[str]
    generators: list[str]
    validators: list[str]
    diff_path: Path | None


def package_digest(patch_root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in patch_root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(patch_root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def build_plan(repo: Path, patch_root: Path, *, require_clean: bool) -> PatchPlan:
    manifest = load_manifest(patch_root)
    verify_compatibility(repo, manifest, require_clean=require_clean)
    ctx = PatchContext(repo, patch_root)
    apply_declarative_operations(ctx, manifest.operations)
    entrypoint = load_plugin(patch_root, manifest)
    if entrypoint is not None:
        try:
            entrypoint(ctx, manifest)
        except RepoPatcherError:
            raise
        except Exception as exc:
            raise RepoPatcherError(f"El plugin falló al preparar el patch: {exc}") from exc
    preflight_commands("generador", manifest.generators, repo, patch_root)
    preflight_commands("validador", manifest.validators, repo, patch_root)
    return PatchPlan(manifest=manifest, context=ctx, has_plugin=entrypoint is not None)


def apply_plan(
    plan: PatchPlan,
    repo: Path,
    patch_root: Path,
    *,
    emit_diff: Path | None = None,
) -> ApplyResult:
    manifest = plan.manifest
    if plan.context.is_already_applied():
        return ApplyResult(manifest, [], [], [], emit_diff)

    transaction = RepositoryTransaction(repo)
    initial_head = transaction.initial_head
    transaction.mark_context_new_paths(plan.context)
    generators_done: list[str] = []
    validators_done: list[str] = []
    try:
        before_commit = transaction.current_paths()
        try:
            plan.context.commit_to_disk()
        finally:
            transaction.record_new_paths_since(before_commit)
        generators_done = execute_commands(
            "generador", manifest.generators, repo, patch_root, transaction=transaction
        )
        if head(repo) != initial_head:
            raise RepoPatcherError("Un generador creó un commit. Los paquetes no pueden mover HEAD.")
        validators_done = execute_commands(
            "validador", manifest.validators, repo, patch_root, transaction=transaction
        )
        whitespace = run_git(repo, "diff", "--check", check=False)
        if whitespace.returncode != 0:
            raise RepoPatcherError(
                "git diff --check detectó problemas:\n"
                f"STDOUT:\n{whitespace.stdout or '(vacío)'}\n"
                f"STDERR:\n{whitespace.stderr or '(vacío)'}"
            )
        if head(repo) != initial_head:
            raise RepoPatcherError("Un validador creó un commit. Los paquetes no pueden mover HEAD.")
        if emit_diff is not None:
            emit_diff = emit_diff.expanduser().resolve()
            emit_diff.parent.mkdir(parents=True, exist_ok=True)
            diff = run_git(repo, "diff", "--binary", "--no-ext-diff").stdout
            temporary = emit_diff.with_name(emit_diff.name + ".tmp")
            temporary.write_text(diff, encoding="utf-8")
            temporary.replace(emit_diff)
    except Exception as primary:
        rollback = transaction.rollback(plan.context)
        raise ApplyRollbackError(primary, rollback) from primary

    changed = run_git(repo, "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    changed_paths = sorted({line[3:] for line in changed if len(line) >= 4})
    return ApplyResult(manifest, changed_paths, generators_done, validators_done, emit_diff)
