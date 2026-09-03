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
        raise AssertionError(f"{name}: esperado {sorted(expected)}, obtenido {sorted(result)}")
    target.unlink()


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        write(root / "notes/questions/Q-001-activa.md", question("Q-001", "false"))
        write(root / "notes/questions/Q-002-cerrada.md", question("Q-002", "true"))
        write(
            root / "specification/00-convenciones-editoriales.md",
            document("Ejemplos permitidos aquí: D-999, ADR-998 y Q-002."),
        )

        run_case(
            root,
            "valid-active-question",
            document("Q-001 delimita esta incertidumbre presente.", ("Q-001",)),
            set(),
        )
        run_case(
            root,
            "decision-id",
            document("Esta regla procede de D-123."),
            {"E_DECISION_BODY"},
        )
        run_case(
            root,
            "adr-id",
            document("La justificación está en ADR-123."),
            {"E_DECISION_BODY"},
        )
        run_case(
            root,
            "migration-heading",
            document("## Actualización por decisión vigente\n\nTexto actual."),
            {"E_EDITORIAL_MIGRATION"},
        )
        run_case(
            root,
            "migration-sentence",
            document("La formulación anterior se sustituye por esta redacción."),
            {"E_EDITORIAL_MIGRATION"},
        )
        run_case(
            root,
            "closed-question-body",
            document("Q-002 todavía delimita este comportamiento.", ("Q-002",)),
            {"E_INACTIVE_QUESTION_BODY", "E_INACTIVE_QUESTION_FRONTMATTER"},
        )
        run_case(
            root,
            "active-question-not-declared",
            document("Q-001 delimita esta incertidumbre."),
            {"E_QUESTION_NOT_DECLARED"},
        )
        run_case(
            root,
            "closed-question-frontmatter",
            document("Sin referencia corporal.", ("Q-002",)),
            {"E_INACTIVE_QUESTION_FRONTMATTER"},
        )
        run_case(
            root,
            "unknown-question",
            document("Q-999 no existe.", ("Q-999",)),
            {"E_UNKNOWN_QUESTION_BODY", "E_UNKNOWN_QUESTION_FRONTMATTER"},
        )

        mechanical = root / "specification/names/fixture.asdl"
        write(mechanical, "-- Q-001 permanece abierta en este artefacto.\n")
        if validator.validate_repository(root):
            raise AssertionError("una Q activa en artefacto sin frontmatter debe ser válida")
        mechanical.unlink()

    print("Fixtures de barrera editorial: 10 casos verificados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
