---
id: Q-026
title: Multiple actions in `eventually`
priority: P2
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-044
  - D-057
affects: []
superseded-by: []
---

# Q-026 — Multiple actions in `eventually`

## Content

Status: **partially closed** by [[notes/decisions/ADR-044-alcanzabilidad-eventually|D-044]] and [[notes/decisions/ADR-057-gramatica-concreta-y-continuacion|D-057]].

`through` accepts a contextual collection, with optional square brackets, of action references. The canonical enumeration order for requests and its possible effect on witnesses and diagnostics remain to be fixed; this does not affect existential truth.
