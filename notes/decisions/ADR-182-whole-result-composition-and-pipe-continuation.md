---
id: D-182
title: Whole-result composition and pipe continuation
status: current
date: 2026-10-23
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/07-lexicon.md
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/17-dictionaries.md
  - specification/21-expressions.md
  - specification/grammar/
  - specification/syntax/
  - specification/types/
---

# ADR-182 — Whole-result composition and pipe continuation

## Decision

The author accepts >> for left-to-right and << for right-to-left pure policy
composition. Pass the upstream complete result to the downstream, including
normal empty; do not distribute across collections. Require compatible complete
contracts and retain ordinary snapshot, failure, dependency and authority rules.
Operand construction remains textual; policy application uses semantic flow.

Composition binds more tightly than brackets, so f >> g[x] applies the composed
value. Both directions share precedence and left associativity. Calls and member
access remain tighter. Following significant >> forces continuation inside the
same unit; explicit semicolons/enclosing boundaries remain separators. Joined
invalid syntax is diagnosed rather than reinterpreted as another statement.

This partially amends D-049/D-057. It adds neither shifts nor alias overloads of
composition. Static specification/certificate checks are not a runtime or a
new causal algorithm. Currification and traits are separately integrated units.
