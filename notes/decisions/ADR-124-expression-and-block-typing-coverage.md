---
id: D-124
title: "Expression and block typing coverage"
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions: []
affects:
  - "[[specification/19-expressions]]"
---

# ADR-124 — Expression and block typing coverage

## Context

The static formalisation needs a contract for each existing expression constructor and for normal results versus recovery channels, without introducing new syntax.

## Decision

Chapter 19 defines synthesis/checking for literals, products, access/reflection, calls, numeric lifting, collection/dictionary algebra, domains, finite traversal, temporal/random/speculative forms and expression/value/effect blocks. It incorporates the existing per-occurrence conjunctive otherwise on, then or raise recovery and normal-result separation from Error collections. Refusal remains outside error recovery.

Coverage maps every Surface AST expression constructor to a chapter section and a declarative example. Finite derivation witnesses are mechanically evaluated where their restricted evidence language applies. Other fragments describe obligations; they are not executable compiler tests. Open numeric, binary64, pruning and termination questions retain their explicit scope and no overload is invented to conceal them.

The chapter remains proposed pending publication. Neither a parser/typechecker nor an evaluator, native adapter or serialized semantic IR is delivered by the documentation validator.

## Verification

MUD-TYPE-009 through MUD-TYPE-013, specification/types/expression-coverage.yaml and specification/types/typing-cases.yaml; validate_type_spec.py checks all current expression constructors, rule coverage and finite witness outcomes.
