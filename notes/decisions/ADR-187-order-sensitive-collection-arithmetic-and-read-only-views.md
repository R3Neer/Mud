---
id: D-187
title: Order-sensitive collection arithmetic and read-only views
status: current
date: 2026-10-25
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/11-type-system.md
  - specification/13-aliases.md
  - specification/15-fields-and-mutability.md
  - specification/16-collections.md
  - specification/21-expressions.md
  - specification/README.md
  - specification/types
---

# ADR-187 — Order-sensitive collection arithmetic and read-only views

## Context

The author accepts arithmetic over multiple collections without requiring an
explicit comprehension. Observable order determines positional versus Cartesian
pairing. A general parameter must not change the calculation merely by omitting
an order requirement. Read authority and permission to write remain distinct.

## Decision

Binary +, -, *, / and % lift over admitted numeric and alias member operations.
At each collection layer, two semantically ordered values pair corresponding
positions and discard unmatched tails; otherwise every occurrence pair
contributes. Empty absorbs. Apply the same procedure recursively to explicit
nested collection layers, without flattening or a matrix-product convention.
Ordinary singleton member arithmetic is the base case, not another recursive
collection wrapper. A singleton with explicit order therefore differs in pairing
from one without order when its other operand is ordered and multiple.

Static overload selection and complete-operand priority remain unchanged.
All possible member alternatives must admit their operation, even for empty
inputs or currently discarded tails. Neither comparison nor set algebra gains
new member lifting. Existing compound-update effect laws are not extended by
this decision.

Omitted ordered/unique requirements hide guarantees, not the argument's actual
properties. Copying an ordered value preserves its sequence; an inferred binding
retains the known guarantee. Arithmetic chooses pairing using the retained
semantic order, never a hash order or merely hidden provenance. Unknown order
requires conservative result bounds covering both modes. Omitted inner mut
does not grant writes or permission to forward the hidden authority to a writable
parameter. Caller authority remains intact. No negative modifier is introduced.

Positional results retain pair order; Cartesian results do not acquire observable
order. No sorted-key guarantee is inferred without proof. Every selected pair
contributes once, with repetitions. Whole-value uniqueness requires proof of no
collisions among selected pair results; keyed uniqueness additionally requires a
valid stable result key and no key collisions. An equality-eligible result with
upper cardinality at most one is trivially unique. Operand uniqueness alone is
insufficient. Explicit [unique] normalization remains available.

Produce and validate operands under their existing demand/error contracts.
Execute member operations only for selected pairs; a discarded divisor zero
does not cause a division, but producing an invalid operand still fails.
Comprehensions express an explicitly different pairing; no new syntax is added.

## Consequences and integration

Partially amends D-080, D-149 and D-161. Their current effective text is updated
together with the canonical chapters and conformance evidence. Numeric
representations, dimensional admission, nominal identities, effect authority and
causal scheduling retain their separate contracts. No compiler or runtime is
implemented.

## Verification

Finite supplied certificates contrast positional/Cartesian counts, tails, empty,
per-layer nesting, ordered singleton behavior, collisions and rounding, static
versus value order, authority forgetting, and demanded versus undemanded faults.
Declarative source fragments and repository-wide consistency review cover the
integration; certificates are not executed Mud programs.
