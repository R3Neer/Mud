---
id: D-019
title: "Mutability orthogonal to collection and members"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "future `14-fields-and-mutability.md`, future `15-collections.md`"
---
# ADR-019 — Mutability orthogonal to collection and members

- Amended by: [[ADR-103-inner-capability-in-derived-values|D-103]].

- Amended by: [[notes/decisions/ADR-084-specialisation-de-aliases-inherited-members-and-derived-views|D-084]]
- Amended by: [[notes/decisions/ADR-063-signatures-given-and-joint-on-bindings|D-063]]
- Documents affected: future `14-campos-y-mutabilidad.md`, future `15-colecciones.md`
- Amended by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].

## Context

Everything field MUD is consistently interpreted as a collection with cardinality. The cardinality omitted is equivalent to `[1]`; it does not convert the field in a category semantics different.

MUD distinguishes between two types of permission:

1. Change the collection stored: add, remove, replace or reorder elements.
2. Amend the `thing` achieved as members of the collection.

The previous wording suggested an exception for cardinality a unique feature whereby:

```mud
mut capital: City [1]
```

could be interpreted as:

```mud
capital: City [1 mut]
```

That equivalence conflated two distinct permissions precisely in this case `[1]`.

## Decision

The two axes are orthogonal for all cardinality, including `[1]`.

- `mut` before the name, it grants mutability outside the collection stored.
- `mut` inside the specification from cardinality bestows inner strength upon its members.
- Neither position implies the other.
- There is no exception for singular fields.
- Outer `mut` refers to a storage location, not to the member type: it is written `mut name: Type`; `name: mut Type` is invalid.

| Declaration | Change collection | Edit members |
| --- | --- | --- |
| `capital: City [1]` | No | No |
| `mut capital: City [1]` | Yes | No |
| `capital: City [1 mut]` | No | Yes |
| `mut capital: City [1 mut]` | Yes | Yes |

The cardinality The omitted one follows exactly the same rule:

```mud
mut capital: City
capital: City [mut]
```

are equivalent, respectively, to:

```mud
mut capital: City [1]
capital: City [1 mut]
```

The first form is not the same as the second: to omit `[1]` does not displace `mut` between the two axes.

## Stored fields and derived fields

A stored field has a value collection whose structure can only change when it declares mutability outdoors.

A derived field it also results, semantically, in a collection, but its membership is recalculated based on its expression. It does not support mutability external because there is no collection stored rather than written. It can specify internal capacity `[mut]` as a liability on the `thing` directly contained only when the value The source already provides that authority and the transformations preserve the identity semantics relevant. The derived form does not generate capacity.

Inner capacity never makes one’s sense of belonging collection derived, does not traverse aliases or nested containers, and does not grant mutability outside a collection whatever the case may be member another collection.

## Participants `for`

Any role `for`, including the singles event at cardinality `[1]`, retains the same two axes. In a action:

```mud
mut patients: Person [1..10, unique, mut]
```

the first `mut` allows you to change the collection provided, and the second allows you to modify the `Person` member. The mutability The external key links the role by reference to a stored location: the receiver of the call must appoint a collection outwardly changeable. A literal, a union or another collection The calculated values are just that – values – and cannot satisfy that contract.

Without `mut` externally, the role receives the value of any expression of collection compatible. The internal capacity continues to be verified regardless of whether the collection comes from a place or an expression. When the type The cash does not contain any amounts with state editable, write `[mut]` It remains legal, but the compiler suggests removing it because the capability cannot be exercised. D-063 Replace the previous rejection with this suggestion.

The mutability 'external' also applies to locations that store basics, aliases, members of `family`, dictionaries or collections of such values. It allows the content to be replaced or reorganised, but does not make the values it contains mutable:

```mud
mut observations: Num [*]
```

Boolean rules and `look` they are pure and do not tolerate mutability outwardly in their roles `for`. Automatic roles `on` They remain individual and can only declare their internal capacity in relation to the `thing` related. The `given` They do not accept either of these permits.

## Consequences

- Replace the only one member from `[1]` It is an external mutation.
- Modify fields in the unique table member requires inner strength.
- One action It may require both permissions and must declare them explicitly.
- The omission of `[1]` It is simply sugar from cardinality; it does not change permissions.
- The AST and the IR must be stored separately `outerMutable` e `elementMutable`.
- Heritable linkage must be analysed independently for both axes.
- One call in a role `for` externally changeable requires a receiver-enter the location and retain the reference to the written destination in the IR.

## Compatibilidad

Any interpretation that equates the two singular forms is hereby withdrawn. Until a stable version is released, no migration of published programmes is required; internal examples should be interpreted in accordance with this decision.

## Future verification

The suite must check the four combinations in the table for both `[1]` as well as for multiple cardinalities, in addition to:

1. Rejection of substitution without mutability outdoors.
2. Rejection of the amendment to the member with no interior capacity.
3. Lack of an implicit inner capacity in `mut field: T`.
4. Absence of mutability external implicit in `field: T [mut]`.
5. Rejection of outer `mut` on a derived field.
6. Inference of inner capability retention in a derived collection.
7. Roles `for` from cardinality `[1]` and collective, with the four capacity combinations.
8. Rejection of a literal o result calculated as receiver of a role that is outwardly changeable.
9. Rejection of outer mutability in Boolean rules, `look` and `on` roles.
10. Outer mutability of a collection of immutable values without any inner capability.
11. A suggestion for removing a demonstrably useless inner capability from immutable values.

## Amended by D-084

The ownership of a collection The derivative is set for the snapshot under review and is recalculated after effects have been consolidated. Members may join or leave automatically. Stored collections are not automatically pruned. Contracts in the result Derivatives are validated following recalculation; if they do not comply, the transition.

