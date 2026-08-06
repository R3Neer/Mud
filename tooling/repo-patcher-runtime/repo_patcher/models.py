from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CommandSpec:
    name: str
    command: tuple[str, ...]
    cwd: str = "."
    env: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PluginSpec:
    file: str
    entrypoint: str = "apply"


@dataclass(frozen=True)
class RepositorySpec:
    names: tuple[str, ...] = ()
    remotes: tuple[str, ...] = ()


@dataclass(frozen=True)
class CompatibilitySpec:
    clean_worktree: bool = True
    exact_heads: tuple[str, ...] = ()
    required_ancestor: str | None = None
    required_files: tuple[str, ...] = ()


@dataclass(frozen=True)
class Manifest:
    source: Path
    schema: int
    patch_id: str
    version: str
    title: str
    description: str
    repository: RepositorySpec
    compatibility: CompatibilitySpec
    plugin: PluginSpec | None
    operations: tuple[dict[str, Any], ...]
    generators: tuple[CommandSpec, ...]
    validators: tuple[CommandSpec, ...]
