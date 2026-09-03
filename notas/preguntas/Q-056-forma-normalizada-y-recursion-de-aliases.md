---
id: Q-056
title: Normalised form and alias recursion
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-084
affects: []
superseded-by: []
---

# Q-056 — Normalised form and alias recursion

## Decided by D-084

- Simple and multiple specialisation of aliases.
- Intersection of nominal representations and compatible domains.
- Inheritance of components and derived fields.
- Diamond deduplication by origin and conflicts between independent names.
- Exclusive overriding of stored defaults.
- Contextual construction and nominal member access.

## Outstanding

Complete inductive definition of normalised structural form for nested or recursive aliases; admission or rejection of direct and indirect recursion; productivity conditions; and decidability of compatibility, defaults and canonical enumeration for each component type.

## Closure criterion

Q-056 can close when the specification defines canonical normalisation for nested aliases, resolves recursion and establishes decidable conditions for compatibility, productivity, defaults and enumeration.
