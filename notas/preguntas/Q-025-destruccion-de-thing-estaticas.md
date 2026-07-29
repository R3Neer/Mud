---
id: Q-025
title: Destrucción de thing estáticas
status: cerrada
priority: P1
opened:
closed:
decisions:
  - D-021
  - D-054
affects: []
superseded-by: []
---

# Q-025 — Destrucción de `thing` estáticas

## Contenido

Estado: **cerrada** mediante [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]] y [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]].

Toda `thing` se define estáticamente y puede activarse mediante `start with` o `create Nombre`. `destroy` suspende su identidad canónica sin borrar ancla, descriptor, aristas ni carga; una activación posterior restaura la misma declaración.
