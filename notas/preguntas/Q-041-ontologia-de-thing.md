---
id: Q-041
title: `thing` ontology
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-28
decisions:
  - D-014
  - D-015
  - D-054
  - D-068
affects: []
superseded-by: []
---

# Q-041 — `thing` ontology

## Content

Status: **closed**.

What is the common mathematical structure of `thing` values declared and activated during execution, and what does `create` add to the world?

Decision: [[notas/decisiones/ADR-014-ontologia-unificada-de-things|ADR-014]].

MUD has one conceptual `thing` domain. Every concrete `thing` is a thing with its own identity and state that may also be an ancestor. Abstract values belong to the same domain but do not directly denote a concrete thing. D-054 specifies that programme declarations are defined canonically at the top level; `start with` or `create Name` activates them without changing identity. D-068 adds the abstract root `Thing`, above all others and with no programme-controlled lifecycle, and separates visible `name` from identity. `is` is reflexive and transitive.

The consequences were split into Q-042 and Q-043 and resolved by [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-014`, `D-015`, `D-054`, `D-068`.
