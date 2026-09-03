---
id: D-064
title: "Ordering by stable path"
status: current
date: 2026-07-30
supersedes: []
superseded-by: []
questions: []
affects:
  - "collections, families, aliases, fields, orderable types, normalisation and iteration"
---
# ADR-064 — Ordering by stable path

- Extended by: [[ADR-081-filtrado-take-and-indexacion-de-colecciones|D-081]]
- Amended by: [[ADR-100-orden-logico-procedencia-pertenencia-and-consolidacion-de-efectos|D-100]].

- Amends: [[notes/decisions/ADR-038-close-knit-families-with-strong-values|D-038]], [[notes/decisions/ADR-039-collections-and-dictionaries|D-039]] and [[notes/decisions/ADR-057-concrete-grammar-precedence-and-continuation|D-057]]
- Affected documents: collections, families, aliases, fields, orderable types, normalisation and iteration

## Context

`ordered by expression` allowed an arbitrary expression as the key. That freedom made it difficult to:

- Explain the criterion as a property of the world.
- Guarantee that the key remained stable.
- Reconstruct and compare ordering criteria.
- Avoid equivalent calculations written in different ways.

MUD favours rules that name the world's concepts. If a criterion requires a calculation, that calculation must first be declared as a field or computed datum, and the collection is then ordered by that name.

## Decision

### Key form

`ordered by` accepts only a non-empty path of fields, components or associated data:

```mud
route: Terrain [* ordered by movementCost]
teams: Team [* ordered by captain.age]
```

It accepts no operators, calls, literals, quantifiers or other arbitrary expressions.

Each intermediate access must be singular and resolve unambiguously on the preceding element. The path is interpreted from each collection member.

When the natural criterion is a formula, it is given a name:

```mud
priority := baseValue * rarityWeight
cards: Card [* ordered by priority]
```

In this example, `baseValue` and `rarityWeight` must be transitively immutable.

### Orderable type

The path's final result must have a total semantic order. A `thing` has no such order by itself and cannot be the final key:

```mud
players: Player [* ordered by team]       # invalid if team is a thing
players: Player [* ordered by team.name]  # may be valid
```

Basic types, magnitudes, ordered families and aliases are keys only when their type rules grant them a total order. The mere existence of `<` or `>` in another context does not automatically make a valid key.

### Stability

The entire path must remain stable throughout the collection's lifetime:

- No consulted stored field may be externally mutable.
- A field or computed datum is valid only if all its transitive dependencies are stable.
- An intermediate singular reference to a `thing` is not sufficient merely because it is immutable if a later field can change.
- No read may depend on randomness, changing activity or state whose variation alters the key.

The check is transitive. If stability cannot be demonstrated, the collection is invalid.

When the member is a union, the path must exist and remain singular and stable for every reachable alternative. Final keys must elaborate to one common type with a total order through at most one implicit widening. Representational coincidence between nominal aliases is insufficient. If an alternative requires adaptation, declare a common computed field and order by it.

### Ties

Two occurrences with the same key retain their stable provenance order. For causally sequential insertions this is the insertion order; when insertions are concurrent, provenance is completed reproducibly in accordance with D-100. Key normalisation does not introduce a nominal, identity, anchor or `family` declaration-order tie-breaker.

Repeated occurrences of the same value remain contiguous when the key gives that result and retain their multiplicity unless `unique` is used.

The complete criterion of two `ordered` collections is compatible only when they use the same resolved path and the same order for the final type. Relative tie stability is part of occurrence provenance, not the path's syntactic identity.

### Absences and custom orders

A path crossing optional cardinality is invalid until MUD defines a semantic position for `empty` in that access class.

MUD 1.0 provides no custom comparison declarations or ordering expressions. Nor does it infer a comparison between `thing` values. This decision adds neither multiple keys nor a tie-break clause: ties use stable provenance.

## Consequences

- The AST retains a resolved path, not a general expression.
- The IR records each path component, the final type and the stability proof.
- Renaming the calculation that defines a key requires updating the path, but concentrates the formula's semantics in an explainable field.
- State changes never implicitly reorder a stored collection.
- Stable provenance remains observable as relative order among equal keys or as the order of an `ordered` collection without a canonical key; in non-concurrent sequences it matches insertion order.

## Verification

1. Simple path over `family` data.
2. Nested singular path.
3. Rejection of a direct arithmetic expression and acceptance of the equivalent computed field.
4. Rejection of a `thing` as the final key.
5. Final key of a basic type, magnitude, ordered family and lexicographic alias.
6. Rejection of a directly mutable field.
7. Rejection of a transitively mutable dependency or unstable intermediate access.
8. Rejection of an optional path without an ordering for `empty`.
9. Preservation of stable provenance order among ties, including concurrency.
10. Compatibility and incompatibility between resolved paths.
