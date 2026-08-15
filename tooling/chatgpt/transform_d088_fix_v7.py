from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()


def read(rel):
    return (root / rel).read_text(encoding="utf-8")


def write(rel, text):
    (root / rel).write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def exact(text, old, new, label, count=1):
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{label}: expected {count}, found {actual}")
    return text.replace(old, new, count)


def case_block(text, case_id):
    marker = f"- id: {case_id}\n"
    if text.count(marker) != 1:
        raise SystemExit(f"case {case_id}: marker expected once, found {text.count(marker)}")
    start = text.index(marker)
    end = text.find("\n- id: ", start + len(marker))
    if end < 0:
        end = len(text)
    return start, end, text[start:end]


def replace_in_case(text, case_id, old, new):
    start, end, block = case_block(text, case_id)
    actual = block.count(old)
    if actual != 1:
        raise SystemExit(f"case {case_id}: expected source fragment once, found {actual}")
    block = block.replace(old, new, 1)
    return text[:start] + block + text[end:]


# -----------------------------------------------------------------------------
# ADR D-088: every fenced mud example should be actual MUD, and examples that
# omit `by` should use a source with its own enumeration rather than relying on
# an unspecified numeric-literal default.
# -----------------------------------------------------------------------------
rel = "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md"
t = read(rel)
t = exact(
    t,
    '''```mud
action Accumulate for mut total: Int {
    then for each i in [1..10]:
        total += i
}
```''',
    '''```mud
action Accumulate for values: Int [* ordered], mut total: Int {
    then for each value in values:
        total += value
}
```''',
    "D088 source-owned enumeration example",
)
t = exact(
    t,
    '''```mud
action AccumulateDoubled for mut total: Int {
    then for each i in [1..10]: {
        doubled := i * 2
        total += doubled
    }
}
```''',
    '''```mud
action AccumulateDoubled for values: Int [* ordered], mut total: Int {
    then for each value in values: {
        doubled := value * 2
        total += doubled
    }
}
```''',
    "D088 block source-owned enumeration example",
)
t = exact(
    t,
    '''```mud
action Forward for mut total: Int {
    then for each i in [1..8] by 2:
        total += i
}
# recorrido: 1, 3, 5, 7

action Backward for mut total: Int {
    then for each i in [1..8] by -3:
        total += i
}
# recorrido: 8, 5, 2
```''',
    '''```mud
action Forward for mut total: Num {
    then for each value in [1..8] by 2:
        total += value
}
# recorrido: 1, 3, 5, 7

action Backward for mut total: Num {
    then for each value in [1..8] by -3:
        total += value
}
# recorrido: 8, 5, 2
```''',
    "D088 signed examples isolate progression",
)
write(rel, t)


# -----------------------------------------------------------------------------
# Older ADR examples touched by D-088: remove pseudocode and avoid accidental
# secondary errors in snippets intended to document another rule.
# -----------------------------------------------------------------------------
rel = "notas/decisiones/ADR-033-claves-y-enumeracion-de-aliases.md"
t = read(rel)
t = exact(
    t,
    '''```mud
for each coordinate in Coordinate: {
    ...
}

exists destination in Coordinate:
    ...
```''',
    '''```mud
action VisitCoordinates for mut visits: Nat {
    then for each coordinate in Coordinate:
        visits += 1
}

rule HasLeftEdge {
    exists destination in Coordinate:
        destination.horizontal == 0
}
```''',
    "D033 real enumeration examples",
)
write(rel, t)

rel = "notas/decisiones/ADR-034-number-exacto-y-rumber-binary64.md"
t = read(rel)
t = exact(
    t,
    '''```mud
for each value in [r0..r1] by r0.1: {}
```''',
    '''```mud
action InvalidRumIteration for mut total: Rum {
    then for each value in [r0..r1] by r0.1:
        total += value
}
```''',
    "D034 isolate Rum non-enumerability",
)
write(rel, t)

