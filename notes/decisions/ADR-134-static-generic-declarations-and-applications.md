---
id: D-134
title: Static generic declarations and applications
status: current
date: 2026-10-07
supersedes: []
superseded-by: []
questions: []
affects:
  - "[[specification/10-type-system]]"
  - "[[specification/07-concrete-grammar]]"
  - "[[specification/08-abstract-syntax]]"
  - "[[specification/09-names-and-anchors]]"
  - "[[specification/19-expressions]]"
---

# ADR-134 — Static generic declarations and applications

## Context

The author accepted the supplied generic-design document, corrected its stale thing initializer examples and resolved callable categories, argument shape, variance and recursive application questions. Interval uses the generic mechanism. Standard-library scope and world-descriptor planning are resumed by [[ADR-138-standard-library-scope-and-world-descriptor|D-138]]; concrete APIs and implementation remain deferred. This extends D-096/D-115 produced-type identity and D-122 finite normalization; reciprocal current-body notes retain that provenance.

## Decision

Generic aliases, families, abstract things and actions/subactions, Boolean rules and looks/sublooks use static with parameters and nominal bounds. Header scope is joint; optional list brackets are sugar. Arguments do not directly carry outer collection shape/domain/modifiers; nominal aliases may wrap them and products may retain complete component contracts. Explicit and postfix application share stable constructor-and-exact-argument identity. Resolved arity distinguishes postfix argument tuples from one product argument. Applications create no anchors, declarations, metadata owners or world identities. Concrete things are never generic; specialisation of applied abstract things provides their canonical identity. Family members retain source anchors and applied types, including phantom distinction.

Conservatively inferred variance follows full-contract read/output and consume/input polarity, with mixed, writable, phantom or unproved cases invariant. Compatibility never erases exact nominal identity or grants authority. Static application closure must be proved finite independently of productive finite values. Generic body checking uses only bounds; callable inference requires a unique admissible solution or explicit arguments. Expected results refine only an already selected declaration. Interval is builtin arity one with its ordinary ordered-member checks.

## Consequences and verification

Canonical integration covers type contracts, expressions, nominal scopes, grammar, CST/AST and conformance evidence. The mechanical artifacts do not implement a compiler or generic solver. The source document's missing stored-field defaults become `= empty` under existing initializer policy. Existing alias recursion/nominality, family and callable variance contracts remain applicable. No standard library or alternate backend is introduced.
