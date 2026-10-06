---
id: Q-056
title: Normalised form and alias recursion
priority: P2
opened: 2026-07-29
resolved: true
closed: 2026-10-06
decisions:
  - D-084
  - D-113
  - D-122
affects: []
superseded-by: []
---

# Q-056 — Normalised form and alias recursion

## Resolution

MUD-TYPE-004 and MUD-TYPE-005 in [[specification/10-type-system]] define constructor productivity, domain witness obligations and finite effective enumeration. The productivity/representation/proof-boundary witnesses and regression tests distinguish recursive reachability from admissible finite values and unknown from proof.

The required analysis is sound and conservative, not a complete solver for arbitrary symbolic predicates. Operational engine and general termination design retain their own questions.

## Closure criterion

- C1: The remaining formal proof/minimum-analysis boundary is specified with objective obligations and contrasting conformance evidence.

## Closure evidence

- C1: MUD-TYPE-004 and MUD-TYPE-005 in [[specification/10-type-system]] define constructor productivity, domain witness obligations and finite effective enumeration. The productivity/representation/proof-boundary witnesses and regression tests distinguish recursive reachability from admissible finite values and unknown from proof. [[notes/decisions/ADR-122-finite-type-graphs-and-proof-obligations|D-122]] records the integration.
