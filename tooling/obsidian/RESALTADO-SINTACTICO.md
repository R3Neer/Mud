---
title: Resaltado sintáctico de MUD
aliases:
  - Coloreado sintáctico de MUD
tags:
  - mud/tooling
  - mud/obsidian
status: implementado
verified: 2026-08-31
---

# Resaltado sintáctico de MUD

> [!abstract]
> El resaltador y formateador es un proyecto independiente y reutilizable. MUD
> aporta el lenguaje de referencia; Obsidian es solo uno de sus adaptadores.

Este documento es informativo. La gramática normativa pertenece a
[[especificacion/06-lexico]] y [[especificacion/07-gramatica-concreta]].

## Proyecto independiente

El código fuente, el historial y las releases públicas están en
[R3Neer/syntax-highlight](https://github.com/R3Neer/syntax-highlight). La copia
antigua bajo `tooling/obsidian/mud-syntax/` ya no forma parte de este repositorio.

La arquitectura separa el conocimiento del lenguaje de los consumidores:

- `@r3nner/syntax-highlight-core`: contratos de lenguajes, spans y ediciones;
- `@r3nner/syntax-highlight-language-mud`: tokenización y formato de MUD;
- `@r3nner/syntax-highlight-html`: HTML escapado y CSS temático;
- `@r3nner/syntax-highlight-codemirror`: integración con CodeMirror 6;
- `@r3nner/syntax-highlight-mcp`: recursos y resultados para MCP Apps;
- `@r3nner/syntax-highlight-cli`: resaltado y formato sin interfaz;
- `@r3nner/syntax-highlight-obsidian`: adaptador para Obsidian.

Todos los paquetes se publican públicamente en npm bajo el ámbito `@r3nner`.
Así, el mismo paquete de MUD puede usarse en Obsidian, en aplicaciones basadas
en CodeMirror, en servidores, en una MCP App o desde la línea de comandos.

## Relación con la gramática normativa

El paquete de MUD incluye una instantánea validada de:

- [[especificacion/gramatica/mud-lexico.ebnf]]
- [[especificacion/gramatica/mud.ebnf]]

Las palabras, los operadores y sus formas compuestas se derivan del léxico. La
inferencia de palabras contextuales calcula también relaciones indirectas de la
gramática, por lo que formas normativas como `~format` y `cycle` no dependen de
una tabla manual de vecinos inmediatos.

Después de modificar cualquiera de las dos gramáticas, debe comprobarse la
compatibilidad desde un checkout de `syntax-highlight`:

```powershell
node scripts/check-mud-compat.mjs --mud-root "D:\OneDrive\Documentos Samuel\Herramientas software\Mud"
```

La comprobación exige que las gramáticas incorporadas coincidan exactamente
con las normativas. Actualizar el lenguaje publicado y aumentar su versión
corresponde al repositorio independiente.

## Obsidian

El plugin instalado usa el identificador `syntax-highlight` y reside localmente
en `.obsidian/plugins/syntax-highlight/`. El identificador anterior era
`mud-syntax-highlighter`; su directorio se conserva durante la migración para
permitir recuperación manual, pero no debe quedar activo a la vez.

Para desarrollar o reinstalar desde un checkout del proyecto independiente:

```powershell
npm ci
npm run install:obsidian -- --vault "D:\OneDrive\Documentos Samuel\Herramientas software\Mud"
```

El instalador exige una bóveda explícita, migra `data.json` cuando procede,
actualiza `community-plugins.json` y no borra la instalación antigua. Después
de ejecutarlo debe recargarse Obsidian.

El adaptador ofrece resaltado de fences en lectura y edición, una vista de
CodeMirror para archivos fuente, temas semánticos y edición inteligente. MUD,
EBNF, ASDL y TOML están disponibles, además de perfiles de lenguaje portables.
El color no sustituye al parser ni valida tipos, dominios o resolución nominal.

## Comprobación manual

Después de recargar Obsidian debe verificarse:

1. Un bloque `mud` en lectura y en Live Preview.
2. Un archivo `.mud` abierto en la vista de código.
3. El resaltado contextual de `~format` y `cycle`.
4. El formato compacto de rangos como `[0..10]`.
5. Los operadores compuestos vigentes del léxico.
6. La conservación de ajustes, perfiles y temas migrados.

La release estable actual puede descargarse desde
[v1.0.0](https://github.com/R3Neer/syntax-highlight/releases/tag/v1.0.0).
