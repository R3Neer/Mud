from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from .errors import PatchConflictError


@dataclass(frozen=True)
class PlannedChange:
    path: str
    action: str
    detail: str


class PatchContext:
    """Editor virtual transaccional ofrecido a operations y plugins.

    Los plugins deben usar esta API y no escribir directamente en disco.
    """

    def __init__(self, repo: Path, patch_root: Path):
        self.repo = repo.resolve()
        self.patch_root = patch_root.resolve()
        self._original: dict[str, bytes | None] = {}
        self._virtual: dict[str, bytes | None] = {}
        self.changes: list[PlannedChange] = []
        self.notes: list[str] = []

    def _path(self, relative: str) -> tuple[str, Path]:
        posix = PurePosixPath(relative.replace("\\", "/"))
        if posix.is_absolute() or ".." in posix.parts:
            raise PatchConflictError(f"Ruta no permitida fuera de la repo: {relative}")
        key = posix.as_posix()
        target = (self.repo / Path(*posix.parts)).resolve()
        try:
            target.relative_to(self.repo)
        except ValueError as exc:
            raise PatchConflictError(f"Ruta no permitida fuera de la repo: {relative}") from exc
        return key, target

    def _load(self, relative: str) -> tuple[str, bytes | None]:
        key, path = self._path(relative)
        if key not in self._original:
            raw = path.read_bytes() if path.exists() else None
            self._original[key] = raw
            self._virtual[key] = raw
        return key, self._virtual[key]

    def exists(self, relative: str) -> bool:
        _key, raw = self._load(relative)
        return raw is not None

    def read_bytes(self, relative: str) -> bytes:
        _key, raw = self._load(relative)
        if raw is None:
            raise PatchConflictError(f"No existe el archivo requerido: {relative}")
        return raw

    def read_text(self, relative: str, encoding: str = "utf-8") -> str:
        try:
            return self.read_bytes(relative).decode(encoding)
        except UnicodeError as exc:
            raise PatchConflictError(f"{relative} no se pudo leer como {encoding}: {exc}") from exc

    def write_bytes(self, relative: str, content: bytes, *, action: str = "modificar", detail: str = "") -> None:
        key, old = self._load(relative)
        if old == content:
            return
        self._virtual[key] = content
        self.changes.append(PlannedChange(key, action, detail))

    def write_text(self, relative: str, content: str, encoding: str = "utf-8") -> None:
        self.write_bytes(relative, content.encode(encoding), action="modificar", detail="reemplazo completo")

    def create_text_file(self, relative: str, content: str, *, encoding: str = "utf-8") -> None:
        key, old = self._load(relative)
        new = content.encode(encoding)
        if old is None:
            self._virtual[key] = new
            self.changes.append(PlannedChange(key, "crear", "archivo nuevo"))
            return
        if old == new:
            return
        raise PatchConflictError(f"No se puede crear {relative}: ya existe con contenido diferente.")

    def create_from_patch(self, relative: str, source: str, *, encoding: str = "utf-8") -> None:
        source_path = (self.patch_root / source).resolve()
        try:
            source_path.relative_to(self.patch_root)
        except ValueError as exc:
            raise PatchConflictError(f"Fuente fuera del paquete: {source}") from exc
        if not source_path.is_file():
            raise PatchConflictError(f"No existe el archivo fuente del paquete: {source}")
        self.create_text_file(relative, source_path.read_text(encoding=encoding), encoding=encoding)

    def delete_file(self, relative: str) -> None:
        key, old = self._load(relative)
        if old is None:
            return
        self._virtual[key] = None
        self.changes.append(PlannedChange(key, "eliminar", "archivo existente"))

    def replace_exact(self, relative: str, old: str, new: str, *, count: int = 1) -> None:
        text = self.read_text(relative)
        occurrences = text.count(old)
        if occurrences == 0:
            if new and new in text:
                return
            raise PatchConflictError(
                f"{relative}: no se encontró el fragmento exacto esperado.\n"
                f"Inicio del fragmento: {old[:180]!r}"
            )
        if count >= 0 and occurrences != count:
            raise PatchConflictError(
                f"{relative}: el fragmento aparece {occurrences} veces; se esperaban {count}."
            )
        limit = count if count >= 0 else -1
        updated = text.replace(old, new, limit)
        self.write_bytes(relative, updated.encode("utf-8"), action="modificar", detail="reemplazo exacto")

    def replace_regex(
        self,
        relative: str,
        pattern: str,
        replacement: str,
        *,
        count: int = 1,
        flags: int = 0,
    ) -> None:
        text = self.read_text(relative)
        updated, substitutions = re.subn(pattern, replacement, text, count=count, flags=flags)
        if substitutions == 0:
            raise PatchConflictError(f"{relative}: no coincidió la expresión regular: {pattern}")
        self.write_bytes(relative, updated.encode("utf-8"), action="modificar", detail="reemplazo regex")

    def append_once(self, relative: str, marker: str, content: str) -> None:
        text = self.read_text(relative)
        if marker in text:
            return
        updated = text.rstrip() + "\n\n" + content.strip() + "\n"
        self.write_bytes(relative, updated.encode("utf-8"), action="modificar", detail="añadir sección")

    def assert_contains(self, relative: str, fragment: str) -> None:
        if fragment not in self.read_text(relative):
            raise PatchConflictError(f"{relative}: falta el fragmento requerido {fragment[:180]!r}")

    def assert_not_contains(self, relative: str, fragment: str) -> None:
        if fragment in self.read_text(relative):
            raise PatchConflictError(f"{relative}: contiene un fragmento prohibido {fragment[:180]!r}")

    def load_yaml(self, relative: str) -> Any:
        try:
            return yaml.safe_load(self.read_text(relative))
        except yaml.YAMLError as exc:
            raise PatchConflictError(f"YAML inválido en {relative}: {exc}") from exc

    def save_yaml(self, relative: str, value: Any, *, sort_keys: bool = False) -> None:
        text = yaml.safe_dump(value, sort_keys=sort_keys, allow_unicode=True, width=120)
        self.write_bytes(relative, text.encode("utf-8"), action="modificar", detail="actualización YAML")

    def note(self, text: str) -> None:
        self.notes.append(text)

    def original_bytes(self, relative: str) -> bytes | None:
        """Devuelve el contenido original registrado para una ruta virtual."""
        key, _raw = self._load(relative)
        return self._original[key]

    def changed_paths(self) -> list[str]:
        return sorted(key for key, value in self._virtual.items() if value != self._original[key])

    def is_already_applied(self) -> bool:
        return not self.changed_paths()

    def commit_to_disk(self) -> None:
        for key in self.changed_paths():
            target = self.repo / Path(*PurePosixPath(key).parts)
            raw = self._virtual[key]
            if raw is None:
                if target.exists():
                    target.unlink()
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)

    def restore_original(self) -> None:
        """Restaura también archivos ignorados que Git no puede recuperar."""
        for key, raw in self._original.items():
            target = self.repo / Path(*PurePosixPath(key).parts)
            if raw is None:
                if target.exists() and target.is_file():
                    target.unlink()
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
