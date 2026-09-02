"""Comprobaciones estructurales para las gramáticas EBNF de MUD.

No sustituye a un parser EBNF. Detecta los errores editoriales que más fácilmente
rompen una gramática mantenida a mano: símbolos duplicados, indefinidos o
inalcanzables desde el símbolo inicial.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from tooling.cli_support import (  # noqa: E402
    HelpCatalogue,
    MudArgumentParser,
    add_presentation_arguments,
    failure,
    parse_cli,
)


COMMENT = re.compile(r"\(\*.*?\*\)", re.DOTALL)
SPECIAL = re.compile(r"\?.*?\?", re.DOTALL)
TERMINAL = re.compile(r'"(?:[^"\\]|\\.)*"')
PRODUCTION_HEAD = re.compile(r"([a-z][a-z0-9-]*)\s*::=\s*")
REFERENCE = re.compile(r"\b[a-z][a-z0-9-]*\b")


def productions(source: str) -> list[tuple[str, str]]:
    """Separa producciones sin confundir el terminal ";" con su cierre."""

    result: list[tuple[str, str]] = []
    position = 0

    while position < len(source):
        while position < len(source) and source[position].isspace():
            position += 1
        if source[position:].strip() == "":
            break

        head = PRODUCTION_HEAD.match(source, position)
        if head is None:
            excerpt = source[position : position + 40].splitlines()[0]
            raise ValueError(f"text outside a production: {excerpt!r}")

        name = head.group(1)
        cursor = head.end()
        in_terminal = False
        in_special = False

        while cursor < len(source):
            character = source[cursor]
            if character == '"' and not in_special:
                in_terminal = not in_terminal
            elif character == "?" and not in_terminal:
                in_special = not in_special
            elif character == ";" and not in_terminal and not in_special:
                result.append((name, source[head.end() : cursor]))
                position = cursor + 1
                break
            cursor += 1
        else:
            raise ValueError(f"production without ';': {name}")

        while position < len(source) and source[position].isspace():
            position += 1

    return result


def balanced_meta(body: str) -> bool:
    cleaned = TERMINAL.sub("", SPECIAL.sub("", body))
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for character in cleaned:
        if character in "([{":
            stack.append(character)
        elif character in pairs:
            if not stack or stack.pop() != pairs[character]:
                return False
    return not stack


def grammar_symbols(
    path: Path,
) -> tuple[dict[str, set[str]], list[str], list[str]]:
    source = COMMENT.sub("", path.read_text(encoding="utf-8"))

    definitions: dict[str, set[str]] = {}
    duplicates: list[str] = []
    malformed: list[str] = []

    for name, body in productions(source):
        if name in definitions:
            duplicates.append(name)
        cleaned = TERMINAL.sub("", SPECIAL.sub("", body))
        definitions[name] = set(REFERENCE.findall(cleaned))
        if not balanced_meta(body):
            malformed.append(name)

    return definitions, duplicates, malformed


def validate(path: Path, start: str) -> list[str]:
    try:
        definitions, duplicates, malformed = grammar_symbols(path)
    except ValueError as error:
        return [f"{path}: {error}"]

    errors = [f"{path}: duplicate production: {name}" for name in duplicates]
    errors.extend(
        f"{path}: metadelimitadores desequilibrados: {name}"
        for name in malformed
    )

    if start not in definitions:
        errors.append(f"{path}: unknown start symbol: {start}")
        return errors

    referenced = set().union(*definitions.values()) if definitions else set()
    for name in sorted(referenced - definitions.keys()):
        errors.append(f"{path}: undefined symbol: {name}")

    reachable: set[str] = set()
    pending = [start]
    while pending:
        name = pending.pop()
        if name in reachable or name not in definitions:
            continue
        reachable.add(name)
        pending.extend(definitions[name] - reachable)

    for name in sorted(definitions.keys() - reachable):
        errors.append(f"{path}: unreachable production: {name}")

    return errors


def main(argv: list[str] | None = None) -> int:
    invocation = "python especificacion/gramatica/validate_grammar.py"
    catalogue = HelpCatalogue(
        product="MUD GRAMMAR",
        version="",
        description="Validate grammar symbols, uniqueness and reachability.",
        invocation=invocation,
        groups=(),
        commands=(),
        usage=(f"{invocation} [--colour MODE] [--ascii]",),
        notes=("Running without arguments validates both normative EBNF grammars.",),
        show_help_on_empty=False,
    )
    parser = MudArgumentParser(prog=invocation, error_code="Mud.Grammar.InvalidArguments")
    add_presentation_arguments(parser)
    parsed = parse_cli(parser, catalogue, argv)
    if parsed.exit_code is not None:
        return parsed.exit_code
    root = Path(__file__).resolve().parent
    checks = (
        (root / "mud-lexico.ebnf", "mud-source"),
        (root / "mud.ebnf", "mud-file"),
    )
    errors = [error for path, start in checks for error in validate(path, start)]

    if errors:
        for error in errors:
            failure(parsed.ui, "Grammar validation failed.", code="Mud.Grammar.Invalid", details=error)
        return 1

    parsed.ui.success("Mud grammars: all symbols are defined, unique and reachable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
