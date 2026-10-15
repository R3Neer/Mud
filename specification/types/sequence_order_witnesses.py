"""Finite supplied ordering premises; not Mud parsing or a causal runtime.

Inputs explicitly provide static member/key facts and existing occurrence order.
The witness never discovers fields, comparator laws, source scopes or provenance.
"""


def value_key(variants):
    """Resolve supplied (has_field, stable_field, ordered_field, ordered_whole)."""
    choices = []
    for has_field, stable, ordered, whole_ordered in variants:
        if has_field:
            if not stable or not ordered:
                raise ValueError('present value member is not a valid key')
            choices.append('member')
        elif whole_ordered:
            choices.append('whole')
        else:
            raise ValueError('whole element has no total comparator')
    if not choices or len(set(choices)) != 1:
        raise ValueError('one interpretation is required over static alternatives')
    return choices[0]


def establish_order(occurrences, key=None, history=None):
    """Order supplied occurrence IDs by supplied history or stable key facts."""
    history = list(occurrences) if history is None else list(history)
    if len(set(history)) != len(history) or set(history) != set(occurrences):
        raise ValueError('history must cover exactly the surviving occurrence IDs')
    return history if key is None else sorted(history, key=key)


def extremum_witness(values, accepted, maximum=False, key=lambda x: x):
    """Choose from supplied normal predicate outcomes, retaining witness identity."""
    if len(values) != len(accepted):
        raise ValueError('one supplied predicate outcome per occurrence is required')
    candidates = [(key(value), index, value) for index, value in enumerate(values)
                  if accepted[index]]
    if not candidates:
        return []
    chosen = (max if maximum else min)(candidates, key=lambda row: row[:2])
    return [chosen[2]]


def replace_association(entries, key, value):
    """Finite sequential association-order witness, independent of hash traversal."""
    if any(old_key == key for old_key, _ in entries):
        return [(old_key, value if old_key == key else old_value)
                for old_key, old_value in entries]
    return [*entries, (key, value)]
