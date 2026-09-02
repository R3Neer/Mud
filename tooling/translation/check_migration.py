from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROFILE = Path(__file__).with_name("mud-es-en.toml")


def run(command: list[str]) -> int:
    print("+ " + subprocess.list2cmdline(command))
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Mud's translation and editorial gates.")
    parser.add_argument("candidate", nargs="?", type=Path, default=Path("README.md"))
    parser.add_argument("--source", type=Path, help="Spanish source paired with the translated candidate.")
    parser.add_argument("--r3translate", help="Path to the r3translate executable.")
    arguments = parser.parse_args()

    executable = arguments.r3translate or os.environ.get("R3TRANSLATE") or shutil.which("r3translate")
    if not executable:
        print("ERROR: r3translate was not found. Install R3Translate v0.1.0 or pass --r3translate.", file=sys.stderr)
        return 2

    candidate = arguments.candidate if arguments.candidate.is_absolute() else ROOT / arguments.candidate
    translation = [executable, "--format", "json", "check", str(candidate), "--profile", str(PROFILE)]
    if arguments.source:
        source = arguments.source if arguments.source.is_absolute() else ROOT / arguments.source
        translation.extend(["--source", str(source)])

    commands = [
        [sys.executable, str(Path(__file__).with_name("render_glossary.py")), "--check"],
        translation,
        [sys.executable, str(ROOT / "gobierno" / "validate_temporaries.py")],
        [sys.executable, str(ROOT / "gobierno" / "validate_spec_editorial.py")],
    ]
    result = 0
    for command in commands:
        code = run(command)
        if code and not result:
            result = code
    if result:
        return result
    print("OK: perfil, glosario, traducción representativa y barreras editoriales")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
