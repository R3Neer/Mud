---
id: D-100
title: "Logical order, provenance, membership and effect consolidation"
status: current
date: 2026-08-29
supersedes: []
superseded-by: []
questions:
  - "Q-006"
  - "Q-032"
affects:
  - "aliases, collections, membership, grammar, syntax, randomness, effects, waves and conflicts"
---
# ADR-100 — Logical order, provenance, membership and effect consolidation

- Modified by: [[ADR-103-inner-capability-in-derived-values|D-103]].

- Modified by: [[ADR-101-bloques-de-valor-variables-locales-almacenadas-and-extremos-por-testigos|D-101]].

- Modifies: [[ADR-019-mutability-orthogonal-to-collection-and-members|D-019]], [[ADR-023-consolidation-of-concurrent-structural-effects|D-023]], [[ADR-037-fields-and-declarative-domains|D-037]], [[ADR-038-close-knit-families-with-strong-values|D-038]], [[ADR-039-collections-and-dictionaries|D-039]], [[ADR-043-speculative-query-with-allowed|D-043]], [[ADR-046-algebra-and-conflicts-of-effects|D-046]], [[ADR-048-reproducible-randomness-and-errors|D-048]], [[ADR-049-operators-precedence-and-standardised-intervals|D-049]], [[ADR-057-concrete-grammar-precedence-and-continuation|D-057]], [[ADR-064-ordering-by-stable-path|D-064]], [[ADR-080-higher-order-collection-algebra-and-updates|D-080]], [[ADR-084-alias-specialisation-inherited-members-and-derived-views|D-084]], [[ADR-085-functional-dictionaries-metadatos-and-activation-estructurada|D-085]], [[ADR-088-iteration-signed-progressions-and-expression-blocks|D-088]] and [[ADR-096-modulos-callables-look-message-and-activation|D-096]].
- Related questions: [[../preguntas/Q-006-c-conflicts|Q-006]] and [[../preguntas/Q-032-a-reproducible-randomness|Q-032]].

## Context

MUD already distinguishes ordered and unordered collections, concurrent effects computed from a common snapshot and canonical structural composition. The logical persistence of order, the provenance needed to order values without a common comparator, local collection transformations, Boolean membership and several concurrent-consolidation rules remained to be unified.

## Decision

### Inherited field refinement

An inherited stored field may refine its contract only when it is externally immutable. A stored field with outer `mut` is invariant: its contract cannot be narrowed or widened by specialisation.

An inherited derived field may refine its contract. If it comes from a single original member it retains its defining expression; the descendant only strengthens the effective contract. Type, domain, cardinality, `unique` and order are admitted only when the new contract is substitutable for every relevant inherited contract.

### Logical order and provenance

The order of an `ordered` collection is part of its logical value throughout its existence. It is not reconstructed when an operation decides to observe it. Filtering, selection, copying, assignment, value passing, viewing, serialisation or loading that preserves order must carry the same logical sequence unless the operation expressly declares that it removes or replaces that order.

Each occurrence also retains stable provenance when it may become semantically relevant. Provenance is distinct from current logical order: an unordered collection has no logical sequence but may retain occurrence provenance. Filtering or removal preserves the provenance of surviving occurrences; reordering changes the logical sequence, not provenance identity; a new occurrence receives new provenance. An implementation may omit this information physically only when it proves that it will never be observable.

Every operation whose semantics depend on order consumes the collection's logical order, not hash order, physical traversal or materialisation order. No special domain priorities replace this principle.

### Local collection transformations

A collection specification applied locally to an expression transforms the temporary value. In value declarations, the contract is verificatory and never transforms the value. In derived declarations, the written nominal or structural type is checked statically, while domain, cardinality, `unique` and order declared in the derived form, whether or not an explicit type exists, are coercive over the result and use the same normalisation as the equivalent local transformation.

Local transformations are normalised, regardless of the modifiers' textual order, in this order:

1. domain restriction;
2. `unique`;
3. establishing or replacing order;
4. cardinality.

