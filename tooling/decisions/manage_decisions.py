from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DECISION_DIR = ROOT / "notas" / "decisiones"
QUESTION_DIR = ROOT / "notas" / "preguntas"
INDEX = DECISION_DIR / "README.md"
RESERVED = DECISION_DIR / "identificadores-reservados.txt"
LEGACY = ROOT / "notas" / "10-registro-de-decisiones.md"

ADR_FILE = re.compile(r"^ADR-(\d{3})-(.+)\.md$")
DECISION_ID = re.compile(r"^D-\d{3}$")
QUESTION_ID = re.compile(r"^Q-\d{3}$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
H1 = re.compile(r"^# ADR-\d{3} — (.+)$", re.MULTILINE)
LEGACY_STATUS = re.compile(r"^- Estado: (.+)$", re.MULTILINE)
LEGACY_DATE = re.compile(r"^- Fecha: (\d{4}-\d{2}-\d{2})$", re.MULTILINE)
LEGACY_AFFECTS = re.compile(r"^- Documentos afectados: (.+)$", re.MULTILINE)
DECISION_LINK = re.compile(
    r"(?:notas/)?decisiones/(ADR-\d{3}-[^|\]#)]+)"
)
QUESTION_LINK = re.compile(r"(?:notas/)?preguntas/(Q-\d{3}-[^|\]#)]+)")
DECISION_TOKEN = re.compile(r"\bD-\d{3}\b")
QUESTION_TOKEN = re.compile(r"\bQ-\d{3}\b")

ALLOWED_STATUSES = {"propuesta", "vigente", "sustituida", "retirada", "rechazada"}
REQUIRED_FIELDS = (
    "id",
    "title",
    "status",
    "date",
    "supersedes",
    "superseded-by",
    "questions",
    "affects",
)


@dataclass(frozen=True)
class Decision:
    path: Path
    identifier: str
    title: str
    status: str
    adopted: str
    supersedes: tuple[str, ...]
    superseded_by: tuple[str, ...]
    questions: tuple[str, ...]
    affects: tuple[str, ...]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def scalar(value: str) -> str:
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return str(json.loads(value))
    return value


def parse_frontmatter(path: Path, text: str) -> tuple[dict[str, object], int]:
    if not text.startswith("---\n"):
        raise ValueError("falta frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter sin cierre")
    lines = text[4:end].splitlines()
    result: dict[str, object] = {}
    current_list: str | None = None
    for line in lines:
        if line.startswith("  - ") and current_list is not None:
            values = result[current_list]
            assert isinstance(values, list)
            values.append(scalar(line[4:]))
            continue
        current_list = None
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"línea YAML no admitida: {line}")
        key, raw = line.split(":", 1)
        raw = raw.strip()
        if raw == "[]":
            result[key] = []
        elif raw == "":
            result[key] = []
            current_list = key
        else:
            result[key] = scalar(raw)
    return result, end + 5


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_list(name: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{name}: []"]
    return [f"{name}:"] + [f"  - {yaml_string(value)}" for value in values]


def render_frontmatter(
    identifier: str,
    title: str,
    status: str,
    adopted: str,
    supersedes: list[str],
    superseded_by: list[str],
    questions: list[str],
    affects: list[str],
) -> str:
    lines = [
        "---",
        f"id: {identifier}",
        f"title: {yaml_string(title)}",
        f"status: {status}",
        f"date: {adopted}",
        *yaml_list("supersedes", supersedes),
        *yaml_list("superseded-by", superseded_by),
        *yaml_list("questions", questions),
        *yaml_list("affects", affects),
        "---",
        "",
    ]
    return "\n".join(lines)


def normalize_status(raw: str) -> str:
    normalized = raw.strip().lower()
    for status in ALLOWED_STATUSES:
        if normalized.startswith(status):
            return status
    raise ValueError(f"estado histórico no reconocido: {raw}")


def unique_tokens(pattern: re.Pattern[str], text: str) -> list[str]:
    return list(dict.fromkeys(pattern.findall(text)))


def migrate_file(path: Path) -> bool:
    text = read(path)
    if text.startswith("---\n"):
        return False
    filename = ADR_FILE.fullmatch(path.name)
    title_match = H1.search(text)
    status_match = LEGACY_STATUS.search(text)
    date_match = LEGACY_DATE.search(text)
    if filename is None or title_match is None or status_match is None or date_match is None:
        raise ValueError(f"no se puede migrar automáticamente {path.relative_to(ROOT)}")
    header = text.split("\n## Contexto", 1)[0]
    affects_match = LEGACY_AFFECTS.search(header)
    affects = [affects_match.group(1).strip()] if affects_match else []
    questions = unique_tokens(QUESTION_TOKEN, header)
    metadata = render_frontmatter(
        identifier=f"D-{filename.group(1)}",
        title=title_match.group(1).strip(),
        status=normalize_status(status_match.group(1)),
        adopted=date_match.group(1),
        supersedes=[],
        superseded_by=[],
        questions=questions,
        affects=affects,
    )
    body = LEGACY_STATUS.sub("", text, count=1)
    body = LEGACY_DATE.sub("", body, count=1)
    body = re.sub(r"\n{3,}", "\n\n", body, count=1)
    path.write_text(metadata + body, encoding="utf-8", newline="\n")
    return True


def load_reserved() -> set[str]:
    reserved: set[str] = set()
    for line in read(RESERVED).splitlines():
        value = line.strip()
        if not value or value.startswith("#"):
            continue
        if not DECISION_ID.fullmatch(value):
            raise ValueError(f"identificador reservado inválido: {value}")
        reserved.add(value)
    return reserved


def load_decisions(errors: list[str]) -> dict[str, Decision]:
    decisions: dict[str, Decision] = {}
    for path in sorted(DECISION_DIR.glob("ADR-*.md")):
        filename = ADR_FILE.fullmatch(path.name)
        if filename is None:
            errors.append(f"Nombre de ADR inválido: {path.relative_to(ROOT)}")
            continue
        text = read(path)
        try:
            data, _ = parse_frontmatter(path, text)
        except ValueError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        missing = [field for field in REQUIRED_FIELDS if field not in data]
        if missing:
            errors.append(
                f"{path.relative_to(ROOT)} omite metadatos: {', '.join(missing)}"
            )
            continue
        identifier = data["id"]
        title = data["title"]
        status = data["status"]
        adopted = data["date"]
        list_fields = ("supersedes", "superseded-by", "questions", "affects")
        if not all(isinstance(data[field], list) for field in list_fields):
            errors.append(f"{path.relative_to(ROOT)} contiene una lista YAML inválida")
            continue
        if not all(isinstance(value, str) for value in (identifier, title, status, adopted)):
            errors.append(f"{path.relative_to(ROOT)} contiene escalares YAML inválidos")
            continue
        expected_id = f"D-{filename.group(1)}"
        if identifier != expected_id:
            errors.append(
                f"ID distinto del nombre en {path.relative_to(ROOT)}: {identifier}"
            )
        if identifier in decisions:
            errors.append(f"ID de decisión duplicado: {identifier}")
        if status not in ALLOWED_STATUSES:
            errors.append(f"Estado inválido en {path.relative_to(ROOT)}: {status}")
        if not ISO_DATE.fullmatch(adopted):
            errors.append(f"Fecha inválida en {path.relative_to(ROOT)}: {adopted}")
        else:
            try:
                date.fromisoformat(adopted)
            except ValueError:
                errors.append(f"Fecha imposible en {path.relative_to(ROOT)}: {adopted}")
        heading = H1.search(text)
        if heading is None or heading.group(1).strip() != title:
            errors.append(f"Título y H1 no coinciden en {path.relative_to(ROOT)}")
        decision = Decision(
            path=path,
            identifier=identifier,
            title=title,
            status=status,
            adopted=adopted,
            supersedes=tuple(data["supersedes"]),
            superseded_by=tuple(data["superseded-by"]),
            questions=tuple(data["questions"]),
            affects=tuple(data["affects"]),
        )
        decisions[identifier] = decision
    return decisions


def render_index(decisions: dict[str, Decision], reserved: set[str]) -> str:
    counts = Counter(decision.status for decision in decisions.values())
    lines = [
        "<!-- Archivo generado por tooling/decisions/manage_decisions.py. -->",
        "<!-- No editar manualmente. -->",
        "",
        "# Decisiones de MUD",
        "",
        "Cada decisión tiene un ADR estable. El ciclo de vida y los metadatos se rigen",
        "por [[gobierno/POLITICA-DE-DECISIONES|la política de decisiones]].",
        "",
        "## Resumen",
        "",
        f"- Total: {len(decisions)}.",
        f"- Vigentes: {counts['vigente']}.",
        f"- Propuestas: {counts['propuesta']}.",
        f"- Sustituidas: {counts['sustituida']}.",
        f"- Retiradas: {counts['retirada']}.",
        f"- Rechazadas: {counts['rechazada']}.",
        "",
        "## Índice",
        "",
        "| ID | Estado | Fecha | Decisión |",
        "| --- | --- | --- | --- |",
    ]
    for identifier in sorted(decisions):
        decision = decisions[identifier]
        stem = decision.path.stem
        lines.append(
            f"| {identifier} | {decision.status} | {decision.adopted} | "
            f"[[notas/decisiones/{stem}|{decision.title}]] |"
        )
    lines.extend(
        [
            "",
            "## Identificadores reservados",
            "",
            "No contienen una decisión recuperable y no pueden reutilizarse:",
            "",
            ", ".join(f"`{identifier}`" for identifier in sorted(reserved)) + ".",
            "",
            "## Regeneración",
            "",
            "```powershell",
            "python tooling/decisions/manage_decisions.py generate",
            "python tooling/decisions/manage_decisions.py validate",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def validate() -> int:
    errors: list[str] = []
    try:
        reserved = load_reserved()
    except ValueError as exc:
        errors.append(str(exc))
        reserved = set()
    decisions = load_decisions(errors)
    decision_ids = set(decisions)
    overlap = sorted(decision_ids & reserved)
    if overlap:
        errors.append(f"Identificadores reservados reutilizados: {', '.join(overlap)}")
    if decision_ids:
        maximum = max(int(identifier[2:]) for identifier in decision_ids | reserved)
        expected = {f"D-{number:03d}" for number in range(1, maximum + 1)}
        holes = sorted(expected - decision_ids - reserved)
        if holes:
            errors.append(f"Huecos de decisión no explicados: {', '.join(holes)}")

    question_paths = {
        f"Q-{match.group(1)}"
        for path in QUESTION_DIR.glob("Q-*.md")
        if (match := re.match(r"^Q-(\d{3})-", path.name))
    }
    adr_stems = {decision.path.stem for decision in decisions.values()}
    question_stems = {path.stem for path in QUESTION_DIR.glob("Q-*.md")}

    for decision in decisions.values():
        for related in (*decision.supersedes, *decision.superseded_by):
            if not DECISION_ID.fullmatch(related) or related not in decision_ids:
                errors.append(
                    f"{decision.identifier} enlaza una decisión inexistente: {related}"
                )
        for question in decision.questions:
            if not QUESTION_ID.fullmatch(question) or question not in question_paths:
                errors.append(
                    f"{decision.identifier} enlaza una pregunta inexistente: {question}"
                )
        if decision.status == "sustituida" and not decision.superseded_by:
            errors.append(f"{decision.identifier} está sustituida sin superseded-by")
        for older in decision.supersedes:
            if decision.identifier not in decisions[older].superseded_by:
                errors.append(
                    f"Sustitución no recíproca: {decision.identifier} -> {older}"
                )
        for newer in decision.superseded_by:
            if decision.identifier not in decisions[newer].supersedes:
                errors.append(
                    f"Sustitución no recíproca: {decision.identifier} <- {newer}"
                )
    for path in QUESTION_DIR.glob("Q-*.md"):
        text = read(path)
        metadata_match = re.search(
            r"^decisions:\s*(.*?)(?=^[a-z][a-z-]*:|\Z)",
            text,
            re.MULTILINE | re.DOTALL,
        )
        if metadata_match:
            for token in DECISION_TOKEN.findall(metadata_match.group(1)):
                if token not in decision_ids:
                    errors.append(
                        f"{path.relative_to(ROOT)} enlaza una decisión inexistente: {token}"
                    )

    export_dir = ROOT / "exports"
    for path in ROOT.rglob("*.md"):
        if path.is_relative_to(export_dir):
            continue
        text = read(path)
        relative = path.relative_to(ROOT)
        if "10-registro-de-decisiones" in text:
            errors.append(f"Enlace al registro sustituido en {relative}")
        for target in DECISION_LINK.findall(text):
            if target not in adr_stems:
                errors.append(f"Enlace a ADR inexistente en {relative}: {target}")
        for target in QUESTION_LINK.findall(text):
            if target not in question_stems:
                errors.append(f"Enlace a pregunta inexistente en {relative}: {target}")
        for token in DECISION_TOKEN.findall(text):
            if token not in decision_ids and token not in reserved:
                errors.append(
                    f"Referencia a decisión inexistente en {relative}: {token}"
                )

    expected_index = render_index(decisions, reserved)
    if not INDEX.is_file() or read(INDEX) != expected_index:
        errors.append("notas/decisiones/README.md no coincide con el índice generado")
    if LEGACY.exists():
        errors.append("El registro sustituido notas/10-registro-de-decisiones.md todavía existe")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    counts = Counter(decision.status for decision in decisions.values())
    print(
        "Decisiones MUD: "
        f"{len(decisions)} ADR únicos; "
        f"{counts['vigente']} vigentes, "
        f"{counts['propuesta']} propuestas y "
        f"{len(reserved)} identificadores reservados; "
        "índice y relaciones verificados."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Gestiona los ADR de MUD.")
    parser.add_argument("command", choices=("migrate", "generate", "validate"))
    args = parser.parse_args()
    if args.command == "migrate":
        migrated = 0
        for path in sorted(DECISION_DIR.glob("ADR-*.md")):
            migrated += int(migrate_file(path))
        print(f"ADR migrados: {migrated}.")
        return 0
    if args.command == "generate":
        errors: list[str] = []
        decisions = load_decisions(errors)
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        content = render_index(decisions, load_reserved())
        INDEX.write_text(content, encoding="utf-8", newline="\n")
        print(f"Índice generado con {len(decisions)} decisiones.")
        return 0
    return validate()


if __name__ == "__main__":
    raise SystemExit(main())