rel = "notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md"
t = read(rel)
t = exact(
    t,
    '''```mud
for each item in source if predicate: {
    ...
}

for each value in source by step if predicate: {
    ...
}
```''',
    '''```mud
for each item in source if predicate:
    iterations += 1

for each value in source by step if predicate:
    iterations += 1
```''',
    "D047 remove ellipsis pseudocode",
)
write(rel, t)


# -----------------------------------------------------------------------------
# Conformance cases: make each case isolate its intended rule. Numeric intervals
# with explicit `by` may remain Num; accumulators are Num where necessary.
# Cases that test omitted `by` use named collections unless omission itself is
# the error under test.
# -----------------------------------------------------------------------------
rel = "especificacion/sintaxis/casos/cst-ast.yaml"
t = read(rel)

t = replace_in_case(
    t,
    "for-each-requires-colon",
    'source: "action Iterate for mut total: Nat {\\n    then for each i in [1..5] {\\n        total += i\\n    }\\n}\\n"',
    'source: "action Iterate for items: Nat [*], mut total: Nat {\\n    then for each i in items {\\n        total += i\\n    }\\n}\\n"',
)
t = replace_in_case(
    t,
    "for-each-negative-step",
    'source: "action Iterate for mut total: Int {\\n    then for each i in [1..8] by -3:\\n        total += i\\n}\\n"',
    'source: "action Iterate for mut total: Num {\\n    then for each i in [1..8] by -3:\\n        total += i\\n}\\n"',
)
t = replace_in_case(
    t,
    "for-each-static-zero-step",
    'source: "action Broken for mut total: Int {\\n    then for each i in [1..8] by 0:\\n        total += i\\n}\\n"',
    'source: "action Broken for mut total: Num {\\n    then for each i in [1..8] by 0:\\n        total += i\\n}\\n"',
)
t = replace_in_case(
    t,
    "d088-for-each-body-after-terminator",
    'source: "action Accumulate for mut total: Int {\\n    then for each i in [1..3]:\\n        total += i\\n}\\n"',
    'source: "action Accumulate for values: Int [*], mut total: Int {\\n    then for each i in values:\\n        total += i\\n}\\n"',
)
t = replace_in_case(
    t,
    "d088-selection-body-after-terminator",
    'source: "thing Sample {\\n    selected := x in [1..3]:\\n        x > 1\\n}\\n"',
    'source: "thing Sample {\\n    values: Int [*]\\n    selected := x in values:\\n        x > 1\\n}\\n"',
)
t = replace_in_case(
    t,
    "d088-quantifier-block-after-terminator",
    'source: "rule HasLarge {\\n    exists x in [1..3]:\\n        {\\n            limit := 1\\n            x > limit\\n        }\\n}\\n"',
    'source: "rule HasLarge for values: Int [*] {\\n    exists x in values:\\n        {\\n            limit := 1\\n            x > limit\\n        }\\n}\\n"',
)
t = replace_in_case(
    t,
    "d088-runtime-zero-step-action",
    'source: "action Accumulate for mut total: Int given step: Int {\\n    then for each i in [1..8] by step:\\n        total += i\\n}\\n"',
    'source: "action Accumulate for mut total: Num given step: Int {\\n    then for each i in [1..8] by step:\\n        total += i\\n}\\n"',
)
t = replace_in_case(
    t,
    "d088-infinite-interval-not-enumerable",
    'source: "action Infinite for mut total: Int {\\n    then for each value in [0..*]:\\n        total += value\\n}\\n"',
    'source: "action Infinite for mut total: Num {\\n    then for each value in [0..*] by 1:\\n        total += value\\n}\\n"',
)
t = replace_in_case(
    t,
    "d088-filter-must-be-bool",
    'source: "action Broken for mut total: Int {\\n    then for each value in [1..4] if value + 1:\\n        total += value\\n}\\n"',
    'source: "action Broken for mut total: Num {\\n    then for each value in [1..4] by 1 if value + 1:\\n        total += value\\n}\\n"',
)
t = replace_in_case(
    t,
    "d088-random-filter-rejected",
    'source: "action Broken for mut total: Int {\\n    then for each value in [1..4] if Rand([true, false]):\\n        total += value\\n}\\n"',
    'source: "action Broken for mut total: Num {\\n    then for each value in [1..4] by 1 if Rand([true, false]):\\n        total += value\\n}\\n"',
)
t = replace_in_case(
    t,
    "d088-step-evaluated-once",
    'source: "thing Counter {\\n    mut step: Int = 2\\n    mut total: Int = 0\\n}\\naction Advance {\\n    then for each value in [1..8] by Counter.step: {\\n        Counter.step = 1\\n        Counter.total += value\\n    }\\n}\\n"',
    'source: "thing Counter {\\n    mut step: Int = 2\\n    mut total: Num = 0\\n}\\naction Advance {\\n    then for each value in [1..8] by Counter.step: {\\n        Counter.step = 1\\n        Counter.total += value\\n    }\\n}\\n"',
)
t = replace_in_case(
    t,
    "d088-open-lower-positive-step",
    'source: "action OpenLower for mut total: Int {\\n    then for each value in (1..8] by 2:\\n        total += value\\n}\\n"',
    'source: "action OpenLower for mut total: Num {\\n    then for each value in (1..8] by 2:\\n        total += value\\n}\\n"',
)
t = replace_in_case(
    t,
    "d088-open-upper-negative-step",
    'source: "action OpenUpper for mut total: Int {\\n    then for each value in [1..8) by -2:\\n        total += value\\n}\\n"',
    'source: "action OpenUpper for mut total: Num {\\n    then for each value in [1..8) by -2:\\n        total += value\\n}\\n"',
)
t = replace_in_case(
    t,
    "d088-empty-inverted-interval-zero-iterations",
    'source: "action EmptyLoop for mut total: Int {\\n    then for each value in [8..1] by -1:\\n        total += value\\n}\\n"',
    'source: "action EmptyLoop for mut total: Num {\\n    then for each value in [8..1] by -1:\\n        total += value\\n}\\n"',
)
write(rel, t)


