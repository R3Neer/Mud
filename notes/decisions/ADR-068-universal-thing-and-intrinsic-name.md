---
id: D-068
title: "Universal `Thing` and intrinsic name"
status: current
date: 2026-08-02
supersedes: []
superseded-by: []
questions:
  - "Q-041"
  - "Q-047"
affects:
  - "thing ontology, specialisation, built-in types, thing bodies, Text representation and tools"
---
# ADR-068 — Universal `Thing` and intrinsic name

- Amended by: [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]], [[ADR-086-exact-nominal-identity-external-arrows-and-dictionary-algebra|D-086]], [[notes/decisions/ADR-084-alias-specialisation-inherited-members-and-derived-views|D-084]] and [[ADR-073-explicit-but-redundant-as-thing|D-073]]
- Amends: [[notes/decisions/ADR-014-unified-ontology-of-thing|D-014]], [[notes/decisions/ADR-015-acyclic-specialisation-and-state-independent|D-015]], [[notes/decisions/ADR-018-as-declares-specialisation-in-is-the-query|D-018]], [[notes/decisions/ADR-035-organisation-names-using-and-anchors|D-035]], [[notes/decisions/ADR-036-participants-recipients-and-calls|D-036]], [[notes/decisions/ADR-037-fields-and-declarative-domains|D-037]], [[notes/decisions/ADR-054-canonical-definitions-and-initial-activation|D-054]] and [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]]
- Related question: [[notes/questions/Q-041-o-thing-ontology|Q-041]]
- Related pending question: [[notes/questions/Q-047-s-selection-of-defaults-by-type|Q-047]]
- Affected documents: `thing` ontology, specialisation, built-in types, `thing` bodies, `Text` representation and tools

## Context

MUD needs operations that accept any `thing`, heterogeneous collections and a common identity type without a declared shared ancestor. Letting each programme declare its own root does not ensure independent modules share it or let tools recognise the contract universally.

Interpolating a `thing` currently uses its nominal name. That value is stable for identity and resolution, but a game may need a different human presentation without renaming anchors or adding a repeated mutable field to every declaration.

## Decision

### `Thing` supertype

`Thing` is a distinguished, always-effective built-in abstract `thing`. It belongs to the same conceptual domain as other `thing` values, but has no source body, concrete state or programme-controlled lifecycle.

- Every `thing` satisfies `is Thing`.
- A `thing` without an `as` clause retains zero declared ancestors and receives an implicit semantic edge to `Thing`.
- A `thing` with declared ancestors reaches `Thing` transitively.
- `Thing is Thing` by reflexivity.
- `Thing` cannot be declared, redefined, activated or destroyed. D-073 permits writing it explicitly in `as`, but the form is redundant and receives a removal suggestion.
- `Thing` may be used as the type of fields, roles, arguments, collections and other compatible type positions.
- `on Thing` selects all concrete active `thing` values; the abstract `Thing` identity is not itself a binding.

`Thing` is a case-sensitive reserved word and built-in type. The effective edge is neither duplicated nor serialised as an additional semantic ancestor when the author writes redundant `as Thing`; CST and superficial AST retain that spelling until the suggested correction is applied.

Its canonical anchor is `thing::Thing`; `Thing~anchor` produces that reflective value. The anchor belongs to the language and is not a path declarable by a programme.

This decision does not select a default member for positive-minimum cardinality positions typed `Thing`. `Thing` is abstract and membership remains strict; Q-047 remains pending on when an explicit initialiser or other valid selection is required.

### Standard `~name` metadata

D-087 removes the special `.name` property and contextual assignment `name = ...`. Every `thing` exposes standard metadata `~name: Name`. If not configured, it is derived from the unqualified source identifier; it may be configured at the start of the body using the general metadata grammar:

```mud
thing BlackCastle {
    ~name = "The Black Castle"
}
```

`~name` belongs to the descriptor and every `~` access is runtime read-only. It is not inherited as presentation: a descendant without its own setting derives its name from its own `~identifier`. Two `thing` values may share a presentation without sharing identity. An ordinary `name` member may coexist with `~name`.

## Consequences

- Every `thing` and heterogeneous collection has a guaranteed common type.
- The graph distinguishes declared ancestors from the implicit edge from roots to `Thing`.
- Human presentation can change without altering identity, MUD path or anchor.
- `~name` introduces no inherited state, merge conflicts or runtime writes.
- An ordinary `name` member may coexist with `~name` because `.` and `~` occupy different namespaces.

## Verification

1. `T is Thing` for every declared `thing`, and `Thing is Thing`.
2. Rejection of declaration, `create` and `destroy` of `Thing`; non-blocking acceptance of `as Thing` with a removal suggestion.
3. Built-in anchor `thing::Thing` and reflective reading through `Thing~anchor`.
4. `on Thing` and `for` roles typed `Thing` over any concrete active `thing`.
5. `Thing [*]` collection containing identities from unrelated branches.
6. Default `name` equal to the unqualified nominal name.
7. Override using one interpolation-free `Text` literal.
8. Rejection of redeclaration, mutability, computation, runtime writing and interpolation in the override.
9. No inheritance of an overridden `name`.
10. `{value~name}` uses configured presentation and `{value~anchor}` retains canonical identity.
11. Duplicate visible names without identity merging.

## Clarification by D-084

Aliases do not receive an intrinsic `name` property. Their declaration retains a nominal name and type anchor, but each alias value has only its declared components. A structural alias may declare an ordinary `name: Text` component. `family` members retain their own intrinsic name.
