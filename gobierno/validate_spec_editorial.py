from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {".md", ".ebnf", ".asdl", ".yaml", ".yml"}
DECISION_ID = re.compile(r"\b(?:ADR|D)-\d{3}\b")
QUESTION_ID = re.compile(r"\bQ-\d{3}\b")
RESOLVED_FIELD = re.compile(r"^resolved:\s*(true|false)?\s*$", re.MULTILINE)
QUESTION_FILE = re.compile(r"^(Q-\d{3})-.+\.md$")
MIGRATION_PATTERNS = (
    re.compile(
        r"^#{1,6}\s+(?:Actualización|Revisión|Corrección|Sustitución)\s+"
        r"(?:por|según|tras)\b.*$",
        re.IGNORECASE | re.MULTILINE,
    ),
    re.compile(
        r"\b(?:la|el)\s+(?:regla|formulación|redacción|versión)\s+"
        r"(?:anterior|previa)\s+(?:se\s+)?"
        r"(?:sustituye|reemplaza|actualiza|corrige)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:se\s+)?(?:sustituye|reemplaza|actualiza|corrige)\s+"
        r"(?:la|el)\s+(?:regla|formulación|redacción|versión)\s+"
        r"(?:anterior|previa)\b",
        re.IGNORECASE,
    ),
)


@dataclass(frozen=True)
class Finding:
    code: str
    path: Path
    line: int
    detail: str

    def render(self, root: Path) -> str:
        try:
            relative = self.path.relative_to(root)
        except ValueError:
            relative = self.path
        return f"{relative}:{self.line}: {self.code}: {self.detail}"


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    marker = text.find("\n---\n", 4)
    if marker == -1:
        return None, text
    return text[4:marker], text[marker + 5 :]


def frontmatter_questions(frontmatter: str | None) -> set[str]:
    if frontmatter is None:
        return set()

    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        match = re.fullmatch(r"questions:\s*(.*)", line)
        if match is None:
            continue

        tail = match.group(1).strip()
        if tail:
            if tail == "[]":
                return set()
            return set(QUESTION_ID.findall(tail))

        result: set[str] = set()
        for item in lines[index + 1 :]:
            if not item.startswith((" ", "\t")):
                break
            stripped = item.strip()
            if stripped.startswith("-"):
                result.update(QUESTION_ID.findall(stripped))
        return result

    return set()


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def load_question_states(root: Path) -> dict[str, bool]:
    states: dict[str, bool] = {}
    for path in sorted((root / "notas" / "preguntas").glob("Q-*.md")):
        filename = QUESTION_FILE.fullmatch(path.name)
        if filename is None:
            continue
        text = path.read_text(encoding="utf-8")
        resolved = RESOLVED_FIELD.search(text)
        if resolved is None:
            continue
        states[filename.group(1)] = resolved.group(1) != "true"
    return states


def iter_spec_text_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in (root / "especificacion").rglob("*")
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS
    )


def validate_file(
    path: Path,
    root: Path,
    question_states: dict[str, bool],
) -> list[Finding]:
    conventions = root / "especificacion" / "00-convenciones-editoriales.md"
    if path.resolve() == conventions.resolve():
        return []

    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".md":
        frontmatter, body = split_frontmatter(text)
    else:
        frontmatter, body = None, text
    body_offset = len(text) - len(body)
    findings: list[Finding] = []

    for match in DECISION_ID.finditer(body):
        findings.append(
            Finding(
                "E_DECISION_BODY",
                path,
                line_number(text, body_offset + match.start()),
                f"identificador decisional {match.group(0)} en cuerpo normativo",
            )
        )

    seen_migrations: set[tuple[int, str]] = set()
    for pattern in MIGRATION_PATTERNS:
        for match in pattern.finditer(body):
            key = (match.start(), match.group(0))
            if key in seen_migrations:
                continue
            seen_migrations.add(key)
            findings.append(
                Finding(
                    "E_EDITORIAL_MIGRATION",
                    path,
                    line_number(text, body_offset + match.start()),
                    f"narración de migración editorial: {match.group(0).strip()}",
                )
            )

    declared_questions = frontmatter_questions(frontmatter)
    body_questions = set(QUESTION_ID.findall(body))

    for question_id in sorted(body_questions):
        active = question_states.get(question_id)
        offset = body.find(question_id)
        line = line_number(text, body_offset + max(offset, 0))
        if active is None:
            findings.append(
                Finding(
                    "E_UNKNOWN_QUESTION_BODY",
                    path,
                    line,
                    f"pregunta inexistente {question_id} en cuerpo normativo",
                )
            )
        elif not active:
            findings.append(
                Finding(
                    "E_INACTIVE_QUESTION_BODY",
                    path,
                    line,
                    f"pregunta inactiva {question_id} en cuerpo normativo",
                )
            )
        elif frontmatter is not None and question_id not in declared_questions:
            findings.append(
                Finding(
                    "E_QUESTION_NOT_DECLARED",
                    path,
                    line,
                    f"pregunta activa {question_id} citada en el cuerpo pero ausente de questions",
                )
            )

    if frontmatter is not None:
        for question_id in sorted(declared_questions):
            active = question_states.get(question_id)
            line = 1
            for index, fm_line in enumerate(frontmatter.splitlines(), start=2):
                if question_id in fm_line:
                    line = index
                    break
            if active is None:
                findings.append(
                    Finding(
                        "E_UNKNOWN_QUESTION_FRONTMATTER",
                        path,
                        line,
                        f"questions: contiene una pregunta inexistente: {question_id}",
                    )
                )
            elif not active:
                findings.append(
                    Finding(
                        "E_INACTIVE_QUESTION_FRONTMATTER",
                        path,
                        line,
                        f"questions: conserva una pregunta inactiva: {question_id}",
                    )
                )

    return findings


def validate_repository(root: Path = ROOT) -> list[Finding]:
    question_states = load_question_states(root)
    findings: list[Finding] = []
    for path in iter_spec_text_files(root):
        findings.extend(validate_file(path, root, question_states))
    return findings


def main() -> int:
    findings = validate_repository(ROOT)
    if findings:
        for finding in findings:
            print(f"ERROR: {finding.render(ROOT)}", file=sys.stderr)
        return 1

    checked = len(iter_spec_text_files(ROOT)) - 1
    active = sum(1 for state in load_question_states(ROOT).values() if state)
    print(
        "Barrera editorial MUD: "
        f"{checked} archivos de especificación comprobados; "
        f"{active} preguntas activas reconocidas; sin regresiones MUD-EDIT-002."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
