---
title: Thing specialisation and identity
tags:
  - mud/specification
status: proposed
normative: true
depends-on:
  - "[[04-mathematical-model]]"
  - "[[10-names-and-anchors]]"
  - "[[11-type-system]]"
  - "[[15-fields-and-mutability]]"
questions: []
decisions:
  - D-014
  - D-015
  - D-018
  - D-021
  - D-054
  - D-068
  - D-073
  - D-084
  - D-087
  - D-096
  - D-099
  - D-111
  - D-112
  - D-114
  - D-116
  - D-122
  - D-128
---

# 12. Thing, specialisation and identity

## Scope

This chapter defines canonical thing declarations, ancestry, schema admission,
initialisation and the static boundary of activity. It states the lifecycle
invariants that these contracts require. It does not define an effective-view
algorithm, identity registry encoding, wave scheduling or causal attribution.
The corresponding operational contracts belong to [[04-mathematical-model]]
and [[28-effects]].

```mud
abstract thing Place
thing Harbor as Place { mut visitors: Nat = 0 }
```

## Identity and declaration

> [!definition] Canonical thing
> A thing declaration introduces one canonical nominal identity. A concrete
> thing denotes that particular identity with independently owned state; an
> abstract thing has identity and may contribute schema but has no own concrete
> stored payload. Both may be predecessors of other things.

There is one canonical definition per identity. `create Name` refers to that
definition and changes activity; it introduces no new identity, body, parent,
field or captured caller environment. There is no class/instance distinction.
Different declarations remain different identities even when their effective
schemas and stored values coincide. Equality of thing values compares identity,
not field contents or materialisation generation.

> [!rule] MUD-THING-001 — Canonical identity and static schema
> A programme must resolve every thing to one definition and an acyclic static
> ancestry graph. Its field declarations are fixed by that definition and the
> inherited schema. Runtime effects must not add, remove or redefine fields.

The concrete grammar is [[grammar/mud.ebnf]]; the source constructors and origin
retention are [[syntax/mud-surface-ast.asdl]]. An empty body may be omitted:
`thing Gate`, `thing Gate {}` and `thing Gate;` have the same semantic definition.
Source trivia and the chosen spelling remain CST information.

## Ancestry and strict membership

Let T be the finite catalogue of resolved thing identities, including `Thing`.
Let D contain the declared direct descendant-to-parent edges. Add the implicit
edge `(t, Thing)` for a root other than Thing lacking a declared predecessor;
call the resulting relation R. The direct graph must be acyclic. Define
`is` as the reflexive-transitive closure R*. Thus `t is t` holds without a
declared self-edge, and `is` is a partial order. The written `as` list is
unordered; it supplies no priority or method-resolution order.

`Thing` is the always-effective built-in abstract root with anchor
`thing::Thing`. It has no source body or own concrete state. It cannot be
redefined, created, destroyed, or included in `start with` or `all Thing`.
Explicit `as Thing` is redundant and receives a removal suggestion. Reflection
distinguishes declared parents from the implicit semantic root edge.

> [!rule] MUD-THING-002 — Strict thing membership
> A member c of a collection typed by thing T must satisfy `c is T` and `c != T`.
> Participant population selection additionally requires the applicable
> concrete activity/effectiveness conditions. Reflexive nominal ancestry alone
> does not make the receiver its own population member.

For a resolved concrete identity c and target T, define Strict(c,T) by
`c != T and (c,T) in R*`. The membership premise of a value admission judgement
is Strict(c,T); ordinary domain, cardinality and capability obligations remain
independent premises. `iis` tests exact effective nominal type and does not
compare two thing identities for equality.

## Generics and public ancestry

Abstract things may declare static type parameters. A well-formed application
retains its constructor and exact arguments, remains abstract, and creates no
new declaration, anchor, runtime identity or lifecycle target. A concrete
descendant supplies its own identity and substitutes the application's schema.
Concrete things cannot declare type parameters. Bounds, invariant writable
positions and finite application closure follow [[11-type-system]].

A cross-part ancestor must be in the public contract's transitive type closure
and the caller must have direct `uses` authorisation. `using` only imports names.
Inheritance grants no private-field access, foreign mutation or foreign
activation permission. Inherited canonical initialisation is elaborated under
its declaring owner's access rights. An external descendant participates in
the linked world's applicable ancestry/population; analyses cannot assume
that all descendants were declared locally.

## Effective schema and initialisation

