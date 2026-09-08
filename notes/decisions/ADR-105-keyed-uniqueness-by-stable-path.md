---
id: D-105
title: "Keyed uniqueness by stable path"
status: current
date: 2026-09-08
supersedes: []
superseded-by: []
questions:
  - "Q-006"
affects:
  - "collections, collection transformations, dictionaries, algebra, grammar, Surface AST, diagnostics, provenance and concurrent insertions"
---

# ADR-105 — Keyed uniqueness by stable path

- Extends: [[ADR-039-collections-and-dictionaries|D-039]] and [[ADR-064-ordering-by-stable-path|D-064]].
- Modifies: [[ADR-037-fields-and-declarative-domains|D-037]], [[ADR-046-algebra-and-conflicts-of-effects|D-046]], [[ADR-049-operators-precedence-and-standardised-intervals|D-049]], [[ADR-075-enumerable-domains-all-and-derived-value-form|D-075]], [[ADR-080-higher-order-collection-algebra-and-updates|D-080]], [[ADR-081-collection-filtering-take-and-indexing|D-081]], [[ADR-085-functional-dictionaries-metadata-and-structured-activation|D-085]], [[ADR-086-exact-nominal-identity-external-arrows-and-dictionary-algebra|D-086]], [[ADR-100-logical-order-provenance-membership-and-effect-consolidation|D-100]] and [[ADR-102-complete-form-of-computed-family-data|D-102]].
- Related question: [[../questions/Q-006-c-conflicts|Q-006]].

## Context

MUD already distinguishes multiplicity from ordinary `unique`, retains stable provenance for occurrences and uses a stable member path for `ordered by`. Some models need a stronger invariant: several distinct values may be permitted in general, but only one may survive for each stable semantic key such as an e-mail address, external identifier or owning `thing`.

## Decision

### One uniqueness axis

A collection has exactly one of these effective uniqueness modes:

```text
non-unique
unique
unique by path
```

`unique` retains at most one occurrence of each whole value under the value's semantic equality. `unique by path` evaluates `path` from each member and retains at most one occurrence for each semantically equal key. The two spellings are alternatives on one axis: writing more than one uniqueness modifier, including `unique unique by p` or two `unique by` criteria, is a contextual syntactic error.

Keyed uniqueness implies ordinary whole-value uniqueness because equal values necessarily produce equal stable keys, but the keyed criterion remains part of the collection contract because it changes future insertion, normalisation and algebra.

### Stable key path

`unique by` accepts the same non-empty path shape as `ordered by`: fields, components or associated data reached from each member. Every intermediate access must be singular and resolve unambiguously, and the entire path must be transitively stable for the lifetime of the collection value. On a union member type, every reachable alternative must provide the path and the final key must elaborate to one common equality-compatible type through the ordinary allowed widening rules.

The final key needs semantic equality, not a total order. Therefore a `thing` may be a valid final `unique by` key even though it is not by itself a valid `ordered by` key. `ordered by` keeps its existing total-order requirement.

### First occurrence survives

Keyed normalisation traverses occurrences in stable provenance order. For each semantic key, the first occurrence survives and later occurrences with the same key are discarded. The survivor is not selected by source spelling, nominal name, implementation identity, hash order or a last-write-wins rule.

For either uniqueness mode, a collection literal contextually intended for that mode and whose collision can be proved at compile time is normalised immediately and produces a non-blocking warning. The diagnostic identifies the exact retained source occurrence and the colliding later occurrence or occurrences. Cardinality is checked after that normalisation, exactly as with ordinary `unique`. This literal-construction rule does not turn a value declaration into a coercion: an already-computed collection assigned to a declared uniqueness contract is verified rather than rewritten, in accordance with D-100. Local and derived transformations remain coercive as defined below.

```mud
members: Person [* unique] = [Alice, Alice]
contacts: Person [* unique by email] = [Alice, Bob]
```

When the compiler can prove `Alice.email == Bob.email`, the second declaration retains `Alice` and warns that `Bob` is discarded by the keyed-uniqueness criterion.

### Updates and removals

Adding or inserting a value into `unique by path` is a no-op when the collection already contains an occurrence with an equal projected key. It produces neither `failed` nor a replacement. `remove` retains its existing value-based meaning; keyed uniqueness does not turn it into removal by projected key.

For compatible concurrent insertions, semantically equal values may first merge as already required for ordinary `unique`. Distinct values with the same keyed-uniqueness key do not merge and do not conflict. Their stable provenance relation is completed using the existing reproducible causal rules, and the earliest occurrence survives. All causes of an already merged equal occurrence remain attached to that occurrence.

### Local and derived transformations

`unique by path` is admitted wherever collection uniqueness can be written, including derived collection shapes and local collection transformations. The normalisation order remains:

```text
domain restriction -> uniqueness -> order -> cardinality
```

A local keyed transformation therefore removes later equal-key occurrences before any `ordered` or `ordered by` transformation and before upper-cardinality truncation.

Filtering, selection, `take`, ordered indexing and other operations that return a subset of existing occurrences preserve the exact uniqueness criterion because they cannot introduce a new key collision and preserve the surviving occurrences' provenance.

### Collection algebra

