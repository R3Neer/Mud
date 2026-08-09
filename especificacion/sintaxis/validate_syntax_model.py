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

    # Regresiones normativas que la mera sincronización de nombres no detecta.
    forbidden_fragments = {
        root / "especificacion/sintaxis/mud-surface-ast.asdl": [
            "AnchorInterpolation(",
            "intrinsic_name_override",
        ],
        root / "especificacion/06-lexico.md": [
            "después `anchor{` y `{`",
        ],
        root / "especificacion/04-modelo-matematico.md": [
            "`name: Text` intrínseco",
            "Una única declaración global `start with` determina un conjunto finito",
        ],
        root / "especificacion/07-gramatica-concreta.md": [
            "propiedad intrínseca e inmutable `name: Text`",
            "`unique` se prohíbe estáticamente en diccionarios",
            "Los paréntesis son obligatorios para anidar un diccionario como valor",
            "`anchor{d}` inserta el ancla canónica",
        ],
        root / "especificacion/08-sintaxis-abstracta.md": [
            "sobrescritura opcional del `name` intrínseco",
            "`prefixes = empty` → `NoPrefixes`",
        ],
        root / "especificacion/sintaxis/cst-a-ast-superficial.md": [
            "`intrinsic_name_override`",
            "produce una colección sintética:",
            "| `name = e` | `name = e` |",
        ],
    }
    for path, fragments in forbidden_fragments.items():
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment in text:
                problems.append(Problem(str(path), f"contrato retirado todavía presente: {fragment}"))

    required_fragments = {
        root / "especificacion/sintaxis/mud-surface-ast.asdl": [
            "ExactTypeTestExpr(",
        ],
        root / "especificacion/sintaxis/mud-resolved-ast.asdl": [
            "ExactNominalTypeTestExpr(",
            "ExactDictionarySetOperationExpr(",
            "FunctionalDictionarySetOperationExpr(",
        ],
    }
    for path, fragments in required_fragments.items():
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                problems.append(Problem(str(path), f"falta contrato D-086: {fragment}"))

    for case in cases.get("cases", []):
        source = case.get("source")
        if not isinstance(source, str):
            continue
        diagnostics = set(case.get("expected_diagnostics", []))
        if "legacy-anchor-interpolation" not in diagnostics and "anchor{" in source:
            problems.append(Problem(str(cases_path), f"{case.get('id')}: ejemplo válido usa anchor{{...}}"))
        if ("root unit" in source or "point over" in source) and "legacy-unit-metadata-without-postfix" not in diagnostics:
            for metadata in ("name", "plural", "abbreviation", "prefixes", "format"):
                if re.search(rf"(?m)^\s*{metadata}\s*=", source):
                    problems.append(Problem(str(cases_path), f"{case.get('id')}: metadato {metadata} sin ~"))

    required_case_ids = {
        "subaction-internal-call",
        "subaction-root-request-rejected",
        "mud-path-not-membership",
        "not-in-chain-rejected",
        "exact-dictionary-substitution",
        "exact-dictionary-iterate-keys",
        "exact-dictionary-iterate-associations",
        "exact-dictionary-unique-collision-noop",
        "functional-explicit-value-selector",
        "functional-explicit-interval-selector",
        "functional-implicit-selector-rejected",
        "functional-boolean-selector",
        "functional-external-read-dependencies",
        "functional-recursion-decreasing",
        "functional-recursion-without-descent-rejected",
        "functional-mut-exterior-rejected",
        "functional-mut-interior-rejected",
        "functional-direct-iteration-rejected",
        "functional-branch-after-fallback-rejected",
        "functional-duplicate-fallback-rejected",
        "firstmatch-unique-redundant",
        "allmatches-overlap-deduplicated",
        "nested-dictionary-application",
        "selection-direct-filter",
        "selection-dictionary-preserves-associations",
        "create-built-in-thing-rejected",
        "destroy-built-in-thing-rejected",
        "all-any-rejected",
        "any-field-requires-initializer",
        "metadata-file-behavior-warning",
        "cardinality-inferred-zero",
        "cardinality-inferred-one",
        "cardinality-inferred-three",
        "cardinality-dictionary-is-one-outer-value",
        "start-with-empty-one-many-deduplicated",
        "exact-type-test-multiple-specialization",
        "functional-branch-edit-operations",
        "functional-composed-dependencies-same-snapshot",
        "functional-ordered-intersection-preserves-order",
        "functional-ordered-difference-preserves-order",
        "exact-dictionary-operation-order",
        "exact-dictionary-operation-unique-noop",
        "firstmatch-no-match-empty",
        "allmatches-no-match-empty",
        "all-thing-excludes-built-in",
        "any-equality-uses-effective-type",
        "any-order-rejected",
        "metadata-path-assignment-rejected",
        "metadata-file-assignment-rejected",
        "iis-negation-equivalence",
        "not-iis-spelling-rejected",
        "is-iis-equality-distinction",
    }
    present_case_ids = {case.get("id") for case in cases.get("cases", [])}
    for missing in sorted(required_case_ids - present_case_ids):
        problems.append(Problem(str(cases_path), f"falta caso de cobertura D-086 v4: {missing}"))

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
