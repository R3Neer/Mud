---
id: Q-076
title: Exact remainder signatures
priority: P1
opened: 2026-10-13
resolved: true
closed: 2026-10-13
decisions:
  - D-161
affects:
  - specification/11-type-system.md
  - specification/21-expressions.md
superseded-by: []
---

# Q-076 — Exact remainder signatures

## Question and resolution

The exact numeric % catalogue lacked signatures and a signed quotient convention.
The author selects Nat/Int/Num remainder, exact widening and truncating quotient.
Floor-based and integral-only alternatives are rejected. D-161 records acceptance.

## Closure criterion

- C1: Exact signatures, rational/sign behavior and zero-divisor treatment are specified.
- C2: Integration and contrasting mechanical/declarative evidence cover the boundary without adding Money remainder or %=.

## Closure evidence

- C1: D-161 and MUD-TYPE-039 in specification/11-type-system.md, with the numeric catalogue in specification/21-expressions.md.
- C2: Exact remainder cases in specification/types/typing-cases.yaml and rational sign/zero certificates in test_rum_witnesses.py; unchanged grammar and update catalogue.
