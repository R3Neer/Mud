---
id: D-047
title: "Quantifiers and finite iteration"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-018"
  - "Q-028"
  - "Q-029"
affects:
  - "expressions, intervals and iteration"
---
# ADR-047 — Quantifiers and finite iteration

- Amended by: [[ADR-101-bloques-de-valor-variables-locales-almacenadas-and-extremos-por-testigos|D-101]].

- Amended by: [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]]
- Expanded by: [[ADR-075-enumerable-domains-all-and-derived-value-form|D-075]]
- Expanded by: [[ADR-081-collection-filtering-take-and-indexing|D-081]]
- Amended by: [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]]
- Amended by: [[ADR-095-empty-extrema-as-ordinary-absence|D-095]]

- Related questions: Q-018, Q-028, Q-029
- Documents affected: expressions, ranges, iteration

## Context

MUD needs to iterate through domain sets without introducing general loops whose termination or result depends on the inner container.

## Decision

Expressions allow:

```mud
exists x in source : predicate
forall x in source : predicate
count x in source : predicate
min x in source : predicate
max x in source : predicate
```

The domain must be finite and countable. Evaluation is pure. The five bodies are Boolean predicates. `min` and `max` return the first or last accepted witness according to the source's semantic order; they require a source with a usable order. These are partial queries: if no witness is accepted, they produce `empty` with cardinality `[0..1]`; otherwise they produce a value of the source member type. The result is a problem only when a later receiving context does not support cardinality zero, in accordance with D-095.

D-081 Add a pure selection that returns the flags rather than consuming them:

```mud
item in source : predicate
```

It shares responsibility for finiteness and enumerability, produces the accepted subcollection, and can subsequently feed into a quantifier, `take` or another expression.

The `for each` The executable appears inside a `then`; D-101 also allows for `LocalForEach` inside `ValueBlock`, with `LocalStatementBlock` and has no external effects. The executable form retains:

```mud
for each item in source if predicate :
    iterations += 1

for each value in source by step if predicate :
    iterations += 1
```

The clause `by` 'optional' always precedes `if`. A dictionary can link a pair by means of `(key, value)`.

Membership of `source` is taken as snapshot at the start of the loop. The filter is pure, deterministic and cannot depend on computed randomness. In a source with semantic order, each filter is evaluated immediately before its iteration and observes the previous sequential effects within the delta private. In a source with no semantic order, all filters read the same snapshot The initial value and the deltas from the accepted iterations are combined as simultaneous effects; a conflict reverses the resolution complete.

The canonical enumeration is derived from the type: declared order of a closed family, lexicographic order for a structural alias, dictionary or collection order, or ascending order for a canonically realised interval. The traversal order of an explicit progression is independent: a negative `by` value moves from the upper limit towards the lower limit in accordance with D-088 without altering the canonical order of the type or domain.

When an enumeration is obtained by progression, the finite intervals of `Nat` e `Int` use default step one and `Money`, step `0.01`. Sources that already have their own numbering do not need to create a step. A general range of `Num` requires an explicit, exact step size. The intervals of `Rum` can never be enumerated. The last one value it is the latest point generated and falling within the interval; the endpoints are not included by default.

A discontinuous interval is normalised into disjoint segments and traversed segment by segment, with the step being reset in each segment. An empty interval results in zero iterations.

## Consequences

- There is no implicit iteration over infinite or uncountable domains.
- The established syntax for discontinuous intervals continues in Q-018; the explicit downward path is expressed by `by` negative in accordance with D-088.
- Tests for finiteness and termination may be conservative.

## Verification

1. Quantifiers over finite sources, including filtered extremes over ordered sources.
2. Gaps for `min` and `max` cause `empty`; any subsequent incompatibility follows the standard cardinality rules.
3. A noticeable difference between an ordered and an unordered loop.
4. Open, closed, discontinuous and stepped intervals.
5. Rejection of a list `Rum` or infinite.
6. Syntactic order `by` before `if` and linking dictionary pairs.

## Amendment by D-088

D-088 generalises `by` compatible signed differences, evaluated once, and distinguishes between ordered filters (which see previous sequential effects) and unordered filters (which read the snapshot (initial). The five quantifiers support `by` when the source defines progression and Boolean expression blocks. `Rum` remains uncountable, and the cyclic domains of point are covered over a maximum of one fundamental period.

