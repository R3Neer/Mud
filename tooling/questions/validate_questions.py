from __future__ import annotations

import re
import sys
import tomllib
from collections import Counter
from datetime import date
from fnmatch import fnmatchcase
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUESTION_DIR = ROOT / "notas" / "preguntas"
INDEX = QUESTION_DIR / "README.md"
LEGACY = ROOT / "notas" / "08-preguntas-abiertas.md"
EXPORT_PROFILES = ROOT / "tooling" / "markdown_export" / "profiles.toml"
EXPORT_DIR = ROOT / "exports"

QUESTION_FILE = re.compile(r"^(Q-\d{3})-.+\.md$")
ID_FIELD = re.compile(r"^id: (Q-\d{3})$", re.MULTILINE)
STATUS_FIELD = re.compile(r"^status: ([a-z-]+)$", re.MULTILINE)
PRIORITY_FIELD = re.compile(r"^priority: (P[012])$", re.MULTILINE)
OPENED_FIELD = re.compile(r"^opened:(?: (true|false))?$", re.MULTILINE)
CLOSED_FIELD = re.compile(r"^closed:(?: (\d{4}-\d{2}-\d{2}))?$", re.MULTILINE)
INDEX_LINK = re.compile(r"\[\[[^|\]]+\|(Q-\d{3}) —")
SPEC_QUESTION = re.compile(r"^  - (Q-\d{3})$", re.MULTILINE)
QUESTION_LINK = re.compile(r"\[\[(notas/preguntas/Q-[^|\]#]+)")

