---
id: D-175
title: Historical order and local collection properties
status: current
date: 2026-10-15
supersedes: []
superseded-by: []
questions: []
affects:
  - Collection ordering, transformations and static result contracts
  - Derived normalization and occurrence provenance
---

# ADR-175 — Historical order and local collection properties

## Decision

Bare ordered always establishes the historical insertion/provenance order of
surviving occurrences, including after explicit key sorting. Key sorting never
rewrites that history. Deletion discards an occurrence; reinsertion creates a
new occurrence. Concurrent provenance retains its existing causal-respecting
reproducible completion, not physical arrival timestamps.

Filtering, deduplication, slicing and identity-preserving selection retain
survivor provenance. Comprehension results are new occurrences whose historical
sequence follows production order; they do not inherit an input occurrence's
old position through arbitrary computation. Unordered production uses stable
provenance enumeration, not physical worker completion or hash order.
Composition uses each operation's
specified operand provenance composition, not a global cross-collection clock.

Local suffixes admit unique, unique by path, ordered and ordered by path.
Mentioned axes replace their prior criterion; compatible unmentioned guarantees
and existing member authority are retained. No local mut modifier is admitted,
even to restate existing authority. Local cardinality transformations are not
admitted: a range index is a positional slice, not a cardinality contract.

Derived declaration contracts still normalize explicitly declared domain,
uniqueness, order and upper cardinality, then check the lower cardinality. Upper
bounds truncate and lower bounds never manufacture members. This is distinct
from stored destination verification. A local deduplication result has its own
bounds; it need not satisfy the source's minimum. Stored writes must prove the
destination cardinality, including the reduced distinct population.

Transformations produce collection values; views, persistent sharing, fusion
and storage reuse are implementation choices. In-place reuse is permitted only
when indistinguishable from producing the result before assignment, including
faults, aliases, coherent snapshots, provenance and authority. A self-assignment
spelling alone proves no ownership or reuse condition.

## Relations and evidence

Partially amends D-039, D-064, D-081, D-100 and D-173. D-174's extrema,
association replacement and functional/family distinctions remain applicable.
Take remains native during the ongoing construction audit; no library API or
unordered/shuffle operation is approved. First/last remain library conveniences,
with positional extreme access specified independently.

Supplied finite occurrence certificates distinguish current key order from
history, reordering from occurrence creation and dictionary replacement from
reinsertion. They do not implement a causal scheduler or collection runtime.
