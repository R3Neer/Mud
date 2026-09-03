---
id: D-084
title: "Alias specialisation, inherited members and derived views"
status: current
date: 2026-08-04
supersedes: []
superseded-by: []
questions:
  - Q-056
affects:
  - "aliases, grammar, syntax, nominal resolution, derived collections and empty `thing` bodies"
---
# ADR-084 — Alias specialisation, inherited members and derived views

- Modified by: [[ADR-103-inner-capability-in-derived-values|D-103]].

- Modified by: [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]]
- Modified by: [[ADR-086-exact-nominal-identity-external-arrows-and-dictionary-algebra|D-086]]
- Modifies: [[notes/decisions/ADR-015-acyclic-specialisation-and-state-independent|D-015]], [[notes/decisions/ADR-018-as-declares-specialisation-in-is-the-query|D-018]], [[notes/decisions/ADR-019-mutability-orthogonal-to-collection-and-members|D-019]], [[notes/decisions/ADR-031-nominal-aliases-immutable-and-without-cycle-of-life|D-031]], [[notes/decisions/ADR-032-contextual-construction-and-nominal-casting-of-aliases|D-032]], [[notes/decisions/ADR-037-fields-and-declarative-domains|D-037]], [[notes/decisions/ADR-054-canonical-definitions-and-initial-activation|D-054]], [[notes/decisions/ADR-068-universal-thing-and-intrinsic-name|D-068]], [[notes/decisions/ADR-074-nominal-unions-and-type-narrowing|D-074]], [[notes/decisions/ADR-078-nominal-resolution-anchor-catalogue-and-initial-graph|D-078]] and [[notes/decisions/ADR-081-collection-filtering-take-and-indexing|D-081]].
- Reduces: [[notes/questions/Q-056-f-normalised-form-and-alias-recursion|Q-056]].
- Affected documents: grammar, superficial and resolved AST, names and anchors, mathematical model and derived-collection semantics.
- Modified by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].

## Context

Aliases were already nominal and immutable types, but it was not fixed how to specialise them, combine inherited representations or inherit a structural form. Derived fields also could not uniformly declare a collection contract with its own inner capability. In addition, the syntax required a `thing` body even when it was empty.

## Decision

### Nominal specialisation

Every alias may declare an unordered list of ancestors using `as`. The direct relation must be acyclic and its `is` closure is reflexive, transitive and antisymmetric. Written order introduces neither priority nor MRO.

A root nominal alias introduces its representation with `:= Type`. A descendant may omit it when the inherited representation is already unique and compatible, or declare `:= Type` to refine it or explicitly resolve several contributions. The local representation must refine all relevant inherited representations simultaneously. A union `A | B` does not by itself satisfy this obligation.

A declaration with ancestors may omit the local definition. `alias A` without ancestors or a definition is invalid.

### Inherited structural form

Structural aliases inherit stored components and derived fields. The same original member reached through several paths is deduplicated by its anchor. Equivalent independent contributions with the same name may be merged; if their contracts differ, the descendant must resolve them explicitly with a contract that refines all inherited ones. There is no priority based on `as` order.

A descendant may override the default of an inherited stored component and refine its contract, because alias values are externally immutable, provided that the new contract refines all inherited contributions. Derived fields from a single source retain their defining expression and may refine their contract. If two independent derived fields with the same name provide different expressions, the descendant must provide a new explicit derived definition whose contract satisfies all contributions.

Members belong to the alias's nominal type. A bare structure does not obtain them through structural matching; it must acquire the alias through context or `to`.

### Derived fields and collections

A structural alias may declare derived fields with `:=`. They are pure, unstored and not assignable. The explicit nominal or structural type is checked statically. Domain, cardinality, uniqueness and order declared in the derived form, whether or not an explicit type exists, are coercive over the result and follow local-transformation normalisation. `[mut]` acts as a capability requirement on immediate `thing` members: it may retain source authority when semantic identity is preserved, but cannot manufacture it.

Selection remains fixed during an evaluation snapshot. After effects are consolidated, the view is recomputed over the new state and its contracts are validated; a violation produces `failed` and rollback. A stored collection does not self-prune or recompute its membership.

### Empty `thing` bodies

A `thing` body may be omitted when it contains no members. `thing A`, `thing A {}` and `thing A;` produce the same AST and IR, although the CST retains the written form.

## Alternatives

It is rejected to interpret ancestor order as priority, resolve multiple specialisation through a union, merge incompatible independent members by name alone, or manufacture inner capability through a derived coercion.

## Consequences

- The nominal graph includes specialisation edges between aliases.
- Elaboration computes effective representations and members before enabling nominal access.
- The CST, ASTs and syntax catalogues represent ancestors, optional definitions, derived fields and overrides.
- [[notes/questions/Q-056-f-normalised-form-and-alias-recursion|Q-056]] is limited to alias normalisation and recursion.

## Verification

1. Acceptance of simple and multiple specialisation, and rejection of cycles.
2. Inheritance of representation and explicit resolution through `:=` when contributions differ, requiring common refinement.
3. Diamond deduplication by origin, merging of equivalent independent contributions and explicit resolution of distinct contracts.
4. Inheritance of components and derived members, with default overrides, substitutable refinements and a new explicit definition when independent derived expressions collide.
5. Member access only after acquiring the nominal type.
6. Inner capability required and preserved by derived views without manufacturing authority, with stable membership during each snapshot.
7. Subsequent recomputation, contract validation and rollback on violation.
8. Semantic equivalence of the three empty `thing` forms.
