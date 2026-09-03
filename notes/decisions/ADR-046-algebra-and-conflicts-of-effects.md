---
id: D-046
title: "Algebra and conflicts of effects"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-002"
  - "Q-006"
  - "Q-021"
  - "Q-046"
affects:
  - "efectos, raíz, ondas, conflictos"
---
# ADR-046 — Algebra and conflicts of effects

- Amended by: [[notes/decisions/ADR-060-additive-deltas-and-nat-normalisation|D-060]]
- Expanded by: [[ADR-080-algebra-elevada-and-actualizaciones-de-coleccion|D-080]]
- Amended by: [[ADR-096-modulos-callables-look-message-and-activacion|D-096]].
- Related questions: Q-002, Q-006, Q-021, Q-046
- Documents affected: effects, root, waves, conflicts
- Amended by: [[ADR-100-orden-logico-procedencia-pertenencia-and-consolidacion-de-efectos|D-100]].

## Context

Concurrent effects must be combined according to their meaning, not according to the arbitrary order in which an implementation encounters them.

## Decisión

The MUD effects catalogue includes:

- allocation `=`;
- cumulative addition and subtraction;
- cumulative multiplication;
- union, intersection, symmetric difference `unique` and cumulative differences;
- `add` y `remove` regarding collections or properties;
- `create` y `destroy`;
- invocations of `action` o `subaction` within any semantic context `then`; the call sequentially incorporates its effects into the delta private asset in accordance with D-096.

Every `then` calculate a delta sequential private from a snapshot common. The consolidation of concurrent deltas is deterministic.

Minimum standards:

| Effects on the same destination | Result |
| --- | --- |
| allocations to it value | compatible, a standardised allocation |
| allocations to other items | conflict |
| homogeneous additive updates | compatible, sum of deltas before normalising the destination |
| homogeneous multiplicative and divisive updates | compatible, accumulation in the numerator `P` and denominator `Q` |
| assignment with arithmetic update | conflict |
| additive update with multiplicative or divisive update | compatible; standard form `((x + Δ) * P) / Q` |
| updates `|=` consistent across collections | union of operands |
| concatenations `|=` consistent data on `Text` | compatible only with a specific total order amount |
| updates `&=` homogeneous | intersection of operands |
| updates `--=` homogeneous | sum of removed multiplicities and final truncation |
| updates `^=` consistent data on `unique` | symmetric difference by parity |
| different types of update collection | conflict |

For structural purposes, the following apply D-023, D-026 y D-054:

- compatible activations via `create` precede additions;
- withdrawals precede destruction;
- `create` y `destroy` The shells leave the target destroyed as the wave;
- several activations of the same canonical definition when absent, they consolidate idempotently;
- several additions to it value to one collection `unique` are idempotently consolidated into a single presence;
- each `then` and all consolidation where possible, they should preserve cardinalities statically.

A conflict It is certainly true that the compiler proves this to be inevitable error static. If it demonstrates that it is possible but not inevitable, it issues a warning. If it demonstrates that the destinations cannot match or that the effects consolidate in a compatible manner, it does not issue diagnostic from conflict. If a conflict Whether it is signalled or cannot be determined statically, it occurs during a resolution, the runtime produces `failed` with a full rollback.

Additive deltas aimed at a `Nat` are signed integers, although the value of destiny can never be negative. For a value initial $n$ and compatible deltas $\delta_i$, D-060 fixed:

$$
n'=\max\left(0,n+\sum_i\delta_i\right).
$$

Inside a `then`, a subsequent reading examines the saturated projection of the value initial plus his delta cumulative private sector debt, but that projection does not reduce the delta pending. Blocks do not observe other parties’ private deltas.

## Consequences

- The semantics It does not depend on the order of rules or threads.
- The saturation of `Nat` it does not violate the commutativity of additive updates.
- Q-006 remains open for the remaining combinations of collections, dictionaries, properties, cycle lifespan and partial overlaps.
- The special conservative analysis of cardinality from D-026 takes precedence over the general rule of deferring undecidable matches.

## Verification

1. Compatible and incompatible cases in each row.
2. Equality under a permutation of deltas.
3. Conflict known statically and conflict depending on the bindings.
4. Consolidation structural with activation by means of `create`, addition, withdrawal and destruction.
5. Full rollback in the event of conflict late.
6. Consolidation of signed deltas on `Nat` before it becomes overloaded.
7. Projected sequential reading without cropping of the delta private.

