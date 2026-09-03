---
id: D-049
title: "Operators, precedence and standardised intervals"
status: vigente
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-001"
  - "Q-018"
  - "Q-050"
affects:
  - "expresiones, intervalos, gramática"
---
# ADR-049 — Operators, precedence and standardised intervals

- Amended by: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Amended by: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]
- Amended by: [[ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]]
- Amended by: [[ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].

- Amended by: [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Amended further by: [[ADR-074-uniones-nominales-y-estrechamiento|D-074]]
- Related questions: Q-001, Q-018, Q-050
- Documents affected: expressions, ranges, grammar

## Context

The reference contained the list of operators and their precedence, but it predates `to`, to the full nominalisation of aliases and to the current system of units.

## Decisión

### Operators’ families

| Family | Shapes |
| --- | --- |
| Arithmetic | `+`, `-`, `*`, `/`, `%` |
| Comparison | `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `is not`, `in` |
| Logic | `not`, `and`, `or`, `xor`, `=>`, `<=>` |
| Temporary | suffix `changes`; composition featuring `and`, `or` inside `when` |
| Intervals | `|`, `&`, `^`, `-` |
| Collections | `|`, `&`, `^`, `-` |
| Text | `|` for concatenation of `Text` |

Shared tokens are resolved by type and syntactic context; they do not permit type coercion between Booleans, numbers, collections and intervals.

Each operation has a single canonical record. `not`, `and`, `or` y `xor` are purely logical. `|`, `&` y `^` do not apply to `Bool`: they mean, respectively union, intersection and symmetric difference on intervals or sets, except for the concatenation of `Text` as already mentioned. When operating on collections, `^` requires operands `unique`; the symmetric difference of intervals preserves its contract its own. `--` shows the differences between collections and `-` is reserved for quantitative subtraction. `=>` conveys commitment and `<=>`, biconditional.

They are removed from the source code `!`, `implies`, `iff`, `union`, `intersection` y `except`. Reserved words are no longer reserved and may be used as identifiers. The token `!=` remains an independent inequality and does not presuppose the existence of a unitary operator `!`.

Equality is defined by the type of value:

- `thing`: identidad;
- `family`: type nominal and member;
- alias: same type nominal value and content;
- numbers: value within the same representation or following explicit conversion;
- quantities: dimensionally compatible normalised quantities;
- intervals: standardised set;
- collection sorted: sequence;
- collection unordered: multiplicity;
- dictionary: a set of key–value pairs–value.

`is` query the relation reflexive and transitive specialisation between `thing` and, in accordance with D-074, the nominal alternative to a union. `is not` is its canonical compound negation. Neither is equality nor casting.

### Precedencia

From highest to lowest:

1. access `.`, indexing `[]`, call `()` and complete extraction `unit from container in point`;
2. prefixes `old`, `allowed`, `not` and sign;
3. multiplication, division and module;
4. set-theoretic sum, subtraction and difference;
5. suffixes `to Type` e `in unit`;
6. comparisons, `is`, `iis`, `has` y `has not`;
7. temporal suffix `changes`;
8. union and intersection;
9. disjunction, union and concatenation;
10. symmetric difference;
11. involvement;
12. biconditional;
13. `eventually ... through ...`.

In a `when` temporary, just the words `and` y `or` make up activators. The symbols `&` y `|` retain their standard typed operations and are rejected if they receive a trigger; nor do they apply to these `not`, `xor`, `^`, `=>` nor `<=>`. D-058 defines the exponentiation of Boolean operands and the semantics of the composition.

`to` and the `in` from unit apply to the value cumulative total to its left. The parser then continues onto the result converted:

```mud
population / regions to Population
distance + offset in km
value to A to B
```

are grouped as `(population / regions) to Population`, `(distance + offset) in km` y `(value to A) to B`.

Homogeneous chains of `<`, `<=`, `>`, `>=` y `==` are formed as combinations of adjacent pairs. The same applies to `<=>`. `!=`, `is`, `iis`, `has`, `has not` y `=>` They are not linked.

`|` concatenates `Text`. The other conjunctive operators do not apply to `Text`, nor is concatenation implicitly inherited by nominal aliases of `Text`. Regarding compatible collections, `|`, `&` y `--` form the multiset algebra of D-039; `^` symmetric differential form defined exclusively on `unique`. `|` It does not concatenate collections.

### Intervals

Operations relating to union, intersection, symmetric difference and difference yield a normalised form in terms of content: disjoint, ordered segments with no duplicates. Two intervals are equal if their normalised forms denote the same set.

`empty` denotes the empty interval. Basic literals and the rules of `*`, `[n]`, canonical cycles and limits belong to D-029; the list belongs to D-047.

D-059 includes intervals of magnitude with local units or a unit external common. Their endpoints are compared after normalising the units. A linear interval with a lower bound greater than the upper bound, or with equal bounds and one open end, is normalised to `empty`; it never implicitly assumes a descending order, nor semantics cyclical.

## Consequences

- Overload is never determined by an implementation priority.
- Compare different aliases or `Num` with `Rum` requires `to`.
- The complete catalogue of supported types and results by operator remains the responsibility of the type system.

## Verification

1. Parsers that distinguish between each level of precedence.
2. Equality and inequality in each class of value.
3. Equivalent normalisation of intervals.
4. Rejection of overloads without a typed combination.
5. Cumulative conversion and continuation with subsequent operators.
6. Accepted and rejected chains.
7. Concatenation of `Text` and rejection of the other joint operations.
8. Resolution of the four joint operators on compatible sets.
9. Rejection of the withdrawn aliases and of `!` isolated, whilst preserving `!=`.
10. Static separation between `xor` logical and `^` collectivist.
11. Precedence from `changes` below comparisons and above `and` y `or`.
12. Rejection of operators other than words `and` y `or` on temporary triggers.
13. Equivalent normalisation of intervals of magnitude with local and shared drives.
14. Normalisation to `empty` of inverted or degenerate open linear endpoints.

