"""Finite supplied pattern/shape certificates; no Mud source or body execution.

Tags are preclassified by the fixture. Schema/nominal/equality/order facts are
supplied premises, not inferred types. Label equality is deliberately bounded.
"""
from dataclasses import dataclass


class ContractError(ValueError):
    pass


class FieldFault(RuntimeError):
    pass


@dataclass(frozen=True)
class Sequence:
    items: tuple
    ordered: bool = False
    order_proved: bool = False
    inner_mut: bool = False


@dataclass(frozen=True)
class Record:
    nominal_types: frozenset
    fields: tuple
    visible: frozenset


def admitted(*, needs_order=False, order_proved=False,
             needs_equality=False, equality_proved=True):
    if needs_order and not order_proved:
        raise ContractError('Static order proof required')
    if needs_equality and not equality_proved:
        raise ContractError('Static equality support required')


def same(left, right):
    # Python bool/int equality must not collapse Mud leaf categories.
    return type(left) is type(right) and left == right


def match_certificate(pattern, value, *, outer_names=(), equality_proved=True,
                      equality_test=same):
    env = {}

    def visit(node, item):
        tag, *args = node
        if tag == 'discard':
            return True
        if tag == 'capture':
            name = args[0]
            if name in outer_names:
                raise ContractError('Capture shadows an outer binding')
            if name in env:
                admitted(needs_equality=True, equality_proved=equality_proved)
                return equality_test(env[name], item)
            env[name] = item
            return True
        if tag == 'literal':
            admitted(needs_equality=True, equality_proved=equality_proved)
            return equality_test(args[0], item)
        if tag == 'test':
            # Supplied Boolean certificate, not a Mud predicate evaluation.
            return args[0]
        if tag == 'tuple':
            return (type(item) is tuple and len(item) == len(args[0])
                    and all(visit(p, v) for p, v in zip(args[0], item)))
        if tag == 'collection':
            if not isinstance(item, Sequence):
                return False
            admitted(needs_order=len(args[0]) > 1, order_proved=item.order_proved)
            return len(item.items) == len(args[0]) and all(
                visit(p, v) for p, v in zip(args[0], item.items))
        if tag == 'cons':
            if not isinstance(item, Sequence):
                return False
            admitted(needs_order=True, order_proved=item.order_proved)
            if not item.items:
                return False
            tail = Sequence(item.items[1:], item.ordered, item.order_proved, item.inner_mut)
            return visit(args[0], item.items[0]) and visit(args[1], tail)
        if tag == 'fields':
            nominal, fields = args
            if not isinstance(item, Record) or nominal not in item.nominal_types:
                return False
            labels = [name for name, _ in fields]
            if len(set(labels)) != len(labels):
                raise ContractError('Duplicate field label')
            if not set(labels) <= item.visible:
                raise ContractError('Field not visible')
            supplied = dict(item.fields)
            for name, subpattern in fields:
                field = supplied[name]
                if isinstance(field, FieldFault):
                    raise field
                if not visit(subpattern, field):
                    return False
            return True
        raise ContractError('Unknown certificate tag')

    return dict(env) if visit(pattern, value) else None


def selector_literal_or_predicate(*, literal, input_value, predicate_result=None):
    """literal is None for a supplied computed Bool predicate."""
    if literal is not None and type(literal) is not bool:
        raise ContractError('Literal certificate must be Boolean')
    if literal is None and type(predicate_result) is not bool:
        raise ContractError('Predicate certificate must supply a Boolean result')
    return predicate_result if literal is None else same(input_value, literal)


def available_result_names(successful_paths):
    if not successful_paths:
        return frozenset()
    common = frozenset.intersection(*(frozenset(path) for path in successful_paths))
    # Supplied binding identities must agree, not merely their written names.
    return frozenset(name for name in common
                     if all(path[name] == successful_paths[0][name]
                            for path in successful_paths))
