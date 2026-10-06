"""Bounded effect witnesses and Surface AST coverage; not a MUD runtime."""
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
CORPUS = Path(__file__).with_name("effect-cases.json")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tooling.cli_support import (
    HelpCatalogue, HelpItem, MudArgumentParser, add_presentation_arguments,
    failure, parse_cli,
)

def evaluate(w):
    kind = w["kind"]
    if kind == "numeric":
        branches = w["branches"]
        if type(w["base"]) is not int:
            raise ValueError("Numeric witness base must be an exact integer")
        for branch in branches:
            for op, value in branch:
                if op not in {"=", "+", "-", "*", "/"} or type(value) is not int:
                    raise ValueError("Numeric witness requires supported operations and exact integer operands")
        replacements = []
        tails = []
        reads = []
        for branch in branches:
            raw = Fraction(w["base"])
            observed = []
            tail = []
            for op, v in branch:
                v = Fraction(v)
                if op == "=":
                    raw = v
                    tail = []
                elif op == "+": raw += v
                elif op == "-": raw -= v
                elif op == "*": raw *= v
                elif op == "/":
                    if not v: return "arithmetic-error"
                    raw /= v
                else: raise ValueError("Unknown numeric operation")
                if op == "=": replacement = v
                else: tail.append((op, v))
                observed.append(max(0, raw) if w.get("nat") else raw)
            if any(op == "=" for op, _ in branch): replacements.append(replacement)
            tails.append(tail)
            reads.append(observed)
        if "private_reads" in w and reads != w["private_reads"]:
            raise ValueError("Private observation witness disagrees")
        if replacements and len(set(replacements)) != 1: return "conflict"
        raw = replacements[0] if replacements else Fraction(w["base"])
        for k in range(max(map(len, tails), default=0)):
            delta, prod, divisor = Fraction(0), Fraction(1), Fraction(1)
            for tail in tails:
                if k >= len(tail): continue
                op, v = tail[k]
                if op == "+": delta += v
                elif op == "-": delta -= v
                elif op == "*": prod *= v
                elif op == "/": divisor *= v
            if not divisor: return "arithmetic-error"
            raw = (raw + delta) * prod / divisor
        return max(0, raw) if w.get("nat") else raw
    if kind == "lifecycle":
        state = dict(w["initial"])
        for op in w["operations"]:
            if op == "create":
                if not state["active"]:
                    state.update(active=True, generation=state["generation"]+1, payload=w["initialiser"])
            elif op == "destroy":
                if state["active"]: state.update(active=False, payload=None)
            else: raise ValueError("Unknown lifecycle operation")
        return state
    if kind == "dictionary":
        initial = w["initial"]
        proposed, deletes = {}, set()
        for index, p in enumerate(w["proposals"]):
            if p[0] == "delete": deletes.add(p[1])
            elif p[0] == "set":
                if p[1] in proposed and proposed[p[1]][0] != p[2]:
                    if not any(q[0] == "delete" and q[1] == p[1] for q in w["proposals"]): return "conflict"
                else: proposed[p[1]] = (p[2], index)
            else: raise ValueError("Unknown association proposal")
        proposed = {k:v for k,v in proposed.items() if k not in deletes}
        active = set(proposed)
        while True:
            candidate = {k:v for k,v in initial.items() if k not in deletes}
            candidate.update({k:proposed[k][0] for k in active})
            if not w.get("unique"): return candidate
            groups = defaultdict(list)
            for k,v in candidate.items(): groups[v].append(k)
            rejected = set()
            for keys in groups.values():
                if len(keys)<2: continue
                unchanged = [k for k in keys if k not in active]
                if len(unchanged)>1: raise ValueError("Invalid unique initial dictionary")
                winner = unchanged[0] if unchanged else min(keys,key=lambda k:proposed[k][1])
                rejected.update(k for k in keys if k != winner)
            if not rejected: return candidate
            if not rejected <= active: raise ValueError("Invalid uniqueness fallback")
            active -= rejected
    raise ValueError("Unknown finite witness kind")

def validate(data):
    ast=(ROOT/"specification/syntax/mud-surface-ast.asdl").read_text(encoding="utf-8")
    effect=ast.split("    effect = ",1)[1].split("    assignment_operator =",1)[0]
    constructors=set(re.findall(r"(?:^|[|=])\s*([A-Z][A-Za-z]+)\(","="+effect,re.M))
    operators=set(re.findall(r"[A-Z][A-Za-z]+",ast.split("    assignment_operator =",1)[1].split("    iteration_binding",1)[0]))
    if constructors != set(data["constructors"]): raise ValueError("Effect constructor coverage differs")
    if operators != set(data["operators"]): raise ValueError("Assignment operator coverage differs")
    cases={c["id"]:c for c in data["cases"]}
    if len(cases)!=len(data["cases"]): raise ValueError("Duplicate case IDs")
    for section, case in list(data["constructors"].values()) + list(data["operators"].values()):
        if case not in cases: raise ValueError("Missing constructor case")
        chapter=(ROOT/"specification/25-effects.md").read_text(encoding="utf-8")
        if not re.search(r"^## "+re.escape(section)+r"\.",chapter,re.M): raise ValueError("Missing chapter section")
    for c in cases.values():
        if not c.get("contract"): raise ValueError("Missing case contract")
        if "witness" in c:
            actual=evaluate(c["witness"])
            if actual!=c["witness"]["expected"]: raise ValueError(f"{c['id']}: expected outcome differs: {actual}")
        elif not c.get("entry") or not c.get("expected_trace"): raise ValueError("Incomplete declarative trace")
    return len(cases),sum("witness" in c for c in cases.values())

def main(argv=None):
    invocation = "python specification/effects/validate_effect_spec.py"
    catalogue = HelpCatalogue(
        product="MUD EFFECT CONTRACTS", version="",
        description="Check effect coverage and bounded witnesses; do not execute MUD source.",
        invocation=invocation, groups=(), commands=(),
        usage=(f"{invocation} [--colour MODE] [--ascii]",),
        global_items=(HelpItem("--colour auto|always|never", "Control colour for human output."),
                      HelpItem("--ascii", "Use ASCII status symbols.")),
        notes=("Running without arguments validates the current repository.",), show_help_on_empty=False,
    )
    parser = MudArgumentParser(prog=invocation, error_code="Mud.Effects.InvalidArguments")
    add_presentation_arguments(parser)
    parsed = parse_cli(parser, catalogue, argv)
    if parsed.exit_code is not None:
        return parsed.exit_code
    try:
        n, w = validate(json.loads(CORPUS.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        failure(parsed.ui, "Effect witness validation failed.", code="Mud.Effects.Invalid", details=str(exc))
        return 1
    parsed.ui.success(f"Effects: {n} cases, {w} bounded witnesses; AST/operator coverage matches.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
