from __future__ import annotations

import base64
import hashlib
import os
import stat
import subprocess
from pathlib import Path
from typing import Any


class SnapshotError(RuntimeError):
    pass


def _git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).decode("utf-8", errors="replace").strip()
        raise SnapshotError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout


def _blob(value: bytes) -> dict[str, Any]:
    return {
        "encoding": "base64",
        "size": len(value),
        "sha256": hashlib.sha256(value).hexdigest(),
        "data": base64.b64encode(value).decode("ascii"),
    }


def _file_digest(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            size += len(chunk)
            digest.update(chunk)
    return size, digest.hexdigest()


def _git_modes(repo: Path) -> dict[str, str]:
    modes: dict[str, str] = {}
    raw = _git(repo, "ls-files", "--stage", "-z")
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode = metadata.split(b" ", 1)[0].decode("ascii")
        modes[path.decode("utf-8", errors="surrogateescape")] = mode
    return modes


def filesystem_tree(root: Path, *, exclude_git: bool = True) -> list[dict[str, Any]]:
    root = root.resolve()
    tracked_modes = _git_modes(root) if (root / ".git").exists() else {}
    entries: list[dict[str, Any]] = []

    def visit(directory: Path) -> None:
        with os.scandir(directory) as iterator:
            children = sorted(iterator, key=lambda item: item.name.casefold())
        for child in children:
            if exclude_git and directory == root and child.name == ".git":
                continue
            path = Path(child.path)
            relative = path.relative_to(root).as_posix()
            info = child.stat(follow_symlinks=False)
            executable = tracked_modes.get(relative) == "100755" or bool(
                stat.S_IMODE(info.st_mode) & stat.S_IXUSR
            )
            if child.is_symlink():
                entries.append(
                    {
                        "relative_path": relative,
                        "entry_type": "symlink",
                        "size": 0,
                        "sha256": None,
                        "symlink_target": os.readlink(path),
                        "executable_bit": executable,
                    }
                )
            elif child.is_dir(follow_symlinks=False):
                entries.append(
                    {
                        "relative_path": relative,
                        "entry_type": "directory",
                        "size": 0,
                        "sha256": None,
                        "symlink_target": None,
                        "executable_bit": executable,
                    }
                )
                visit(path)
            elif child.is_file(follow_symlinks=False):
                size, digest = _file_digest(path)
                entries.append(
                    {
                        "relative_path": relative,
                        "entry_type": "file",
                        "size": size,
                        "sha256": digest,
                        "symlink_target": None,
                        "executable_bit": executable,
                    }
                )
            else:
                entries.append(
                    {
                        "relative_path": relative,
                        "entry_type": "other",
                        "size": 0,
                        "sha256": None,
                        "symlink_target": None,
                        "executable_bit": executable,
                    }
                )

    visit(root)
    return sorted(entries, key=lambda item: item["relative_path"])


def _index_path(repo: Path) -> Path:
    raw = _git(repo, "rev-parse", "--git-path", "index").decode("utf-8").strip()
    path = Path(raw)
    return path if path.is_absolute() else (repo / path).resolve()


def capture_repository(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    head = _git(repo, "rev-parse", "HEAD").decode("ascii").strip()
    index_semantic = _git(repo, "ls-files", "--stage", "-z")
    status = _git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    diff = _git(repo, "diff", "--binary", "--no-ext-diff")
    tree = filesystem_tree(repo)
    index_path = _index_path(repo)
    index_bytes = index_path.read_bytes() if index_path.exists() else b""
    return {
        "head": head,
        "index_physical_sha256": hashlib.sha256(index_bytes).hexdigest(),
        "index_physical_size": len(index_bytes),
        "index_semantic": _blob(index_semantic),
        "status_porcelain_z": _blob(status),
        "diff_binary": _blob(diff),
        "filesystem_tree": tree,
    }


def repository_difference(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    return sorted(key for key in before if before.get(key) != after.get(key))
