---
id: D-181
title: String primitive spelling
status: current
date: 2026-10-23
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/
  - notes/examples/duelo-spellcasting
  - notes/decisions/
  - tooling/README.md
---

# ADR-181 — String primitive spelling

## Decision

The canonical textual primitive is String. The author confirms the rename from
Text without changing textual value semantics, Unicode/Char contracts, literal
syntax, interpolation, conversion, order or equality. String is reserved as the
primitive spelling. Text is not a compatibility spelling or a builtin alias.
It may only denote an independently declared user type under ordinary naming
rules. Existing semantic AST/token names such as TextTemplateExpr describe
literal structure rather than a primitive source spelling and remain unchanged.

Current specification surfaces, catalogue/corpus checks, current decision
examples and the source-only spell model use String consistently. This partially
amends the spelling in D-056/D-085/D-157 without changing their other semantics.

## Verification

Lexical fixed tokens, grammar references and builtin type witnesses agree.
Repository validators and bounded tests check the rename; no compiler, native
bridge or external editor release is implemented by this decision.
