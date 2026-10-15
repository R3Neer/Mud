---
id: D-179
title: Optional empty magnitude bodies
status: current
date: 2026-10-16
supersedes: []
superseded-by: []
questions: []
affects:
  - specification/08-concrete-grammar.md
  - specification/09-abstract-syntax.md
  - specification/19-magnitudes.md
  - specification/grammar/mud.ebnf
  - specification/syntax/mud-syntax-kinds.yaml
  - specification/syntax/cst-lossless.md
  - specification/syntax/cst-to-surface-ast.md
---

# ADR-179 — Optional empty magnitude bodies

## Context

The author requests omission of empty braces for magnitude declarations. Base
and point declarations currently require a body; derived declarations already
permit omission. Empty braces carry no quantitative information.

## Decision

A base or point magnitude may omit its body. Omission is equivalent to an
explicit empty body. A base with no body has no units or direct metadata, and
retains its independent nominal dimension. A point with no body inherits its
underlying representation and units and has no direct format metadata.
Written domains and cycle contracts remain unchanged. A declaration containing
units or direct metadata uses its ordinary braced body. Explicit empty braces
remain valid. Prefer the bodyless spelling for an empty body in authored examples.

The contextual newline rule is unchanged. Incomplete annotations, domains and
point-over headers must complete; a complete declaration before a new declaration
is separated normally. A following braced body can continue its header.

CST distinguishes omitted and written bodies losslessly. Both project to the
same Surface AST fields and retain the same nominal identity. No new AST node,
implicit unit, metadata inheritance or runtime behaviour is introduced.

## Consequences and verification

This extends the base/point source forms of the quantity and point contracts;
previous braced examples remain valid. Chapters 08, 09 and 19, concrete grammar,
CST catalogue and projection are integrated together. Finite token fixtures cover
both spellings, domains, cycles, adjacent declarations and malformed headers.
They do not implement a scanner, source parser or typechecker.
