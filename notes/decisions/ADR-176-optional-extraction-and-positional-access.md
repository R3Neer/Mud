---
id: D-176
title: Optional extraction and positional access
status: current
date: 2026-10-15
supersedes: []
superseded-by: []
questions: []
affects:
  - Lexicon, grammar, syntax, expression typing and collection construction
---

# ADR-176 — Optional extraction and positional access

## Decision

T [?] abbreviates T [0..1]. C[?] requires static upper cardinality at most one;
one member extracts that complete member and zero produces non-storable
omission. It never picks from a possibly multi-member source, flattens nested
members, converts a computing fault to absence or grants authority.

Omission propagates through dependent access, operators, construction and calls,
including from call arguments. Retain normative evaluation order: prior demanded
work/faults remain, and pending dependent operands are skipped. Optimization
may avoid earlier work only with an observational-equivalence proof. An omitted
assignment/update performs no write, not assignment of empty, and other block
statements continue. No rollback of earlier effects or implicit block exit.

Collection literals consume omitted complete elements; comprehensions consume
omission for that one emission. An ordinary empty collection result remains a
member. A possibly omitted non-Boolean initializer or required result cannot
escape its owner: reject missing definite initialization/result statically,
even for a zero-admitting destination. Wrap an optional emission in a collection
construction to obtain an ordinary possibly empty result. Boolean contexts use
the existing structural pruning core, including negation, and/or, derived
transparency and closing a wholly erased ordinary Boolean result to true.

C[*] accesses the last observable position and C[1] the first. Empty collections
produce ordinary optional absence; neither access itself propagates omission.
No [..*] or [*..] extreme sugar. Anonymous tuples admit static in-range component
indices and [*] for their last component. Dynamic component indices and indices
outside arity are static errors. Collection-of-tuple access selects the outer
member first. [?] extracts the optional whole tuple, not one component; a
mandatory tuple's [?] is redundant. No automatic extension of component indexing
to arbitrary aliases or dictionaries is approved.

## Relations and verification

Partially amends D-081, D-100, D-169 and D-172. Preserve stored-cardinality proofs,
required handler results and already pending Errors; omission handles no Error.
Finite supplied outcome/shape certificates cover demand, faults, omission
boundaries, nested empty members and constant tuple access, not a parser/runtime.
