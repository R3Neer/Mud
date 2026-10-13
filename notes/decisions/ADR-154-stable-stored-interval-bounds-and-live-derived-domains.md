---
id: D-154
title: Stable stored interval bounds and live derived domains
status: current
date: 2026-10-13
supersedes: []
superseded-by: []
questions:
affects:
  - specification/08-concrete-grammar.md
  - specification/11-type-system.md
  - specification/15-fields-and-mutability.md
  - specification/21-expressions.md
  - specification/types
  - specification/README.md
---

# ADR-154 — Stable stored interval bounds and live derived domains

## Decision

An interval restricting a stored field or stored local must have bounds whose values are stable for that stored binding's lifetime. Reject a bound that directly or transitively depends on mutable state, including through calculated bindings, member reads or callable calculations. Purity and acyclicity alone do not establish stability. A stable bound need not be a literal or a globally constant expression: an already captured immutable scalar binding can supply it. Its initialization history does not become a live dependency of the bound. An immutable thing handle does not freeze mutable state reached through that handle.

Derived fields and derived locals defined with := may have dynamic interval bounds and dynamic domains. Each demanded read computes the result and its domain in the same applicable semantic view, records all transitive dependencies and applies normal filtering/normalization then cardinality obligations. A failure is not converted to empty or repaired by invented members. Already captured collection values remain ordinary captured values.

This restricts interval endpoint dependencies in stored constraints. It does not freeze domain members, prohibit all state-dependent named sets, grant authority through domains or change participant-domain rules. Existing purity, determinism, acyclicity, capability and admissibility rules continue to apply. No snapshot capture of mutable endpoints is implicit.

## Examples and consequences

A stored a: Int in [0..upper] = candidate is invalid if upper is mutable or derived from settings.limit where that field is mutable. It is valid with a supplied stable immutable integer upper and otherwise valid initialization. A derived selected: Int in [0..upper] [*] := source may observe mutable upper; later reads can filter differently. Explicitly capturing limit: Int = settings.limit in an admitted local context provides an immutable scalar bound for a subsequent stored local; it does not freeze settings.

Dynamic relational invariants over mutable endpoints need the existing explicit invariant mechanisms rather than a silently moving stored interval contract. Their causal execution remains outside this decision.

## Integration and provenance

Partially amends [[ADR-037-fields-and-declarative-domains|D-037]] and clarifies [[ADR-130-acyclic-domain-evaluation|D-130]]. MUD-TYPE-034, binding/domain prose and contrasting declarative cases cover direct/hidden mutable dependencies, stable captured bounds and dynamic derived filtering. The interval grammar and nominal HIR are unchanged; no runtime/compiler implementation is added.
