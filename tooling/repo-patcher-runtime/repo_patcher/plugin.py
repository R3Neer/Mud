from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable

from .context import PatchContext
from .errors import ManifestError, RepoPatcherError
from .models import Manifest


def load_plugin(patch_root: Path, manifest: Manifest) -> Callable[[PatchContext, Manifest], None] | None:
    spec_data = manifest.plugin
    if spec_data is None:
        return None
    path = (patch_root / spec_data.file).resolve()
    try:
        path.relative_to(patch_root.resolve())
    except ValueError as exc:
        raise ManifestError(f"plugin.file sale del paquete: {spec_data.file}") from exc
    if not path.is_file():
        raise ManifestError(f"No existe el plugin: {spec_data.file}")
    module_name = f"repo_patcher_plugin_{manifest.patch_id.replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RepoPatcherError(f"No se pudo cargar el plugin {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise RepoPatcherError(f"El plugin falló al cargarse: {exc}") from exc
    entrypoint = getattr(module, spec_data.entrypoint, None)
    if not callable(entrypoint):
        raise ManifestError(
            f"El plugin {spec_data.file} no define una función invocable {spec_data.entrypoint}(ctx, manifest)."
        )
    return entrypoint
