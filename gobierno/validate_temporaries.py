from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tooling.cli_support import (  # noqa: E402
    HelpCatalogue,
    MudArgumentParser,
    add_presentation_arguments,
    failure,
    parse_cli,
)

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


def markdown_metadata(path: Path) -> dict[str, object]:
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


def candidate_files(root: Path) -> list[Path]:
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
                "*.toml",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return sorted(
            path
            for pattern in ("*.md", "*.toml")
            for path in root.rglob(pattern)
            if ".git" not in path.parts
        )
    paths = (root / item.decode("utf-8") for item in completed.stdout.split(b"\0") if item)
    return sorted(path for path in paths if path.is_file())


def toml_metadata(path: Path) -> tuple[dict[str, object], str | None]:
    text = path.read_text(encoding="utf-8-sig")
    marker = re.compile(r"(?m)^(?:temporary|temporary-reason|temporary-delete-when|temporary-delete-after)\s*=")
    if not marker.search(text):
        return {}, None
    try:
        parsed = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return {}, f"invalid temporary TOML: {exc}"
    return {key: parsed[key] for key in TEMP_KEYS if key in parsed}, None


def metadata(path: Path) -> tuple[dict[str, object], str | None]:
    if path.suffix.casefold() == ".md":
        return markdown_metadata(path), None
    if path.suffix.casefold() == ".toml":
        return toml_metadata(path)
    return {}, None


def validate(root: Path) -> tuple[list[Temporary], list[str]]:
    active: list[Temporary] = []
    errors: list[str] = []
    today = date.today()

    for path in candidate_files(root):
        data, parse_error = metadata(path)
        rel = path.relative_to(root)
        if parse_error:
            errors.append(f"{rel}: {parse_error}")
            continue
        present = TEMP_KEYS.intersection(data)
        if not present:
            continue
        flag = data.get("temporary")

        if flag is False:
            errors.append(f"{rel}: temporary: false is not allowed; remove temporary-* properties from permanent files")
            continue
        if flag is not True:
            errors.append(f"{rel}: temporary-* properties require temporary: true")
            continue

        reason = data.get("temporary-reason")
        delete_when = data.get("temporary-delete-when")
        reason_text = reason.strip() if isinstance(reason, str) else ""
        when_text = delete_when.strip() if isinstance(delete_when, str) else ""
        if not reason_text:
            errors.append(f"{rel}: a non-empty temporary-reason is required")
        if not when_text:
            errors.append(f"{rel}: a non-empty temporary-delete-when is required")

        deadline: date | None = None
        raw_deadline = data.get("temporary-delete-after")
        if raw_deadline is not None:
            if isinstance(raw_deadline, date):
                deadline = raw_deadline
            elif not isinstance(raw_deadline, str) or not ISO_DATE.fullmatch(raw_deadline):
                errors.append(f"{rel}: temporary-delete-after must use YYYY-MM-DD")
            else:
                try:
                    deadline = date.fromisoformat(raw_deadline)
                except ValueError:
                    errors.append(f"{rel}: temporary-delete-after is not a valid date")
            if deadline is not None and today > deadline:
                errors.append(f"{rel}: temporary-delete-after expired on {deadline.isoformat()}")

        active.append(Temporary(rel, reason_text, when_text, deadline))

    return active, errors


def print_inventory(active: list[Temporary], ui) -> None:
    ui.heading("Active temporary files")
    if not active:
        ui.info("None.")
        return
    for item in sorted(active, key=lambda value: str(value.path)):
        deadline = item.delete_after.isoformat() if item.delete_after else ("-" if ui.ascii else "—")
        ui.section(str(item.path))
        ui.key_value("Reason", item.reason or "[MISSING]")
        ui.key_value("Delete when", item.delete_when or "[MISSING]")
        ui.key_value("Deadline", deadline)
    ui.warning("Semantic review is required: check whether any delete condition is already satisfied.")


def main(argv: list[str] | None = None) -> int:
    invocation = "python gobierno/validate_temporaries.py"
    catalogue = HelpCatalogue(
        product="MUD TEMPORARIES",
        version="",
        description="Validate intentionally versioned temporary Markdown and TOML files.",
        invocation=invocation,
        groups=(),
        commands=(),
        usage=(f"{invocation} [--root PATH] [--colour MODE] [--ascii]",),
        notes=("Running without arguments validates the current Mud repository.",),
        show_help_on_empty=False,
    )
    parser = MudArgumentParser(prog=invocation, error_code="Mud.Temporaries.InvalidArguments")
    parser.add_argument("--root", type=Path, default=ROOT)
    add_presentation_arguments(parser)
    parsed = parse_cli(parser, catalogue, argv)
    if parsed.exit_code is not None:
        return parsed.exit_code
    args = parsed.arguments
    assert args is not None
    root = args.root.resolve()
    active, errors = validate(root)
    print_inventory(active, parsed.ui)
    if errors:
        for error in errors:
            failure(parsed.ui, "Temporary-file validation failed.", code="Mud.Temporaries.InvalidMetadata", details=error)
        return 1
    parsed.ui.success(f"Validated {len(active)} active temporary file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
