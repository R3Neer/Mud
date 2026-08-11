---
id: Q-026
title: Varias acciones en eventually
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

# Q-026 — Varias acciones en `eventually`

## Contenido

Estado: **parcialmente cerrada** mediante [[notas/decisiones/ADR-044-alcanzabilidad-eventually|D-044]] y [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|D-057]].

`through` acepta una colección contextual, con corchetes opcionales, de referencias a acciones. Falta fijar el orden canónico de enumeración de solicitudes y su posible efecto en testigos y diagnósticos; no afecta a la verdad existencial.
