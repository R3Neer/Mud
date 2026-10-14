"""Finite supplied policy/comprehension certificates, not source execution.

Callables are Python witness predicates supplied by the test, not inferred Mud
expressions. Coverage concerns only the explicit finite input certificate.
"""


def covers(inputs, selectors, fallback=False):
    return fallback or all(any(test(item) for test in selectors) for item in inputs)


def apply_first(item, branches, fallback):
    for predicate, result in branches:
        if predicate(item):
            return result(item)
    return fallback(item)


def apply_all(item, branches, fallback):
    matching = [result for predicate, result in branches if predicate(item)]
    if matching:
        return [result(item) for result in matching]
    return [fallback(item)]


def comprehension(source, body, predicate=lambda item: True):
    captured = tuple(source)
    return [body(item) for item in captured if predicate(item)]


def interval_member(item, lower, upper, lower_closed, upper_closed):
    return (item >= lower if lower_closed else item > lower) and (
        item <= upper if upper_closed else item < upper)
