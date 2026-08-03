---
title: Resaltado sintáctico de MUD en Obsidian
aliases:
  - Coloreado sintáctico de MUD
tags:
  - mud/tooling
  - mud/obsidian
status: implementado
verified: 2026-07-29
---

# Resaltado sintáctico de MUD en Obsidian

> [!abstract]
> La bóveda incluye un plugin local configurable que colorea bloques MUD, EBNF y ASDL, abre sus archivos fuente y deriva el catálogo visual de MUD de las gramáticas normativas.

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
- El mismo registro de lenguajes y tokenizadores en ambas superficies.
- Una pestaña de ajustes para perfiles, gramáticas, validación y temas.
- Una vista común para editar directamente `.mud`, `.ebnf` y `.asdl`.

## Uso

Todo bloque con identificador `mud` se colorea automáticamente:

````markdown
```mud
ordered family Terrain {
    movementCost: Nat = 1

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
- Formas de `Text` y `Char` con comillas dobles; la distinción de tipo es contextual.
- Números exactos y `Rum`.
- Palabras reservadas, incluida `ordered`.
- Palabras contextuales inequívocas como `abstract thing` y `always rule`.
- Tipos básicos.
- Nombres de declaraciones, propiedades y llamadas.
- Operadores y puntuación.
- Formas de punto numéricas como `12:30:00`.
- Uniones de tipos, dominios escalonados, `all` e `is not`.
- Unidades adyacentes como `3m`, `90km/h` y `r0.1m`, separando número y unidad.
- Unidades cualificadas como `Length.meter` y nombres `lowerCamel` declarados tras `unit`.

Los bloques `ebnf` también se colorean automáticamente con el tokenizador
integrado de la metanotación.

Los bloques `asdl` usan el dialecto Zephyr/CPython para describir árboles de
sintaxis abstracta. El perfil registra también la extensión `.asdl`.

## Relación con la gramática

El perfil MUD analiza directamente:

- [[especificacion/gramatica/mud-lexico.ebnf]]
- [[especificacion/gramatica/mud.ebnf]]

Las categorías normativas de palabras y símbolos se declaran como producciones
EBNF y ya no se duplican en un JSON manual. Cuando cambia una de las gramáticas,
el plugin la valida y recarga; si falla, conserva la última configuración válida.

También pueden crearse perfiles genéricos indicando las dos gramáticas, sus
símbolos iniciales y el mapeo entre producciones y categorías visuales. Es una
infraestructura de resaltado léxico configurable, no un generador universal de
parsers ni un sustituto del futuro parser MUD.

## Temas

Los colores se configuran desde los ajustes del plugin, por perfil y por modo
claro u oscuro. Las plantillas disponibles son Catppuccin, Visual Studio Code
Dark+/Light+, Solarized, GitHub Default y Gruvbox. Modificar una plantilla crea
un estado personalizado que puede guardarse con nombre y reutilizarse.
`styles.css` solo contiene estructura y énfasis tipográfico.

## Límites deliberados

El color no decide si un programa es válido. En particular, no comprueba:

- Tipos o dominios.
- Resolución de participantes o nombres.
- Cardinalidad.
- Orden Unicode de los valores de `Char [* ordered]`.
- Colisiones semánticas entre formas de unidad; el resaltador reconoce su forma y el compilador resuelve la magnitud.
- Validez de un literal de punto respecto del `format` declarado; el resaltador
  reconoce la forma numérica, pero el rango y la interpretación corresponden al
  compilador.

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
8. Derivación del catálogo desde EBNF y rechazo de gramáticas inválidas.
9. Perfiles, aliases y conservación de la última configuración válida.
10. Paletas predeterminadas y reglas separadas para tema claro y oscuro.
11. Preservación de plugins durante la instalación.
12. Uniones de tipos, `all`, `is not` y dominios con `by`.
13. Unidades pegadas, cualificadas y compuestas sin confundir identificadores con dígitos ni `Rum` con `ronto`.

La instalación se preparó para Obsidian 1.12.7. Cuando Obsidian permanece abierto durante `install-local`, puede restaurar en disco su lista anterior de plugins; en ese caso debe activarse `Syntax Highlight` desde los ajustes comunitarios antes de realizar la comprobación visual definitiva.
