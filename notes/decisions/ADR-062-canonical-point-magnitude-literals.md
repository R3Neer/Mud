---
id: D-062
title: "Canonical point-magnitude literals"
status: current
date: 2026-07-29
supersedes: []
superseded-by: []
questions:
  - "Q-055"
affects:
  - "lexicon, concrete grammar, point magnitudes, scanner, parser and conformance tests"
---
# ADR-062 — Canonical point-magnitude literals

- Amended by: [[ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]] and [[ADR-089-clasificacion-contextual-de-formas-fuente-sin-dependencia-circular-del-scanner|D-089]]
- Extends: [[notes/decisions/ADR-029-intervals-effective-limits-and-cycles-of-point|D-029]] and [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]]
- Jointly closed by this decision and [[ADR-089-clasificacion-contextual-de-formas-fuente-sin-dependencia-circular-del-scanner|D-089]]: [[notes/questions/Q-055-l-point-magnitude-literals|Q-055]]
- Affected documents: lexicon, concrete grammar, point magnitudes, scanner, parser and conformance tests

## Context

The `~format` metadata already determines how a point magnitude is represented. The grammar reserved `POINT_LITERAL`, but did not establish whether a format was only for output or how to reconstruct a point when it omitted precision, coincided with another type's format, or described a value outside its domain.

## Decision

### Contextual selection

`POINT_LITERAL` is a contextual literal. It is permitted only where the context requires one point-magnitude `point over` type. If the expected type does not exist or is not unique, the program contains a static error.

Selection by type occurs before format interpretation. Two magnitudes may therefore produce the same visible sequence without colliding when the context determines one of them.

### Magnitude with `~format`

When the expected type declares `~format`, the literal must exactly match the canonical representation that the format would produce. It must contain:

- every fixed fragment;
- every component, in declared order;
- the exact separators and characters;
- the canonical numeric form determined by every width and precision specification.

Alternative spellings are not accepted even if they produce the same components. For example, where the canonical format produces `07:05:00`, `7:05:00` is not the same literal.

A point `~format` must be statically invertible: its fragments and holes must make it possible to reconstruct one point. A declaration whose format does not have an unambiguous inverse is invalid. This obligation constrains arbitrary expressions within a point magnitude's `~format`, even when they are renderable in an ordinary `Text` template.

The canonical check is equivalent to:

1. recognise the format's fragments and components;
2. reconstruct the point;
3. render it again with the same format;
4. require exact equality with the source text.

### Omitted precision

Every precision component smaller than the least unit represented by the format has value zero. Thus, a format ending in seconds constructs a point with zero fractions of a second, including milliseconds, microseconds, nanoseconds and picoseconds where those units exist.

Omission neither rounds nor retains implicit information.

### Magnitude without `~format`

When the expected type declares no `~format`, its literal uses ordinary quantity syntax and must write a compatible unit enabled for the underlying magnitude. The quantity is interpreted as the point's complete coordinate relative to its canonical origin.

### Domain

After reconstructing the coordinate, the compiler checks that it belongs to the point magnitude's declared domain. A literal outside the domain is a compilation error.

The check occurs before any cyclic normalisation. A `[0..86_400) cycle` domain whose root unit is the second does not authorise a `26 hour` literal or its formatted equivalent; out-of-range source values do not wrap around.

Cyclic normalisation continues to apply to runtime operations under the point-magnitude rules, but does not repair an invalid literal.

## Consequences

- `~format` is both the canonical representation and, when present, the source form of the point type.
- `POINT_LITERAL` is a D-089 contextual classification over the source span; the base scanner does not require the expected type or the resolved magnitude declaration.
- Point formats have an invertibility constraint that does not affect general `Text` templates.
- Format collisions are resolved by expected type, not global lexical priority.
- Unwritten precision has a defined, reproducible value.
- Cycles do not turn source errors into valid values.

## Examples

```mud
magnitude TimeOfDay point over Time in [0..86_400) cycle {
    ~format = "{hour:2}:{minute:2}:{second:2}"
}

opening: TimeOfDay = 07:05:00
```

The value of `opening` has zero fractional seconds.

```mud
opening: TimeOfDay = 7:05:00   # invalid: not the canonical form
opening: TimeOfDay = 26:00:00  # invalid: outside the domain
```

Without a format:

```mud
magnitude Timestamp point over Time {}

created: Timestamp = 90 second
```

## Verification

1. Acceptance of the exact canonical representation.
2. Rejection of width, separator or component variants.
3. Initialisation to zero of every omitted lower precision.
4. Resolution of coincident formats through distinct expected types.
5. Rejection without an expected type or with an ambiguous type.
6. Static rejection of non-invertible formats.
7. A literal with a unit for a magnitude without `~format`.
8. Rejection of coordinates outside linear and cyclic domains.
