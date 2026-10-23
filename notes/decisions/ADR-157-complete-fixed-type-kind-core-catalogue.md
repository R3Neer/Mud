---
id: D-157
title: Complete fixed TypeKind core catalogue
status: current
date: 2026-10-13
supersedes: []
superseded-by: []
questions:
  - Q-060
affects:
  - specification/11-type-system.md
  - specification/types
  - specification/09-abstract-syntax.md
---

# ADR-157 — Complete fixed TypeKind core catalogue

- Amended by: [[ADR-184-structural-traits-and-capability-views|D-184]].

## Decision and formalization

The author accepts Name, Anchor, MudPath, MudFile, Cardinality and Order as immutable nominal aliases for TypeKind classification, and Prefix as the closed SI family. This does not invent their payload APIs or introduce any TypeKind. The finite core inventory covers every public type constructor and established descriptor/support type under the existing public-exterior policy.

Projection first normalizes the effective public contract. Bare unrestricted singleton forms retain their member category; nondefault or nested collection-shaped contracts are Collection; a redundant unrestricted singleton specification is equivalent to omission. A nominal alias remains Alias even when represented by a collection, union or descriptor. Thus Errors and ActionReply are Alias; their unwrapped representation categories are not substituted. Applied generics retain constructor category. Named results/payloads retain their established producer categories.

Type, Field, Component, Participant, Metadata and Domain descriptor types retain their specific categories. Other declaration descriptor types, including family-member/unit/operator descriptors and the general Rule/Declaration views, use DeclarationDescriptor unless their effective public type has an established callable category. Operand name/type description records are Tuple. All reflective families, including TypeKind/DeclarationKind, are Family. Host-only Ticket, AST/IR/source nodes, erasure and block outcomes introduce no Mud value category.

A catalogue is fixed for the selected language version. Changing compiler releases cannot change it under the same target. A later version's catalogue is not merged into an earlier version; source moved to another language version is checked against that version. Added members can affect exhaustive family uses, and no automatic fallback or conversion is guaranteed. Project version declaration and persistent migrations remain Q-038, separate from fixed-version classification.

## Verification and provenance

Completes [[ADR-148-fixed-type-kind-family-and-normalized-projection|D-148]] and [[ADR-144-public-type-kind-categories|D-144]]. Chapter 11's complete core table/projection, support inventory and contrasting corpus cases cover Q-060. The schema of support aliases remains independent library/specification work; classification does not choose new representations.

The fixed target catalogue includes Trait for structural trait contracts and DeclarationKind.Trait for their declarations under D-184; trait declaration descriptors themselves remain DeclarationDescriptor. This is a language catalogue entry, not user extension.
