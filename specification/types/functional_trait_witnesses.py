"""Supplied finite constraint/schema/origin certificates, not Mud inference.

Rows already contain valid complete operator contracts. Field records already
contain checked accessible contracts. This module does not scan source, discover
members/overloads, prove arbitrary domains or execute Mud/causal work.
"""
import json


def aggregate_contribution_certificate(contributions):
    """Exterior occurrence population of supplied, already selected results.

    This checks a finite shape certificate; it neither selects Mud branches nor
    evaluates their bodies, orders an unordered source or executes a policy.
    """
    return tuple(member for contribution in contributions for member in contribution)


def specialize_rows(rows, prefix):
    # Each prefix is a set of admissible static types for one evaluated input.
    # Contextual literal sets are retained; typed variables provide singletons.
    return tuple(row for row in rows if len(prefix)<=len(row['inputs']) and
                 all(actual in admitted for actual,admitted in zip(row['inputs'],prefix)))


def implicit_binders(occurrences, bound):
    captured, parameters = [], []
    for role,name in occurrences:
        if role!='variable' or name=='value': continue
        target=captured if name in bound else parameters
        if name not in target: target.append(name)
    return tuple(parameters),tuple(captured)


def application_choice(product, curried):
    choices=[name for name,valid in [('product',product),('curried',curried)] if valid]
    if len(choices)!=1: raise ValueError('ambiguous' if choices else 'incompatible')
    return choices[0]


def fields_satisfy(requirements,candidate,visible,includes):
    for name,required in requirements.items():
        if name not in visible or name not in candidate:return False
        actual=candidate[name]
        target=dict(required['type']); source=dict(actual['type'])
        if target.get('order')=='sequence':
            if source.get('order') is None:return False
            target.pop('order'); source.pop('order',None)
        if required.get('write',False):
            if actual.get('kind')!='stored' or not actual.get('write',False):return False
            if not includes(source,target) or not includes(target,source):return False
        elif not includes(source,target):return False
    return True


def normalized_requirements(requirements):
    # The supplied objects are minimum requirement contracts, not candidate
    # implementation records; member kind is absent from a read requirement.
    return json.dumps(requirements,sort_keys=True,separators=(',',':'))


def coherent_operators(declarations):
    grouped={}
    for row in declarations:
        key=(row['symbol'],json.dumps(row['operands'],sort_keys=True))
        grouped.setdefault(key,[]).append(row)
    chosen=[]
    for group in grouped.values():
        explicit={row['origin']:row for row in group if row['explicit']}
        if len(explicit)>1:raise ValueError('distinct explicit global signature')
        implicit={row['origin']:row for row in group if not row['explicit']}
        if len({row['semantic_key'] for row in implicit.values()})>1:
            raise ValueError('incompatible implicit origins')
        if explicit:chosen.append(next(iter(explicit.values())))
        elif implicit:chosen.append(next(iter(implicit.values())))
    return tuple(chosen)
