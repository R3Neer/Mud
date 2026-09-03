---
id: D-043
title: "Consulta especulativa `allowed`"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-007"
  - "Q-032"
  - "Q-035"
  - "Q-053"
affects:
  - "expresiones, acciones, análisis de admisibilidad"
---
# ADR-043 — Consulta especulativa `allowed`

- Amended by: [[ADR-100-orden-procedencia-pertenencia-y-consolidacion|D-100]].
- Related questions: Q-007, Q-032, Q-035, Q-053
- Documents concerned: expressions, actions, analysis of admissibility

## Context

A rule must be able to check whether a action would be admissible without implementing a simplified version of it or altering the world.

## Decisión

```mud
allowed game.Move(origin, destination)
allowed (source, destination).Transfer(amount)
```

`allowed call` assesses the action specified using the same complete protocol as a request the original, but in a speculative copy:

1. brings participants together;
2. provides and validates `given`;
3. assesses `if`;
4. calculates and consolidates the root;
5. generate waves until they stabilise;
6. check `always`;
7. assesses `after`;
8. Discard the copy.

The translation of result is:

$$
\begin{aligned}
\mathsf{accepted} &\mapsto \mathsf{true},\\
\mathsf{rejected} &\mapsto \mathsf{false},\\
\mathsf{failed} &\mapsto \text{fallo propagado}.
\end{aligned}
$$

A failure it is not downgraded to ‘false’.

Speculative valuation does not alter the world, the queue actions, logs, global randomness or the identifier for resolution. If chance comes into play, use a branch concrete, established and reproducible, which does not consume the branch of the actual execution.

When the action declare a role `for` with mutability exterior, the receiver-the location is resolved within the speculative copy. Its effects never retain a reference to the world real.

`allowed` may appear in Boolean rules, `if`, `after`, `when`, rules `always` and quantifiers, always within a pure expression. The graph of departments of admissibility it must be acyclic.

## Consequences

- An implementation may reuse the standard transactional engine, replacing confirmation with discard.
- Cost or a resource limit cannot silently change ‘true’ to ‘false’.
- The identity semantics of each point random and its reproducible derivation from the seed have already been set. Q-032 maintains the cache rules, retry rules and result display; Q-035 retains its own characteristics of `allowed`.

## Verification

1. Correlation between the three results.
2. Equality of the internal trace between the actual and speculative executions with the same branch.
3. Absence of mutations, messages and global randomness.
4. Static rejection of cycles of admissibility.

