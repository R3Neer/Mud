---
id: D-152
title: Ordered demand and value boundaries for pruning
status: current
date: 2026-10-13
supersedes: []
superseded-by: []
questions:
  - Q-050
affects:
  - specification/21-expressions.md
  - specification/types
---

# ADR-152 — Ordered demand and value boundaries for pruning

## Decision

Boolean and/or demand their operands left to right. An ordinary decisive left Bool short-circuits the right operand. Erasure has no truth value and cannot itself decide a short circuit. A demanded erased derivation retains its independent prefix computations, in order, and their faults; an undemanded derivation performs none. Inactive call receivers and arguments remain deleted. Negation retains demanded prefix work and propagates residual erasure. These rules also apply to a demanded erased initial eventually goal; query admissibility remains independently checked and no causal search algorithm is selected.

Boolean equality, inequality and xor retain their canonical expansion and evaluate each original operand at most once, in original left-to-right order. If either is erased, both operand reads are demanded unless the first faults; the constant residual result does not discard either read's independent work. Separate source occurrences are not memoized together. Existing ordinary expansion demand remains unchanged when neither is erased.

A derived domain restriction consumes ordinary values: close residual erasure to true before filtering/checking, and the transformed result is ordinary. A type annotation or statically identical shape confirmation, including Bool [1] on an already singleton Bool, retains transparency. A value-consuming collection transformation closes erasure before operating on values. Constructing a collection closes each erased element and never deletes that member. Storage capture remains ordinary, and recovery returning an ordinary Bool does not restore original erasure.

## Examples

For an erased p carrying a division-by-zero prefix, p or true and p and false fault; true or p and false and p skip the read. Both p == q and p != q demand p then q; a fault stops further demand. With successful prefixes their residual truth values retain canonical pruning. Bare Bool and redundant Bool [1] annotations transmit erasure; Bool in [true] materializes true before restriction, so not of the resulting singleton is false. A restriction excluding true may produce empty and fail the required singleton cardinality; it never invents a value.

## Verification and provenance

Extends [[ADR-150-transparent-derived-boolean-pruning-boundaries|D-150]] and [[ADR-142-canonical-pruning-and-empty-filter-closures|D-142]]. MUD-TYPE-024/032, contrasting declarative cases and finite supplied-demand witnesses cover Q-050. They do not implement a Mud evaluator or causal runtime.