Local domain restriction uses the form:

```mud
people in Adults
```

and filters out members that do not belong to the domain. `unique` removes repeated occurrences. `ordered by path` establishes order by the indicated key and uses stable provenance to break equal-key ties. `ordered` uses the complete type's intrinsic total semantic order when one exists; if the complete type has no common total comparator, it uses the provenance of all occurrences. No order is invented between union branches by textual position, nominal name, internal tag or implementation identity.

An upper cardinality bound truncates after filtering, deduplication and ordering. A lower bound requires enough members to exist and never manufactures members. A local transformation cannot introduce inner `[mut]` capability or any authority not possessed by the source expression. In a derived form, `[mut]` is therefore a capability requirement: it may be preserved through transformations retaining the semantic identity of the same `thing` values, but is never obtained by coercion.

Writing a local exact cardinality that would be indistinguishable from indexing retains indexing as the short form; the exact transformation may be written as a degenerate interval, for example `[2..2]`. A specification containing `unique` or `ordered` is unambiguously a transformation.

### Boolean membership

Boolean membership is written with the container on the left:

```mud
inventory has Key
inventory has not BrokenKey
0..100 has score
```

`has` is a reserved word and `has not` is the canonical negation. `in` is not a Boolean membership operator: it remains for restrictions, filters, domains, bindings and conversions where applicable. `not in` is not part of current Boolean membership.

### Concurrent insertions and provenance order

When compatible concurrent insertions need to complete a provenance relation and no natural semantic criterion prefers one over another, MUD uses a reproducible pseudo-random choice based on the same semantic seed system as the language's other random points. The choice point has stable semantic identity and does not depend on accidental sequential consumption of a global PRNG, the scheduler, physical arrival order, hashes, machine time or source order between concurrent `then` blocks.

The choice produces a linear extension of the causal partial order: it respects every real causal relation and decides only between concurrent occurrences. It is chosen over the complete concurrent group; it is not implemented through independent pairwise random comparisons that could introduce cycles. Once fixed, the result becomes part of stable provenance and is not redrawn when a collection is observed or later transformed to `ordered`.

In a `unique` collection, equivalent concurrent insertions are merged before completing order. The surviving occurrence retains all causes jointly, without selecting a winning cause. An acyclic causal relation is induced over surviving occurrences, preserving the semantically valid causal constraints of all merged causes; only then is any missing order completed reproducibly. The representation or concrete algorithm used to obtain that induced relation is an implementation detail so long as it preserves these properties.

### Concurrent arithmetic normal form

Concurrent arithmetic effects on the same target are normalised into three accumulators:

- `Δ`: signed sum of all `+=` and `-=` operations;
- `P`: product of all `*=` factors;
- `Q`: product of all `/=` divisors.

The canonical application is:

```text
x' = ((x + Δ) * P) / Q
```

with identities `Δ = 0`, `P = 1` and `Q = 1`. The additive family is applied before the multiplicative family. `/=` is not modelled through a mandatory inverse, and no intermediate divisions or roundings arising from arbitrary ordering between concurrent effects are introduced.

Multiplicative and divisive factors are cancelled when the type's laws guarantee that cancellation preserves semantics exactly, including the accepted case `*= 3` together with `/= 3`. A simplification cannot hide division by zero, overflow, domain violations, units or any other observable property. An invalid consolidated denominator produces the failure applicable to division of the type and the transition is reverted.

Concurrent assignments to the same value remain compatible; assignments to different values are a conflict. An assignment mixed with an arithmetic update remains a conflict.


### Consolidation of local `for each` accumulators

A mutable local outside a `for each` may be written by its iterations. If the source has semantic order, iterations are sequential and each observes the value left by the previous one. Without semantic order, all start from the same prior projection and their slot modifications are consolidated as concurrent using the same algebraic rules as equivalent effects. Thus several compatible `+=` operations may form a reduction, whereas `x = x + value` produces concurrent absolute assignments and receives no special accumulator semantics.