# -----------------------------------------------------------------------------
# Postconditions: no examples newly maintained by D-088 may still use ellipsis,
# empty effect bodies, or the specific bare-Num/no-step patterns fixed above.
# -----------------------------------------------------------------------------
checks = {
    "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md": [
        "action Accumulate for values: Int [* ordered]",
        "action Forward for mut total: Num",
        "action Backward for mut total: Num",
    ],
    "notas/decisiones/ADR-033-claves-y-enumeracion-de-aliases.md": [
        "action VisitCoordinates for mut visits: Nat",
        "rule HasLeftEdge",
    ],
    "notas/decisiones/ADR-034-number-exacto-y-rumber-binary64.md": [
        "action InvalidRumIteration for mut total: Rum",
    ],
    "notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md": [
        "iterations += 1",
    ],
    "especificacion/sintaxis/casos/cst-ast.yaml": [
        'source: "action Iterate for items: Nat [*], mut total: Nat',
        'source: "action Accumulate for values: Int [*], mut total: Int',
        'source: "thing Sample {\\n    values: Int [*]',
        'source: "rule HasLarge for values: Int [*]',
        'source: "action Infinite for mut total: Num {\\n    then for each value in [0..*] by 1:',
    ],
}
for rel, needles in checks.items():
    text = read(rel)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"missing {needle!r} in {rel}")

for rel in (
    "notas/decisiones/ADR-088-iteracion-progresiones-y-bloques-de-expresion.md",
    "notas/decisiones/ADR-033-claves-y-enumeracion-de-aliases.md",
    "notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita.md",
):
    if "    ..." in read(rel):
        raise SystemExit(f"ellipsis pseudocode remains in D088-maintained example: {rel}")

if "for each value in [r0..r1] by r0.1: {}" in read("notas/decisiones/ADR-034-number-exacto-y-rumber-binary64.md"):
    raise SystemExit("empty Rum rejection body remains")

print("D088_FIX_V7_OK")
