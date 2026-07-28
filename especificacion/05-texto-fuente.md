---
title: Texto fuente y estructura física
aliases:
  - Archivos MUD
tags:
  - mud/especificacion
  - mud/fuente
status: propuesta
normative: true
depends-on:
  - "[[01-alcance-y-conformidad]]"
  - "[[notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas|D-035]]"
questions: []
decisions:
  - D-035
  - D-050
  - D-057
---

# 05. Texto fuente y estructura física

## Estado y propósito

Este capítulo define la unidad física que recibe un procesador MUD. La identidad semántica de las declaraciones se define en el futuro capítulo 09; la estructura léxica pertenece a [[06-lexico]].

## Archivos

> [!rule] MUD-LEX-001 — Codificación
> Un archivo MUD debe estar codificado en UTF-8. Puede comenzar con un único BOM `U+FEFF`; ese carácter no puede aparecer como BOM en ninguna otra posición.

> [!rule] MUD-LEX-002 — Extensión
> Un archivo fuente ordinario debe usar la extensión `.mud`.

> [!rule] MUD-LEX-003 — Saltos
> El procesador debe reconocer `LF` y `CRLF`. También debe aceptar `CR` aislado como salto y normalizar las tres formas a un único token `NEWLINE`.

## Namespace derivado

El namespace de un archivo se deriva de la ruta relativa desde la raíz MUD:

```text
world/kingdoms.mud
```

pertenece al namespace:

```text
world
```

El nombre del archivo no forma parte del namespace. Un archivo situado directamente en la raíz pertenece al namespace raíz.

> [!rule] MUD-NAME-001 — Ruta segura
> Todo archivo debe permanecer dentro de la raíz MUD después de resolver componentes de ruta. Los nombres de directorio que forman namespaces deben ser identificadores `lowerCamelCase` válidos.

## Contenido

Un archivo puede contener:

- Declaraciones `using`.
- Varias declaraciones de primer nivel de cualquier categoría.
- La declaración global `start with`.

El orden físico de archivos no es semántico. Tampoco resuelve duplicidades ni ambigüedades.

```mud
using world.people
using physics.*

thing Kingdom {
    mut name: Text
}

action Rename for kingdom: Kingdom [mut]
given newName: Text {
    then kingdom.name = newName
}
```

> [!rule] MUD-SYN-001 — Separación superior
> Dos elementos de primer nivel deben estar separados por al menos un terminador. Los comentarios y espacios no sustituyen por sí solos ese terminador.

## Fin de archivo

El fin de archivo puede actuar como cierre de un comentario de línea o de un literal `Text` ordinario sin comilla final. No puede cerrar implícitamente:

- Paréntesis o corchetes.
- Bloques entre llaves.
- Literales o comentarios multilínea.
- Literales `Character`.
