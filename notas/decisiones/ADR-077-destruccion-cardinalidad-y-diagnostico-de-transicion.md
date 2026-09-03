---
id: D-077
title: "Cardinality-conditioned destruction and transition diagnostics"
status: current
date: 2026-08-03
supersedes: []
superseded-by: []
questions:
  - "Q-049"
affects:
  - "lifecycle, collections, effects, results and `otherwise`"
---
# ADR-077 — Cardinality-conditioned destruction and transition diagnostics

## Context

Hiding destroyed members and allowing effective cardinality to diverge from its declaration breaks guarantees for later consumers. Dynamically changing the type or propagating degraded collections is likewise unacceptable.

## Decision

`destroy c` computes the complete transition and validates every affected property. If removing `c` from the effective projection violates a cardinality or domain, the transition returns `failed` and is rolled back in full:

```mud
members: Person [2] = Alice, Bob

destroy Bob # failed
```

There is no committed state whose effective cardinality contradicts its declaration.

When removal is valid, a relationship without `mut` capability retains membership latently and `create c` restores it. A `mut` relationship removes stored membership and `create c` does not recreate it. Authorised `remove` also removes latent membership. Every `create` restoration is validated atomically and may return `failed`.

Destroying the declared type of a property preserves D-021's structural suspension: the complete property and its payload remain stored. This differs from destroying an identity used as a value.

### Transition `otherwise`

A `then` block may end with an `otherwise` diagnostic:

```mud
then {
    destroy Bob
}
otherwise "Bob is still required by {team}"
```

The text is evaluated lazily only when the atomic transition returns `failed`. It does not recover, execute an alternative branch or turn `failed` into `rejected`. The diagnostic must also identify the property, cardinality or domain that blocked the operation.

## Consequences

- D-021 no longer rules out `mut` affecting member removal.
- D-026's check includes lifecycle effects and their consolidation.
- There are no cascades of cardinality-degraded states: there is a valid commit or rollback.
- `otherwise` belongs to the result of the complete `then`, not to an individual instruction.

## Verification

1. `destroy` blocked by exact cardinality.
2. Valid removal within a range.
3. Immutable restoration and permanent `mut` removal.
4. Rollback with several affected collections.
5. `create` restoration exceeding a maximum.
6. Distinction between a destroyed identity and a destroyed type.
7. Lazy `otherwise` evaluation and diagnosis of the cause.
