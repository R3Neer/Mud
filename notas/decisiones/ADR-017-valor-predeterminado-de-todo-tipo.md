---
id: D-017
title: "Everything type well-built has default value"
status: vigente
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-047"
affects:
  - "futuro `10-sistema-de-tipos.md`, futuro `14-campos.md`"
---
# ADR-017 — Everything type well-built has default value

- Amended by: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Amended by: [[notas/decisiones/ADR-069-literales-char-con-comillas-dobles|D-069]]
- As further amended by: [[ADR-074-uniones-nominales-y-estrechamiento|D-074]]

- Related open-ended question: [[notas/preguntas/Q-047-seleccion-de-predeterminados-por-tipo|Q-047]]
- Documents affected: future `10-sistema-de-tipos.md`, future `14-campos.md`

## Context

MUD allows you to declare properties without always having to write an explicit initialiser. The semantics You need to determine your value initial without introducing an implicit absence or leaving any mandatory positions unfilled value.

## Decisión

Everything type well-built has a default value belonging to his domain semantic.

Be $\mathcal T_P$ the set of well-formed types of a solved programme, and let $\mathcal V_P$ its value space. There is a total function:

$$
\operatorname{default}_P:
\mathcal T_P
\to
\mathcal V_P
$$

such that:

$$
\forall\tau\in\mathcal T_P:
\operatorname{default}_P(\tau)
\in
\llbracket\tau\rrbracket_P
$$

Therefore, everything type If it is well-built, it is habitable:

$$
\forall\tau\in\mathcal T_P:
\llbracket\tau\rrbracket_P
\neq
\varnothing
$$

A construction of types whose domain if it were empty, it could not be accepted as type well-built.

## Cases already scheduled

The basic cases, updated by D-028, are:

| Type or family | Default value |
| --- | --- |
| `Bool` | `false` |
| `Nat` | `0` |
| `Int` | `0` |
| `Num` | `0` |
| `Rum` | `r0` |
| `Char` | `"\u{0}"` (`U+0000`) in context `Char` |
| `Text` | `""` |
| `Money` | `0` in context `Money` |
| Collections | `empty` |
| Dictionaries | `empty` |
| Intervals | `empty` |

These cases do not, on their own, resolve the issue of refined types that exclude the value database or collections whose cardinality the minimum is positive.

## Precedence during initialisation

For a stored property, the value The initial result is obtained in the following conceptual order:

1. The property’s effective explicit default value, if any.
2. Default value of his type in cash, otherwise.
3. Explicit assignment or initialisation upon creation, where the relevant syntax permits this.

The third phase replaces the value initial creation of that property; it does not, therefore, alter the default rules governing the inheritance of that property or those of the type.

D-038 apply the same precedence for each associated data item of a member from `family`: allocation of the member, the explicit default value for the data and the default value for its type.

D-031 Apply this composition to structural aliases: each component uses its explicit default or, if none exists, the default of its type cash. The default value from the alias contains all the components.

## Consequences

- A mandatory stored property may be initialised even if an explicit default value is omitted.
- Refinements, intervals, families, non-structural aliases, collections and types that depend on `thing` they must define how they extract a specific element from its domain.
- The validity check must ensure that the default value satisfies all the constraints of the type.
- Materialisers must reproduce the value from MUD rather than selecting the destination technology’s own default settings.

## Unresolved issues

Q-047 shall determine:

- The rule for non-structural aliases and restricted collections; the composition of structural aliases is determined by D-031.
- Selection within intervals, closed families and refinements.
- Dealing with people whose domain may depend on the world asset.
- If other types of type Derivatives can explicitly override their intrinsic default values.

## Future verification

The suite must verify:

1. Existence and membership of the domain from the default setting for each type Agreed.
2. Interest rate cut with domain empty.
3. Using the default type when a property does not declare another.
4. Priority of the explicit default property.
5. Final priority of an explicit creation initialisation.
6. Independence from the default settings of the implemented technology.
7. Composition of the default value for a structural alias based on its components.
8. Default `"\u{0}"` from `Char`.