Let Fields(t) collect the inherited and local field declarations for t by their
original declaration identities. Reaching one origin through a diamond counts
once. Contributions and refinements must satisfy the member-conflict and
substitutability rules in [[11-type-system]] and [[15-fields-and-mutability]];
ancestor order never resolves a conflict. Externally writable stored contracts
are invariant. Initialisers select values and cannot create declarations.

Every newly declared stored field has an explicit, statically admissible
initialiser. A declaration `field: Type = value` is one declaration, not a
separate assignment. `field = value` in a thing body must resolve to an inherited
stored field. Declaring that field locally and assigning it separately in the
same definition is invalid. Types supply no implicit initial value.

Abstract predecessor initialisers can contribute to concrete descendants.
A more specific applicable initialiser overrides a less specific one; a diamond
deduplicates one original initialiser. Independent incomparable initialisers
for the same field conflict. A concrete thing's own local assignment initialises
its own payload and does not become an inheritable schema default for future
descendants. Inherited field defaults and abstract initialisers remain distinct.

> [!rule] MUD-THING-003 — Independent initial payload
> Materialisation uses the effective static field defaults and applicable
> initialisers. It must not read or copy the active mutable payload of an
> ancestor merely because the thing specialises it. Every initial value must
> meet the complete stored contract.

Write Schema(t) admitted when: all origins resolve without conflict, required
initialisers exist, their static evaluation succeeds, and each resulting value
passes its field's type/domain/shape contract. This judgement is required before
the declaration can supply an initial payload. It is not a runtime world
stabilisation judgement. Derived fields have no independent stored load.

## Activity, suspension and generations

Activity, canonical identity and effectiveness are distinct. An inactive hard
dependency can suspend a declaration or field from the effective projection
without deleting its static descriptor or independently owned stored load.
Specialisation alone does not suspend every descendant of an inactive ancestor;
canonical ancestry survives such activity changes.

An active concrete thing owns one materialisation generation. Destruction
discards its own payload; subsequent creation retains canonical identity and
constructs a fresh generation from the static schema. A stored write observed
in an older generation cannot migrate to the new one. Suspension alone neither
destroys the owner nor resets its retained payload.

`create` on an already explicitly active declaration and `destroy` on an
explicitly inactive one are instruction-local successful no-ops. Their targets
must still be resolved, lifecycle-capable and accessible. No-op admission does
not skip subsequent instructions. The protected transaction validates resulting
domains/cardinalities, fresh payload and applicable relation restorations;
failure supplies Errors and rollback. This chapter does not prescribe how the
operational algorithm discovers all those consequences.

## Reflection and visibility

Metadata is separate from ordinary state and remains read-only during execution.
`~name` is presentation; `~anchor` and `~path` identify the canonical declaration.
Metadata is not inherited. An inactive declaration retains its metadata.
`~fields` describes effective inherited schema origins and `~declaredFields`
describes locally declared fields; suspension is not source-schema deletion.
The precise reflective availability and origin rules are
[[10-names-and-anchors]] and [[21-expressions]]. A reflective contract cannot
expose invisible declarations by silently filtering them from an aggregate.

## Examples and counterexamples

```mud
thing Kingdom { mut treasury: Money = 0 }
thing Egypt as Kingdom
thing France as Kingdom { treasury = 20 }
abstract thing RichKingdom as Kingdom { treasury = 20 }
thing Lydia as RichKingdom
```

Informative interaction example: Egypt initially has zero; France and Lydia
initially have 20. Mutating Kingdom's own treasury does not mutate those values.
France's local assignment does not supply a schema default to its descendants.
Destroying and recreating Egypt reconstructs its payload, preserving identity.

```mud
thing A as B
thing B as A                 # invalid: ancestry cycle
thing Store with T           # invalid: concrete generic declaration
thing Broken as Kingdom {
    treasury: Money = 10
    treasury = 20            # invalid: local declaration plus assignment
}
```

`create Thing` is invalid, as is treating `remove treasury from Egypt` as schema
deletion. Collection removal requires a compatible writable collection place.

## Conformance evidence

[[types/typing-cases.yaml]] records stored initialisation, opaque thing type
identity, concrete-generic rejection and abstract-application admission.
[[types/test_declaration_witnesses.py]] checks supplied ancestry, strict
membership and origin/initialiser conflict certificates. These finite witnesses
do not implement lifecycle execution or a compiler. The grammar, CST coverage
and nominal HIR remain the declaration/resolution contracts; typed schema and
materialisation generations are not nominal HIR fields.
