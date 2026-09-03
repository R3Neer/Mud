---
id: D-029
title: "Intervals, effective limits and cycles of point"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-018"
  - "Q-055"
affects:
  - "futuro `15-colecciones.md`, futuro `17-dominios-e-intervalos.md`, futuro `18-magnitudes.md`"
---
# ADR-029 — Intervals, effective limits and cycles of point

- Amended by: [[notes/decisions/ADR-059-magnitude-intervals-and-inverted-endpoints|D-059]], [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]], [[notes/decisions/ADR-062-canonical-point-magnitude-literals|D-062]] y [[ADR-082-cycle-as-point-domain-modifier|D-082]]
- Related questions: Q-018, [[notes/questions/Q-055-l-point-magnitude-literals|Q-055]]
- Documents affected: future `15-colecciones.md`, future `17-dominios-e-intervalos.md`, future `18-magnitudes.md`

## Context

MUD uses intervals for numerical domains, magnitudes and cardinalities. The original reference did not uniformly define the lateral meaning of `*` nor was it part of the cycle of a magnitude from point in his domain.

## Decisión

### Interval forms

The four defined shapes are:

```mud
[n..m]
(n..m)
[n..m)
(n..m]
```

`n..m` is equivalent to `[n..m]` y `[n]` is equivalent to `[n..n]`.

D-059 adds local and shared units to ordinary interval expressions and specifies that a linear interval with inverted effective limits is normalised to `empty`. This inversion does not indicate a descending order, nor cycle.

The shape `[n]` it also coincides, on the surface, with a collection unitary. Neither of the two uses is eliminated, nor is priority given to either: the type expected, and the restrictions on expression must produce a single elaboration. If a shunt without type If it supports both, you must declare the type explicitly in accordance with D-037.

### Effective limits

`*` represents the effective boundary of the side on which it appears. The two sides do not necessarily denote the same value:

```mud
Nat [*..10]  # [0..10]
Nat [1..*]   # [1..+∞]
[*..*]           # dominio efectivo completo
```

`[*]` is sugar from `[*..*]`. In a cardinality ordinary, `Thing[*]` starts at zero and goes up to the maximum permitted limit.

Every line written with `*` must be closed:

```mud
[*..10]
[1..*]
[*..*]
[*]
```

They are invalid `(*..10]`, `[1..*)`, `(*..*)` and any other form that leaves one end open, written as `*`.

### Domains from magnitude

One magnitude can declare their domain in the header:

```mud
magnitude PlayerCount: Nat in 1..8 {
    ...
}

magnitude Speed in [0..*] :=
    Length / Time
```

In a magnitude non-derivative; the optional numerical representation always precedes the domain:

```text
magnitude nombre [: representación-numérica] [in intervalo] bloque
```

Boundaries are written as bare numbers. In a magnitude non-derivative are interpreted in their unit root; in a derivative, in the canonical combination inferred from the units root components.

Therefore, if the unit canonical of `Speed` is `m/s`, `[0..100]` means 'of' `0 m/s` a `100 m/s`. Neither explicit units nor alternative units are permitted within these limits. Values entered subsequently using another unit are normalised before checking the domain.

### Magnitudes of point

One magnitude from point is declared with `point over` at the top. Its domain is optional:

```mud
magnitude RawInstant point over Time {}

magnitude Timestamp point over Time {
    ~format = "{day}:{hour:2}:{minute:2}"
}

magnitude WorkdayTime point over Time in [0..28_800] {
    ~format = "{hour:2}:{minute:2}"
}

magnitude TimeOfDay point over Time in [0..86_400) cycle {
    ~format = "{hour:2}:{minute:2}:{second:2}"
}
```

It represents positions on a magnitude linear and uses its units. You cannot declare units or `root unit`.
Without `in`, admits the domain the full range of the underlying coordinate. With a linear interval, it is bounded without wrapping. With `[a..b) cycle`, it is limited and cyclically normalised.

You can file your tax return via the metadata `~format` optional: a special textual representation. If omitted, it is rendered like any magnitude ordinary: coordinate at the unit root followed by the abbreviation or name of that unit. In accordance with D-061, `~format` use a template `Text`: `hour`, `minute` y `second` are contextual expressions of the point, y `:2` move two positions to the left. D-061 It also specifies the explicit extraction `minute from hour in time`; D-062 demands that `~format` if it is invertible, it uses it as a form literal canonical and rejects it before normalising any literal outside the domain.

His maths is as follows:

| Operation | Result |
| --- | --- |
| $P-P$ | $M$ |
| $P+M$ | $P$ |
| $M+P$ | $P$ |
| $P-M$ | $P$ |
| $P+P$ | error |

Just one magnitude `point over` it may be cyclical. In accordance with D-082, `cycle` appears after the full interval, and the only valid cyclic form is:

```mud
[a..b) cycle
```

The domain It must be finite, contiguous, non-empty, closed on the left and open on the right. Its period is $b-a$ and everything value is normalised module that period in relation to $a$.

For `[0..360) cycle`:

```text
360  → 0
370  → 10
-10  → 350
```

`cycle` modifies the normalisation of the domain from point. It does not alter the semantics nor the iteration of the general intervals. Its period must be strictly positive: normalisation to `empty` from D-059 does not repair a domain inverted or degenerate cyclic.
Nor does it resolve or modify the cycles of dependency between computed domains addressed by Q-017.

## Consequences

- The interval AST will treat each limit as a specific or actual value and will retain the opening on each side.
- Domain verification for magnitude will be carried out after standardising the units.
- One magnitude from point it does not need to be cyclical or be declared domain.
- Where it exists, the cycle is part of the domain of a magnitude from point, it is not a property independent of the block.

## Future verification

1. Contextual expansion of `[*]` for types, magnitudes and cardinalities.
2. Rejection of all open-ended questions written in `*`.
3. Canonical interpretation of bare boundaries.
4. Rejection of explicit units in the header `in` of a magnitude.
5. Cyclic normalisation with a non-zero lower bound.
6. Rejection of cycles in non-point-wise quantities and non-semi-open domains.
7. Resolution contextual of `[n]` as a unit interval and rejection when it is also viable as collection without type waited long enough.
8. Normalisation of inverted linear intervals to `empty` without top-down interpretation.
9. Rejection of a zero or negative cycle period.
10. Magnitudes of point without domain, with domain linear and with domain cyclical.
11. `~format` optional and standard quantitative representation, with unit, when it is omitted.

