---
id: Q-055
title: Point-magnitude literals
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-08-16
decisions:
  - D-061
  - D-062
  - D-089
affects:
  - specification/06-lexicon.md
  - specification/07-concrete-grammar.md
  - specification/grammar/mud-lexico.ebnf
superseded-by: []
---

# Q-055 — Point-magnitude literals

## Question

How can `~format` define both canonical representation and a direct source literal form without requiring the initial scanner to know the expected type and resolved magnitude declaration?

## Resolution

D-062 retains the direct source form, canonicality, inversion and domain. D-089 makes the base scanner ignore `~format`; when a position has one expected point type, the contextual classifier reads the original source span and may produce `POINT_LITERAL` in preference to ordinary tokenisation of that span. Without one expected type, this alternative does not exist.

Static inversion includes the ability to determine the end of the complete representation deterministically. No new delimiter is therefore needed, and the base scanner has no circular dependency.

## Closure criterion

- C1: The initial scanner can run without consulting magnitude declarations.
- C2: A source sequence is reproducibly reclassified when the expected type identifies one point magnitude.
- C3: Collisions with an ordinary interpretation have an explicit priority.
- C4: Lexical artefacts distinguish base scanning and contextual classification.

## Closure evidence

- C1: `D-089` and `MUD-LEX-012`.
- C2: `D-062`, `D-089` and `MUD-LEX-013`.
- C3: `D-089` and `MUD-LEX-014`.
- C4: `specification/06-lexicon.md` and `specification/grammar/mud-lexico.ebnf`.
