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
  - D-138
affects:
  - foreign adapters, effects, dependency tracking, part dependencies, runtime and tooling
superseded-by: []
---

# Q-069 — Foreign adapter contract and hosting protocol

## Resolution

Abstract contracts fix inputs, conversion validation, capabilities, reads, determinism, checked/trusted purity, isolation and Error translation. Unknown effects do not imply purity.

## Pending

Concrete ABI/version negotiation, native hosting, conversion/borrowing tables, lifetime protocols and adapter-specific conformance remain to be specified and implemented.

## Descriptor boundary

Q-071 owns the world/package schema and resolution. Adapter declarations, label-to-parser lookup, alias scope in installed distributions, minimum environments, native-manifest delegation, executable selection and diagnostics remain here. Author-selected labels and editor quick fixes are proposals, not implemented or accepted lookup rules. A foreign-language declaration does not itself prove purity or grant write authority.

## Closure criterion

- C1: Specify contract validation and rejection of missing/unknown effects; capture and dependency reporting including temporal snapshots; ABI/version negotiation; native build/runtime hosting including C# AOT; source maps and parser recovery; isolation, reentrancy and cancellation; dependency declarations coordinated with the fixed local-part boundary of Q-062 and the open distribution/schema boundary of Q-071. Provide conformance cases for each protocol guarantee without reopening the accepted boundary.
- C2: Specify adapter declarations, label/parser resolution, environment defaults, dependency-local scope, delegated manifests and incompatible/missing configuration diagnostics.
