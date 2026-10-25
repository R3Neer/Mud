---
id: D-161
title: Exact truncating remainder
status: current
date: 2026-10-13
supersedes: []
superseded-by: []
questions:
  - Q-076
affects:
  - specification/11-type-system.md
  - specification/21-expressions.md
  - specification/types
---

# ADR-161 — Exact truncating remainder

## Context and acceptance

During static chapter drafting, the arithmetic catalogue included % without
complete Nat/Int/Num signatures or a quotient convention. The author accepts
remainder for all three exact representations with quotient truncated toward
zero, rather than integer-only remainder or a floor quotient.

## Decision

Nat%Nat yields Nat, Int%Int yields Int, and Num%Num yields Num. Mixed exact
operands use the existing Nat-to-Int-to-Num widening chain. For nonzero divisor
b, compute q=trunc(a/b) mathematically and return exact a-q*b. A zero divisor
produces Error occurrences under the ordinary demand/recovery contract.

Thus (-5)%3=-2, 5%(-3)=2 and (5/2)%1=1/2. Nonzero remainder has the dividend's
sign and magnitude strictly below abs(b). Money has no remainder signature;
Rum remains governed by D-160. No %= or implicit exact/Rum mixing is introduced.
Order-sensitive arithmetic collection lifting applies under
[[ADR-187-order-sensitive-collection-arithmetic-and-read-only-views|D-187]].

## Verification

MUD-TYPE-039, the expression catalogue, declarative sign/rational/mixing cases
and exact-rational supplied witnesses constitute the scoped evidence. This
adds no source syntax, compiler or runtime implementation. It extends D-129's
numeric matrix while retaining its Money and failure policies.
