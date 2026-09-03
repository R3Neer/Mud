---
id: D-091
title: "Family data as anchored descriptors"
status: current
date: 2026-08-16
supersedes: []
superseded-by: []
questions:
  - "Q-061"
affects:
  - "family, associated data, metadata, anchors, grammar, CST, superficial AST, post-typing and elaboration semantic representation, reflection and tooling"
---

# ADR-091 — Family data as anchored descriptors

- Modified by: [[ADR-102-complete-form-of-computed-family-data|D-102]].
- Modifies: [[ADR-038-close-knit-families-with-strong-values|D-038]].
- Clarifies: [[ADR-087-reflective-metadata-stable-descriptors-and-external-visibility|D-087]].
- Extends: [[ADR-070-lossless-cst-and-normalised-surface-ast|D-070]] and [[ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]].

## Context

D-038 defined uniform associated data for a `family` and stated that it had no identity of its own, referring to the values projected by each member. D-087 subsequently established that metadata-bearing elements need a typed descriptor and a stable public anchor. The anchor specification already classified `family` data under the `family` category, but the grammar and superficial AST did not allow metadata to be attached to it.

The declarable form of computed data is the complete `derived-value-shape` of computed fields, in accordance with D-102. This identity and metadata decision does not alter that contract.

## Decision

The declaration of stored or computed associated data is a stable semantic entity in the `family`'s uniform schema. It has:

- reflective `Field` descriptor;
- `FieldKind.Stored` or `FieldKind.Calculated`;
- subordinate anchor `family::<qualified-name>::<data>`;
- its own metadata sequence.

No `FamilyDataKind` or new anchor category is introduced.

A datum may be followed immediately by a body consisting exclusively of `~...` declarations:

```mud
family Terrain {
    movementCost: Nat = 1 {
        ~summary = "Base movement cost"
    }
    costly := movementCost >= 3 {
        ~summary = "Indicates costly terrain"
    }

    Plain,
    Mountain {
        movementCost = 4
    }
}
```

The metadata body belongs to the `movementCost` or `costly` descriptor, not to the value obtained for `Plain`, `Mountain` or another member. Querying `Mountain.movementCost` produces the associated value; it does not create a new descriptor per member.

A `family-data-assignment` within a member body is only an override of the effective value of stored data. It has no anchor, does not admit a metadata body and cannot modify the metadata of the declared datum.

The metadata body is added after the ordinary declaration form of computed data. The metadata preamble belongs to the descriptor and does not modify or restrict its `derived-value-shape`.


## Consequences

- Renaming associated data changes its descriptor's anchor.
- Changing a member's value changes neither anchors nor metadata.
- Data descriptors participate in a `family`'s `~fields` and `~declaredFields` as `Field`.
- `StoredFamilyDataDecl` and `CalculatedFamilyDataDecl` retain `metadata_assignment* metadata`.
- `CalculatedFamilyDataDecl` retains `derived_value_shape?` with the same derived form as computed fields.
- `FamilyDataAssignment` remains without metadata.

## Rejected alternatives

### Independent descriptor per member and datum

Rejected because it would artificially multiply entities that share a single schema and make a value override look like a declaration.

### New reflective `FamilyData` category

Rejected because the contract already matches `Field` and `FieldKind`; adding another reflective family provides no semantic difference.

### Allow a metadata body in a member override

Rejected because metadata describes the declared slot, not an occurrence of its value.

## Verification

1. The EBNF admits a metadata body on both declared data forms and does not admit it on `family-data-assignment`.
2. CST, coverage and AST projection retain the metadata body and complete `derived-value-shape` in the descriptor.
3. The superficial AST stores metadata in both data constructors and not in `FamilyDataAssignment`.
4. The anchor specification identifies the descriptor under the `family` category.
5. D-038 distinguishes descriptor identity from the absence of runtime identity for the projected value.
