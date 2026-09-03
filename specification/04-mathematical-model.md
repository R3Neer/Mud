---
title: Model mathematician from world
aliases:
  - Model official version of the world MUD
tags:
  - mud/specification
  - mud/normativa
status: draft
normative: true
depends-on:
  - "[[02-terminology]]"
  - "[[03-notation]]"
questions:
  - Q-005
  - Q-046
  - Q-047
decisions:
  - D-014
  - D-015
  - D-054
  - D-017
  - D-025
  - D-019
  - D-026
  - D-021
  - D-055
  - D-068
  - D-077
  - D-085
  - D-086
  - D-087
  - D-096
  - D-099
  - D-103
---

# 04. Model mathematician from world

## State and purpose

This chapter defines the mathematical constraints already established for representing a programme and an state of the world MUD before introducing its concrete syntax or its execution. The complete mathematical structure of the world remains under development and must extend these constraints without contradicting them.

## Sub-units

- [[02-terminology|Terminology]].
- [[03-notation|Mathematical notation and metalanguage]].

## Planned content

- Canonical programme definitions and active identities in each world.
- Initial set `start with`, creation, destruction and reactivation.
- Identity from `thing`.
- Relation specialisation `is`.
- Fields and relationships store.
- Stored information and effective projection.
- Suspension transitive via hard dependencies.
- Identity versus structural equality.
- Well-established states.
- Stable and tentative states.
- Semantically visible comments.
- Isolated and disposable worlds from the tests.

## Restriction on model

MUD does not presuppose a distinction between classes and objects. In particular, an `thing` has no instances. The mathematical model must represent, within a single conceptual domain, both the canonical definitions of the programme and the active identities in each world, without converting them into classes and instances.


## Confirmed restrictions

The model current stipulates:

