---
id: Q-041
title: Ontología de thing
status: cerrada
priority: P0
opened:
closed:
decisions:
  - D-014
  - D-015
  - D-054
  - D-068
affects: []
superseded-by: []
---

# Q-041 — Ontología de `thing`

## Contenido

Estado: **cerrada**.

¿Cuál es la estructura matemática común de las `thing` declaradas y las activadas durante la ejecución, y qué añade `create` al mundo?

Decisión: [[notas/decisiones/ADR-014-ontologia-unificada-de-things|ADR-014]].

MUD tiene un único dominio conceptual de `thing`. Toda `thing` concreta es una cosa con identidad y estado propio que también puede ser antecesora. Las abstractas pertenecen al mismo dominio, pero no denotan directamente una cosa concreta. D-054 precisa que las declaraciones del programa se definen canónicamente en el nivel superior; `start with` o `create Nombre` las activan sin cambiar su identidad. D-068 incorpora la raíz abstracta `Thing`, superior a todas las demás y sin ciclo de vida controlable por el programa, además de separar el `name` visible de la identidad. `is` es reflexivo y transitivo.

Las consecuencias se separaron en Q-042 y Q-043 y quedaron resueltas mediante [[notas/decisiones/ADR-015-especializacion-aciclica-y-estado-independiente|ADR-015]].
