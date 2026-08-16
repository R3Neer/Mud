from __future__ import annotations

import re
import sys
import tomllib
from argparse import ArgumentParser
from collections import Counter
from dataclasses import dataclass
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
PRIORITY_FIELD = re.compile(r"^priority: (P[012])$", re.MULTILINE)
HEADING = re.compile(r"^# Q-\d{3} — (.+)$", re.MULTILINE)
OPENED_FIELD = re.compile(r"^opened: (\d{4}-\d{2}-\d{2})$", re.MULTILINE)
RESOLVED_FIELD = re.compile(r"^resolved:(?: (true|false))?$", re.MULTILINE)
CLOSED_FIELD = re.compile(r"^closed:(?: (\d{4}-\d{2}-\d{2}))?$", re.MULTILINE)
INDEX_LINK = re.compile(r"\[\[[^|\]]+\|(Q-\d{3}) —")
SPEC_QUESTION = re.compile(r"^  - (Q-\d{3})$", re.MULTILINE)
QUESTION_LINK = re.compile(r"\[\[(notas/preguntas/Q-[^|\]#]+)")
CRITERION_ENTRY = re.compile(r"^- (C\d+):\s+\S.*$", re.MULTILINE)
EVIDENCE_ENTRY = re.compile(r"^- (C\d+):\s+\S.*$", re.MULTILINE)

ACTIVE_STATES = {"abierta", "parcialmente-decidida"}
RESOLVED_STATES = {
    "false": "abierta",
    None: "parcialmente-decidida",
    "true": "cerrada",
}
REQUIRED_FIELDS = (
    "id:",
    "title:",
    "priority:",
    "opened:",
    "resolved:",
    "closed:",
    "decisions:",
    "affects:",
    "superseded-by:",
)

PRIORITY_HEADINGS = {
    "P0": "Antes de congelar el núcleo",
    "P1": "Antes de ampliar el lenguaje",
    "P2": "Producto y operación",
}
STATUS_LABELS = {
    "abierta": "Abierta",
    "parcialmente-decidida": "Parcialmente decidida",
}


