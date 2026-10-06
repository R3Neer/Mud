---
id: D-043
title: "Speculative query with `allowed`"
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
  - "expressions, actions and admissibility analysis"
---
# ADR-043 — Speculative query with `allowed`

- Amended by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].
- Related questions: Q-007, Q-032, Q-035, Q-053
- Documents concerned: expressions, actions, analysis of admissibility

- Developed by: [[ADR-110-tentative-wave-journal-and-atomic-confirmation|D-110]].

## Context

A rule must be able to check whether a action would be admissible without implementing a simplified version of it or altering the world.

## Decision

```mud
allowed game.Move(origin, destination)
allowed (source, destination).Transfer(amount)
```

`allowed call` assesses the action specified using the same complete protocol as a request the original, but in an isolated speculative projection with a disposable tentative journal:

1. brings participants together;
2. provides and validates `given`;
3. assesses `if`;
4. calculates and consolidates the root;
5. generate waves until they stabilise;
6. check `always`;
7. assesses `after`;
8. Always discard the tentative journal, even on acceptance.

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

When an action declares a `for` role with outer mutability, its receiver place is resolved within the speculative copy. Its effects never retain a reference to the real world.

`allowed` may appear in Boolean rules, `if`, `after`, `when`, rules `always` and quantifiers, always within a pure expression. The graph of departments of admissibility it must be acyclic.

## Consequences

- The reference implementation reuses the standard semantic transactional engine, replacing confirmation with unconditional discard. Physical copying is not required; isolated overlays may implement the projection.
- Cost or a resource limit cannot silently change ‘true’ to ‘false’.
- The identity semantics of each point random and its reproducible derivation from the seed have already been set. Q-032 maintains the cache rules, retry rules and result display; Q-035 retains its own characteristics of `allowed`.

## Verification

1. Correlation between the three results.
2. Equality of the internal trace between the actual and speculative executions with the same branch.
3. Absence of mutations, messages and global randomness.
4. Static rejection of cycles of admissibility.

