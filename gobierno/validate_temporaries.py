from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

TEMP_KEYS = {
    "temporary",
    "temporary-reason",
    "temporary-delete-when",
    "temporary-delete-after",
}
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class Temporary:
    path: Path
    reason: str
    delete_when: str
    delete_after: date | None


def scalar(raw: str) -> object:
    raw = raw.strip()
    if raw == "true":
        return True
    if raw == "false":
        return False
    if raw.startswith('"') and raw.endswith('"'):
        return json.loads(raw)
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1].replace("''", "'")
    return raw


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, object] = {}
    for line in text[4:end].splitlines():
        if not line or line.startswith((" ", "\t", "#")) or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        if key in TEMP_KEYS:
            result[key] = scalar(raw)
    return result


def markdown_files(root: Path) -> list[Path]:
    try:
        completed = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                "*.md",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return sorted(path for path in root.rglob("*.md") if ".git" not in path.parts)
    paths = (root / item.decode("utf-8") for item in completed.stdout.split(b"\0") if item)
    return sorted(path for path in paths if path.is_file())


def validate(root: Path) -> tuple[list[Temporary], list[str]]:
    active: list[Temporary] = []
    errors: list[str] = []
    today = date.today()

    for path in markdown_files(root):
        data = frontmatter(path)
        present = TEMP_KEYS.intersection(data)
        if not present:
            continue
        rel = path.relative_to(root)
        flag = data.get("temporary")

        if flag is False:
            errors.append(f"{rel}: no se admite temporary: false; elimina las propiedades temporary-* si el archivo es permanente")
            continue
        if flag is not True:
            errors.append(f"{rel}: las propiedades temporary-* requieren temporary: true")
            continue

        reason = data.get("temporary-reason")
        delete_when = data.get("temporary-delete-when")
        reason_text = reason.strip() if isinstance(reason, str) else ""
        when_text = delete_when.strip() if isinstance(delete_when, str) else ""
        if not reason_text:
            errors.append(f"{rel}: falta temporary-reason no vacío")
        if not when_text:
            errors.append(f"{rel}: falta temporary-delete-when no vacío")

        deadline: date | None = None
        raw_deadline = data.get("temporary-delete-after")
        if raw_deadline is not None:
            if not isinstance(raw_deadline, str) or not ISO_DATE.fullmatch(raw_deadline):
                errors.append(f"{rel}: temporary-delete-after debe usar YYYY-MM-DD")
            else:
                try:
                    deadline = date.fromisoformat(raw_deadline)
                except ValueError:
                    errors.append(f"{rel}: temporary-delete-after no es una fecha válida")
                else:
                    if today > deadline:
                        errors.append(f"{rel}: temporary-delete-after venció el {deadline.isoformat()}")

        active.append(Temporary(rel, reason_text, when_text, deadline))

    return active, errors


def print_inventory(active: list[Temporary]) -> None:
    print("Temporales activos:")
    if not active:
        print("  ninguno")
        return
    for item in sorted(active, key=lambda value: str(value.path)):
        deadline = item.delete_after.isoformat() if item.delete_after else "—"
        print(f"- {item.path}")
        print(f"  motivo: {item.reason or '[FALTA]'}")
        print(f"  eliminar cuando: {item.delete_when or '[FALTA]'}")
        print(f"  fecha límite: {deadline}")
    print("Revisión semántica obligatoria: comprueba si alguna condición 'eliminar cuando' ya se cumple.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida documentos temporales intencionadamente versionados.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    root = args.root.resolve()
    active, errors = validate(root)
    print_inventory(active)
    if errors:
        print("Errores:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
