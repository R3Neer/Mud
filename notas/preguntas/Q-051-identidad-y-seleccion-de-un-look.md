---
id: Q-051
title: Identidad y selección de un look
priority: P1
opened: 2026-07-29
resolved: true
closed: 2026-08-28
decisions:
  - D-027
  - D-061
  - D-096
affects: []
superseded-by: []
---

# Q-051 — Identidad y selección de un `look`

Estado: **resuelta** mediante [[notas/decisiones/ADR-096-modulos-callables-look-message-y-activacion|D-096]].

Un `look` es un callable puro con participantes `for` y parámetros `given`. Una llamada devuelve exactamente un objeto resultado de tipo anónimo, no una secuencia especial de filas. La vista de lectura procede del contexto de llamada: estado estable desde el host, instantánea de la rule o delta privado visible desde un `then`.

Las cuestiones que permanecen abiertas ya no son de identidad/selección básica del `look`: el join de resultados dinámicos se sigue en Q-065 y la identidad de tipos anónimos en Q-068.

## Criterio de cierre

- C1: fijar cómo se suministran participantes y parámetros de un `look`.
- C2: fijar la cardinalidad conceptual del resultado de una llamada.
- C3: fijar la vista de lectura usada por la consulta.

## Evidencia de cierre

- C1: D-096 define `look` como callable puro con `for` y `given`.
- C2: D-096 define una llamada como exactamente un objeto resultado anónimo; la multiplicidad se expresa en sus campos.
- C3: D-096 define la vista heredada del llamador: estable desde host, instantánea de rule o delta privado visible desde `then`.
