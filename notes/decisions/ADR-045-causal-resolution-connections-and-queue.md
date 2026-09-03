---
id: D-045
title: "Causal resolution, connections and queue"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-003"
  - "Q-005"
  - "Q-020"
  - "Q-052"
affects:
  - "semántica dinámica, reglas reactivas, mensajes"
---
# ADR-045 — Causal resolution, connections and queue

- Amended by: [[notes/decisions/ADR-058-temporal-triggers-changes-and-reactive-old|D-058]], [[notes/decisions/ADR-060-additive-deltas-and-nat-normalisation|D-060]]
- Related questions: Q-003, Q-005, Q-020, Q-052
- Documents concerned: semantics dynamics, reactive rules, messages

## Context

The result MUD behaviour cannot depend on the order in which rules, files, threads or internal structures are evaluated. Reactions are organised into waves based on snapshots.

## Decisión

One resolution Follow this sequence:

```text
estado estable anterior
→ validación de la solicitud
→ raíz tentativa
→ onda 1
→ onda 2
→ …
→ estado estable tentativo
→ always y after
→ confirmar o revertir
```

In each wave:

1. the set of links is constructed `on` active;
2. All the rules say the same thing snapshot home page;
3. the temporal activators of are evaluated `when`;
4. each `then` produces, in sequence, a delta private;
5. Deltas are consolidated by means of D-023, D-046 y D-060;
6. the values are normalised to their base types and validated;
7. the state The resulting expression, if valid, feeds into the wave Next.

The links are set at the start of the wave. Changes in ownership, activations or suspensions occurring during a block only affect the next block. No block takes account of partial deltas from another block.

The root and every wave form causal blocks with the same boundary of consolidation. For a destination `Nat`, all compatible additive deltas are summed as signed integers and the total is clipped to zero just once before constructing the snapshot Next. No rule monitors the signed accumulator.

For memory-based association, the temporal activators compare values in the initial snapshots of two consecutive waves in accordance with D-041 y D-058. A `when e` Purely Boolean detects only $\mathsf{false}\rightarrow\mathsf{true}$ y `e changes` compares the two values directly. D-096 generalises the result from a trigger to zero or more causal matches: `and` performs a natural join on compatible matches and `or` his union, whilst retaining bindings, markers and identifiers from occurrence.

A connection that was not present in the first one snapshot as evidenced by `start with` joins the group in the first wave subsequent instance in which it is active. That wave initialises all its temporary memory without firing it. Its first possible firing occurs at the wave Next. The connections that have been present since the very beginning snapshot are the express exception: each branch High Boolean begins with ‘previous virtual’ `false` and you can press during the stabilisation initial; `changes` y `old` compare that snapshot with itself.

One resolution ends when a wave has no effect and leaves no new consequences or pending causal events for the next one. A cycle u oscillation detected cases result in `failed`; a resource limit is a distinct technical safeguard, not an alternative definition of stabilisation.

There’s only one causal resolution activated by world. External applications received during this period are placed in a queue and bring participants together, assess `given`, domains and `if` when they are due to start, not when they were glued on.

Every `message` what has happened is preserved as a occurrence causal attempt with identity, declaration, bindings and birth view. Its payload The interior is projected onto that view causal and the same occurrence is available as a trigger in the wave next; to the host, after confirmation, the payload is projected onto the stable state end. A reversal cancels everything delivery outdoor.
Confirmed deliveries retain their order causal between waves and are used within each wave a stable and reproducible technical process that is not a priority semantics.

## Consequences

- The order in which the operations are physically executed does not alter the result.
- The canonical identity and the retention of memory after a link has been severed remain open in Q-005; his value The starting price has already been set.
- Detection semantics fluctuations and technical safeguards remain open in Q-020.
- The multiplicity of causally distinct occurrences is preserved and is not deduplicated by payload. Q-067 leaves open the question of what happens if a participant no longer exists or cannot be assessed in the final external projection.

## Verification

1. Permutations of the physical order produce the same result transition.
2. A link created in a wave Just take part in the next one.
3. One action The pasted text is validated against the state where it begins.
4. One oscillation does not confirm state partial.
5. One resolution revertida does not publish messages.
6. A genuine initial connection takes hold during the stabilisation from `start with`.
7. A link created in a wave take baseline on the next one, and can only fire from the one after that.
8. Two consecutive net changes produce two pulses `changes`.
9. Two activators linked by `and` They only fire when both press the same button wave.
10. A change brought about by `or` to a transition The Boolean signal preserves either of the two pulses.
11. Deltas `-2` y `+3` on a `Nat` A zero at the start produces a one in the next one snapshot.
12. None snapshot from wave sets out a `Nat` negative.

## Amendment current by D-096

A `message` is a occurrence causal with identity and bindings, not merely an output whose fields are deferred to the state end. The occurrence born in a wave is available as a trigger in the wave next. Within the MUD, its payload is projected onto the view causal from the start; to the host, after commit, it is projected onto the stable state final. Both projections belong to the same occurrence. The stabilisation it also requires that there be no consequences/ocurrencias pending cases.
