---
id: D-048
title: "Reproducible randomness and errors"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-007"
  - "Q-032"
  - "Q-035"
  - "Q-058"
affects:
  - "expressions, effects, runtime and diagnostics"
---
# ADR-048 — Reproducible randomness and errors

- Amended by: [[notes/decisions/ADR-061-non-accepted-results-and-text-templates|D-061]]
- Expanded by: [[ADR-081-filtering-take-and-indexing-de-collectiones|D-081]]
- Amended by: [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]].
- Related questions: Q-007, Q-032, Q-035, Q-058
- Documents affected: expressions, effects, runtime, diagnostics

## Context

MUD allows for randomness, but does not permit this or errors to introduce platform-dependent results or to turn failed queries into falsehoods.

## Decision

MUD 1.0 sets out an explicitly random method of sampling:

```mud
Rand(source)
```

The source must be a collection o domain demonstrable. There are as yet no compelling arguments regarding weights, distributions or policy local.

D-081 add `take amount from source`. Based on a source with no discernible order and with more occurrences than `amount`, `take` is a point reproducible randomness even if I don’t write anything `Rand`: selects uniformly without replacement. It has the same identity, cache by snapshot and contextual constraints. When dealing with a well-organised source, or when there is no real choice, `take` It is deterministic and does not involve chance.

`Rand` It can intervene in three ways:

- stored field initialised randomly using `=`;
- computed field randomly using `:=`;
- sampling within a effect.

Everything point random has identity semantics and derives its result of a seed reproducible. A computed field 'random' remains the same result within the same snapshot evaluation. It cannot be read directly from Boolean rules, domains, `if`, `when`, `always` nor iteration filters.

`allowed` use a branch specific, planted and disposable. `eventually` quantifies existentially on outcomes with a positive probability in accordance with D-044.

The non-finite results of `Rum`, division by zero, an unavailable reference, an operation outside domain and any effect which cannot produce a state well-formed are errors. Within a action actually produce `failed` and rollback. Within `allowed` they spread like failure assessment purposes and do not amount to falsehood.

Each of these errors must have a diagnostic human `Text`. When it reaches the boundary of a action real, that one diagnostic forms the `reason` mandatory for its result `failed` in accordance with D-061.

Resource constraints and internal flaws in an implementation should not be confused with a `failed` semantic. Q-007 It must define their external representation and the exact boundary between the two categories.

## Consequences

- An implementation must not use machine time or evaluation order as a source semantics of chance.
- Everything point random possesses identity semantics stable, and its selection must be based on the seed reproducible and of that identity without relying on the accidental sequential consumption of a global PRNG. The specific derivation or sub-seeding algorithm is a matter of implementation, provided that it preserves that contract. Q-032 It keeps the cache and retry rules, as well as the display of results, active.
- The arithmetic portability of `Rum` continues at Q-058.
- The semantics errors within ordinary Boolean expressions, outside `allowed`, requires a table of regulations within Q-007.

## Verification

1. Repetition with the same seed and controlled divergence from another.
2. Stability of a computed field random within a snapshot.
3. Restrictions on conditions and filters.
4. Protection against speculative risk.
5. Rollback and fault propagation.
6. Acceptance of `Rand(source)`, rejection of additional signatures and contextual classification from `take` ordered or stochastic.

