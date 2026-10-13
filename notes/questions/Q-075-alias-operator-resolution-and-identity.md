---
id: Q-075
title: Alias operator resolution and identity
priority: P0
opened: 2026-10-08
resolved: true
closed: 2026-10-13
decisions:
  - D-156
  - D-153
  - D-149
  - D-146
affects:
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/21-expressions.md
superseded-by: []
---

# Q-075 — Alias operator resolution and identity

## Resolution

Static selection, origin-preserving inheritance, complete textual encoding and read-only operator/operand reflection are specified. Metadata attachment forms and descriptor categories are fixed; no first-class operator call or new TypeKind is introduced.

## Closure criterion

- C1: Deterministic selection and contrasting ambiguous/inherited cases exist.
- C2: Nominal/typed identity and complete descriptor encoding/schema cover declarations and applications.
- C3: Union/collection matching and builtin interactions have static evidence.

## Closure evidence

- C1: D-149, MUD-TYPE-031 and specification/types/test_operator_contract_witnesses.py.
- C2: D-156, specification/names/operator-contract-identity.md, chapter 10, reviewed nominal HIR and finite identity witnesses in specification/types/test_operator_identity_witnesses.py.
- C3: D-149, operator-union-and-narrowing / operator-direct-collection-priority corpus cases and test_operator_contract_witnesses.py.
