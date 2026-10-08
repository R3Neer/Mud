---
id: Q-018
title: Discontinuous intervals
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-10-08
decisions:
  - D-143
  - D-049
  - D-059
  - D-082
  - D-088
affects: []
superseded-by: []
---

# Q-018 — Discontinuous intervals

## Question

How are discontinuous intervals written, normalized and used as keys?

## Closure criterion

- C1: Define the source form without an ambiguous segment literal.
- C2: Define canonical content, equality and keys, including empty and boundary gaps.
- C3: Define signed traversal and per-segment stepping.

## Resolution

Closed by [[../decisions/ADR-143-discontinuous-interval-normal-form]]. Existing interval algebra constructs discontinuous intervals. Canonical maximal segments determine content and keys. Signed traversal remains the D-088 contract.

## Closure evidence

- C1: specification/08-concrete-grammar.md and existing interval-algebra productions in grammar/mud.ebnf.
- C2: MUD-TYPE-025 and discontinuous-interval-content in types/typing-cases.yaml; finite integral certificates in test_interval_witnesses.py.
- C3: D-088 and specification/08-concrete-grammar.md signed progression/segment-restart rules, retained by MUD-TYPE-025.
