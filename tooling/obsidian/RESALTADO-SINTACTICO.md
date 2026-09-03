---
title: MUD syntax highlighting
aliases:
  - MUD syntax colouring
tags:
  - mud/tooling
  - mud/obsidian
status: implemented
verified: 2026-08-31
---

# MUD syntax highlighting

> [!abstract]
> The highlighter and formatter are an independent, reusable project. MUD
> supplies the reference language; Obsidian is only one of its adapters.

This document is informative. The normative grammar belongs to
[[especificacion/06-lexico]] and [[especificacion/07-gramatica-concreta]].

## Independent project

The source code, history and public releases are in
[R3Neer/syntax-highlight](https://github.com/R3Neer/syntax-highlight). The old
copy under `tooling/obsidian/mud-syntax/` is no longer part of this repository.

The architecture separates knowledge of the language from its consumers:

- `@r3nner/syntax-highlight-core`: language, span and editing contracts;
- `@r3nner/syntax-highlight-language-mud`: MUD tokenisation and formatting;
- `@r3nner/syntax-highlight-html`: escaped HTML and themed CSS;
- `@r3nner/syntax-highlight-codemirror`: CodeMirror 6 integration;
- `@r3nner/syntax-highlight-mcp`: resources and results for MCP Apps;
- `@r3nner/syntax-highlight-cli`: highlighting and formatting without a user interface;
- `@r3nner/syntax-highlight-obsidian`: the Obsidian adapter.

All packages are published publicly to npm under the `@r3nner` scope. The same
MUD package can therefore be used in Obsidian, CodeMirror-based applications,
servers, an MCP App or from the command line.

## Relationship with the normative grammar

The MUD package includes a validated snapshot of:

- [[especificacion/gramatica/mud-lexico.ebnf]]
- [[especificacion/gramatica/mud.ebnf]]

Words, operators and their compound forms are derived from the lexicon. The
contextual-word inference also calculates indirect grammar relationships, so
normative forms such as `~format` and `cycle` do not depend on a manually
maintained table of immediate neighbours.

After changing either grammar, check compatibility from a `syntax-highlight`
checkout:

```powershell
node scripts/check-mud-compat.mjs --mud-root "D:\OneDrive\Documentos Samuel\Herramientas software\Mud"
```

The check requires the embedded grammars to match the normative ones exactly.
Updating the published language and increasing its version belong to the
independent repository.

## Obsidian

The installed plugin uses the `syntax-highlight` identifier and is located at
`.obsidian/plugins/syntax-highlight/`. Its previous identifier was
`mud-syntax-highlighter`; its directory is kept during the migration to allow
manual recovery, but it must not remain active at the same time.

To develop or reinstall from a checkout of the independent project:

```powershell
npm ci
npm run install:obsidian -- --vault "D:\OneDrive\Documentos Samuel\Herramientas software\Mud"
```

The installer requires an explicit vault, migrates `data.json` where needed,
updates `community-plugins.json`, and does not delete the old installation.
Reload Obsidian after it has run.

The adapter provides fence highlighting in reading and editing modes, a
CodeMirror view for source files, semantic themes and smart editing. MUD, EBNF,
ASDL and TOML are available, alongside portable language profiles. Colour does
not replace the parser or validate types, domains or nominal resolution.

Since version 1.1.0, the MUD package distinguishes words by semantic function
without putting MUD knowledge into the adapters: declarations, declaration
modifiers, control flow, quantifiers, effects and clauses receive independent
categories. In particular, `mut` is a declaration modifier and both words in
`for each` are highlighted as a quantifier. Each theme can assign different
colours to these categories, and other language profiles can reuse the same
mechanism.

## Manual check

After reloading Obsidian, verify:

1. A `mud` fence in Reading view and Live Preview.
2. A `.mud` file opened in the code view.
3. Contextual highlighting of `~format` and `cycle`.
4. Compact formatting of ranges such as `[0..10]`.
5. The compound operators currently defined by the lexicon.
6. That `family`, `mut`, `for each`, `then`, `destroy` and `from` are
   distinguished according to their semantic function.
7. Preservation of migrated settings, profiles and themes.

The current stable release is available from
[v1.1.0](https://github.com/R3Neer/syntax-highlight/releases/tag/v1.1.0).
