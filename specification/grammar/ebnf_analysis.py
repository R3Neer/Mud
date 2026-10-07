"""Analyse EBNF structure for grammar regressions; not a Mud source parser."""
from __future__ import annotations

import re

from specification.grammar.validate_grammar import COMMENT, productions

TOKEN = re.compile(r'"(?:[^"\\]|\\.)*"|\?.*?\?|[A-Za-z][A-Za-z0-9_-]*|[\[\]{}(),|]', re.S)


def parse_rhs(source: str):
    tokens = TOKEN.findall(source)
    if re.sub(r'\s+', '', TOKEN.sub('', source)):
        raise ValueError(f"Unsupported EBNF notation: {source}")
    cursor = 0

    def alternative(end=None):
        nonlocal cursor
        branches, sequence = [], []
        while cursor < len(tokens) and tokens[cursor] != end:
            token = tokens[cursor]
            cursor += 1
            if token == ',':
                continue
            if token == '|':
                branches.append(('seq', tuple(sequence)))
                sequence = []
            elif token in ('(', '[', '{'):
                child = alternative({'(': ')', '[': ']', '{': '}'}[token])
                sequence.append(child if token == '(' else ('opt' if token == '[' else 'rep', child))
            elif token.startswith(('"', '?')) or token.isupper():
                sequence.append(('terminal', token))
            elif token in (')', ']', '}'):
                raise ValueError(f"Unexpected delimiter: {token}")
            else:
                sequence.append(('ref', token))
        if end is not None:
            if cursor >= len(tokens):
                raise ValueError(f"Missing delimiter: {end}")
            cursor += 1
        branches.append(('seq', tuple(sequence)))
        return ('alt', tuple(branches))

    return alternative()


def grammar_trees(source: str):
    return {name: parse_rhs(rhs) for name, rhs in productions(COMMENT.sub('', source))}


def nullable(node, names: set[str]) -> bool:
    kind, value = node
    if kind == 'ref':
        return value in names
    if kind == 'terminal':
        return value == '""'
    if kind in ('opt', 'rep'):
        return True
    return (any if kind == 'alt' else all)(nullable(child, names) for child in value)


def first_references(node, empty: set[str]) -> set[str]:
    kind, value = node
    if kind == 'ref':
        return {value}
    if kind == 'terminal':
        return set()
    if kind in ('opt', 'rep'):
        return first_references(value, empty)
    result = set()
    for child in value:
        result.update(first_references(child, empty))
        if kind == 'seq' and not nullable(child, empty):
            break
    return result


def left_corner_graph(source: str) -> dict[str, set[str]]:
    trees = grammar_trees(source)
    empty: set[str] = set()
    while True:
        expanded = empty | {name for name, tree in trees.items() if nullable(tree, empty)}
        if expanded == empty:
            break
        empty = expanded
    return {name: first_references(tree, empty) & trees.keys() for name, tree in trees.items()}


def left_recursion_path(graph: dict[str, set[str]], start: str) -> list[str]:
    pending = [(child, [start, child]) for child in sorted(graph.get(start, set()))]
    visited = set()
    while pending:
        name, path = pending.pop()
        if name == start:
            return path
        if name in visited:
            continue
        visited.add(name)
        pending.extend((child, path + [child]) for child in sorted(graph.get(name, set())))
    return []


def lower_to_bnf(trees):
    """Lower repetitions/options to epsilon productions for bounded test witnesses."""
    result = {}
    counter = 0

    def symbol(node):
        nonlocal counter
        if node[0] in ('ref', 'terminal'):
            return node[1]
        counter += 1
        name = f'@ebnf{counter}'
        define(name, node)
        return name

    def define(name, node):
        kind, value = node
        if kind == 'alt':
            result[name] = [tuple(symbol(child) for child in branch[1]) for branch in value]
        elif kind == 'seq':
            result[name] = [tuple(symbol(child) for child in value)]
        elif kind in ('opt', 'rep'):
            child = symbol(value)
            result[name] = [(), (child,) if kind == 'opt' else (child, name)]
        else:
            result[name] = [(symbol(node),)]

    for name, tree in trees.items():
        define(name, tree)
    return result


def recognises(bnf, start: str, tokens: list[str]) -> bool:
    """Earley recognition of token fixtures, including nullable/recursive rules."""
    grammar = {**bnf, '@start': [(start,)]}
    chart = [set() for _ in range(len(tokens) + 1)]
    chart[0].add(('@start', (start,), 0, 0))
    for position, states in enumerate(chart):
        changed = True
        while changed:
            before = len(states)
            for name, rhs, dot, origin in list(states):
                if dot == len(rhs):
                    for parent, body, mark, begin in list(chart[origin]):
                        if mark < len(body) and body[mark] == name:
                            states.add((parent, body, mark + 1, begin))
                else:
                    next_symbol = rhs[dot]
                    if next_symbol in grammar:
                        states.update((next_symbol, body, 0, position) for body in grammar[next_symbol])
                    elif position < len(tokens) and next_symbol == tokens[position]:
                        chart[position + 1].add((name, rhs, dot + 1, origin))
                    elif next_symbol == '""':
                        states.add((name, rhs, dot + 1, origin))
            changed = len(states) != before
    return ('@start', (start,), 1, 0) in chart[-1]