Collection `|`, `&`, `--` and `^` remain defined over whole-value multiplicities. They do not silently change their content operation into a keyed merge merely because an operand uses `unique by`.

Let `N` mean no uniqueness guarantee, `V` ordinary whole-value uniqueness and `K(p)` keyed uniqueness by resolved path `p`. Every `K(p)` also guarantees `V`.

The conservative result rules are:

- `A | B` guarantees `V` exactly when both operands guarantee at least `V`; it does not retain `K(p)` merely because both operands use the same `p`, because distinct values from opposite operands may share that key.
- `A & B` preserves `K(p)` when at least one operand guarantees `K(p)` and the other operand has no different keyed criterion. If both operands have different keyed criteria, the canonical exposed guarantee is `V`, although the concrete result is a subset of both. With no keyed criterion, the existing rule remains: `V` is guaranteed when either operand guarantees it.
- `A -- B` preserves the exact uniqueness mode of `A` because it only removes occurrences from the left operand.
- `A ^ B` requires both operands to guarantee at least `V` and conservatively produces `V`. A keyed criterion is not generally preserved across the two exclusive sides.

Analysis may strengthen these conservative results when it proves that cross-operand keyed collisions are impossible. It may never claim a keyed criterion by choosing arbitrarily between two incompatible paths.

### Dictionaries

Dictionary keys remain intrinsically unique and are not reinterpreted by this feature. A written uniqueness modifier on a dictionary continues to constrain associated or produced **values**.

In an exact dictionary, `unique by path` interprets `path` from the associated value. An insertion or replacement whose projected value key is already represented under another dictionary key is a complete no-op, just as an ordinary `[unique]` value collision already is. A statically provable collision inside a contextual exact-dictionary literal follows the same first-association warning rule.

For exact-dictionary algebra, let `N`, `V` and `K(p)` have the meanings defined for collections, while remembering that the operators first select associations by **dictionary key**:

- `L | R` guarantees `V` exactly when both operands guarantee at least `V`; it does not automatically retain `K(p)`, even for the same path, because distinct values introduced from opposite operands may share that projected key.
- `L & R` preserves the exact uniqueness mode of `L`, because it filters `L` by key and retains `L`'s associated values. A uniqueness guarantee of `R` alone says nothing about those retained values.
- `L -- R` preserves the exact uniqueness mode of `L` for the same reason.
- `L ^ R` remains admitted regardless of associated-value uniqueness because exact symmetric difference is defined on dictionary keys. Its result guarantees `V` exactly when both operands guarantee at least `V`; otherwise it is `N`. It does not automatically retain `K(p)` across the two exclusive sides.

Analysis may strengthen these conservative guarantees only when it proves the necessary absence of projected-value collisions. Whenever the inferred exact-dictionary result has a value-uniqueness criterion, candidate associations are incorporated in D-086's established order and any later association violating that criterion is omitted as a no-op. In particular, the exact-dictionary `&` rule deliberately differs from ordinary collection `&`: the former keeps left associated values, while the latter is a subset of both operand values.

In a functional dictionary, `unique by path` normalises the result collection of each application. In `FirstMatch` it is valid but redundant because at most one result is produced; tooling suggests its removal. In `AllMatches`, equal projected keys are deduplicated by stable result-occurrence provenance without changing which branches applied. Pointwise functional-dictionary algebra then follows the ordinary collection rules above.

## Consequences

- Surface syntax reuses the existing reserved words `unique` and `by`; the lexicon gains no keyword.
- The shared syntactic path is no longer order-specific and is represented as a collection key path.
- The Surface AST represents uniqueness as a sum rather than a Boolean flag, and local transformations likewise retain whether uniqueness is ordinary or keyed.
- Keyed uniqueness is an invariant over values, not a hidden ordering rule.
- A keyed collision is deterministic normalisation, not a conflict.
- The final-key requirements of `unique by` and `ordered by` intentionally differ: equality versus total order.

## Rejected alternatives

- Rejecting equal-key values as an error or runtime conflict.
- Letting the last occurrence replace the first.
- Treating ordinary and keyed uniqueness as independent simultaneous modifiers.
- Requiring total ordering for a keyed-uniqueness key.
- Applying a dictionary's `unique by` path to its dictionary key rather than its associated/result value.
- Silently keyed-normalising ordinary collection union or symmetric difference in order to preserve `K(p)`.

## Verification

1. Ordinary `unique` remains unchanged.
2. Simple and nested `unique by` paths, including a final `thing` key that is equality-comparable but not orderable.
3. Rejection of two uniqueness-axis modifiers.
4. Static literal collision warning naming the retained occurrence and cardinality failure after normalisation.
5. Sequential `add` no-op on an existing key and value-based `remove`.
6. Concurrent distinct equal-key insertions selecting the earliest stable provenance without conflict.
7. Local transformation order: domain -> keyed uniqueness -> order -> cardinality.
8. Union-path totality and equality compatibility without a total-order requirement.
9. Conservative uniqueness inference for `|`, `&`, `--` and `^`, including different keyed criteria.
10. Exact-dictionary projected-value collision no-op, result-uniqueness inference for `|`, `&`, `--` and `^`, and functional `AllMatches` keyed result normalisation.
