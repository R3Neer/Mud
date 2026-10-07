---
id: D-136
title: Static given call disambiguation
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions: []
affects:
  - "[[specification/10-names-and-anchors]]"
  - "[[specification/11-type-system]]"
  - "[[specification/21-expressions]]"
  - "[[specification/08-concrete-grammar]]"
---

# ADR-136 — Static given call disambiguation

## Context

The author accepts extending receiver-based selection to provided given names/types to help programmers select homonymous imported operations. This partially amends D-035, D-036, D-072, D-078 and D-106; reciprocal current-body amendments preserve their other contracts.

## Decision

At the first non-empty nominal lookup level, candidates governed by for independently check supplied receivers and actually written given arguments. Use static names, binding shape, types, guarantees and permissions; only proven incompatibility excludes a candidate. Missing required arguments are incompatible; a written default permits omission without invented evidence or preference. Candidate-local contextual literals and generic constraints cannot inherit a competing candidate's contextual interpretation. Generic explicit arguments/bounds participate; unresolved inference is not proof of failure. Exactly one declaration must remain before an expected result may refine its inference. No runtime expressions, predicates, defaults or bodies execute to select it, no most-specific tie-break is added and failed compatibility cannot fall through to later levels. Bare descriptor references and stored callable role contracts retain their existing rules.

## Verification

Equal receiver signatures with different given names/types can be separated by written arguments. Contextual literals, overlapping accepted argument types, expected outputs and omitted defaults cannot create an implicit priority. Unions require one static target for all alternatives. Nominal HIR retains its candidate set and source syntax without type or inference proofs. Declarative and finite signature witnesses cover selection, ambiguity, missing roles, defaults and lookup blocking.
