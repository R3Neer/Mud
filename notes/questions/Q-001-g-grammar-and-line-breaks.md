---
id: Q-001
title: Grammar and line breaks
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-28
decisions:
  - D-050
  - D-056
  - D-057
  - D-141
affects: []
superseded-by: []
---

# Q-001 — Grammar and line breaks

## Content

Status: **closed** by [[notes/decisions/ADR-050-comments-terminators-text-and-numeric-separators|D-050]], [[notes/decisions/ADR-056-char-text-and-unicode-ordering|D-056]] and [[notes/decisions/ADR-057-concrete-grammar-precedence-and-continuation|D-057]].

An instruction ends with `;` or a separating newline. An open prefix admits grammatical continuation. For a complete prefix, a following separate-unit start wins, including an incomplete next instruction; otherwise a valid extension continues the current unit. Neither viable interpretation means a syntax error. Comments and blank lines are skipped; semicolons and enclosing boundaries are not crossed. Indentation, names and types do not select the boundary. The accepted amendment is [[notes/decisions/ADR-141-contextual-newline-continuation|D-141]]; this scope remains resolved.

The complete syntax lives in `specification/grammar/`; [[specification/08-concrete-grammar]] fixes precedence, open prefixes and contextual distinctions. Error recovery may vary between implementations, but never expands the accepted language.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-050`, `D-056`, `D-057`, `D-141`; MUD-SYN-015 in `specification/08-concrete-grammar.md`, the CST trivia/projection contract and `specification/syntax/cases/newline-cases.json` with its finite boundary checker.
