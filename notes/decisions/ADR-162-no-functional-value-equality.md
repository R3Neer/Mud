---
id: D-162
title: No functional value equality
status: current
date: 2026-10-14
supersedes: []
superseded-by: []
questions:
  - Q-077
affects:
  - specification/11-type-system.md
  - specification/13-aliases.md
  - specification/16-collections.md
  - specification/21-expressions.md
  - specification/types
---

# ADR-162 — No functional value equality

## Context and acceptance

Functional algebra is extensional, but neither an extensional equality oracle
nor structural/capture equality was specified. The author accepts prohibiting
value ==/!= on FunctionalDictionary and comparisons that need it transitively.

## Decision

A raw functional dictionary has no admitted value equality. Alias nominality
does not manufacture it. An alias/tuple/collection/exact dictionary comparison
that would compare a contained functional dictionary is likewise rejected.
Inspect stored representation and all possible compared static alternatives;
derived fields, family associated data and metadata are not equality payload. Unproved absence of an
unsupported compared alternative is not proof of equality support.

Functional values cannot be exact dictionary keys or ordinary unique criteria
requiring that equality. Keyed uniqueness may use another supported projected
key when its existing path/authority/stability requirements hold; that does not
create whole-functional value equality or enable whole-value collection algebra.
Automatic on binding sets and temporal changes must likewise not compare unsupported functional values. Thing identity and closed family member equality ignore ordinary fields/associated data. FirstMatch ordered policy mode, policy application and noncomparing traversal
retain their contracts. Type ===/!== remains normalized contract comparison and
does not compare policy behavior or captured values.

## Consequences and evidence

This amends the blanket equality wording for aliases/collections in D-031,
D-032/D-039 and the separate-equality placeholder in D-086; D-085 records the
functional exclusion. No new source trait, TypeKind, operator overload or
runtime identity is introduced. MUD-TYPE-040 and supplied finite equality-path
certificates distinguish functional payload, derived-only members and projected
key equality. Q-077 closes with this rule and its cases.
