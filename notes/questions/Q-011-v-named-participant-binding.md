---
id: Q-011
title: Named participant binding
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-07-30
decisions:
  - D-036
  - D-063
affects: []
superseded-by: []
---

# Q-011 — Named participant binding

## Content

Status: **closed** by [[notes/decisions/ADR-036-participants-recipients-and-calls|D-036]], amended by [[notes/decisions/ADR-063-signatures-given-and-joint-on-bindings|D-063]].

A call may use a positional receiver or a named receiver in parentheses. The named form must be exact, exhaustive and non-mixable with positional arguments: it permits no missing, repeated or unknown roles. Roles may be reordered, but the compiler suggests declaration order. `for` roles may contain values of any type; a collection occupies one position and is not expanded. A `thing` is bound by identity, an immutable value by value, and an externally mutable role by stored location. Subsequent arguments correspond exclusively to `given` parameters.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-036`, `D-063`.
