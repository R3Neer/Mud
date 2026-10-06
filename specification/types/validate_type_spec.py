"""Validate static-specification coverage and finite contract witnesses.

This is an editorial derivation checker, not a MUD parser, typechecker or runtime.
Its witness language is confined to finite nominal/cardinality/guarantee facts,
callable variance, constructor productivity and labelled graph bisimulation.
"""
from __future__ import annotations

import math
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tooling.cli_support import (
    HelpCatalogue, HelpItem, MudArgumentParser, add_presentation_arguments,
    failure, parse_cli,
)


def check_witness(witness):
    """Reject malformed certificates rather than reporting semantic rejection."""
    def natural(value):
        return type(value) is int and value >= 0

    def contract(value):
        if not isinstance(value.get("name"), str) or not value["name"]:
            raise ValueError("A contract needs a nonempty type name")
        card = value.get("card", [1, 1])
        if len(card) != 2 or not natural(card[0]) or not (
            card[1] is None or natural(card[1]) and card[0] <= card[1]
        ):
            raise ValueError("Invalid cardinality interval")
        domain = value.get("domain", [None, None])
        if len(domain) != 2 or any(x is not None and type(x) is not int for x in domain):
            raise ValueError("This witness language uses integer domain endpoints")
        if all(x is not None for x in domain) and domain[0] > domain[1]:
            raise ValueError("Inverted domain witness")
        unique = value.get("unique", "none")
        if unique not in ("none", "value") and not (isinstance(unique, str) and unique.startswith("key:") and len(unique) > 4):
            raise ValueError("Unknown uniqueness guarantee")
        if type(value.get("inner_mut", False)) is not bool:
            raise ValueError("Invalid authority flag")

    parents = witness.get("parents", {})
    for name, entries in parents.items():
        if not isinstance(entries, list):
            raise ValueError("Nominal parents must be a list")
        if any(name in ancestors(parent, parents) for parent in entries):
            raise ValueError("Nominal ancestry contains a cycle")
    kind = witness["kind"]
    if kind == "inclusion":
        contract(witness["source"])
        contract(witness["target"])
    elif kind == "callable":
        for signature in (witness["supplied"], witness["requested"]):
            contract(signature["output"])
            for slot in signature["inputs"]:
                if slot["mode"] not in ("read", "write"):
                    raise ValueError("Unknown input permission")
                contract(slot["type"])
    elif kind in ("productivity", "representation"):
        nodes = witness["nodes"]
        for name, node in nodes.items():
            children = node.get("children", [])
            if not isinstance(children, list) or any(child not in nodes for child in children):
                raise ValueError(f"{name}: undefined constructor edge")
            if node["kind"] not in ("leaf", "product", "union", "abstract", "transparent", "container"):
                raise ValueError(f"{name}: unknown constructor")
            if node["kind"] == "leaf" and children:
                raise ValueError(f"{name}: a leaf has constructor children")
            if node["kind"] == "transparent" and len(children) != 1:
                raise ValueError(f"{name}: a transparent edge has exactly one target")
            if node["kind"] == "container":
                if not natural(node["minimum"]) or not natural(node.get("witness_count", 0)):
                    raise ValueError(f"{name}: invalid witness count")
            for flag in ("valid", "empty_valid", "unique"):
                if flag in node and type(node[flag]) is not bool:
                    raise ValueError(f"{name}: invalid {flag} premise")
        roots = [witness["root"]] if kind == "productivity" else [witness["left"], witness["right"]]
        if any(root not in nodes for root in roots):
            raise ValueError("Undefined witness root")
    elif kind == "proof-boundary":
        if witness["context"] not in ("value-admission", "stored-cardinality") or witness["proof"] not in ("proved", "false", "unknown"):
            raise ValueError("Unknown proof obligation or disposition")
    else:
        raise ValueError(f"Unknown witness kind: {kind}")


def ancestors(name, parents):
    seen, pending = {name}, [name]
    while pending:
        current = pending.pop()
        for parent in parents.get(current, []):
            if parent not in seen:
                seen.add(parent)
                pending.append(parent)
    return seen


def bound(value):
    return math.inf if value is None else value


