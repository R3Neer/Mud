from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from .errors import CompatibilityError, RepoPatcherError
from .models import Manifest


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            text=True,
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        raise RepoPatcherError("No se encontró Git en PATH.") from exc
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RepoPatcherError(f"Git falló: git {' '.join(args)}\n{detail}")
    return result


def find_repo(explicit: Path | None, start: Path | None = None) -> Path:
    candidate = (explicit or start or Path.cwd()).expanduser().resolve()
    if explicit is not None and not candidate.exists():
        raise RepoPatcherError(f"La ruta de repo no existe: {candidate}")
    probe = candidate if candidate.is_dir() else candidate.parent
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=probe,
            text=True,
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        raise RepoPatcherError("No se encontró Git en PATH.") from exc
    if result.returncode != 0:
        raise RepoPatcherError(
            f"No se encontró una repo Git desde {probe}.\n"
            "Entra primero en la repo con Set-Location o usa --repo RUTA."
        )
    return Path(result.stdout.strip()).resolve()


def head(repo: Path) -> str:
    return run_git(repo, "rev-parse", "HEAD").stdout.strip()


def status_porcelain(repo: Path) -> str:
    return run_git(repo, "status", "--porcelain=v1", "--untracked-files=all").stdout


def normalize_remote(value: str) -> str:
    value = value.strip().removesuffix(".git")
    if value.startswith("git@"):
        host, path = value[4:].split(":", 1)
        return f"{host}/{path}".lower()
    value = re.sub(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", "", value)
    value = value.split("@")[-1]
    return value.strip("/").lower()


def origin_remote(repo: Path) -> str | None:
    result = run_git(repo, "remote", "get-url", "origin", check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def verify_compatibility(repo: Path, manifest: Manifest, *, require_clean: bool) -> None:
    repo_name = repo.name.lower()
    if manifest.repository.names and repo_name not in {name.lower() for name in manifest.repository.names}:
        expected = ", ".join(manifest.repository.names)
        raise CompatibilityError(f"Repo incorrecta: se esperaba nombre {expected}; se encontró {repo.name}.")

    if manifest.repository.remotes:
        actual = origin_remote(repo)
        normalized_expected = {normalize_remote(item) for item in manifest.repository.remotes}
        if actual is None or normalize_remote(actual) not in normalized_expected:
            expected = ", ".join(manifest.repository.remotes)
            raise CompatibilityError(
                f"Remote origin incompatible.\nEsperado: {expected}\nEncontrado: {actual or '(sin origin)'}"
            )

    current = head(repo)
    if manifest.compatibility.exact_heads and current not in manifest.compatibility.exact_heads:
        expected = "\n  ".join(manifest.compatibility.exact_heads)
        raise CompatibilityError(
            f"HEAD incompatible: {current}\nEl paquete admite exactamente:\n  {expected}"
        )

    ancestor = manifest.compatibility.required_ancestor
    if ancestor:
        result = run_git(repo, "merge-base", "--is-ancestor", ancestor, "HEAD", check=False)
        if result.returncode != 0:
            raise CompatibilityError(
                f"La revisión requerida {ancestor} no es antepasado del HEAD actual {current}."
            )

    for relative in manifest.compatibility.required_files:
        if not (repo / relative).exists():
            raise CompatibilityError(f"Falta un archivo requerido por el paquete: {relative}")

    if require_clean and manifest.compatibility.clean_worktree:
        dirty = status_porcelain(repo).strip()
        if dirty:
            preview = "\n".join(dirty.splitlines()[:20])
            raise CompatibilityError(
                "El árbol de trabajo no está limpio. No se ha modificado nada.\n\n"
                f"Cambios detectados:\n{preview}\n\n"
                "Confirma, guarda con git stash o descarta esos cambios antes de aplicar el paquete."
            )



def clean_worktree_contract(repo: Path) -> str:
    """Devuelve el estado usado por el preflight.

    Equivale a ``git status --porcelain=v1 --untracked-files=all``: incluye
    cambios rastreados staged/unstaged y archivos no rastreados no ignorados.
    No enumera archivos ignorados y delega en Git la representación de
    submódulos.
    """
    return status_porcelain(repo)


def ensure_runtime() -> list[str]:
    lines = [f"Python: {sys.version.split()[0]} ({sys.executable})"]
    git = shutil.which("git")
    lines.append(f"Git: {git or 'NO ENCONTRADO'}")
    lines.append(f"Sistema: {os.name}")
    return lines
