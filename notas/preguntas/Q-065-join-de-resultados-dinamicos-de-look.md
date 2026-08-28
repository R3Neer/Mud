---
id: Q-065
title: Join de resultados dinámicos de `look`
priority: P1
opened: 2026-08-28
resolved: false
closed:
decisions:
  - D-096
affects:
  - look, callables, tipado
superseded-by: []
---

# Q-065 — Join de resultados dinámicos de `look`

## Contenido

Definir únicamente el caso en que una invocación dinámica de `look` posee varios mínimos comunes incomparables. D-096 ya fija el uso del común más específico cuando es único y la conservación explícita de las alternativas mediante unión cuando no existe un supertipo común más informativo que esa unión; esta pregunta no reabre esas reglas.
