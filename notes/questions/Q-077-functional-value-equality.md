---
id: Q-077
title: Functional value equality
priority: P1
opened: 2026-10-14
resolved: true
closed: 2026-10-14
decisions:
  - D-162
affects:
  - specification/11-type-system.md
  - specification/13-aliases.md
  - specification/16-collections.md
  - specification/21-expressions.md
superseded-by: []
---

# Q-077 — Functional value equality

## Resolution

The author rejects value ==/!= on functional dictionaries, including comparisons
that require one transitively. Exact keys and ordinary uniqueness requiring that
comparison are also inadmissible. Other supported projected keys remain usable.
Type contract comparison remains separate. No equality of normalized policy
bodies/captures or all-input semantic equivalence is introduced.

## Closure criterion

- C1: Raw/contained functional equality and equality-requiring operations have explicit admission boundaries.
- C2: Type comparison, noncomparing operations and projected keys remain distinguished with evidence.

## Closure evidence

- C1: D-162, MUD-TYPE-040 and functional equality/key/unique cases in specification/types/typing-cases.yaml.
- C2: Chapter 11's exact normalized contract equality, projected-key cases and finite equality-path certificates in test_declaration_witnesses.py; FirstMatch mode remains unchanged.
