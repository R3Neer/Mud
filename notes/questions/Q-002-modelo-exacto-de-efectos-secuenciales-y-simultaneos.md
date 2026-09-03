---
id: Q-002
title: Exact model of sequential and simultaneous effects
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-023
  - D-042
  - D-046
  - D-060
  - D-096
affects: []
superseded-by: []
---

# Q-002 — Exact model of sequential and simultaneous effects

## Content

How are the reads and consolidations of every family of effects formalised operationally within a sequential `then`, and between independent deltas of one resolution?

Status: **partially decided** by [[notes/decisions/ADR-023-consolidacion-de-efectos-estructurales|D-023]], [[notes/decisions/ADR-042-acciones-raiz-y-resultados|D-042]], [[notes/decisions/ADR-046-algebra-y-conflictos-de-efectos|D-046]], [[notes/decisions/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]] and [[notes/decisions/ADR-096-modulos-callables-look-message-y-activacion|D-096]].

D-096 establishes that there are no elementary/compound actions: each `then` is interpreted sequentially over its private delta, and an internal call observes the delta at its textual position, contributes its effects to the same resolution and leaves those effects visible to later statements. No block observes partial deltas from other independent blocks. In `Nat`, a private read projects the sum of the initial value and accumulated local delta to zero without clipping the delta itself.

The complete operational semantics of intermediate reads for the other effect families, and of their consolidation when several independent deltas run concurrently in one resolution, remains open.
