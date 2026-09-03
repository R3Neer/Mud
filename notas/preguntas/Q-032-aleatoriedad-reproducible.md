---
id: Q-032
title: Reproducible randomness
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-048
  - D-081
  - D-100
affects: []
superseded-by: []
---

# Q-032 — Reproducible randomness

## Question

Which caching, retry and exposure rules complete the contract for reproducible random points?

## Already decided

The question is **partially decided** by [[notas/decisiones/ADR-048-azar-reproducible-y-fallos|D-048]], [[notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]] and [[notas/decisiones/ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].

Every random point has stable semantic identity and derives its choice from a reproducible seed. A computed field keeps its sample within one snapshot. `take` from an unordered source with genuine choice is also a random point, uniform and without replacement. Random consolidation points must not depend on accidental sequential consumption of a global PRNG: the choice must derive from the seed and the point's semantic identity, so independent points do not shift mechanically with consumption order. The concrete derivation or sub-seed algorithm is an implementation detail provided it preserves these properties.

## Outstanding

Caching and retry rules, and the observable exposure of stochastic fields or results, remain to be fixed.

## Closure criterion

- C1. Caching and retry rules for random points are fixed.
- C2. Observable exposure of stochastic fields and results is fixed.

## Resolution

Pending satisfaction of C1–C2.
