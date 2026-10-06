---
id: D-111
title: "Static thing field schema"
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-002
affects:
  - "Thing fields, lifecycle, effects, metadata, grammar, CST, Surface AST, nominal resolution and conformance"
---

# ADR-111 — Static thing field schema

- Modifies: [[ADR-021-cycle-logical-lifespan-and-suspension-by-department|D-021]], [[ADR-046-algebra-and-conflicts-of-effects|D-046]], [[ADR-054-canonical-definitions-and-initial-activation|D-054]], [[ADR-087-reflective-metadata-stable-descriptors-and-external-visibility|D-087]] and [[ADR-099-fresh-materialisations-after-destroy-and-create|D-099]].
- Clarifies the surviving collection/activity scope of [[ADR-023-consolidation-of-concurrent-structural-effects|D-023]].
- Preserves canonical identity, dependency suspension, stored-value reset after destruction, collection algebra and the transactional adapter boundary of [[ADR-109-foreign-language-blocks-and-value-exports|D-109]].

## Context

The author excludes runtime creation and deletion of field declarations. `add` previously had a field-declaration form, and `remove` could delete a property. Those two operations are withdrawn together; collection membership operations remain.

## Decision

The complete set of fields a `thing` may have comes exclusively from its canonical static schema, including specialisation. Runtime may change permitted stored values, collection membership, relations and activity, but cannot add or delete field declarations, alter their descriptors or redefine their contracts. Foreign adapters are subject to the same restriction.

`add expression to assignable-expression` and `remove expression from assignable-expression` operate on compatible writable collections under their existing contracts. Inserting or deleting a dictionary association changes collection contents, not the owning `thing`'s field schema. A `thing` declaration is not interpreted as a destination for property creation/deletion; singleton cardinality does not grant that capability.

The field-declaration alternative of `add-effect` and `AddFieldEffect` are eliminated. `remove-effect` retains its grammar and `RemoveEffect`; name resolution and elaboration no longer give it a property-deletion interpretation. Thus an attempted field declaration in `add` is a syntactic error, whereas a syntactically valid `remove` with a non-collection/non-writable target is rejected at the appropriate later phase.

Dependency suspension may remove a field from the effective projection while retaining its static declaration and applicable stored load. That is not schema deletion. Destroying a concrete owner discards its own materialisation's stored values; recreating the same canonical identity derives its effective schema from static definitions and reapplies defaults/initialisers. No runtime-edited schema needs to be retained or restored. Rule activation memory and immutable/mutable relation restoration retain their existing contracts.

All field descriptors and their metadata derive from canonical declarations. There is no dynamic-field metadata admission case. Editing the source model remains a tooling operation, distinct from runtime effects.

## Integration review

The change covers grammar and its CST catalogue/coverage, Surface AST, CST conversion, developed mathematical/syntax/nominal surfaces, specification roadmap and affected current ADR bodies. The nominal HIR has been reviewed: it already represents canonical field symbols and needs no structural change. Collection value insertion/removal, immutable alias write-back, `create`/`destroy`, branch editing by authoring tools and local frame storage remain in scope under their existing contracts.

Q-002 remains partially decided for the complete operational semantics of the surviving effect families; this decision removes schema edits from that scope without claiming to finish the algebra.

## Verification

1. Ordinary and `mut` field-declaration forms of `add` are syntactically rejected.
2. Removing a property from a `thing` does not receive a property-deletion interpretation.
3. Collection insertion/removal and dictionary association updates retain their surface nodes and contracts.
4. Destruction/recreation restores initial values from the static inherited schema; suspension retains declarations and independently owned load.
5. Mechanical regression checks reject reintroduction of the field alternative or constructor and preserve collection `add`/`remove`.
6. No existing current surface describes runtime field creation/deletion as valid; negative examples and this decision's provenance remain explicit.
