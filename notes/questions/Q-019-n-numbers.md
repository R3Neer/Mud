---
id: Q-019
title: Numbers
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-10-07
decisions:
  - D-028
  - D-030
  - D-034
  - D-040
  - D-060
  - D-067
  - D-080
  - D-129
affects: []
superseded-by: []
---

# Q-019 — Numbers

## Resolution

Nat/Int/Money have arbitrary precision. Money's scaling, ratio and unsupported-operation matrix is fixed, combined with existing nominal dimensional admission. Impossible supported arithmetic uses the Error channel. Num exactness, finite Rum, rounding/conversion, Nat saturation and restricted collection lifting retain their existing contracts. Error subtype taxonomy and binary64 portability remain separately scoped, not missing numerical limit/signature choices.

## Closure criterion

- C1: Fix Nat/Int/Money representation bounds and observable overflow behaviour.
- C2: Fix Money's member arithmetic signatures, widening boundary, rounding, update results and combination with magnitude dimensions.
- C3: Fix failure versus normal-result behaviour without altering existing Nat or empty-lifting semantics.

## Closure evidence

- C1: [[notes/decisions/ADR-129-unbounded-exact-numbers-and-money-operators|D-129]] and chapter 10's inclusion section require arbitrary precision and promotion before overflow, distinguishing resource faults from numerical values.
- C2: MUD-TYPE-015 and the table/rounding paragraphs of [[specification/19-expressions]] define the matrix and dimensional boundary; [[specification/types/typing-cases.yaml]] contrasts scaling, exact ratio, rejected operations and invalid update narrowing.
- C3: Chapter 19's numeric failure contract and [[specification/25-effects]] preserve ordinary Error/recovery/rollback, Nat ledger rules and empty lifting; conformance fragments distinguish zero divisors from a non-evaluated empty pair.
