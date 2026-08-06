from __future__ import annotations

import os
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .context import PatchContext
from .errors import RollbackReport
from .gitops import head, run_git


@dataclass(frozen=True)
class FileSnapshot:
    path: str
    exists: bool
    kind: str
    content: bytes | str | None
    mode: int | None


def _snapshot_path(repo: Path, relative: str) -> FileSnapshot:
    target = repo / Path(*PurePosixPath(relative).parts)
    if not target.exists() and not target.is_symlink():
        return FileSnapshot(relative, False, "missing", None, None)
    info = target.lstat()
    mode = stat.S_IMODE(info.st_mode)
    if target.is_symlink():
        return FileSnapshot(relative, True, "symlink", os.readlink(target), mode)
    if target.is_file():
        return FileSnapshot(relative, True, "file", target.read_bytes(), mode)
    if target.is_dir():
        return FileSnapshot(relative, True, "directory", None, mode)
    return FileSnapshot(relative, True, "other", None, mode)


def _restore_snapshot(repo: Path, snapshot: FileSnapshot) -> None:
    target = repo / Path(*PurePosixPath(snapshot.path).parts)
    if not snapshot.exists:
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.is_dir():
            target.rmdir()
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if snapshot.kind == "directory":
        target.mkdir(parents=True, exist_ok=True)
    elif snapshot.kind == "symlink":
        if target.exists() or target.is_symlink():
            if target.is_dir() and not target.is_symlink():
                target.rmdir()
            else:
                target.unlink()
        os.symlink(str(snapshot.content), target)
    elif snapshot.kind == "file":
        if target.is_dir() and not target.is_symlink():
            target.rmdir()
        target.write_bytes(snapshot.content if isinstance(snapshot.content, bytes) else b"")
    if snapshot.mode is not None and not target.is_symlink():
        try:
            target.chmod(snapshot.mode)
        except OSError:
            pass


def _split_nul(value: str) -> list[str]:
    return [item for item in value.split("\0") if item]


def _repo_paths(repo: Path) -> set[str]:
    paths: set[str] = set()
    for root, dirs, files in os.walk(repo):
        root_path = Path(root)
        if root_path == repo:
            dirs[:] = [name for name in dirs if name != ".git"]
        relative_root = root_path.relative_to(repo)
        for name in dirs:
            paths.add((relative_root / name).as_posix())
        for name in files:
            paths.add((relative_root / name).as_posix())
    return paths


class RepositoryTransaction:
    """Captura el estado necesario para un rollback limitado y diagnosticable."""

    def __init__(self, repo: Path):
        self.repo = repo.resolve()
        self.initial_head = head(repo)
        self.initial_paths = _repo_paths(repo)
        tracked = _split_nul(run_git(repo, "ls-files", "-z").stdout)
        untracked = _split_nul(
            run_git(repo, "ls-files", "--others", "--exclude-standard", "-z").stdout
        )
        self.tracked = {path: _snapshot_path(repo, path) for path in tracked}
        self.preexisting_untracked = {path: _snapshot_path(repo, path) for path in untracked}
        index_path_raw = run_git(repo, "rev-parse", "--git-path", "index").stdout.strip()
        index_path = Path(index_path_raw)
        if not index_path.is_absolute():
            index_path = (repo / index_path).resolve()
        self.index_path = index_path
        self.index_bytes = index_path.read_bytes() if index_path.exists() else None
        self.attributed_new_paths: set[str] = set()

    def current_paths(self) -> set[str]:
        return _repo_paths(self.repo)

    def mark_context_new_paths(self, context: PatchContext) -> None:
        for path in context.changed_paths():
            if context.original_bytes(path) is None:
                self.attributed_new_paths.add(path)

    def record_new_paths_since(self, before: set[str]) -> None:
        self.attributed_new_paths.update(self.current_paths() - before)

    def rollback(self, context: PatchContext) -> RollbackReport:
        report = RollbackReport()

        try:
            context.restore_original()
            report.add_success("Restauración de archivos registrados")
        except Exception as exc:  # pragma: no cover - exercised by injected failure tests
            report.add_failure(
                "Restauración de archivos registrados",
                f"{type(exc).__name__}: {exc}",
                context.changed_paths(),
            )

        try:
            current = head(self.repo)
            if current != self.initial_head:
                run_git(self.repo, "update-ref", "HEAD", self.initial_head, current)
            report.add_success("Restauración de HEAD", f"HEAD: {self.initial_head}")
        except Exception as exc:
            report.add_failure("Restauración de HEAD", f"{type(exc).__name__}: {exc}")

        tracked_failures: list[str] = []
        tracked_details: list[str] = []
        for path, snapshot in self.tracked.items():
            try:
                _restore_snapshot(self.repo, snapshot)
            except Exception as exc:
                tracked_failures.append(path)
                tracked_details.append(f"{path}: {type(exc).__name__}: {exc}")
        if tracked_failures:
            report.add_failure(
                "Restauración de archivos rastreados",
                "\n".join(tracked_details),
                tracked_failures,
            )
        else:
            report.add_success("Restauración de archivos rastreados", f"{len(self.tracked)} ruta(s)")

        untracked_failures: list[str] = []
        untracked_details: list[str] = []
        for path, snapshot in self.preexisting_untracked.items():
            try:
                _restore_snapshot(self.repo, snapshot)
            except Exception as exc:
                untracked_failures.append(path)
                untracked_details.append(f"{path}: {type(exc).__name__}: {exc}")
        if untracked_failures:
            report.add_failure(
                "Conservación de archivos no rastreados preexistentes",
                "\n".join(untracked_details),
                untracked_failures,
            )
        else:
            report.add_success(
                "Conservación de archivos no rastreados preexistentes",
                f"{len(self.preexisting_untracked)} ruta(s)",
            )

        cleanup_failures: list[str] = []
        cleanup_details: list[str] = []
        candidates = sorted(
            (path for path in self.attributed_new_paths if path not in self.initial_paths),
            key=lambda value: (len(PurePosixPath(value).parts), value),
            reverse=True,
        )
        for path in candidates:
            target = self.repo / Path(*PurePosixPath(path).parts)
            try:
                self._remove_created_path(target)
            except Exception as exc:
                cleanup_failures.append(path)
                cleanup_details.append(f"{path}: {type(exc).__name__}: {exc}")
        if cleanup_failures:
            report.add_failure(
                "Limpieza limitada de rutas nuevas",
                "\n".join(cleanup_details),
                cleanup_failures,
            )
        else:
            report.add_success("Limpieza limitada de rutas nuevas", f"{len(candidates)} ruta(s)")

        try:
            if self.index_bytes is None:
                if self.index_path.exists():
                    self.index_path.unlink()
            else:
                self.index_path.parent.mkdir(parents=True, exist_ok=True)
                self.index_path.write_bytes(self.index_bytes)
            report.add_success("Restauración del índice Git")
        except Exception as exc:
            report.add_failure("Restauración del índice Git", f"{type(exc).__name__}: {exc}")

        return report

    def _remove_created_path(self, target: Path) -> None:
        if not target.exists() and not target.is_symlink():
            return
        if target.is_symlink() or target.is_file():
            target.unlink()
            return
        if target.is_dir():
            try:
                target.rmdir()
            except OSError:
                # Conservador: no borra recursivamente un directorio si contiene rutas
                # que no estén registradas individualmente como creadas.
                remaining = list(target.iterdir())
                if remaining:
                    raise OSError(
                        "el directorio contiene elementos no atribuidos o bloqueados: "
                        + ", ".join(item.name for item in remaining[:10])
                    )
                raise
