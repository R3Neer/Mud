---
id: D-063
title: "Signatures, `given` and joint `on` bindings"
status: current
date: 2026-07-30
supersedes: []
superseded-by: []
questions:
  - "Q-011"
  - "Q-012"
  - "Q-013"
affects:
  - "signatures, calls, capabilities, automatic bindings, name analysis, AST, IR and diagnostics"
---
# ADR-063 — Signatures, `given` and joint `on` bindings

- Amends: [[notes/decisions/ADR-019-mutability-orthogonal-to-collection-and-members|D-019]], [[notes/decisions/ADR-036-participants-recipients-and-calls|D-036]], [[notes/decisions/ADR-041-contracts-under-the-three-types-of-rules|D-041]], [[notes/decisions/ADR-051-graph-future-semantics-and-reconstructable-information|D-051]] and [[notes/decisions/ADR-057-concrete-grammar-precedence-and-continuation|D-057]]
- Extends: [[notes/decisions/ADR-037-fields-and-declarative-domains|D-037]]
- Closes again: [[notes/questions/Q-011-v-named-participant-binding|Q-011]], [[notes/questions/Q-012-v-named-given-values|Q-012]] and [[notes/questions/Q-013-r-relational-constraints-between-on-participants|Q-013]]
- Affected documents: signatures, calls, capabilities, automatic bindings, name analysis, AST, IR and diagnostics

## Context

MUD separates the subjects of an operation, declared with `for`, from its auxiliary `given` parameters. The original positional binding of `given` made it impossible to omit an intermediate default value and treated `name = expression` as a label rather than a name binding.

Related `on` headers were also resolved from left to right. That restriction prevented expressing symmetric or cyclic relationships even though the active world and all observed collections were finite:

```mud
rule MutualFriends on
    alice in bob.friends,
    bob in alice.friends
{
    ...
}
```

## Decision

### `given` values

Every `given` has a mandatory name, is read-only and may declare a static default value:

```mud
given
    origin: Square = Capital,
    depth: Nat,
    exhaustive: Bool = false
```

A `given` permits neither external mutability nor an inner `mut` capability. If an action needs to write to the supplied collection or to the state of a received `thing`, that value is an operation subject and must be declared with `for`.

The annotation of a `given` accepts the general type expression, including exact and decision-based dictionary types. For example, `given prices: Product -> Money` is valid. Being able to write a dictionary grants no capability: all its collections and values remain subject to the prohibition on `mut` in `given`.

The default:

- Is a closed, pure and deterministic static expression.
- Cannot consult participants, other `given` values, local values or world state.
- May use literals, statically known nominal values and operations between constants.
- Is elaborated against the expected type and must satisfy the `given`'s domain and collection specification.

`given` parameters with defaults may appear in any position of the signature.

### Positional and named arguments

A call may use:

1. Positional arguments only.
2. A positional prefix followed by named arguments.
3. Named arguments only.

After the first named argument, no positional argument may appear.

Positional arguments bind as-yet-unbound `given` parameters in declaration order. Only a complete suffix whose `given` parameters have defaults may be omitted positionally.

An argument of the form `name = expression` performs a genuine named binding. It may:

- Bind any `given` parameter not yet bound.
- Omit an intermediate `given` parameter that has a default.
- Appear in an order different from that of the signature.

It may not repeat a name or use an unknown one. When the call ends, every `given` without a default must have been bound exactly once.

The non-canonical order is valid, but the compiler suggests ordering named arguments as declared:

```mud
game.Search(depth = 3, origin = Capital)
```

is suggested as:

```mud
game.Search(origin = Capital, depth = 3)
```

The suggestion preserves exactly the same bindings and is not emitted when the order is already canonical.

### `for` receivers

Every `for` role has an explicit source identifier, including cardinality `[1]`, in accordance with D-087. The signature retains declaration order, but that order does not replace the slot's stable identity.

The named multipart receiver form remains exact, exhaustive and non-mixable with positional arguments. Roles may be reordered, but the compiler suggests declaration order. A signature declaration never contains anonymous participants.

### Useless inner capability

The inner capability `[mut]` expresses permission, not a guarantee that the type provides mutable state. It is therefore legal to write it on a collection or dictionary whose effective values are basic values, aliases, `family` members or other immutable values.

When analysis can prove that no value accessible through that capability can be mutable, the compiler emits a suggestion to remove `[mut]`. This is not a warning: the program is correct, there is no risk, and removing it preserves effective behaviour.

In a dictionary:

