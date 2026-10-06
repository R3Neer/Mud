---
id: Q-005
title: Binding identity and lifecycle
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-10-07
decisions:
  - D-041
  - D-045
  - D-058
  - D-099
  - D-126
affects: []
superseded-by: []
---

# Q-005 — Binding identity and lifecycle

## Resolution

Resolved by [[notes/decisions/ADR-126-reactive-binding-identity-and-observation-episodes|D-126]] and integrated into the developed normative surfaces below. Complete operational trace formalisation remains separate work; the choices identified by this question are fixed.

## Closure criterion

- C1: Binding identity distinguishes named role assignments and is independent of field values and enumeration order.
- C2: Observation continuity is defined for disappearance, suspension, rule recreation and participant rematerialisation, including generations changing between snapshots.
- C3: Initial/later baselines, changes, false filters and lifecycle no-ops have explicit compatible behaviour.

## Closure evidence

- C1: MUD-TIME-001 in [[specification/04-mathematical-model]] identifies the rule and role-to-participant mapping; D-126 distinguishes swapped roles and preserves causal occurrence identity.
- C2: MUD-TIME-001 and the temporal contract in [[specification/07-concrete-grammar]] end episodes on absence, suspension and generation changes; D-126 contrasts resumed observation and participant rematerialisation.
- C3: MUD-TIME-002 and [[specification/19-expressions]] retain changes as consecutive-observation comparison. D-126 cases contrast initial Rise, empty-to-member collection changes, returning bindings, false if and no-op creation.
