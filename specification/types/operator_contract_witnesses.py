"""Finite supplied applicability sets; not Mud lookup, inference or execution.

Each operand contract is supplied as a finite set of abstract inhabitants.
The certificate therefore checks inclusion and selection independently of
source parsing, nominal resolution and any general domain proof procedure.
"""
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Signature:
    origin: str
    owner: str
    operands: tuple[frozenset[str], ...]
    result: str


class SelectionError(ValueError):
    pass


def deduplicate_origins(candidates):
    by_origin = {}
    for candidate in candidates:
        previous = by_origin.setdefault(candidate.origin, candidate)
        if previous != candidate:
            raise SelectionError('Conflicting certificates for one origin')
    return tuple(by_origin.values())


def check_local_duplicates(candidates):
    seen = set()
    for candidate in deduplicate_origins(candidates):
        key = (candidate.owner, candidate.operands)
        if key in seen:
            raise SelectionError('Duplicate signature in one owner')
        seen.add(key)


def dominates(left, right):
    return (len(left.operands) == len(right.operands)
            and all(a <= b for a, b in zip(left.operands, right.operands))
            and any(a < b for a, b in zip(left.operands, right.operands)))


def select(candidates, actual):
    applicable = [candidate for candidate in deduplicate_origins(candidates)
                  if len(candidate.operands) == len(actual)
                  and all(value in admitted
                          for value, admitted in zip(actual, candidate.operands))]
    if not applicable:
        return None
    winners = [candidate for candidate in applicable
               if all(other == candidate or dominates(candidate, other)
                      for other in applicable)]
    if len(winners) != 1:
        raise SelectionError('Ambiguous signatures')
    return winners[0]


def select_alternatives(candidates, alternatives):
    results = set()
    for actual in product(*alternatives):
        selected = select(candidates, actual)
        if selected is None:
            raise SelectionError('Missing static alternative')
        results.add(selected.result)
    return frozenset(results)


def resolve_with_fallback(candidates, actual, builtin, lifted):
    selected = select(candidates, actual)
    if selected is not None:
        return selected
    return builtin() if builtin is not None else lifted()
