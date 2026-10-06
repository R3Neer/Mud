---
id: D-129
title: Unbounded exact numbers and Money operators
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-019
affects:
  - "[[specification/10-type-system]]"
  - "[[specification/19-expressions]]"
  - "[[specification/25-effects]]"
  - Numeric and dimensional operator contracts
---

# ADR-129 — Unbounded exact numbers and Money operators

## Context

The author accepts arbitrary precision for Nat/Int/Money, specific Money scaling signatures and Error outcomes for impossible computations. This completes Q-019's remaining representation-limit, Money-matrix and arithmetic-failure scope. It extends D-034's exactness policy and amends the pending scope of D-028/D-040.

## Decision

Nat and Int are mathematical nonnegative and signed integers respectively. Money is a signed integer number of hundredths, without a language-level bound on that integer. Num remains an exact rational. Native bounded storage is permitted only with promotion before observable overflow; exhaustion of resources is a technical fault, not numerical wraparound or a new arithmetic value.

Money + Money and Money - Money yield Money. Money * Num, Num * Money and Money / Num yield Money; Nat/Int factors use the existing exact widening chain to Num. Money / Money yields Num. Money * Money, a scalar divided by Money, and mixed Money addition/subtraction are not admitted. No Money remainder signature is introduced. Rum and Money never mix implicitly. These specific signatures are not a general implicit conversion to/from Money.

A Money-producing scaling operation computes its exact rational amount, rounds to hundredths using round-to-nearest, ties-to-even, then checks the result domain. Sequential operations round at their own sites. Concurrent stages use the existing canonical stage evaluation and normalisation, not an invented ordering among sibling operators. A Money ratio remains exact Num and is not rounded to hundredths.

For magnitudes, apply the representation signatures together with existing nominal dimensional/linear/point admission. Multiplication/division compose nominal factors; addition/subtraction need the compatible dimensions and modes. Representation compatibility alone never erases a dimension or coerces unrelated unitless magnitudes. An explicit representation annotation does not grant an extra conversion or rounding operation. An undefined coordinate signature rejects the quantitative operation.

Unsupported signatures are static errors. A supported computation with a zero divisor, invalid destination domain/conversion, or a prohibited nonfinite Rum result has no normal value and uses Error occurrences under the owner's existing recovery/rollback contract. A statically invalid closed computation is diagnosed statically. No wraparound, sentinel, implicit empty or additional saturation is introduced. Pure Nat subtraction and signed additive effect bookkeeping retain their established distinct rules. Empty collection lifting still performs no member operation.

An arithmetic update must preserve the stored destination contract. Money *= Num and Money /= Num are admitted with the ordinary proof/authority obligations; Money /= Money is not, since its member result is Num and there is no implicit narrowing into Money. Error subtype names remain in Q-007 and binary64 portability in Q-058.

## Contrasting evidence

- Money 10.00 * Num 0.125 yields Money 1.25.
- Money 0.01 / Num 2 yields Money 0.00; Money 0.03 / Num 2 yields Money 0.02.
- Money 0.01 / Money 0.03 yields exact Num 1/3.
- Money plus an Int, Money multiplied by Money and Money divided by Rum are rejected.
- Nat/Int/Money do not wrap at a native integer boundary.

## Integration

Chapters 10/19 fix the scalar contracts, signatures and error boundary. Chapter 25 delegates representation validation/rounding to those contracts. Static conformance fragments distinguish these cases. No grammar, nominal resolver, AST or HIR constructor changes are required.
