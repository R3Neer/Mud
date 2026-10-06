---
id: D-108
title: "Considered interactive model environment"
status: current
date: 2026-10-06
supersedes: []
superseded-by: []
questions: []
affects:
  - "System architecture and considered language expansions"
---

# ADR-108 — Considered interactive model environment

- Complements: [[ADR-107-executable-language-and-rust-reference-implementation|D-107]].

## Decision

An interactive environment similar in purpose to GHCi is a desirable considered expansion: load a MUD model, interrogate it and evaluate its operations under their ordinary contracts. It is not an initial implementation commitment.

Entering an expression or operation already requests its evaluation or execution. There is no separate `:run` command. This decision does not design REPL command syntax, loading, reloading, sessions, persistence, presentation or debugger behaviour. Ordinary visibility, purity, transaction and error contracts continue to apply.

## Verification

Architecture describes the expansion without a command catalogue or new language semantics. The existing illustrative CLI is distinct from the considered interactive environment.
