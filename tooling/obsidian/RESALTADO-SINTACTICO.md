---
title: Resaltado sintáctico de MUD en Obsidian
aliases:
  - Coloreado sintáctico de MUD
tags:
  - mud/tooling
  - mud/obsidian
status: propuesta
verified: 2026-07-27
---

# Resaltado sintáctico de MUD en Obsidian

> [!abstract]
> Añadir un resaltado útil para bloques ` ```mud ` es sencillo. Crear un resaltador exacto, derivado de la gramática y mantenible como herramienta propia, tiene dificultad moderada. Conviene aplicar esas dos soluciones en fases.

Este documento es informativo. No define la gramática de MUD.

## Necesidad

La especificación contendrá muchos bloques:

````markdown
```mud
action Recruit for Kingdom [mut]
given
    amount: Natural
{
    then {
        soldiers += amount
    }
}
```
````

Sin una gramática registrada para `mud`, Obsidian conoce el bloque pero no puede clasificar palabras clave, tipos, literales, comentarios y operadores.

## Dos superficies de Obsidian

Obsidian utiliza CodeMirror 6 en el editor y PrismJS en el modo lectura. Un resaltador que solo atienda uno de los motores producirá resultados distintos entre edición y lectura.

Referencias:

- [Editor de Obsidian y CodeMirror](https://docs.obsidian.md/Plugins/Editor/Editor)
- [Decoraciones de editor en Obsidian](https://docs.obsidian.md/Plugins/Editor/Decorations)

## Fase 1 — Resaltado pragmático

La opción recomendada durante la formalización es una gramática de expresiones regulares cargada por un plugin existente.

Dos plugins ofrecen actualmente lenguajes personalizados mediante JSON:

- [Codeblock Customizer](https://community.obsidian.md/plugins/codeblock-customizer) permite definir `customPrismLanguages.json` y aplicar PrismJS tanto en lectura como en edición si se activa su opción correspondiente.
- [Extended Code Highlight](https://community.obsidian.md/plugins/extended-code-highlight) permite un archivo JSON por lenguaje y aplica reglas en lectura, Source y Live Preview.

Categorías iniciales:

- `comment`
- `keyword`
- `builtin`
- `class-name`
- `property`
- `string`
- `number`
- `operator`
- `punctuation`

Ventajas:

- Configuración pequeña.
- Resultado inmediato.
- Bloques Markdown normales.
- No exige terminar el parser.

Limitaciones:

- El resaltado es léxico, no semántico.
- Puede confundir un identificador con una palabra en ciertos contextos.
- Los comentarios `#...#` y `###...###` exigen patrones y prioridades cuidadosos.
- Debe actualizarse al cambiar palabras reservadas o literales.

## Fase 2 — Resaltador derivado de la gramática

Cuando la gramática concreta sea estable, MUD debería tener una herramienta propia:

1. Un parser o tokenizer compartido.
2. Integración de edición mediante CodeMirror 6.
3. Renderizado de lectura mediante PrismJS o un postprocesador equivalente.
4. Tests que relacionen tokens con casos del léxico normativo.
5. Generación o validación de las listas de palabras reservadas.

Esto evita mantener manualmente tres descripciones divergentes:

- Gramática del lenguaje.
- Lexer del compilador.
- Reglas del resaltador.

## Recomendación actual

No es necesario esperar a la gramática completa. Cuando se priorice esta tarea:

1. Instalar uno de los plugins anteriores.
2. Crear una definición provisional `mud`.
3. Versionar la fuente de esa definición en `tooling/obsidian/`.
4. Copiar o generar el archivo local bajo `.obsidian/plugins/`.
5. Probar todos los ejemplos léxicos disponibles.
6. Marcar expresamente que el resaltado no decide validez sintáctica.

La configuración local de `.obsidian/` permanece ignorada por Git. La fuente mantenible del resaltado sí debe versionarse en este directorio.

## Momento recomendado

Puede construirse un primer resaltado después de cerrar:

- El conjunto provisional de palabras reservadas.
- Literales de texto y números.
- Comentarios.
- Operadores y puntuación.

No hace falta haber formalizado acciones, ondas o tipos por completo. El resaltado inicial depende del léxico, no de toda la semántica.
