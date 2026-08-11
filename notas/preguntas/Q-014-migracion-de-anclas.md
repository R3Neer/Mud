---
id: Q-014
title: Migración de anclas
status: parcialmente-decidida
priority: P1
opened:
closed:
decisions:
  - D-072
  - D-078
affects:
  - futuro capítulo 09, compatibilidad, persistencia y tooling de renombrado
superseded-by: []
---

# Q-014 — Migración de anclas

## Pregunta

¿Cómo se renombra o mueve una declaración sin perder historia, referencias ni compatibilidad?

## Ya decidido

[[notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas|D-072]] y [[notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]] adoptan anclas legibles y una correspondencia explícita y dirigida desde el ancla anterior a la nueva. La correspondencia sirve para migrar referencias persistentes, historial y datos; no introduce un alias silencioso para compilar código fuente antiguo.

## Pendiente

- Formato y ubicación del registro de migraciones.
- Composición y aplanado de cadenas de movimientos o renombrados.
- Detección de ciclos y colisiones entre destinos.
- Periodo de conservación de entradas históricas.
- Procedimiento concreto para aplicar la migración a mundos persistidos y artefactos externos.

## Criterio de cierre

La pregunta podrá cerrarse cuando una decisión de compatibilidad y tooling fije esos cinco aspectos y exista una verificación representativa de migración encadenada y colisión.
