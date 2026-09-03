from __future__ import annotations

import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tooling.cli_support import (  # noqa: E402
    CommandHelp,
    HelpCatalogue,
    HelpItem,
    MudArgumentParser,
    add_presentation_arguments,
    failure,
    parse_cli,
)

DECISION_DIR = ROOT / "notes" / "decisions"
QUESTION_DIR = ROOT / "notes" / "questions"
INDEX = DECISION_DIR / "README.md"
RESERVED = DECISION_DIR / "reserved-identifiers.txt"
LEGACY = ROOT / "notes" / "10-registro-de-decisiones.md"

ADR_FILE = re.compile(r"^ADR-(\d{3})-(.+)\.md$")
DECISION_ID = re.compile(r"^D-\d{3}$")
QUESTION_ID = re.compile(r"^Q-\d{3}$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
H1 = re.compile(r"^# ADR-\d{3} — (.+)$", re.MULTILINE)
LEGACY_STATUS = re.compile(r"^- Estado: (.+)$", re.MULTILINE)
LEGACY_DATE = re.compile(r"^- Fecha: (\d{4}-\d{2}-\d{2})$", re.MULTILINE)
LEGACY_AFFECTS = re.compile(r"^- Documentos afectados: (.+)$", re.MULTILINE)
DECISION_LINK = re.compile(
    r"(?:notes/)?decisions/(ADR-\d{3}-[^|\]#)]+)"
)
QUESTION_LINK = re.compile(r"(?:notes/)?questions/(Q-\d{3}-[^|\]#)]+)")
DECISION_TOKEN = re.compile(r"\bD-\d{3}\b")
QUESTION_TOKEN = re.compile(r"\bQ-\d{3}\b")

ALLOWED_STATUSES = {"proposed", "current", "superseded", "withdrawn", "rejected"}
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
        raise ValueError("frontmatter is missing")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter is not closed")
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
            raise ValueError(f"unsupported YAML line: {line}")
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
    raise ValueError(f"unknown historical status: {raw}")


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
        raise ValueError(f"cannot migrate {path.relative_to(ROOT)} automatically")
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
            raise ValueError(f"invalid reserved identifier: {value}")
        reserved.add(value)
    return reserved


def load_decisions(errors: list[str]) -> dict[str, Decision]:
    decisions: dict[str, Decision] = {}
    for path in sorted(DECISION_DIR.glob("ADR-*.md")):
        filename = ADR_FILE.fullmatch(path.name)
        if filename is None:
            errors.append(f"Invalid ADR filename: {path.relative_to(ROOT)}")
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
                f"{path.relative_to(ROOT)} omits metadata: {', '.join(missing)}"
            )
            continue
        identifier = data["id"]
        title = data["title"]
        status = data["status"]
        adopted = data["date"]
        list_fields = ("supersedes", "superseded-by", "questions", "affects")
        if not all(isinstance(data[field], list) for field in list_fields):
            errors.append(f"{path.relative_to(ROOT)} contains an invalid YAML list")
            continue
        if not all(isinstance(value, str) for value in (identifier, title, status, adopted)):
            errors.append(f"{path.relative_to(ROOT)} contains invalid YAML scalars")
            continue
        expected_id = f"D-{filename.group(1)}"
        if identifier != expected_id:
            errors.append(
                f"ID does not match the filename in {path.relative_to(ROOT)}: {identifier}"
            )
        if identifier in decisions:
            errors.append(f"Duplicate decision ID: {identifier}")
        if status not in ALLOWED_STATUSES:
            errors.append(f"Invalid status in {path.relative_to(ROOT)}: {status}")
        if not ISO_DATE.fullmatch(adopted):
            errors.append(f"Invalid date in {path.relative_to(ROOT)}: {adopted}")
        else:
            try:
                date.fromisoformat(adopted)
            except ValueError:
                errors.append(f"Impossible date in {path.relative_to(ROOT)}: {adopted}")
        heading = H1.search(text)
        if heading is None or heading.group(1).strip() != title:
            errors.append(f"Title and H1 do not match in {path.relative_to(ROOT)}")
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
        "por [[governance/DECISIONS-POLICY|la política de decisiones]].",
        "",
        "## Resumen",
        "",
        f"- Total: {len(decisions)}.",
        f"- Current: {counts['current']}.",
        f"- Proposed: {counts['proposed']}.",
        f"- Superseded: {counts['superseded']}.",
        f"- Withdrawn: {counts['withdrawn']}.",
        f"- Rejected: {counts['rejected']}.",
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
            f"[[notes/decisions/{stem}|{decision.title}]] |"
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


