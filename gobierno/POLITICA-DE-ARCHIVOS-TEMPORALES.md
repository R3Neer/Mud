---
title: Política de archivos temporales de MUD
aliases:
  - Archivos temporales
tags:
  - mud/gobierno
  - mud/temporales
status: vigente
---

# Política de archivos temporales de MUD

## Propósito

Esta política regula los documentos que deben permanecer versionados durante varios commits porque coordinan trabajo en curso, pero que no forman parte del estado permanente del proyecto.

Un archivo efímero ordinario no se versiona. Logs, builds, caches, volcados, estado local de herramientas y demás residuos reproducibles deben vivir fuera del repositorio o quedar cubiertos por `.gitignore`.

## Fuente de verdad

El frontmatter del propio documento es la única fuente de verdad sobre su temporalidad. Un documento Markdown intencionadamente temporal usa:

```yaml
temporary: true
temporary-reason: "Motivo por el que debe permanecer versionado"
temporary-delete-when: "Condición semántica de eliminación"
temporary-delete-after: 2026-09-30
```

`temporary-delete-after` es opcional y solo se usa cuando existe una fecha límite objetiva.

No se usa `temporary: false`. Si un documento temporal pasa legítimamente a ser permanente, se eliminan `temporary` y todas las propiedades `temporary-*`. Si deja de ser necesario, se elimina el archivo.

## Significado de las propiedades

- `temporary: true`: el documento debe desaparecer eventualmente o abandonar explícitamente su ciclo temporal convirtiéndose en permanente.
- `temporary-reason`: explica por qué merece estar versionado mientras tanto. Es obligatorio y no puede estar vacío.
- `temporary-delete-when`: condición semántica obligatoria que determina cuándo debe eliminarse. Es obligatoria y no puede estar vacía.
- `temporary-delete-after`: fecha límite opcional en formato ISO `YYYY-MM-DD`. Una fecha ya vencida bloquea el commit.

Las propiedades son planas. No se mantiene un registro manual paralelo de archivos temporales.

## Alcance

El contrato `temporary:*` se aplica a documentos Markdown intencionadamente versionados. Un artefacto temporal no Markdown no se introduce en `main` mediante esta política; debe mantenerse fuera del repositorio, en una rama de laboratorio o quedar cubierto por una política específica que establezca un ciclo de vida equivalente.

## Vista de Obsidian

`[[temporales.base|gobierno/temporales.base]]` es una vista humana derivada de las Properties de las notas. No es una segunda fuente de verdad y ningún archivo se añade manualmente a ella.

La Base ofrece:

- **Temporales activos**: todos los documentos con `temporary: true`.
- **Con fecha límite**: temporales que declaran `temporary-delete-after`, ordenados por fecha.
- **Metadata incompleta**: temporales sin motivo o sin condición de eliminación.

## Validación mecánica

Desde la raíz del repositorio:

```powershell
python gobierno/validate_temporaries.py
```

El validador:

- descubre documentos Markdown versionados y no ignorados;
- imprime siempre el inventario de temporales activos;
- exige `temporary-reason` y `temporary-delete-when` no vacíos;
- rechaza `temporary: false` y propiedades `temporary-*` sin `temporary: true`;
- valida `temporary-delete-after` como fecha ISO cuando existe;
- falla si una fecha límite ya ha vencido.

El validador no intenta interpretar condiciones semánticas arbitrarias como «se complete la Etapa 8». La persona o agente que prepara el commit debe revisar el inventario impreso y decidir si alguna condición ya se cumple.

## Gate antes de cada commit

Antes de crear cualquier commit se ejecuta el validador y se revisa el inventario de `temporary: true`.

Si la condición `temporary-delete-when` de un documento ya se cumple, el documento debe eliminarse antes de cerrar el commit, salvo que el propio cambio esté modificando explícitamente su ciclo de vida. Una fecha `temporary-delete-after` vencida es un bloqueo mecánico y no puede ignorarse mediante una excepción informal.

La revisión se aplica a todos los temporales activos, no solo a los archivos modificados por el commit.
