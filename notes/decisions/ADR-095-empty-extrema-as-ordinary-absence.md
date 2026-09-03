---
id: D-095
title: "Empty extrema as ordinary absence"
status: current
date: 2026-08-16
supersedes: []
superseded-by: []
questions: []
affects:
  - "min, max, quantifiers, empty, cardinality, failures and conformance"
---
# ADR-095 — Empty extrema as ordinary absence

- Modifies: [[ADR-047-quantifiers-and-finite-iteration|D-047]].
- Extends: [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]].
- Modified by: [[ADR-101-value-blocks-stored-local-variables-and-witness-extrema|D-101]].

## Context

D-047 referred `min` and `max` over an empty source to a supposed special empty-aggregation error that was never defined. MUD already uses `empty` to represent partial queries without turning absence into an immediate failure.

## Decision

`min` and `max` over a finite, enumerable and ordered source with no candidates accepted by its predicate produce `empty` with the source's member type. Their result form permits cardinality `[0..1]`:

```text
min : T [0..1]
max : T [0..1]
```

Over a source with at least one accepted candidate they produce exactly one value of type `T`: `min`, the first accepted witness; `max`, the last, always according to the source's semantic order. The `ExpressionBlock` only filters and does not compute an ordering criterion. The extrema operation does not itself introduce `failed`.

If the receiving context requires cardinality `[1]`, an `empty` result undergoes the ordinary type, domain and cardinality checks and may produce the same normal failure as any other incompatible absence. There is no special category of “empty-extrema aggregation error”.

Static cardinality may be narrowed when the compiler proves that at least one candidate is accepted by the predicate; without that proof it must retain the possibility `[0..1]`.

## Consequences

- `min` and `max` behave as compositional partial queries.
- A `[0..1]` variable can receive an absent extremum directly.
- A `[1]` variable does not force the extrema operation to invent its own error: the incompatibility is resolved in the ordinary context.
- The normative reference to a nonexistent empty-aggregation error disappears.

## Verification

1. `min` and `max` without accepted witnesses, including a non-empty source whose predicate rejects all members, produce `empty`.
2. The conservative result form is `T [0..1]`.
3. A `[0..1]` receiving context accepts absence.
4. A `[1]` receiving context fails under the ordinary cardinality rule, not through a special aggregator diagnostic.
5. A proof that at least one witness is accepted may narrow the result to `[1]`.
