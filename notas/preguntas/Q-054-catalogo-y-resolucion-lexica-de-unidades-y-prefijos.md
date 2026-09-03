---
id: Q-054
title: Catalogue and lexical resolution of units and prefixes
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-08-16
decisions:
  - D-076
  - D-089
affects:
  - especificacion/06-lexico.md
  - especificacion/gramatica/mud-lexico.ebnf
superseded-by: []
---

# Q-054 — Catalogue and lexical resolution of units and prefixes

## Question

How are unit forms configured by the programme's own declarations recognised without making the initial scanner depend on an already parsed and resolved magnitude, and which lexical collisions are admissible?

## Resolution

D-076 fixes the catalogue, enabled forms, prefixes and adjacency. D-089 separates the base scanner from the contextual classifier: `UNIT_FORM` is created only over source text once the semantic catalogue is resolved. The expected type restricts candidates; without it, global uniqueness is required, candidates of different lengths use the longest complete form, and one span with several candidates remains ambiguous. `MUD-LEX-016` permits spaces in `~name`, `~plural` and `~abbreviation` when used as source forms, requires at least one alphabetic character and excludes every MUD keyword; `MUD-LEX-017` checks collisions within a magnitude after expanding all permitted prefix combinations.

## Closure criterion

- C1: The pipeline explicitly separates initial recognition from contextual resolution of unit forms.
- C2: Every unit source form has a deterministic delimitation and disambiguation rule.
- C3: The specification requires conformance for collisions, expected context and adjacency.

## Closure evidence

- C1: `D-089`, `MUD-LEX-012` and `MUD-LEX-013`.
- C2: `D-089`, `MUD-LEX-015`, `MUD-LEX-016` and `MUD-LEX-017`.
- C3: D-089 verification and `MUD-LEX-015` through `MUD-LEX-017`, together with D-076/06-lexico adjacency.
