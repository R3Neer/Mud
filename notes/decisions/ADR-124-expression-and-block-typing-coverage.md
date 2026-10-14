---
id: D-124
title: "Expression and block typing coverage"
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions: []
affects:
  - "[[specification/21-expressions]]"
---

# ADR-124 — Expression and block typing coverage

Partially amended by [[ADR-169-explicit-values-selectors-and-foreach-comprehensions|D-169]].

## Context

The static formalisation needs a contract for each existing expression constructor and for normal results versus recovery channels, without introducing new syntax.

## Decision

Chapter 21 defines synthesis/checking for literals, products, access/reflection, calls, numeric lifting, collection/dictionary algebra, domains, finite traversal, temporal/random/speculative forms and expression/value/effect blocks. It incorporates the existing per-occurrence conjunctive otherwise on, then or raise recovery and normal-result separation from Error collections. Refusal remains outside error recovery.

Coverage maps every Surface AST expression constructor to a chapter section and a declarative example. Finite derivation witnesses are mechanically evaluated where their restricted evidence language applies. Other fragments describe obligations; they are not executable compiler tests. The integrated numeric, binary64, pruning and body-certification decisions retain their defined contracts; independently pending causal/native protocols are not inferred from this coverage.

Chapter 21 is current after its construct publication review. Neither a parser/typechecker nor an evaluator, native adapter or serialized semantic IR is delivered by the documentation validator.

## Verification

MUD-TYPE-009 through MUD-TYPE-013, specification/types/expression-coverage.yaml and specification/types/typing-cases.yaml; validate_type_spec.py checks all current expression constructors, rule coverage and finite witness outcomes.
