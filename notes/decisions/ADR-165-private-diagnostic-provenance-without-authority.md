---
id: D-165
title: Private diagnostic provenance without authority
status: current
date: 2026-10-14
supersedes: []
superseded-by: []
questions:
  - Q-080
affects:
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/20-blocks-and-recovery.md
  - specification/26-public-boundary.md
  - specification/types
---

# ADR-165 — Private diagnostic provenance without authority

## Context and acceptance

Mandatory Error/Refusal origins and ArgumentRefusal argument descriptors can
identify a part-only helper. Blanket private-value export prohibition otherwise
blocks normal public diagnostic propagation. The author accepts a diagnostic
provenance exception rather than requiring every private-helper failure to be
explicitly translated into a public diagnostic without its original provenance.

## Decision

Only established inherited Error.origin, Refusal.origin and ArgumentRefusal.argument
components may export their private declaration/participant descriptor references
as diagnostic provenance. Recognition is by original component declaration,
not the spelling origin/argument. The exception applies within finite cause
chains and diagnostic containers when their value types are otherwise visible.

The references retain canonical identity, with read-only intrinsic identifier,
anchor, path, file and supported category information. The existing category
availability rules still apply. No invocation, state access, private schema,
participant list, ancestry/type frontier or arbitrary configured metadata access
is granted by receipt. Ordinary static ~type/privacy rules cannot reveal a
private signature through this exception. Independent existing visibility rights
remain separate from the diagnostic reference.

Copying/widening/narrowing cannot make the private declaration visible or grant
host root capability. Export outside those reserved diagnostic component positions
retains the ordinary prohibition. A private Error subtype or an arbitrary extra
field exposing private types/declarations is not permitted by this exception.
No new source type, TypeKind, keyword, descriptor identity or nominal HIR field
is introduced; hosting must preserve the restriction under its pending protocol.

## Integration and evidence

MUD-TYPE-042 and MUD-PUBLIC-005 define the scoped exception. Current D-087/D-096/
D-118/D-131 bodies are reconciled. Public contract certificates and declarative
cases distinguish builtin diagnostics with private provenance, private schema
reflection, arbitrary payload fields and private Error subtype leakage.
