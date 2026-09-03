---
id: D-036
title: "Participants, recipients and calls"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-011"
  - "Q-012"
  - "Q-013"
affects:
  - "futuro `07-concrete-grammar.md`, futuro `19-expresiones.md`, futuros capítulos 21 a 24"
---
# ADR-036 — Participants, recipients and calls

- Amended by: [[ADR-101-bloques-de-valor-variables-locales-almacenadas-and-extremos-por-testigos|D-101]].

- Amended by: [[notes/decisions/ADR-068-universal-thing-and-intrinsic-name|D-068]]

- Read more: [[notes/decisions/ADR-025-vocabulary-from-thing-headings-and-sections|D-025]]
- Amended by: [[notes/decisions/ADR-063-signatures-given-and-joint-on-bindings|D-063]]
- Amended by: [[ADR-087-metadatos-reflectivos-descriptores-estables-and-visibilidad-exterior|D-087]]
- Amended by: [[notes/decisions/ADR-096-modulos-callables-look-message-and-activation|D-096]]
- Related questions: Q-011, Q-012, Q-013
- Documents affected: future `07-concrete-grammar.md`, future `19-expresiones.md`, forthcoming episodes 21 to 24

## Decisión

### Participants and `given`

A participant occupies a semantic role filled by one or more values. It determines the subjects of the operation and, where the role has capabilities, access to state or a place to write.

A `given` is a value provided as an auxiliary parameter; it has no semantic role, although its type it might also appear in `for`.

Everything `given` has a mandatory name, is read-only and does not allow mutability external or internal capacity. You may declare a static closed default in accordance with D-063.

D-025 sets the headers:

- `on`: automatic links from a value by role for reactive rules, `always` y `message`; the direct form uses the implicit universe of `thing` active concrete forms and the related form `nombre[: Tipo] in fuente` retrieves values from a finite, countable source.
- `for`: individual or collective roles in any type declared, supplied to Boolean rules, actions and `look`.
- `given`: auxiliary values for Boolean rules, actions, sub-actions and `look`.

Reactive rules, `always` y `message` do not allow `given`. A `look` it does allow `given` in accordance with D-096.

### Cardinality and names

A role `for` accepts any `declared-type`, including basic types, aliases, families, dictionaries and `thing`, a domain `in` and the specification full list of collection. The domain restricts the permissible values for the role and is entered between the type and the specification from collection. The cardinality omitted is equivalent to `[1]` in accordance with D-039. A role `on` links a single value by association and does not allow cardinality nor the modifiers for collection `unique` u `ordered`: the direct form without `in` uses the implicit universe of `thing` active concrete forms; the related form `nombre[: Tipo] in fuente` may take elements from a finite, countable set in accordance with D-096.

The type incorporated `Thing` accepts any `thing`. Therefore, a role `for` from type `Thing` accepts any identity specific, compatible and `on Thing` lists all the `thing` concrete and active; the root In the abstract, it does not create a connection of its own.

Everything participant `for`, `on` y `given` You must declare an explicit source identifier. The cardinality `[1]` It does not create an anonymous exception. The members are accessed via that identifier and are not implicitly projected onto the scope of the body.

```mud
rule IsDestroyed for army: Army {
    army.soldiers == 0
}

rule CanGovern for person: Person, kingdom: Kingdom {
    person.age >= 18 and kingdom.treasury > 0
}
```

The identifier forms part of the signature slot and, in accordance with D-087, takes part alongside the clause class in its anchor subordinate. Reordering participants does not change that identity. A collection it still does not implicitly project the fields of its members.

Values without identity runtime:

```mud
rule IsWeekend for day: Day {
    day == Saturday or day == Sunday
}
```

### Mutability of participants `for`

In a action, `mut` before the name of any role `for`, including one from cardinality `[1]`, grants mutability external on the collection supplied. That role must always have a name. The receiver The corresponding item must be an externally stored, mutable object. It may be state from the world or a declared local slot `mut`; a literal, a calculated move `:=` or a stored immutable local variable are not compatible writable locations and are rejected.

