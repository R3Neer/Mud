---
id: D-103
title: "Inner capability in derived values"
status: current
date: 2026-08-29
supersedes: []
superseded-by: []
questions: []
affects:
  - "collections, derived values, inner capability, semantic identity and elaboration"
---
# ADR-103 — Inner capability in derived values

- Modifies: [[ADR-019-mutability-orthogonal-to-collection-and-members|D-019]], [[ADR-037-fields-and-declarative-domains|D-037]], [[ADR-081-filtering-take-and-indexing-de-collectiones|D-081]], [[ADR-084-specialisation-de-aliases-inherited-members-and-derived-views|D-084]] and [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].
- Relies on the derived collection form from [[ADR-075-enumerable-domains-all-and-derived-value-form|D-075]] and leaves D-039's algebraic `mut` propagation rules unchanged.

## Context

Every MUD value denotes a collection. Inner `[mut]` capability is distinct from the outer mutability of the place storing a collection and affects only immediate `thing` members. Derived forms could already declare cardinality and modifiers, but incompatible formulations coexisted about whether a view could grant inner capability absent from its source.

## Decision

### Derived cardinality

A derived cardinality declaration `[n]` produces a single collection whose result must have exactly `n` members after applicable transformations. A comma-separated list of expressions constructs that collection's outer members. An expression producing another collection occupies one member and is not implicitly flattened.

### Inner capability

`[mut]` is a collection guarantee, not outer mutability of its contents. In a derived form it acts as a capability requirement: it can be satisfied only when the source value already provides the necessary authority and transformations preserve the semantic identity of the same `thing` values. The derived form never manufactures authority.

Capability is reasoned about as a guarantee of the resulting collection, not as a superficial permission map per occurrence. A transformation may preserve it when the result still contains the same semantic identities with sufficient authority. Filtering, selection, `take`, indexing, slicing, deduplication, reordering and nominal view changes are preserving operations when they meet that condition. A projection or calculation producing other values does not preserve the source entity's capability.

### Collection algebra

This decision does not replace the collection algebra's specific inner-capability propagation rules. `|`, `&`, `--` and `^` retain exactly the rules fixed by D-039, including the capability an intersection may obtain from one operand and the capability a difference retains from its left operand.

### Nested containers

`[mut]` is not recursive. It reaches only `thing` values that are immediate members of the qualified collection. It does not cross aliases, structures or other containers and does not grant outer mutability to a collection appearing as a member of another collection.

When the effective member type contains no values with modifiable state, `[mut]` remains legal under the general inoperative-capability policy, but it enables no additional writes.

## Consequences

- A derived collection never has outer mutability merely by declaring `[mut]`.
- A `[n mut]` derived form combines a cardinality requirement with a capability requirement on its immediate `thing` members.
- A view that preserves semantic identity may retain already available capability, but cannot create it.
- A projection or calculation producing different values loses the source entities' capability.
- Nested collections retain their own mutability axes; outer `[mut]` does not make an inner collection externally mutable.
- Multiset algebra retains D-039's specialised rules and is not reduced to a uniform binary rule.

## Rejected alternatives

It is rejected that a derived view should grant inner capability absent from its source, that `[mut]` should cross containers or become outer mutability of a nested collection, or that this decision should replace the algebraic propagation rules already fixed for collection operations.

## Verification

1. A derived `[mut]` form is accepted only when the source and transformations can guarantee the required capability.
2. Selection, `take`, indexing, slicing, deduplication, ordering and view changes preserve capability when they preserve semantic identity and authority.
3. Projections and calculations producing other values do not thereby manufacture or preserve the source `thing`'s capability.
4. D-039 literally retains its `mut` propagation rules for `|`, `&`, `--` and `^`.
5. `[mut]` does not make a derived collection or a nested collection that is another collection's member writable.
6. A derived list retains its outer cardinality and does not flatten collections used as members.
