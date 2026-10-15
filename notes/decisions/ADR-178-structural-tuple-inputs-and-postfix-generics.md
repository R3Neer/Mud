---
id: D-178
title: Structural tuple inputs and postfix generics
status: current
date: 2026-10-15
supersedes: []
superseded-by: []
questions: []
affects:
  - Anonymous products, dictionary input admission, coverage and generic presentation
---

# ADR-178 — Structural tuple inputs and postfix generics

## Decision

Prefer postfix generic application in examples, especially arity one: Nat List,
Rum Interval and Nat List(arguments). The latter folds as (Nat List)(arguments)
without required grouping. Explicit with application remains valid. This does
not infer missing generic arguments or add representation-alias constructors.

An anonymous tuple input of an exact or functional dictionary admits a
structural alias with an identical stored component sequence and complete
component contracts, comparing by position and ignoring source component names.
The target tuple names, if present, label the projected input. No extra/missing
components, implicit widening of distinct nominal component types, private
schema exposure or authority creation. This is a boundary projection, not
structural ===, nominal subtyping or automatic conversion between two aliases.

The input is the target tuple value, not the original alias with extra visible
members. Functional branches use value and .component/value.component; tuple
names do not inject bare locals. Additional original/common fields are not
exposed. Exact dictionary construction, insertion and lookup normalize through
the same tuple projection, so hashing/equality use target tuple components and
their ordinary supported equality. Equal projected keys collide regardless of
the source outer alias. Original caller values retain their nominal identity.
Structural type === still includes member names/order and complete guarantees.

A functional policy whose application-result cardinality admits zero needs no
universal selector coverage: no matching branch produces ordinary empty.
A zero minimum alone does not authorize discarding a required branch value.
FirstMatch stops at the first matching branch even if it returns empty;
AllMatches collects applicable results. Faults and ambiguous inference remain
errors, not fallback/absence. A positive application minimum retains coverage
and required result proofs. Take remains native pending its broader audit.

Partially amends D-039, D-041, D-085, D-086 and D-169. Existing neutral syntax for
named tuples, applications and CallExpr remains sufficient for projection.
No synthetic names or inferred type facts are added to Nominal HIR.
