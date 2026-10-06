---
id: Q-070
title: Foreign value conversion, lifetime and errors
priority: P0
opened: 2026-10-06
resolved: false
closed:
decisions:
  - D-109
affects:
  - foreign adapters, wrappers, value exports, types, collections and diagnostics
superseded-by: []
---

# Q-070 — Foreign value conversion, lifetime and errors

## Question

Define concrete wrapper/native representations and conversion rules for Rust, Python and Csharp, including ownership, lifetime, exception mapping and unique type inference.

## Accepted boundary

D-109 requires immutable MUD values, inbound validation, preservation of nominal types, domains, exact numbers and collection contracts, and no opaque foreign escape or hidden mutable aliases. Writes through wrappers remain subject to MUD capabilities and transaction isolation.

## Closure criteria

Specify conversion tables (including exact rational `Num`, text, nominal aliases and collections), borrowing/copying, identity-bearing inputs, wrapper disposal, retained-reference rejection, error categories and source-mapped diagnostics. Test alias leakage, invalid inbound domains/cardinality/order and exceptions after partial private work. Distinguish semantic rejection from technical failure.
