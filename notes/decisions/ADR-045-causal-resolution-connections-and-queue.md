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
  - "dynamic semantics, reactive rules and messages"
---
# ADR-045 — Causal resolution, connections and queue

- Amended by: [[notes/decisions/ADR-058-temporal-triggers-changes-and-reactive-old|D-058]], [[notes/decisions/ADR-060-additive-deltas-and-nat-normalisation|D-060]]
- Related questions: Q-003, Q-005, Q-020, Q-052
- Documents concerned: semantics dynamics, reactive rules, messages

## Context

The result MUD behaviour cannot depend on the order in which rules, files, threads or internal structures are evaluated. Reactions are organised into waves based on snapshots.

## Decision

One resolution Follow this sequence:

```text
estado estable anterior
→ request validation
→ tentative root
→ onda 1
→ onda 2
→ …
→ estado estable tentativo
→ always and after
→ confirm or roll back
```

In each wave:

1. the set of links is constructed `on` active;
2. All the rules say the same thing snapshot home page;
3. the temporal activators of are evaluated `when`;
4. each `then` produces, in sequence, a delta private;
5. Deltas are consolidated by means of D-023, D-046 and D-060;
6. the values are normalised to their base types and validated;
7. the resulting expression, if valid, feeds into the next wave.

The links are set at the start of the wave. Changes in ownership, activations or suspensions occurring during a block only affect the next block. No block takes account of partial deltas from another block.

The root and every wave form causal blocks with the same boundary of consolidation. For a destination `Nat`, all compatible additive deltas are summed as signed integers and the total is clipped to zero just once before constructing the snapshot Next. No rule monitors the signed accumulator.

For memory-based association, temporal activators compare values in the initial snapshots of two consecutive waves in accordance with D-041 and D-058. A purely Boolean `when e` detects only $\mathsf{false}\rightarrow\mathsf{true}$, while `e changes` compares the two values directly. D-096 generalises the result from a trigger to zero or more causal matches: `and` performs a natural join on compatible matches and `or` their union, while retaining bindings, markers and occurrence identifiers.

A connection that was not present in the first snapshot, as evidenced by `start with`, joins the group in the first subsequent wave in which it is active. That wave initialises its temporary memory without firing it. Its first possible firing occurs in the following wave. Connections present from the initial snapshot are the express exception: each Boolean branch begins with virtual previous `false` and may fire during initial stabilisation; `changes` and `old` compare that snapshot with itself.

One resolution ends when a wave has no effect and leaves no new consequences or pending causal events for the next one. A detected cycle or oscillation produces `failed`; a resource limit is a distinct technical safeguard, not an alternative definition of stabilisation.

Only one causal resolution is active for a world at a time. External applications received during this period are placed in a queue and bind participants, evaluate `given`, domains and `if` when they are due to start, not when they are enqueued.

Every `message` occurrence is preserved as a causal attempt with identity, declaration, bindings and birth view. Its payload is projected onto that causal view, and the same occurrence is available as a trigger in the next wave; after confirmation, the payload is projected to the host against the final stable state. A rollback cancels all external delivery.
Confirmed deliveries retain causal order between waves and are processed within each wave in a stable, reproducible technical order that carries no semantic priority.

## Consequences

- The order in which the operations are physically executed does not alter the result.
- Canonical identity and memory retention after a link is severed remain open in Q-005; the value-level starting policy is already fixed.
- Detection semantics fluctuations and technical safeguards remain open in Q-020.
- The multiplicity of causally distinct occurrences is preserved and is not deduplicated by payload. Q-067 leaves open the question of what happens if a participant no longer exists or cannot be assessed in the final external projection.

## Verification

1. Permutations of physical execution order produce the same transition result.
2. A link created in one wave participates only in the next wave.
3. Each action is validated against the state in which it begins.
4. An oscillation does not confirm a partial state.
5. A rolled-back resolution publishes no messages.
6. A genuine initial connection takes effect during stabilisation from `start with`.
7. A link created in one wave takes its baseline in the next and can fire only from the following wave.
8. Two consecutive net changes produce two `changes` pulses.
9. Two activators linked by `and` fire only when both match in the same wave.
10. A change introduced by `or` preserves either Boolean transition pulse.
11. Deltas `-2` and `+3` on a `Nat` starting at zero produce one in the next snapshot.
12. No wave snapshot exposes a negative `Nat`.

## Amendment current by D-096

A `message` is a occurrence causal with identity and bindings, not merely an output whose fields are deferred to the state end. The occurrence born in a wave is available as a trigger in the wave next. Within the MUD, its payload is projected onto the view causal from the start; to the host, after commit, it is projected onto the stable state final. Both projections belong to the same occurrence. The stabilisation it also requires that there be no consequences/ocurrencias pending cases.
