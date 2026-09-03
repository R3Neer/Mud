---
id: Q-025
title: Destruction of static `thing` values
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-07-28
decisions:
  - D-021
  - D-054
affects: []
superseded-by: []
---

# Q-025 — Destruction of static `thing` values

## Content

Status: **closed** by [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]] and [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

Every `thing` is defined statically and may be activated through `start with` or `create Name`. `destroy` suspends its canonical identity without deleting its anchor, descriptor, edges or payload; a later activation restores the same declaration.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-021`, `D-054`.
