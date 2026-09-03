---
id: D-081
title: "Filtering, `take` and collection indexing"
status: current
date: 2026-08-04
supersedes: []
superseded-by: []
questions:
  - "Q-028"
  - "Q-032"
affects:
  - "collections, dictionaries, Text, domains, randomness, ordering, grammar and AST"
---

# ADR-081 — Filtering, `take` and collection indexing

- Modified by: [[ADR-103-inner-capability-in-derived-values|D-103]].

- Modified by: [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]]
- Modified by: [[notes/decisions/ADR-084-specialisation-de-aliases-inherited-members-and-derived-views|D-084]]
- Modified by: [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]]
- Modifies: [[ADR-039-collections-and-dictionaries|D-039]], [[ADR-047-quantifiers-and-finite-iteration|D-047]], [[ADR-048-reproducible-randomness-and-errors|D-048]], [[ADR-056-char-text-and-unicode-ordering|D-056]], [[ADR-064-ordering-by-stable-path|D-064]] and [[ADR-075-enumerable-domains-all-and-derived-value-form|D-075]].
- Related questions: [[notes/questions/Q-028-f-finiteness|Q-028]] and [[notes/questions/Q-032-a-reproducible-randomness|Q-032]].

## Context

`for each ... if ...` selects participants to produce effects, but does not build a reusable pure collection. Quantifiers consume witnesses to produce booleans or aggregates and `all` enumerates a complete domain; none of these forms returns the subcollection satisfying a predicate.

There was also no distinction between observable position, quantitative selection and reproducible random choice, without forcing `Rand` when the rule merely says to take some members.

## Decision

### Filtering as an expression

The form is:

```mud
player in players :
    player.score == 2
```

is a selection expression. It binds each enumerable member of the source, evaluates a pure deterministic predicate and returns the occurrences for which the predicate is `true`.

The binding may be simple or a dictionary pair, as in `for each`:

```mud
(key, value) in stock :
    value > 0
```

The variable is available only in the predicate. The source is captured when evaluation begins. It must be a finite enumerable collection; if the conceptual source is a domain, it is explicitly materialised as `all D` before selection. If finiteness or enumerability cannot be demonstrated, the expression is invalid.

The result:

- preserves the type and nominal identity of its members;
- preserves multiplicity and `unique`;
- preserves ordering and its criterion when the source is ordered;
- produces identities with provenance and preserves inner capability when the source guarantees it; an external derived form may require that capability, but cannot grant it when absent;
- never acquires external mutability;
- has conservative cardinality `[0..u]` for a source `[l..u]`, narrowable by analysis;
- can narrow alternatives through tests such as `is`.

On a dictionary, pair binding returns a dictionary containing the accepted associations.

### General `take` expression

The general form is:

```mud
take amount from source
```

`amount` must elaborate to a `Nat [1]`. The source must be finite and enumerable. If it contains $k$ occurrences and the amount is $n$, the result contains $\min(k,n)$ occurrences.

- `take 0 from source` produce `empty`.
- `take n from empty` produce `empty`.
- A lack of members never fails by itself; an external contract may require a greater cardinality.

For a source with static cardinality $[l..u]$ and a constant amount $n$, the result has:

$$
[\min(l,n)..\min(u,n)].
$$

If the source has observable semantic ordering or its own canonical enumeration, `take` preserves its prefix. If the source is a collection or dictionary without observable ordering, it selects uniformly and without replacement among occurrences using the reproducible seed. The result does not acquire ordering from the sample's internal order.

An unordered `take` is a random point even though it does not write `Rand`: it has semantic identity, snapshot caching and the same contextual restrictions. It is deterministic and consumes no randomness when `n=0` or when the source can be shown to contain at most `n` occurrences.

`take` also applies to:

- `all D` materialisations of finite enumerable domains, taking their first canonical values;
- dictionaries, preserving complete associations;
- `Text`, producing a prefix of up to `n` `Char` values as another `Text`.

A bare domain is not a direct source for `take`: when producing a collection, materialisation must be explicit in the programme.

The nominality of a container alias is not reconstructed implicitly: the result preserves the underlying collection or sequence and needs an explicit nominal construction or conversion when the context again requires the alias.

### Composition

`take` and selection are ordinary expressions and compose without exclusive syntactic sugar:

```mud
# Up to n matches.
best := take n from player in players :
    player.score == 2

# Matches within a previous selection.
best := player in take m from players :
    player.score == 2

# Both constraints.
best := take n from player in take m from players :
    player.score == 2
```

The declaration annotation is independent of the selection:

```mud
chosen [3] := take 3 from player in players :
    player.score == 2
```

`take 3` selects up to three; `[3]` requires exactly three.

### Indexing and sections

A collection admits positional access only when it has observable ordering. Indices start at one.

```mud
queue[1]
queue[2..5]
```

A singular index produces a `[1]` collection when the source cardinality proves that the position exists, and `[0..1]` otherwise. An index range produces the positions existing within the range and never fails for exceeding the end. It preserves ordering, multiplicity, member type and inner capability.

On an unordered collection, positional access is invalid; use `take` when the intent is to select a quantity. Dictionaries retain key indexing and `Text` retains sequence indexing; type resolution distinguishes these forms.

### `ordered by` over unions

When a collection member is a union, every `ordered by` path must be total over all possible alternatives:

1. Every segment exists in every reachable alternative.
2. Every intermediate access is singular.
3. The entire path is transitively stable.
4. Final keys elaborate to one common type with total semantic ordering.

Unique implicit widenings, such as `Nat` to `Int`, are admitted. Nominal alias identities are not removed and no choice is made among several conversions. If an alternative needs adapting, first declare a common calculated field and order by it.

## Consequences

- Queries can build groups defined by a rule without introducing mutable variables or auxiliary effects.
- `for each` remains the way to act on members; selection is the way to obtain them as a value.
- `take` expresses a general quantitative constraint and uses ordering or a seed according to source semantics.
- Indexing never invents positions for unordered collections.
- A union cannot make an `ordered by` key partial.

## Verification

1. Ordered and unordered filtering, `unique`, multiplicities and dictionaries.
2. Union narrowing within the predicate.
3. `take` over ordered and unordered collections, `all D`, dictionaries and `Text`, and rejection of a bare domain as a collection-producing source.
4. Sampling without replacement, reproducibility and snapshot stability.
5. Deterministic simplification when no real choice exists.
6. Composition of `take` before and after filtering.
7. Separation between selection and cardinality contract.
8. Ordered index and section, including out-of-range bounds.
9. Rejection of unordered positional indexing.
10. Total and invalid `ordered by` paths over union alternatives.

## Amendment by D-084

A selection used to define a derived field retains the inner capability of its source because it returns the same accepted identities. A `[mut]` view requires that capability to be available; the declaration does not manufacture it. The selected list remains stable during the snapshot and is recalculated after effects are consolidated.

## Amendment by D-088

Pure selection admits `item in source by step : predicate` when the source defines progression by difference. It is not a stride over an arbitrary collection. The predicate may be a short expression or an `ExpressionBlock` with locals and remains pure and deterministic. The AST retains `step?` and the predicate as an `ExpressionBlock`.

## Current amendment by D-096

Selection and `take` produce collections. When their conceptual source is a domain, it must be explicitly materialised through `all D`; for example `candidate in all Actions : ...` and `take n from all D`. Traversals and quantifiers that do not produce a collection may consume a finite enumerable domain directly.
