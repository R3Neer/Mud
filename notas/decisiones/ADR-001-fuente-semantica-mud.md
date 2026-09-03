---
id: D-001
title: "`.mud` as a source semantics really"
status: current
date: 2026-07-27
supersedes: []
superseded-by: []
questions: []
affects:
  - "especificacion/01-alcance-y-conformidad.md"
  - "arquitectura de compilador, runtime y materializadores"
---

# ADR-001 — `.mud` as a source semantics really

## Context

The logic of a domain may be divided between code, data, tests,
configuration and documentation. If several of these representations can be added
taken separately, there is no source from which to reconstruct or
to audit the entire process.

## Decisión

The files `.mud` are the only source semantics on the behaviour of domain
represented by MUD. AST, IR, graphs, generated code, indexes, documentation
Derivatives and materialisations are reconstructible projections and cannot be added
rules on domain.

Decisions and the specification they govern the language in which they
are interpreted by the source, but do not form part of the state of a world MUD.

## Consequences

- An implementation must be able to reconstruct its derivatives from the source.
- Lasting meaning cannot lie solely in prompts, caches or
  manual code.
- D-011, D-051 y D-052 specify the terms of the derivatives contracts.

## Verification

Two reconstructions using the same source, version by specification and version
Compilers must preserve the same semantic distinctions.

