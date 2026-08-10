from __future__ import annotations

import argparse
import json
from pathlib import Path


def verify_runtime(runtime_root: Path) -> dict[str, object]:
    import repo_patcher

    runtime_root = runtime_root.resolve()
    expected_package = (runtime_root / "repo_patcher").resolve()
    module_file = Path(repo_patcher.__file__).resolve()
    try:
        module_file.relative_to(expected_package)
    except ValueError as exc:
        raise RuntimeError(
            f"repo_patcher was imported from {module_file}, expected {expected_package}"
        ) from exc
    if repo_patcher.__version__ != "0.2.0":
        raise RuntimeError(f"expected RepoPatcher 0.2.0, found {repo_patcher.__version__}")
    return {"version": repo_patcher.__version__, "module_file": str(module_file)}


def package_metadata(package: Path) -> dict[str, object]:
    from repo_patcher.manifest import load_manifest
    from repo_patcher.patch_source import open_patch_source

    with open_patch_source(package.resolve()) as patch_root:
        manifest = load_manifest(patch_root)
        return {
            "patch_id": manifest.patch_id,
            "plugin_present": manifest.plugin is not None,
        }


def plan(repo: Path, package: Path) -> dict[str, object]:
    from repo_patcher.engine import build_plan
    from repo_patcher.patch_source import open_patch_source

    with open_patch_source(package.resolve()) as patch_root:
        result = build_plan(repo.resolve(), patch_root, require_clean=False)
        return {"changed_paths": result.context.changed_paths()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("runtime", "package", "plan"))
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--package", type=Path)
    args = parser.parse_args()
    runtime = verify_runtime(args.runtime_root)
    if args.command == "runtime":
        value = runtime
    elif args.command == "package":
        if args.package is None:
            parser.error("--package is required")
        value = {**runtime, **package_metadata(args.package)}
    else:
        if args.package is None or args.repo is None:
            parser.error("--package and --repo are required")
        value = {**runtime, **plan(args.repo, args.package)}
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
