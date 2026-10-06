---
id: D-130
title: Acyclic domain evaluation
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-017
affects:
  - "[[specification/10-type-system]]"
  - "[[specification/19-expressions]]"
  - "[[specification/README]]"
  - Declarative domain dependency and evaluation contracts
---

# ADR-130 — Acyclic domain evaluation

## Context

The author accepts rejecting cycles of domain evaluation. Q-017 concerns computed admissible sets, not nominal inheritance or module-path dependencies. This clarifies D-037's invalid-cycle restriction and D-029's separation between cyclic point intervals and domain dependencies.

## Decision

A computed domain must not depend, directly or transitively, on its own evaluation. Reject a circular dependency statically; do not select a least/greatest fixed point or iterate mutually recursive domain equations. Follow transitive calculations/callable dependencies needed to obtain the domain, rather than checking only its directly written names. Static admission must establish acyclicity; an unresolved potential recursive dependency is not evidence of safety. This does not claim a complete solver for arbitrary predicates or dynamic call graphs.

Reading an already stored value from the inherited coherent view does not evaluate its domain again. Checking a completed candidate's several field contracts against those available values therefore does not create a calculation edge between their validators. Constraints a <= b and b <= a can both be checked and require equality; they do not define a recursive fixed point. An initializer that actually needs an as-yet uncomputed value still obeys the separate initialization/dependency rules.

Recursive type descriptions, their finite immutable values and bounded constructor enumeration retain their existing rules. They do not license recursive computed-domain definitions. Periodic point-domain normalisation with cycle is also independent. Existing nominal inheritance, no-forward-reference and callable-cycle rules are unchanged.

## Contrasting cases

- A domain calculated from already stored cap and a finite interval is acyclic.
- Two domain validations reading already stored a and b in one candidate can both succeed when a equals b.
- EligibleA requires EligibleB to be evaluated, which requires EligibleA: statically invalid even if the equations are positive or finite sets.
- A negative self-dependency through complement is likewise invalid; no fixed point is chosen.
- A type Node with optional finite children can still have finite values and bounded constructor enumeration without recursive computed domains.

## Integration

MUD-TYPE-016 in chapter 10 defines static admission and the stored-read boundary; chapter 19 applies it to expression typing. The future domain chapter's remit and current ADR bodies are updated, and static conformance fragments contrast stored reads, hidden transitive cycles and positive recursion. No domain keyword, grammar constructor, nominal anchor or HIR field is introduced. Q-023's general dynamically selected callable proof question remains separate.
