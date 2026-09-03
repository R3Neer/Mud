---
id: Q-014
title: Anchor migration
priority: P1
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-072
  - D-078
affects:
  - future chapter 09, compatibility, persistence and renaming tooling
superseded-by: []
---

# Q-014 — Anchor migration

## Question

How can a declaration be renamed or moved without losing history, references or compatibility?

## Already decided

[[notes/decisions/ADR-072-resolution-environments-and-explicit-anchor-migrations|D-072]] and [[notes/decisions/ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]] adopt readable anchors and an explicit directed correspondence from the former anchor to the new one. The correspondence migrates persistent references, history and data; it does not introduce a silent alias for compiling old source code.

## Outstanding

- Format and location of the migration record.
- Composition and flattening of chains of moves or renames.
- Detection of cycles and collisions between destinations.
- Retention period for historical entries.
- Concrete procedure for applying migration to persisted worlds and external artefacts.

## Closure criterion

The question can close when a compatibility and tooling decision fixes these five aspects and representative verification exists for chained migration and collision.
