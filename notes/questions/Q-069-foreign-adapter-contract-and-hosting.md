---
id: Q-069
title: Foreign adapter contract and hosting protocol
priority: P0
opened: 2026-10-06
resolved:
closed:
decisions:
  - D-109
  - D-121
affects:
  - foreign adapters, effects, dependency tracking, part dependencies, runtime and tooling
superseded-by: []
---

# Q-069 — Foreign adapter contract and hosting protocol

## Resolution

Abstract contracts fix inputs, conversion validation, capabilities, reads, determinism, checked/trusted purity, isolation and Error translation. Unknown effects do not imply purity.

## Pending

Concrete ABI/version negotiation, native hosting, conversion/borrowing tables, lifetime protocols and adapter-specific conformance remain to be specified and implemented.

## Closure criterion

- C1: Specify contract validation and rejection of missing/unknown effects; capture and dependency reporting including temporal snapshots; ABI/version negotiation; native build/runtime hosting including C# AOT; source maps and parser recovery; isolation, reentrancy and cancellation; dependency declarations coordinated with Q-062. Provide conformance cases for each protocol guarantee without reopening the accepted boundary.
