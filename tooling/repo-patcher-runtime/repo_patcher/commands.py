from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Protocol

from .errors import CommandError
from .models import CommandSpec


class CommandTransaction(Protocol):
    def current_paths(self) -> set[str]: ...
    def record_new_paths_since(self, before: set[str]) -> None: ...


def _expand(value: str, repo: Path, patch_root: Path) -> str:
    return (
        value.replace("{python}", sys.executable)
        .replace("{repo}", str(repo))
        .replace("{patch}", str(patch_root))
    )


def preflight_commands(kind: str, commands: tuple[CommandSpec, ...], repo: Path, patch_root: Path) -> None:
    for spec in commands:
        argv = [_expand(part, repo, patch_root) for part in spec.command]
        cwd = (repo / _expand(spec.cwd, repo, patch_root)).resolve()
        try:
            cwd.relative_to(repo)
        except ValueError as exc:
            raise CommandError(
                kind=kind,
                name=spec.name,
                argv=argv,
                returncode=-1,
                stdout="",
                stderr=f"cwd fuera de la repo: {cwd}",
            ) from exc
        if not cwd.is_dir():
            raise CommandError(
                kind=kind,
                name=spec.name,
                argv=argv,
                returncode=-1,
                stdout="",
                stderr=f"no existe el directorio de trabajo {cwd}",
            )
        executable = argv[0]
        has_separator = any(sep in executable for sep in ("/", "\\"))
        if has_separator:
            if not Path(executable).exists():
                raise CommandError(
                    kind=kind,
                    name=spec.name,
                    argv=argv,
                    returncode=-1,
                    stdout="",
                    stderr=f"no existe el ejecutable {executable}",
                )
        elif shutil.which(executable) is None:
            raise CommandError(
                kind=kind,
                name=spec.name,
                argv=argv,
                returncode=-1,
                stdout="",
                stderr=f"no se encontró {executable} en PATH",
            )


def execute_commands(
    kind: str,
    commands: tuple[CommandSpec, ...],
    repo: Path,
    patch_root: Path,
    *,
    transaction: CommandTransaction | None = None,
) -> list[str]:
    completed: list[str] = []
    for spec in commands:
        argv = [_expand(part, repo, patch_root) for part in spec.command]
        cwd = (repo / _expand(spec.cwd, repo, patch_root)).resolve()
        try:
            cwd.relative_to(repo)
        except ValueError as exc:
            raise CommandError(
                kind=kind,
                name=spec.name,
                argv=argv,
                returncode=-1,
                stdout="",
                stderr=f"cwd fuera de la repo: {cwd}",
            ) from exc
        env = os.environ.copy()
        env.update({key: _expand(value, repo, patch_root) for key, value in spec.env.items()})
        before = transaction.current_paths() if transaction is not None else set()
        try:
            result = subprocess.run(
                argv,
                cwd=cwd,
                env=env,
                text=True,
                capture_output=True,
                check=False,
                encoding="utf-8",
                errors="replace",
            )
        finally:
            if transaction is not None:
                transaction.record_new_paths_since(before)
        if result.returncode != 0:
            raise CommandError(
                kind=kind,
                name=spec.name,
                argv=argv,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
            )
        completed.append(spec.name)
    return completed