1.  Every `thing` has identity semantics.
2. Every specific `thing` denotes a specific thing with its own state and may be ancestor from others.
3. An abstract `thing` belongs to the same domain, but does not directly denote a specific thing with its own state.
4. Each `thing` has a single top-level canonical definition, which determines whether it is abstract or concrete, its direct predecessors and its body.
5. The relation semantics `is` is reflexive and transitive.
6. Direct specialisation is acyclic, so `is` is also antisymmetric and forms a partial order.
7. Declarations, constraints, domains and effective defaults are inherited, but not state active mutable variables.
8. Each specific `thing` has its own state.
9. `create Nombre` only activates a single `thing` or defined rule; it does not support categories, predecessors or the body.
10. If a canonical `thing` does not have an active materialisation, `create` instantiates that same identity and descriptor. Following a previous `destroy`, the new materialisation reconstructs the schema from the canonical definition and reapplies defaults and initialisers; it does not restore the own stored data or the runtime structural modifications of the destroyed materialisation.
11. Every well-formed type has an default value belonging to its domain, unless a decision expressly excludes it. `Any` has no universal default, and an stored field of type type `Any` must have an initialiser.
12. `as` introduces direct specialisation; `is` query its reflexive and transitive closure; `iis` and `iis not` exclusively refer to or exclude the specified nominal effect type.
13. A rule containing `create A` is only executed if canonical identity `A` is absent.
14. Every field denotes a collection; its outer mutability and the capacity over its members are orthogonal permissions even with cardinality `[1]`.
15.  A collection of `thing` always requires strict membership: $c\neq T\land c\ \mathsf{is}\ T$. There is no `reflexive`.
16. `destroy` only commits a withdrawal if all the resulting cardinalities and domains are valid; otherwise, it produces `failed` and a rollback.
17.  A declaration with an inactive hard dependency is suspended entirely; its fields and participants are not partially rewritten, and that derived suspension does not clear its own stored payload. Only a `destroy` directed at the declaration itself terminates its materialisation runtime in accordance with the current cycle lifetime rules.
18. `remove` on a property removes its declaration and load stored within the current materialisation. A suspension via an inactive dependency, on the other hand, retains the property and its payload; destroying the owning `thing` terminates all its materialisations, and a future materialisation restarts from the canonical definition.
19. Each module may contribute at most one `start with`; their finite, unordered contributions are combined into a single surface of activatable statements `thing | rule`, and the contributions of all modules are materialised jointly prior to the initial stabilisation.
20. Each contribution is a static expression that produces either an activatable declaration or a flat collection; it does not support instructions, effects or nested collections.
21. If a module omits `start with`, its contribution is empty. `Thing` remains in effect at all times and forms no part of the activatable collection nor of the enumeration materialised by `all Thing`.
22. Each test constructs a fresh, isolated world; before the test root, the static transitive closure of reachable tests is computed and their contributions are combined in `start with`.
23. Tests are not executable statements, nor do they form part of world or the host’s public API; their visibility between modules exists solely in the context of tests.
24. The world constructed for a test and all its outputs are discarded upon completion of its execution.
25. `Thing` is an embedded abstract `thing`, which is always effective and takes precedence over any `thing` via `is`.
26. A root without an `as` retains zero declared predecessors and receives an implicit semantic edge towards `Thing`.
27. `Thing` has no specific state nor a cycle whose lifespan can be controlled by the programme.
28. The declarations and values supported by presentation specify typed postfix metadata; `~name` has type `Name`, whilst `~path`, `~anchor` and `~file` describe provenance and identity.
29.  The default value of `~name` is derived from the unqualified nominal identifier when the category defines it. It can be configured using the declaration or by editing the model, but no `~` access may be the target of a runtime assignment or update; metadata is not inherited.
30. The identity, the effective nominal type, the path and the anchor do not depend on `~name`; multiple entities may share the same presentation. All access to `~` is read-only during execution; `~path`, `~anchor` and `~file` are also intrinsic properties and not configurable metadata.
31. An immutable relation retains a withdrawn identity in a latent state and can restore that membership when `create` re-materialises the same identity; a relation `mut` removes that stored affiliation.
32.  No confirmed state contains a collection whose effective cardinality contradicts its declaration.
33. Destroying a specific `thing` discards the stored values and runtime structural modifications belonging to its current materialisation, but does not clear loads belonging to other declarations that are merely suspended because they depend on its identity or type.
34. Explicitly destroying a reactive rule clears the temporary memory of that activation. A subsequent activation establishes a new baseline without triggering it merely by reactivation; the policy memory for suspensions or disappearances of bindings not caused by `destroy` remains open in Q-005.

Examples of confirmed distinctions:

```mud
thing Alexandria as City {
    ~name = "Alejandría"
}

start with {
    Alexandria,
    empty
}

rule ExactIdentifier given value: Identifier {
    value iis PersonId
}
```

`Alexandria is City` query specialisation, `value iis PersonId` requires exact effective nominal type and `Alexandria == Alexandria` compares identity with value. None of these relationships depends on `Alexandria~name`.


## Open questions

> [!question] Q-046 — Invalid creation
> Determine the result for actions and blocks with multiple creations. For a rule with a single creation, it has already been decided that the entire rule is not executed if the identity is active.

> [!question] Q-047 — Specific defaults
>  Determine the default value for each type constructor and its behaviour when the domain depends on the world.

## Nominal aliases

Aliases form a second nominal partial order. Their nodes are types of value, not activatable identities. Direct specialisation is acyclic, and its closure `is` is reflexive, transitive and antisymmetric.

For an nominal alias with several predecessors, the set of values of the descendant must be contained within the intersection of the sets of values of all of them. The union `A | B` does not satisfy this requirement. For structural aliases, the effective form is obtained by aggregating members by origin: a single member inherited via multiple paths is deduplicated, and independent members with the same name produce conflict.

Derived fields denote recalculated collections. Their membership is determined during an snapshot evaluation and is recalculated based on the subsequent consolidated state. The internal capacity `[mut]` may form part of its contract, but does not create authority: it must be guaranteed by the source value and preserved through transformations that maintain the identity semantics of the member `thing`s. This capability applies only to immediate members and does not make derived membership or nested collections writable. Stored collections, on the other hand, retain their membership until an explicit structural modification is made.
