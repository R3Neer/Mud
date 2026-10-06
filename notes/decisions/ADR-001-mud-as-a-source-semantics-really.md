---
id: D-001
title: "`.mud` as a source semantics really"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "specification/01-scope-and-conformance.md"
  - "compiler architecture, runtime and materialisers"
---

# ADR-001 — `.mud` as a source semantics really

- Amended by: [[ADR-107-executable-language-and-rust-reference-implementation|D-107]].

## Context

The logic of a domain may be divided between code, data, tests,
configuration and documentation. If several of these representations can be added
taken separately, there is no source from which to reconstruct or
to audit the entire process.

## Decision

The `.mud` files explicitly define domain behaviour and the boundaries through which foreign code contributes to it. Reproduction requires the declared foreign sources, library versions and adapter contracts as well as the MUD source and language version. Foreign contributions must be explicit rather than hidden in generated code. AST, IR, graphs, generated code, indexes, documentation and materialisations remain reconstructible projections and cannot add undeclared domain rules.

Decisions and the specification they govern the language in which they
are interpreted by the source, but do not form part of the state of a world MUD.

## Consequences

- An implementation must be able to reconstruct its derivatives from the source.
- Lasting meaning cannot lie solely in prompts, caches or
  manual code.
- D-011, D-051 and D-052 specify the terms of the derived contracts.

## Verification

Two reconstructions using the same MUD and declared foreign sources, dependency and adapter versions, language version and conforming implementation must preserve the same semantic distinctions. Reproducibility guarantees are conditional on the declared contracts of foreign operations.