- Outer `mut` permits creating or removing associations and replacing the value of an existing key.
- `[mut]` grants capability exclusively over materially associated `thing` values.
- It never grants capability over keys.
- It does not cross aliases or nested containers and does not introduce deep mutability.
- Reading an absent key produces `empty` with the declared shape and does not grant inner capability as if an association existed.

Each nested level retains its own capabilities.

### Joint `on` headers

Names declared in an `on` header are visible throughout the header, even before their textual position. Elaboration occurs in two phases:

1. Roles, names, annotations and constraints are collected.
2. Their types and domains are resolved jointly.

A related participant may have an annotation that nominally refines the members of its collection:

```mud
alice: Person in bob.friends
```

The annotation does not declare the type of `bob.friends`. It requires `alice` to satisfy both the collection member type and `is Person`. This permits selecting a specialisation within a collection declared with a more general root.

Type constraints for the whole header must have one unique nominal solution. If there are several solutions or none, the program is invalid and must add sufficient annotations.

### Universe and binding set

`on` binds one individual value per role. In a direct form without `in`, the role's universe is the finite set of concrete, active `thing` values in the read snapshot that satisfy its effective type. In a related form `name[: Type] in source`, the universe comes from the members of that finite enumerable source and the optional annotation acts as a refinement. A type without an implicit finite universe, such as `Nat`, cannot use the direct form.

Let `r_1,\\ldots,r_n` be the textual role order and `U_1,\\ldots,U_n` their resulting universes. The header denotes the set:

$$
B
=
\\{
(v_1,\\ldots,v_n)\\in U_1\\times\\cdots\\times U_n
\\mid
\\text{all relational constraints are true}
\\}.
$$

Constraints are interpreted jointly. Repeated membership by multiplicity does not duplicate the same role assignment.

This is a finite relational join, not a fixed point. An implementation may use filtered products, indexes, joins or another strategy, provided that it produces the same set.

A cycle of constraints is not a calculation cycle:

```mud
a in b.neighbours,
b in c.neighbours,
c in a.neighbours
```

All collections are read in the same starting snapshot. Effects do not retroactively alter the wave's bindings; they may produce different bindings in the next wave. Cycles between computed fields remain subject to their own rules and are not legitimised merely by appearing in `on`.

### Identity, orientation and technical order

A binding is a total assignment of roles. No implicit inequality is imposed: two roles may receive the same value if their constraints permit it.

Roles also retain orientation. If a symmetric relation admits both `(Alice, Bob)` and `(Bob, Alice)`, these are distinct bindings. MUD does not deduplicate pairs by symmetry or assume that the body treats the roles identically.

Semantically, a wave's bindings form a set and their order does not determine effects. When all bound values are `thing`, the reproducible technical order already defined by anchors remains available for traces and diagnostics; D-096 does not turn that technical convention into a semantic order for general `on` values.

## Consequences

- `given` labels become named bindings.
- Adding a `given` with a default can preserve existing calls.
- Defaults introduce no dependencies between parameters.
- `given` carries no write capability.
- `on` cycles are finite constraints, not recursive evaluation.
- AST and IR retain defaults, binding mode, written order, suggested canonical order, nominal refinements and the resolved constraint set.
- Capability analysis distinguishes an existing association from a default read of an absent key.

## Verification

1. `given` with an initial, intermediate and final default.
2. Positional omission of a complete defaulted suffix only.
3. Named omission of an intermediate default.
4. Positional prefix followed by names, and rejection of a later positional argument.
5. Rejection of a repeated or unknown argument, or a missing required argument.
6. Canonical-order suggestions for named arguments and receivers.
7. Rejection of both forms of `mut` in `given`.
8. A suggestion, not a warning or error, for demonstrably useless `[mut]`.
9. Outer writing of collections and dictionaries of immutable values through `for mut`.
10. Inner capability over present `thing` values, and no capability over keys, aliases, nested levels or defaults for absent keys.
11. Forward references between `on` roles.
12. `role: Type in expression` refinement.
13. Acyclic joins, two-role cycles and three-role cycles.
14. Rejection of ambiguous nominal inference.
15. Implicit universes of concrete active `thing` values for direct `on`, and finite enumerable sources for `on ... in source`, including rejection of a type without an implicit finite universe.
16. Preservation of both symmetric orientations and an allowed reflexive binding.

## Current amendment by D-096

`on` retains its automatic binding role and does not absorb `message` occurrences: message/rule causality belongs to `when`. D-096 extends the related form `name[: Type] in source` to values from a finite enumerable source. The direct form without `in` continues to select `thing` identities from the implicit universe.
