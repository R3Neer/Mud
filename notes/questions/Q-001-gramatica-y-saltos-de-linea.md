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
affects: []
superseded-by: []
---

# Q-001 — Grammar and line breaks

## Content

Status: **closed** by [[notes/decisions/ADR-050-comentarios-terminadores-y-separadores-numericos|D-050]], [[notes/decisions/ADR-056-char-texto-y-orden-unicode|D-056]] and [[notes/decisions/ADR-057-gramatica-concreta-y-continuacion|D-057]].

An instruction ends with `;` or a line break. A line break continues when the prefix cannot yet form a complete syntactic unit but admits a valid continuation; indentation has no role.

The complete syntax lives in `specification/grammar/`; [[specification/07-gramatica-concreta]] fixes precedence, open prefixes and contextual distinctions. Error recovery may vary between implementations, but never expands the accepted language.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-050`, `D-056`, `D-057`.
