---
id: Q-023
title: Dynamic composition
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-10-14
decisions:
  - D-166
affects:
  - specification/types/contextual-call-analysis.md
  - specification/11-type-system.md
  - specification/15-fields-and-mutability.md
superseded-by: []
---

# Q-023 — Dynamic composition

## Resolution

D-166 specifies finite nominal destination contexts, conservative compatible
catalogue fallback and an exact least-fixed-point procedure. Contextual call
SCCs preserve action/test/admissibility acyclicity. Pure recursive components
need their separate termination certificate. Read/write/domain/availability
summaries substitute actual bindings and join every remaining target.
The resolution does not design the causal or host/native algorithm.

## Closure criterion

- C1: Specify destination/context construction, conservative unknowns and exact finite completion.
- C2: Define contextual acyclicity, complete transitive impact and permission boundaries.
- C3: Provide contrasting finite contextual/cyclic/open-input and summary evidence.

## Closure evidence

- C1: D-166, MUD-TYPE-043 and MUD-CALL-001 in specification/types/contextual-call-analysis.md.
- C2: MUD-CALL-002/MUD-CALL-003, caller place substitution and existing cardinality/privacy interfaces.
- C3: specification/types/test_contextual_call_witnesses.py and contextual-call corpus cases in specification/types/typing-cases.yaml; nominal HIR reviewed without shape changes.
