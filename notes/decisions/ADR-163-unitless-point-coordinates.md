---
id: D-163
title: Unitless point coordinates
status: current
date: 2026-10-14
supersedes: []
superseded-by: []
questions:
  - Q-078
affects:
  - specification/11-type-system.md
  - specification/21-expressions.md
  - specification/19-magnitudes.md
  - specification/types
---

# ADR-163 — Unitless point coordinates

## Context and acceptance

D-083 admits unitless linear magnitudes, while D-062's unformatted point literal
required a unit inherited from the underlying magnitude. The author accepts
points over a magnitude lacking units and contextual numeric coordinate
construction, rather than forbidding the composition.

## Decision

When a point has no ~format and its underlying magnitude has no admitted unit
presentation, a bare numeric literal can construct its full canonical coordinate
under one unique expected point type. A typed numeric expression uses explicit
to Point. Apply the existing quantitative representation conversion and check
the target domain; a compatible representation does not erase point nominality.
Other nominal magnitudes/points gain no conversion solely from absent unit text.

Source literals are checked against the domain before any cyclic normalization.
Explicit coordinate materialization retains to's conversion/domain check and
does not silently repair an invalid coordinate. Runtime point arithmetic retains
its existing cycle contract. No synthetic unit, unit presentation, unit component
extraction, metadata hole or implicit unrelated point conversion is introduced.
Existing ~format inversion/canonical checks still apply where such a format exists.
Rum prefix requirements remain ordinary numeric requirements without unit context.

## Evidence

MUD-TYPE-041 and chapter 19 distinguish contextual coordinate construction,
typed numeric to, unavailable unit presentation and literal domain failure.
Declaration/type cases provide static evidence. This amends D-029/D-030/D-062/
D-083 and leaves source grammar, AST and nominal HIR unchanged.
