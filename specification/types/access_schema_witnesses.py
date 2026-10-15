"""Bounded supplied outcome/schema certificates; no Mud source evaluation.

Tags describe previously supplied outcomes; contracts are supplied normalized
labels. This does not discover types, instantiate schemas or execute effects.
"""


def dependent_demand(tags):
    """Return demanded prefix and supplied terminal qualification."""
    for i, tag in enumerate(tags):
        if tag not in ('normal', 'omit', 'fault'):
            raise ValueError('unknown supplied outcome')
        if tag != 'normal':
            return tag, i + 1
    return 'normal', len(tags)


def emitted_values(outcomes):
    values = []
    for tag, value in outcomes:
        if tag == 'fault':
            raise ValueError('a fault is not omitted')
        if tag == 'normal':
            values.append(value)
        elif tag != 'omit':
            raise ValueError('unknown supplied outcome')
    return values


def tuple_component(contracts, index):
    if index == '*':
        index = len(contracts)
    if type(index) is not int or not 1 <= index <= len(contracts):
        raise ValueError('static in-range tuple position required')
    return contracts[index - 1]


def project_input(source_names, source_contracts, target_names, target_contracts, values):
    if not (len(source_names) == len(values) == len(target_names)
            == len(source_contracts) == len(target_contracts)):
        raise ValueError('all stored components must correspond')
    if source_contracts != target_contracts:
        raise ValueError('complete component contracts must match')
    return tuple(zip(target_names, values))


def initialization_admitted(abstract, required_origins, resolved_origins):
    return abstract or set(required_origins) <= set(resolved_origins)
