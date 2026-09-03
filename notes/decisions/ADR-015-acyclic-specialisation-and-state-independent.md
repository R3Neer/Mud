---
id: D-015
title: "Acyclic specialisation and state independent"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-042"
  - "Q-043"
affects:
  - "[[specification/04-mathematical-model]], futuro `11-things.md`"
---
# ADR-015 — Acyclic specialisation and state independent

- Amended by: [[notes/decisions/ADR-084-especializacion-de-aliases-miembros-heredados-and-vistas-derivadas|D-084]]
- Updated: 28 July 2026 to use the terminology from D-025
- Amended by: [[notes/decisions/ADR-068-universal-thing-and-intrinsic-name|D-068]]
- Questions: [[notes/questions/Q-042-e-specialisation-from-a-concrete-thing|Q-042]], [[notes/questions/Q-043-c-specialisation-cycles|Q-043]]
- Documents concerned: [[specification/04-mathematical-model]], future `11-things.md`

## Context

[[notes/decisions/ADR-014-unified-ontology-of-thing|ADR-014]] provides that every `thing` A concrete thing is simultaneously a thing with state its own and a possible ancestor. This makes it necessary to clarify:

1. If a descendant observes or copies the state current value of a ancestor specific.
2. If the relation Direct specialisation allows cycles between distinct identities.

## Decisión

### State independent

Specialisation entails:

- field declarations;
- restrictions;
- domains;
- effective default values;
- initiators of `thing` applicable;
- the other elements of the diagram that the specification expressly authorise.

It does not inherit, copy or observe the state current value of the ancestor.

Intrinsic property `name` nor is it inherited. It belongs to the descriptor premises of each identity and, if it is not overwritten, it is derived from its own nominal name.

Every `thing` specifically possesses state independent. Mutate a `thing` does not in itself alter the state of their descendants.

The canonical definition of a `thing`, whether concrete or abstract, may declare predecessors and initialisers:

```mud
thing N as BaseOne, BaseTwo {
    field = value
}

abstract thing A as BaseOne {
    field = value
}
```

The shape `field = value` does not declare a field. You should contact a stored field already provided by the legacy scheme. A single definition of `thing` You cannot declare a field and also initialise it using another statement `field = value`. The form `field: Type = value` it remains a single one declaration from field with a default value and does not count as a separate initialiser.

One `thing` abstract does not materialise own stored data, but their initialisers form part of the specialisation and may contribute to the first materialisation of a specific descendant. For the same field, an initialiser declared in a more specific descendant overrides the less specific inherited initialisers. If the same original initialiser reaches a descendant via several paths in a diamond, it is deduplicated by origin; independent and incomparable initialisers that compete for the same field produce conflict, with no priority based on the written order of `as`, in accordance with D-084.

When you first activate a `thing` specifically through `start with` o:

```mud
create N
```

the initialisation of $N$ It takes the effective defaults from its predecessors, incorporates the local declarations and then applies the effective initialisers. It does not take the active states from its predecessors. If there are no predecessors, fields without an explicit default use the default from its type. A reactivation preserves the stored charge in accordance with D-021.

Initialisers do not become declarations of field nor in schema defaults. That an initialiser of a `thing` The fact that an abstract class can be inherited as an initialisation argument does not alter the default inheritability of the field.

### Acyclic specialisation

The relation direct $R_{\mathrm{dir}}$ does not contain any cycles:

- does not support $(t,t)$;
- does not admit any non-empty path that begins and ends at the same point `thing`.

The relation:

$$
R_{\mathsf{is}}
:=
R_{\mathrm{dir}}^*
$$

is reflexive, transitive and antisymmetric. Therefore:

$$
t_1\mathrel{R_{\mathsf{is}}}t_2
\land
t_2\mathrel{R_{\mathsf{is}}}t_1
\Rightarrow
t_1=t_2.
$$

The reflexivity of `is` belongs to the closure and does not introduce loops in $R_{\mathrm{dir}}$.

## Options ruled out

- **A vibrant delegation to the state of the ancestor:** would cause non-local changes and complicate waves, rollbacks and explanation.
- **Copy of the state current when activated:** would mean that the same first activation depended on state someone else’s changeability.
- **Cycles:** would convert `is` in a pre-order and would prevent fields and default values from being set in a well-founded manner.

## Consequences

- The graph as defined by the canonical definitions, it must be acyclic.
- The IR separates the inheritable schema from state changeable.
- Initialisation calculates effective defaults before applying explicit assignments.
- Writing about a ancestor It does not impose any implicit obligations regarding their descendants.
- `is` affects substitutability and resolution schematic, does not propagate state.

## Example

```mud
thing Kingdom {
    mut treasury: Money = 0
}

thing Egypt as Kingdom {}
```

When it is switched on for the first time, `Egypt` starts with `treasury = 0`. A later text on `Kingdom.treasury` does not change `Egypt.treasury`.

```mud
thing France as Kingdom {
    treasury = 20
}
```

When it is activated for the first time, `France.treasury` OK `20`, but that allocation of a `thing` This specific constructor does not become the default constructor or an inheritable constructor for future descendants of `France`.

```mud
abstract thing RichKingdom as Kingdom {
    treasury = 20
}

thing Lydia as RichKingdom {}
```

`RichKingdom` It does not generate its own cash flow. Its initiator does, however, contribute to the first materialisation from `Lydia`, which begins with `treasury = 20`.

It is invalid to declare and initialise the same variable separately field in a single definition:

```mud
thing Broken as Kingdom {
    treasury: Money = 10
    treasury = 20
}
```

## Verification

1. Rejection of reflective edges and non-trivial cycles.
2. Non-cyclic multiple specialisation.
3. Antisymmetry of `is`.
4. Independence of states.
5. Initialisation using the current defaults.
6. Application of the effective initialisers in the first activation.
7. Inheritance of initialisers from `thing` abstract types and the absence of propagation from local initialisers of `thing` specific.
8. Refusal to declare a field and initialise it separately within the same one `thing`.
9. Deduplication by source and conflict no priority for abstract constructors inherited through multiple specialisation.

## Extension by D-084

Acyclicity and the policy The rules for unordered ancestors also apply to aliases. For inherited members, a diamond deduplicates the same origin. Equivalent independent contributions may be merged; distinct contracts require resolution an explicit solution that satisfies all branches, whilst the incompatible categories remain conflict. It does not exist in aliases state a mutable property to inherit.

