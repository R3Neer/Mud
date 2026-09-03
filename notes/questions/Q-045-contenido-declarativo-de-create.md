---
id: Q-045
title: Declarative content of `create`
priority: P0
opened: 2026-07-29
resolved: true
closed: 2026-07-28
decisions:
  - D-054
affects: []
superseded-by: []
---

# Q-045 — Declarative content of `create`

## Content

Status: **closed**.

Where is the declarative content of an identity activated through `create` defined?

Current decision: [[notes/decisions/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

```mud
abstract thing B as A {
    # Single canonical definition.
}

create B
```

`create` accepts no block, category, ancestors or declarative content. The canonical definition contains all properties, constraints, defaults and ancestors. Activation merely incorporates them into the effective projection.

## Closure criterion

- C1: The accepted resolution covers the full scope stated by the question and the affected artefacts reflect that answer.

## Closure evidence

- C1: `D-054`.
