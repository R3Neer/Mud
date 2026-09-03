---
id: Q-057
title: Inner capability within alias values
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-07-30
decisions:
  - "D-031"
affects:
  - "structural aliases, capabilities and concrete grammar"
superseded-by: []
---

# Q-057 — Inner capability within alias values

## Question

If an alias representation contains a collection of `thing` values, decide whether it may declare an inner `[mut]` capability even when the alias value is immutable, what authority it grants and how to preserve the distinction between modifying a reached member and replacing the contained collection.

## Resolution

Yes. An alias component permits no outer `mut`, but its collection specification may declare `[mut]`. That capability permits modifying contained `thing` values directly without making the collection replaceable or the component updateable. It does not propagate implicitly through aliases or nested containers.

The decision is incorporated in [[notes/decisions/ADR-031-aliases-nominales-e-inmutables|D-031]] and the concrete grammar.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-031`, `structural aliases, capabilities and concrete grammar`.
