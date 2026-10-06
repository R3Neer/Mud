---
id: Q-069
title: Foreign adapter contract and hosting protocol
priority: P0
opened: 2026-10-06
resolved: false
closed:
decisions:
  - D-109
affects:
  - foreign adapters, effects, dependency tracking, module dependencies, runtime and tooling
superseded-by: []
---

# Q-069 — Foreign adapter contract and hosting protocol

## Question

Define the machine-readable adapter protocol for native parsing, bridge boundaries, lexical captures, effect contracts, reads, determinism, static evaluation, errors, transactional calls and deferred host delivery.

## Accepted boundary

D-109 fixes syntax, immutable exports and inherited capability restrictions. Contracts are mandatory; arbitrary native libraries are not automatically pure or transactional. Rust, Python and Csharp are initial planned adapters, not implemented support.

## Closure criteria

Specify contract validation and rejection of missing/unknown effects; capture and dependency reporting including temporal snapshots; ABI/version negotiation; native build/runtime hosting including C# AOT; source maps and parser recovery; isolation, reentrancy and cancellation; dependency declarations coordinated with Q-062. Provide conformance cases for each protocol guarantee without reopening the accepted boundary.
