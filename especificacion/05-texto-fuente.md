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
  - "[[notas/decisiones/ADR-065-cabecera-using-de-fichero|D-065]]"
questions: []
decisions:
  - D-035
  - D-050
  - D-057
  - D-061
  - D-065
  - D-069
  - D-070
  - D-078
---

# 05. Texto fuente y estructura física

## Estado y propósito

Este capítulo define la unidad física que recibe un procesador MUD. La identidad semántica de las declaraciones se define en [[09-nombres-y-anclas]]; la estructura léxica pertenece a [[06-lexico]].

## Archivos

> [!rule] MUD-LEX-001 — Codificación
> Un archivo MUD debe estar codificado en UTF-8. Puede comenzar con un único BOM `U+FEFF`; ese carácter no puede aparecer como BOM en ninguna otra posición.

> [!rule] MUD-LEX-002 — Extensión
> Un archivo fuente ordinario debe usar la extensión `.mud`.

> [!rule] MUD-LEX-003 — Saltos
> El procesador debe reconocer `LF` y `CRLF`. También debe aceptar `CR` aislado como salto y normalizar las tres formas a un único token `NEWLINE`.

## Namespace derivado

El path de MUD de un archivo se deriva de la ruta relativa desde la raíz MUD:

```text
world/kingdoms.mud
```

pertenece al path de MUD:

```text
world
```

El nombre del archivo no forma parte del path. Un archivo situado directamente en la raíz pertenece al path raíz.

> [!rule] MUD-NAME-001 — Ruta segura
> Todo archivo debe permanecer dentro de la raíz MUD después de resolver componentes de ruta. Los nombres de directorio que forman paths de MUD deben ser identificadores `lowerCamelCase` válidos.

## Contenido

Un archivo contiene, en este orden:

1. Cero o más declaraciones `using`.
2. Cero o más declaraciones de primer nivel de cualquier categoría, incluida la declaración global `start with`.

El orden físico de archivos no es semántico. Tampoco resuelve duplicidades ni ambigüedades.

```mud
using world.people
using physics.*

thing Kingdom {
    mut title: Text
}

action Retitle for kingdom: Kingdom [mut]
given newTitle: Text {
    then kingdom.title = newTitle
}
```

> [!rule] MUD-SYN-001 — Separación superior
> Dos elementos de primer nivel deben estar separados por al menos un terminador. Los comentarios y espacios no sustituyen por sí solos ese terminador.

> [!rule] MUD-SYN-002 — Cabecera `using`
> Toda declaración `using` debe aparecer antes de cualquier declaración de primer nivel del mismo archivo. Un `using` posterior es inválido y nunca introduce alcance local.

## Identidad de fuente y procedencia

Cada archivo recibe un `SourceId` formado a partir de su ruta relativa normalizada. El `SourceId` identifica la unidad de procedencia durante una compilación; no es un ancla semántica y puede cambiar al mover el archivo.

Las posiciones sintácticas usan:

```text
SourcePosition(byteOffset, line, column)
SourceSpan(sourceId, start, end)
```

- Índices basados en cero.
- Offsets en bytes UTF-8.
- Final exclusivo.
- Columnas en valores escalares Unicode.

La conversión a posiciones UTF-16 pertenece a la frontera LSP.

## Raíces sintácticas

Cada archivo produce una CST independiente y, tras validación, un `MudFile` del AST superficial. Un `MudProject` agrega varios `MudFile`; no es una construcción escrita en un único archivo.

Para serialización estructural, los archivos de `MudProject` se ordenan por ruta relativa normalizada. Ese orden no altera la semántica.

## Metadatos físicos conservados

La CST o sus metadatos conservan:

- Presencia del BOM inicial.
- Ruta relativa normalizada.
- Namespace derivado.
- Forma física de cada salto mediante el texto de sus tokens o trivia.

El AST superficial conserva solo los metadatos necesarios para procedencia y tooling; no utiliza el BOM o el estilo de salto como significado del programa.

## Fin de archivo

El fin de archivo puede actuar como cierre de un comentario de línea o de un literal `Text` ordinario sin comilla final. No puede cerrar implícitamente:

- Paréntesis o corchetes.
- Bloques entre llaves.
- Interpolaciones de una plantilla `Text`.
- Literales o comentarios multilínea.
- Literales contextuales `Char` con las mismas comillas dobles que `Text`.
