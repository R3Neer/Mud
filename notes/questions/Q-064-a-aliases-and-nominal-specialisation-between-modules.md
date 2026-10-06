---
id: Q-064
title: Aliases and nominal specialisation between modules
priority: P1
opened: 2026-08-28
resolved: true
closed: 2026-10-06
decisions:
  - D-096
  - D-116
affects:
  - modules, aliases, types
superseded-by: []
---

# Q-064 — Aliases and nominal specialisation between modules

## Resolution

Things and aliases use the same policy: uses authorization plus membership in the public contract type closure permits specialization. Private state and activation authority remain encapsulated; generated tooling exposes the frontier.

## Closure criterion

- C1: The complete choice described above is explicit and its affected developed surfaces agree.

## Closure evidence

- C1: D-116, its integration review and accompanying grammar/AST or semantic examples state the applicable contracts and delimit their conformance scope.
