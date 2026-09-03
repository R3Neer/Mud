---
title: MUD’s syntactic highlighting
aliases:
  - Syntax highlighting in MUDs
tags:
  - mud/tooling
  - mud/obsidian
status: implementado
verified: 2026-08-31
---

# Syntax highlighting in MUD

> [!abstract]
> The highlighter and formatter is an independent, reusable project. MUD
>  provides the reference language; Obsidian is just one of its adapters.

This document is for information purposes only. The standard grammar is set out in
[[especificacion/06-lexico]] y [[especificacion/07-gramatica-concreta]].

## Independent project

The source code, version history and public releases can be found at
[R3Neer/syntax-highlight](https://github.com/R3Neer/syntax-highlight). The copy
The former `tooling/obsidian/mud-syntax/` is no longer part of this repository.

The architecture separates knowledge from the language used by consumers:

- `@r3nner/syntax-highlight-core`: language, span and edition contracts;
- `@r3nner/syntax-highlight-language-mud`: tokenisation and MUD formatting;
- `@r3nner/syntax-highlight-html`: Escaped HTML and themed CSS;
- `@r3nner/syntax-highlight-codemirror`: integration with CodeMirror 6;
- `@r3nner/syntax-highlight-mcp`: resources and results for MCP Apps;
- `@r3nner/syntax-highlight-cli`: highlighting and formatting without an interface;
- `@r3nner/syntax-highlight-obsidian`: adapter for Obsidian.

All packages are published publicly on npm under scope `@r3nner`.
Thus, the same MUD package can be used in Obsidian, in applications based on
in CodeMirror, on servers, in an MCP App or from the command line.

## Relation in accordance with the standard grammar

The MUD package includes a validated snapshot of:

- [[especificacion/gramatica/mud-lexico.ebnf]]
- [[especificacion/gramatica/mud.ebnf]]

Words, operators and their compound forms are derived from the lexicon. The
inference for contextual words also calculates indirect relationships from the
grammar, so standard forms such as `~format` and `cycle` do not depend on
a manual table of immediate neighbours.

After modifying either of the two grammars, the
compatibility from a checkout of `syntax-highlight`:

```powershell
node scripts/check-mud-compat.mjs --mud-root "D:\OneDrive\Documentos Samuel\Herramientas software\Mud"
```

The check requires that the embedded grammars match exactly
in accordance with the regulations. Update the published text and increase its version number
corresponds to the standalone repository.

## Obsidian

The installed plugin uses the identifier `syntax-highlight` and is stored locally
in `.obsidian/plugins/syntax-highlight/`. The previous identifier was
`mud-syntax-highlighter`; its directory is retained during migration so that
allow manual recovery, but it must not be active at the same time.

To build or reinstall from a standalone project checkout:

```powershell
npm ci
npm run install:obsidian -- --vault "D:\OneDrive\Documentos Samuel\Herramientas software\Mud"
```

The installer requires an explicit vault and migrates to `data.json` where appropriate,
updates `community-plugins.json` without deleting the old installation. Afterwards
To run it, you must restart Obsidian.

The adapter provides fence highlighting during reading and editing, a view of
CodeMirror for source files, semantic themes and intelligent editing. MUD,
EBNF, ASDL and TOML are available, as well as portable language profiles.
The colour does not replace the parser, nor does it validate types, domains or nominal resolution.

From version 1.1.0 onwards, the MUD package distinguishes between words based on their function
semantics without incorporating MUD knowledge into the adaptors: declarations,
modifiers for declaration, control flow, quantifiers, effects and
These clauses are assigned separate categories. In particular, `mut` is a
The modifier for declaration and the two words in `for each` are highlighted as
quantifier. Each topic can assign different colours to these categories and
Profiles in other languages can reuse the same mechanism.

## Manual check

After reloading Obsidian, the following should be checked:

1. A block `mud` in read-only mode and in Live Preview.
2. An `.mud` file open in code view.
3. Contextual highlighting of `~format` and `cycle`.
4. The compact range format, such as `[0..10]`.
5. The compound operators currently in use in the lexicon.
6. That `family`, `mut`, `for each`, `then`, `destroy` and `from` are distinguished
   according to its function semantics.
7. Preserving settings, profiles and themes that have been migrated.

The current stable release can be downloaded from
[v1.1.0](https://github.com/R3Neer/syntax-highlight/releases/tag/v1.1.0).

