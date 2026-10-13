---
id: Q-080
title: Private diagnostic origin boundary
priority: P1
opened: 2026-10-14
resolved: true
closed: 2026-10-14
decisions:
  - D-165
affects:
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/20-blocks-and-recovery.md
  - specification/26-public-boundary.md
superseded-by: []
---

# Q-080 — Private diagnostic origin boundary

## Resolution

The author accepts private provenance descriptors in the established Error/Refusal
origin and ArgumentRefusal argument components, without operational/private-schema
authority. No private subtype or arbitrary user field becomes exportable.
Mandatory explicit translation of every internal failure is rejected.

## Closure criterion

- C1: Define the diagnostic exception and its identity/provenance visibility.
- C2: Preserve privacy, invocation/schema restrictions and inherited component provenance with evidence.

## Closure evidence

- C1: D-165, MUD-TYPE-042 and MUD-PUBLIC-005 with private diagnostic cases in specification/types/typing-cases.yaml.
- C2: Original-component recognition, private subtype/arbitrary-field/reflection rejection cases and finite public-contract certificates; 10/HIR reviewed with no new nominal entities.
