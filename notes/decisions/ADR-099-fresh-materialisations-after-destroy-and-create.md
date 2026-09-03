---
id: D-099
title: "Fresh materialisations after `destroy` and `create`"
status: current
date: 2026-08-28
supersedes: []
superseded-by: []
questions:
  - Q-005
  - Q-046
  - Q-049
  - Q-032
affects:
  - "`thing` lifecycle, materialisation, stored state, dependency suspension, runtime structure and reactive memory"
  - "D-021, D-041, D-054, D-058 and D-077"
  - "chapter 04 and future chapters 11, 21 to 25 and 32"
---

# ADR-099 — Fresh materialisations after `destroy` and `create`

- Modifies: [[ADR-021-cycle-logical-lifespan-and-suspension-by-department|D-021]], [[ADR-041-contracts-under-the-three-types-of-rules|D-041]], [[ADR-054-canonical-definitions-and-initial-activation|D-054]], [[ADR-058-temporal-triggers-changes-and-reactive-old|D-058]] and [[ADR-077-cardinality-conditioned-destruction-and-transition-diagnostics|D-077]].
- Keeps open: [[notes/questions/Q-005-i-binding-identity-and-lifecycle|Q-005]], Q-046 and Q-032 on aspects not fixed here. Q-049 remains closed; this decision retains its resolution on membership and only clarifies the policy for the materialisation itself.

## Context

D-021 and D-054 made `destroy d` remove a declaration from the effective projection while also retaining a `thing`'s own runtime load; a later `create d` reactivated that same load without running initialisers again. That rule correctly addressed a different problem: when another declaration becomes uninterpretable because it depends on a destroyed declaration, its state must not be erased merely because it is suspended.

The two situations need not share a policy. If `King.kingdom` stores `Panama` and the `Kingdom` type is destroyed, the property belongs to `King`: it may retain its load latently while its type is not effective. By contrast, if a concrete `thing` whose own `health` field is `2` is destroyed, retaining that `2` after `create` turns `destroy` into temporary deactivation and prevents a new materialisation from returning to its declared state.

The same distinction applies to runtime structural modifications owned by a `thing` and to the temporary memory of an explicitly destroyed rule.

## Decision

### Canonical identity and materialisation

The canonical definition and semantic identity of a `thing` survive `destroy`. Its own runtime materialisation does not.

For an active concrete `thing`, the following are conceptually distinct:

1. its canonical definition and identity, belonging to the program;
2. its current runtime materialisation, containing its stored-field load and runtime structural modifications owned by that `thing`;
3. the loads of other declarations that may refer to its identity or depend on its type.

`destroy d`, when the complete transition is valid, ends the current materialisation of concrete `thing` `d`. Its identity, descriptor, declared ancestors and canonical definition remain available for a future materialisation.

An abstract `thing` has no concrete own load to reinitialise; its `destroy` retains the applicable activity-removal and structural-suspension semantics.

### Own load and runtime structure

When `destroy d` is confirmed for a concrete `thing`, the following are discarded:

- stored values belonging to its current materialisation;
- runtime structural modifications owned by `d`, including fields added during that materialisation;
- runtime removals of `d`'s canonical properties: a future materialisation starts from the canonical definition, not from the edited structure of the ended materialisation.

Por tanto, si:

```mud
thing Goblin {
    mut health: Nat = 10
}
```

reaches `health = 2`, after a confirmed sequence of `destroy Goblin` followed later by `create Goblin`, the new materialisation starts again with `health = 10`.

This rule does not introduce successive identities: both materialisations correspond to the same canonical identity `Goblin`.

### New materialisation through `create`

`create d` on a canonical `thing` without an active materialisation creates a fresh materialisation using the ordinary first-materialisation rules:

- the effective schema is reconstructed from the canonical definition and its applicable inherited contributions;
- defaults and initialisers are applied again;
- no values or structural modifications from the destroyed materialisation are recovered.

The seed and result policy for stochastic initialisers remains under Q-032; this decision only requires the operation to be a new materialisation rather than recovery of a previous load.

The applicability of `create` when the declaration is already active remains under Q-046.

### Dependency suspension is not destruction

When a declaration ceases to be effective because a hard dependency is inactive, its materialisation and load are not destroyed. Only a `destroy` directed at the declaration itself applies the load-discard defined here.

En particular:

```mud
thing King {
    kingdom: Kingdom = Panama
}
```

