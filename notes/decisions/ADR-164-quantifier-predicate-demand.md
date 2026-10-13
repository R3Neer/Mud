---
id: D-164
title: Quantifier predicate demand
status: current
date: 2026-10-14
supersedes: []
superseded-by: []
questions:
  - Q-079
affects:
  - specification/21-expressions.md
  - specification/22-quantifiers-and-iteration.md
  - specification/types
---

# ADR-164 — Quantifier predicate demand

## Context and acceptance

Finite quantifier result contracts did not specify which predicate instances
must be evaluated when a truth/witness result is already known. The author
accepts semantic-order short circuit for exists/forall, common-view complete
evaluation for unordered sources, and extremum-direction witness search.

## Decision

Produce, capture and validate the source and step before predicate search;
source faults cannot be hidden by a witness. All syntax remains statically
checked. For a source with usable semantic order, exists evaluates predicates
in that order until first true; forall until first false. Skipped predicate
instances contribute no reads or faults. A demanded fault stops dependent
ordered evaluation and remains recoverable under the producing block.

Without semantic order, exists/forall evaluate all predicate instances in one
view under the ordinary independent-computation error contract. A witness does
not erase a fault elsewhere, and technical hash/provenance order cannot choose
which predicates are skipped. Count examines all: sequential semantic order
where supplied, otherwise common-view independent contributions.

Min requires usable source order and searches from the first end; max searches
from the last in reverse. Each stops at its first accepted witness. This uses
an already ordered source; it does not find an arbitrary minimum without
examining unsorted input or avoid source construction/sorting costs. The body
is Bool filtering, not a minimization expression. No accepted witness gives
empty; ordinary empty-source exists/forall/count/extrema results remain unchanged.

## Evidence

MUD-ITER-004, chapter 21's interface, demand-label certificates and ordered versus
unordered fault cases cover all five quantifiers and their demand boundaries.
Use position-ordered records for divisor [1,0] examples, avoiding the misleading
assumption that a literal Int [ordered] retains reverse numeric order. Extends
D-047/D-088/D-095 and preserves D-152 demanded Boolean prefix behavior.
