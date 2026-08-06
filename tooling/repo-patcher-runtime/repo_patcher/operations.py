from __future__ import annotations

import re
from typing import Any

from .context import PatchContext
from .errors import ManifestError


def _one_key(operation: dict[str, Any], index: int) -> tuple[str, dict[str, Any]]:
    if len(operation) != 1:
        raise ManifestError(f"operations[{index}] debe contener exactamente una operación.")
    name, payload = next(iter(operation.items()))
    if not isinstance(payload, dict):
        raise ManifestError(f"operations[{index}].{name} debe ser un mapa.")
    return name, payload


def _text(payload: dict[str, Any], key: str, where: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str):
        raise ManifestError(f"{where}.{key} debe ser texto.")
    return value


def apply_declarative_operations(ctx: PatchContext, operations: tuple[dict[str, Any], ...]) -> None:
    for index, operation in enumerate(operations, 1):
        name, payload = _one_key(operation, index)
        where = f"operations[{index}].{name}"
        if name == "create":
            path = _text(payload, "path", where)
            if "source" in payload:
                ctx.create_from_patch(path, _text(payload, "source", where))
            else:
                ctx.create_text_file(path, _text(payload, "content", where))
        elif name == "delete":
            ctx.delete_file(_text(payload, "path", where))
        elif name == "replace":
            count = payload.get("count", 1)
            if not isinstance(count, int):
                raise ManifestError(f"{where}.count debe ser entero.")
            ctx.replace_exact(
                _text(payload, "path", where),
                _text(payload, "old", where),
                _text(payload, "new", where),
                count=count,
            )
        elif name == "regex_replace":
            count = payload.get("count", 1)
            raw_flags = payload.get("flags", [])
            if not isinstance(raw_flags, list) or not all(isinstance(item, str) for item in raw_flags):
                raise ManifestError(f"{where}.flags debe ser una lista de textos.")
            flags = 0
            for flag_name in raw_flags:
                try:
                    flags |= getattr(re, flag_name)
                except AttributeError as exc:
                    raise ManifestError(f"Flag regex desconocido: {flag_name}") from exc
            ctx.replace_regex(
                _text(payload, "path", where),
                _text(payload, "pattern", where),
                _text(payload, "replacement", where),
                count=count,
                flags=flags,
            )
        elif name == "append_once":
            ctx.append_once(
                _text(payload, "path", where),
                _text(payload, "marker", where),
                _text(payload, "content", where),
            )
        elif name == "assert_contains":
            ctx.assert_contains(_text(payload, "path", where), _text(payload, "text", where))
        elif name == "assert_not_contains":
            ctx.assert_not_contains(_text(payload, "path", where), _text(payload, "text", where))
        else:
            raise ManifestError(f"Operación declarativa desconocida: {name}")
