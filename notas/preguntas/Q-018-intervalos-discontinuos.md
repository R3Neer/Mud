---
id: Q-018
title: Intervalos discontinuos
priority: P1
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-049
  - D-059
  - D-082
  - D-088
affects: []
superseded-by: []
---

# Q-018 — Intervalos discontinuos

## Contenido

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]] y [[notas/decisiones/ADR-082-cycle-como-modificador-de-dominio-de-punto|D-082]].

Los intervalos se normalizan por contenido. En los lineales, extremos efectivos invertidos producen `empty` y no implican recorrido descendente ni ciclo. `cycle` es un modificador posterior exclusivo de un dominio de punto `[a..b)`, no parte de la expresión intervalo. Permanece abierta la sintaxis consolidada de intervalos discontinuos y sus claves. D-088 cierra el recorrido descendente explícito: se expresa mediante `by` con diferencia negativa, nunca invirtiendo extremos.
