---
id: D-060
title: "Additive deltas and `Nat` normalisation"
status: current
date: 2026-07-29
supersedes: []
superseded-by: []
questions:
  - "Q-002"
  - "Q-006"
  - "Q-019"
affects:
  - "future chapters `10-sistema-de-tipos.md`, `25-efectos.md`, `28-resolucion-de-acciones.md` and `29-ondas.md`"
---
# ADR-060 — Additive deltas and `Nat` normalisation

- Amends: [[notas/decisiones/ADR-040-semantica-numerica-basica-restante|D-040]], [[notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]] and [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]]
- Related to: [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]]
- Related questions: Q-002, Q-006, Q-019
- Affected documents: future chapters `10-sistema-de-tipos.md`, `25-efectos.md`, `28-resolucion-de-acciones.md` and `29-ondas.md`

## Context

D-040 established that `Nat` arithmetic saturates at zero. D-046 also established that compatible additive updates are consolidated by summing deltas. Without specifying the point of saturation, these rules allowed two distinct results:

```mud
# counter is 0
counter -= 2
counter += 3
```

Saturating each update would produce `3`; summing the deltas first and saturating only once would produce `1`. The first alternative depends on order and contradicts the commutative purpose of additive effects.

## Decision

### Values and deltas

A value of type `Nat` is never negative. Stored states, wave snapshots and every reading of a `Nat` expression belong to:

$$
\mathbb N=\{0,1,2,\ldots\}.
$$

An additive delta targeting a `Nat` is not itself a `Nat` value. The IR represents it as a signed integer:

$$
\delta\in\mathbb Z.
$$

Therefore, `counter -= 2` contributes the $-2$ delta; it does not store the value $-2$.

### Pure arithmetic

Ordinary subtraction of `Nat` values retains the immediate saturation from D-040:

$$
a-_{\mathsf N}b=\max(0,a-b).
$$

A pure expression always produces a value of its type. In particular:

```mud
result: Nat := 0 - 2
```

produces `0`.

### Accumulative effects

Accumulative instructions are not assignment sugar:

```mud
target += amount
target -= amount
```

They produce positive and negative additive deltas respectively. They are not elaborated as:

```mud
target = target + amount
target = target - amount
```

Let $n\in\mathbb N$ be the target's value in the common snapshot and let $\delta_1,\ldots,\delta_k\in\mathbb Z$ be every compatible additive delta targeting it during one causal batch. The value fed into the following snapshot is:

$$
n'=
\max\left(
0,\;
n+\sum_{i=1}^{k}\delta_i
\right).
$$

Deltas are summed before normalisation. This rule applies when consolidating the root and when closing each wave, before constructing the snapshot that the following batch can read.

In the opening example:

$$
\max(0,0-2+3)=1.
$$

The result is the same for every permutation of the deltas.

### Sequential overlay within a `then`

Each `then` retains its textual order when evaluating operands for subsequent effects. Let $\Delta_j$ be the signed sum of the deltas already emitted by that same `then` against a `Nat` target after its first $j$ instructions.

A subsequent reading of the target within that private delta observes:

$$
\operatorname{read}_{j}(n)=\max(0,n+\Delta_j).
$$

This projection neither replaces nor truncates $\Delta_j$. The internal delta may remain negative even when the visible reading is zero:

```mud
# counter is 0
counter -= 2
snapshot = counter
counter += 3
```

Reading `counter` to calculate `snapshot` produces `0`, but the final accumulated delta is $-2+3=1$, and the next state contains `counter == 1`.

A `then` never observes another `then`'s private deltas. They all start from the same common snapshot, and only their final deltas are consolidated.

### Domains and observation

After the result has been normalised to `Nat`, the target's refined domain is checked in accordance with D-037. If the domain excludes the normalised value, the tentative state is invalid and resolution produces `failed`.

No reactive rule, message, `look`, `old` or `changes` observes negative deltas or intermediate values of a `then`. Waves compare only snapshots that have already been consolidated and normalised.

### Scope

D-060 defines only homogeneous additive updates. The following remain in force:

- the conflict between assignment and arithmetic update;
- the conflict between additive and multiplicative update;
- composition by product of compatible multiplicative updates;
- D-046's open questions about structural effects and partially overlapping targets.

## Consequences

- `Nat` saturation does not break the commutativity of additive deltas.
- The IR distinguishes natural values from signed integer deltas.
- The physical order of rules or threads does not alter the consolidated result.
- Private sequentiality affects readings used to calculate subsequent effects, not the global point of normalisation.
- `+=` and `-=` cannot be rewritten as ordinary assignment.
- The lower bounds of refined domains are checked after normalisation to the basic type.

## Rejected alternatives

### Saturate every update

For an initial value of zero, applying `-2` and `+3` would produce `3` or `1` according to order. That would make declared compatible effects non-commutative.

### Expose the negative accumulator

This would permit a `Nat` expression temporarily to produce a negative integer and would leak IR details into observable semantics.

### Also truncate the private delta

If a reading projected to zero replaced the $-2$ delta with zero, the later compensation by $+3$ would be lost and per-instruction saturation would reappear.

### Equate `-=` with assignment

This would conflate the accumulative effect with saturated pure calculation and make it impossible to consolidate updates from distinct rules by summing deltas.

## Verification

1. `Nat` never contains or exposes a negative value.
2. Pure subtraction `0 - 2` produces `0`.
3. With initial value `0`, the `-2` and `+3` deltas produce `1`.
4. Every permutation of additive deltas produces the same result.
5. A still-negative total is normalised to `0`.
6. A private reading after a negative delta observes `0` without truncating the pending delta.
7. A private reading after several deltas observes the projection of their accumulated sum.
8. A `then` does not observe deltas from another `then`.
9. The root and waves deliver only normalised values to the following snapshot.
10. A refined domain is checked after basic normalisation.
11. Rejection of expanding `+=` or `-=` into an assignment.
12. Preservation of conflicts between incompatible effect families.
