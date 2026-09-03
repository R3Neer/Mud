#!/usr/bin/env python3
"""Valida la coherencia editorial entre EBNF, catálogo CST, cobertura y ASDL.

No implementa el parser de MUD ni valida semántica. Su objetivo es impedir que
una producción quede sin inventariar o que los archivos mecánicos diverjan.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Mud syntax validation requires PyYAML. "
        "Install it with: python -m pip install -r tooling/requirements.txt"
    ) from exc

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from tooling.cli_support import (  # noqa: E402
    HelpCatalogue,
    HelpItem,
    MudArgumentParser,
    add_presentation_arguments,
    failure,
    parse_cli,
)


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
        raise ValueError(f"{path}: does not contain an ```ebnf``` block")
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
    grammar = root / "specification/grammar/mud.ebnf"
    lexical = root / "specification/grammar/mud-lexico.ebnf"
    kinds_path = root / "specification/syntax/mud-syntax-kinds.yaml"
    coverage_path = root / "specification/syntax/cobertura-sintactica.yaml"
    asdl_path = root / "specification/syntax/mud-surface-ast.asdl"
    nominal_hir_path = root / "specification/names/mud-nominal-hir.asdl"
    retired_ir_dir = root / "specification/ir"
    retired_resolved_ast_path = root / "specification/syntax/mud-resolved-ast.asdl"

    syntax_productions = production_names(grammar)
    lexical_productions = production_names(lexical)
    kinds = load_yaml(kinds_path)

    for path, names in ((grammar, syntax_productions), (lexical, lexical_productions)):
        duplicates = sorted({name for name in names if names.count(name) > 1})
        for name in duplicates:
            problems.append(Problem(str(path), f"duplicate production: {name}"))

    # La gramática léxica contiene cláusulas especiales ?...?... en prosa;
    # la comprobación automática de references se aplica a mud.ebnf.
    for name in sorted(grammar_references(grammar) - set(syntax_productions)):
        problems.append(Problem(str(grammar), f"reference to undefined production: {name}"))
    coverage = load_yaml(coverage_path)
    symbols = asdl_symbols(asdl_path)
    asdl_defined, asdl_used = asdl_types_and_uses(asdl_path)
    if retired_resolved_ast_path.exists():
        problems.append(Problem(str(retired_resolved_ast_path), "retired contract: use surface AST + nominal HIR"))
    if not nominal_hir_path.exists():
        problems.append(Problem(str(nominal_hir_path), "the nominal HIR contract is missing"))
        nominal_hir_defined, nominal_hir_used = set(), set()
    else:
        nominal_hir_defined, nominal_hir_used = asdl_types_and_uses(nominal_hir_path)
    if retired_ir_dir.exists():
        problems.append(Problem(str(retired_ir_dir), "retired surface: the nominal HIR lives in specification/names and no normative semantic IR exists yet"))

    kind_syntax = kinds.get("syntax_nodes", {})
    kind_lexical = kinds.get("lexical_forms", {})
    covered = coverage.get("productions", {})
    fixed_tokens = {str(item.get("spelling")) for item in kinds.get("fixed_tokens", [])}

    for spelling in sorted(literal_terminals(grammar) - fixed_tokens):
        problems.append(Problem(str(kinds_path), f"literal terminal is not inventoried: {spelling!r}"))
    for spelling in sorted(fixed_tokens - literal_terminals(grammar)):
        problems.append(Problem(str(kinds_path), f"orphaned fixed terminal: {spelling!r}"))

    for name in syntax_productions:
        if name not in kind_syntax:
            problems.append(Problem(str(kinds_path), f"syntax production is missing: {name}"))
        if name not in covered:
            problems.append(Problem(str(coverage_path), f"coverage is missing for {name}"))

    for name in lexical_productions:
        if name not in kind_lexical:
            problems.append(Problem(str(kinds_path), f"lexical production is missing: {name}"))

    for name in sorted(set(kind_syntax) - set(syntax_productions)):
        problems.append(Problem(str(kinds_path), f"orphaned CST node: {name}"))
    for name in sorted(set(kind_lexical) - set(lexical_productions)):
        problems.append(Problem(str(kinds_path), f"orphaned lexical form: {name}"))
    for name in sorted(set(covered) - set(syntax_productions)):
        problems.append(Problem(str(coverage_path), f"orphaned coverage entry: {name}"))

    for name, item in covered.items():
        ast = item.get("ast", {})
        if not ast.get("disposition"):
            problems.append(Problem(str(coverage_path), f"{name}: disposition is missing"))
        target = ast.get("target")
        if target and target not in symbols:
            problems.append(Problem(str(coverage_path), f"{name}: unknown ASDL target {target}"))
        expected_kind = kind_syntax.get(name, {}).get("kind")
        if expected_kind and item.get("cst") != expected_kind:
            problems.append(Problem(str(coverage_path), f"{name}: CST {item.get('cst')} != {expected_kind}"))

    for unknown in sorted(asdl_used - asdl_defined - {"int", "string", "identifier"}):
        problems.append(Problem(str(asdl_path), f"undefined ASDL type: {unknown}"))
    for unknown in sorted(nominal_hir_used - nominal_hir_defined - {"int", "string", "identifier"}):
        problems.append(Problem(str(nominal_hir_path), f"undefined ASDL type: {unknown}"))
    if nominal_hir_path.exists():
        hir_text = nominal_hir_path.read_text(encoding="utf-8")
        if "module MUDNominalHIR" not in hir_text:
            problems.append(Problem(str(nominal_hir_path), "module MUDNominalHIR is missing"))
        for fragment in ["semantic_type", "effective_domain", "collection_shape", "effective_cardinality", "termination_evidence", "ConversionExpr"]:
            if fragment in hir_text:
                problems.append(Problem(str(nominal_hir_path), f"the nominal HIR contains forbidden elaboration: {fragment}"))
    if nominal_hir_path.exists():
        hir_text = nominal_hir_path.read_text(encoding="utf-8")
        for fragment in ["Owns(", "Specializes(", "RefersTo("]:
            if fragment not in hir_text:
                problems.append(Problem(str(nominal_hir_path), f"required nominal relationship is missing: {fragment}"))

    cases_path = root / "specification/syntax/cases/cst-ast.yaml"
    cases = load_yaml(cases_path)
    seen_case_ids: set[str] = set()
    for case in cases.get("cases", []):
        case_id = case.get("id")
        if not case_id:
            problems.append(Problem(str(cases_path), "case has no id"))
        elif case_id in seen_case_ids:
            problems.append(Problem(str(cases_path), f"duplicate case id: {case_id}"))
        else:
            seen_case_ids.add(case_id)
        if "produces_ast" not in case:
            problems.append(Problem(str(cases_path), f"{case_id}: produces_ast is missing"))

    # Propiedades globales del AST.
    ast_text = asdl_path.read_text(encoding="utf-8")
    required = ["module MUDSurface", "project = MudProject", "source_file = MudFile", "flag = Disabled | Enabled"]
    for snippet in required:
        if snippet not in ast_text:
            problems.append(Problem(str(asdl_path), f"required contract is missing: {snippet}"))

    # Regresiones normativas que la mera sincronización de nombres no detecta.
    forbidden_fragments = {
        root / "specification/syntax/mud-surface-ast.asdl": [
            "AnchorInterpolation(",
            "intrinsic_name_override",
        ],
        root / "specification/06-lexico.md": [
            "después `anchor{` y `{`",
        ],
        root / "specification/04-modelo-matematico.md": [
            "`name: Text` intrínseco",
            "Una única declaración global `start with` determina un conjunto finito",
        ],
        root / "specification/07-gramatica-concreta.md": [
            "propiedad intrínseca e inmutable `name: Text`",
            "`unique` se prohíbe estáticamente en diccionarios",
            "Los paréntesis son obligatorios para anidar un diccionario como valor",
            "`anchor{d}` inserta el ancla canónica",
        ],
        root / "specification/08-sintaxis-abstracta.md": [
            "sobrescritura opcional del `name` intrínseco",
            "`prefixes = empty` → `NoPrefixes`",
        ],
        root / "specification/syntax/cst-a-ast-superficial.md": [
            "`intrinsic_name_override`",
            "produce una colección sintética:",
            "| `name = e` | `name = e` |",
        ],
    }
    for path, fragments in forbidden_fragments.items():
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment in text:
                problems.append(Problem(str(path), f"retired contract is still present: {fragment}"))

    required_fragments = {
        root / "specification/syntax/mud-surface-ast.asdl": [
            "ExactTypeTestExpr(",
            "ThingInitializer(",
        ],
    }
    for path, fragments in required_fragments.items():
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                problems.append(Problem(str(path), f"D-086 contract is missing: {fragment}"))

    for case in cases.get("cases", []):
        source = case.get("source")
        if not isinstance(source, str):
            continue
        diagnostics = set(case.get("expected_diagnostics", []))
        if "legacy-anchor-interpolation" not in diagnostics and "anchor{" in source:
            problems.append(Problem(str(cases_path), f"{case.get('id')}: valid example uses anchor{{...}}"))
        if ("root unit" in source or "point over" in source) and "legacy-unit-metadata-without-postfix" not in diagnostics:
            for metadata in ("name", "plural", "abbreviation", "prefixes", "format"):
                if re.search(rf"(?m)^\s*{metadata}\s*=", source):
                    problems.append(Problem(str(cases_path), f"{case.get('id')}: metadata {metadata} has no ~"))

    required_case_ids = {
        "thing-concrete-initializer",
        "thing-name-field-initializer",
        "abstract-thing-inherited-initializer",
        "thing-local-field-and-initializer-rejected",
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
        "explicit-representation-to-alias",
        "typed-representation-does-not-implicitly-become-alias",
        "contextual-alias-comparison-literal",
        "contextual-basic-alias-literal",
        "iis-negation-equivalence",
        "not-iis-spelling-rejected",
        "is-iis-equality-distinction",
    }
    present_case_ids = {case.get("id") for case in cases.get("cases", [])}
    for missing in sorted(required_case_ids - present_case_ids):
        problems.append(Problem(str(cases_path), f"D-086 v4 coverage case is missing: {missing}"))

    return problems


def main(argv: Iterable[str] | None = None) -> int:
    invocation = "python specification/syntax/validate_syntax_model.py"
    catalogue = HelpCatalogue(
        product="MUD SYNTAX MODEL",
        version="",
        description="Check that the grammar, CST catalogue, coverage and ASDL models agree.",
        invocation=invocation,
        groups=(),
        commands=(),
        usage=(f"{invocation} [--root PATH] [--colour MODE] [--ascii]",),
        global_items=(
            HelpItem("--root PATH", "Repository root to inspect. Default: the current Mud repository."),
            HelpItem("--colour auto|always|never", "Control colour for human output. Default: auto; NO_COLOR disables it."),
            HelpItem("--ascii", "Use ASCII status symbols when Unicode is unsuitable."),
        ),
        notes=("Running without arguments validates the current Mud repository.",),
        show_help_on_empty=False,
    )
    parser = MudArgumentParser(prog=invocation, error_code="Mud.Syntax.InvalidArguments")
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT)
    add_presentation_arguments(parser)
    values = None if argv is None else tuple(argv)
    parsed = parse_cli(parser, catalogue, values)
    if parsed.exit_code is not None:
        return parsed.exit_code
    args = parsed.arguments
    assert args is not None
    problems = validate(args.root)
    if problems:
        for problem in problems:
            failure(
                parsed.ui,
                "The syntax model is inconsistent.",
                code="Mud.Syntax.InconsistentModel",
                details=f"{problem.file}: {problem.message}",
            )
        parsed.ui.failure(f"{len(problems)} problem(s) found.")
        return 1
    parsed.ui.success("Grammar, CST, coverage and ASDL are synchronised.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
