---
id: D-156
title: Canonical operator contract encoding and reflection schema
status: current
date: 2026-10-13
supersedes: []
superseded-by: []
questions:
  - Q-075
affects:
  - specification/10-names-and-anchors.md
  - specification/11-type-system.md
  - specification/21-expressions.md
  - specification/names
  - specification/types
  - specification/08-concrete-grammar.md
---

# ADR-156 — Canonical operator contract encoding and reflection schema

- Amended by: [[ADR-185-functional-operator-fields-and-global-signature-coherence|D-185]].

## Decision and formalization

Add DeclarationKind.Operator for an operator declaration descriptor. Its own TypeKind remains DeclarationDescriptor; no OperatorCallable or new TypeKind is introduced. This category was explicitly accepted by the author while completing the reflective schema.

The canonical specification in specification/names/operator-contract-identity.md defines a self-contained textual signature encoding over finite normalized contract graphs, with nominal references retained, canonical symbolic/binder labels, collision-free string escaping and graph numbering independent of source allocation. It preserves the accepted simple anchor, ordered signatures, original generic declaration ownership and metadata anchors. It is not a semantic IR schema or a serialization of callable implementations.

The schema exposes owner, anchor, kind, symbol, arity, ordered operand name/type descriptions, result and configured metadata. Operand descriptions are structural immutable named records, without independent anchors or metadata, not public for/given participants. An applied catalogue retains origin anchors but substitutes effective type contracts in its descriptor view. Static visibility remains mandatory and cannot silently filter inaccessible entries.

## Verification and provenance

Completes [[ADR-149-alias-operator-selection-inheritance-and-reflection|D-149]] and [[ADR-153-operator-descriptors-metadata-and-textual-anchor-policy|D-153]]. The chapter, complete identity/schema contract, contrasting declarative cases and finite supplied-graph witnesses cover Q-075. Witnesses do not normalize Mud source, implement nominal lookup or compile/evaluate operators. Chapter publication status remains unchanged.