seguido por:

```mud
destroy Kingdom
```

makes `King.kingdom` temporarily cease to belong to the effective projection while its declared type is not effective. The property and its `Panama` load belong to `King` and remain stored. If `create Kingdom` confirms a new materialisation of `Kingdom`, `King.kingdom` may become effective again with the same `Panama` value.

This external preservation does not imply retaining the own load of `Kingdom`'s destroyed materialisation.

### References and membership of the destroyed identity

Latent references continue to point to the same canonical identity and may become effective again when a compatible new materialisation exists.

D-077's collection policy is retained:

- a relation without `mut` capability may retain membership of the removed identity latently and restore it with the new materialisation;
- a `mut` relation removes that stored membership when the identity is destroyed, and `create` does not rebuild it by itself;
- destroying a property's declared type suspends the complete property and retains its load, because that load belongs to the property's owner, not to the destroyed type.

Every removal, membership restoration and reappearance of suspended loads remains subject to atomic cardinality and domain validation.

### Atomicity of the new materialisation

A `create d` that materialises a `thing` again must validate jointly:

- the new own load obtained from the definition, defaults and initialisers;
- latent memberships that D-077 may restore;
- external declarations and properties that become effective again when the dependency reappears.

If the resulting state is not well formed, the transition produces `failed` and rollback. No partial materialisation is confirmed.

### Memory of explicitly destroyed rules

`destroy r` on a rule also ends the runtime memory belonging to that rule activation. For a reactive rule, its baselines and temporary binding memory associated with the destroyed activation are discarded.

If `create r` activates it again after `start with`, it is treated as a later activation for temporal purposes: its first active wave establishes the current baseline without triggering `when`, `changes` or temporal expressions merely because of reactivation. From the next wave onwards it compares normally with that new baseline.

A Boolean rule does not retain this kind of temporal memory. An `always` reasserts its invariant at its ordinary validation points.

This decision fixes the effect of an explicit `destroy` on rule memory. Q-005 remains open for the canonical identity of bindings and for the memory policy when a binding disappears or a rule is merely suspended for reasons other than explicit destruction.

## Consequences

- `destroy` is no longer mere deactivation with hibernation of a concrete `thing`'s own load.
- `create` after `destroy` materialises the same canonical identity again, not a new identity or recovery of the previous load.
- Respawn resets matching declared defaults and initialisers naturally arise from `destroy` + `create`; respawn rules needing to retain or modify additional information remain explicit domain logic.
- Dependency suspension remains reversible and does not erase external state.
- Runtime structural edits belonging to a materialisation do not survive its destruction.
- The temporary memory of an explicitly destroyed rule does not cross into its new activation.

## Rejected alternatives

### Retain all own load after `destroy`

Rejected. It makes `destroy` behave like `deactivate` and forces even ordinary reinitialisation of a new materialisation to be expressed separately.

### Also erase suspended external loads

Rejected. The disappearance of a type or dependency does not make data stored by other identities its property. Structural suspension remains reversible.

### Create a new runtime identity

Rejected. `create` continues to operate on a predeclared canonical identity and introduces no instantiation, fresh IDs or distinct nominal incarnations.

### Retain structural modifications from the destroyed materialisation

Rejected. A new materialisation reconstructs its structure from the canonical definition; retaining earlier `add`/`remove` operations would mix an ended materialisation with the next.

### Retain the temporary memory of a destroyed rule

Rejected. A rule explicitly removed from the world must not compare its new activation with a snapshot belonging to the previous activation.

## Verification

1. A destroyed and recreated `thing` retains its identity and descriptor but recovers initial values instead of its previous load.
2. Runtime fields added to the destroyed materialisation do not reappear; runtime-removed canonical properties do reappear from the definition.
3. An external property suspended by destroying its type retains exactly its load and is projected again when the type is recreated.
4. Suspension caused by a dependency does not erase the suspended declaration's own load.
5. Immutable and `mut` relations retain the restoration distinction fixed by D-077.
6. A new materialisation that would invalidate cardinality or domain produces `failed` and complete rollback.
7. A destroyed and recreated reactive rule establishes a new baseline without triggering merely because of reactivation.
8. Q-005 remains open for binding disappearances and suspensions not caused by explicit `destroy`.
9. Q-032 continues to govern the concrete reproducibility of random initialisers between materialisations.