@dataclass(frozen=True)
class Question:
    path: Path
    state: str
    priority: str
    title: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_index(questions: dict[str, Question]) -> str:
    active = {
        question_id: question
        for question_id, question in questions.items()
        if question.state in ACTIVE_STATES
    }
    counts = Counter(question.state for question in active.values())
    lines = [
        "---",
        "title: Preguntas activas de MUD",
        "tags:",
        "  - mud/notas",
        "  - mud/preguntas",
        "status: activo",
        "---",
        "",
        "# Preguntas activas de MUD",
        "",
        "Este índice contiene únicamente preguntas en estado `abierta` o `parcialmente-decidida`. Su gestión se rige por [[gobierno/POLITICA-DE-PREGUNTAS|Política de preguntas de MUD]].",
        "",
        f"Hay {len(active)} preguntas activas: {counts['abierta']} abiertas y {counts['parcialmente-decidida']} parcialmente decididas.",
        "",
        "Prioridades:",
        "",
        "- **P0**: bloquea el núcleo v0 o puede forzar una reescritura cercana.",
        "- **P1**: bloquea una fase posterior concreta.",
        "- **P2**: puede aplazarse sin falsear el núcleo.",
        "",
    ]
    for priority, heading in PRIORITY_HEADINGS.items():
        lines.extend([
            f"## {priority} — {heading}",
            "",
            "| Pregunta | Estado |",
            "| --- | --- |",
        ])
        for question_id in sorted(active):
            question = active[question_id]
            if question.priority != priority:
                continue
            stem = question.path.stem
            lines.append(
                f"| [[{stem}|{question_id} — {question.title}]] | "
                f"{STATUS_LABELS[question.state]} |"
            )
        lines.append("")
    lines.extend([
        "## Historial",
        "",
        "Las preguntas cerradas, descartadas o sustituidas no aparecen en este índice. Sus archivos permanecen en esta carpeta con una ubicación estable para conservar la trazabilidad.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = ArgumentParser(description="Genera o valida el registro de preguntas de MUD.")
    parser.add_argument(
        "command",
        nargs="?",
        choices=("validate", "generate"),
        default="validate",
    )
    args = parser.parse_args()
    errors: list[str] = []
    questions: dict[str, Question] = {}

    for path in sorted(QUESTION_DIR.glob("Q-*.md")):
        filename = QUESTION_FILE.fullmatch(path.name)
        text = read(path)
        identifier = ID_FIELD.search(text)
        priority = PRIORITY_FIELD.search(text)
        heading = HEADING.search(text)
        opened = OPENED_FIELD.search(text)
        resolved = RESOLVED_FIELD.search(text)
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
        if priority is None:
            errors.append(f"Prioridad ausente en {path.relative_to(ROOT)}")
        if heading is None:
            errors.append(f"Título H1 ausente o inválido en {path.relative_to(ROOT)}")
        for field in REQUIRED_FIELDS:
            if not re.search(rf"^{re.escape(field)}", text, re.MULTILINE):
                errors.append(f"Falta {field} en {path.relative_to(ROOT)}")
        if opened is None:
            errors.append(f"Fecha de apertura inválida en {path.relative_to(ROOT)}")
        else:
            try:
                date.fromisoformat(opened.group(1))
            except ValueError:
                errors.append(
                    f"Fecha de apertura inválida en {path.relative_to(ROOT)}: "
                    f"{opened.group(1)}"
                )
        if resolved is None:
            errors.append(f"Valor inválido de resolved en {path.relative_to(ROOT)}")
            continue
        question_state = RESOLVED_STATES[resolved.group(1)]
        if closed is None:
            errors.append(f"Valor inválido de closed en {path.relative_to(ROOT)}")
        else:
            closed_value = closed.group(1)
            if question_state in ACTIVE_STATES and closed_value is not None:
                errors.append(
                    f"Pregunta activa con fecha de cierre en {path.relative_to(ROOT)}"
                )
            if question_state not in ACTIVE_STATES and closed_value is None:
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
        if question_state == "cerrada":
            criterion_match = re.search(
                r"^## Criterio de cierre\s*$([\s\S]*?)(?=^## |\Z)",
                text,
                re.MULTILINE,
            )
            evidence_match = re.search(
                r"^## Evidencia de cierre\s*$([\s\S]*?)(?=^## |\Z)",
                text,
                re.MULTILINE,
            )
            if criterion_match is None:
                errors.append(f"Pregunta cerrada sin criterios identificados: {path.relative_to(ROOT)}")
            if evidence_match is None:
                errors.append(f"Pregunta cerrada sin evidencia de cierre: {path.relative_to(ROOT)}")
            if criterion_match is not None and evidence_match is not None:
                criteria = CRITERION_ENTRY.findall(criterion_match.group(1))
                evidence = EVIDENCE_ENTRY.findall(evidence_match.group(1))
                criterion_counts = Counter(criteria)
                evidence_counts = Counter(evidence)
                if not criteria:
                    errors.append(f"Pregunta cerrada sin entradas Cn: {path.relative_to(ROOT)}")
                duplicated_criteria = sorted(k for k, v in criterion_counts.items() if v != 1)
                duplicated_evidence = sorted(k for k, v in evidence_counts.items() if v != 1)
                if duplicated_criteria:
                    errors.append(
                        f"Criterios duplicados en {path.relative_to(ROOT)}: {', '.join(duplicated_criteria)}"
                    )
                if duplicated_evidence:
                    errors.append(
                        f"Evidencia duplicada en {path.relative_to(ROOT)}: {', '.join(duplicated_evidence)}"
                    )
                missing_evidence = sorted(set(criteria) - set(evidence))
                unknown_evidence = sorted(set(evidence) - set(criteria))
                if missing_evidence:
                    errors.append(
                        f"Criterios sin evidencia en {path.relative_to(ROOT)}: {', '.join(missing_evidence)}"
                    )
                if unknown_evidence:
                    errors.append(
                        f"Evidencia para criterios inexistentes en {path.relative_to(ROOT)}: {', '.join(unknown_evidence)}"
                    )

        if priority is not None and heading is not None:
            questions[question_id] = Question(
                path=path,
                state=question_state,
                priority=priority.group(1),
                title=heading.group(1),
            )

    expected_index = render_index(questions)
    if args.command == "generate":
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        INDEX.write_text(expected_index, encoding="utf-8", newline="\n")

    index_text = read(INDEX)
    if index_text != expected_index:
        errors.append(
            "El índice de preguntas no coincide con los metadatos; ejecuta "
            "python tooling/questions/validate_questions.py generate"
        )
    indexed = INDEX_LINK.findall(index_text)
    indexed_counts = Counter(indexed)
    active = {question_id for question_id, question in questions.items() if question.state in ACTIVE_STATES}

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
        question_id: question.path.relative_to(ROOT).as_posix()
        for question_id, question in questions.items()
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
            question = questions.get(question_id)
            state = question.state if question is not None else None
            if state not in ACTIVE_STATES:
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

    counts = Counter(question.state for question in questions.values())
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
