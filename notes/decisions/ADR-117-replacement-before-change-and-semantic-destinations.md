---
id: D-117
title: Replacement before change and semantic destinations
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions:
  - Q-002
  - Q-006
  - Q-046
affects:
  - Language contracts and their developed normative surfaces
---

# ADR-117 — Replacement before change and semantic destinations

- Formalised/amended by: [[ADR-128-sequential-effects-and-staged-consolidation|D-128]].

- Amended by: [[ADR-125-instruction-local-lifecycle-no-ops|D-125]].

- Formalised by: [[ADR-123-static-capabilities-and-conflict-proof-boundaries|D-123]].

## Context

The author accepts replacement before change, disjoint component composition, dictionary deletion precedence and generation-bound writes. This amends D-046, D-098 and the concurrent dictionary scope of D-039/D-100. Runtime field schema changes remain excluded by D-111.

## Decision

A sequential then keeps textual semantics over its private projection. Normalize each branch before merging sibling deltas: an absolute replacement supersedes preceding local contributions to that destination, while subsequent relative updates remain. Never resurrect an overwritten local update during concurrent consolidation. Siblings evaluate RHS expressions on their common snapshot and cannot observe one another's private deltas.

Concurrent equal complete replacements merge; unequal complete replacements conflict. A replacement supplies the base for surviving relative updates. Numeric operations preserve each branch's textual sequence; stage k combines the kth surviving operation of each branch at that destination, using ((base + delta) * P) / Q within that stage. An assignment x = old x + 5 is an absolute replacement, not interchangeable with x += 5. Nat projects/saturates only after combining signed deltas under its existing rule.

Semantic destinations retain their root, dictionary keys, stored component path and materialisation generation. Reconstructing two distinct alias components does not manufacture two conflicting whole-root assignments: preserve their independent intents and merge them before one immutable write-back. A whole-container replacement precedes descendant changes when the replacement supports the same well-typed path and nominal contract. Unequal replacements of the same semantic component conflict. A structurally invalid path or insufficient authority is rejected during elaboration.

Exact dictionaries compose different keys. On one key, equal whole-value replacements merge, unequal ones conflict, a whole-value replacement precedes compatible partial changes, and disjoint partial components compose. Repeated deletion is idempotent; deletion wins over insertion, replacement and partial modification for the same association. Intermediate missing-key partial paths remain no-ops as determined by the branch's actual read view: another branch inserting that key does not resurrect a missing partial update. Direct complete key assignment may insert. Dictionary add retains its existing complete-association insertion/replacement contract, including key replacement when the resulting contract is valid.

Value uniqueness is checked over the joint candidate dictionary, allowing an atomic swap of two distinct values. Untouched existing associations have priority over proposed associations colliding with them; among conflicting proposed associations retain earliest stable provenance. Stable provenance uses the existing reproducible causal-order completion, not source or scheduler order. Reject a losing association proposal as a whole no-op, restoring its previous association if present. Recompute collisions after restoration; every pass permanently rejects at least one remaining proposal, so termination is bounded by the finite proposal count. Restored associations count as unchanged and may force other proposals to become no-ops. Valid original state guarantees a collision-free fallback. Final domains/cardinalities still must hold; uniqueness normalization cannot excuse their violation. This procedure applies to association insertion/replacement and partial association changes, not to silently repairing an invalid full dictionary assignment.

Homogeneous collection algebra and Text ordering retain their existing rules. Heterogeneous collection updates lacking a specified canonical composition conflict. This decision does not invent a universal ordering over every effect. Structural activity/membership consolidation retains create -> add -> remove -> destroy as an unobservable semantic order.

Every stored write targets the materialisation generation observed by its branch. Destruction closes that generation and discards its own load; writes aimed at the destroyed generation never carry into a fresh materialisation. A sequential destroy/create may initialize the new generation and write there in the same branch, under lifecycle admission rules. Suspension preserves independently owned load and is not destruction. Lifecycle admission is instruction-local: create on explicitly active and destroy on explicitly inactive are successful no-ops, without suppressing the surrounding effects.

Static analysis reports proven inevitable conflict as an error, proven possible conflict as a warning and proven compatible/disjoint effects without a conflict warning. Runtime conflict rolls back under the structured-error protocol. Domain checking remains mandatory at initialization/write; cardinality analysis retains its stricter proof obligations for complete then results and possible consolidations. D-123 and chapter 15 specify the minimum proof and residual-runtime boundary. No complete solver for arbitrary symbolic destinations or unstated scheduler priority is required.

## Verification

- Concurrent x = 10 and x += 2 produce 12; x = 10 versus x = 11 conflicts.
- Sequential x += 2; x = 10 discards that local delta before merging.
- Independent profile.name/profile.age edits merge; replacing profile precedes compatible partial edits.
- Same-key deletion wins, and absent-key partial changes remain no-ops despite sibling insertion.
- Swapping a -> Red, b -> Blue into a -> Blue, b -> Red passes joint uniqueness.
- Restoring a rejected replacement rechecks newly created collisions and terminates.
- An old-generation write cannot survive destroy/create; unrelated suspended load survives.

## Integration review

Assignable-path syntax and AST remain reconstructible expressions; semantic leaf intents belong to elaboration. The developed mathematical and grammar explanations reflect overlapping writes and generation identity. No new field, scope or anchor is introduced; nominal HIR needs no effect representation. Chapter 28 defines private effect judgments, normalisation and finite root/wave batch consolidation; complete scheduling and invocation/evaluation implementations remain separately scoped.
