---
id: D-065
title: "Cabecera `using` de fichero"
status: vigente
date: 2026-07-30
supersedes: []
superseded-by: []
questions: []
affects:
  - "modelo de fichero, gramática concreta, parser y diagnósticos"
---
# ADR-065 — Cabecera `using` de fichero

- Modifica: [[notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas|D-035]] y [[notas/decisiones/ADR-057-gramatica-concreta-y-continuacion|D-057]]
- Documentos afectados: modelo de fichero, gramática concreta, parser y diagnósticos

## Contexto

Las declaraciones `using` poseen alcance de fichero y su posición textual no modifica la resolución. Permitirlas entre declaraciones de primer nivel sugería falsamente un alcance local o secuencial.

## Decisión

Un fichero MUD consta, en este orden, de:

1. Cero o más declaraciones `using`.
2. Cero o más declaraciones de primer nivel.

Después de la primera declaración de primer nivel no puede aparecer ningún `using`.

```mud
using world.people
using physics.*

thing Player {
    ...
}

action Move {
    ...
}
```

La restricción es sintáctica. No cambia:

- El alcance de fichero de cada `using`.
- La precedencia de resolución.
- La independencia respecto del orden textual entre varios `using`.
- La identidad o ancla de las declaraciones.

## Consecuencias

- Las herramientas pueden tratar los `using` como una cabecera física única.
- Un `using` intercalado es un error, no un cambio de alcance.
- Mover un `using` existente a la cabecera conserva el significado cuando el fichero no contenía otra ambigüedad independiente.

## Verificación

1. Fichero vacío.
2. Fichero solo con `using`.
3. Fichero solo con declaraciones.
4. Varios `using` seguidos de varias declaraciones.
5. Rechazo de un `using` posterior a la primera declaración de primer nivel.

## Modificación vigente por D-096

`using` sigue siendo una cabecera de resolución de nombres de un `.mud`. La nueva dependencia modular `uses` vive en `mud.module` y autoriza el cruce de la frontera semántica; un `using` no crea esa autorización y un `uses` no importa automáticamente todos los nombres en cada fichero.
