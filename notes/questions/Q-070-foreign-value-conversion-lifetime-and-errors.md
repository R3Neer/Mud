---
id: Q-070
title: Foreign value conversion, lifetime and errors
priority: P0
opened: 2026-10-06
resolved:
closed:
decisions:
  - D-109
  - D-121
affects:
  - foreign adapters, wrappers, value exports, types, collections and diagnostics
superseded-by: []
---

# Q-070 — Foreign value conversion, lifetime and errors

## Resolution

Abstract contracts fix inputs, conversion validation, capabilities, reads, determinism, checked/trusted purity, isolation and Error translation. Unknown effects do not imply purity.

## Pending

Concrete ABI/version negotiation, native hosting, conversion/borrowing tables, lifetime protocols and adapter-specific conformance remain to be specified and implemented.

## Closure criterion

- C1: Specify conversion tables (including exact rational `Num`, text, nominal aliases and collections), borrowing/copying, identity-bearing inputs, wrapper disposal, retained-reference rejection, error categories and source-mapped diagnostics. Test alias leakage, invalid inbound domains/cardinality/order and exceptions after partial private work. Distinguish semantic rejection from technical failure.
