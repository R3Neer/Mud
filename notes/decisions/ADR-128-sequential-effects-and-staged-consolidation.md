---
id: D-128
title: Sequential effects and staged consolidation
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions:
  - Q-002
affects:
  - "[[specification/25-effects]]"
  - "[[specification/14-fields-and-mutability]]"
  - "[[specification/07-concrete-grammar]]"
  - Effect conformance corpus and root/wave batch interface
---

# ADR-128 — Sequential effects and staged consolidation

## Context

The author confirms x *= 2; x += 3 from x = 5 gives 13, then accepts staged concurrent composition: A *= 2; += 3 and B *= 3; += 4 give 37. This specifies the boundary between textual sequencing and concurrent arithmetic normalisation and completes Q-002's effect-family scope.

## Decision

Evaluate each branch in textual order against its private projection. Freeze RHS results, destination identities/generations and provenance at their evaluation sites. Absolute replacement discards preceding contributions of that branch to the replaced destination; retain later relative contributions.

For one numeric semantic destination, surviving relative operations form each branch's local ordered sequence. Stage k groups the kth operation of every branch that has one. Apply the existing within-stage normal form ((base + delta) * P) / Q, then advance to the next stage. Unrelated destinations do not occupy a position in this sequence. Equal replacements supply one common replacement base; unequal replacements conflict. The stage rule does not reorder operations within one branch or reevaluate operands on a sibling's projection.

Preserve signed Nat accumulation rather than truncating pending deltas at stage boundaries or private reads. Private observations remain nonnegative. Pure Nat subtraction remains independently saturated. Other representations retain their established operation, rounding, domain and error laws; this rule invents no Money/Rum overload or missing arithmetic policy.

Other effect families retain their established canonical composition: homogeneous collection operations, semantic alias/component paths, exact dictionary association deletion and joint uniqueness, lifecycle admission and generations, causal outputs, finite traversal, action replies and block recovery. No universal source/scheduler priority or structural textual merge is introduced.

## Contrasting cases

| Common entry and branches | Result |
| --- | --- |
| 5; one branch *= 2; += 3 | 13 |
| 5; A *= 2; += 3, B *= 3; += 4 | 37 |
| 5; A += 2, B *= 3 | 21 |
| 5; A *= 2; += 3, B += 4 | 21 |
| 5; A changes an unrelated y before *= 2; += 3, B *= 3; += 4 | x remains 37 |
| 5; A += 2; = 10, B += 3 | 13; A's overwritten delta is not resurrected |
| 0 Nat; -= 2; += 3 | 1; private intermediate read is 0 |

## Integration and evidence

[[specification/25-effects]] defines private statement/effect judgments, all surviving AST effect families, branch normalisation, staged consolidation, dictionaries, lifecycle generations, root/wave batch validation and rollback/recovery boundaries. [[specification/effects/README]] records bounded executable witnesses and declarative boundary cases. This is not a full MUD interpreter, a complete scheduler, a foreign ABI or a general solver for termination/dynamic domains.

Amends D-117 and the sequential/concurrent arithmetic wording of D-100/D-046/D-060. D-023's obsolete admission and open-conflict claims are rewritten to current policy. Q-020/Q-023/Q-007/Q-069/Q-070 remain separately scoped.
