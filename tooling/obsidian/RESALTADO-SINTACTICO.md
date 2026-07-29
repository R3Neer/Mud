---
title: Resaltado sintáctico de MUD en Obsidian
aliases:
  - Coloreado sintáctico de MUD
tags:
  - mud/tooling
  - mud/obsidian
status: implementado
verified: 2026-07-28
---

# Resaltado sintáctico de MUD en Obsidian

> [!abstract]
> La bóveda incluye un plugin local que colorea bloques ` ```mud ` en modo lectura, Source y Live Preview mediante un único tokenizador compartido.

Este documento es informativo. La gramática normativa pertenece a [[especificacion/06-lexico]] y [[especificacion/07-gramatica-concreta]].

## Implementación

Fuente:

```text
tooling/obsidian/mud-syntax/
```

Instalación local generada:

```text
.obsidian/plugins/mud-syntax-highlighter/
```

El plugin no depende de Codeblock Customizer ni de otro plugin comunitario. Usa:

- Un procesador de bloques Markdown para el modo lectura.
- Decoraciones de CodeMirror 6 para Source y Live Preview.
- El mismo scanner en ambas superficies.

## Uso

Todo bloque con identificador `mud` se colorea automáticamente:

````markdown
```mud
ordered family Terrain {
    movementCost: Natural = 1

    Plain,
    Forest {
        movementCost = 2
    }
}
```
````

Se reconocen:

- Comentarios de línea, comentarios cerrados y bloques `###`.
- `Text` ordinario y multilínea.
- Literales `Char`.
- Números exactos y `Rumber`.
- Palabras reservadas, incluida `ordered`.
- Palabras contextuales inequívocas como `abstract thing` y `always rule`.
- Tipos básicos.
- Nombres de declaraciones, propiedades y llamadas.
- Operadores y puntuación.

## Relación con la gramática

El tokenizador sigue actualmente:

- [[especificacion/gramatica/mud-lexico.ebnf]]
- [[especificacion/06-lexico]]
- [[notas/decisiones/ADR-056-char-texto-y-orden-unicode|D-056]]

Las listas de palabras todavía se mantienen en TypeScript. Cuando exista el parser MUD, el siguiente salto de calidad será generar esas categorías desde sus tokens o reutilizar directamente su árbol.

## Límites deliberados

El color no decide si un programa es válido. En particular, no comprueba:

- Tipos o dominios.
- Resolución de participantes o nombres.
- Cardinalidad.
- Orden Unicode de los valores de `Char [* ordered]`.
- Formas dinámicas de unidad pendientes de Q-054.
- Literales contextuales `POINT_LITERAL` definidos por D-062, todavía no implementados por este resaltador.

Los términos contextuales que no puedan reconocerse con seguridad permanecen como identificadores ordinarios para evitar falsos positivos.

## Desarrollo e instalación

```powershell
cd tooling/obsidian/mud-syntax
npm install
npm run check
npm run install-local
```

`install-local` conserva los plugins ya activos y añade `mud-syntax-highlighter` una sola vez. Después de instalar o actualizar debe recargarse Obsidian.

La configuración local de `.obsidian/`, `node_modules/` y `dist/` no se versiona. La fuente, el lockfile y las pruebas sí.

## Verificación

La suite cubre:

1. Palabras reservadas, tipos, declaraciones y propiedades.
2. Posiciones de palabras contextuales.
3. Comentarios cerrados con código posterior.
4. Texto ordinario y multilínea.
5. `Char`.
6. Comentarios multilínea.
7. Fences de backticks y virgulillas.
8. Preservación de plugins durante la instalación.

La instalación se preparó para Obsidian 1.12.7. Cuando Obsidian permanece abierto durante `install-local`, puede restaurar en disco su lista anterior de plugins; en ese caso debe activarse `MUD Syntax Highlight` desde los ajustes comunitarios antes de realizar la comprobación visual definitiva.
