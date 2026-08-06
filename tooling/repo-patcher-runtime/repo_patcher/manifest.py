from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .errors import ManifestError
from .models import CommandSpec, CompatibilitySpec, Manifest, PluginSpec, RepositorySpec


def _mapping(value: Any, where: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ManifestError(f"{where} debe ser un mapa YAML.")
    return value


def _string_list(value: Any, where: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ManifestError(f"{where} debe ser texto o una lista de textos.")
    return tuple(value)


def _commands(value: Any, where: str) -> tuple[CommandSpec, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ManifestError(f"{where} debe ser una lista.")
    result: list[CommandSpec] = []
    for index, item in enumerate(value, 1):
        data = _mapping(item, f"{where}[{index}]")
        raw_command = data.get("command")
        if not isinstance(raw_command, list) or not raw_command or not all(isinstance(part, str) for part in raw_command):
            raise ManifestError(f"{where}[{index}].command debe ser una lista no vacía de textos.")
        name = data.get("name") or " ".join(raw_command)
        if not isinstance(name, str):
            raise ManifestError(f"{where}[{index}].name debe ser texto.")
        cwd = data.get("cwd", ".")
        if not isinstance(cwd, str):
            raise ManifestError(f"{where}[{index}].cwd debe ser texto.")
        env = _mapping(data.get("env"), f"{where}[{index}].env")
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items()):
            raise ManifestError(f"{where}[{index}].env solo admite pares de texto.")
        result.append(CommandSpec(name=name, command=tuple(raw_command), cwd=cwd, env=dict(env)))
    return tuple(result)


def load_manifest(patch_root: Path) -> Manifest:
    path = patch_root / "patch.yaml"
    if not path.is_file():
        raise ManifestError(f"El paquete no contiene {path.name}.")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ManifestError(f"No se pudo leer {path}: {exc}") from exc
    data = _mapping(raw, "patch.yaml")

    schema = data.get("schema", 1)
    if schema != 1:
        raise ManifestError(f"Schema no soportado: {schema}. Esta versión admite schema: 1.")

    patch_id = data.get("id")
    title = data.get("title")
    if not isinstance(patch_id, str) or not patch_id.strip():
        raise ManifestError("patch.yaml necesita un id no vacío.")
    if not isinstance(title, str) or not title.strip():
        raise ManifestError("patch.yaml necesita un title no vacío.")
    version = data.get("version", "1")
    if not isinstance(version, (str, int, float)):
        raise ManifestError("version debe ser texto o número.")
    description = data.get("description", "")
    if not isinstance(description, str):
        raise ManifestError("description debe ser texto.")

    repo_raw = _mapping(data.get("repository"), "repository")
    repository = RepositorySpec(
        names=_string_list(repo_raw.get("names") or repo_raw.get("name"), "repository.names"),
        remotes=_string_list(repo_raw.get("remotes") or repo_raw.get("remote"), "repository.remotes"),
    )

    compat_raw = _mapping(data.get("compatibility"), "compatibility")
    clean = compat_raw.get("clean_worktree", True)
    if not isinstance(clean, bool):
        raise ManifestError("compatibility.clean_worktree debe ser true o false.")
    required_ancestor = compat_raw.get("required_ancestor")
    if required_ancestor is not None and not isinstance(required_ancestor, str):
        raise ManifestError("compatibility.required_ancestor debe ser texto.")
    compatibility = CompatibilitySpec(
        clean_worktree=clean,
        exact_heads=_string_list(compat_raw.get("exact_heads") or compat_raw.get("exact_head"), "compatibility.exact_heads"),
        required_ancestor=required_ancestor,
        required_files=_string_list(compat_raw.get("required_files"), "compatibility.required_files"),
    )

    plugin_raw = data.get("plugin")
    plugin: PluginSpec | None = None
    if plugin_raw is not None:
        plugin_data = _mapping(plugin_raw, "plugin")
        file = plugin_data.get("file")
        entrypoint = plugin_data.get("entrypoint", "apply")
        if not isinstance(file, str) or not file:
            raise ManifestError("plugin.file debe ser texto no vacío.")
        if not isinstance(entrypoint, str) or not entrypoint:
            raise ManifestError("plugin.entrypoint debe ser texto no vacío.")
        plugin = PluginSpec(file=file, entrypoint=entrypoint)

    operations = data.get("operations", [])
    if not isinstance(operations, list) or not all(isinstance(item, dict) for item in operations):
        raise ManifestError("operations debe ser una lista de mapas.")
    if plugin is None and not operations:
        raise ManifestError("El paquete debe declarar operations, plugin o ambos.")

    return Manifest(
        source=path,
        schema=schema,
        patch_id=patch_id,
        version=str(version),
        title=title,
        description=description,
        repository=repository,
        compatibility=compatibility,
        plugin=plugin,
        operations=tuple(operations),
        generators=_commands(data.get("generators"), "generators"),
        validators=_commands(data.get("validators"), "validators"),
    )
