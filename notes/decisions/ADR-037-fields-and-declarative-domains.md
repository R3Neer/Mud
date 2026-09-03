---
id: D-037
title: "Fields and declarative domains"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-003"
  - "Q-017"
  - "Q-061"
affects:
  - "future `14-fields-and-mutability.md`, future `17-domains-and-intervals.md`, future `30-final-constraints.md`"
---
# ADR-037 — Fields and declarative domains

- Amended by: [[ADR-103-inner-capability-in-derived-values|D-103]].

- Amended by: [[ADR-101-value-blocks-stored-local-variables-and-witness-extrema|D-101]].

- Amended by: [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]]
- Amended by: [[notes/decisions/ADR-084-alias-specialisation-inherited-members-and-derived-views|D-084]]
- Read more: D-019, D-026
- Amended by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].
- Amended by: [[notes/decisions/ADR-066-static-values-and-local-bindings-in-then|D-066]]
- Amended by: [[notes/decisions/ADR-068-universal-thing-and-intrinsic-name|D-068]]
- Expanded by: [[ADR-075-enumerable-domains-all-and-derived-value-form|D-075]]
- Related questions: Q-003, Q-017
- Documents affected: future `14-fields-and-mutability.md`, future `17-domains-and-intervals.md`, future `30-final-constraints.md`

## Decision

### Types of field

```mud
title: Text = ""
mut treasury: Money = 0
age: Nat in 0..150 [1] = 18
subjects: Person [* unique]
maintenanceCost := soldiers * 2
displayCost: Money := maintenanceCost
```

- `=` Enter the stored load.
- `:=` Enter a calculated, pure expression.
- `mut` grants outer mutability in accordance with D-019.
- Everything field denotes a collection in accordance with D-026. In a stored field immutable with an initialiser, a cardinality The omitted part can be inferred from the exact external shape of the value in accordance with D-085; in a field outwardly changeable yet enduring `[1]`.
- `~name` belongs to the metadata space of D-087. A field ordinary roll call `name` It is part of the members’ area and makes no secret of it.

The specific form of a stored field is:

```text
[mut] name : type [in domain] [collection-specification] [= value-body]
```

The domain precedes the specification from collection. A computed field usa:

```text
name [ derived-form ] := value-body
```

where the derived form may declare type and, in accordance with D-075, domain, cardinality and modifiers for collection compatible with the result.

Outer `mut` refers to the stored location and therefore precedes the name; it is neither a constructor nor a qualifier of the type. The form `name: mut type` is invalid.

An explicit stored-field value may be a short expression or a `ValueBlock`, but the entire body must be statically evaluable in accordance with D-066 and D-101. It may use internal temporary storage provided that it introduces no runtime dependencies or external effects. A computed field may likewise use a `ValueBlock` without acquiring persistent storage.

The entry for type is optional. If omitted, the compiler infers the type static nature of the expression; if written, the expression must be compatible with it, and the annotation may provide the type necessary to generate contextual phrases. When an unannotated expression does not have a type cannot be inferred unambiguously, the declaration is a error It is static and you must type it out.

The inference It does not apply a default priority between compatible interpretations. This includes both the representation of numeric literals and shared contextual forms. For example, `[3]` can draw up a collection the unit interval or the unit interval `[3..3]`: both forms are retained and one declaration calculated without sufficient context to allow a single choice to be made; you must note down your type. This omission is intended for common uses where the operations and dependencies of the expression determine a single type, not to ensure that every isolated expression is inferable.

The computed field always has a statically resolved type, whether declared or inferred. It has no assignable storage and does not support outer `mut`. Explicit nominal or structural types are checked statically. Domain, cardinality, `unique` and order declared in the derived form are coercive: they transform the result with the same semantics and normalisation as equivalent local transformations. `[mut]` is not a coercion that creates authority; it is an obligation based on capability and is fulfilled only when the result is already guaranteed by source-preserving transformations over the `thing` members.

For example, if `leftChars` has type `Char [1..5]` and `rightChars` has type `Char [0..2]`, `combinedChars := leftChars | rightChars` infers `Char [1..7]` in accordance with D-039. The result does not acquire modifiers that the propagation rules cannot guarantee.

When the context of declaration also supports a stored field and if the evaluated expression is statically closed, the compiler must suggest the equivalent immutable stored form. The suggestion is conservative; it does not alter the validity of the programme and does not authorise an automatic rewriting. It does not apply if the expression depends on state or whether storing it would affect its dependencies or its evaluation time.

### Domains

`in` restricts permissible values:

```mud
age: Nat in 0..150
given amount: Nat in 1..100
for people: Person in EligibleCitizens [1..* unique]
```

It may appear in fields, alias components, and `for` and `given` roles. A domain calculation must be pure, deterministic, non-stochastic, analysable and free from invalid cycles.

In a stored field or a role `for`, `in` appears after the type and before the specification from collection:

```mud
citizens: Person in EligibleCitizens [1..* unique]
```

The semantics from the type and explicit conversions are applied before checking for membership of the domain.

### Results by context

- `given` outside domain when applying for a action: `rejected` before assessing `if`, root or waves.
- `given` outside domain when looking up a Boolean rule: result `false`; if it is constant, it can be diagnosed statically.
- Field outside domain in a state candidate: the resolution it turns out `failed` and reverses.
- Constant initialiser outside domain: error static.

Calculated fields must satisfy both the domain of his type static, just like any other domain `in` declared in its derived form. That domain it may be explicit or be derived in accordance with D-075.

### Checkpoints

Domains are preserved during initialisation, materialisation, specialisation, deeds, title deeds, waves and publishable statuses. Q-003 must set out these points in a single semantics operational and determine which internal tentative states may exist without being observable.

The intermediate state exception granted by D-026 refers to cardinality inside the delta deprived of a `then`; it does not remove the ultimate obligation to domain.

### Contextual meanings of `in`

The parser and the AST distinguish between:

- Declarative restriction of domain.
- Local restriction or filtering of an expression by domain.
- Selection binding.
- Participant related.
- Unit from presentation of a magnitude.

`in` does not express Boolean membership; that operation uses `has` and `has not`. Sharing a token among the remaining uses of `in` does not merge their meanings.

## Consequences

- Domains form part of the type refined and the graph of departments.
- The validation 'entries' is separated from `if`.
- An invalid deed is never registered state partial.
- Finite domains power interfaces, tests, enumeration and `eventually`.

## Future verification

1. Domain steady and calculated.
2. `given` outside domain in good standing and action.
3. Stored field outside its domain, and valid `in` on a computed field in accordance with its derived form.
4. Cycle and invalid stochastic dependencies.
5. Computed field with type stated, inferred and not unambiguously inferable.
6. Rejection of `mut` external and `[mut]` such as authority manufactured in designated areas; acceptance of `[mut]` when the supplier guarantees the capacity, and `in`, cardinality, `unique` and order as derivative constraints.
7. Rollback without state Invalid publication.
8. Literal contextual `[3]` resolved by type expected and rejected without a inference unambiguous.
9. Suggested by stored field for a demonstrably accurate calculation invariant and the absence of any suggestion when it depends on state ever-changing.
10. Inference from cardinality, domain and modifiers in a computed field using operators from collection.
11. A compound static expression such as value stored and rejected runtime dependencies.
12. Role `for` individual or restricted group, limited by domain.

## Amendment by D-084

Structural aliases support derived fields and overrides of inherited defaults. Their derived forms preserve the distinction between a verification constraint and enforcement for domain/collection; coercion cannot create `[mut]` capability.
