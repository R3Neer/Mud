from __future__ import annotations

import tempfile
from pathlib import Path

import validate_spec_editorial as validator


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def question(question_id: str, resolved: str) -> str:
    return (
        "---\n"
        f"id: {question_id}\n"
        f"resolved: {resolved}\n"
        "---\n"
        f"# {question_id} — fixture\n"
    )


def document(body: str, questions: tuple[str, ...] = ()) -> str:
    if questions:
        question_field = "questions:\n" + "".join(
            f"  - {question_id}\n" for question_id in questions
        )
    else:
        question_field = "questions: []\n"
    return (
        "---\n"
        "title: Fixture\n"
        "status: proposed\n"
        "normative: true\n"
        f"{question_field}"
        "---\n"
        "# Fixture\n\n"
        f"{body}\n"
    )


def codes(findings: list[validator.Finding]) -> set[str]:
    return {finding.code for finding in findings}


def run_case(root: Path, name: str, content: str, expected: set[str]) -> None:
    target = root / "specification" / f"{name}.md"
    write(target, content)
    result = codes(validator.validate_repository(root))
    if result != expected:
        raise AssertionError(f"{name}: expected {sorted(expected)}, got {sorted(result)}")
    target.unlink()


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        write(root / "notes/questions/Q-001-activa.md", question("Q-001", "false"))
        write(root / "notes/questions/Q-002-closed.md", question("Q-002", "true"))
        write(
            root / "specification/00-editorial-conventions.md",
            document("Allowed examples here: D-999, ADR-998 and Q-002."),
        )

        run_case(
            root,
            "valid-active-question",
            document("Q-001 marks this present uncertainty.", ("Q-001",)),
            set(),
        )
        run_case(
            root,
            "decision-id",
            document("This rule comes from D-123."),
            {"E_DECISION_BODY"},
        )
        run_case(
            root,
            "adr-id",
            document("The rationale is in ADR-123."),
            {"E_DECISION_BODY"},
        )
        run_case(
            root,
            "migration-heading",
            document("## Update from current decision\n\nCurrent text."),
            {"E_EDITORIAL_MIGRATION"},
        )
        run_case(
            root,
            "migration-sentence",
            document("The previous wording is replaced by this wording."),
            {"E_EDITORIAL_MIGRATION"},
        )
        run_case(
            root,
            "closed-question-body",
            document("Q-002 still marks this behaviour.", ("Q-002",)),
            {"E_INACTIVE_QUESTION_BODY", "E_INACTIVE_QUESTION_FRONTMATTER"},
        )
        run_case(
            root,
            "active-question-not-declared",
            document("Q-001 marks this uncertainty."),
            {"E_QUESTION_NOT_DECLARED"},
        )
        run_case(
            root,
            "closed-question-frontmatter",
            document("Without a body reference.", ("Q-002",)),
            {"E_INACTIVE_QUESTION_FRONTMATTER"},
        )
        run_case(
            root,
            "unknown-question",
            document("Q-999 does not exist.", ("Q-999",)),
            {"E_UNKNOWN_QUESTION_BODY", "E_UNKNOWN_QUESTION_FRONTMATTER"},
        )

        mechanical = root / "specification/names/fixture.asdl"
        write(mechanical, "-- Q-001 remains open in this artefact.\n")
        if validator.validate_repository(root):
            raise AssertionError("una Q activa en artefacto sin frontmatter debe ser válida")
        mechanical.unlink()

    print("Editorial-barrier fixtures: 10 cases verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
