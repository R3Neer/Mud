from __future__ import annotations

import re
import sys
import tomllib
from collections import Counter
from dataclasses import dataclass
from datetime import date
from fnmatch import fnmatchcase
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

QUESTION_DIR = ROOT / "notes" / "questions"
INDEX = QUESTION_DIR / "README.md"
LEGACY = ROOT / "notes" / "08-open-questions.md"
EXPORT_PROFILES = ROOT / "markdown-export.toml"
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
QUESTION_LINK = re.compile(r"\[\[(notes/questions/Q-[^|\]#]+)")
CRITERION_ENTRY = re.compile(r"^- (C\d+):\s+\S.*$", re.MULTILINE)
EVIDENCE_ENTRY = re.compile(r"^- (C\d+):\s+\S.*$", re.MULTILINE)

ACTIVE_STATES = {"open", "partially-decided"}
RESOLVED_STATES = {
    "false": "open",
    None: "partially-decided",
    "true": "closed",
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
    "open": "Open",
    "partially-decided": "Partially decided",
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
        "title: MUD active questions",
        "tags:",
        "  - mud/notes",
        "  - mud/preguntas",
        "status: active",
        "---",
        "",
        "# MUD active questions",
        "",
        "This index contains only questions in `open` or `partially-decided` state. They are governed by [[governance/QUESTIONS-POLICY|MUD question policy]].",
        "",
        f"There are {len(active)} active questions: {counts['open']} open and {counts['partially-decided']} partially decided.",
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
        "Closed, discarded or superseded questions do not appear in this index. Their files remain in this folder at stable locations for traceability.",
        "",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    invocation = "python tooling/questions/validate_questions.py"
    commands = ("validate", "generate")
    catalogue = HelpCatalogue(
        product="MUD QUESTIONS",
        version="",
        description="Generate or validate Mud's active-question index.",
        invocation=invocation,
        groups=("QUESTIONS",),
        commands=(
            CommandHelp("validate", "QUESTIONS", "Validate questions and the index", "Validate question metadata, lifecycle, links, export profiles and the active index.", (f"{invocation} validate", f"{invocation}",)),
            CommandHelp("generate", "QUESTIONS", "Generate the active-question index", "Regenerate the active-question index and then validate the complete question registry.", (f"{invocation} generate",), notes=("The index is written only when source metadata is valid.",)),
        ),
        usage=(f"{invocation} [validate|generate] [--colour MODE] [--ascii]", f"{invocation} <command> --help"),
        global_items=(
            HelpItem("--colour auto|always|never", "Control colour for human output. Default: auto; NO_COLOR disables it."),
            HelpItem("--ascii", "Use ASCII status symbols when Unicode is unsuitable."),
        ),
        notes=("Running without a command performs validation.",),
        show_help_on_empty=False,
    )
    parser = MudArgumentParser(prog=invocation, error_code="Mud.Questions.InvalidArguments")
    parser.add_argument(
        "command",
        nargs="?",
        choices=("validate", "generate"),
        default="validate",
    )
    add_presentation_arguments(parser)
    parsed = parse_cli(parser, catalogue, argv, executable_commands=commands)
    if parsed.exit_code is not None:
        return parsed.exit_code
    args = parsed.arguments
    assert args is not None
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
            errors.append(f"Invalid filename: {path.relative_to(ROOT)}")
            continue
        if identifier is None or identifier.group(1) != filename.group(1):
            errors.append(f"Missing ID or ID does not match filename: {path.relative_to(ROOT)}")
            continue
        question_id = identifier.group(1)
        if question_id in questions:
            errors.append(f"Duplicate ID: {question_id}")
        if priority is None:
            errors.append(f"Missing priority in {path.relative_to(ROOT)}")
        if heading is None:
            errors.append(f"Missing or invalid H1 title in {path.relative_to(ROOT)}")
        for field in REQUIRED_FIELDS:
            if not re.search(rf"^{re.escape(field)}", text, re.MULTILINE):
                errors.append(f"Missing {field} in {path.relative_to(ROOT)}")
        if opened is None:
            errors.append(f"Invalid opening date in {path.relative_to(ROOT)}")
        else:
            try:
                date.fromisoformat(opened.group(1))
            except ValueError:
                errors.append(
                    f"Invalid opening date in {path.relative_to(ROOT)}: "
                    f"{opened.group(1)}"
                )
        if resolved is None:
            errors.append(f"Invalid resolved value in {path.relative_to(ROOT)}")
            continue
        question_state = RESOLVED_STATES[resolved.group(1)]
        if closed is None:
            errors.append(f"Invalid closed value in {path.relative_to(ROOT)}")
        else:
            closed_value = closed.group(1)
            if question_state in ACTIVE_STATES and closed_value is not None:
                errors.append(
                    f"Active question has a closing date in {path.relative_to(ROOT)}"
                )
            if question_state not in ACTIVE_STATES and closed_value is None:
                errors.append(
                    f"Inactive question has no closing date in {path.relative_to(ROOT)}"
                )
            if closed_value is not None:
                try:
                    date.fromisoformat(closed_value)
                except ValueError:
                    errors.append(
                        f"Invalid closing date in {path.relative_to(ROOT)}: {closed_value}"
                    )
        if question_state == "closed":
            criterion_match = re.search(
                r"^## (?:Closure criterion|Criterio de cierre)\s*$([\s\S]*?)(?=^## |\Z)",
                text,
                re.MULTILINE,
            )
            evidence_match = re.search(
                r"^## (?:Closure evidence|Evidencia de cierre)\s*$([\s\S]*?)(?=^## |\Z)",
                text,
                re.MULTILINE,
            )
            if criterion_match is None:
                errors.append(f"Closed question has no identified criteria: {path.relative_to(ROOT)}")
            if evidence_match is None:
                errors.append(f"Closed question has no closure evidence: {path.relative_to(ROOT)}")
            if criterion_match is not None and evidence_match is not None:
                criteria = CRITERION_ENTRY.findall(criterion_match.group(1))
                evidence = EVIDENCE_ENTRY.findall(evidence_match.group(1))
                criterion_counts = Counter(criteria)
                evidence_counts = Counter(evidence)
                if not criteria:
                    errors.append(f"Closed question has no Cn entries: {path.relative_to(ROOT)}")
                duplicated_criteria = sorted(k for k, v in criterion_counts.items() if v != 1)
                duplicated_evidence = sorted(k for k, v in evidence_counts.items() if v != 1)
                if duplicated_criteria:
                    errors.append(
                        f"Duplicate criteria in {path.relative_to(ROOT)}: {', '.join(duplicated_criteria)}"
                    )
                if duplicated_evidence:
                    errors.append(
                        f"Duplicate evidence in {path.relative_to(ROOT)}: {', '.join(duplicated_evidence)}"
                    )
                missing_evidence = sorted(set(criteria) - set(evidence))
                unknown_evidence = sorted(set(evidence) - set(criteria))
                if missing_evidence:
                    errors.append(
                        f"Criteria without evidence in {path.relative_to(ROOT)}: {', '.join(missing_evidence)}"
                    )
                if unknown_evidence:
                    errors.append(
                        f"Evidence for unknown criteria in {path.relative_to(ROOT)}: {', '.join(unknown_evidence)}"
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
                failure(parsed.ui, "The question index could not be generated.", code="Mud.Questions.InvalidRegistry", details=error)
            return 1
        INDEX.write_text(expected_index, encoding="utf-8", newline="\n")

    index_text = read(INDEX)
    if index_text != expected_index:
        errors.append(
            "The question index does not match its metadata; run "
            "python tooling/questions/validate_questions.py generate"
        )
    indexed = INDEX_LINK.findall(index_text)
    indexed_counts = Counter(indexed)
    active = {question_id for question_id, question in questions.items() if question.state in ACTIVE_STATES}

    duplicate_index = sorted(question_id for question_id, count in indexed_counts.items() if count > 1)
    missing_index = sorted(active - set(indexed))
    inactive_index = sorted(set(indexed) - active)
    if duplicate_index:
        errors.append(f"Duplicate questions in the index: {', '.join(duplicate_index)}")
    if missing_index:
        errors.append(f"Active questions missing from the index: {', '.join(missing_index)}")
    if inactive_index:
        errors.append(f"Inactive questions present in the index: {', '.join(inactive_index)}")

    if LEGACY.exists():
        errors.append("The superseded notes/08-preguntas-abiertas.md registry still exists.")

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
                f"Profile {profile_name} omits required questions: {', '.join(missing)}"
            )
        if unexpected:
            errors.append(
                f"Profile {profile_name} includes unexpected questions: {', '.join(unexpected)}"
            )

    for path in (ROOT / "specification").glob("*.md"):
        for question_id in SPEC_QUESTION.findall(read(path)):
            question = questions.get(question_id)
            state = question.state if question is not None else None
            if state not in ACTIVE_STATES:
                errors.append(
                    f"{path.relative_to(ROOT)} references an unknown or inactive question in frontmatter: {question_id}"
                )

    for path in ROOT.rglob("*.md"):
        if path.is_relative_to(EXPORT_DIR):
            continue
        text = read(path)
        if "08-preguntas-abiertas" in text:
            errors.append(f"Link to the superseded registry: {path.relative_to(ROOT)}")
        for target in QUESTION_LINK.findall(text):
            target_path = ROOT / f"{target}.md"
            if not target_path.is_file():
                errors.append(
                    f"Link to an unknown question in {path.relative_to(ROOT)}: {target}"
                )

    counts = Counter(question.state for question in questions.values())
    if errors:
        for error in errors:
            failure(parsed.ui, "Question validation failed.", code="Mud.Questions.InvalidRegistry", details=error)
        return 1

    parsed.ui.success(
        "Mud questions: "
        f"{len(questions)} unique files; "
        f"{counts['open']} open, "
        f"{counts['partially-decided']} partially decided and "
        f"{counts['closed']} closed; "
        f"{len(indexed)} active entries verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
