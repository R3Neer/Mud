"""Supplied interval/owner certificates, not Mud inference or execution.

Inputs already contain the independently justified body/initializer bounds.
This checker neither discovers branches nor proves coverage of Mud source.
Explicit bounds here certify admission; derived truncation is separately scoped.
"""


def checked_interval(value):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError("A cardinality certificate has two bounds")
    lower, upper = value
    if type(lower) is not int or lower < 0 or not (
        upper is None or type(upper) is int and upper >= lower
    ):
        raise ValueError("Invalid cardinality certificate")
    return lower, upper


def effective_cardinality(owner, inferred=None, written=None):
    if owner not in ("immutable-stored", "derived", "mutable-stored", "type-only"):
        raise ValueError("Unknown declaration owner")
    evidence = None if inferred is None else checked_interval(inferred)
    if written is not None:
        return checked_interval(written), "Explicit"
    if owner in ("mutable-stored", "type-only"):
        return (1, 1), "OrdinaryScalarDefault"
    if evidence is None:
        raise ValueError("Omitted definition cardinality needs inference evidence")
    origin = "InferredFromInitializer" if owner == "immutable-stored" else "InferredFromExpression"
    return evidence, origin


def admits(actual, required):
    lo, hi = checked_interval(actual)
    lower, upper = checked_interval(required)
    return lo >= lower and (upper is None or hi is not None and hi <= upper)


def certificate_admitted(witness):
    card, _ = effective_cardinality(witness["owner"], witness.get("inferred"), witness.get("written"))
    return admits(witness["actual"], card)
