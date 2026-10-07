---
id: D-040
title: "Semantics remaining basic numeracy"
status: current
date: 2026-07-28
supersedes: []
superseded-by: []
questions:
  - "Q-001"
  - "Q-019"
affects:
  - "future `07-lexicon.md`, future `11-type-system.md`, future `18-domains-and-intervals.md`"
---
# ADR-040 — Semantics remaining basic numeracy

- Read more: D-028, D-030, D-034
- Amended by: [[notes/decisions/ADR-060-additive-deltas-and-nat-normalisation|D-060]]
- Related questions: Q-001, Q-019
- Documents affected: future `07-lexicon.md`, future `11-type-system.md`, future `18-domains-and-intervals.md`

- Amended by: [[ADR-129-unbounded-exact-numbers-and-money-operators|D-129]].

## Decision

### Exact extensions

Implicit expansions are permitted:

$$
\mathsf{Nat}
\longrightarrow
\mathsf{Int}
\longrightarrow
\mathsf{Num}
$$

They do not extend to `Rum` nor to `Money`. A mixed operation uses the least-expanded common exact representation. Narrowing operations require `to`.

### `Nat`

A purely arithmetic operation that would result in a negative integer under this representation `Nat` reset to zero before checking the domain stated.

This saturation does not apply to `to Nat`: D-030 requires rounding and then validation, without corrective saturation.

D-060 distinguishes the effects from the pure operations `+=` and `-=`. These produce signed integer deltas; the deltas are added before saturation, and only then do they form the next `Nat` value. They therefore cannot be expanded into an assignment that applies saturated subtraction separately.

### `Money`

`Money` uses exact decimal arithmetic with two decimal places. The context provides the type of its clauses.

When an operation or conversion needs to be scaled down, the policy overall number of draws set by D-034. Nat/Int/Money have no language-level integer bound. Money scaling and ratio signatures follow chapter 21; magnitude dimensions remain independently checked.

### Number separators

`_` You can group figures for clarity, including exact forms and `Rum`:

```mud
1_000
r1_000
```

It does not alter the value. The precise rules governing permitted positions and diagnoses are set out in Q-001; the standard examples are grouped in threes.

### Typed intervals

The nominal form of type The interval is:

```text
Nat Interval
Int Interval
Num Interval
Rum Interval
Money Interval
```

Interval values are normalised with respect to the set they denote. D-029 governs limits and D-034 prohibits the listing of intervals `Rum`.

## Consequences

- The inference Exacta does not permit approximate mixing.
- Saturation of `Nat` and domain validation are different stages.
- `Money` stop relying on lexical suffixes.
- The IR must preserve value, not written separators.

## Future verification

1. Exact expansion chain.
2. Rejection of implicit mixing between `Rum` and `Money`.
3. Saturation of pure arithmetic of `Nat`, consolidation preliminary analysis of additive deltas and non-saturation of `to Nat`.
4. Scaling and rounding of `Money`.
5. Valid and invalid separators.
6. Normalisation of interval types.