ACTIVE_STATUSES = {"abierta", "parcialmente-decidida"}
ALLOWED_STATUSES = ACTIVE_STATUSES | {"cerrada", "descartada", "sustituida"}
EXPECTED_OPENED = {
    "abierta": "true",
    "parcialmente-decidida": None,
    "cerrada": "false",
    "descartada": "false",
    "sustituida": "false",
}
REQUIRED_FIELDS = (
    "id:",
    "title:",
    "status:",
    "priority:",
    "opened:",
    "closed:",
    "decisions:",
    "affects:",
    "superseded-by:",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    questions: dict[str, tuple[Path, str]] = {}

    for path in sorted(QUESTION_DIR.glob("Q-*.md")):
        filename = QUESTION_FILE.fullmatch(path.name)
        text = read(path)
        identifier = ID_FIELD.search(text)
        status = STATUS_FIELD.search(text)
        priority = PRIORITY_FIELD.search(text)
        opened = OPENED_FIELD.search(text)
        closed = CLOSED_FIELD.search(text)

        if filename is None:
            errors.append(f"Nombre de archivo inválido: {path.relative_to(ROOT)}")
            continue
        if identifier is None or identifier.group(1) != filename.group(1):
            errors.append(f"ID ausente o distinto del nombre: {path.relative_to(ROOT)}")
            continue
        question_id = identifier.group(1)
        if question_id in questions:
            errors.append(f"ID duplicado: {question_id}")
        if status is None or status.group(1) not in ALLOWED_STATUSES:
            errors.append(f"Estado inválido en {path.relative_to(ROOT)}")
            continue
        if priority is None:
            errors.append(f"Prioridad ausente en {path.relative_to(ROOT)}")
        for field in REQUIRED_FIELDS:
            if not re.search(rf"^{re.escape(field)}", text, re.MULTILINE):
                errors.append(f"Falta {field} en {path.relative_to(ROOT)}")
        question_status = status.group(1)
        if opened is None:
            errors.append(f"Valor inválido de opened en {path.relative_to(ROOT)}")
        elif opened.group(1) != EXPECTED_OPENED[question_status]:
            errors.append(
                f"opened no corresponde a status en {path.relative_to(ROOT)}: "
                f"{opened.group(1) or 'vacío'} frente a {question_status}"
            )
        if closed is None:
            errors.append(f"Valor inválido de closed en {path.relative_to(ROOT)}")
        else:
            closed_value = closed.group(1)
            if question_status in ACTIVE_STATUSES and closed_value is not None:
                errors.append(
                    f"Pregunta activa con fecha de cierre en {path.relative_to(ROOT)}"
                )
            if question_status not in ACTIVE_STATUSES and closed_value is None:
                errors.append(
                    f"Pregunta inactiva sin fecha de cierre en {path.relative_to(ROOT)}"
                )
            if closed_value is not None:
                try:
                    date.fromisoformat(closed_value)
                except ValueError:
                    errors.append(
                        f"Fecha de cierre inválida en {path.relative_to(ROOT)}: {closed_value}"
                    )
        questions[question_id] = (path, question_status)

    index_text = read(INDEX)
    indexed = INDEX_LINK.findall(index_text)
    indexed_counts = Counter(indexed)
    active = {question_id for question_id, (_, status) in questions.items() if status in ACTIVE_STATUSES}

    duplicate_index = sorted(question_id for question_id, count in indexed_counts.items() if count > 1)
    missing_index = sorted(active - set(indexed))
    inactive_index = sorted(set(indexed) - active)
    if duplicate_index:
        errors.append(f"Preguntas duplicadas en el índice: {', '.join(duplicate_index)}")
    if missing_index:
        errors.append(f"Preguntas activas ausentes del índice: {', '.join(missing_index)}")
    if inactive_index:
        errors.append(f"Preguntas inactivas presentes en el índice: {', '.join(inactive_index)}")

    if LEGACY.exists():
        errors.append("El registro sustituido notas/08-preguntas-abiertas.md todavía existe.")

    with EXPORT_PROFILES.open("rb") as stream:
        profiles = tomllib.load(stream)["profiles"]

    all_question_ids = set(questions)
    question_paths = {
        question_id: path.relative_to(ROOT).as_posix()
        for question_id, (path, _) in questions.items()
    }

    def questions_selected_by(profile_name: str) -> set[str]:
        profile = profiles[profile_name]
        includes = profile.get("include", [])
        excludes = profile.get("exclude", [])

        def included(relative: str, pattern: str) -> bool:
            normalized = pattern.replace("\\", "/").strip("/")
            return (
                normalized in {"", "."}
                or relative == normalized
                or relative.startswith(f"{normalized}/")
                or fnmatchcase(relative, pattern)
            )

        return {
            question_id
            for question_id, relative in question_paths.items()
            if any(included(relative, pattern) for pattern in includes)
            and not any(fnmatchcase(relative, pattern) for pattern in excludes)
        }

    expected_by_profile = {
        "specification": set(),
        "decisions": all_question_ids,
        "language": active,
        "current": active,
    }
    for profile_name, expected in expected_by_profile.items():
        selected = questions_selected_by(profile_name)
        missing = sorted(expected - selected)
        unexpected = sorted(selected - expected)
        if missing:
            errors.append(
                f"El perfil {profile_name} omite preguntas requeridas: {', '.join(missing)}"
            )
        if unexpected:
            errors.append(
                f"El perfil {profile_name} incluye preguntas impropias: {', '.join(unexpected)}"
            )

    for path in (ROOT / "especificacion").glob("*.md"):
        for question_id in SPEC_QUESTION.findall(read(path)):
            status = questions.get(question_id, (None, None))[1]
            if status not in ACTIVE_STATUSES:
                errors.append(
                    f"{path.relative_to(ROOT)} referencia en frontmatter una pregunta inexistente o inactiva: {question_id}"
                )

    for path in ROOT.rglob("*.md"):
        if path.is_relative_to(EXPORT_DIR):
            continue
        text = read(path)
        if "08-preguntas-abiertas" in text:
            errors.append(f"Enlace al registro sustituido: {path.relative_to(ROOT)}")
        for target in QUESTION_LINK.findall(text):
            target_path = ROOT / f"{target}.md"
            if not target_path.is_file():
                errors.append(
                    f"Enlace a pregunta inexistente en {path.relative_to(ROOT)}: {target}"
                )

    counts = Counter(status for _, status in questions.values())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Preguntas MUD: "
        f"{len(questions)} archivos únicos; "
        f"{counts['abierta']} abiertas, "
        f"{counts['parcialmente-decidida']} parcialmente decididas y "
        f"{counts['cerrada']} cerradas; "
        f"{len(indexed)} entradas activas verificadas."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