The slot remains local-frame storage, not world state; applying the same algebra does not turn local mutation into a persistent effect.

### General consolidation rule

Effect consolidation follows three levels:

1. within one class, algebraic combination, idempotent combination or specific normalisation is used where defined;
2. between different classes, a canonical language composition is used where declared;
3. if neither exists, the coincidence is a conflict.

Conflict is not inferred merely because two effects appear to express opposing intentions, nor compatibility by analogy with another family.

For concurrent structural effects, canonical composition is retained:

```text
create → add → remove → destroy
```

This order is declarative delta normalisation, not an observable temporal sequence. Thus `create X || destroy X` leaves `X` absent and `add A || remove A` leaves `A` removed. `unique` does not change this rule. Within a single `then`, however, textual order represents local sequentiality: `destroy X; create X` ends by requesting activation, while `create X; destroy X` ends by requesting destruction. A history such as creating, working with and destroying an entity must be expressed causally, not inferred from independent concurrent effects.

### Conflict diagnostics

A true conflict that the compiler proves inevitable is a static error. If it proves that the conflict is possible but not inevitable, it emits a warning. If it proves that targets cannot coincide or that effects consolidate compatibly, it emits no conflict diagnostic. If a warned or statically undecidable conflict materialises at runtime, resolution produces `failed` and complete rollback.

Analysis may exploit the explicit graph of rules, actions, subactions, bindings, types, domains, guards and causality. The minimum power every implementation must achieve remains open.

## Consequences

- The parser and AST distinguish `has`/`has not`, local `in` restriction and `binding in source : predicate` selection.
- The AST no longer represents Boolean membership through `Membership`/`NotMembership` associated with `in`.
- Local transformations retain their own representation and do not admit `mut`.
- Provenance is per occurrence, not only per value.
- Runtime must identify consolidation random points stably and complete order while respecting causality.
- Arithmetic consolidation no longer treats compatible additive/multiplicative mixing as a conflict and applies `(Δ, P, Q)`.
- Structural consolidation exposes no intermediate states between concurrent deltas.

## Rejected alternatives

The following are rejected:

- `in` and `not in` as Boolean membership;
- ordering heterogeneous branches by textual order, tags, names or accidental identities;
- a universal total order over all concurrent effects based on source, anchors, hashes, producers or scheduler;
- indefinitely deferring simultaneous insertion order until a later operation observes it;
- pairwise random comparators to construct order;
- selecting a different winning assignment through randomness, source position or implicit priority;
- configurable local `latest wins` policies, priorities or conflict resolution;
- converting every concurrent division into multiplication by inverses;
- automatically treating `add A || remove A` as a conflict;
- interpreting `create → add → remove → destroy` as observable time;
- allowing a local transformation to manufacture `[mut]` capability.

## Open questions

Q-006 remains partially decided. Families for which no concrete algebraic combination or canonical composition has yet been fixed remain open, including remaining cases of dictionaries, properties, structural cardinality and partially overlapping write-back. The mandatory minimum precision of static conflict analysis also remains unfixed. Q-032 remains partially decided only for caching and retry rules and exposure of stochastic results; the concrete derivation or sub-seed algorithm needs no additional decision while it preserves the semantic contract already fixed.

## Verification

Conformance must cover at least:

1. inherited refinements that strengthen guarantees and rejection of those that remove capability;
2. persistence of logical order through filters, copies and assignments;
3. intrinsic order of totally orderable types and provenance fallback for heterogeneous types;
4. local normalisation domain → `unique` → order → cardinality and rejection of local `[mut]`;
5. `has` and `has not`, with rejection of `in` as Boolean membership;
6. prior merging of `unique` insertions and reproducible causal-respecting linear extension;
7. arithmetic form `(Δ, P, Q)`, valid cancellations and preserved failures;
8. conflict between distinct assignments and between assignment and arithmetic;
9. structural composition `create → add → remove → destroy` and its distinction from sequentiality within a `then`;
10. error, warning, absence of diagnostic and runtime `failed` according to what can be demonstrated.
