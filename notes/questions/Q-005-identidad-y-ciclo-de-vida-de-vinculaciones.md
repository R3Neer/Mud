---
id: Q-005
title: Binding identity and lifecycle
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-041
  - D-045
  - D-058
  - D-099
affects: []
superseded-by: []
---

# Q-005 — Binding identity and lifecycle

## Content

How is an `on` binding identified canonically, when is its memory removed, and what happens if an equivalent binding disappears and reappears?

Status: **partially decided** by [[notes/decisions/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notes/decisions/ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]], [[notes/decisions/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]] and [[notes/decisions/ADR-099-materializaciones-frescas-tras-destroy-create|D-099]].

Temporal memory belongs to the binding; bindings are fixed at the start of each wave and additions or removals take effect in the next. A binding present in the first snapshot materialised by `start with` uses a false virtual predecessor for Boolean branches and the snapshot itself for `changes` and `old`; one created later uses its first active wave to establish the complete baseline without firing.

D-099 fixes one removal case: explicit `destroy` of a rule discards that activation's temporal memory, and a later `create` establishes a new baseline without firing merely because it was reactivated. The canonical identity of a binding, and the memory policy when it disappears through participant changes or when the rule is merely suspended by a dependency without explicit `destroy`, remain undefined.
