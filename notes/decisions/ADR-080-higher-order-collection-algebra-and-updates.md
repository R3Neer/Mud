---
id: D-080
title: "Higher algebra and collection updates"
status: current
date: 2026-08-04
supersedes: []
superseded-by: []
questions:
  - "Q-006"
  - "Q-019"
affects:
  - "collections, operators, effects, grammar, AST and cardinality analysis"
---

# ADR-080 — Higher algebra and collection updates

- Modified by: [[ADR-086-exact-nominal-identity-external-arrows-and-dictionary-algebra|D-086]]
- Extended by: [[ADR-098-assignable-paths-and-write-back-of-immutable-aliases|D-098]]
- Modified by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].

- Modifies: [[ADR-039-collections-and-dictionaries|D-039]], [[ADR-046-algebra-and-conflicts-of-effects|D-046]], [[ADR-049-operators-precedence-and-standardised-intervals|D-049]] and [[ADR-057-concrete-grammar-precedence-and-continuation|D-057]].
- Related questions: [[notes/questions/Q-006-c-conflicts|Q-006]] and [[notes/questions/Q-019-n-numbers|Q-019]].

## Context

Every MUD field denotes a collection, and an omitted cardinality is equivalent to `[1]`. It remained necessary to determine how arithmetic operators receive those values, to distinguish numeric subtraction from collection difference, and to complete the compound updates corresponding to collection algebra.

The symmetric difference of multisets defined by absolute multiplicity difference was not associative either. That property prevented `^=` from being consolidated and made a chain of `^` appear to have XOR's usual laws when it did not.

## Decision

### Restricted arithmetic lifting

The binary arithmetic operators `+`, `-`, `*`, `/` and `%` are lifted over collections when at least one operand has a static upper cardinality bound less than or equal to one.

For a member operator `\odot`:

$$
A\mathbin{\odot}B
=
[\,a\mathbin{\odot}b\mid a\in A,\ b\in B\,].
$$

The collection retains one occurrence for each pair of occurrences. If the cardinalities are $[\ell_A..u_A]$ and $[\ell_B..u_B]$, the cardinality before any `unique` normalisation is:

$$
[\ell_A\ell_B..u_Au_B].
$$

Therefore, `empty` is absorbing: if either operand is empty, no pair exists and no member operation is evaluated. In particular, `empty / [0]` produces `empty` without performing a division by zero.

Two operands whose upper bounds may exceed one do not permit implicit arithmetic lifting. MUD does not silently choose between positional pairing, a full Cartesian product, reduction or mutual broadcasting.

When unions are involved, every possible pair of alternatives must support the member operator and their results must form a well-formed union type. Prior narrowing may remove impossible pairs.

If only one operand can be multiple, the result preserves its order whenever that order was observable. `unique` is retained only when analysis demonstrates that the operation cannot collapse distinct members; otherwise the result retains ordinary multiplicity.

### Collection difference

`--` is collection difference. For each value $v$:

$$
\mu_{A\mathbin{--}B}(v)
=
\max(\mu_A(v)-\mu_B(v),0).
$$

`-` no longer denotes collection difference and is reserved for lifted arithmetic subtraction. Thus, over unit cardinality numeric collections:

```text
[5] -  [3] = [2]
[5] -- [3] = [5]
[5] -- [5] = empty
```

`--` has the same precedence and left associativity as `+` and `-`. The spelling `a--b` forms one operator; subtracting a negative value is written `a - -b` or `a - (-b)`.

### Symmetric difference

`^` and `^=` are admitted only when all their effective operands are `unique` collections. They then retain ordinary set symmetric difference and its associative, commutative and involutive laws.

The binary absolute difference of two multisets remains expressible without introducing a misleadingly associative operator:

```mud
(left -- right) | (right -- left)
```

### Compound updates

The grammar admits:

```mud
target |= value
target &= value
target ^= value
target --= value
```

An update `target op= value` requires `target` to designate either a directly externally mutable location or a reconstructible assignable path whose write-back terminates at one, that `target op value` be well typed, and that the result be assignable to the leaf's effective type. Intermediate immutable aliases are reconstructed without acquiring mutability of their own. Inner `[mut]` capability does not replace the requirement for an externally writable root.

Within a `then`, the update observes the value projected by the same private delta's preceding sequential effects. It is not reduced in the AST to an ordinary assignment because its operator determines concurrent consolidation.

Homogeneous updates to the same target are consolidated as follows when observable order and the target's constraints can also be preserved:

| Operator | Consolidation |
| --- | --- |
| `|=` on a collection | Union of all operands; idempotent |
| `&=` | Intersection of all operands; idempotent |
| `--=` | Sum of removed multiplicities and a single truncation at zero |
| `^=` | Symmetric difference by parity; only over `unique` |

Mixing different update classes on the same target is a conflict unless another decision expressly fixes a consolidation. Preserving cardinality, domain, order and uniqueness remains a static obligation of each `then` and of every possible consolidation.

When several compatible concurrent updates add new members to an `ordered` collection and the existing semantic criterion does not by itself determine a total order, provenance is completed reproducibly in accordance with D-100, while respecting all real causality. This situation no longer constitutes an open case of Q-006 on its own. Operations that only filter the target preserve its relative order.

For `Text`, `|=` concatenates sequentially like `|`. Several concurrent concatenations are neither idempotent nor commutative: they are consolidated only when a semantically determined total order exists; otherwise they conflict.

### Typed overloading

`|=`, `&=` and `^=` follow the symbolic operation resolved by types, without themselves extending the domains of `|`, `&` or `^`. In particular, they do not replace word boolean operators. `|=` may denote `Text` concatenation or collection union; `&=` and `^=` denote collection operations wherever defined, and `^=` retains the `unique` requirement. `--=` denotes collection difference only.

## Consequences

- Singular cardinality no longer needs a separate scalar category.
- Arithmetic over a multiple collection and an optional or unit collection has uniform meaning.
- `empty` absorbs all lifted arithmetic without evaluating nonexistent pairs.
- Numeric subtraction and collection difference no longer compete for `-`.
- XOR retains the laws a reader expects because it operates only on `unique` sets.
- The new compound operators preserve algebraic intent through to the IR.

## Verification

1. Lifting `[1]` with `[n..m]` in both orders.
2. Lifting `[0..1]` and absorption by `empty`.
3. Rejection when both upper bounds may exceed one.
4. Matrix of nominal alternatives and prior narrowing.
5. Distinction between `-`, `--`, `-=` and `--=`.
6. Rejection of `^` and `^=` over non-`unique` collections.
7. Homogeneous consolidation of `|=`, `&=`, `^=` and `--=`.
8. Conflict between different classes and preservation of cardinality and order.
