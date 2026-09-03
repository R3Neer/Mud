---
id: Q-024
title: Data associated with `family` members
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-07-28
decisions:
  - D-038
affects: []
superseded-by: []
---

# Q-024 — Data associated with `family` members

## Content

Status: **closed** by [[notes/decisions/ADR-038-familias-cerradas-de-valores|D-038]].

A `family` may directly declare a uniform schema of immutable, stored or computed data before its members. Each member may override stored values in a sub-block; omitted values come first from the data's explicit default and then from its type's default. Computed data is evaluated statically for each member, has an optional type when it can be inferred uniquely, permits acyclic dependencies on other associated data and cannot be overridden by the member. Data does not alter the member's identity or nominal equality.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-038`.
