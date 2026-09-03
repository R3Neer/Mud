---
id: D-038
title: "Close-knit families with strong values"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-024"
  - "Q-047"
  - "Q-061"
affects:
  - "futuro `13-familias-cerradas.md`"
---
# ADR-038 — Close-knit families with strong values

- Amended by: [[ADR-102-forma-completa-de-datos-calculados-de-family|D-102]].
- Amended by: [[ADR-101-bloques-de-valor-variables-locales-y-extremos|D-101]].

- Amended by: [[ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].

- Expanded by: [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]]
- Amended by: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]], [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]] y [[ADR-091-datos-de-family-como-descriptores-anclados|D-091]]
- Amended by: [[notes/decisions/ADR-064-orden-por-ruta-estable|D-064]]
- As further amended by: [[notes/decisions/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]]
- Amended by: [[notes/decisions/ADR-061-resultados-fallidos-y-plantillas-text|D-061]]
- Related question: Q-024
- Documents affected: future `13-familias-cerradas.md`

## Decisión

The MUD admits `family` such as declaration top-level domain independent of `thing`:

```mud
family Color {
    Red,
    Green,
    Blue
}
```

`ordered` is a reserved word which, situated immediately before `family`, adds semantic structure:

```mud
ordered family Severity {
    Low,
    Medium,
    High,
    Critical
}
```

The declaration enter a type finite nominal and a anchor static `family::*`. Each member:

- It belongs, in name, to his family.
- It is a value nominal, not one identity from `thing`.
- It lacks state changeable and cycle runtime.
- Does not support `create`, `destroy`, `as` or enquiries `is`.
- It is listed in the order of declaration.
- It’s the same as another one member if, and only if, both belong to the same nominal family and have the same name.
- It only supports order operators if the declaration use `ordered family`.

Every member has the metadata standard `~name: Name`, whose default value is derived from its name identifier. It can be configured via `~name = "..."` without changing identity, equality, anchor or order. A configuration identical to the default is flagged for deletion. In a template `Text`, interpolate a member generates the textual representation of its `~name` cash.

The order of declaration It is standard practice to list any `family`, but it’s only one aspect of relationships `<`, `<=`, `>` y `>=` when it appears `ordered`.

The statements `family` do not specialise, nor can they inherit from other families. An open hierarchy of `thing` abstract subjects and specialisms are not a closed family and does not acquire enumerability automatic.

### Related data

One `family` You can declare a uniform schema of immutable data. The schema declarations appear directly within the family block, before the members, without a sub-block `data`:

```mud
family Terrain {
    movementCost: Nat = 1
    passable: Bool = true
    costly := movementCost >= 3

    Plain,
    Forest {
        movementCost = 2
    },
    Mountain {
        movementCost = 4
    },
    Water {
        movementCost = 0
        passable = false
    }
}
```

An associated data item may be stored or calculated. Stored data does not support `mut`:

```text
nombre : tipo [in dominio] [especificación-de-colección] [= value-body] [metadata-body]
```

The calculated figure uses the full form of computed field:

```text
nombre [forma-derivada] := value-body
```

`forma-derivada` is the `derived-value-shape` ordinary of D-037: you can set a type, declare a domain shaped like collection optional, or declare a form of collection. The entry for type is optional; if omitted, the compiler must infer a single type static. The calculated value does not allow for `mut` external, pre-stored or self-hosted storage. Domain, cardinality, `unique` and commands written in the derived form reuse the constraints of D-037, and no form can create capacity `[mut]` nor any other authority absent from the result of origin. D-091 allows both stored and calculated data to have an immediate body consisting solely of metadata declarations `~...`, belonging to the descriptor data standardisation.

All members follow exactly this pattern. The optional sub-block of a member contains only assignments that replace the default values of stored data; it cannot declare new data, omit the name of the assigned data, or modify its type, domain o specification from collection nor assign a calculated value.

For each piece of data in each member, the value It is obtained in the following order:

1. Explicit assignment in the sub-block of the member.
2. Explicit default for the declaration of the data.
3. Default setting for the type cash in accordance with D-017.

Therefore, a member you may omit a stored value provided that its default value can be determined statically. In particular, a piece of data `Nat` if no explicit default is specified, it returns `0`. Even if the omission is valid, it is recommended that values whose meaning is important for understanding the model.

After processing the stored data from a member, its calculated data is evaluated for that member. The expression may use unqualified names to access other associated data from the same family, including calculated data declared before or after. Dependencies between calculated data must be acyclic and resolved without relying on the textual order of declaration. The defaults and assignments of member can use `ValueBlock`, but the entire body must be capable of being assessed statically in accordance with D-066 y D-101. The calculated data is also evaluated statically by member and they must be of high quality, as well as meeting the specifications and, where applicable, the domain and the collection.

In the example, `Mountain.costly` is `true`, whilst `Plain.costly` is `false`. The associated values obtained for a member, stored or calculated:

- They are unchangeable.
- They do not have identity nor cycle own runtime values: these are actual values of the descriptor uniform, no separate statements by member.
- They are queried as properties of the value family-related, for example `terrain.movementCost`.
- They do not alter the identity nor the equality of the member: they still depend on the nominal family and the name of the member.

The declaration the data itself is an entity semantics stable version of the scheme `family`: has descriptor `Field`, anchor subordinate and its own metadata in accordance with D-091. An allocation of member just replace the value it uses data that is already stored and does not create a second entity.

### Associated data as a key for collection

One collection of members of a `ordered family` you can use `ordered by ruta`. The path part of each member and select a stable associated value:

```mud
ordered family Terrain {
    movementCost: Nat = 1

    Plain,
    Forest {
        movementCost = 2
    },
    Mountain {
        movementCost = 4
    }
}

route: Terrain [* ordered by movementCost]
```

Within `ordered by movementCost`, `movementCost` refers to the data from the member from `Terrain` which is being sorted out. The result must have a complete semantic structure. The data for a family is immutable, so this path is stable. A formula must first be declared as a calculated field and then sorted by its name; `ordered by` does not contain arbitrary expressions.

`ordered by` replaces the order of declaration as the main criterion for that collection, but it does not change the comparison operators specific to the family. When two occurrences produce the same key, they retain their relative order of provenance stable; in a purely sequential narrative, it corresponds to the order of insertion. Repeated occurrences retain their multiplicity unless the collection or `unique`.

The selection of the member The family’s default setting continues to belong to Q-047.

## Future verification

1. Closed family ordered and unordered.
2. Equality between values within the same family and between different families.
3. Canonical enumeration.
4. Rejection of order in a disorderly family.
5. Rejection of `create`, `destroy`, `as` e `is`.
6. Distinction with regard to an open hierarchy of `thing`.
7. Anchor formation and stability `family::*`.
8. A standardised data format and the rejection of specific, undeclared data.
9. Precedence between value from member, explicit default and default of type.
10. Immutability and access to associated data.
11. Collection from `ordered family` sorted by one path associated data, with ties due to provenance stability and preservation of multiplicity.
12. Inference from type, assessment by member and acyclic dependencies on computed data.
13. Rejection of allocations of member aimed at calculated data.
14. Rendering using `~name` of a member and explicit access to a piece of data `Text` alternative.

