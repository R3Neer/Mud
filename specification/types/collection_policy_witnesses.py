"""Finite supplied policy/comprehension certificates, not source execution.

Callables are Python witness predicates supplied by the test, not inferred Mud
expressions. Coverage concerns only the explicit finite input certificate.
"""


def covers(inputs, selectors, fallback=False):
    return fallback or all(any(test(item) for test in selectors) for item in inputs)


def apply_first(item, branches, fallback=None):
    for predicate, result in branches:
        if predicate(item):
            return result(item)
    return [] if fallback is None else fallback(item)


def apply_all(item, branches, fallback=None):
    matching = [result for predicate, result in branches if predicate(item)]
    if matching:
        return [result(item) for result in matching]
    return [] if fallback is None else [fallback(item)]


def comprehension(source, body, predicate=lambda item: True):
    captured = tuple(source)
    return [body(item) for item in captured if predicate(item)]


def interval_member(item, lower, upper, lower_closed, upper_closed):
    return (item >= lower if lower_closed else item > lower) and (
        item <= upper if upper_closed else item < upper)


def coverage_admitted(inputs, selectors, minimum, fallback=False):
    """Supplied finite application-minimum certificate, not source coverage solving."""
    return minimum == 0 or covers(inputs, selectors, fallback)