def includes(source, target, parents):
    """Read-only contract inclusion; nominal identity is not representation."""
    if target["name"] != "Any" and target["name"] not in ancestors(source["name"], parents):
        return False
    a, b = source.get("card", [1, 1]), target.get("card", [1, 1])
    if a[0] < b[0] or bound(a[1]) > bound(b[1]):
        return False
    da, db = source.get("domain", [None, None]), target.get("domain", [None, None])
    lower = lambda x: -math.inf if x is None else x
    if lower(da[0]) < lower(db[0]) or bound(da[1]) > bound(db[1]):
        return False
    qa, qb = source.get("unique", "none"), target.get("unique", "none")
    if qb != "none" and not (qa == qb or qb == "value" and qa.startswith("key:")):
        return False
    if target.get("order") and source.get("order") != target["order"]:
        return False
    return not target.get("inner_mut", False) or source.get("inner_mut", False)


def callable_substitution(supplied, requested, parents):
    inputs_s, inputs_t = supplied["inputs"], requested["inputs"]
    if len(inputs_s) != len(inputs_t):
        return False
    for s, t in zip(inputs_s, inputs_t):
        if s["mode"] != t["mode"]:
            return False
        if t["mode"] == "write":
            if not includes(s["type"], t["type"], parents) or not includes(t["type"], s["type"], parents):
                return False
        elif not includes(t["type"], s["type"], parents):
            return False
    return includes(supplied["output"], requested["output"], parents) and (
        not requested.get("root", False) or supplied.get("root", False)
    )


def productive(nodes):
    """Least fixed point; explicit flags witness leaf/domain/uniqueness facts."""
    found = set()
    while True:
        previous = set(found)
        for name, node in nodes.items():
            kind, children = node["kind"], node.get("children", [])
            valid = node.get("valid", True)
            if not valid:
                continue
            if kind == "leaf":
                found.add(name)
            elif kind == "product" and all(child in found for child in children):
                found.add(name)
            elif kind in ("union", "abstract", "transparent") and any(child in found for child in children):
                found.add(name)
            elif kind == "container":
                if node["minimum"] == 0 and node.get("empty_valid", True):
                    found.add(name)
                elif children and all(child in found for child in children):
                    if not node.get("unique", False) or node.get("witness_count", 0) >= node["minimum"]:
                        found.add(name)
        if found == previous:
            return found


def equivalent(nodes, left, right):
    """Greatest fixed point: revisiting a recursive pair is not enough."""
    pairs = {
        (a, b) for a, x in nodes.items() for b, y in nodes.items()
        if x["kind"] == y["kind"] and x.get("label") == y.get("label")
        and len(x.get("children", [])) == len(y.get("children", []))
    }
    while True:
        remaining = {
            (a, b) for a, b in pairs
            if all((x, y) in pairs for x, y in zip(nodes[a].get("children", []), nodes[b].get("children", [])))
        }
        if remaining == pairs:
            return (left, right) in pairs
        pairs = remaining


def witness_result(witness):
    check_witness(witness)
    kind = witness["kind"]
    parents = {"Nat": ["Int"], "Int": ["Num"], **witness.get("parents", {})}
    if kind == "inclusion":
        return "static-accept" if includes(witness["source"], witness["target"], parents) else "static-reject"
    if kind == "callable":
        return "static-accept" if callable_substitution(witness["supplied"], witness["requested"], parents) else "static-reject"
    if kind == "productivity":
        return "static-accept" if witness["root"] in productive(witness["nodes"]) else "static-reject"
    if kind == "representation":
        return "static-accept" if equivalent(witness["nodes"], witness["left"], witness["right"]) else "static-reject"
    if kind == "proof-boundary":
        if witness["proof"] == "proved":
            return "static-accept"
        return "runtime-check" if witness["context"] == "value-admission" and witness["proof"] == "unknown" else "static-reject"
    raise ValueError(f"Unknown witness kind: {kind}")


def expression_constructors(text):
    start = re.search(r"(?m)^    expr = ", text).end()
    end = text.index("        attributes", start)
    return set(re.findall(r"(?:^|\|)\s*([A-Z]\w*)", text[start:end]))


