---
id: Q-062
title: Complete grammar of `mud.part`
priority: P1
opened: 2026-08-28
resolved: true
closed: 2026-10-07
decisions:
  - D-132
  - D-096
  - D-109
affects:
  - part grammar, source text, tooling
superseded-by: []
---

# Q-062 — Complete grammar of `mud.part`

## Resolution

The local Mud manifest is minimal: zero or more exact root-relative uses statements separated by newline or semicolon. Empty files delimit parts; no grouped dependencies, wildcard/relative paths or other properties exist. Operational permission is direct and nontransitive; necessary contract-type closure is separate. Foreign dependency/version/adapter declarations are explicitly outside this local grammar and remain Q-069.

## Closure criterion

- C1: Specify syntax, separators, empty files and forbidden forms with mechanical syntax coverage.
- C2: Specify target validity and dependency permissions without claiming a foreign package protocol.

## Closure evidence

- C1: D-132, specification/grammar/mud.ebnf part-file/uses-declaration, Surface AST MudPartFile/UsesDecl and part manifest conformance cases.
- C2: D-132 and specification/05-source-text define exact manifest-bearing targets, duplicate warnings and direct uses versus transitive contract types; Q-069 retains native dependencies.
