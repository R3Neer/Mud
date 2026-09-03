---
title: Source text and physical structure
aliases:
  - MUD Archives
tags:
  - mud/specification
  - mud/fuente
status: proposed
normative: true
depends-on:
  - "[[01-scope-and-conformance]]"
questions:
  - Q-062
decisions:
  - D-035
  - D-050
  - D-057
  - D-061
  - D-065
  - D-069
  - D-070
  - D-078
  - D-085
  - D-086
  - D-087
  - D-096
---

# 05. Source text and physical structure

## State and purpose

This chapter defines the physical unit received by a MUD processor. The identity semantics of the statements is defined in [[09-names-and-anchors]]; the lexical structure belongs to [[06-lexicon]].

## Files

> [!rule] MUD-LEX-001 — Encoding
> A MUD file must be encoded in UTF-8. It may begin with a single BOM `U+FEFF`; that character must not appear as a BOM anywhere else in the file.

> [!rule] MUD-LEX-002 — Extension
> A standard source file must use the `.mud` extension.

> [!rule] MUD-LEX-003 — Jumps
> The processor must recognise `LF` and `CRLF`. It must also accept `CR` on its own as a jump and normalise all three forms to a single token `NEWLINE`.

## Derived namespace

The path MUD for a file is derived from the relative path from the root MUD:

```text
world/kingdoms.mud
```

belongs to MUD’s path:

```text
world
```

The file name is not part of path. A file located directly within root belongs to path root.

> [!rule] MUD-NAME-001 — Path safe
> Every file must remain within the root MUD after resolving path components. Directory names that form MUD paths must be valid `lowerCamelCase` identifiers.

## Contents

A file contains, in this order:

1. Zero or more stored defaults and metadata constants `~...` applicable to the file.
2. Zero or more statements `using`.
3. Zero or more top-level declarations of any category, including `start with` of module.

The physical order of files is not semantic. Nor does it resolve duplicates or ambiguities.

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

> [!rule] MUD-SYN-001 — Top separation
> Two top-level elements must be separated by at least one terminator. Comments and spaces alone do not serve as that terminator.

> [!rule] MUD-SYN-002 — Header `using`
> Every declaration `using` must appear before any top-level declaration in the same file. A subsequent `using` is invalid and never introduces a local scope.

## Identity from the source and provenance

Each file is assigned an `SourceId` derived from its normalised relative path. The `SourceId` identifies the unit of provenance during a build; it is not an anchor semantics and may change when the file is moved.

Syntactic positions use:

```text
SourcePosition(byteOffset, line, column)
SourceSpan(sourceId, start, end)
```

- Zero-based indices.
- Offsets in UTF-8 bytes.
-  Exclusive ending.
- Columns in Unicode scalar values.

The conversion to UTF-16 positions falls within the LSP boundary.

## Syntactic roots

Each file produces an independent CST and, following validation, an `MudFile` derived from Surface AST. An `MudProject` combines several `MudFile`s; it is not a construction written in a single file.

For structural serialisation, `MudProject` files are sorted by normalised relative path. This ordering does not alter the semantics.

## Physical metadata retained

The CST or its metadata retain:

- Existence of the initial BOM.
- Path standardised relative.
- Derived namespace.
- The format of each jump, as specified by the text of its tokens or trivia.

The Surface AST retains only the metadata required for provenance and tooling; it does not use the BOM or the jump style to denote the programme’s meaning.

## End of file

The end-of-file character can act as a terminator for a line-ending comment or an ordinary literal `Text` without a closing quotation mark. It cannot implicitly terminate:

- Round brackets or square brackets.
- Blocks in curly brackets.
- Interpolations of a template `Text`.
- Multi-line literals or comments.
- Contextual literals `Char` using the same double quotation marks as `Text`.


## Recommended editorial structure

> [!note] MUD-SRC-001 — Cohesion of domain
> Files should group concepts, places, processes or situations from world rather than syntactic categories. This recommendation does not affect paths, resolution, anchors or conformance; a cross-cutting relation may occupy its own file when it better represents the domain.

For example:

```text
forest/
├── wolves.mud
└── weather.mud

village/
├── market.mud
└── guards.mud
```

An `battle.mud` file may contain `thing`, aliases, dictionaries, rules, actions, `look` and `message` which, taken together, describe a battle. Separating them solely because they belong to different syntactic categories makes it difficult to read the world as a conceptual unit.

## Modules

An `.mud` file must belong to the module determined by the `mud.module` of its nearest ancestral directory. A nested `mud.module` opens a new boundary, and an `.mud` without a modular ancestor is invalid. The logical name of the module is derived from the directory’s MudPath and need not be repeated in the module file.

`uses` is a subset of `mud.module` and permits dependencies on contract between modules; `using` belongs to the `.mud` family and resolves /importa names. Neither replaces the other. The complete grammar of `mud.module` remains open in Q-062.

Dependencies declared using `uses` may form cycles. A modular cycle is valid, but the compiler must warn of cyclic coupling. That cycle does not establish or allow the inference of an initialisation order: the `start with` contributions from the modules are materialised jointly in accordance with the model of activation.

