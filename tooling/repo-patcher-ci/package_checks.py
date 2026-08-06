from __future__ import annotations

import argparse
import sys
from pathlib import Path

from repo_patcher.engine import build_plan
from repo_patcher.manifest import load_manifest
from repo_patcher.patch_source import open_patch_source


def plugin_command(args: argparse.Namespace) -> int:
    package = Path(args.package).expanduser().resolve()
    with open_patch_source(package) as root:
        present = load_manifest(root).plugin is not None
    print("true" if present else "false")
    return 0


def idempotence_command(args: argparse.Namespace) -> int:
    repo = Path(args.repo).expanduser().resolve()
    package = Path(args.package).expanduser().resolve()
    with open_patch_source(package) as root:
        plan = build_plan(repo, root, require_clean=False)
        changed = plan.context.changed_paths()
    if changed:
        print("Package is not idempotent; a second plan still proposes:", file=sys.stderr)
        for path in changed:
            print(f"  {path}", file=sys.stderr)
        return 1
    print("Second plan is a no-op.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Runtime-backed checks used by the MUD repo-patcher CI workflow."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    plugin = sub.add_parser("plugin", help="print whether the package declares a Python plugin")
    plugin.add_argument("--package", required=True)
    plugin.set_defaults(func=plugin_command)

    idempotence = sub.add_parser(
        "idempotence", help="fail if a second in-memory plan still proposes changed paths"
    )
    idempotence.add_argument("--repo", required=True)
    idempotence.add_argument("--package", required=True)
    idempotence.set_defaults(func=idempotence_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
