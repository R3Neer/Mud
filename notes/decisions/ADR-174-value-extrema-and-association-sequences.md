---
id: D-174
title: Value extrema and exact-dictionary association sequences
status: current
date: 2026-10-15
supersedes: []
superseded-by: []
questions: []
affects:
  - Quantifier extrema, predicate demand and exact-dictionary ordering
---

# ADR-174 — Value extrema and exact-dictionary association sequences

- Amended by: [[ADR-175-historical-order-and-local-collection-properties|D-175]], [[ADR-176-optional-extraction-and-positional-access|D-176]] and [[ADR-178-structural-tuple-inputs-and-postfix-generics|D-178]].

## Decision

Min/max select least/greatest accepted witnesses by a defined total criterion,
not by arbitrary sequence position. Use a source's explicit ordered-by criterion
when present, otherwise the established total comparison of its witness type.
An exact dictionary's ordinary witness is its key. A bare sequence of things
without a usable key does not establish an extremum comparator.

For a source without explicit compatible key order, evaluate all required
predicate candidates in the ordinary source view before selecting an extremum.
Do not internally sort to omit predicates or infer early termination from an
accidental current sequence. A source explicitly ordered by the selected
criterion retains directional short circuit: min from the first end, max from
the last. Source construction, key validation and demanded errors remain
observable. Empty accepted population remains ordinary absence.

The author accepts full traversal without explicit compatible key ordering.
First/last are library/structure conveniences, not additional core quantifiers.
Their concrete library API is not designed here. D-176 separately defines star/optional indexing and D-178 defines zero-admitting
functional coverage; they do not turn first/last into new core quantifiers.

Bare ordered on an exact dictionary establishes historical association order
under D-175. Literal association order establishes it; a new sequential key
appends, replacing an existing value retains that key's position, and deleting
then reinserting creates a new position. Concurrent additions retain the
existing causal-respecting provenance contract. Key uniqueness, value uniqueness
and order remain independent; equality still compares associations rather than
physical storage or iteration order. Explicit key ordering remains distinct.

Ordered families retain member comparison; ordered functional policies retain
FirstMatch branch priority. Neither is redefined as association insertion order.

Partially amends D-039, D-047, D-100, D-101, D-164 and D-173. No compiler,
scheduler, library implementation or host adapter is introduced.

## Verification

Review mathematical extrema on [3,1,2], predicate faults on unsorted versus
explicitly sorted sources, empty populations and stable key ties. Verify
association order for replacement versus delete/reinsert. Finite witnesses
receive supplied source order, key and predicate premises; they are not source
evaluation or a new causal algorithm.
