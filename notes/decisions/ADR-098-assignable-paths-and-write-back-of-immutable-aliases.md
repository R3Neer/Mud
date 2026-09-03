---
id: D-098
title: "Assignable paths and write-back of immutable aliases"
status: current
date: 2026-08-28
supersedes: []
superseded-by: []
questions:
  - Q-006
affects:
  - "structural aliases, exact dictionaries, assignable targets, effects, typing and elaboration, chapters 07 and 08, future chapters 12, 16 and 25"
---

# ADR-098 — Assignable paths and write-back of immutable aliases

- Modifies: [[ADR-031-nominal-aliases-immutable-and-without-cycle-of-life|D-031]], [[ADR-039-collections-and-dictionaries|D-039]] and [[ADR-080-algebra-higher-and-updates-de-collection|D-080]].
- Related to: [[ADR-046-algebra-and-conflicts-of-effects|D-046]], [[ADR-084-specialisation-de-aliases-inherited-members-and-derived-views|D-084]] and [[ADR-086-exact-nominal-identity-external-arrows-and-algebra-de-diccionarios|D-086]].
- Keeps [[notes/questions/Q-006-c-conflicts|Q-006]] open for compatibility of concurrent effects on partially overlapping targets.

## Context

Alias values are immutable and exact dictionaries allow dynamic keyed populations to be maintained. The grammar and superficial AST already admit targets formed by a base followed by member accesses and indices, such as `orders[id].status`. Without a specific elaboration rule, updating a component of a stored alias would require manually reconstructing the complete value and then replacing the association or field containing it.

This surface convenience must not turn aliases into mutable objects or introduce runtime identity into their values. Nor must it confuse a partial update with direct assignment of an association, which may already materialise a missing key.

## Decision

### Reconstructible assignable path

An assignable path may traverse one or more immutable structural alias values when an externally writable storage location exists to which the replacement can ultimately be propagated. Once that root location is found by the ordinary assignability rules, the steps this decision adds as reconstructible are exclusively accesses to stored alias components and exact-dictionary indexing. Each step must be well typed and unambiguously determine which value is to be reconstructed; no implicit write-back is granted to other selection classes.

The write:

```mud
orders[id].status = Shipped
```

does not mutate the `Order` value obtained from `orders[id]`. It is elaboration sugar for:

1. read the current value reached by the path;
2. construct a new value of the alias's exact nominal type, replacing only the target component;
3. retain all other stored components unchanged;
4. recompute derived fields from the new value;
5. propagate the replacement outwards, reconstructing the necessary containing aliases and replacing traversed dictionary associations until the writable root is reached.

Component defaults are not reapplied during reconstruction. The operation preserves the existing value's exact nominality and does not create runtime identity for the alias.

The same rule applies recursively to deeper paths:

```mud
users[userId].profile.address.city = Madrid
games[gameId].players[playerId].score += 10
```

The compound operators `+=`, `-=`, `*=`, `/=`, `|=`, `&=`, `^=` and `--=` use the value reached by the path and apply the same write-back when their leaf operation is well typed.

### Preserved immutability

A local binding containing only an alias value does not become a writable location:

```mud
order := orders[id]
order.status = Shipped # invalid
```

The second line attempts to modify an immutable value without a path back to storage. Likewise, a derived alias field cannot be a target: only stored components may be replaced during reconstruction.

The path root must have the writing authority already required by MUD. Write-back does not cross a nonexistent outer-mutability boundary and does not turn inner `[mut]` capability into permission to replace a value.

### Missing exact key

When exact-dictionary indexing appears as an intermediate step of a write-back path and its key does not exist, the query produces `empty` absence and the effect contributes no change to the delta. The absence of that key:

- does not materialise an association;
- does not construct an alias from its defaults;
- does not itself produce `failed`.

Therefore:

```mud
orders[missingId].status = Shipped
```

is a no-op if `missingId` is not present.

This rule does not modify direct assignment of a complete association:

```mud
orders[id] = order
```

Direct writing retains exact-dictionary semantics: it replaces an existing association and may materialise a missing key when the value and dictionary contract permit it.

### Sequentiality and concurrency

Within the same `then`, a reconstructible path observes the value projected by the private delta's preceding sequential effects, and its write-back is visible to later statements like any other effect.

This decision does not complete the concurrent-conflict matrix. In particular, Q-006 remains open on compatibility between concurrent updates to different components of one reconstructed alias, between a partial update and complete replacement of its container, and other partially overlapping targets.

## Rejected alternatives

### Make aliases mutable

Rejected. Abbreviated writing does not change the value's ontology: the before and after aliases are distinct immutable values.

### Require explicit reconstruction

Rejected. Requiring the author to copy every unchanged component and manually reinsert the value exposes a mechanical persistence detail and makes modelling dynamic populations through dictionaries particularly costly.

### Create a missing key with defaults

Rejected for partial write-back. Without an existing value there is no unambiguous base to reconstruct, and silently materialising the alias would confuse updating with creation. Explicit insertion remains available through direct assignment of the complete association or `add`.

### Produce `failed` for a missing key

Rejected. A missing exact query already represents ordinary absence through `empty`; partial write-back retains that philosophy and reduces to a no-op.

## Consequences

- `dictionary[key].component = value` is the idiomatic way to update a stored alias component in an exact dictionary.
- Aliases remain immutable values without runtime identity.
- Elaboration, not the superficial AST, reconstructs intermediate values and obtains the actual storage target.
- Deep paths avoid introducing copy APIs, registries or manual reconstruction merely to update keyed-population state.
- A missing key cleanly distinguishes partial update from complete insertion.
- Compatibility of partially overlapping concurrent write-backs remains pending in the general conflict matrix.

## Verification

1. `orders[id].status = Shipped` reconstructs an `Order` of the same exact nominal type and retains its other components.
2. A path with nested structural aliases reconstructs from the inside out.
3. A compound update to the component uses the previous value and writes back the reconstructed alias.
4. An alias-typed local does not become assignable merely by containing a value read from storage.
5. A derived alias field cannot be a write-back target.
6. A missing exact key in an intermediate step produces a no-op without insertion or `failed` for that absence.
7. `dictionary[key] = wholeValue` retains the ability to create or replace the complete association.
8. A root without sufficient outer mutability makes the path invalid.
9. Sequential semantics within a `then` observe earlier write-backs.
10. Concurrent overlaps receive no new rule beyond what is already fixed and remain delimited by Q-006.
