---
id: D-067
title: "Short names for numeric types"
status: current
date: 2026-08-02
supersedes: []
superseded-by: []
questions: []
affects:
  - "built-in numeric types, lexicon, concrete grammar, examples, diagnostics and syntax highlighting"
---
# ADR-067 — Short names for numeric types

- Amends: [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]], [[notas/decisiones/ADR-034-number-exacto-y-rumber-binary64|D-034]], [[notas/decisiones/ADR-040-semantica-numerica-basica-restante|D-040]], [[notas/decisiones/ADR-050-comentarios-terminadores-y-separadores-numericos|D-050]] and [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]]
- Affected documents: built-in numeric types, lexicon, concrete grammar, examples, diagnostics and syntax highlighting

## Context

The names `Integer`, `Natural`, `Number` and `Rumber` came from technical English terminology and made the most frequently used type unnecessarily long. MUD is also aimed at non-programmers and children creating games; its vocabulary should be short, recognisable and easy to type without losing the distinction between numeric domains.

`Money` already expresses an everyday idea and needs no abbreviation. The name `Rum` conflicts with no current language declaration, and case sensitivity still permits `rum` as an ordinary identifier.

## Decision

Built-in numeric types are written as follows:

| Former name | Current name | Domain |
| --- | --- | --- |
| `Integer` | `Int` | Signed integers. |
| `Natural` | `Nat` | Non-negative integers. |
| `Number` | `Num` | Ordinary exact numbers. |
| `Rumber` | `Rum` | `binary64` floating-point numbers. |
| `Money` | `Money` | Exact monetary amounts. |

`Int`, `Nat`, `Num`, `Rum` and `Money` are reserved words and built-in type names whose spelling is case-sensitive.

The four replaced forms cease to be reserved words and do not act as aliases. A program that still uses them as types must receive an unresolved-name diagnostic suggesting the current form when the intention is unambiguous.

This decision changes the concrete vocabulary, not the domains, conversions, operators, literals or normalisation rules defined for each type.

## Consequences

- Declarations and annotations are shorter.
- There is one canonical name for each numeric type.
- The change is source-incompatible and requires replacing the four former forms.
- Grammar, documentation and tools must recognise and display the current names.
- Internal tool identifiers may retain historical names when they are not visible and changing them would break existing configurations.

## Verification

1. Recognition of `Int`, `Nat`, `Num`, `Rum` and `Money` as built-in types.
2. Rejection of the four former forms as built-in types.
3. Preservation of each domain's semantics, literals and conversions.
4. Highlighting of the five current forms as built-in types.
5. Migration diagnostic suggesting the current name for each former form.
6. No collision between type `Rum` and ordinary identifier `rum`.