The `mut` included in the specification from collection provides an inner understanding of values member who possess state editable. Type it when the type An array that contains only immutable values is valid, but it raises a warning because the permission It is pointless. Both permissions are orthogonal in accordance with D-019:

| Declaration | Change collection | Edit members |
| --- | --- | --- |
| `patients: Person [*]` | No | No |
| `mut patients: Person [*]` | Yes | No |
| `patients: Person [* mut]` | No | Yes |
| `mut patients: Person [* mut]` | Yes | Yes |

Boolean rules and `look` do not allow `mut` outside because they are pure. The participants `on` nor do they admit it: their `[mut]` The optional feature relates exclusively to the interior capacity of the `thing` related individual. The `given` do not allow any form of `mut`.

The mutability The organisation does not require its members to be `thing`: changes the location containing the collection, not the fixed values they contain. For example:

```mud
action Record for mut observations: Num [*]
given value: Num {
    then add value to observations
}
```

### Types of employment

The linking method depends on the contract from the role:

| Role | Mode |
| --- | --- |
| `thing` without `mut` outdoor | identity of each `thing` |
| basic, alias, `family`, dictionary or other value unchangeable | value |
| any type with `mut` outdoor | identity time of the stored location and value current; the place may belong to the world or to a local frame |

One collection it also retains cardinality, multiplicity and order. To repeat a value or a identity produces as many ideas as the contract unless the role is `unique`.

### Several participants

Several participants declare ordered roles. The order forms part of the API semantics:

```mud
rule CanAttack for
    attacker: Army,
    defender: Army
{
    ...
}
```

Automatically linked participants can use `in`:

```mud
rule ApplyStarvation on
    world: World,
    kingdom in world.kingdoms [mut]
{
    ...
}
```

The entry may be kept in front of `in` to refine the element nominally:

```mud
rule MutualFriends on
    alice: Person in bob.friends,
    bob in alice.friends
{
    ...
}
```

The names are visible across the entire header and their restrictions are resolved collectively, not from left to right. Each role is assigned its own universe according to its form: the implicit universe of `thing` specific actions to `on` directly or the members of the countably finite set for `on ... in fuente`. The set of relationships is the finite join that satisfies all membership conditions on a single snapshot. An ambiguous type solution requires additional annotations. Relational cycles are not fixed points and read a single snapshot, in accordance with D-063.

Role assignments retain orientation and allow two roles to be assigned the same value when both contracts are fulfilled and symmetrical pairs are not automatically deduplicated. In participants supplied via `for`, additional relational constraints are expressed using types or conditions.

### Identity exact and selection by type

A qualified reference written in the body of the document (without a header listing the participants) refers to the canonical identity exact:

```mud
rule AdvanceCalendar {
    when World.day changes
    then World.date += 1 day
}
```

Here `World` does not mean ‘all’ `thing` whatever the case may be `World`", but the only one identity `World`.

On the other hand, a participant individual `on World` o `for World` select `thing` active concrete projects whose type meets `is World`. Each member `thing` of a role `for` The group undergoes the same selection process. The selection is a deliberate one: it includes the identity exact `World` when it is concrete and active, in addition to its active specialisations. A `thing` ‘abstract’ does not in itself provide a specific link, although its specialisations may do so. This selection rule does not apply to roles of value.

To deliberately exclude the identity root A role must be declared and the condition must be specified:

```mud
rule DescendantOnly for world: World {
    world != World and ...
}
```

Selection by type It never replaces an exact nominal reference written outside a heading.

### Recipients and arguments

Recipients connect participants; storylines connect `given`.

```mud
army.IsDestroyed()
game.InCheck(White)
(attacker, defender).CanAttack()
(source, destination).Transfer(amount)
```

The standard enrolment of participants and `given` It may be positional. Reorder the declaration changes the canonical order of the API.

The separation does not depend on the type. A value is `for` when it constitutes a semantic subject of the declaration y `given` when it merely sets the parameters for the operation:

```mud
action Record for mut observations: Num [*]
given value: Num {
    then add value to observations
}
```

