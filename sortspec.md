---
title: Orden del explorador de Obsidian
tags:
  - mud/gobierno
  - mud/obsidian
status: vigente
sorting-spec: |
  target-folder: /
  especificacion
  notas
  aprendizaje
  gobierno
  referencias
  tooling
  AGENTS
  sortspec
  ...
   < a-z

  target-folder: aprendizaje
  README
  PROGRESO
  REGLAS-DIDACTICAS
  PERFIL
  AUDITORIA-DE-VIGENCIA
  unidades
  ejercicios
  respuestas
  revisiones
  historico
  ...
   < a-z

  target-folder: gobierno
  README
  POLITICA-DE-DECISIONES
  POLITICA-DE-PREGUNTAS
  CICLO-DOCUMENTAL
  POLITICA-DE-COMMITS
  USO-DE-REPO-PATCHER
  ...
   < a-z
---

# Orden del explorador de Obsidian

Esta nota configura `Custom File Explorer sorting` solo donde existe un orden
editorial útil:

- en la raíz, primero las superficies documentales y después el soporte técnico;
- en `aprendizaje/`, primero la orientación y el progreso, después el material;
- en `gobierno/`, primero las políticas que gobiernan decisiones y preguntas.

Las carpetas de la especificación, los ADR y las preguntas conservan su orden
natural por identificador. Sus prefijos forman parte de la navegación portable
y no deben eliminarse solo para mejorar la presentación en Obsidian.

## Configuración local

El plugin se instala y activa con:

```powershell
obsidian plugin:install id=custom-sort enable
```

La configuración de `.obsidian/` no se versiona. Para evitar que dependencias y
salidas generadas contaminen las búsquedas, el vault local excluye al menos:

```text
exports/
/node_modules/
/__pycache__/
tooling/.deps/
tooling/obsidian/markdown-export/dist/
tooling/obsidian/mud-syntax/dist/
/coverage/
/.wrangler/
```
