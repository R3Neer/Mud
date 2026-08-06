from __future__ import annotations

import contextlib
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Iterator

from .errors import RepoPatcherError


def _safe_extract(zf: zipfile.ZipFile, destination: Path) -> None:
    base = destination.resolve()
    for info in zf.infolist():
        target = (destination / info.filename).resolve()
        try:
            target.relative_to(base)
        except ValueError as exc:
            raise RepoPatcherError(f"El ZIP contiene una ruta insegura: {info.filename}") from exc
    zf.extractall(destination)


def _manifest_root(extracted: Path) -> Path:
    direct = extracted / "patch.yaml"
    if direct.is_file():
        return extracted
    candidates = list(extracted.glob("*/patch.yaml"))
    if len(candidates) == 1:
        return candidates[0].parent
    if not candidates:
        raise RepoPatcherError("No se encontró patch.yaml dentro del paquete.")
    raise RepoPatcherError("El ZIP contiene más de un patch.yaml y no se puede decidir cuál usar.")


@contextlib.contextmanager
def open_patch_source(source: Path) -> Iterator[Path]:
    source = source.expanduser().resolve()
    if source.is_dir():
        if not (source / "patch.yaml").is_file():
            raise RepoPatcherError(f"{source} no contiene patch.yaml.")
        yield source
        return
    if not source.is_file():
        raise RepoPatcherError(f"No existe el paquete: {source}")
    if not zipfile.is_zipfile(source):
        raise RepoPatcherError("El paquete debe ser un directorio o un archivo ZIP.")
    temp = Path(tempfile.mkdtemp(prefix="repo-patcher-"))
    try:
        with zipfile.ZipFile(source) as zf:
            _safe_extract(zf, temp)
        yield _manifest_root(temp)
    finally:
        shutil.rmtree(temp, ignore_errors=True)
