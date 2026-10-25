"""Finite supplied shape/pair certificates, not a Mud evaluator or typechecker.

Result labels, order facts, faults and authority are supplied premises. These
helpers check the consequences without executing arithmetic or Mud source.
"""
from dataclasses import dataclass
from itertools import product


def selected_pairs(left_count, right_count, left_ordered, right_ordered):
    """Occurrence indices are zero-based certificate labels, not Mud indices."""
    if any(type(n) is not int or n < 0 for n in (left_count, right_count)):
        raise ValueError('Counts must be nonnegative integers')
    if any(type(flag) is not bool for flag in (left_ordered, right_ordered)):
        raise ValueError('Order facts must be Boolean')
    if left_ordered and right_ordered:
        return tuple((i, i) for i in range(min(left_count, right_count)))
    # This technical enumeration is not a semantic sequence guarantee.
    return tuple(product(range(left_count), range(right_count)))


def cardinality_bounds(left, right, *, both_ordered):
    """both_ordered: True proved positional; False proved Cartesian; None unknown."""
    for lower, upper in (left, right):
        if (type(lower) is not int or lower < 0
                or upper is not None and (type(upper) is not int or upper < lower)):
            raise ValueError('Invalid interval')
    if both_ordered is not None and type(both_ordered) is not bool:
        raise ValueError('Invalid order proof')
    la, ua = left
    lb, ub = right
    positional = (min(la, lb),
                  ub if ua is None else ua if ub is None else min(ua, ub))
    high_product = (0 if ua == 0 or ub == 0 else
                    None if ua is None or ub is None else ua * ub)
    cartesian = (la * lb, high_product)
    if both_ordered is True:
        return positional
    if both_ordered is False:
        return cartesian
    upper = (None if positional[1] is None or cartesian[1] is None
             else max(positional[1], cartesian[1]))
    return min(positional[0], cartesian[0]), upper


@dataclass(frozen=True)
class Layer:
    members: tuple
    ordered: bool = False


def pair_shape(left, right):
    """Supplied leaves are opaque labels; only explicit Layer nodes recurse."""
    if not isinstance(left, Layer) and not isinstance(right, Layer):
        return left, right
    a = left if isinstance(left, Layer) else Layer((left,))
    b = right if isinstance(right, Layer) else Layer((right,))
    pairs = selected_pairs(len(a.members), len(b.members), a.ordered, b.ordered)
    return Layer(tuple(pair_shape(a.members[i], b.members[j]) for i, j in pairs),
                 a.ordered and b.ordered)


def result_certificate(pairs, labels, *, equality=True, keys=None,
                       key_valid=False, fault_pairs=(), operand_fault=False):
    """Check finite supplied results. No source body/operator is executed."""
    if operand_fault:
        raise ValueError('Operand production failed')
    if any(pair in fault_pairs for pair in pairs):
        raise ValueError('Selected member fault')
    values = tuple(labels[pair] for pair in pairs)
    unique = equality and len(set(values)) == len(values)
    if keys is not None and key_valid:
        by_value = {}
        for pair, value in zip(pairs, values):
            key = keys[pair]
            if value in by_value and by_value[value] != key:
                raise ValueError('Equal values cannot have distinct projected keys')
            by_value[value] = key
    keyed = (equality and key_valid and keys is not None
             and len({keys[pair] for pair in pairs}) == len(pairs))
    return values, unique, keyed


@dataclass(frozen=True)
class View:
    value: Layer
    order_guaranteed: bool
    inner_mut: bool


def readonly_view(source, *, require_order=False, require_mut=False):
    if require_order and not source.order_guaranteed:
        raise ValueError('Order guarantee missing')
    if require_mut and not source.inner_mut:
        raise ValueError('Write authority missing')
    return View(source.value, require_order, require_mut)
