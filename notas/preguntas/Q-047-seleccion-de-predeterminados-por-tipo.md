---
id: Q-047
title: Selection of defaults by type
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-017
  - D-026
  - D-031
  - D-068
  - D-069
  - D-074
affects: []
superseded-by: []
---

# Q-047 — Selection of defaults by type

## Content

Premise status: **decided** by [[notas/decisiones/ADR-017-valor-predeterminado-de-todo-tipo|ADR-017]].

Every well-formed type has a default value belonging to its domain. Basic types already have concrete selections; in particular, `Char` uses `"\u{0}"` (`U+0000`) in a `Char` context. D-031 establishes that a structural alias composes its default using, for each component, its explicit default or that of its effective type. The concrete function remains to be defined for:

- Non-structural aliases and constrained collections.
- Intervals, selection of a default member of a closed family and refinements.
- Types whose domain may depend on the active world.

D-074 decides that a union without one unique nominal default requires an explicit initialiser in the context that must materialise it; textual alternative order does not decide. Integrating this exception with D-017's general formulation and completing the other classes above remain outstanding.

Components of a structural alias may explicitly replace the default obtained from their type. Whether other derived type classes may replace their intrinsic default remains undecided.

Since [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]], it must also be defined how a `thing` collection with a positive minimum obtains a default. The exact anchor is never a candidate; requiring a strict default descendant or an explicit initialiser may be necessary.

The top type `Thing` introduced by D-068 does not itself provide that distinguished member: it is abstract and membership remains strict.