def validate(ui=None) -> int:
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
        errors.append(f"Reused reserved identifiers: {', '.join(overlap)}")
    if decision_ids:
        maximum = max(int(identifier[2:]) for identifier in decision_ids | reserved)
        expected = {f"D-{number:03d}" for number in range(1, maximum + 1)}
        holes = sorted(expected - decision_ids - reserved)
        if holes:
            errors.append(f"Unexplained gaps in decision identifiers: {', '.join(holes)}")

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
                    f"{decision.identifier} links to an unknown decision: {related}"
                )
        for question in decision.questions:
            if not QUESTION_ID.fullmatch(question) or question not in question_paths:
                errors.append(
                    f"{decision.identifier} links to an unknown question: {question}"
                )
        if decision.status == "superseded" and not decision.superseded_by:
            errors.append(f"{decision.identifier} is superseded without superseded-by")
        for older in decision.supersedes:
            if decision.identifier not in decisions[older].superseded_by:
                errors.append(
                    f"Non-reciprocal supersession: {decision.identifier} -> {older}"
                )
        for newer in decision.superseded_by:
            if decision.identifier not in decisions[newer].supersedes:
                errors.append(
                    f"Non-reciprocal supersession: {decision.identifier} <- {newer}"
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
                        f"{path.relative_to(ROOT)} links to an unknown decision: {token}"
                    )

    export_dir = ROOT / "exports"
    for path in ROOT.rglob("*.md"):
        if path.is_relative_to(export_dir):
            continue
        text = read(path)
        relative = path.relative_to(ROOT)
        if "10-registro-de-decisiones" in text:
            errors.append(f"Link to the superseded registry in {relative}")
        for target in DECISION_LINK.findall(text):
            if target not in adr_stems:
                errors.append(f"Link to an unknown ADR in {relative}: {target}")
        for target in QUESTION_LINK.findall(text):
            if target not in question_stems:
                errors.append(f"Link to an unknown question in {relative}: {target}")
        for token in DECISION_TOKEN.findall(text):
            if token not in decision_ids and token not in reserved:
                errors.append(
                    f"Reference to an unknown decision in {relative}: {token}"
                )

    expected_index = render_index(decisions, reserved)
    if not INDEX.is_file() or read(INDEX) != expected_index:
        errors.append("notes/decisions/README.md does not match the generated index")
    if LEGACY.exists():
        errors.append("The superseded notes/10-registro-de-decisiones.md registry still exists")

    if errors:
        for error in errors:
            if ui is None:
                print(f"ERROR: {error}", file=sys.stderr)
            else:
                failure(ui, "Decision validation failed.", code="Mud.Decisions.InvalidRegistry", details=error)
        return 1
    counts = Counter(decision.status for decision in decisions.values())
    message = (
        "Mud decisions: "
        f"{len(decisions)} unique ADRs; "
        f"{counts['current']} current, "
        f"{counts['proposed']} proposed and "
        f"{len(reserved)} reserved identifiers; index and relationships verified."
    )
    if ui is None:
        print(message)
    else:
        ui.success(message)
    return 0


def main(argv: list[str] | None = None) -> int:
    invocation = "python tooling/decisions/manage_decisions.py"
    commands = ("migrate", "generate", "validate")
    catalogue = HelpCatalogue(
        product="MUD DECISIONS",
        version="",
        description="Manage Mud architecture decision records and their generated index.",
        invocation=invocation,
        groups=("DECISIONS",),
        commands=(
            CommandHelp("migrate", "DECISIONS", "Migrate legacy ADR metadata", "Migrate legacy ADR metadata to the current frontmatter contract.", (f"{invocation} migrate",), notes=("This command may rewrite ADR files.",)),
            CommandHelp("generate", "DECISIONS", "Generate the decision index", "Regenerate the decision index from ADR metadata.", (f"{invocation} generate",), notes=("The index is written only after the source records validate.",)),
            CommandHelp("validate", "DECISIONS", "Validate decisions and relationships", "Validate identifiers, metadata, links, relationships and the generated index.", (f"{invocation} validate",)),
        ),
        usage=(f"{invocation} <command> [--colour MODE] [--ascii]", f"{invocation} <command> --help"),
        global_items=(
            HelpItem("--colour auto|always|never", "Control colour for human output. Default: auto; NO_COLOR disables it."),
            HelpItem("--ascii", "Use ASCII status symbols when Unicode is unsuitable."),
        ),
        notes=(f"Run {invocation} <command> --help for detailed help.",),
        show_help_on_empty=True,
    )
    parser = MudArgumentParser(prog=invocation, error_code="Mud.Decisions.InvalidArguments")
    parser.add_argument("command", choices=("migrate", "generate", "validate"))
    add_presentation_arguments(parser)
    parsed = parse_cli(parser, catalogue, argv, executable_commands=commands)
    if parsed.exit_code is not None:
        return parsed.exit_code
    args = parsed.arguments
    assert args is not None
    if args.command == "migrate":
        migrated = 0
        for path in sorted(DECISION_DIR.glob("ADR-*.md")):
            migrated += int(migrate_file(path))
        parsed.ui.success(f"Migrated {migrated} ADR file(s).")
        return 0
    if args.command == "generate":
        errors: list[str] = []
        decisions = load_decisions(errors)
        if errors:
            for error in errors:
                failure(parsed.ui, "The decision index could not be generated.", code="Mud.Decisions.InvalidRegistry", details=error)
            return 1
        content = render_index(decisions, load_reserved())
        INDEX.write_text(content, encoding="utf-8", newline="\n")
        parsed.ui.success(f"Generated the index with {len(decisions)} decisions.")
        return 0
    return validate(parsed.ui)


if __name__ == "__main__":
    raise SystemExit(main())
