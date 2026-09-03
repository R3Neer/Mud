---
id: D-082
title: "`cycle` as a point-domain modifier"
status: current
date: 2026-08-04
supersedes: []
superseded-by: []
questions:
  - "Q-018"
affects:
  - "point magnitudes, intervals, grammar, CST and AST"
---

# ADR-082 — `cycle` as a point-domain modifier

- Modifies: [[ADR-029-intervals-effective-limits-and-cycles-of-point|D-029]], [[ADR-059-magnitude-intervals-and-inverted-endpoints|D-059]] and [[ADR-062-canonical-point-magnitude-literals|D-062]].
- Related question: [[notes/questions/Q-018-i-discontinuous-intervals|Q-018]].
- Modified by: [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]]

## Context

The form `[a..b cycle)` placed `cycle` inside the delimiters of an interval even though it does not determine endpoint inclusion. This mixed the domain's mathematical notation with a property exclusive to point magnitudes and suggested that `cycle` was part of the general interval expression.

Collection cardinalities do not share this problem: their `[cardinality modifiers]` form is a specialised specification whose bounds are always closed and natural.

## Decision

`cycle` becomes a trailing modifier of the complete domain of a point magnitude:

```mud
magnitude TimeOfDay point over Time in [0..86_400) cycle {
}
```

The former `[a..b cycle)` form is no longer valid.

The modifier remains exclusive to `point over`. The interval preceding `cycle` must be finite, contiguous, non-empty, closed on the left and open on the right. Its period is the difference between the upper and lower bounds and must be strictly positive.

`cycle` modifies point-domain normalisation, not the interval value. Therefore `[a..b)` retains the same ordinary-interval AST, and the subsequent presence of `cycle` selects `CyclicPointDomain` during domain transformation.

Cardinality syntax is unchanged:

```mud
players: Player [1..3 unique mut]
```

Open or nested intervals are not admitted as cardinalities.

## Consequences

- The delimiters `[` `(` `]` `)` once again describe only interval endpoint membership.
- The source visibly distinguishes the `[a..b)` domain from its `cycle` behaviour.
- The grammar can diagnose a cyclic domain with an unsuitable interval form separately.
- The semantic AST `OrdinaryPointDomain` / `CyclicPointDomain` is unchanged.

## Verification

1. Acceptance of `in [a..b) cycle` in a point magnitude.
2. Rejection of the retired `in [a..b cycle)` form.
3. Rejection of `cycle` in non-point magnitudes.
4. Rejection of `cycle` after closed, left-open, infinite, empty or degenerate intervals.
5. Preservation of the cardinality forms `[1]`, `[1..3]` and `[1..3 mut]`.
6. A progression over a cyclic point domain visits at most one fundamental period and never wraps indefinitely.

## Amendment by D-088

A cyclic point domain can feed an exact progression through a compatible difference. Enumeration covers a single fundamental period and never repeats the cycle indefinitely. The sign and bounds apply to the fundamental interval `[a..b)`.
