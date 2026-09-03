---
id: D-026
title: "Membership strict and cardinality by `then`"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions:
  - "Q-003"
  - "Q-021"
  - "Q-047"
affects:
  - "[[specification/04-mathematical-model]], future `10-type-system.md`, future `15-collections.md`"
---
# ADR-026 — Membership strict and cardinality by `then`

- Expanded by: [[ADR-077-cardinality-conditioned-destruction-and-transition-diagnostics|D-077]]

- Questions affected: [[notes/questions/Q-003-p-validation-points|Q-003]], [[notes/questions/Q-021-a-static-conflict-analysis|Q-021]], [[notes/questions/Q-047-s-selection-of-defaults-by-type|Q-047]]
- Documents affected: [[specification/04-mathematical-model]], future `10-type-system.md`, future `15-collections.md`

## Context

One collection characterised by a `thing` contains his own specialisations, not the subject itself identity which acts as type. It is also necessary to determine whether a change to collection must comply with the cardinality after each instruction or upon completion of one unit atomic effects.

## Decision

### Membership from `thing`

Be $T$ the `thing` which appears as type from member and let it be $c$ one identity candidate. Membership is valid precisely when:

$$
c\neq T
\land
c\ \mathsf{is}\ T
$$

It does not exist `reflexive` nor any other modifier that would allow for this case $c=T$.

For example, a property:

```mud
kingdom: Kingdom[1]
```

may contain `Panama` if `Panama is Kingdom` and `Panama != Kingdom`. It must not contain `Kingdom`.

This condition compares the member with the anchor from type, not with the identity the owner of the property. If `Alice is Person`, a property owned by `Alice` classified as `Person` it may contain `Alice`, because `Alice != Person`.

### Point on-site verification

The instructions for the same `then` are evaluated sequentially with respect to their delta private. The intermediate states of that delta do not have to meet the limits of cardinality. Once the `then`, every collection The modified version must comply with its cardinality declared.

Thus, for a collection from cardinality `[1]`, this pattern may be valid within a single block:

```mud
then {
    remove oldKing from kingdom.kings
    add newKing to kingdom.kings
}
```

It is not valid to split the substitution between two `then`. Each `then` must preserve the cardinality; no one can rely on a effect a third party to repair their result.

### Static obligation

Verification is an obligation on the part of the static analysis. For each `then` $t$, every collection affected $p$ and everything state For a well-formed input permitted by the types and guards, the compiler must demonstrate:

$$
\ell_p
\leq
\left|\operatorname{apply}(t,p)\right|
\leq
u_p
$$

where $[\ell_p,u_p]$ is the cardinality declared and $\operatorname{apply}(t,p)$ is the final content of $p$ in the delta deprived of $t$.

The analysis must, as a minimum, take into account:

- The possible initial range of sizes.
- The demonstrable presence or absence of the member withdrawn.
- The oneness and multiplicity of the collection.
- Guard rails and control arms.
- The complete sequence of effects of the `then`.

If the constraint cannot be proven, the programme is rejected as a precaution. A potential local violation is not deferred until runtime.

### Compatibility between `then`

Local evidence is not enough when several `then` they can amend it collection in a wave. Conflict analysis must demonstrate that its consolidation it also retains the cardinality, or demonstrate that the blocks are mutually exclusive. If you cannot prove either of these, the programme is rejected.

For example, two blocks that add different elements to a collection empty `[0..1]` They are valid locally, but cannot co-exist within the same wave unless the compiler demonstrates mutual exclusion.

## Consequences

- There is no modifier `reflexive` in the lexicon, grammar, AST or IR.
- The cardinality is an output property of each `then`, not of every state in the middle of his delta.
- Static rules require an abstract analysis of intervals and effects of collection.
- The language’s acceptance criteria are deliberately conservative: a programme that is safe but cannot be proven may be rejected.
- The consolidation It retains a type-checking mechanism as a runtime safeguard, but failing this check would indicate a compiler error or an invalid external input, not a conflict expected semantic meaning.

## Interaction with default values

One collection from `thing` with a minimum positive result requires a default value that it is a strict specialisation of the type written. D-017 continues to demand that all type has a well-formed default; Q-047 must determine when such type it is well-formed and when an explicit initialiser is required.

## Future verification

1. Acceptance of a direct descendant.
2. Rejection of the anchor exact.
3. Lexical or syntactic rejection of `reflexive`.
4. Replacement `remove`–`add` valid within the same `then`.
5. Rejection of each half of that substitution in `then` separate.
6. An analysis of branches that preserve and break boundaries.
7. Rejection of two locally valid effects whose consolidation it may overflow.
8. Acceptance when mutual exclusivity is demonstrated.