def validate(root=ROOT):
    problems = []
    chapters = ("10-type-system.md", "14-fields-and-mutability.md", "19-expressions.md")
    texts = {name: (root / "specification" / name).read_text(encoding="utf-8") for name in chapters}
    declared = []
    for text in texts.values():
        declared += re.findall(r"(?m)^> \[!rule\] (MUD-(?:TYPE|EFFECT)-\d+)", text)
    if len(declared) != len(set(declared)):
        problems.append("Static chapters contain duplicate rule identifiers.")
    cases = yaml.safe_load((root / "specification/types/typing-cases.yaml").read_text(encoding="utf-8"))["cases"]
    seen, covered = set(), set()
    for case in cases:
        name = case["id"]
        if name in seen:
            problems.append(f"{name}: duplicate case identifier.")
        seen.add(name)
        if not case.get("source", "").strip() or not case.get("contract", "").strip():
            problems.append(f"{name}: source and explicit contract are required.")
        if case["expected"] not in ("static-accept", "static-reject", "runtime-check"):
            problems.append(f"{name}: unknown expected disposition.")
        for rule in case["rules"]:
            covered.add(rule)
            if rule not in declared:
                problems.append(f"{name}: unknown rule {rule}.")
        if "witness" in case:
            try:
                actual = witness_result(case["witness"])
                if actual != case["expected"]:
                    problems.append(f"{name}: witness yields {actual}, expected {case['expected']}.")
            except (KeyError, ValueError, TypeError) as error:
                problems.append(f"{name}: malformed witness: {error}.")
    problems += [f"No conformance instance for {rule}." for rule in sorted(set(declared) - covered)]
    coverage = yaml.safe_load((root / "specification/types/expression-coverage.yaml").read_text(encoding="utf-8"))["expressions"]
    ast = (root / "specification/syntax/mud-surface-ast.asdl").read_text(encoding="utf-8")
    constructors = expression_constructors(ast)
    problems += [f"Missing expression coverage: {x}." for x in sorted(constructors - coverage.keys())]
    problems += [f"Unknown expression constructor: {x}." for x in sorted(coverage.keys() - constructors)]
    headings = set(re.findall(r"(?m)^## (.+)$", texts["19-expressions.md"]))
    for name, entry in coverage.items():
        if entry["section"] not in headings:
            problems.append(f"{name}: expression section does not exist.")
        if not set(entry["cases"]) <= seen:
            problems.append(f"{name}: references missing cases.")
        if not entry.get("cases"):
            problems.append(f"{name}: requires a conformance instance.")
    return problems


def main(argv=None):
    invocation = "python specification/types/validate_type_spec.py"
    catalogue = HelpCatalogue(
        product="MUD STATIC CONTRACTS", version="",
        description="Check static rule coverage and finite derivation witnesses; do not execute MUD source.",
        invocation=invocation, groups=(), commands=(),
        usage=(f"{invocation} [--root PATH] [--colour MODE] [--ascii]",),
        global_items=(HelpItem("--root PATH", "Repository root to inspect."),
                      HelpItem("--colour auto|always|never", "Control colour for human output."),
                      HelpItem("--ascii", "Use ASCII status symbols.")),
        notes=("Running without arguments validates the current repository.",), show_help_on_empty=False,
    )
    parser = MudArgumentParser(prog=invocation, error_code="Mud.Types.InvalidArguments")
    parser.add_argument("--root", type=Path, default=ROOT)
    add_presentation_arguments(parser)
    parsed = parse_cli(parser, catalogue, argv)
    if parsed.exit_code is not None:
        return parsed.exit_code
    try:
        problems = validate(parsed.arguments.root)
    except (OSError, yaml.YAMLError, KeyError, TypeError, AttributeError) as error:
        failure(parsed.ui, "Cannot read the static contract corpus.", code="Mud.Types.InvalidCorpus", details=str(error))
        return 1
    if problems:
        for problem in problems:
            failure(parsed.ui, "Static contract validation failed.", code="Mud.Types.Invalid", details=problem)
        return 1
    parsed.ui.success("Static rules, expression coverage and finite contract witnesses are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
