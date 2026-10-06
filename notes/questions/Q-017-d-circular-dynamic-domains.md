---
id: Q-017
title: Circular dynamic domains
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-10-07
decisions:
  - D-130
affects: []
superseded-by: []
---

# Q-017 — Circular dynamic domains

## Resolution

Computed-domain evaluation must be acyclic. Recursive domain equations are statically invalid; no fixed point is selected. Validation against already stored candidate values does not recursively evaluate those values' domains. Recursive types/finite constructor enumeration and cyclic point intervals retain their distinct contracts.

## Closure criterion

- C1: Identify prohibited domain-evaluation dependencies and state whether fixed-point evaluation is admitted.
- C2: Distinguish these cycles from stored-value validation, initialization cycles, recursive types/enumeration and cyclic point domains.

## Closure evidence

- C1: [[notes/decisions/ADR-130-acyclic-domain-evaluation|D-130]] and MUD-TYPE-016 in [[specification/10-type-system]] require static acyclicity including transitive calculation dependencies and reject recursive equations without fixed-point evaluation.
- C2: Chapter 10's stored-read and enumeration paragraphs, chapter 19's expression admission, the domain roadmap and [[specification/types/typing-cases.yaml]] contrast available candidate values with direct/transitive recursive domain calculations.
