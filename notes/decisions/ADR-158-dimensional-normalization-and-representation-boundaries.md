---
id: D-158
title: Dimensional normalization and representation boundaries
status: current
date: 2026-10-13
supersedes: []
superseded-by: []
questions:
  - Q-034
affects:
  - specification/11-type-system.md
  - specification/21-expressions.md
  - specification/types
  - specification/08-concrete-grammar.md
---

# ADR-158 — Dimensional normalization and representation boundaries

## Formalization of accepted contracts

Normalize linear dimensions as finite integer exponent maps over original base magnitude anchors, including independent unitless bases. Multiplication adds exponents and division subtracts them; remove zeros and serialize factors in anchor order. Derived declarations and unit equivalences form acyclic dependency graphs and are evaluated in topological anchor order. Canonical unit factors are reduced positive exact ratios of their checked canonical coordinate values, with fixed SI decimal powers. Derived root units are structural; normalization never creates or merges nominal magnitude/unit anchors.

Check every original representation operation before dimensional cancellation using existing numeric signatures. Money scaling and Money/Money follow chapter 21; unsupported Money*Money cannot be repaired by cancellation or reassociation. Money-producing arithmetic retains source-site ties-to-even rounding and result-domain admission. Explicit derived representation annotations must satisfy the established representability rules and cannot invent a cast or operation. Point kind/cycle compatibility is checked independently and never erased by linear factor equality.

Rum representation inference and literal/constant arithmetic portability remain Q-058. The dimensional algorithm consumes checked canonical quantities and does not choose those pending numeric rules. This completes Q-034's dimensional algorithm/Money boundary, not Q-058's numeric semantics.

## Verification and provenance

Formalizes [[ADR-028-system-of-quantities-and-units|D-028]], numeric representation contracts in chapter 21, D-030, D-076 and D-083 without introducing exponent syntax, conversions, unit declarations for every product or a compiler/runtime. MUD-TYPE-037, finite supplied-factor/ratio witnesses and contrasting corpus examples cover normalization, nominally independent bases and representation failures.
