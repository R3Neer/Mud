---
id: Q-046
title: Creación inefectiva dentro de una raíz
status: parcialmente-decidida
priority: P0
opened: 2026-07-29
resolved:
closed:
decisions:
  - D-023
  - D-031
  - D-054
affects: []
superseded-by: []
---

# Q-046 — Creación inefectiva dentro de una raíz

## Contenido

Estado: **parcialmente decidida** mediante [[notas/decisiones/ADR-023-consolidacion-de-efectos-estructurales|D-023]] y [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

Si una regla contiene `create A` cuando la identidad canónica `A` ya está activa, la regla completa no se ejecuta y no publica ninguno de sus efectos.

Falta decidir:

- Qué resultado obtiene una acción solicitada en el mismo caso: `rejected`, `failed` u otro resultado.
- Si una regla con varias creaciones exige que todas sus identidades estén ausentes.
- Cómo se combinan creaciones de disponibilidad mixta dentro de acciones compuestas.

D-054 exige una única definición completa de primer nivel para cada `thing` y regla. Varias activaciones concurrentes de una misma identidad ausente se consolidan idempotentemente; ya no existen cuerpos ni fragmentos que fusionar. D-031 retira los aliases del sistema de `create` y `destroy`. La activación y destrucción solicitadas por `then` distintos dejan la identidad destruida al cerrar la oleada.

Bloquea la semántica operacional completa de `create`, los conjuntos de efectos y la atomicidad.
