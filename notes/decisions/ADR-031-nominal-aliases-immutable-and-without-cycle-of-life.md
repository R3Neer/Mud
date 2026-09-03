---
id: D-031
title: "Nominal aliases, immutable and without cycle of life"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-057"
affects:
  - "futuro `12-aliases.md`, futuro `25-efectos.md`"
---
# ADR-031 — Nominal aliases, immutable and without cycle of life

- Amended by: [[notes/decisions/ADR-084-specialisation-de-aliases-inherited-members-and-derived-views|D-084]] y [[ADR-098-assignable-paths-and-write-back-of-immutable-aliases|D-098]]
- Expanded by: [[ADR-074-nominal-unions-and-type-narrowing|D-074]]

- Related to: [[notes/decisions/ADR-021-cycle-logical-lifespan-and-suspension-by-department|D-021]], [[notes/decisions/ADR-054-canonical-definitions-and-initial-activation|D-054]]
- Resolves: [[notes/questions/Q-057-c-inner-capability-within-alias-values|Q-057]]
- Documents affected: future `12-aliases.md`, future `25-efectos.md`

## Context

A alias must provide identity nominal value of securities, no identity runtime or state changeable. Therefore, its declaration it is static and does not take part in the cycle lifespan of the world.

## Decision

### Definition of type

A alias defined by an expression of type USA `:=`:

```mud
alias PlayerName :=
    Text

alias Board :=
    Square -> Piece [0..32 ordered]

alias Path :=
    Position [* ordered]
```

In this context, `:=` introduces a static definition of type. It does not declare a computed field nor a runtime evaluation.

A structural alias declares an ordered block of components:

```mud
alias Square {
    file: File
    rank: Rank
}

alias Pagination {
    page: Nat = 1
    size: Nat = 20
}
```

Each component:

1. It is an essential part of everything value built.
2. Take up a position semantics in the order of declaration.
3. It forms part of the structure of the alias.
4. You can declare a domain.
5. It cannot expose outer mutability: the form `mut name: type` does not exist for components.
6. It can accommodate indoor use `[mut]` on the `thing` contained directly by a collection.
7. You can declare a default value by means of `=`.

The explicit default must be a pure expression that can be evaluated statically and must satisfy the component's type, domain and collection specification. The default value of a structural alias is obtained component by component:

1. Explicit default for the component, if one exists.
2. Default for the type actual component in accordance with D-017, in another case.

The defaults do not remove any components from the representation. After constructing a value, everyone is present and takes part as normal, in a spirit of equality and order.

### Nominality

Everything alias enter a type New name. Two different aliases are not automatically interchangeable, even if their standardised representations match:

```mud
alias PlayerName :=
    Text

alias CityName :=
    Text
```

`PlayerName`, `CityName` and `Text` are three different types. Their common representation allows explicit nominal conversion in accordance with D-032, not implicit assignment.

### Immutability

A value from alias is unchangeable. A link that contains only that value It is unable to update one of its components:

```mud
square := Piece.square
square.file = B # invalid
```

An outer-mutable place can replace the complete value, and an assignable path may traverse stored alias components through reconstruction and write-back:

```mud
thing Piece {
    mut square: Square
}

Piece.square = (B, Four)
Piece.square.file = C
```

The second deed does not transfer the value `Square`: build another one `Square` of the same type exact nominal value, retains the unmodified components and replaces the value stored in `Piece.square`. The same reconstruction can propagate through nested aliases and exact dictionary indexing as long as there is a path back to a writable location. Derived fields are recalculated and are not write-back destinations.

The `mut` of the specification from collection A component’s internal capacity is determined by the `thing` contained directly by that collection. It does not make the collection nor does it, on its own, make a value from alias in a writable location: the reconstruction requires a root with mutability sufficient external capacity. Nor does capacity implicitly encompass another alias or nested container; each level required to grant it must expressly declare it when the operation being performed is ‘internal capacity’.

### Absence of identity runtime

The declaration has a anchor static for resolution and nominality, but their values do not possess identity runtime. A alias:

- It cannot appear as a target for `create`.
- It cannot appear as a target for `destroy`.
- That can’t be right `abstract`.
- Participates in acyclic nominal specialisation in accordance with D-084, without purchasing identity nor cycle runtime.
- It does not maintain state its own mutable variable.

The values are compared by type nominal value and content. The declaration It is present throughout the programme in its fully developed form and does not form part of the projected activity of the world.

## Consequences

- D-021 governs the cycle lifespan of `thing` and rules; aliases do not fall into these categories.
- D-054 requires top-level canonical definitions and reservations `create Nombre` to activate `thing` and rules; aliases are excluded from that cycle of life.
- The AST only needs `AliasDecl`; delete `DefineAndCreateAlias` and any effect `create`/`destroy` from alias.
- The runtime does not require activity markers, caching or restoration for aliases.
- Properties and declarations that use a alias cannot be suspended due to inactivity on the part of that alias.
- The immutability of the container alias is compatible with authority explicit instruction to modify the `thing` achieved through a collective component `[mut]`.

## Future verification

1. Alias simply by means of `:=`.
2. Alias from collection and using a dictionary `:=`.
3. Structural alias with components arranged in order.
4. Component with an explicit default and a default derived from its type.
5. Rejection of a default value that is impure, non-static, or outside its type, domain or collection specification.
6. Rejection of `mut` external and acceptance of `[mut]` internal aspect of a collective component of `thing`.
7. Rejection of a partial update regarding a branch alias and agreement to reconstruction/write-back when the path ends up in writable storage.
8. Complete replacement from a field mutable and preservation of unmodified components during a partial write-back.
9. Rejection of `create`, `destroy` and `abstract`; acceptance of `as` and `is` as nominal specialisation in accordance with D-084.

## Amended by D-084

Aliases may declare one or more specialisations. Root nominal forms retain `:= type`; descendants inherit a common effective representation. Structural types inherit components and derived fields. A descendant may override the default value of an inherited stored component and refine inherited contracts where that strengthens guarantees without removing observable or write capabilities. Outer mutability remains unchanged, while inner capability may be enhanced in the absence of `[mut]`; the presence of `[mut]`, type, domain, cardinality, `unique` and order remain governed by substitutability. Inherited derived fields retain their defining expression and may only strengthen the contract of their result. This amendment introduces neither runtime identity nor mutability to alias values.