An expression of collection holds a single position as receiver when the corresponding role is a group role; it is not propagated to multiple recipients. If the role declares mutability externally, the expression must be a compatible mutable location, and the binding retains that destination for the purposes of the action.

A receiver A multi-part form can use a named form:

```mud
(
    attacker = leftArmy,
    defender = rightArmy
).CanAttack()
```

You must name existing roles exactly once, be exhaustive, and provide compatible types. The names allow roles to be reordered in this construction of call; these should not be confused with the rule governing the order of named components in alias.

The specified form is valid in any order, but the compiler recommends the order of declaration. It cannot be combined with positional receptors.

The arguments `given` can actually be linked by name using `=` inside the brackets:

```mud
game.InCheck(color = White)
(source, destination).Transfer(amount = 10)
```

One call accepts positions, names or a prefix a positional term followed by names. A positional term cannot appear after the first name. The names may be reordered `given`, although the compiler suggests the order of declaration.

Static defaults allow omissions. In terms of position, only a complete suffix of `given` defaults; the names allow you to skip any intermediate defaults:

```mud
game.Search(origin, depth = 3)
game.Search(depth = 3)
```

If the firm states `origin = Capital`, `depth` y `exhaustive = false` In that order, both calls are valid. This, however, would not be:

```mud
game.Search(depth = 3, origin)
```

because a position cannot appear after the first argument appointed.

### Nature of the call

One call A rule does not create a general function. A request or composition of action nor does it allow arbitrary code to be executed. Both create a link semantics verifiable towards a declaration well-known.

## Consequences

- AST and IR separate argument receivers.
- Everything participant has a name and anchor stable subordinate in accordance with D-087.
- A collective role preserves cardinality, modifiers of collection and both capacity axes in AST and IR.
- An externally mutable connection preserves the location receiver, not just its value.
- The IR distinguishes between role-based relationships by identity, by value and by location.
- D-025 and this one decision resolve Q-011 for nominated participants.
- The compiler can reconstruct reads, writes and dependencies from the signature.

## Future verification

1. Participants `for`, `on` y `given` always named, and a rejection of anonymity.
2. Access for members only via the participant.
3. Receiver a positional, named multi-part entity.
4. Role missing, duplicated, unknown or misspelt.
5. Arguments `given` positional, appointed and with prefix positional followed by nouns.
6. Omission of final defaults by position and intermediate defaults by name.
7. Distance between participants and `given`.
8. Engagement `on` related, refined, advanced and cyclical through `in`.
9. Rejection of incompatible headers.
10. Difference between the exact reference `World` and a participant `on World` o `for World`.
11. Reflexivity for a root specific and the absence of a direct link to a root abstract.
12. Role `for` group with domain, cardinality and each modifier for collection.
13. A name is required for all cardinality, including `[1]`, and for mutability outdoors.
14. Receiver a set occupying a single position, with no implicit extension.
15. The four combinations of mutability exterior and interior.
16. Acceptance of a mutable placeholder and rejection of literals or calculated expressions for `mut nombre`.
17. Rejection of collections in `on` and from mutability exterior in minimalist buildings.
18. Roles `for` basic, alias, `family`, dictionary and `thing`.
19. Link via identity, value and place.
20. A suggestion regarding an demonstrably useless internal capacity relating to immutable values.
21. Difference between a value subject `for` and a value auxiliary `given` of the same type.
22. Rejection of mutability exterior and interior in `given`.
23. Preservation of symmetrical orientations and reflexive roles in `on`.

## Amendment current by D-096

A `look` supports `given` in accordance with the general rules for binding and defaults. Declarations governed by `on` are still not `given` and, when used as triggers, they are referenced without `()`. Stored callable values are invoked using the standard method of receivers and arguments; storing the descriptor does not pre-assign roles or `given`.

Furthermore, a participant related `on nombre: Tipo in fuente` It can map values from a finite, countable source, not just identities `thing`. The direct form without a source remains reserved for the implicit universe of `thing`; therefore `on n: Nat` without a finite source is invalid.

