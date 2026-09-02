---
title: Orden del explorador de Obsidian
tags:
  - mud/gobierno
  - mud/obsidian
status: vigente
sorting-spec: |
  target-folder: /*
  README
  /:files. ....base
   < a-z
  sorting: standard

  target-folder: /
  README
  /:files. ....base
   < a-z
  especificacion
  notas
  gobierno
  referencias
  tooling
  AGENTS
  sortspec
  ...
   < a-z

  target-folder: gobierno
  README
  /:files. ....base
   < a-z
  POLITICA-DE-DECISIONES
  POLITICA-DE-PREGUNTAS
  CICLO-DOCUMENTAL
  POLITICA-DE-COMMITS
  ...
   < a-z
---

# Orden del explorador de Obsidian

Esta nota configura `Custom File Explorer sorting` con una regla general y dos
órdenes editoriales concretos:

- en cualquier carpeta, `README.md` aparece primero y los archivos `.base`
  inmediatamente después, ordenados alfabéticamente si hay más de uno;

- en la raíz, primero las superficies documentales y después el soporte técnico;
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
/coverage/
/.wrangler/
```
