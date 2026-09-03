---
id: D-059
title: "Magnitude intervals and inverted endpoints"
status: current
date: 2026-07-29
supersedes: []
superseded-by: []
questions:
  - "Q-018"
affects:
  - "[[specification/07-gramatica-concreta]], `specification/grammar/mud.ebnf`"
---
# ADR-059 — Magnitude intervals and inverted endpoints

- Amended by: [[ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]]
- Amends: [[notes/decisions/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notes/decisions/ADR-029-intervalos-estrellas-y-ciclos|D-029]], [[notes/decisions/ADR-042-acciones-raiz-y-resultados|D-042]], [[notes/decisions/ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]] and [[notes/decisions/ADR-057-gramatica-concreta-y-continuacion|D-057]]
- Related to: [[notes/decisions/ADR-037-campos-y-dominios-declarativos|D-037]]
- Related questions: Q-018
- Affected documents: [[specification/07-gramatica-concreta]], `specification/grammar/mud.ebnf`

## Context

The endpoints of an interval may be literals or already typed expressions. Requiring a unit on every literal is repetitive when they all share one unit:

```mud
[1 m..5 m]
```

However, removing local units would prevent intervals with different representations and mixed cases:

```mud
[1 m..5 km]
[minimumDistance..5 m]
```

It was also necessary to define the meaning of a linear interval whose state-dependent endpoints become inverted.

## Decision

### Two ways to provide units

A magnitude interval permits local units on its endpoints:

```mud
[1 m..5 m]
[1 m..5 km]
[minimumDistance..5 m]
[1 km..maximumDistance]
[minimumDistance..maximumDistance]
```

Each finite endpoint is an ordinary expression. After name and type resolution, both endpoints must belong to the same magnitude and use compatible numeric representations. Quantities are normalised to that magnitude's canonical unit before they are compared.

When every written finite endpoint is a unitless numeric literal, one unit expression may follow the interval:

```mud
[1..5] m
1..5 m
[1..5) km
[*..5] m
[1] m
[] m
```

The outer unit is distributed over every finite endpoint. The preceding forms are elaborated respectively as quantity intervals, while `[] unit` directly produces the empty interval of the magnitude identified by `unit`.

The undelimited closed form retains the sugar from D-029. In particular:

```mud
1..5 m
```

is grouped as:

```text
(1..5) m
```

not as `1..(5 m)`.

An outer unit does not complete mixed intervals or intervals with expression endpoints:

```mud
[minimumDistance..5] m   # invalid
[minimumDistance..5 m]   # valid
[1 m..5 m] m             # invalid
```

A numeric literal next to a magnitude expression must carry its own unit. Within a delimited form, a unit written before the closing delimiter belongs only to that endpoint:

```mud
[1..5 m]                 # invalid: Num versus Length
[1 m..5 m]               # valid
```

### Preferred form

When all finite endpoints are literals written in the same unit, canonical serialisation uses one outer unit:

```mud
[1..5] m
```

The repeated form `[1 m..5 m]` remains valid. Local units are necessary to preserve different representations such as `[1 m..5 km]` and to combine literals with already typed expressions.

The ordinary lexical separation between number and unit remains: the canonical forms are `1 m` and `5 km`.

### Normalisation of linear intervals

Let $l$ be the effective lower bound and $u$ the effective upper bound of a linear interval, after expressions have been evaluated and units normalised.

- If $l<u$, the interval retains its open or closed endpoints.
- If $l=u$ and both sides are closed, the result is the singleton interval.
- If $l=u$ and either side is open, the result is `empty`.
- If $l>u$, the result is `empty`.

These rules define normalisation by endpoint order. They do not exclude other empty intervals by content; for example, a discrete type may contain no value between two consecutive open endpoints.

Inversion does not denote descending traversal or wraparound. The possible descending enumeration order remains separate in Q-018.

Constructing `empty` this way is a valid, total operation. A calculated field whose endpoints cross denotes the empty interval; crossing is not itself an evaluation error.

### Interaction with actions and constraints

An action does not produce `failed` merely because an interval evaluated during its resolution becomes empty.

The result depends on later use:

- a `given` that does not belong to the empty interval produces `rejected`;
- an `if` that tests membership in it may be false and produce `rejected`;
- an `after` that requires it not to be empty and is false produces `rejected`;
- if the interval forms a domain and leaves a stored value outside that domain, the tentative state is invalid and produces `failed`;
- if it causes an `always` rule to be violated, it produces `failed`.

A genuine error while evaluating an endpoint — for example, an invalid reference — retains the ordinary failure taxonomy and does not become `empty`.

### Cycles

Normalisation to `empty` applies to linear intervals. It introduces no implicit cyclic semantics.

The `[a..b) cycle` form from D-029 and D-082 remains exclusive to the domain of a point magnitude. It must define a strictly positive period and retains bare numeric bounds in its canonical representation; the new local and outer units are not permitted in that header.

## Consequences

- The AST distinguishes intervals with ordinary endpoints from numeric intervals with a shared unit.
- `[] unit` supplies a magnitude type to the empty interval without relying on an outer context.
- Elaborating `1..5 unit` must resolve the unit as common to the complete interval.
- Unit normalisation precedes comparison and normalisation by endpoint order.
- Linear intervals are total values: crossing their endpoints produces `empty`, not an exception.
- State invalidity is determined by its domains and invariants, not by the mere presence of an empty interval.

## Rejected alternatives

### Prohibit local units

This would prevent intervals with different units or a literal alongside a magnitude field from being expressed.

### Apply the outer unit to mixed expressions

Forms such as `[minimumDistance..5] m` would obscure which subexpressions receive a unit context and complicate elaboration. The local literal must be a complete quantity.

### Fail on inverted endpoints

This would make interval construction partial and turn an ordinary set operation into a resolution error. The set defined by inverted linear bounds is empty; constraints that cannot tolerate that emptiness already produce the corresponding operational result.

### Interpret inversion as descent or a cycle

This would conflate interval content, enumeration order and cyclic topology. MUD keeps those three decisions separate.

## Verification

1. A shared unit in closed, open, singleton, unbounded and empty forms.
2. Grouping `1..5 m` with a unit common to the interval.
3. Equal and distinct local units with dimensional normalisation.
4. A magnitude field and a literal with a compulsory local unit.
5. Rejection of `[field..5] m`, `[1..5 m]` and a second outer unit.
6. Rejection of endpoints from different magnitudes or with incompatible representations.
7. Equal closed endpoints produce a singleton; with either side open they produce `empty`.
8. Dynamically inverted endpoints produce `empty` without construction failure.
9. An empty domain that excludes a stored value produces `failed`.
10. An `if`, `given` or `after` made false by emptiness produces `rejected`.
11. No implicit descending or cyclic interpretation.
12. Preservation of the special domain constraints for magnitudes and `[a..b) cycle`.
