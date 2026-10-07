#!/usr/bin/env python3
"""Validate editorial consistency between EBNF, the CST catalogue, coverage and ASDL.

This does not implement the MUD parser or validate semantics. Its purpose is to
prevent an unlisted production or divergence between mechanical files.
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
    # Parameterless constructors before | or end of line.
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


def nominal_hir_contract_problems(text: str) -> list[str]:
    """Check nominal lookup storage without performing receiver elaboration."""
    code = re.sub(r"--.*", "", text)
    problems: list[str] = []
    if "module MUDNominalHIR" not in code:
        problems.append("module MUDNominalHIR is missing")
    for fragment in ["semantic_type", "effective_domain", "collection_shape", "effective_cardinality", "termination_evidence", "ConversionExpr"]:
        if fragment in code:
            problems.append(f"the nominal HIR contains forbidden elaboration: {fragment}")
    for fragment in ["Owns(", "Specializes(", "RefersTo("]:
        if fragment not in code:
            problems.append(f"required nominal relationship is missing: {fragment}")

    constructors = {
        "ResolvedReference": "surface_ref occurrence, symbol_id target, string role",
        "PendingReceiverCall": "surface_ref occurrence, symbol_id* candidates, lookup_level level, string role",
    }
    for name, expected in constructors.items():
        matches = re.findall(rf"\b{name}\s*\(([^()]*)\)", code, re.S)
        if len(matches) != 1 or re.sub(r"\s+", " ", matches[0]).strip() != expected:
            problems.append(f"{name} must preserve the nominal reference contract: {expected}")
    reference_sum = re.search(r"\bnominal_reference\s*=\s*(.*?)(?=\n\s*[a-z][a-z0-9_]*\s*=|\n\s*\})", code, re.S)
    if not reference_sum or re.findall(r"\b([A-Z][A-Za-z0-9_]*)\s*\(", reference_sum.group(1)) != ["ResolvedReference", "PendingReceiverCall"]:
        problems.append("nominal_reference must distinguish resolved targets from pending receiver calls")
    if not re.search(r"\bnominal_reference\*\s+bindings\b", code):
        problems.append("NominalHIR bindings must preserve resolved and pending references")
    levels = re.search(r"\blookup_level\s*=\s*(.*?)(?=\n\s*[a-z][a-z0-9_]*\s*=|\n\s*\})", code, re.S)
    expected_levels = {"LexicalLevel", "OwnerLevel", "CurrentPathLevel", "ExactUsingLevel", "RecursiveUsingLevel", "BuiltinLevel"}
    if not levels or set(re.findall(r"\b[A-Z][A-Za-z0-9_]*\b", levels.group(1))) != expected_levels:
        problems.append("lookup_level must preserve the six nominal lookup priorities")
    return problems


def local_contract_problems(grammar_text: str, ast_text: str) -> list[str]:
    """Guard annotation contexts and pattern/preamble distinctions, not inference."""
    from specification.grammar.validate_grammar import productions, COMMENT

    rhs = dict(productions(COMMENT.sub("", grammar_text)))
    refs = {
        name: set(re.findall(r"\b[a-z][a-z0-9-]*\b", re.sub(r'"[^"]*"', "", body)))
        for name, body in rhs.items()
    }

    def reachable(start: str, target: str) -> bool:
        pending, seen = [start], set()
        while pending:
            name = pending.pop()
            if name == target:
                return True
            if name not in seen:
                seen.add(name)
                pending.extend(refs.get(name, set()) & refs.keys())
        return False

    problems = []
    # Only traverse the type grammar: an ordinary signature's domain expression
    # may contain its own local stored computation, which is a separate owner.
    type_nodes = {name for name in rhs if name.startswith("stored-")}
    type_nodes.update({"type-expression", "type-alternative", "union-type-expression",
                      "declared-type", "product-type", "positional-product-type",
                      "named-product-type", "named-product-component", "dictionary-type",
                      "dictionary-link", "dictionary-value-type", "callable-type",
                      "callable-receiver", "nominal-type", "generic-type-application",
                      "explicit-generic-type-application", "postfix-generic-type-application",
                      "generic-argument", "generic-argument-head", "callable-type-suffix",
                      "generic-argument-list", "generic-union-argument",
                      "type-inference-hole"})
    refs = {name: values & type_nodes for name, values in refs.items()}
    if reachable("type-expression", "type-inference-hole"):
        problems.append("ordinary type expressions must not admit inference holes")
    if not reachable("stored-type-expression", "type-inference-hole"):
        problems.append("stored annotations must retain inference holes")
    for name in ("stored-positional-product-type", "stored-generic-argument",
                 "stored-dictionary-value-type", "stored-nominal-type"):
        if not reachable(name, "type-inference-hole"):
            problems.append(f"{name} must preserve recursive annotation holes")
    pure = rhs.get("pure-preamble-statement", "")
    if any(name in pure for name in ("local-stored-declaration", "local-pattern-declaration",
                                     "behaviour-preamble-statement")):
        problems.append("expression preambles cannot acquire stored/value-body locals")
    if "pure-pattern-declaration" not in pure:
        problems.append("expression preambles must retain pure derived patterns")
    if "value-body" in rhs.get("pure-pattern-declaration", ""):
        problems.append("pure patterns require expression RHSs")
    behaviour = rhs.get("behaviour-preamble-statement", "")
    if "immutable-local-stored-declaration" not in behaviour or re.search(r'"mut"', behaviour):
        problems.append("behaviour preambles require immutable stored locals")
    if "local-stored-declaration" in behaviour.replace("immutable-local-stored-declaration", ""):
        problems.append("behaviour preambles cannot admit mutable stored locals")
    for owner in ("action-signature-body", "reactive-rule-declaration", "message-signature-body"):
        if "behaviour-preamble-statement" not in rhs.get(owner, ""):
            problems.append(f"{owner} must preserve the shared behaviour preamble")
    if not rhs.get("iteration-binding", "").strip() == "binding-pattern":
        problems.append("iteration binding must use the general pattern")
    if "iteration-binding" not in rhs.get("quantifier-expression", ""):
        problems.append("quantifiers must retain general patterns")
    if "positional-binding-pattern" not in rhs.get("local-pattern-declaration", ""):
        problems.append("local pattern declarations require positional roots")
    if "binding-pattern" in rhs.get("local-pattern-declaration", "").replace("positional-binding-pattern", ""):
        problems.append("local pattern declarations cannot acquire standalone name/discard roots")
    required = ("TypeInferenceHole", "NameBinding(", "DiscardBinding", "PositionalBinding(",
                "IterationBinding(binding_pattern pattern)", "behaviour_preamble_statement* leading_preamble",
                "BehaviourStoredLocal(local_stored_decl value)", "PurePatternDecl(binding_pattern binding, expression_block value)")
    normalized = re.sub(r"\s+", " ", ast_text)
    for item in required:
        if item not in normalized:
            problems.append(f"local surface contract is missing: {item}")
    if "DictionaryIterationBinding" in ast_text or "ValueIterationBinding" in ast_text:
        problems.append("iteration AST must not restrict general binding patterns")
    return problems


def generic_contract_problems(grammar_text: str, ast_text: str, lexicon_text: str) -> list[str]:
    """Guard source distinctions; do not perform inference or generic resolution."""
    code = strip_comments(grammar_text)
    ast = re.sub(r"--.*", "", ast_text)
    problems = []
    from specification.grammar.ebnf_analysis import left_corner_graph, left_recursion_path
    graph = left_corner_graph(grammar_text)
    for name in ("generic-type-application", "postfix-generic-type-application",
                 "generic-argument", "stored-generic-type-application",
                 "stored-postfix-generic-type-application", "stored-generic-argument"):
        path = left_recursion_path(graph, name)
        if path:
            problems.append("generic left recursion: " + " -> ".join(path))
    group = re.search(r'(?m)^generic-parameter-group\s*::=\s*(.*?)\s*;', code, re.S)
    if not group or not group[1].strip().startswith("HEADER_WITH ,"):
        problems.append("generic parameter groups must consume the contextual HEADER_WITH boundary")
    from specification.grammar.validate_grammar import productions
    boundary_users = {name for name, body in productions(code) if re.search(r'\bHEADER_WITH\b', body)}
    if boundary_users != {"generic-parameter-group"}:
        problems.append("only generic-parameter-group may consume HEADER_WITH")
    for name in ("ThingDecl", "AliasDecl", "FamilyDecl", "BooleanRuleDecl",
                 "ActionDecl", "LookDecl", "SublookDecl"):
        constructor = re.search(rf"\b{name}\(([^()]*)\)", ast, re.S)
        if not constructor or "generic_parameter* parameters" not in constructor[1]:
            problems.append(f"{name} must retain generic parameter declarations")
    for name in ("ReactiveRuleDecl", "AlwaysRuleDecl", "MessageDecl", "SubmessageDecl", "TestDecl"):
        constructor = re.search(rf"\b{name}\(([^()]*)\)", ast, re.S)
        if constructor and "generic_parameter" in constructor[1]:
            problems.append(f"{name} cannot declare generic parameters")
    equality = re.search(r"\bStructuralTypeEqualityExpr\(([^()]*)\)", ast, re.S)
    if not equality or re.sub(r"\s+", " ", equality[1]).strip() != "type_expr left, type_expr right, flag negated":
        problems.append("structural equality must retain complete Type operands and negation")
    if "IntervalType(" in ast or "generic_application_form form" not in ast:
        problems.append("type applications must retain source grouping and use one generic Interval constructor")
    lexical = strip_comments(lexicon_text)
    triples = re.search(r'(?m)^three-character-token\s*::=\s*(.*?);', lexical, re.S)
    if not triples or any(f'"{token}"' not in triples[1] for token in ("===", "!==")):
        problems.append("structural comparison tokens must be indivisible three-character tokens")
    for production in ("generic-parameter-group", "generic-type-application", "generic-family-member", "structural-type-comparison"):
        if not re.search(rf"(?m)^{production}\s*::=", code):
            problems.append(f"missing generic/type grammar distinction: {production}")
    return problems


def foreign_contract_problems(grammar_text: str, ast_text: str) -> list[str]:
    """Guard delegation and body cardinality; does not parse native source."""
    grammar_code = strip_comments(grammar_text)
    ast_code = re.sub(r"--.*", "", ast_text)
    problems: list[str] = []
    body = re.search(r'(?m)^foreign-body\s*::=\s*(.*?)\s*;', grammar_code, re.S)
    expected = 'foreign-item | "{" , declaration-layout , foreign-item , { required-separation , foreign-item } , [ required-separation ] , "}"'
    if not body or re.sub(r"\s+", " ", body.group(1)).strip() != expected:
        problems.append("foreign-body must have one short item and a non-empty braced sequence")
    rhs = re.search(r'(?m)^foreign-code-expression\s*::=\s*(.*?)\s*;', grammar_code, re.S)
    if not rhs or rhs.group(1).strip() != "FOREIGN_EXPRESSION":
        problems.append("foreign export RHS must remain delegated FOREIGN_EXPRESSION")
    for constructor, fields in {
        "ForeignBlock": "nominal_name language, foreign_item first, foreign_item* remaining",
        "ForeignValueExport": "variable_name name, type_expr? annotation, foreign_code value",
        "ForeignCode": "string text",
    }.items():
        found = re.findall(rf"\b{constructor}\s*\(([^()]*)\)", ast_code, re.S)
        if len(found) != 1 or re.sub(r"\s+", " ", found[0]).strip() != fields:
            problems.append(f"{constructor} must preserve source-only foreign structure: {fields}")
    for fragment in ["PureForeignBlock(foreign_block value)", "ForeignBlockValueStatement(foreign_block value)", "ForeignBlockEffect(foreign_block value)"]:
        if fragment not in ast_code:
            problems.append(f"compatible foreign owner is missing: {fragment}")
    if "local_value_decl*" in ast_code:
        problems.append("pure preambles must preserve foreign items as well as calculated locals")
    return problems


def static_schema_contract_problems(grammar_text: str, ast_text: str) -> list[str]:
    """Preserve collection effects without admitting runtime field declarations."""
    code = strip_comments(grammar_text)
    ast_code = re.sub(r"--.*", "", ast_text)
    problems: list[str] = []
    for name, expected in {
        "add-effect": '"add" , expression , "to" , assignable-expression',
        "remove-effect": '"remove" , expression , "from" , assignable-expression',
    }.items():
        found = re.search(rf"(?m)^{name}\s*::=\s*(.*?)\s*;", code, re.S)
        if not found or re.sub(r"\s+", " ", found.group(1)).strip() != expected:
            problems.append(f"{name} must contain only its collection-value form")
    if re.search(r"\bAddFieldEffect\b", ast_code):
        problems.append("runtime field declarations must not have a Surface AST effect")
    for constructor in ["AddValueEffect", "RemoveEffect"]:
        found = re.findall(rf"\b{constructor}\s*\(([^()]*)\)", ast_code, re.S)
        if len(found) != 1 or re.sub(r"\s+", " ", found[0]).strip() != "expr value, assignable_expr target":
            problems.append(f"{constructor} must retain the collection value and target")
    return problems


def catalogue_contract_problems(grammar_text: str, entries: dict) -> list[str]:
    """Compare complete RHSs, including quoted semicolon terminals."""
    code = strip_comments(grammar_text)
    found = list(re.finditer(r"(?m)^([a-z][a-z0-9-]*)\s*::=", code))
    problems = []
    for index, match in enumerate(found):
        end = found[index + 1].start() if index + 1 < len(found) else len(code)
        rhs = code[match.end():end].strip().removesuffix(";").strip()
        recorded = entries.get(match.group(1), {}).get("rhs", "")
        normal = lambda value: re.sub(r"\s+", " ", value).strip()
        if normal(rhs) != normal(recorded):
            problems.append(f"{match.group(1)} RHS differs from its CST catalogue")
    return problems


def recovery_contract_problems(grammar_text: str, ast_text: str) -> list[str]:
    """Guard semantic boundaries rather than runtime execution results."""
    code = strip_comments(grammar_text)
    ast = re.sub(r"--.*", "", ast_text)
    problems = []
    for constructor in ("ExpressionBlock", "ValueBlock", "EffectBlock"):
        found = re.search(rf"\b{constructor}\(([^()]*)\)", ast, re.S)
        if not found or "recovery_handler* handlers" not in found.group(1):
            problems.append(f"{constructor} must retain block handlers")
    for fragment in ("AliasDecl(flag is_abstract", "ImagineQuery", "RecoverThen(recovery_body body)", "RecoverRaise(value_block errors)"):
        if fragment not in ast:
            problems.append(f"missing block/type boundary: {fragment}")
    if re.search(r"\bAllowedQuery\b", ast):
        problems.append("the speculative AST operator must be ImagineQuery")
    field = re.search(r"stored_field_data\s*=\s*\(([^()]*)\)", ast, re.S)
    if not field or "value_block default_value" not in field.group(1) or "value_block? default_value" in field.group(1):
        problems.append("new stored fields require an explicit value")
    for name in ("thing-body", "metadata-body", "alias-definition", "structural-alias-body", "family-declaration", "family-member-body", "magnitude-body", "derived-unit-body", "point-magnitude-body", "unit-body", "local-statement-block"):
        found = re.search(rf"(?m)^{name}\s*::=\s*(.*?)\s*;", code, re.S)
        if found and "otherwise-clause" in found.group(1):
            problems.append(f"{name} is not an independent block handler owner")
    branch = re.search(r"(?m)^recovery-branch\s*::=\s*(.*?)\s*;", code, re.S)
    if not branch or re.sub(r"\s+", " ", branch.group(1)).strip() != '"then" , recovery-body | "raise" , value-body':
        problems.append("recovery must choose exactly then or raise")
    return problems


def part_contract_problems(grammar_text: str, ast_text: str) -> list[str]:
    """Protect the file/category boundary without claiming a Mud parser."""
    code = strip_comments(grammar_text)
    ast = re.sub(r"--.*", "", ast_text)
    problems = []
    found = list(re.finditer(r"(?m)^([a-z][a-z0-9-]*)\s*::=", code))
    rhs = {}
    for i, match in enumerate(found):
        end = found[i + 1].start() if i + 1 < len(found) else len(code)
        rhs[match[1]] = re.sub(r"\s+", " ", code[match.end():end].strip().removesuffix(";").strip())
    expected = {
        "mud-input": "mud-file | part-file",
        "uses-declaration": '\"uses\" , mud-path',
        "part-only-directive": '\"part\" , \"only\"',
        "part-file": "layout , [ uses-declaration , { required-separation , uses-declaration } , [ required-separation ] ] , EOF",
        "sublook-declaration": '\"sublook\" , look-signature-body',
        "submessage-declaration": '\"submessage\" , message-signature-body',
    }
    for name, value in expected.items():
        if rhs.get(name) != value:
            problems.append(f"{name} must preserve the minimal part/category boundary")
    if "[ part-only-directive , required-separation ]" not in rhs.get("mud-file", ""):
        problems.append("source root must retain the optional part-only header")
    for fragment in ("flag part_only", "part_file* parts", "MudPartFile(", "UsesDecl(", "SublookDecl(", "SubmessageDecl("):
        if fragment not in ast:
            problems.append(f"part AST contract is missing: {fragment}")
    return problems


def validate(root: Path) -> list[Problem]:
    problems: list[Problem] = []
    grammar = root / "specification/grammar/mud.ebnf"
    lexical = root / "specification/grammar/mud-lexico.ebnf"
    kinds_path = root / "specification/syntax/mud-syntax-kinds.yaml"
    coverage_path = root / "specification/syntax/syntax-coverage.yaml"
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

    # The lexical grammar contains special ?...?... prose clauses;
    # automatic reference checking applies to mud.ebnf.
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
    for path, entries in ((grammar, kind_syntax), (lexical, kind_lexical)):
        problems.extend(Problem(str(kinds_path), message) for message in
                        catalogue_contract_problems(path.read_text(encoding="utf-8"), entries))
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
        problems.extend(Problem(str(nominal_hir_path), message)
                        for message in nominal_hir_contract_problems(hir_text))

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

    # Global AST properties.
    ast_text = asdl_path.read_text(encoding="utf-8")
    problems.extend(Problem(str(asdl_path), message) for message in
                    local_contract_problems(grammar.read_text(encoding="utf-8"), ast_text))
    problems.extend(Problem(str(asdl_path), message) for message in
                    generic_contract_problems(grammar.read_text(encoding="utf-8"), ast_text,
                                              (root / "specification/grammar/mud-lexico.ebnf").read_text(encoding="utf-8")))
    problems.extend(Problem(str(asdl_path), message) for message in
                    part_contract_problems(grammar.read_text(encoding="utf-8"), asdl_path.read_text(encoding="utf-8")))
    problems.extend(Problem(str(asdl_path), message) for message in
                    foreign_contract_problems(grammar.read_text(encoding="utf-8"), ast_text))
    problems.extend(Problem(str(asdl_path), message) for message in
                    static_schema_contract_problems(grammar.read_text(encoding="utf-8"), ast_text))
    add_kind = kind_syntax.get("add-effect", {})
    if (set(add_kind.get("references", [])) != {"expression", "assignable-expression"}
            or re.sub(r"\s+", " ", add_kind.get("rhs", "")).strip()
            != '"add" , expression , "to" , assignable-expression'):
        problems.append(Problem(str(kinds_path), "add-effect catalogue must contain only collection insertion"))
    if covered.get("add-effect", {}).get("ast", {}).get("target") != "AddValueEffect":
        problems.append(Problem(str(coverage_path), "add-effect must map directly to AddValueEffect"))
    required = ["module MUDSurface", "project = MudProject", "source_file = MudFile", "flag = Disabled | Enabled"]
    for snippet in required:
        if snippet not in ast_text:
            problems.append(Problem(str(asdl_path), f"required contract is missing: {snippet}"))

    # Normative regressions not detected by name synchronisation alone.
    forbidden_fragments = {
        root / "specification/syntax/mud-surface-ast.asdl": [
            "AnchorInterpolation(",
            "intrinsic_name_override",
        ],
        root / "specification/07-lexicon.md": [
            "after `anchor{` and `{`",
        ],
        root / "specification/04-mathematical-model.md": [
            "intrinsic `name: Text`",
            "A single global `start with` declaration determines a finite set",
        ],
        root / "specification/08-concrete-grammar.md": [
            "intrinsic and immutable `name: Text` property",
            "`unique` is statically forbidden in dictionaries",
            "Parentheses are mandatory when nesting a dictionary as a value",
            "`anchor{d}` inserts the canonical anchor",
        ],
        root / "specification/09-abstract-syntax.md": [
            "optional override of intrinsic `name`",
            "`prefixes = empty` → `NoPrefixes`",
        ],
        root / "specification/syntax/cst-to-surface-ast.md": [
            "`intrinsic_name_override`",
            "produces a synthetic collection:",
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
        "runtime-add-field-rejected",
        "runtime-add-mut-field-rejected",
        "runtime-remove-field-rejected",
        "collection-add-preserved",
        "collection-remove-preserved",
        "dictionary-association-add-preserved",
        "static-inherited-schema-rematerialisation",
        "foreign-schema-write-rejected",
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
        "unique-by-path",
        "duplicate-unique-axis",
        "local-unique-by-path",
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

    problems.extend(Problem(str(asdl_path), message) for message in
                    recovery_contract_problems(grammar.read_text(encoding="utf-8"), asdl_path.read_text(encoding="utf-8")))
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
