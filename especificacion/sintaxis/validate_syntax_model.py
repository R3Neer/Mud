#!/usr/bin/env python3
"""Valida la coherencia editorial entre EBNF, catálogo CST, cobertura y ASDL.

No implementa el parser de MUD ni valida semántica. Su objetivo es impedir que
una producción quede sin inventariar o que los archivos mecánicos diverjan.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import sys
from typing import Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Se requiere PyYAML para ejecutar este validador") from exc


@dataclass(frozen=True)
class Problem:
    file: str
    message: str


def extract_ebnf_block(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".ebnf":
        return text
    match = re.search(r"```ebnf\n(.*?)\n```", text, re.S)
    if not match:
        raise ValueError(f"{path}: no contiene un bloque ```ebnf```")
    return match.group(1)


def strip_comments(text: str) -> str:
    return re.sub(r"\(\*.*?\*\)", lambda m: " " * len(m.group(0)), text, flags=re.S)


def production_names(path: Path) -> list[str]:
    code = strip_comments(extract_ebnf_block(path))
    return re.findall(r"(?m)^([a-z][a-z0-9-]*)\s*::=", code)


def grammar_references(path: Path) -> set[str]:
    code = strip_comments(extract_ebnf_block(path))
    code = re.sub(r'"(?:[^"\\]|\\.)*"', "", code)
    return set(re.findall(r"\b[a-z][a-z0-9-]*\b", code))


def literal_terminals(path: Path) -> set[str]:
    code = strip_comments(extract_ebnf_block(path))
    return set(re.findall(r'"((?:[^"\\]|\\.)*)"', code))


def asdl_symbols(path: Path) -> set[str]:
    text = re.sub(r"--.*", "", path.read_text(encoding="utf-8"))
    symbols = set(re.findall(r"(?m)^\s*([a-z][a-z0-9_]*)\s*=", text))
    symbols.update(re.findall(r"\b([A-Z][A-Za-z0-9_]*)\s*(?:\(|\||\n)", text))
    # Constructores sin parámetros antes de | o fin de línea.
    symbols.update(re.findall(r"(?:=|\|)\s*([A-Z][A-Za-z0-9_]*)\b", text))
    symbols.update({"int", "string", "identifier"})
    return symbols


def asdl_types_and_uses(path: Path) -> tuple[set[str], set[str]]:
    text = re.sub(r"--.*", "", path.read_text(encoding="utf-8"))
    defined = set(re.findall(r"(?m)^\s*([a-z][a-z0-9_]*)\s*=", text))
    used = {
        match.group(1)
        for match in re.finditer(r"\b([a-z][a-z0-9_]*)[?*]?\s+[a-z][a-z0-9_]*\b", text)
    }
    return defined, used


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate(root: Path) -> list[Problem]:
    problems: list[Problem] = []
    grammar = root / "especificacion/gramatica/mud.ebnf"
    lexical = root / "especificacion/gramatica/mud-lexico.ebnf"
    kinds_path = root / "especificacion/sintaxis/mud-syntax-kinds.yaml"
    coverage_path = root / "especificacion/sintaxis/cobertura-sintactica.yaml"
    asdl_path = root / "especificacion/sintaxis/mud-surface-ast.asdl"

    syntax_productions = production_names(grammar)
    lexical_productions = production_names(lexical)
    kinds = load_yaml(kinds_path)

    for path, names in ((grammar, syntax_productions), (lexical, lexical_productions)):
        duplicates = sorted({name for name in names if names.count(name) > 1})
        for name in duplicates:
            problems.append(Problem(str(path), f"producción duplicada: {name}"))

    # La gramática léxica contiene cláusulas especiales ?...?... en prosa;
    # la comprobación automática de referencias se aplica a mud.ebnf.
    for name in sorted(grammar_references(grammar) - set(syntax_productions)):
        problems.append(Problem(str(grammar), f"referencia a producción no definida: {name}"))
    coverage = load_yaml(coverage_path)
    symbols = asdl_symbols(asdl_path)
    asdl_defined, asdl_used = asdl_types_and_uses(asdl_path)

    kind_syntax = kinds.get("syntax_nodes", {})
    kind_lexical = kinds.get("lexical_forms", {})
    covered = coverage.get("productions", {})
    fixed_tokens = {str(item.get("spelling")) for item in kinds.get("fixed_tokens", [])}

    for spelling in sorted(literal_terminals(grammar) - fixed_tokens):
        problems.append(Problem(str(kinds_path), f"terminal literal sin inventariar: {spelling!r}"))
    for spelling in sorted(fixed_tokens - literal_terminals(grammar)):
        problems.append(Problem(str(kinds_path), f"terminal fijo huérfano: {spelling!r}"))

    for name in syntax_productions:
        if name not in kind_syntax:
            problems.append(Problem(str(kinds_path), f"falta la producción sintáctica {name}"))
        if name not in covered:
            problems.append(Problem(str(coverage_path), f"falta cobertura para {name}"))

    for name in lexical_productions:
        if name not in kind_lexical:
            problems.append(Problem(str(kinds_path), f"falta la producción léxica {name}"))

    for name in sorted(set(kind_syntax) - set(syntax_productions)):
        problems.append(Problem(str(kinds_path), f"nodo CST huérfano: {name}"))
    for name in sorted(set(kind_lexical) - set(lexical_productions)):
        problems.append(Problem(str(kinds_path), f"forma léxica huérfana: {name}"))
    for name in sorted(set(covered) - set(syntax_productions)):
        problems.append(Problem(str(coverage_path), f"entrada de cobertura huérfana: {name}"))

    for name, item in covered.items():
        ast = item.get("ast", {})
        if not ast.get("disposition"):
            problems.append(Problem(str(coverage_path), f"{name}: falta disposition"))
        target = ast.get("target")
        if target and target not in symbols:
            problems.append(Problem(str(coverage_path), f"{name}: destino ASDL desconocido {target}"))
        expected_kind = kind_syntax.get(name, {}).get("kind")
        if expected_kind and item.get("cst") != expected_kind:
            problems.append(Problem(str(coverage_path), f"{name}: CST {item.get('cst')} != {expected_kind}"))

    for unknown in sorted(asdl_used - asdl_defined - {"int", "string", "identifier"}):
        problems.append(Problem(str(asdl_path), f"tipo ASDL no definido: {unknown}"))

    cases_path = root / "especificacion/sintaxis/casos/cst-ast.yaml"
    cases = load_yaml(cases_path)
    seen_case_ids: set[str] = set()
    for case in cases.get("cases", []):
        case_id = case.get("id")
        if not case_id:
            problems.append(Problem(str(cases_path), "caso sin id"))
        elif case_id in seen_case_ids:
            problems.append(Problem(str(cases_path), f"id de caso duplicado: {case_id}"))
        else:
            seen_case_ids.add(case_id)
        if "produces_ast" not in case:
            problems.append(Problem(str(cases_path), f"{case_id}: falta produces_ast"))

    # Propiedades globales del AST.
    ast_text = asdl_path.read_text(encoding="utf-8")
    required = ["module MUDSurface", "project = MudProject", "source_file = MudFile", "flag = Disabled | Enabled"]
    for snippet in required:
        if snippet not in ast_text:
            problems.append(Problem(str(asdl_path), f"falta contrato requerido: {snippet}"))

    return problems


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args(argv)
    problems = validate(args.root)
    if problems:
        for problem in problems:
            print(f"ERROR {problem.file}: {problem.message}")
        print(f"\n{len(problems)} problema(s)")
        return 1
    print("OK: gramática, CST, cobertura y ASDL están sincronizados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
